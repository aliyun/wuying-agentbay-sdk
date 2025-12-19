#!/usr/bin/env python3
"""
NL Web Mobile Control demo (FastAPI).

This demo provides:
- Create an AgentBay session and return resource_url (open in browser to view the phone)
- A simple web UI to send natural-language instructions
- A LangChain ReAct agent to execute instructions on the cloud phone
"""

from __future__ import annotations

import asyncio
import json
import os
import sys
import time
import uuid
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional

from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse


REPO_ROOT = Path(__file__).resolve().parents[3]
DEFAULT_IMAGE_ID = "imgc-0aae4rgl3u35xrhoe"

SRC_DIR = Path(__file__).resolve().parent / "langchain" / "src"
sys.path.insert(0, str(SRC_DIR))

from nl_mobile_agent import MobileNLController, create_langchain_mobile_agent  # noqa: E402  # pyright: ignore[reportMissingImports]

from agentbay import AsyncAgentBay, CreateSessionParams  # noqa: E402


def _web_index() -> str:
    html_path = Path(__file__).resolve().parent / "web" / "index.html"
    return html_path.read_text(encoding="utf-8")


def _require_env(name: str) -> str:
    v = os.getenv(name)
    if not v:
        raise HTTPException(status_code=400, detail=f"Missing env var: {name}")
    return v


def _format_tool_result(payload: Dict[str, Any]) -> str:
    return json.dumps(payload, ensure_ascii=False, indent=2)


@dataclass
class SessionState:
    session_id: str
    resource_url: str
    image_id: str
    created_at_s: float = field(default_factory=lambda: time.time())


@dataclass
class JobState:
    job_id: str
    status: str
    prompt: str
    logs: List[str] = field(default_factory=list)
    final_answer: str = ""
    error: str = ""
    started_at_s: float = field(default_factory=lambda: time.time())
    finished_at_s: float = 0.0


app = FastAPI()

_lock = asyncio.Lock()
_session: Optional[SessionState] = None
_jobs: Dict[str, JobState] = {}


@app.get("/", response_class=HTMLResponse)
async def index() -> str:
    return _web_index()


@app.get("/api/session")
async def get_session() -> Dict[str, Any]:
    if _session is None:
        return {"session_id": "", "resource_url": "", "image_id": ""}
    return {
        "session_id": _session.session_id,
        "resource_url": _session.resource_url,
        "image_id": _session.image_id,
        "created_at_s": _session.created_at_s,
    }


@app.post("/api/session/create")
async def create_session(_: Dict[str, Any]) -> Dict[str, Any]:
    """
    Create a new session. If a session already exists, returns it.
    """
    _require_env("AGENTBAY_API_KEY")
    _require_env("DASHSCOPE_API_KEY")

    async with _lock:
        global _session
        if _session is not None:
            return {
                "session_id": _session.session_id,
                "resource_url": _session.resource_url,
                "image_id": _session.image_id,
                "mode": "existing",
            }

        image_id = os.getenv("MOBILE_IMAGE_ID", DEFAULT_IMAGE_ID)
        client = AsyncAgentBay(api_key=os.environ["AGENTBAY_API_KEY"])
        params = CreateSessionParams(image_id=image_id, framework="langchain")
        res = await client.create(params)
        if not res.success or not res.session:
            raise HTTPException(status_code=500, detail=res.error_message or "create_session_failed")

        s = res.session
        _session = SessionState(
            session_id=s.session_id,
            resource_url=getattr(s, "resource_url", "") or "",
            image_id=image_id,
        )
        return {
            "session_id": _session.session_id,
            "resource_url": _session.resource_url,
            "image_id": _session.image_id,
            "mode": "created",
        }


@app.post("/api/session/delete")
async def delete_session(_: Dict[str, Any]) -> Dict[str, Any]:
    _require_env("AGENTBAY_API_KEY")
    async with _lock:
        global _session
        if _session is None:
            return {"success": True, "deleted": False}
        client = AsyncAgentBay(api_key=os.environ["AGENTBAY_API_KEY"])
        get_res = await client.get(_session.session_id)
        if get_res.success and get_res.session:
            await client.delete(get_res.session)
        _session = None
        return {"success": True, "deleted": True}


def _iter_tool_messages(messages: List[Any]) -> List[Any]:
    tool_msgs: List[Any] = []
    for msg in messages:
        cls = msg.__class__.__name__
        msg_type = getattr(msg, "type", "")
        if cls == "ToolMessage" or msg_type == "tool":
            tool_msgs.append(msg)
    return tool_msgs


