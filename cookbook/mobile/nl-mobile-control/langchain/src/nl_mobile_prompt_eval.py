#!/usr/bin/env python3
"""
Evaluate different prompt styles for natural language mobile control.

This script runs the same task(s) under different system prompts and reports:
- Success rate (based on post-check of visible UI texts)
- Smoothness (heuristic score: fewer tool calls/failures + faster)

Outputs:
  ./tmp/nl-mobile-eval/<run_id>/
    - results.json
    - report.md
    - <prompt>/<task>/ (screenshots)
"""

from __future__ import annotations

import argparse
import json
import os
import time
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from nl_mobile_agent import MobileNLController, create_langchain_mobile_agent
from nl_mobile_eval import PromptVariant, RunMetrics, aggregate_results, compute_smoothness_score
from nl_mobile_tasks import AppTaskScenario, default_app_tasks


XHS_IMAGE_ID = "imgc-0aae4rgl3u35xrhoe"
XHS_PACKAGE = "com.xingin.xhs"


def _repo_root() -> Path:
    # .../cookbook/mobile/xiaohongshu-nl-control/async/langchain/src/<file>
    return Path(__file__).resolve().parents[6]


def _now_run_id() -> str:
    return datetime.now().strftime("%Y%m%d-%H%M%S")


def _safe_name(s: str) -> str:
    out = []
    for ch in s:
        if ch.isalnum() or ch in {"-", "_", "."}:
            out.append(ch)
        else:
            out.append("_")
    t = "".join(out).strip("_")
    return t or "run"


def _load_texts(payload_json: str) -> List[str]:
    try:
        obj = json.loads(payload_json)
    except Exception:
        return []
    texts = obj.get("texts")
    if isinstance(texts, list):
        return [t for t in texts if isinstance(t, str)]
    return []

async def _post_check_async(
    controller: MobileNLController, expected_tokens: List[str], min_found: int
) -> Tuple[bool, List[str], List[str]]:
    raw = await controller.get_visible_texts()
    texts = _load_texts(raw)
    joined = "\n".join(texts)
    if not expected_tokens:
        return True, [], []
    found = [x for x in expected_tokens if x in joined]
    missing = [x for x in expected_tokens if x not in joined]
    ok = len(found) >= max(1, int(min_found))
    return ok, found, missing


def _extract_final_answer(result: Dict[str, Any]) -> str:
    msgs = result.get("messages") or []
    if not msgs:
        return ""
    last = msgs[-1]
    return getattr(last, "content", "") or ""


def _iter_tool_messages(messages: List[Any]) -> List[Any]:
    tool_msgs: List[Any] = []
    for msg in messages:
        cls = msg.__class__.__name__
        msg_type = getattr(msg, "type", "")
        if cls == "ToolMessage" or msg_type == "tool":
            tool_msgs.append(msg)
    return tool_msgs


def _tool_name(msg: Any) -> str:
    name = getattr(msg, "name", None)
    if isinstance(name, str) and name:
        return name
    return ""


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


def _default_prompt_variants() -> List[PromptVariant]:
    return [
        PromptVariant(
            name="tool_first_concise",
            system_prompt=(
                "You are a careful mobile operator. Use the provided tools to act on the phone.\n"
                "Rules:\n"
                "- Always start with start_session.\n"
                "- Do NOT call stop_session (the runner will clean up).\n"
                "- Only call screenshot when the user asks or when you need visual evidence.\n"
                "- If a tool fails, try an alternative (tap_text vs tap vs swipe) and continue.\n"
                "- At the end, state DONE and briefly explain what you verified on screen."
            ),
            notes="Concise tool-first policy with screenshots.",
        ),
        PromptVariant(
            name="verify_each_step",
            system_prompt=(
                "You are a mobile automation agent.\n"
                "For every step: (1) decide action, (2) execute tool, (3) verify via get_visible_texts, "
                "(4) screenshot, then continue.\n"
                "Minimize redundant actions. If UI is blocked, run dismiss_popups.\n"
                "Do NOT call stop_session (the runner will clean up).\n"
                "Finish with DONE and your evidence."
            ),
            notes="Explicit verify loop (texts + screenshot).",
        ),
        PromptVariant(
            name="ui_text_driven",
            system_prompt=(
                "You operate the phone using tools.\n"
                "Always call get_visible_texts first to understand current UI, then decide next tool.\n"
                "Prefer tap_text with a unique label. Use swipe when an element may be off-screen.\n"
                "Only call screenshot when needed. Finish with DONE."
            ),
            notes="UI-text-first strategy.",
        ),
        PromptVariant(
            name="minimal_instruction_only",
            system_prompt=(
                "You can control a phone using tools. Try your best to complete the user's request.\n"
                "Do NOT call stop_session (the runner will clean up)."
            ),
            notes="Weak baseline (less structured).",
        ),
    ]


