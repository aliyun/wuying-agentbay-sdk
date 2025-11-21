package com.aliyun.agentbay.examples;

import com.aliyun.agentbay.AgentBay;
import com.aliyun.agentbay.mcp.McpToolsResult;
import com.aliyun.agentbay.model.CommandResult;
import com.aliyun.agentbay.model.SessionResult;
import com.aliyun.agentbay.session.CreateSessionParams;
import com.aliyun.agentbay.session.Session;

/**
 * Example demonstrating code execution functionality in AgentBay Java SDK
 */
public class SessionResumeExample {
    
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
            params.setImageId("imgc-0abxi0lc574y4cltl");
            params.setIsVpc(true);
            SessionResult sessionResult = agentBay.create(params);

            if (!sessionResult.isSuccess()) {
                System.err.println("Failed to create session: " + sessionResult.getErrorMessage());
                return;
            }

            Session session = sessionResult.getSession();
            System.out.println("✅ Session created successfully!");
            System.out.println("   Session ID: " + session.getSessionId());
            System.out.println("   Request ID: " + sessionResult.getRequestId());

            CommandResult commandResult = session.getCommand().executeCommand("echo 'Hello, World!' > /tmp/test", 1000);
            if (!commandResult.isSuccess()) {
                System.err.println("❌ Failed to execute command: " + commandResult.getErrorMessage());
                return;
            }
            System.out.println("✅ Command executed successfully!");
            System.out.println("   Command executed output: " + commandResult.getOutput());

            System.out.println("\n=== Testing Session State Dump/Restore ===");

            String stateJson = session.dumpState();
            System.out.println("✅ Session state dumped!");
            System.out.println("   State JSON length: " + stateJson.length() + " characters");
            System.out.println("   State preview: " + (stateJson.length() > 100 ? stateJson.substring(0, 100) + "..." : stateJson));

            for (int i = 0; i < 1000; i++) {
                Session restoredSession = Session.restoreState(agentBay, stateJson);
                System.out.println("✅ Session state restored!");
                System.out.println("   Restored session ID: " + restoredSession.getSessionId());
                System.out.println("   VPC enabled: " + restoredSession.isVpcEnabled());
                if (restoredSession.isVpcEnabled()) {
                    System.out.println("   HTTP Port: " + restoredSession.getHttpPort());
                    System.out.println("   VPC Link URL: " + (restoredSession.getVpcLinkUrl() != null ? "cached" : "not cached"));
                }

                CommandResult restoreCommandResult = restoredSession.getCommand().executeCommand("cat /tmp/test", 1000);
                if (!restoreCommandResult.isSuccess()) {
                    System.err.println("❌ Failed to execute command on restored session: " + restoreCommandResult.getErrorMessage());
                } else {
                    System.out.println("✅ Command executed on restored session!");
                    System.out.println("   Output: " + restoreCommandResult.getOutput());
                }
                stateJson = session.dumpState();
                Thread.sleep(10000);
            }
            
        } catch (Exception e) {
            System.err.println("❌ Unexpected error: " + e.getMessage());
            e.printStackTrace();
        }
    }
}