package com.example.agent;

import dev.langchain4j.service.SystemMessage;
import dev.langchain4j.service.UserMessage;

public interface DataAnalysisAgent {

    @SystemMessage("""
            你是一个专业的数据分析助手。
            当需要执行计算、数据处理或代码生成任务时，你可以使用以下工具：
            - executePythonCode: 执行 Python 代码
            - executeShellCommand: 执行 Shell 命令
            - executeJavaScriptCode: 执行 JavaScript 代码

            请根据用户的需求选择合适的工具来完成任务。
            在返回结果时，请用简洁清晰的语言解释结果。
            """)
    String analyze(@UserMessage String query);
}