async def _run_single(
    *,
    agent: Any,
    controller: MobileNLController,
    prompt: PromptVariant,
    task: AppTaskScenario,
    run_id: str,
    recursion_limit: int,
    timeout_s: float,
) -> RunMetrics:
    start_t = time.time()
    error = ""
    final_answer = ""
    tool_calls = 0
    failed_tool_calls = 0
    screenshots = 0
    success = False
    found_tokens: List[str] = []
    missing_tokens: List[str] = []

    try:
        result = await asyncio.wait_for(
            agent.ainvoke(
                {
                    "messages": [
                        {"role": "system", "content": prompt.system_prompt},
                        {"role": "user", "content": task.user_instruction},
                    ]
                },
                {"recursion_limit": recursion_limit},
            ),
            timeout=max(1.0, float(timeout_s)),
        )
        final_answer = _extract_final_answer(result)
        msgs = result.get("messages") or []
        tool_msgs = _iter_tool_messages(msgs)
        tool_calls = len(tool_msgs)

        for tm in tool_msgs:
            name = _tool_name(tm)
            if name == "screenshot":
                screenshots += 1
            ok = _tool_success_from_content(getattr(tm, "content", None))
            if ok is False:
                failed_tool_calls += 1

        ok_ui, found_tokens, missing_tokens = await _post_check_async(
            controller, task.expected_tokens, task.min_tokens_found
        )
        success = bool(ok_ui and failed_tool_calls == 0)
        if not success:
            error = f"post_check_failed_found={found_tokens};missing={missing_tokens};failed_tool_calls={failed_tool_calls}"
    except asyncio.TimeoutError:
        error = f"timeout_after_{timeout_s}s"
        success = False
    except Exception as e:
        error = f"exception: {e}"
        success = False
    finally:
        duration_s = time.time() - start_t

    return RunMetrics(
        prompt_name=prompt.name,
        task_name=task.name,
        run_id=run_id,
        success=bool(success),
        duration_s=float(duration_s),
        tool_calls=int(tool_calls),
        failed_tool_calls=int(failed_tool_calls),
        screenshots=int(screenshots),
        error=error,
        final_answer=final_answer,
        found_tokens=found_tokens,
        missing_tokens=missing_tokens,
    )


def _render_report_md(runs: List[RunMetrics], out_dir: Path, config: Dict[str, Any]) -> str:
    summary = aggregate_results(runs)
    by_prompt = summary["by_prompt"]

    lines: List[str] = []
    lines.append("## 云手机自然语言操作 - 提示词评测报告")
    lines.append("")
    lines.append("### 配置")
    lines.append("")
    lines.append("```json")
    lines.append(json.dumps(config, ensure_ascii=False, indent=2))
    lines.append("```")
    lines.append("")
    lines.append("### 汇总（按提示词）")
    lines.append("")
    lines.append("| prompt | runs | success_rate | avg_smoothness | avg_duration_s | avg_tool_calls | avg_failed_tool_calls |")
    lines.append("|---|---:|---:|---:|---:|---:|---:|")

    for name in sorted(by_prompt.keys()):
        s = by_prompt[name]
        lines.append(
            "| {prompt} | {runs} | {sr:.2f} | {sm:.1f} | {dur:.1f} | {tc:.1f} | {ftc:.1f} |".format(
                prompt=name,
                runs=s["runs"],
                sr=s["success_rate"],
                sm=s["avg_smoothness"],
                dur=s["avg_duration_s"],
                tc=s["avg_tool_calls"],
                ftc=s["avg_failed_tool_calls"],
            )
        )

    lines.append("")
    lines.append("### 明细（每次运行）")
    lines.append("")
    lines.append("| prompt | task | success | smoothness | duration_s | tool_calls | failed_tool_calls | screenshots | error |")
    lines.append("|---|---|---:|---:|---:|---:|---:|---:|---|")
    for r in runs:
        lines.append(
            "| {p} | {t} | {s} | {sm:.1f} | {dur:.1f} | {tc} | {ftc} | {ss} | {e} |".format(
                p=r.prompt_name,
                t=r.task_name,
                s=1 if r.success else 0,
                sm=compute_smoothness_score(r),
                dur=r.duration_s,
                tc=r.tool_calls,
                ftc=r.failed_tool_calls,
                ss=r.screenshots,
                e=(r.error or "").replace("\n", " "),
            )
        )

    lines.append("")
    lines.append("### 说明")
    lines.append("")
    lines.append(
        "- 成功判定：post-check 时 UI 可见文本至少命中指定 token 的最小数量，且工具调用无失败。"
    )
    lines.append("- 流畅度：启发式分数 [0,100]，综合 tool_calls / failures / duration / screenshots。")
    lines.append("")

    report = "\n".join(lines)
    (out_dir / "report.md").write_text(report, encoding="utf-8")
    return report


