#!/usr/bin/env python3
"""
Run a LangGraph ReAct agent to control Xiaohongshu (小红书) on a cloud phone.

It will download screenshots after key steps into:
  ./tmp/xhs-langchain-mobile/
"""

import asyncio
import os
from datetime import datetime
from pathlib import Path

from xhs_mobile_agent import XhsMobileController, create_xhs_langchain_agent


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
    tmp_dir = Path.cwd() / "tmp" / "xhs-langchain-mobile" / run_id
    controller = XhsMobileController(
        agentbay_api_key=agentbay_api_key,
        tmp_dir=tmp_dir,
    )

    agent_dict = create_xhs_langchain_agent(controller=controller)
    agent = agent_dict["agent"]

    instruction = (
        "打开小红书，搜索少女高颜值穿搭，总结搜索到的内容。"
        "你必须按步骤调用工具：start_session -> launch_xiaohongshu -> dismiss_popups -> "
        "search_xiaohongshu -> get_visible_texts。每个关键步骤后调用 screenshot 工具保存截图。"
        "最后用中文给出总结。"
    )

    try:
        result = await agent.ainvoke(
            {"messages": [{"role": "user", "content": instruction}]},
            {"recursion_limit": 200},
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


