package com.example.agentdemo.service;

import com.aliyun.agentbay.AgentBay;
import com.aliyun.agentbay.model.CodeExecutionResult;
import com.aliyun.agentbay.model.SessionResult;
import com.aliyun.agentbay.session.CreateSessionParams;
import com.aliyun.agentbay.session.Session;
import com.fasterxml.jackson.annotation.JsonClassDescription;
import com.fasterxml.jackson.annotation.JsonProperty;
import com.fasterxml.jackson.annotation.JsonPropertyDescription;
import org.springframework.stereotype.Service;

import java.util.function.Function;

@Service
public class AgentBayToolService implements Function<AgentBayToolService.Request, AgentBayToolService.Response> {

    private final AgentBay agentBay;

    public AgentBayToolService(AgentBay agentBay) {
        this.agentBay = agentBay;
    }

    @JsonClassDescription("在安全的云端沙箱中执行 Python 3 代码")
    public record Request(
            @JsonProperty(required = true, value = "code")
            @JsonPropertyDescription("要执行的 Python 3 代码字符串")
            String code
    ) {}

    public record Response(String result, boolean success) {}

    @Override
    public Response apply(Request request) {
        String code = request.code();
        System.out.println(">>> AgentBay: 收到代码执行任务...\n" + code);
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
                return new Response(execResult.getResult(), true);
            } else {
                System.err.println(">>> AgentBay: 执行失败: " + execResult.getErrorMessage());
                return new Response(execResult.getErrorMessage(), false);
            }

        } catch (Exception e) {
            e.printStackTrace();
            return new Response("SDK调用异常: " + e.getMessage(), false);
        } finally {
            if (session != null) {
                try {
                    agentBay.delete(session, false);
                    System.out.println(">>> AgentBay: 环境已清理.");
                } catch (Exception e) {
                    e.printStackTrace();
                }
            }
        }
    }
}
