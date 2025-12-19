from __future__ import annotations

from dataclasses import dataclass
from typing import List


@dataclass(frozen=True)
class AppTaskScenario:
    """
    A task scenario for an app, with an explicit difficulty level.

    Success definition (used by evaluator):
    - Post-check: UI visible texts contain at least `min_tokens_found` tokens from `expected_tokens`
    - No tool failures reported in tool message payloads
    """

    app_name: str
    app_package: str
    level: int
    name: str
    user_instruction: str
    expected_tokens: List[str]
    min_tokens_found: int = 1
    notes: str = ""


PDD_PACKAGE = "com.xunmeng.pinduoduo"
TAOBAO_PACKAGE = "com.taobao.taobao"
WEIBO_PACKAGE = "com.sina.weibo"


def default_app_tasks(*, query_cn: str = "少女高颜值穿搭") -> List[AppTaskScenario]:
    """
    Default exploration tasks (progressive complexity) for:
    - Xiaohongshu
    - Pinduoduo
    - Taobao (Flash buy / same-day)
    - Weibo
    """

    tasks: List[AppTaskScenario] = []

    # Xiaohongshu (baseline / known-good)
    tasks += [
        AppTaskScenario(
            app_name="Xiaohongshu",
            app_package="com.xingin.xhs",
            level=1,
            name="xhs_open_search",
            user_instruction=(
                "Start session, launch the app, dismiss popups. "
                "Open the search page (if search button not found, try tapping near the top-right area). "
                f"Search for '{query_cn}'. Take screenshots at key steps. "
                "Stop after you see the search results page."
            ),
            expected_tokens=["全部", "综合", query_cn],
            min_tokens_found=2,
            notes="Stable baseline; used to validate the general workflow.",
        )
    ]

    # Pinduoduo (progressive)
    tasks += [
        AppTaskScenario(
            app_name="Pinduoduo",
            app_package=PDD_PACKAGE,
            level=1,
            name="pdd_open_to_search",
            user_instruction=(
                "Start session, launch Pinduoduo, dismiss popups. "
                "Navigate to the search entry/search box page. "
                "Take screenshots at each transition and stop when the search input is visible."
            ),
            expected_tokens=["搜索", "拼多多", "推荐"],
            min_tokens_found=1,
            notes="Basic navigation + popup handling.",
        ),
        AppTaskScenario(
            app_name="Pinduoduo",
            app_package=PDD_PACKAGE,
            level=2,
            name="pdd_search_and_filter",
            user_instruction=(
                "Start session, launch Pinduoduo, dismiss popups. "
                "Search for '蓝牙耳机'. On results page, apply a common sort/filter "
                "(e.g. 综合/销量/筛选). Take screenshots and stop on the results page."
            ),
            expected_tokens=["综合", "销量", "筛选", "蓝牙耳机"],
            min_tokens_found=2,
            notes="Search + results understanding; query text may or may not appear in UI texts.",
        ),
        AppTaskScenario(
            app_name="Pinduoduo",
            app_package=PDD_PACKAGE,
            level=3,
            name="pdd_open_product_and_comments",
            user_instruction=(
                "Start session, launch Pinduoduo, dismiss popups. "
                "Search for '蓝牙耳机', open the first product card, "
                "then open '评价/评论' section and scroll down a bit. "
                "Take screenshots and stop on the comments/ratings section."
            ),
            expected_tokens=["评价", "评论", "详情"],
            min_tokens_found=1,
            notes="Multi-step navigation; depends on UI accessibility labels.",
        ),
        AppTaskScenario(
            app_name="Pinduoduo",
            app_package=PDD_PACKAGE,
            level=4,
            name="pdd_add_to_cart_boundary",
            user_instruction=(
                "Start session, launch Pinduoduo, dismiss popups. "
                "Search for '蓝牙耳机', open a product, then try to add it to cart. "
                "If login is required, stop at the login page. "
                "DO NOT proceed to any payment. Take screenshots."
            ),
            expected_tokens=["购物车", "登录", "加入购物车"],
            min_tokens_found=1,
            notes="Boundary: add-to-cart may require login; reaching login is considered acceptable.",
        ),
    ]

    # Taobao (flash / same-day) - progressive
    tasks += [
        AppTaskScenario(
            app_name="Taobao",
            app_package=TAOBAO_PACKAGE,
            level=1,
            name="tb_find_flash_buy",
            user_instruction=(
                "Start session, launch Taobao, dismiss popups. "
                "Find the entrance of '闪购' (or '小时达' / local instant delivery) and open it. "
                "Take screenshots and stop when you see the flash-buy page."
            ),
            expected_tokens=["闪购", "小时达", "配送"],
            min_tokens_found=1,
            notes="Discovering a feature entry (may vary by UI/region).",
        ),
        AppTaskScenario(
            app_name="Taobao",
            app_package=TAOBAO_PACKAGE,
            level=2,
            name="tb_flash_search",
            user_instruction=(
                "Start session, launch Taobao, dismiss popups. "
                "Enter '闪购/小时达' section if possible, then search for '牛奶'. "
                "Stop at results page and take screenshots."
            ),
            expected_tokens=["综合", "销量", "筛选", "牛奶"],
            min_tokens_found=1,
            notes="Search inside a sub-feature; labels may differ.",
        ),
        AppTaskScenario(
            app_name="Taobao",
            app_package=TAOBAO_PACKAGE,
            level=3,
            name="tb_open_product_delivery_info",
            user_instruction=(
                "Start session, launch Taobao, dismiss popups. "
                "Search for '牛奶', open a product, and locate delivery/ETA info "
                "(e.g. 配送/送达/地址). Take screenshots and stop on product detail."
            ),
            expected_tokens=["配送", "送达", "地址", "店铺"],
            min_tokens_found=1,
            notes="Requires locating a specific info block on a complex page.",
        ),
        AppTaskScenario(
            app_name="Taobao",
            app_package=TAOBAO_PACKAGE,
            level=4,
            name="tb_add_to_cart_boundary",
            user_instruction=(
                "Start session, launch Taobao, dismiss popups. "
                "Search for '牛奶', open a product, try to add it to cart. "
                "If login is required, stop at login. DO NOT proceed to payment. "
                "Take screenshots."
            ),
            expected_tokens=["加入购物车", "购物车", "登录"],
            min_tokens_found=1,
            notes="Boundary: login barrier is acceptable; avoid any payment steps.",
        ),
    ]

    # Weibo - progressive / boundary exploration
    tasks += [
        AppTaskScenario(
            app_name="Weibo",
            app_package=WEIBO_PACKAGE,
            level=1,
            name="wb_open_to_search",
            user_instruction=(
                "Start session, launch Weibo, dismiss popups. "
                "Navigate to the search entry and open the search page. "
                "Take screenshots and stop when search input is visible."
            ),
            expected_tokens=["搜索", "热搜", "微博"],
            min_tokens_found=1,
            notes="Basic navigation; tab labels vary.",
        ),
        AppTaskScenario(
            app_name="Weibo",
            app_package=WEIBO_PACKAGE,
            level=2,
            name="wb_search_topic",
            user_instruction=(
                "Start session, launch Weibo, dismiss popups. "
                "Search for 'AI', open the first topic/result. "
                "Take screenshots and stop when you see the topic/feed page."
            ),
            expected_tokens=["热搜", "话题", "评论", "转发"],
            min_tokens_found=1,
            notes="Search + enter a topic/feed.",
        ),
        AppTaskScenario(
            app_name="Weibo",
            app_package=WEIBO_PACKAGE,
            level=3,
            name="wb_open_post_comments",
            user_instruction=(
                "Start session, launch Weibo, dismiss popups. "
                "Search for 'AI', open a post, then open comments and scroll a bit. "
                "Take screenshots and stop at the comments view."
            ),
            expected_tokens=["评论", "转发", "赞"],
            min_tokens_found=1,
            notes="Multi-step; comment view labels should appear if accessible.",
        ),
        AppTaskScenario(
            app_name="Weibo",
            app_package=WEIBO_PACKAGE,
            level=4,
            name="wb_compose_boundary",
            user_instruction=(
                "Start session, launch Weibo, dismiss popups. "
                "Try to open the compose/write-post screen (写微博/发布). "
                "Stop when you reach the editor screen or a login barrier. "
                "DO NOT publish anything. Take screenshots."
            ),
            expected_tokens=["发布", "写微博", "登录"],
            min_tokens_found=1,
            notes="Boundary: reaching editor/login is acceptable; do not post.",
        ),
    ]

    return tasks


__all__ = [
    "AppTaskScenario",
    "PDD_PACKAGE",
    "TAOBAO_PACKAGE",
    "WEIBO_PACKAGE",
    "default_app_tasks",
]


