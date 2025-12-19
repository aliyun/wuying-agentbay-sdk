from __future__ import annotations

import sys
from pathlib import Path


def _import_xhs_module():
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
    import xhs_mobile_agent as m  # noqa: E402  # pyright: ignore[reportMissingImports]

    return m


def test_flatten_and_extract_texts_dedup():
    m = _import_xhs_module()
    elements = [
        {
            "text": "搜索",
            "bounds": {"left": 0, "top": 0, "right": 10, "bottom": 10},
            "children": [
                {"text": "少女高颜值穿搭", "children": []},
                {"text": "搜索", "children": []},
            ],
        }
    ]

    flat = m._flatten_ui_elements(elements)
    assert len(flat) == 3

    texts = m._extract_texts(elements)
    assert texts == ["搜索", "少女高颜值穿搭"]


def test_bounds_center():
    m = _import_xhs_module()
    assert m._bounds_center({"left": 0, "top": 0, "right": 10, "bottom": 20}) == (5, 10)
    assert m._bounds_center("0,0,10,20") == (5, 10)
    assert m._bounds_center({"left": 5, "top": 5, "right": 5, "bottom": 20}) is None
    assert m._bounds_center("not-a-dict") is None
    assert m._parse_bounds_rect("1,2,3,4") == (1, 2, 3, 4)


def test_find_first_element_by_text_contains():
    m = _import_xhs_module()
    elements = [
        {"text": "首页", "children": []},
        {
            "text": "",
            "children": [
                {"text": "搜索", "bounds": {"left": 10, "top": 10, "right": 30, "bottom": 30}},
            ],
        },
    ]
    found = m._find_first_element_by_text(elements, text_contains="搜索")
    assert found is not None
    assert found.get("text") == "搜索"


def test_find_best_element_prefers_button_and_short_text():
    m = _import_xhs_module()
    elements = [
        {
            "text": "点击“同意”按钮，表示您已知情并同意以上协议",
            "className": "TextView",
            "bounds": "0,0,100,100",
            "children": [],
        },
        {
            "text": "同意",
            "className": "Button",
            "bounds": "0,200,100,300",
            "children": [],
        },
    ]
    best = m._find_best_element_by_text(elements, text_contains="同意", prefer_button=True)
    assert best is not None
    assert best.get("className") == "Button"
    assert best.get("text") == "同意"


