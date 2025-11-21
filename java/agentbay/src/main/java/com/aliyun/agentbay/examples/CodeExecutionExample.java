package com.aliyun.agentbay.examples;

import com.aliyun.agentbay.AgentBay;
import com.aliyun.agentbay.model.CodeExecutionResult;
import com.aliyun.agentbay.exception.AgentBayException;
import com.aliyun.agentbay.exception.SessionException;
import com.aliyun.agentbay.model.SessionResult;
import com.aliyun.agentbay.session.CreateSessionParams;
import com.aliyun.agentbay.session.Session;

/**
 * Example demonstrating code execution functionality in AgentBay Java SDK
 */
public class CodeExecutionExample {

    public static void main(String[] args) {
        try {
            String apiKey = System.getenv("AGENTBAY_API_KEY");
            if (apiKey == null || apiKey.trim().isEmpty()) {
                System.err.println("Error: AGENTBAY_API_KEY environment variable not set");
                return;
            }

            // Create AgentBay client (API key from environment variable AGENTBAY_API_KEY)
            System.out.println("Creating AgentBay client...");
            AgentBay agentBay = new AgentBay(apiKey);

            // Create a session
            System.out.println("Creating session...");
            CreateSessionParams params = new CreateSessionParams();
            params.setImageId("linux_latest");
            SessionResult sessionResult = agentBay.create(params);

            if (!sessionResult.isSuccess()) {
                System.err.println("Failed to create session: " + sessionResult.getErrorMessage());
                return;
            }

            Session session = sessionResult.getSession();

            System.out.println("✅ Session created successfully!");
            System.out.println("   Session ID: " + session.getSessionId());
            System.out.println("   Request ID: " + sessionResult.getRequestId());

            // Example 1: Execute Python code
            System.out.println("\n🐍 Executing Python code...");
            String pythonCode = "print(\"hello world\")";
            CodeExecutionResult pythonResult = session.getCode().runCode(pythonCode, "python");

            if (pythonResult.isSuccess()) {
                System.out.println("✅ Python code executed successfully!");
                System.out.println("   Output: " + pythonResult.getResult());
                System.out.println("   Request ID: " + pythonResult.getRequestId());
            } else {
                System.err.println("❌ Failed to execute Python code: " + pythonResult.getErrorMessage());
            }

            // Example 2: Execute JavaScript code
            System.out.println("\n🟨 Executing JavaScript code...");
            String jsCode = "console.log('Hello from JavaScript!');\nconst result = 5 * 4;\nconsole.log(`5 * 4 = ${result}`);";
            CodeExecutionResult jsResult = session.getCode().runCode(jsCode, "javascript");

            if (jsResult.isSuccess()) {
                System.out.println("✅ JavaScript code executed successfully!");
                System.out.println("   Output: " + jsResult.getResult());
                System.out.println("   Request ID: " + jsResult.getRequestId());
            } else {
                System.err.println("❌ Failed to execute JavaScript code: " + jsResult.getErrorMessage());
            }

            // Clean up - delete the session


        } catch (SessionException e) {
            System.err.println("❌ Session error: " + e.getMessage());
            e.printStackTrace();
        } catch (AgentBayException e) {
            System.err.println("❌ AgentBay error: " + e.getMessage());
            e.printStackTrace();
        } catch (Exception e) {
            System.err.println("❌ Unexpected error: " + e.getMessage());
            e.printStackTrace();
        }
    }
}