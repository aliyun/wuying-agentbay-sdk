package com.aliyun.agentbay.examples;

import com.aliyun.agentbay.AgentBay;
import com.aliyun.agentbay.context.Context;
import com.aliyun.agentbay.context.ContextListResult;
import com.aliyun.agentbay.context.ContextResult;
import com.aliyun.agentbay.context.ContextSync;
import com.aliyun.agentbay.context.SyncPolicy;
import com.aliyun.agentbay.context.UploadMode;
import com.aliyun.agentbay.exception.AgentBayException;
import com.aliyun.agentbay.model.CommandResult;
import com.aliyun.agentbay.model.DeleteResult;
import com.aliyun.agentbay.model.SessionResult;
import com.aliyun.agentbay.session.CreateSessionParams;
import com.aliyun.agentbay.session.Session;

import java.util.Arrays;

/**
 * Context Management Example - Java equivalent of Python context management
 * 
 * This example demonstrates how to:
 * 1. List all contexts
 * 2. Get context information (create if doesn't exist)
 * 3. Create a session with the context
 * 4. Update the context
 * 5. Clean up resources
 */
public class SessionContextExample {
    
    public static void main(String[] args) {
        // Initialize the AgentBay client
        // You can provide the API key as a parameter or set the AGENTBAY_API_KEY environment variable
        String apiKey = System.getenv("AGENTBAY_API_KEY");
        if (apiKey == null || apiKey.isEmpty()) {
            apiKey = ""; // Replace with your actual API key
        }
        
        Session session = null;
        Context context = null;
        
        try {
            AgentBay agentBay = new AgentBay(apiKey);
            
            // Example 1: List all contexts
            System.out.println("\nExample 1: Listing all contexts...");
            try {
                ContextListResult result = agentBay.getContext().list();
                System.out.println("Request ID: " + result.getRequestId());
                if (result.isSuccess()) {
                    System.out.println("Found " + result.getContexts().size() + " contexts:");
                    for (Context ctx : result.getContexts()) {
                        System.out.println("- " + ctx.getName() + " (" + ctx.getId() + "): state=" + ctx.getState() + 
                                         ", os=" + ctx.getOsType());
                    }
                } else {
                    System.out.println("Failed to list contexts");
                }
            } catch (Exception e) {
                System.err.println("Error listing contexts: " + e.getMessage());
            }
            
            // Example 2: Get a context (create if it doesn't exist)
            System.out.println("\nExample 2: Getting a context (creating if it doesn't exist)...");
            String contextName = "test-context-java-1234";
            try {
                ContextResult result = agentBay.getContext().get(contextName, true);
                System.out.println("Request ID: " + result.getRequestId());
                if (result.isSuccess() && result.getContext() != null) {
                    context = result.getContext();
                    System.out.println("Got context: " + context.getName() + " (" + context.getId() + ")");
                } else {
                    System.out.println("Context not found and could not be created");
                    return;
                }
            } catch (Exception e) {
                System.err.println("Error getting context: " + e.getMessage());
                return;
            }
            
            // Example 3: Create a session with the context
            System.out.println("\nExample 3: Creating a session with the context...");
            try {
                CreateSessionParams params = new CreateSessionParams();
                
                // Fix: context_syncs should be a list, not a single ContextSync object
                SyncPolicy syncPolicy = SyncPolicy.defaultPolicy();
                ContextSync contextSync = ContextSync.create(
                    context.getId(),
                    "/tmp/shared",
                    syncPolicy
                );
                params.setContextSyncs(Arrays.asList(contextSync));
                params.setImageId("linux_latest");
                
                SessionResult sessionResult = agentBay.create(params);
                session = sessionResult.getSession();
                System.out.println("Session created with ID: " + session.getSessionId());
                System.out.println("Request ID: " + sessionResult.getRequestId());
                System.out.println("Note: The create() method automatically monitored the context status");
                System.out.println("and only returned after all context operations were complete or reached maximum retries.");
            } catch (AgentBayException e) {
                System.err.println("Error creating session: " + e.getMessage());
                return;
            }

            CommandResult commandResult = session.getCommand().executeCommand("mkdir -p /tmp/shared/ && touch /tmp/shared/"+session.getSessionId(), 1000);
            if (!commandResult.isSuccess()) {
                System.err.println("❌ Failed to execute command: " + commandResult.getErrorMessage());
                return;
            }
            System.out.println("✅ Command executed successfully!");
            System.out.println("   Request ID: " + commandResult.getRequestId());
            System.out.println("   Command executed output: " + commandResult.getOutput());

            commandResult = session.getCommand().executeCommand("ls -al /tmp/shared", 1000);
            if (!commandResult.isSuccess()) {
                System.err.println("❌ Failed to execute command: " + commandResult.getErrorMessage());
                return;
            }
            System.out.println("✅ Command executed successfully!");
            System.out.println("   Command executed output: " + commandResult.getOutput());
            System.out.println("   Request ID: " + commandResult.getRequestId());

            // Clean up
            System.out.println("\nCleaning up...");

            // Delete the session with context synchronization
            System.out.println("Deleting the session with context synchronization...");
            DeleteResult deleteResult = agentBay.delete(session, true); // sync_context=true
            System.out.println("Session deletion request ID: " + deleteResult.getRequestId());
            System.out.println("Session deletion success: " + deleteResult.isSuccess());
            System.out.println("Note: The delete() method synchronized the context before session deletion");
            System.out.println("and monitored all context operations until completion.");
        } catch (Exception e) {
            System.err.println("Error initializing AgentBay: " + e.getMessage());
        }
    }
    
}