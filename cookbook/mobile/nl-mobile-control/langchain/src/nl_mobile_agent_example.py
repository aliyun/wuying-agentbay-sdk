#!/usr/bin/env python3
"""
Generic natural language mobile control example.

This example uses the generic controller/tools and a Xiaohongshu preset image/package,
but the agent and tools are app-agnostic.
"""

from __future__ import annotations

import asyncio
import os
from datetime import datetime
from pathlib import Path

from nl_mobile_agent import MobileNLController, create_langchain_mobile_agent


XHS_IMAGE_ID = "imgc-0aae4rgl3u35xrhoe"
XHS_PACKAGE = "com.xingin.xhs"


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[6]


async def main() -> None:
    agentbay_api_key = os.getenv("AGENTBAY_API_KEY")
    dashscope_api_key = os.getenv("DASHSCOPE_API_KEY")

    if not agentbay_api_key:
        print("Error: AGENTBAY_API_KEY environment variable must be set")
        return
    if not dashscope_api_key:
        print("Error: DASHSCOPE_API_KEY environment variable must be set")
        return

    run_id = datetime.now().strftime("%Y%m%d-%H%M%S")
    tmp_dir = _repo_root() / "tmp" / "nl-mobile-example" / run_id

    controller = MobileNLController(
        agentbay_api_key=agentbay_api_key,
        image_id=os.getenv("MOBILE_IMAGE_ID", XHS_IMAGE_ID),
        tmp_dir=tmp_dir,
    )

    agent = create_langchain_mobile_agent(controller=controller)["agent"]

    app_package = os.getenv("MOBILE_APP_PACKAGE", XHS_PACKAGE)
    query = os.getenv("MOBILE_QUERY", "少女高颜值穿搭")

    instruction = (
        f"请在云手机上完成：\n"
        f"1) start_session\n"
        f"2) launch_app 打开应用包名：{app_package}\n"
        f"3) dismiss_popups 处理弹窗\n"
        f"4) 进入搜索并搜索：{query}\n"
        f"5) 用 get_visible_texts 简要验证搜索结果页出现了查询词\n"
        f"每个关键步骤后都调用 screenshot 保存截图。\n"
        f"最后用中文输出：DONE + 你看到的证据文本片段。"
    )

    try:
        result = await agent.ainvoke(
            {"messages": [{"role": "user", "content": instruction}]},
            {"recursion_limit": 220},
        )
        if "messages" in result and result["messages"]:
            final = result["messages"][-1]
            content = getattr(final, "content", None)
            print(content if content else final)
        else:
            print(result)
    finally:
        try:
            await controller.stop()
        except Exception:
            pass


if __name__ == "__main__":
    asyncio.run(main())


