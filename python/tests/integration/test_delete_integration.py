import os
import time
import unittest
from uuid import uuid4

from agentbay import AgentBay
from agentbay.session_params import CreateSessionParams
from agentbay.context_sync import ContextSync


def get_test_api_key():
    """获取测试用的 API key"""
    return os.environ.get("AGENTBAY_API_KEY")


class TestDeleteIntegration(unittest.TestCase):
    """测试会话删除功能的集成测试"""

    @classmethod
    def setUpClass(cls):
        # 获取API Key
        api_key = get_test_api_key()
        if not api_key:
            raise unittest.SkipTest("未设置 AGENTBAY_API_KEY 环境变量")

        # 初始化AgentBay客户端
        cls.agent_bay = AgentBay(api_key=api_key)

    def test_delete_without_params(self):
        """测试不带参数删除会话的功能"""
        # 创建一个会话
        print("创建用于无参数删除测试的会话...")
        result = self.agent_bay.create()
        self.assertTrue(result.success)
        self.assertIsNotNone(result.session)
        session = result.session
        print(f"会话创建成功，ID: {session.session_id}")

        # 使用默认参数删除会话
        print("使用不带参数的delete方法删除会话...")
        delete_result = session.delete()
        self.assertTrue(delete_result.success)
        print(f"会话删除成功 (RequestID: {delete_result.request_id})")

        # 验证会话已被删除
        # 等待一段时间确保删除操作完成
        time.sleep(2)
        
        # 使用 list_by_labels 从服务器获取最新会话列表
        list_result = self.agent_bay.list_by_labels()
        self.assertTrue(list_result.success)
        
        # 检查会话是否已被删除
        session_ids = [s.session_id for s in list_result.sessions]
        self.assertNotIn(
            session.session_id,
            session_ids,
            f"会话 ID {session.session_id} 在删除后仍然存在",
        )

    def test_delete_with_sync_context(self):
        """测试带sync_context参数删除会话的功能"""
        # 创建上下文
        context_name = f"test-context-{uuid4().hex[:8]}"
        print(f"创建上下文: {context_name}...")
        context_result = self.agent_bay.context.create(context_name)
        self.assertTrue(context_result.success)
        self.assertIsNotNone(context_result.context)
        context = context_result.context
        print(f"上下文创建成功，ID: {context.id}")

        # 创建持久化配置
        persistence_data = [
            ContextSync(
                context_id=context.id,
                path="/home/wuying/test"
            )
        ]

        # 创建带上下文的会话
        params = CreateSessionParams(
            image_id="linux_latest",
            context_syncs=persistence_data
        )

        print("创建带上下文的会话...")
        result = self.agent_bay.create(params)
        self.assertTrue(result.success)
        self.assertIsNotNone(result.session)
        session = result.session
        print(f"会话创建成功，ID: {session.session_id}")

        # 在会话中创建测试文件
        test_cmd = "echo 'test file content' > /home/wuying/test/testfile.txt"
        try:
            cmd_result = session.command.execute_command(test_cmd)
            print(f"创建测试文件: {cmd_result}")
        except Exception as e:
            print(f"警告: 创建测试文件失败: {e}")

        # 使用sync_context=True删除会话
        print("使用sync_context=True删除会话...")
        delete_result = session.delete(sync_context=True)
        self.assertTrue(delete_result.success)
        print(f"会话删除成功 (RequestID: {delete_result.request_id})")

        # 验证会话已被删除
        # 等待一段时间确保删除操作完成
        time.sleep(2)
        
        # 使用 list_by_labels 从服务器获取最新会话列表
        list_result = self.agent_bay.list_by_labels()
        self.assertTrue(list_result.success)
        
        # 检查会话是否已被删除
        session_ids = [s.session_id for s in list_result.sessions]
        self.assertNotIn(
            session.session_id,
            session_ids,
            f"会话 ID {session.session_id} 在删除后仍然存在",
        )

        # 清理上下文
        try:
            delete_context_result = self.agent_bay.context.delete(context)
            if delete_context_result.success:
                print(f"上下文 {context.id} 已删除")
            else:
                print(f"警告: 删除上下文失败")
        except Exception as e:
            print(f"警告: 删除上下文时出错: {e}")

    def test_agentbay_delete_with_sync_context(self):
        """测试AgentBay.delete带sync_context参数的功能"""
        # 创建上下文
        context_name = f"test-context-{uuid4().hex[:8]}"
        print(f"创建上下文: {context_name}...")
        context_result = self.agent_bay.context.create(context_name)
        self.assertTrue(context_result.success)
        self.assertIsNotNone(context_result.context)
        context = context_result.context
        print(f"上下文创建成功，ID: {context.id}")

        # 创建持久化配置
        persistence_data = [
            ContextSync(
                context_id=context.id,
                path="/home/wuying/test2"
            )
        ]

        # 创建带上下文的会话
        params = CreateSessionParams(
            image_id="linux_latest",
            context_syncs=persistence_data
        )

        print("创建带上下文的会话...")
        result = self.agent_bay.create(params)
        self.assertTrue(result.success)
        self.assertIsNotNone(result.session)
        session = result.session
        print(f"会话创建成功，ID: {session.session_id}")

        # 在会话中创建测试文件
        test_cmd = "echo 'test file for agentbay delete' > /home/wuying/test2/testfile2.txt"
        try:
            cmd_result = session.command.execute_command(test_cmd)
            print(f"创建测试文件: {cmd_result}")
        except Exception as e:
            print(f"警告: 创建测试文件失败: {e}")

        # 使用agent_bay.delete带sync_context=True删除会话
        print("使用agent_bay.delete带sync_context=True删除会话...")
        delete_result = self.agent_bay.delete(session, sync_context=True)
        self.assertTrue(delete_result.success)
        print(f"会话删除成功 (RequestID: {delete_result.request_id})")

        # 验证会话已被删除
        # 等待一段时间确保删除操作完成
        time.sleep(2)
        
        # 使用 list_by_labels 从服务器获取最新会话列表
        list_result = self.agent_bay.list_by_labels()
        self.assertTrue(list_result.success)
        
        # 检查会话是否已被删除
        session_ids = [s.session_id for s in list_result.sessions]
        self.assertNotIn(
            session.session_id,
            session_ids,
            f"会话 ID {session.session_id} 在删除后仍然存在",
        )

        # 清理上下文
        try:
            delete_context_result = self.agent_bay.context.delete(context)
            if delete_context_result.success:
                print(f"上下文 {context.id} 已删除")
            else:
                print(f"警告: 删除上下文失败")
        except Exception as e:
            print(f"警告: 删除上下文时出错: {e}")


if __name__ == "__main__":
    unittest.main()