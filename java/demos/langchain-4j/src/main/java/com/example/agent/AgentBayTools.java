package com.example.agent;

import com.aliyun.agentbay.AgentBay;
import com.aliyun.agentbay.exception.AgentBayException;
import com.aliyun.agentbay.model.CodeExecutionResult;
import com.aliyun.agentbay.model.CommandResult;
import com.aliyun.agentbay.model.SessionResult;
import com.aliyun.agentbay.session.CreateSessionParams;
import com.aliyun.agentbay.session.Session;
import dev.langchain4j.agent.tool.Tool;

public class AgentBayTools {

    private final AgentBay agentBay;

    public AgentBayTools(String apiKey) throws AgentBayException {
        this.agentBay = new AgentBay(apiKey);
    }

    @Tool("在安全的云端沙箱中执行 Python 3 代码。适用于任何计算、数据分析或代码生成任务。返回执行结果或错误信息。")
    public String executePythonCode(String code) {
        System.out.println(">>> AgentBay: 收到代码执行任务...");
        System.out.println(">>> 代码:\n" + code);

        Session session = null;
        try {
            CreateSessionParams params = new CreateSessionParams();
            params.setImageId("code_latest");

            SessionResult result = agentBay.create(params);
            session = result.getSession();
            System.out.println(">>> AgentBay: 沙箱环境已创建. Session ID: " + session.getSessionId());

            CodeExecutionResult execResult = session.getCode().runCode(code, "python");

            if (execResult.isSuccess()) {
                System.out.println(">>> AgentBay: 执行成功.");
                return "执行成功，输出:\n" + execResult.getResult();
            } else {
                System.err.println(">>> AgentBay: 执行失败: " + execResult.getErrorMessage());
                return "执行失败，错误信息:\n" + execResult.getErrorMessage();
            }

        } catch (AgentBayException e) {
            e.printStackTrace();
            return "SDK调用异常: " + e.getMessage();
        } finally {
            if (session != null) {
                try {
                    agentBay.delete(session, false);
                    System.out.println(">>> AgentBay: 环境已清理.");
                } catch (Exception e) {
                    System.err.println("清理环境时出错: " + e.getMessage());
                }
            }
        }
    }

    @Tool("在云端 Linux 环境中执行 Shell 命令。可用于文件操作、系统管理等任务。")
    public String executeShellCommand(String command) {
        System.out.println(">>> AgentBay: 收到Shell命令执行任务...");
        System.out.println(">>> 命令: " + command);

        Session session = null;
        try {
            CreateSessionParams params = new CreateSessionParams();
            SessionResult result = agentBay.create(params);
            session = result.getSession();
            System.out.println(">>> AgentBay: 环境已创建. Session ID: " + session.getSessionId());

            CommandResult cmdResult = session.getCommand().executeCommand(command, 30000);

            System.out.println(">>> AgentBay: 命令执行完成.");
            return "命令执行结果:\n" + cmdResult.getOutput();

        } catch (Exception e) {
            e.printStackTrace();
            return "命令执行异常: " + e.getMessage();
        } finally {
            if (session != null) {
                try {
                    agentBay.delete(session, false);
                    System.out.println(">>> AgentBay: 环境已清理.");
                } catch (Exception e) {
                    System.err.println("清理环境时出错: " + e.getMessage());
                }
            }
        }
    }

    @Tool("在云端环境中执行 JavaScript 代码。适用于 Node.js 相关的计算任务。")
    public String executeJavaScriptCode(String code) {
        System.out.println(">>> AgentBay: 收到JavaScript执行任务...");
        System.out.println(">>> 代码:\n" + code);

        Session session = null;
        try {
            CreateSessionParams params = new CreateSessionParams();
            params.setImageId("code_latest");

            SessionResult result = agentBay.create(params);
            session = result.getSession();
            System.out.println(">>> AgentBay: 沙箱环境已创建. Session ID: " + session.getSessionId());

            CodeExecutionResult execResult = session.getCode().runCode(code, "javascript");

            if (execResult.isSuccess()) {
                System.out.println(">>> AgentBay: 执行成功.");
                return "执行成功，输出:\n" + execResult.getResult();
            } else {
                System.err.println(">>> AgentBay: 执行失败: " + execResult.getErrorMessage());
                return "执行失败，错误信息:\n" + execResult.getErrorMessage();
            }

        } catch (AgentBayException e) {
            e.printStackTrace();
            return "SDK调用异常: " + e.getMessage();
        } finally {
            if (session != null) {
                try {
                    agentBay.delete(session, false);
                    System.out.println(">>> AgentBay: 环境已清理.");
                } catch (Exception e) {
                    System.err.println("清理环境时出错: " + e.getMessage());
                }
            }
        }
    }
}