def _write_incremental(out_dir: Path, runs: List[RunMetrics], config: Dict[str, Any]) -> None:
    results_path = out_dir / "results.json"
    results_path.write_text(
        json.dumps([r.__dict__ for r in runs], ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    _render_report_md(runs, out_dir, config)


async def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--image-id", default=os.getenv("MOBILE_IMAGE_ID", XHS_IMAGE_ID))
    parser.add_argument(
        "--apps",
        default=os.getenv("EVAL_APPS", "xhs,pdd,taobao,weibo"),
        help="Comma-separated: xhs,pdd,taobao,weibo",
    )
    parser.add_argument("--max-level", type=int, default=int(os.getenv("EVAL_MAX_LEVEL", "4")))
    parser.add_argument("--query", default=os.getenv("MOBILE_QUERY", "少女高颜值穿搭"))
    parser.add_argument("--runs", type=int, default=int(os.getenv("EVAL_RUNS", "1")))
    parser.add_argument("--recursion-limit", type=int, default=220)
    parser.add_argument(
        "--per-run-timeout-s",
        type=float,
        default=float(os.getenv("EVAL_PER_RUN_TIMEOUT_S", "240")),
        help="Hard timeout for a single agent run (seconds).",
    )
    parser.add_argument(
        "--prompts",
        default=os.getenv("EVAL_PROMPTS", "all"),
        help="Comma-separated prompt names to run, or 'all'.",
    )
    args = parser.parse_args()

    agentbay_api_key = os.getenv("AGENTBAY_API_KEY")
    dashscope_api_key = os.getenv("DASHSCOPE_API_KEY")
    if not agentbay_api_key:
        raise SystemExit("Error: AGENTBAY_API_KEY must be set")
    if not dashscope_api_key:
        raise SystemExit("Error: DASHSCOPE_API_KEY must be set")

    run_id = _now_run_id()
    out_dir = _repo_root() / "tmp" / "nl-mobile-eval" / run_id
    out_dir.mkdir(parents=True, exist_ok=True)

    prompts_all = _default_prompt_variants()
    prompts_sel = {x.strip() for x in (args.prompts or "").split(",") if x.strip()}
    if not prompts_sel or "all" in {p.lower() for p in prompts_sel}:
        prompts = prompts_all
    else:
        prompts = [p for p in prompts_all if p.name in prompts_sel]
        if not prompts:
            raise SystemExit(f"Unknown --prompts: {args.prompts}. Available: {[p.name for p in prompts_all]}")
    selected = {x.strip().lower() for x in (args.apps or "").split(",") if x.strip()}
    tasks_all = default_app_tasks(query_cn=args.query)
    tasks: List[AppTaskScenario] = []
    for t in tasks_all:
        app_key = t.app_name.lower()
        if app_key == "xiaohongshu":
            app_key = "xhs"
        if app_key == "pinduoduo":
            app_key = "pdd"
        if app_key == "taobao":
            app_key = "taobao"
        if app_key == "weibo":
            app_key = "weibo"
        if selected and app_key not in selected:
            continue
        if int(t.level) > int(args.max_level):
            continue
        tasks.append(t)

    all_runs: List[RunMetrics] = []

    config = {
        "run_id": run_id,
        "image_id": args.image_id,
        "apps": sorted(list(selected)),
        "max_level": args.max_level,
        "query": args.query,
        "runs_per_prompt_task": args.runs,
        "recursion_limit": args.recursion_limit,
        "per_run_timeout_s": args.per_run_timeout_s,
        "prompts": [p.name for p in prompts],
        "prompt_variants": [p.__dict__ for p in prompts],
        "tasks": [t.__dict__ for t in tasks],
    }
    _write_incremental(out_dir, all_runs, config)

    for prompt in prompts:
        for task in tasks:
            for i in range(max(1, int(args.runs))):
                sub_id = f"{prompt.name}__{task.name}__{i+1}"
                tmp_dir = out_dir / _safe_name(prompt.name) / _safe_name(task.name) / f"run_{i+1}"
                controller = MobileNLController(
                    agentbay_api_key=agentbay_api_key,
                    image_id=args.image_id,
                    tmp_dir=tmp_dir,
                )
                agent = create_langchain_mobile_agent(controller=controller)["agent"]

                try:
                    print(
                        f"[eval] prompt={prompt.name} task={task.name} "
                        f"app={task.app_name} level={task.level} run={i+1}/{args.runs} "
                        f"timeout={args.per_run_timeout_s}s",
                        flush=True,
                    )
                    m = await _run_single(
                        agent=agent,
                        controller=controller,
                        prompt=prompt,
                        task=task,
                        run_id=sub_id,
                        recursion_limit=args.recursion_limit,
                        timeout_s=args.per_run_timeout_s,
                    )
                    all_runs.append(m)
                    _write_incremental(out_dir, all_runs, config)
                finally:
                    try:
                        await controller.stop()
                    except Exception:
                        pass

    _write_incremental(out_dir, all_runs, config)
    print(f"Wrote: {out_dir}")


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())


