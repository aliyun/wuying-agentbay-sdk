from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, Iterable, List


@dataclass(frozen=True)
class PromptVariant:
    name: str
    system_prompt: str
    notes: str = ""


@dataclass(frozen=True)
class TaskScenario:
    name: str
    user_instruction: str
    expected_text_contains: List[str]


@dataclass
class RunMetrics:
    prompt_name: str
    task_name: str
    run_id: str
    success: bool
    duration_s: float
    tool_calls: int
    failed_tool_calls: int
    screenshots: int
    error: str
    final_answer: str
    found_tokens: List[str] = field(default_factory=list)
    missing_tokens: List[str] = field(default_factory=list)


def compute_smoothness_score(m: RunMetrics) -> float:
    """
    Compute a heuristic smoothness score in [0, 100].

    Interpretation:
    - Higher is better (fewer tool calls, fewer failures, faster completion).
    - Failed runs are strongly penalized.
    """
    tool_penalty = max(0.0, float(m.tool_calls)) * 1.5
    failed_penalty = max(0.0, float(m.failed_tool_calls)) * 12.0
    duration_penalty = max(0.0, float(m.duration_s)) * 0.5
    screenshot_penalty = max(0.0, float(m.screenshots)) * 0.3

    score = 100.0 - tool_penalty - failed_penalty - duration_penalty - screenshot_penalty
    if not m.success:
        score -= 30.0
    if score < 0.0:
        return 0.0
    if score > 100.0:
        return 100.0
    return score


def _avg(nums: Iterable[float]) -> float:
    xs = list(nums)
    if not xs:
        return 0.0
    return sum(xs) / len(xs)


def aggregate_results(runs: List[RunMetrics]) -> Dict[str, Any]:
    by_prompt: Dict[str, Dict[str, Any]] = {}

    for r in runs:
        p = by_prompt.setdefault(
            r.prompt_name,
            {
                "runs": 0,
                "successes": 0,
                "success_rate": 0.0,
                "avg_smoothness": 0.0,
                "avg_duration_s": 0.0,
                "avg_tool_calls": 0.0,
                "avg_failed_tool_calls": 0.0,
                "avg_screenshots": 0.0,
            },
        )
        p["runs"] += 1
        p["successes"] += 1 if r.success else 0

        p.setdefault("_smoothness", []).append(compute_smoothness_score(r))
        p.setdefault("_duration_s", []).append(float(r.duration_s))
        p.setdefault("_tool_calls", []).append(float(r.tool_calls))
        p.setdefault("_failed_tool_calls", []).append(float(r.failed_tool_calls))
        p.setdefault("_screenshots", []).append(float(r.screenshots))

    for name, p in by_prompt.items():
        runs_n = p["runs"]
        p["success_rate"] = (p["successes"] / runs_n) if runs_n else 0.0
        p["avg_smoothness"] = _avg(p.pop("_smoothness", []))
        p["avg_duration_s"] = _avg(p.pop("_duration_s", []))
        p["avg_tool_calls"] = _avg(p.pop("_tool_calls", []))
        p["avg_failed_tool_calls"] = _avg(p.pop("_failed_tool_calls", []))
        p["avg_screenshots"] = _avg(p.pop("_screenshots", []))
        by_prompt[name] = p

    return {"by_prompt": by_prompt, "runs": runs}


__all__ = [
    "PromptVariant",
    "TaskScenario",
    "RunMetrics",
    "compute_smoothness_score",
    "aggregate_results",
]



