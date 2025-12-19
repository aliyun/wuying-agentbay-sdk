"""Integration tests for Mobile UI elements bounds_rect normalization (no mocks)."""

from __future__ import annotations

import os
import re
from typing import Any, Dict, Optional, Tuple

import pytest
import pytest_asyncio

from agentbay import AsyncAgentBay, CreateSessionParams


def _parse_bounds_rect(bounds: Any) -> Optional[Tuple[int, int, int, int]]:
    if bounds is None:
        return None
    if isinstance(bounds, dict):
        left = bounds.get("left")
        top = bounds.get("top")
        right = bounds.get("right")
        bottom = bounds.get("bottom")
        if all(isinstance(v, int) for v in [left, top, right, bottom]):
            return int(left), int(top), int(right), int(bottom)
        return None
    if isinstance(bounds, str):
        nums = re.findall(r"-?\d+", bounds)
        if len(nums) >= 4:
            return int(nums[0]), int(nums[1]), int(nums[2]), int(nums[3])
        return None
    return None


@pytest_asyncio.fixture(scope="module")
async def agent_bay():
    api_key = os.environ.get("AGENTBAY_API_KEY")
    if not api_key:
        pytest.skip("AGENTBAY_API_KEY environment variable not set")
    return AsyncAgentBay(api_key=api_key)


@pytest_asyncio.fixture
async def session(agent_bay):
    session_param = CreateSessionParams(image_id="mobile_latest")
    result = await agent_bay.create(session_param)
    assert result.success, f"Failed to create session: {result.error_message}"
    s = result.session
    yield s
    await s.delete()


@pytest.mark.asyncio
@pytest.mark.integration
async def test_clickable_ui_elements_bounds_rect_contract(session):
    ui = await session.mobile.get_clickable_ui_elements(timeout_ms=5000)
    assert ui.success, f"get_clickable_ui_elements failed: {ui.error_message}"
    assert isinstance(ui.elements, list)
    assert len(ui.elements) > 0

    for e in ui.elements[:50]:
        assert "bounds_rect" in e, "bounds_rect must exist for compatibility evolution"
        rect = _parse_bounds_rect(e.get("bounds"))
        if rect is None:
            assert e.get("bounds_rect") is None
            continue
        assert isinstance(e.get("bounds_rect"), dict)
        br = e["bounds_rect"]
        assert all(k in br for k in ["left", "top", "right", "bottom"])
        assert all(isinstance(br[k], int) for k in ["left", "top", "right", "bottom"])
        assert (br["left"], br["top"], br["right"], br["bottom"]) == rect


@pytest.mark.asyncio
@pytest.mark.integration
async def test_all_ui_elements_bounds_rect_contract(session):
    ui = await session.mobile.get_all_ui_elements(timeout_ms=8000)
    assert ui.success, f"get_all_ui_elements failed: {ui.error_message}"
    assert isinstance(ui.elements, list)
    assert len(ui.elements) > 0

    for e in ui.elements[:20]:
        assert "bounds_rect" in e, "bounds_rect must exist on parsed elements"
        rect = _parse_bounds_rect(e.get("bounds"))
        if rect is None:
            assert e.get("bounds_rect") is None
            continue
        br = e["bounds_rect"]
        assert isinstance(br, dict)
        assert (br["left"], br["top"], br["right"], br["bottom"]) == rect


