package com.example.agent;

import com.aliyun.agentbay.exception.AgentBayException;
import dev.langchain4j.model.chat.ChatLanguageModel;
import dev.langchain4j.model.openai.OpenAiChatModel;
import dev.langchain4j.service.AiServices;

public class AgentBayDemo {

    public static void main(String[] args) throws AgentBayException {
        String agentbayApiKey = System.getenv("AGENTBAY_API_KEY");
        if (agentbayApiKey == null || agentbayApiKey.isEmpty()) {
            System.err.println("错误: 请设置环境变量 AGENTBAY_API_KEY");
            System.exit(1);
        }

        String apiKey = System.getenv("OPENAI_API_KEY");
        String baseUrl = System.getenv("OPENAI_BASE_URL");
        String modelName =  System.getenv("MODEL_NAME");

        if (apiKey == null || apiKey.isEmpty()) {
            System.err.println("错误: 请设置环境变量 OPENAI_API_KEY");
            System.exit(1);
        }

        if (modelName == null || modelName.isEmpty()) {
            modelName = "gpt-4";
        }

        OpenAiChatModel.OpenAiChatModelBuilder builder = OpenAiChatModel.builder()
                .apiKey(apiKey)
                .modelName(modelName)
                .temperature(0.0);

        if (baseUrl != null && !baseUrl.isEmpty()) {
            builder.baseUrl(baseUrl);
        }

        ChatLanguageModel chatModel = builder.build();

        AgentBayTools tools = new AgentBayTools(agentbayApiKey);

        DataAnalysisAgent agent = AiServices.builder(DataAnalysisAgent.class)
                .chatLanguageModel(chatModel)
                .tools(tools)
                .build();

        System.out.println("=".repeat(80));
        System.out.println("LangChain4j + AgentBay Demo - 数据分析助手");
        System.out.println("=".repeat(80));
        System.out.println();

        runExample1(agent);
        System.out.println("\n" + "=".repeat(80) + "\n");

        runExample2(agent);
        System.out.println("\n" + "=".repeat(80) + "\n");

        runExample3(agent);
        System.out.println("\n" + "=".repeat(80) + "\n");
    }

    private static void runExample1(DataAnalysisAgent agent) {
        System.out.println("示例 1: Python 计算任务");
        System.out.println("-".repeat(80));
        String query1 = "帮我用 Python 计算 1000 以内所有质数的和";
        System.out.println("用户: " + query1);
        System.out.println();

        String response1 = agent.analyze(query1);
        System.out.println("\n助手: " + response1);
    }

    private static void runExample2(DataAnalysisAgent agent) {
        System.out.println("示例 2: 数据分析任务");
        System.out.println("-".repeat(80));
        String query2 = "用 Python 生成一个包含 100 个随机数的列表，然后计算它们的平均值、中位数和标准差";
        System.out.println("用户: " + query2);
        System.out.println();

        String response2 = agent.analyze(query2);
        System.out.println("\n助手: " + response2);
    }

    private static void runExample3(DataAnalysisAgent agent) {
        System.out.println("示例 3: Shell 命令任务");
        System.out.println("-".repeat(80));
        String query3 = "在云端环境中，创建一个文本文件，写入当前日期和系统信息，然后读取它";
        System.out.println("用户: " + query3);
        System.out.println();

        String response3 = agent.analyze(query3);
        System.out.println("\n助手: " + response3);
    }
}
