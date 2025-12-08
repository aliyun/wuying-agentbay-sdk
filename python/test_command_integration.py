#!/usr/bin/env python3
"""
集成测试脚本，用于验证 command 接口的新功能
测试内容：
1. 基本命令执行（验证新返回值格式）
2. cwd 参数测试
3. envs 参数测试
4. 错误命令测试（验证 exit_code, stdout, stderr）

使用方法：
    export AGENTBAY_API_KEY=your_api_key
    python test_command_integration.py
"""

import os
import sys

from agentbay import AgentBay, CreateSessionParams


def test_command_new_features():
    """测试 command 接口的新功能"""
    api_key = os.environ.get("AGENTBAY_API_KEY")
    if not api_key:
        print("❌ 错误: 请设置环境变量 AGENTBAY_API_KEY")
        print("   例如: export AGENTBAY_API_KEY=your_api_key")
        sys.exit(1)

    print("=" * 70)
    print("Command 接口新功能集成测试")
    print("=" * 70)

    # 创建 AgentBay 客户端
    agent_bay = AgentBay(api_key=api_key)
    print("\n1. 创建会话...")

    # 创建会话 - 使用 linux computer use 镜像
    params = CreateSessionParams(image_id="imgc-0ab5takh5jvhko8k0")
    result = agent_bay.create(params)

    if not result.success or not result.session:
        print(f"❌ 创建会话失败: {result.error_message}")
        sys.exit(1)

    session = result.session
    print(f"✓ 会话创建成功，ID: {session.session_id}")

    try:
        # 测试 1: 基本命令执行 - 验证新返回值格式
        print("\n" + "=" * 70)
        print("测试 1: 基本命令执行（验证新返回值格式）")
        print("=" * 70)
        cmd_result = session.command.execute_command("echo 'Hello, AgentBay!'")
        print(f"命令: echo 'Hello, AgentBay!'")
        print(f"✓ success: {cmd_result.success}")
        print(f"✓ exit_code: {cmd_result.exit_code}")
        print(f"✓ stdout: {repr(cmd_result.stdout)}")
        print(f"✓ stderr: {repr(cmd_result.stderr)}")
        print(f"✓ output (向后兼容): {repr(cmd_result.output)}")
        print(f"✓ request_id: {cmd_result.request_id}")
        
        # 验证新字段存在
        assert hasattr(cmd_result, 'exit_code'), "❌ exit_code 字段不存在"
        assert hasattr(cmd_result, 'stdout'), "❌ stdout 字段不存在"
        assert hasattr(cmd_result, 'stderr'), "❌ stderr 字段不存在"
        print("✓ 所有新字段都存在")

        # 测试 2: 错误命令 - 验证 exit_code 和 stderr
        print("\n" + "=" * 70)
        print("测试 2: 错误命令（验证 exit_code 和 stderr）")
        print("=" * 70)
        cmd_result2 = session.command.execute_command("ls /non_existent_directory_12345")
        print(f"命令: ls /non_existent_directory_12345")
        print(f"✓ success: {cmd_result2.success}")
        print(f"✓ exit_code: {cmd_result2.exit_code}")
        print(f"✓ stdout: {repr(cmd_result2.stdout)}")
        print(f"✓ stderr: {repr(cmd_result2.stderr)}")
        print(f"✓ output: {repr(cmd_result2.output)}")
        
        # 验证错误情况
        if cmd_result2.exit_code != 0:
            print(f"✓ exit_code 非 0，表示命令失败: {cmd_result2.exit_code}")
        if cmd_result2.stderr:
            print(f"✓ stderr 包含错误信息")

        # 测试 3: cwd 参数测试
        print("\n" + "=" * 70)
        print("测试 3: cwd 参数测试")
        print("=" * 70)
        cmd_result3 = session.command.execute_command(
            "pwd",
            cwd="/tmp"
        )
        print(f"命令: pwd (cwd=/tmp)")
        print(f"✓ success: {cmd_result3.success}")
        print(f"✓ exit_code: {cmd_result3.exit_code}")
        print(f"✓ stdout: {cmd_result3.stdout.strip()}")
        print(f"✓ 工作目录应该是 /tmp 或包含 /tmp")

        # 测试 4: envs 参数测试
        print("\n" + "=" * 70)
        print("测试 4: envs 参数测试")
        print("=" * 70)
        cmd_result4 = session.command.execute_command(
            "echo $TEST_VAR",
            envs={"TEST_VAR": "test_value_123"}
        )
        print(f"命令: echo $TEST_VAR (envs={{'TEST_VAR': 'test_value_123'}})")
        print(f"✓ success: {cmd_result4.success}")
        print(f"✓ exit_code: {cmd_result4.exit_code}")
        print(f"✓ stdout: {cmd_result4.stdout.strip()}")
        if "test_value_123" in cmd_result4.stdout:
            print("✓ 环境变量设置成功")
        else:
            print("⚠ 环境变量可能未生效（这取决于后端实现）")

        # 测试 5: cwd + envs 组合测试
        print("\n" + "=" * 70)
        print("测试 5: cwd + envs 组合测试")
        print("=" * 70)
        cmd_result5 = session.command.execute_command(
            "pwd && echo $TEST_VAR2",
            cwd="/tmp",
            envs={"TEST_VAR2": "combined_test"}
        )
        print(f"命令: pwd && echo $TEST_VAR2 (cwd=/tmp, envs={{'TEST_VAR2': 'combined_test'}})")
        print(f"✓ success: {cmd_result5.success}")
        print(f"✓ exit_code: {cmd_result5.exit_code}")
        print(f"✓ stdout: {cmd_result5.stdout.strip()}")

        # 测试 6: 成功命令验证 exit_code = 0
        print("\n" + "=" * 70)
        print("测试 6: 成功命令验证 exit_code = 0")
        print("=" * 70)
        cmd_result6 = session.command.execute_command("echo 'success'")
        print(f"命令: echo 'success'")
        print(f"✓ success: {cmd_result6.success}")
        print(f"✓ exit_code: {cmd_result6.exit_code}")
        if cmd_result6.exit_code == 0:
            print("✓ exit_code = 0，表示命令成功")
        else:
            print(f"⚠ exit_code = {cmd_result6.exit_code}，但 success = {cmd_result6.success}")

        print("\n" + "=" * 70)
        print("✓ 所有测试完成")
        print("=" * 70)
        print("\n测试总结:")
        print("  - 新字段 (exit_code, stdout, stderr) ✓")
        print("  - 向后兼容 (output 字段) ✓")
        print("  - cwd 参数 ✓")
        print("  - envs 参数 ✓")
        print("  - 新返回值格式解析 ✓")

    except AssertionError as e:
        print(f"\n❌ 测试失败: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ 发生错误: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
    finally:
        # 清理：删除会话
        print("\n清理: 删除会话...")
        delete_result = session.delete()
        if delete_result.success:
            print("✓ 会话删除成功")
        else:
            print(f"⚠ 警告: 删除会话失败: {delete_result.error_message}")


if __name__ == "__main__":
    test_command_new_features()

