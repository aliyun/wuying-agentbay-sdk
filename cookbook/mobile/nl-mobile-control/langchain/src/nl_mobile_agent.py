#!/usr/bin/env python3
"""
Generic natural language mobile control via LangChain (LangGraph ReAct agent).

This module is intentionally app-agnostic:
- You can provide any AgentBay mobile image_id (with any apps installed)
- You can launch any app by package name (or custom start command)
- Tools expose generic UI operations: tap, swipe, input, key press, screenshot, read UI texts

The Xiaohongshu example in this directory is implemented as a preset on top of this controller.
"""

from __future__ import annotations

import asyncio
import json
import os
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional, Sequence, Tuple

import anyio
import requests
from dotenv import load_dotenv

from agentbay import AsyncAgentBay, CreateSessionParams, KeyCode


load_dotenv()


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


def _bounds_center(bounds: Any) -> Optional[Tuple[int, int]]:
    rect = _parse_bounds_rect(bounds)
    if rect is None:
        return None
    left, top, right, bottom = rect
    if right <= left or bottom <= top:
        return None
    return (left + right) // 2, (top + bottom) // 2


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
        s -= min(len(t), 500)

        rect = _parse_bounds_rect(e.get("bounds"))
        if rect is not None:
            left, top, right, bottom = rect
            area = max(0, right - left) * max(0, bottom - top)
            if area > 500_000:
                s -= 200
            if top <= 250:
                s += 20
        return s

    return max(candidates, key=score)


def _format_tool_result(payload: Dict[str, Any]) -> str:
    return json.dumps(payload, ensure_ascii=False, indent=2)


def _get_elem_strings(e: Dict[str, Any]) -> List[str]:
    """
    Extract text-like fields from a UI element dict for heuristic matching.
    """
    out: List[str] = []
    for k in ["text", "contentDescription", "contentDesc", "desc", "resourceName", "resourceId"]:
        v = e.get(k)
        if isinstance(v, str):
            t = v.strip()
            if t:
                out.append(t)
    return out


def _find_best_search_candidate(
    elements: Sequence[Dict[str, Any]],
    *,
    screen_size: Tuple[int, int],
) -> Optional[Dict[str, Any]]:
    """
    Heuristically find a search entry (search bar / magnifier icon) in the current UI.
    """
    width, height = screen_size
    if width <= 0 or height <= 0:
        width, height = (1080, 1920)

    keywords = ["搜索", "热搜", "大家都在搜", "Search", "search"]

    best: Optional[Dict[str, Any]] = None
    best_score = -10_000

    for e in _flatten_ui_elements(elements):
        rect = _parse_bounds_rect(e.get("bounds"))
        if rect is None:
            continue
        left, top, right, bottom = rect
        w = max(0, right - left)
        h = max(0, bottom - top)
        if w <= 0 or h <= 0:
            continue

        cls = e.get("className") or ""
        if not isinstance(cls, str):
            cls = ""
        cls_l = cls.lower()

        score = 0
        # Prefer top bar region (stricter).
        if top <= int(height * 0.12):
            score += 70
        elif top <= int(height * 0.18):
            score += 35
        elif top <= int(height * 0.25):
            score += 10
        else:
            score -= 10

        # Prefer right-side elements (top-right search icon/pill is very common).
        cx = (left + right) // 2
        if cx >= int(width * 0.70):
            score += 25
        elif int(width * 0.35) <= cx <= int(width * 0.65):
            score -= 10

        # Prefer plausible search bar shapes near top.
        if w >= int(width * 0.45) and h <= int(height * 0.12):
            score += 50
        if w >= int(width * 0.25) and h <= int(height * 0.10) and top <= int(height * 0.14):
            score += 25
        # Strong boost for "search pill" geometry near top-right (covers icon+placeholder pills).
        if (
            top <= int(height * 0.14)
            and right >= int(width * 0.78)
            and w >= int(width * 0.22)
            and w <= int(width * 0.70)
            and h <= int(height * 0.10)
        ):
            score += 70
        # Also allow small icon buttons in top-right.
        if w <= int(width * 0.18) and h <= int(height * 0.12):
            score += 10

        # Class-based hints.
        if "edittext" in cls_l:
            score += 70
        if "search" in cls_l:
            score += 55
        if "textview" in cls_l:
            score += 5
        if "imagebutton" in cls_l or "imageview" in cls_l:
            score += 10

        # Text/content hints.
        strings = _get_elem_strings(e)
        matched_kw = False
        for s in strings:
            for kw in keywords:
                if kw in s:
                    score += 80
                    matched_kw = True
                    break

        # Penalize huge containers (usually root).
        area = w * h
        if area > int(width * height * 0.35):
            score -= 200

        # If we have no keyword match and no class hint, be conservative.
        if not matched_kw and ("edittext" not in cls_l) and ("search" not in cls_l):
            # Penalize icon-only candidates without any semantic hint.
            if w <= int(width * 0.18):
                score -= 80
            else:
                score -= 10

        if score > best_score:
            best_score = score
            best = e

    # Only accept if we have some evidence it's a top search-ish element.
    if best is None or best_score < 55:
        return None
    return best


