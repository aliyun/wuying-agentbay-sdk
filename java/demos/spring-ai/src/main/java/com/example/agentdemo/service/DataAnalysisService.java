package com.example.agentdemo.service;

import org.springframework.ai.chat.client.ChatClient;
import org.springframework.ai.chat.messages.UserMessage;
import org.springframework.ai.chat.prompt.Prompt;
import org.springframework.ai.chat.prompt.SystemPromptTemplate;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
public class DataAnalysisService {

    private final ChatClient chatClient;

    public DataAnalysisService(ChatClient chatClient) {
        this.chatClient = chatClient;
    }

    public String runAnalysis(String prompt) {
        System.out.println(">>> 用户: " + prompt);

        String response = chatClient.prompt()
                .user(prompt)
                .call()
                .content();

        System.out.println(">>> 助手: " + response);
        return response;
    }
}
