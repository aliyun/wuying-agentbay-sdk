#!/usr/bin/env python3
"""
简单的测试脚本：执行一个会出错的命令，检查返回的 exit_code
"""

import os
from agentbay import AgentBay

def main():
    # 初始化 AgentBay（不传 api_key 参数，会自动从环境变量 AGENTBAY_API_KEY 读取）
    # 如果环境变量未设置，AgentBay 会抛出 ValueError 提示
    try:
        agent_bay = AgentBay()
    except ValueError as e:
        print(f"错误：{e}")
        print("请设置环境变量：export AGENTBAY_API_KEY='your-api-key'")
        return
    
    # 创建 session
    result = agent_bay.create()
    if not result.success:
        print(f"Failed to create session: {result.error_message}")
        return
    
    session = result.session
    
    try:
        # 执行一个会出错的命令（访问不存在的文件）
        print("执行命令: cat /nonexistent_file_12345")
        cmd_result = session.command.execute_command("rm -rf /")
        
        print(f"\n执行结果:")
        print(f"  success: {cmd_result.success}")
        print(f"  exit_code: {cmd_result.exit_code}")
        print(f"  stdout: {cmd_result.stdout}")
        print(f"  stderr: {cmd_result.stderr}")
        print(f"  output: {cmd_result.output}")
        print(f"  trace_id: {cmd_result.trace_id}")
        
        # 验证 exit_code 是否为非 0
        if cmd_result.exit_code != 0:
            print(f"\n✓ 测试通过：exit_code = {cmd_result.exit_code} (非 0，表示命令执行失败)")
        else:
            print(f"\n✗ 测试失败：exit_code = {cmd_result.exit_code} (应该是非 0)")
            
    finally:
        # 清理 session
        session.delete()
        print("\nSession 已清理")

if __name__ == "__main__":
    main()

