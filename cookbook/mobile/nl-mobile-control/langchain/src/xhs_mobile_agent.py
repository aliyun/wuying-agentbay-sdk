#!/usr/bin/env python3
"""
Xiaohongshu (小红书) natural language mobile control via LangChain (LangGraph ReAct agent).

Key features:
- Create a mobile session with a custom image containing Xiaohongshu preinstalled
- Provide LangChain tools for: launching app, dismissing popups, searching, and taking step screenshots
- Download each screenshot URL to ./tmp for step-by-step inspection
"""

from __future__ import annotations

import os
import re
import json
import asyncio
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Sequence, Tuple

import anyio
import requests
from dotenv import load_dotenv

from agentbay import AsyncAgentBay, CreateSessionParams
from agentbay import KeyCode


load_dotenv()


XHS_IMAGE_ID = "imgc-0aae4rgl3u35xrhoe"
XHS_PACKAGE = "com.xingin.xhs"


def _ensure_tmp_dir(tmp_dir: Path) -> None:
    tmp_dir.mkdir(parents=True, exist_ok=True)


def _flatten_ui_elements(elements: Sequence[Dict[str, Any]]) -> List[Dict[str, Any]]:
    flat: List[Dict[str, Any]] = []

    def walk(node: Dict[str, Any]) -> None:
        flat.append(node)
        for child in node.get("children", []) or []:
            if isinstance(child, dict):
                walk(child)

    for e in elements:
        if isinstance(e, dict):
            walk(e)
    return flat


def _extract_texts(elements: Sequence[Dict[str, Any]]) -> List[str]:
    texts: List[str] = []
    for e in _flatten_ui_elements(elements):
        t = e.get("text") or ""
        if not isinstance(t, str):
            continue
        t = t.strip()
        if not t:
            continue
        texts.append(t)

    seen = set()
    deduped: List[str] = []
    for t in texts:
        if t in seen:
            continue
        seen.add(t)
        deduped.append(t)
    return deduped


def _bounds_center(bounds: Any) -> Optional[Tuple[int, int]]:
    rect = _parse_bounds_rect(bounds)
    if rect is None:
        return None
    left, top, right, bottom = rect
    if right <= left or bottom <= top:
        return None
    return (left + right) // 2, (top + bottom) // 2


def _parse_bounds_rect(bounds: Any) -> Optional[Tuple[int, int, int, int]]:
    left: Optional[int] = None
    top: Optional[int] = None
    right: Optional[int] = None
    bottom: Optional[int] = None

    if isinstance(bounds, dict):
        left = bounds.get("left")
        top = bounds.get("top")
        right = bounds.get("right")
        bottom = bounds.get("bottom")
    elif isinstance(bounds, str):
        nums = re.findall(r"-?\d+", bounds)
        if len(nums) >= 4:
            left, top, right, bottom = (int(nums[0]), int(nums[1]), int(nums[2]), int(nums[3]))
        else:
            return None
    else:
        return None
    if not all(isinstance(v, int) for v in [left, top, right, bottom]):
        return None
    return left, top, right, bottom


def _find_first_element_by_text(
    elements: Sequence[Dict[str, Any]],
    *,
    text_contains: str,
) -> Optional[Dict[str, Any]]:
    needle = (text_contains or "").strip()
    if not needle:
        return None

    for e in _flatten_ui_elements(elements):
        t = e.get("text") or ""
        if isinstance(t, str) and needle in t:
            return e
    return None


def _find_best_element_by_text(
    elements: Sequence[Dict[str, Any]],
    *,
    text_contains: str,
    prefer_button: bool = True,
) -> Optional[Dict[str, Any]]:
    needle = (text_contains or "").strip()
    if not needle:
        return None

    candidates: List[Dict[str, Any]] = []
    for e in _flatten_ui_elements(elements):
        t = e.get("text") or ""
        if isinstance(t, str) and needle in t:
            candidates.append(e)

    if not candidates:
        return None

    def score(e: Dict[str, Any]) -> int:
        t = (e.get("text") or "")
        if not isinstance(t, str):
            t = ""
        t = t.strip()
        cls = e.get("className") or ""
        if not isinstance(cls, str):
            cls = ""

        s = 0
        if prefer_button and ("Button" in cls or "button" in cls.lower()):
            s += 100
        if t == needle:
            s += 80
        if t.startswith(needle):
            s += 60
        s += 30
        # Prefer shorter text nodes (avoid huge container nodes that contain many labels)
        s -= min(len(t), 500)

        rect = _parse_bounds_rect(e.get("bounds"))
        if rect is not None:
            left, top, right, bottom = rect
            area = max(0, right - left) * max(0, bottom - top)
            # Strongly penalize very large areas (often root containers)
            if area > 500_000:
                s -= 200
            # Prefer top-bar elements for search-like interactions
            if top <= 250:
                s += 20
        return s

    return max(candidates, key=score)


def _format_tool_result(payload: Dict[str, Any]) -> str:
    return json.dumps(payload, ensure_ascii=False, indent=2)