def _tool_success_from_content(content: Any) -> Optional[bool]:
    if not isinstance(content, str):
        return None
    content = content.strip()
    if not content:
        return None
    try:
        obj = json.loads(content)
    except Exception:
        return None
    if isinstance(obj, dict) and isinstance(obj.get("success"), bool):
        return obj["success"]
    return None


def _extract_final_answer(result: Dict[str, Any]) -> str:
    msgs = result.get("messages") or []
    if not msgs:
        return ""
    last = msgs[-1]
    return getattr(last, "content", "") or ""


@app.post("/api/agent/run")
async def run_agent(payload: Dict[str, Any]) -> Dict[str, Any]:
    """
    Start a background job to run the agent.
    """
    prompt = (payload.get("prompt") or "").strip()
    if not prompt:
        raise HTTPException(status_code=400, detail="prompt is required")

    _require_env("AGENTBAY_API_KEY")
    _require_env("DASHSCOPE_API_KEY")

    async with _lock:
        if _session is None:
            raise HTTPException(status_code=400, detail="session not created")

        job_id = uuid.uuid4().hex[:12]
        job = JobState(job_id=job_id, status="running", prompt=prompt)
        _jobs[job_id] = job

        asyncio.create_task(_run_job(job_id))
        return {"job_id": job_id}


@app.get("/api/agent/jobs/{job_id}")
async def get_job(job_id: str) -> Dict[str, Any]:
    j = _jobs.get(job_id)
    if not j:
        raise HTTPException(status_code=404, detail="job not found")
    return {
        "job_id": j.job_id,
        "status": j.status,
        "prompt": j.prompt,
        "logs": j.logs,
        "final_answer": j.final_answer,
        "error": j.error,
        "started_at_s": j.started_at_s,
        "finished_at_s": j.finished_at_s,
    }


async def _run_job(job_id: str) -> None:
    j = _jobs[job_id]
    j.logs.append("Starting job...")

    async with _lock:
        if _session is None:
            j.status = "failed"
            j.error = "session not created"
            j.finished_at_s = time.time()
            return
        session_id = _session.session_id

    client = AsyncAgentBay(api_key=os.environ["AGENTBAY_API_KEY"])
    get_res = await client.get(session_id)
    if not get_res.success or not get_res.session:
        j.status = "failed"
        j.error = get_res.error_message or "failed_to_get_session"
        j.finished_at_s = time.time()
        return

    session = get_res.session
    tmp_dir = REPO_ROOT / "tmp" / "nl-mobile-control-web" / job_id
    controller = MobileNLController(
        agentbay_api_key=os.environ["AGENTBAY_API_KEY"],
        image_id=os.getenv("MOBILE_IMAGE_ID", DEFAULT_IMAGE_ID),
        tmp_dir=tmp_dir,
    )
    controller.bind_existing_session(client=client, session=session)
    agent = create_langchain_mobile_agent(controller=controller)["agent"]

    system_prompt = (
        "You are controlling a cloud phone. The session already exists.\n"
        "Rules:\n"
        "- Do NOT call stop_session.\n"
        "- Prefer dismiss_popups when blocked.\n"
        "- Only call screenshot when the user asks or when you need visual evidence.\n"
        "- If you need to open an app search UI, prefer open_search_entry('搜索,热搜,大家都在搜').\n"
        "  If it still fails, try press_key('KEYCODE_SEARCH') and tap_top_right('0.50,0.07') / tap_top_right('0.90,0.06').\n"
        "- If a tool fails, try an alternative (tap_text vs tap vs swipe) and continue.\n"
        "Finish with DONE and short evidence from get_visible_texts.\n"
    )

    try:
        j.logs.append(f"Using session_id={session_id}")
        result = await agent.ainvoke(
            {"messages": [{"role": "system", "content": system_prompt}, {"role": "user", "content": j.prompt}]},
            {"recursion_limit": 220},
        )
        j.final_answer = _extract_final_answer(result)

        msgs = result.get("messages") or []
        tool_msgs = _iter_tool_messages(msgs)
        failed = 0
        for tm in tool_msgs:
            name = getattr(tm, "name", "") or ""
            ok = _tool_success_from_content(getattr(tm, "content", None))
            if ok is False:
                failed += 1
            j.logs.append(f"tool[{name}] ok={ok}")

        j.logs.append(f"tool_calls={len(tool_msgs)} failed_tool_calls={failed}")
        j.status = "succeeded" if failed == 0 else "failed"
        if failed != 0:
            j.error = f"failed_tool_calls={failed}"
    except Exception as e:
        j.status = "failed"
        j.error = str(e)
    finally:
        j.finished_at_s = time.time()
        try:
            j.logs.append(_format_tool_result({"tmp_dir": str(tmp_dir)}))
        except Exception:
            pass


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000, log_level="info")