def _looks_like_login_screen(
    elements: Sequence[Dict[str, Any]],
    *,
    screen_size: Tuple[int, int],
) -> bool:
    """
    Heuristic detection for login/registration blocking pages when texts are obfuscated.

    We look for a very large button-like element around the middle-lower area.
    """
    width, height = screen_size
    if width <= 0 or height <= 0:
        width, height = (1080, 1920)

    for e in _flatten_ui_elements(elements):
        cls = e.get("className") or ""
        if not isinstance(cls, str):
            continue
        cls_l = cls.lower()
        if "button" not in cls_l:
            continue
        rect = _parse_bounds_rect(e.get("bounds"))
        if rect is None:
            continue
        left, top, right, bottom = rect
        w = max(0, right - left)
        h = max(0, bottom - top)
        if w <= 0 or h <= 0:
            continue
        cx = (left + right) / 2
        cy = (top + bottom) / 2
        if w >= width * 0.55 and (height * 0.40) <= cy <= (height * 0.80) and h <= height * 0.12:
            if abs(cx - (width / 2)) <= width * 0.20:
                return True
    return False


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


class MobileNLController:
    """
    A generic controller over an AgentBay mobile session.
    """

    def __init__(
        self,
        *,
        agentbay_api_key: str,
        image_id: str,
        tmp_dir: Path,
        auto_screenshot: bool = False,
    ):
        self._agentbay_api_key = agentbay_api_key
        self._image_id = image_id
        self._tmp_dir = tmp_dir
        self._client: Optional[AsyncAgentBay] = None
        self._session = None
        self._recorder = StepRecorder(tmp_dir=tmp_dir)
        self._screen_size: Optional[Tuple[int, int]] = None
        self._auto_screenshot = bool(auto_screenshot)

    @property
    def session_id(self) -> Optional[str]:
        if self._session is None:
            return None
        return getattr(self._session, "session_id", None)

    async def start(self) -> str:
        """
        Start a session (create if not already bound).

        This method is idempotent:
        - If a session is already bound (e.g. from a web UI), it will return the existing session info.
        """
        _ensure_tmp_dir(self._tmp_dir)
        if self._session is not None:
            return _format_tool_result(
                {
                    "success": True,
                    "session_id": getattr(self._session, "session_id", None),
                    "resource_url": getattr(self._session, "resource_url", None),
                    "image_id": self._image_id,
                    "mode": "bound",
                }
            )

        self._client = AsyncAgentBay(api_key=self._agentbay_api_key)
        params = CreateSessionParams(image_id=self._image_id, framework="langchain")
        session_result = await self._client.create(params)
        self._session = session_result.session
        return _format_tool_result(
            {
                "success": True,
                "session_id": self._session.session_id,
                "resource_url": getattr(self._session, "resource_url", None),
                "image_id": self._image_id,
                "mode": "created",
            }
        )

    def bind_existing_session(self, *, client: AsyncAgentBay, session: Any) -> None:
        """
        Bind an already created session (e.g. created by a web UI).

        Notes:
        - `session` should be an AsyncSession returned by `AsyncAgentBay.create()` or `AsyncAgentBay.get()`.
        - This does not create/delete resources by itself.
        """
        self._client = client
        self._session = session
        _ensure_tmp_dir(self._tmp_dir)

    def set_auto_screenshot(self, enabled: bool) -> None:
        self._auto_screenshot = bool(enabled)

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
            {"success": True, "screenshot_url": shot.data, "local_path": str(local_path)}
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

    async def launch_app_by_package(self, package: str) -> str:
        if not self._session:
            return _format_tool_result({"success": False, "error": "session_not_started"})
        package = (package or "").strip()
        if not package:
            return _format_tool_result({"success": False, "error": "package_empty"})
        cmd = f"monkey -p {package} 1"
        result = await self._session.mobile.start_app(cmd)
        if self._auto_screenshot:
            await self.screenshot_to_tmp(f"app_launched_{package}")
        return _format_tool_result(
            {
                "success": bool(result.success),
                "package": package,
                "start_cmd": cmd,
                "process_count": len(result.data or []) if result.success else None,
                "error": result.error_message if not result.success else "",
            }
        )

    async def launch_app_by_cmd(self, start_cmd: str) -> str:
        if not self._session:
            return _format_tool_result({"success": False, "error": "session_not_started"})
        start_cmd = (start_cmd or "").strip()
        if not start_cmd:
            return _format_tool_result({"success": False, "error": "start_cmd_empty"})
        result = await self._session.mobile.start_app(start_cmd)
        if self._auto_screenshot:
            await self.screenshot_to_tmp("app_launched_cmd")
        return _format_tool_result(
            {
                "success": bool(result.success),
                "start_cmd": start_cmd,
                "process_count": len(result.data or []) if result.success else None,
                "error": result.error_message if not result.success else "",
            }
        )

    async def dismiss_common_popups(self, max_rounds: int = 6) -> str:
        if not self._session:
            return _format_tool_result({"success": False, "error": "session_not_started"})

        keywords = [
            "同意",
            "同意并继续",
            "允许",
            "跳过",
            "稍后",
            "以后再说",
            "我知道了",
            "关闭",
            "取消",
            "知道了",
            "仅使用期间允许",
            "始终允许",
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
            if self._auto_screenshot:
                await self.screenshot_to_tmp(f"popup_dismiss_{picked_kw or 'popup'}")
            await asyncio.sleep(1.2)

        # Best-effort: exit blocking login / agreement pages if possible.
        try:
            tr = await self.get_visible_texts()
            obj = json.loads(tr)
            texts = obj.get("texts") or []
            joined = "\n".join([t for t in texts if isinstance(t, str)])
            login_indicators = [
                "手机号登录",
                "其他登录方式",
                "登录发现更多精彩",
                "去登录",
            ]
            if any(x in joined for x in login_indicators):
                back1 = json.loads(await self.press_key("KEYCODE_BACK"))
                tapped.append({"action": "press_back_to_exit_login", "success": back1.get("success", False)})
                await asyncio.sleep(1.0)
                tr2 = await self.get_visible_texts()
                obj2 = json.loads(tr2)
                texts2 = obj2.get("texts") or []
                joined2 = "\n".join([t for t in texts2 if isinstance(t, str)])
                if any(x in joined2 for x in login_indicators):
                    back2 = json.loads(await self.press_key("KEYCODE_BACK"))
                    tapped.append({"action": "press_back_to_exit_login_2", "success": back2.get("success", False)})
        except Exception:
            pass

        return _format_tool_result({"success": True, "tapped": tapped})

    async def tap(self, x: int, y: int) -> str:
        if not self._session:
            return _format_tool_result({"success": False, "error": "session_not_started"})
        res = await self._session.mobile.tap(int(x), int(y))
        if self._auto_screenshot:
            await self.screenshot_to_tmp("tap")
        return _format_tool_result({"success": bool(res.success), "x": int(x), "y": int(y), "error": res.error_message})

    async def tap_text(self, text_contains: str) -> str:
        """
        Find a clickable element by text substring and tap its center.
        """
        if not self._session:
            return _format_tool_result({"success": False, "error": "session_not_started"})
        needle = (text_contains or "").strip()
        if not needle:
            return _format_tool_result({"success": False, "error": "text_empty"})

        ui = await self._session.mobile.get_clickable_ui_elements(timeout_ms=5000)
        if not ui.success:
            return _format_tool_result({"success": False, "error": ui.error_message or "get_ui_failed"})

        elem = _find_best_element_by_text(ui.elements or [], text_contains=needle, prefer_button=True)
        if not elem:
            return _format_tool_result({"success": False, "error": "element_not_found", "needle": needle})

        center = _bounds_center(elem.get("bounds"))
        if not center:
            return _format_tool_result({"success": False, "error": "element_no_bounds", "needle": needle})

        x, y = center
        tap_res = await self._session.mobile.tap(x, y)
        if self._auto_screenshot:
            await self.screenshot_to_tmp(f"tap_text_{needle}")
        return _format_tool_result(
            {"success": bool(tap_res.success), "needle": needle, "x": x, "y": y, "text": elem.get("text"), "error": tap_res.error_message if not tap_res.success else ""}
        )

    async def tap_text_any(self, text_contains: str) -> str:
        """
        Find an element by text substring from ALL UI elements and tap its center.

        This is a fallback for apps that do not mark certain elements as "clickable" in the
        accessibility tree, or when `get_clickable_ui_elements` returns incomplete results.
        """
        if not self._session:
            return _format_tool_result({"success": False, "error": "session_not_started"})
        needle = (text_contains or "").strip()
        if not needle:
            return _format_tool_result({"success": False, "error": "text_empty"})

        ui = await self._session.mobile.get_all_ui_elements(timeout_ms=5000)
        if not ui.success:
            return _format_tool_result({"success": False, "error": ui.error_message or "get_ui_failed"})

        elem = _find_best_element_by_text(ui.elements or [], text_contains=needle, prefer_button=True)
        if not elem:
            return _format_tool_result({"success": False, "error": "element_not_found", "needle": needle})

        center = _bounds_center(elem.get("bounds"))
        if not center:
            return _format_tool_result({"success": False, "error": "element_no_bounds", "needle": needle})

        x, y = center
        tap_res = await self._session.mobile.tap(x, y)
        if self._auto_screenshot:
            await self.screenshot_to_tmp(f"tap_text_any_{needle}")
        return _format_tool_result(
            {"success": bool(tap_res.success), "needle": needle, "x": x, "y": y, "text": elem.get("text"), "error": tap_res.error_message if not tap_res.success else ""}
        )

    async def tap_top_right(self, x_ratio: float = 0.90, y_ratio: float = 0.06) -> str:
        """
        Tap near the top-right area using screen size ratios.

        Useful for icon-only buttons in the top bar (e.g. search) where text-based matching fails.
        """
        if not self._session:
            return _format_tool_result({"success": False, "error": "session_not_started"})
        width, height = await self._get_screen_size()
        xr = float(x_ratio)
        yr = float(y_ratio)
        xr = 0.0 if xr < 0.0 else (1.0 if xr > 1.0 else xr)
        yr = 0.0 if yr < 0.0 else (1.0 if yr > 1.0 else yr)
        x = int(width * xr)
        y = int(height * yr)
        res = await self._session.mobile.tap(x, y)
        if self._auto_screenshot:
            await self.screenshot_to_tmp("tap_top_right")
        return _format_tool_result(
            {
                "success": bool(res.success),
                "x": x,
                "y": y,
                "x_ratio": xr,
                "y_ratio": yr,
                "error": res.error_message if not res.success else "",
            }
        )

    async def open_search_entry(self, tokens: List[str]) -> str:
        """
        Best-effort open search UI for apps with icon-only or non-clickable search entries.

        Strategy (stop at first successful tap/key call):
        1) tap_text(token) for each token (clickable elements)
        2) tap_text_any(token) for each token (all elements)
        3) press_key(KEYCODE_SEARCH)
        4) tap near top center (search bar area) and top right (icon area)

        Returns a JSON payload with attempt logs.
        """
        if not self._session:
            return _format_tool_result({"success": False, "error": "session_not_started"})

        toks = [t.strip() for t in (tokens or []) if isinstance(t, str) and t.strip()]
        if not toks:
            toks = ["搜索", "热搜", "大家都在搜", "Search", "search"]

        attempts: List[Dict[str, Any]] = []

        async def looks_opened() -> bool:
            """
            Best-effort check whether a search UI is opened.
            """
            # Prefer UI-structure checks (works even if texts are obfuscated).
            ui2 = await self._session.mobile.get_all_ui_elements(timeout_ms=5000)
            if not ui2.success:
                return False
            width, height = await self._get_screen_size()
            for e in _flatten_ui_elements(ui2.elements or []):
                cls = e.get("className") or ""
                if not isinstance(cls, str):
                    continue
                cls_l = cls.lower()
                if "edittext" not in cls_l and "search" not in cls_l:
                    continue
                rect = _parse_bounds_rect(e.get("bounds"))
                if rect is None:
                    continue
                left, top, right, bottom = rect
                h = max(0, bottom - top)
                if h <= 0:
                    continue
                # Search inputs are commonly in the top area (phone login inputs are usually mid).
                if top <= int(height * 0.30):
                    return True

            # Fallback: text indicators (best-effort).
            tr = await self.get_visible_texts()
            obj = json.loads(tr)
            texts = obj.get("texts") or []
            joined = "\n".join([t for t in texts if isinstance(t, str)])
            indicators = ["取消", "清空", "搜索历史", "热搜", "大家都在搜", "搜索"]
            return any(x in joined for x in indicators)

        # 0) heuristic: try to tap a likely search entry in top bar (works for icon-only search)
        ui = await self._session.mobile.get_all_ui_elements(timeout_ms=5000)
        if ui.success and ui.elements:
            screen = await self._get_screen_size()
            if _looks_like_login_screen(ui.elements, screen_size=screen):
                back = json.loads(await self.press_key("KEYCODE_BACK"))
                attempts.append({"method": "pre_back_from_login", "result": back})
                await asyncio.sleep(1.0)
                ui = await self._session.mobile.get_all_ui_elements(timeout_ms=5000)
                if not ui.success:
                    ui = ui
            cand = _find_best_search_candidate(ui.elements, screen_size=screen)
            if cand is not None:
                center = _bounds_center(cand.get("bounds"))
                if center:
                    x, y = center
                    res = await self._session.mobile.tap(x, y)
                    payload = {"success": bool(res.success), "x": x, "y": y, "className": cand.get("className"), "text": cand.get("text"), "error": res.error_message if not res.success else ""}
                    attempts.append({"method": "heuristic_top_search", "result": payload})
                    if payload["success"]:
                        await asyncio.sleep(0.8)
                        if await looks_opened():
                            return _format_tool_result(
                                {"success": True, "method": "heuristic_top_search", "attempts": attempts}
                            )

        # 1) clickable text
        for t in toks:
            r = json.loads(await self.tap_text(t))
            attempts.append({"method": "tap_text", "token": t, "result": r})
            if r.get("success"):
                await asyncio.sleep(0.8)
                if await looks_opened():
                    return _format_tool_result(
                        {"success": True, "method": "tap_text", "token": t, "attempts": attempts}
                    )

        # 2) any element text
        for t in toks:
            r = json.loads(await self.tap_text_any(t))
            attempts.append({"method": "tap_text_any", "token": t, "result": r})
            if r.get("success"):
                await asyncio.sleep(0.8)
                if await looks_opened():
                    return _format_tool_result(
                        {"success": True, "method": "tap_text_any", "token": t, "attempts": attempts}
                    )

        # 3) hardware search
        r = json.loads(await self.press_key("KEYCODE_SEARCH"))
        attempts.append({"method": "press_key", "key": "KEYCODE_SEARCH", "result": r})
        if r.get("success"):
            await asyncio.sleep(0.8)
            if await looks_opened():
                return _format_tool_result(
                    {"success": True, "method": "press_key", "key": "KEYCODE_SEARCH", "attempts": attempts}
                )

        # 4) ratio taps (top center, then top right)
        r = json.loads(await self.tap_top_right(0.50, 0.07))
        attempts.append({"method": "tap_ratio", "pos": "top_center", "result": r})
        if r.get("success"):
            await asyncio.sleep(0.8)
            if await looks_opened():
                return _format_tool_result(
                    {"success": True, "method": "tap_ratio", "pos": "top_center", "attempts": attempts}
                )

        r = json.loads(await self.tap_top_right(0.90, 0.06))
        attempts.append({"method": "tap_ratio", "pos": "top_right", "result": r})
        if r.get("success"):
            await asyncio.sleep(0.8)
            if await looks_opened():
                return _format_tool_result(
                    {"success": True, "method": "tap_ratio", "pos": "top_right", "attempts": attempts}
                )

        return _format_tool_result({"success": False, "error": "search_entry_not_found", "attempts": attempts})

    async def swipe_direction(self, direction: str, times: int = 1) -> str:
        if not self._session:
            return _format_tool_result({"success": False, "error": "session_not_started"})
        direction = (direction or "").strip().lower()
        times = max(1, int(times))

        width, height = await self._get_screen_size()
        cx = int(width * 0.5)
        cy = int(height * 0.5)

        def points(dir_: str) -> Tuple[int, int, int, int]:
            if dir_ in {"up", "u", "scroll_up"}:
                return cx, int(height * 0.75), cx, int(height * 0.25)
            if dir_ in {"down", "d", "scroll_down"}:
                return cx, int(height * 0.25), cx, int(height * 0.75)
            if dir_ in {"left", "l"}:
                return int(width * 0.75), cy, int(width * 0.25), cy
            if dir_ in {"right", "r"}:
                return int(width * 0.25), cy, int(width * 0.75), cy
            return cx, int(height * 0.75), cx, int(height * 0.25)

        start_x, start_y, end_x, end_y = points(direction)
        ok = True
        errors: List[str] = []
        for _ in range(times):
            res = await self._session.mobile.swipe(start_x, start_y, end_x, end_y, duration_ms=350)
            ok = ok and bool(res.success)
            if not res.success and res.error_message:
                errors.append(res.error_message)
            await asyncio.sleep(0.8)
        if self._auto_screenshot:
            await self.screenshot_to_tmp(f"swipe_{direction}")
        return _format_tool_result(
            {
                "success": ok,
                "direction": direction,
                "times": times,
                "start": [start_x, start_y],
                "end": [end_x, end_y],
                "errors": errors,
            }
        )

    async def input_text(self, text: str) -> str:
        if not self._session:
            return _format_tool_result({"success": False, "error": "session_not_started"})
        res = await self._session.mobile.input_text(text)
        if self._auto_screenshot:
            await self.screenshot_to_tmp("input_text")
        return _format_tool_result(
            {"success": bool(res.success), "text_len": len(text or ""), "error": res.error_message if not res.success else ""}
        )

    async def press_key(self, key_name: str) -> str:
        if not self._session:
            return _format_tool_result({"success": False, "error": "session_not_started"})
        key_name = (key_name or "").strip().upper()
        key = getattr(KeyCode, key_name, None)
        if key is None:
            return _format_tool_result({"success": False, "error": "unknown_key", "key_name": key_name})
        res = await self._session.mobile.send_key(key)
        if self._auto_screenshot:
            await self.screenshot_to_tmp(f"key_{key_name}")
        return _format_tool_result(
            {"success": bool(res.success), "key_name": key_name, "error": res.error_message if not res.success else ""}
        )

    async def wait(self, seconds: float = 1.0) -> str:
        seconds_f = max(0.0, float(seconds))
        await asyncio.sleep(seconds_f)
        return _format_tool_result({"success": True, "seconds": seconds_f})

    async def get_visible_texts(self) -> str:
        if not self._session:
            return _format_tool_result({"success": False, "error": "session_not_started"})
        ui = await self._session.mobile.get_all_ui_elements(timeout_ms=5000)
        if not ui.success:
            return _format_tool_result({"success": False, "error": ui.error_message or "get_ui_failed"})
        texts = _extract_texts(ui.elements or [])
        return _format_tool_result({"success": True, "text_count": len(texts), "texts": texts})


def create_langchain_mobile_agent(*, controller: MobileNLController) -> Dict[str, Any]:
    """
    Create a LangGraph ReAct agent exposing generic mobile tools.
    """
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
        """Start the AgentBay mobile session. Input can be empty."""
        return await controller.start()

    @tool("stop_session")
    async def stop_session_async(_: str = "") -> str:
        """Stop and delete the AgentBay session. Input can be empty."""
        return await controller.stop()

    @tool("screenshot")
    async def screenshot_async(label: str = "") -> str:
        """Take a screenshot and download it into ./tmp. Input is a short label."""
        return await controller.screenshot_to_tmp(label or "step")

    @tool("launch_app")
    async def launch_app_async(package: str) -> str:
        """Launch an app by package name, e.g. 'com.android.settings'."""
        return await controller.launch_app_by_package(package)

    @tool("launch_app_cmd")
    async def launch_app_cmd_async(start_cmd: str) -> str:
        """Launch an app by a custom command, e.g. 'monkey -p com.android.settings 1'."""
        return await controller.launch_app_by_cmd(start_cmd)

    @tool("dismiss_popups")
    async def dismiss_async(_: str = "") -> str:
        """Best-effort dismiss common permission/pop-up dialogs. Input can be empty."""
        return await controller.dismiss_common_popups()

    @tool("tap")
    async def tap_async(x_y: str) -> str:
        """Tap at coordinates. Input format: 'x,y'."""
        m = re.findall(r"-?\\d+", x_y or "")
        if len(m) < 2:
            return _format_tool_result({"success": False, "error": "invalid_format", "expected": "x,y"})
        return await controller.tap(int(m[0]), int(m[1]))

    @tool("tap_text")
    async def tap_text_async(text_contains: str) -> str:
        """Tap a clickable element whose text contains the given substring."""
        return await controller.tap_text(text_contains)

    @tool("tap_text_any")
    async def tap_text_any_async(text_contains: str) -> str:
        """Fallback: tap an element found by text substring from ALL UI elements."""
        return await controller.tap_text_any(text_contains)

    @tool("tap_top_right")
    async def tap_top_right_async(x_y_ratio: str = "0.90,0.06") -> str:
        """
        Tap near the top-right area using ratios. Input format: 'x_ratio,y_ratio', e.g. '0.90,0.06'.
        """
        parts = [p.strip() for p in (x_y_ratio or "").split(",") if p.strip()]
        xr = float(parts[0]) if len(parts) >= 1 else 0.90
        yr = float(parts[1]) if len(parts) >= 2 else 0.06
        return await controller.tap_top_right(xr, yr)

    @tool("open_search_entry")
    async def open_search_entry_async(tokens: str = "") -> str:
        """
        Best-effort open search UI.

        Input can be empty or comma-separated tokens, e.g. "搜索,热搜,大家都在搜".
        """
        toks = [t.strip() for t in (tokens or "").split(",") if t.strip()]
        return await controller.open_search_entry(toks)

    @tool("swipe")
    async def swipe_async(direction_times: str) -> str:
        """
        Swipe in a direction. Input formats:
        - 'up' / 'down' / 'left' / 'right'
        - 'up,2' (direction,times)
        """
        parts = [p.strip() for p in (direction_times or "").split(",") if p.strip()]
        direction = parts[0] if parts else "up"
        times = int(parts[1]) if len(parts) >= 2 and parts[1].isdigit() else 1
        return await controller.swipe_direction(direction, times=times)

    @tool("input_text")
    async def input_text_async(text: str) -> str:
        """Input text into the currently focused field."""
        return await controller.input_text(text)

    @tool("press_key")
    async def press_key_async(key_name: str) -> str:
        """
        Press a key by KeyCode name, e.g. KEYCODE_ENTER / KEYCODE_BACK / KEYCODE_HOME.
        """
        return await controller.press_key(key_name)

    @tool("get_visible_texts")
    async def get_texts_async(_: str = "") -> str:
        """Get current UI texts extracted from the accessibility tree. Input can be empty."""
        return await controller.get_visible_texts()

    @tool("wait")
    async def wait_async(seconds: str = "1") -> str:
        """Wait for N seconds. Input can be '1.5'."""
        try:
            s = float(seconds)
        except Exception:
            s = 1.0
        return await controller.wait(s)

    async_tools = [
        start_session_async,
        stop_session_async,
        screenshot_async,
        launch_app_async,
        launch_app_cmd_async,
        dismiss_async,
        tap_async,
        tap_text_async,
        tap_text_any_async,
        tap_top_right_async,
        open_search_entry_async,
        swipe_async,
        input_text_async,
        press_key_async,
        get_texts_async,
        wait_async,
    ]

    agent = create_react_agent(llm, async_tools)
    return {"agent": agent, "tools": async_tools}


__all__ = [
    "MobileNLController",
    "create_langchain_mobile_agent",
]