@dataclass
class StepRecorder:
    tmp_dir: Path
    step: int = 0

    def next_path(self, label: str) -> Path:
        self.step += 1
        safe_label = re.sub(r"[^a-zA-Z0-9._-]+", "_", label).strip("_")
        if not safe_label:
            safe_label = "step"
        return self.tmp_dir / f"{self.step:04d}_{safe_label}.png"


class XhsMobileController:
    def __init__(
        self,
        *,
        agentbay_api_key: str,
        image_id: str = XHS_IMAGE_ID,
        tmp_dir: Path,
    ):
        self._agentbay_api_key = agentbay_api_key
        self._image_id = image_id
        self._tmp_dir = tmp_dir
        self._client: Optional[AsyncAgentBay] = None
        self._session = None
        self._recorder = StepRecorder(tmp_dir=tmp_dir)
        self._screen_size: Optional[Tuple[int, int]] = None

    @property
    def session_id(self) -> Optional[str]:
        if self._session is None:
            return None
        return getattr(self._session, "session_id", None)

    async def start(self) -> str:
        _ensure_tmp_dir(self._tmp_dir)
        self._client = AsyncAgentBay(api_key=self._agentbay_api_key)
        params = CreateSessionParams(
            image_id=self._image_id,
            framework="langchain",
        )
        session_result = await self._client.create(params)
        self._session = session_result.session
        return _format_tool_result(
            {
                "success": True,
                "session_id": self._session.session_id,
                "resource_url": getattr(self._session, "resource_url", None),
                "image_id": self._image_id,
            }
        )

    async def stop(self) -> str:
        if self._client and self._session:
            try:
                await self._client.delete(self._session)
            finally:
                self._session = None
        return _format_tool_result({"success": True})

    async def screenshot_to_tmp(self, label: str) -> str:
        if not self._session:
            return _format_tool_result({"success": False, "error": "session_not_started"})

        shot = await self._session.mobile.screenshot()
        if not shot.success or not shot.data:
            return _format_tool_result(
                {"success": False, "error": shot.error_message or "screenshot_failed"}
            )

        local_path = self._recorder.next_path(label)

        def _download(url: str) -> bytes:
            resp = requests.get(url, timeout=30)
            resp.raise_for_status()
            return resp.content

        try:
            content = await anyio.to_thread.run_sync(_download, shot.data)
            local_path.write_bytes(content)
        except Exception as e:
            return _format_tool_result(
                {
                    "success": False,
                    "screenshot_url": shot.data,
                    "error": f"download_failed: {e}",
                }
            )

        return _format_tool_result(
            {
                "success": True,
                "screenshot_url": shot.data,
                "local_path": str(local_path),
            }
        )

    async def _get_screen_size(self) -> Tuple[int, int]:
        if self._screen_size is not None:
            return self._screen_size
        if not self._session:
            return (1080, 1920)
        res = await self._session.command.execute_command("wm size")
        m = re.search(r"(\\d+)x(\\d+)", (res.output or ""))
        if m:
            self._screen_size = (int(m.group(1)), int(m.group(2)))
        else:
            self._screen_size = (1080, 1920)
        return self._screen_size

    async def launch_xiaohongshu(self) -> str:
        if not self._session:
            return _format_tool_result({"success": False, "error": "session_not_started"})

        cmd = f"monkey -p {XHS_PACKAGE} 1"
        result = await self._session.mobile.start_app(cmd)
        return _format_tool_result(
            {
                "success": bool(result.success),
                "start_cmd": cmd,
                "process_count": len(result.data or []) if result.success else None,
                "error": result.error_message if not result.success else "",
            }
        )

    async def dismiss_common_popups(self, max_rounds: int = 5) -> str:
        if not self._session:
            return _format_tool_result({"success": False, "error": "session_not_started"})

        keywords = [
            "同意",
            "允许",
            "跳过",
            "稍后",
            "以后再说",
            "我知道了",
            "关闭",
            "取消",
            "知道了",
            "仅使用期间允许",
        ]
        tapped: List[Dict[str, Any]] = []

        for _ in range(max_rounds):
            ui = await self._session.mobile.get_clickable_ui_elements(timeout_ms=2500)
            if not ui.success:
                break

            flat = ui.elements or []
            candidate = None
            picked_kw = None
            for kw in keywords:
                candidate = _find_best_element_by_text(flat, text_contains=kw, prefer_button=True)
                if candidate:
                    picked_kw = kw
                    break

            if not candidate:
                break

            center = _bounds_center(candidate.get("bounds"))
            if not center:
                break

            x, y = center
            tap_res = await self._session.mobile.tap(x, y)
            tapped.append(
                {
                    "keyword": picked_kw,
                    "text": candidate.get("text"),
                    "x": x,
                    "y": y,
                    "tap_success": bool(tap_res.success),
                }
            )
            await asyncio.sleep(1.5)

        return _format_tool_result({"success": True, "tapped": tapped})

    async def search(self, query: str) -> str:
        """
        Best-effort search flow:
        - Find an element containing '搜索' and tap it
        - Input query
        - Press ENTER
        - Take screenshots along the way
        """
        if not self._session:
            return _format_tool_result({"success": False, "error": "session_not_started"})

        await self.dismiss_common_popups()

        needles = ["搜索笔记", "搜索", "搜", "Search", "search"]
        tapped_search = False
        last_ui_error = ""

        for attempt in range(3):
            ui = await self._session.mobile.get_all_ui_elements(timeout_ms=5000)
            if not ui.success:
                last_ui_error = ui.error_message or "get_ui_failed"
                await asyncio.sleep(1.5)
                continue

            elem = None
            for needle in needles:
                elem = _find_best_element_by_text(ui.elements, text_contains=needle, prefer_button=True)
                if elem:
                    break

            if not elem:
                await asyncio.sleep(1.5)
                continue

            center = _bounds_center(elem.get("bounds"))
            if not center:
                await asyncio.sleep(1.5)
                continue

            x, y = center
            tap_res = await self._session.mobile.tap(x, y)
            if tap_res.success:
                tapped_search = True
                break
            await asyncio.sleep(1.5)

        if not tapped_search:
            # Fallback: tap on the top-right search pill area.
            width, height = await self._get_screen_size()
            fx = int(width * 0.90)
            fy = int(height * 0.06)
            tap_res = await self._session.mobile.tap(fx, fy)
            if tap_res.success:
                tapped_search = True
            else:
                if last_ui_error:
                    return _format_tool_result({"success": False, "error": last_ui_error})
                return _format_tool_result({"success": False, "error": "search_button_not_found"})

        input_res = await self._session.mobile.input_text(query)
        if not input_res.success:
            return _format_tool_result({"success": False, "error": input_res.error_message})

        enter_res = await self._session.mobile.send_key(KeyCode.KEYCODE_ENTER)
        if not enter_res.success:
            return _format_tool_result({"success": False, "error": enter_res.error_message})

        return _format_tool_result({"success": True, "query": query})

    async def get_visible_texts(self) -> str:
        if not self._session:
            return _format_tool_result({"success": False, "error": "session_not_started"})

        ui = await self._session.mobile.get_all_ui_elements(timeout_ms=4000)
        if not ui.success:
            return _format_tool_result({"success": False, "error": ui.error_message})

        texts = _extract_texts(ui.elements)
        return _format_tool_result({"success": True, "text_count": len(texts), "texts": texts})


