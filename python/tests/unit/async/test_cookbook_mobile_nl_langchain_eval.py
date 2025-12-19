from __future__ import annotations

import sys
from pathlib import Path


def _import_eval_module():
    repo_root = Path(__file__).resolve().parents[4]
    src_dir = (
        repo_root
        / "cookbook"
        / "mobile"
        / "nl-mobile-control"
        / "langchain"
        / "src"
    )
    sys.path.insert(0, str(src_dir))
    import nl_mobile_eval as m  # noqa: E402  # pyright: ignore[reportMissingImports]

    return m


def test_compute_smoothness_score_penalizes_more_steps_and_failures():
    m = _import_eval_module()

    base = m.RunMetrics(
        prompt_name="p1",
        task_name="t1",
        run_id="r1",
        success=True,
        duration_s=30.0,
        tool_calls=10,
        failed_tool_calls=0,
        screenshots=4,
        error="",
        final_answer="ok",
        found_tokens=[],
        missing_tokens=[],
    )
    s_base = m.compute_smoothness_score(base)

    worse_steps = m.RunMetrics(**{**base.__dict__, "tool_calls": 30})
    worse_failures = m.RunMetrics(**{**base.__dict__, "failed_tool_calls": 2})
    worse_duration = m.RunMetrics(**{**base.__dict__, "duration_s": 90.0})

    assert m.compute_smoothness_score(worse_steps) < s_base
    assert m.compute_smoothness_score(worse_failures) < s_base
    assert m.compute_smoothness_score(worse_duration) < s_base


def test_aggregate_results_by_prompt_outputs_success_rate_and_avg_scores():
    m = _import_eval_module()

    runs = [
        m.RunMetrics(
            prompt_name="A",
            task_name="t",
            run_id="1",
            success=True,
            duration_s=10.0,
            tool_calls=5,
            failed_tool_calls=0,
            screenshots=2,
            error="",
            final_answer="",
            found_tokens=["x"],
            missing_tokens=[],
        ),
        m.RunMetrics(
            prompt_name="A",
            task_name="t",
            run_id="2",
            success=False,
            duration_s=20.0,
            tool_calls=8,
            failed_tool_calls=1,
            screenshots=3,
            error="failed",
            final_answer="",
            found_tokens=[],
            missing_tokens=["x"],
        ),
        m.RunMetrics(
            prompt_name="B",
            task_name="t",
            run_id="1",
            success=True,
            duration_s=15.0,
            tool_calls=6,
            failed_tool_calls=0,
            screenshots=2,
            error="",
            final_answer="",
            found_tokens=["y"],
            missing_tokens=[],
        ),
    ]

    summary = m.aggregate_results(runs)
    by_prompt = summary["by_prompt"]

    assert by_prompt["A"]["runs"] == 2
    assert by_prompt["A"]["successes"] == 1
    assert by_prompt["A"]["success_rate"] == 0.5

    assert by_prompt["B"]["runs"] == 1
    assert by_prompt["B"]["success_rate"] == 1.0



