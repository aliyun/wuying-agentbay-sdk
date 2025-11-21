package com.example.agentdemo.config;

import com.aliyun.agentbay.AgentBay;
import com.aliyun.agentbay.exception.AgentBayException;
import com.example.agentdemo.service.AgentBayToolService;
import org.springframework.ai.chat.client.ChatClient;
import org.springframework.ai.chat.model.ChatModel;
import org.springframework.ai.model.function.FunctionCallback;
import org.springframework.ai.model.function.FunctionCallbackWrapper;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

@Configuration
public class AiConfig {

    @Bean
    public AgentBay agentBay() {
        String apiKey = System.getenv("AGENTBAY_API_KEY");
        if (apiKey == null || apiKey.isEmpty()) {
            throw new IllegalStateException("环境变量 AGENTBAY_API_KEY 未设置");
        }
        try {
            return new AgentBay(apiKey);
        } catch (AgentBayException e) {
            throw new IllegalStateException("初始化 AgentBay 失败", e);
        }
    }

    @Bean
    public FunctionCallback agentBayFunctionCallback(AgentBayToolService agentBayToolService) {
        return FunctionCallbackWrapper.builder(agentBayToolService)
                .withName("executePythonCode")
                .withDescription("在安全的云端沙箱中执行 Python 3 代码")
                .build();
    }

    @Bean
    public ChatClient chatClient(ChatModel chatModel, FunctionCallback agentBayFunctionCallback) {
        return ChatClient.builder(chatModel)
                .defaultFunctions(agentBayFunctionCallback)
                .build();
    }
}