def create_xhs_langchain_agent(*, controller: XhsMobileController) -> Dict[str, Any]:
    # Import LangChain-related dependencies lazily so unit tests can run in restricted sandboxes
    # without triggering SSL/cert loading side-effects at import time.
    from langchain_core.tools import tool
    from langchain_openai import ChatOpenAI
    from langgraph.prebuilt import create_react_agent

    llm = ChatOpenAI(
        api_key=os.getenv("DASHSCOPE_API_KEY"),
        base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
        model=os.getenv("DASHSCOPE_MODEL", "qwen3-max"),
    )

    @tool("start_session")
    async def start_session_async(_: str = "") -> str:
        """Start the AgentBay mobile session (custom image with Xiaohongshu). Input can be empty."""
        return await controller.start()

    @tool("stop_session")
    async def stop_session_async(_: str = "") -> str:
        """Stop and delete the AgentBay session. Input can be empty."""
        return await controller.stop()

    @tool("screenshot")
    async def screenshot_async(label: str = "") -> str:
        """Take a screenshot and download it into ./tmp. Input is a short label, e.g. 'after_open'."""
        return await controller.screenshot_to_tmp(label or "step")

    @tool("launch_xiaohongshu")
    async def launch_xhs_async(_: str = "") -> str:
        """Launch Xiaohongshu app. Input can be empty."""
        return await controller.launch_xiaohongshu()

    @tool("dismiss_popups")
    async def dismiss_async(_: str = "") -> str:
        """Try to dismiss common permission/pop-up dialogs by clicking on keywords like '允许/同意/跳过'. Input can be empty."""
        return await controller.dismiss_common_popups()

    @tool("search_xiaohongshu")
    async def search_async(query: str) -> str:
        """Search in Xiaohongshu. Input is the search query text."""
        return await controller.search(query)

    @tool("get_visible_texts")
    async def get_texts_async(_: str = "") -> str:
        """Get current UI texts extracted from the accessibility tree. Input can be empty."""
        return await controller.get_visible_texts()

    async_tools = [
        start_session_async,
        stop_session_async,
        screenshot_async,
        launch_xhs_async,
        dismiss_async,
        search_async,
        get_texts_async,
    ]

    agent = create_react_agent(llm, async_tools)
    return {"agent": agent, "tools": async_tools}


__all__ = [
    "XhsMobileController",
    "create_xhs_langchain_agent",
    "_extract_texts",
    "_flatten_ui_elements",
    "_find_first_element_by_text",
    "_find_best_element_by_text",
    "_bounds_center",
]


