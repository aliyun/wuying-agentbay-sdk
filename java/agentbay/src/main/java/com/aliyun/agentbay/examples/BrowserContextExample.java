package com.aliyun.agentbay.examples;

import com.aliyun.agentbay.AgentBay;
import com.aliyun.agentbay.browser.BrowserContext;
import com.aliyun.agentbay.browser.BrowserFingerprintContext;
import com.aliyun.agentbay.browser.ExtensionOption;
import com.aliyun.agentbay.context.Context;
import com.aliyun.agentbay.context.ContextResult;
import com.aliyun.agentbay.exception.AgentBayException;
import com.aliyun.agentbay.model.DeleteResult;
import com.aliyun.agentbay.model.SessionResult;
import com.aliyun.agentbay.session.CreateSessionParams;
import com.aliyun.agentbay.session.Session;

import java.util.Arrays;
import java.util.HashMap;
import java.util.Map;

/**
 * Browser Context Configuration Examples
 * 
 * This example demonstrates how to use Browser Context to persist browser data
 * (cookies, localStorage, etc.) across multiple sessions.
 * 
 * Key concepts:
 * 1. Basic browser context for persistent browser data
 * 2. Browser context with extension support
 * 3. Browser context with fingerprint support
 * 4. Complete workflow with context synchronization
 * 
 * Note: This example is equivalent to Python's browser_context_cookie_persistence.py
 */
public class BrowserContextExample {
    
    /**
     * Helper method to repeat a string n times (Java 8 compatible)
     * Replaces String.repeat() which is only available in Java 11+
     */
    private static String repeat(String str, int count) {
        if (count <= 0) return "";
        StringBuilder sb = new StringBuilder(str.length() * count);
        for (int i = 0; i < count; i++) {
            sb.append(str);
        }
        return sb.toString();
    }
    
    public static void main(String[] args) {
        try {
            // Initialize AgentBay client
            String apiKey = System.getenv("AGENTBAY_API_KEY");
            if (apiKey == null || apiKey.isEmpty()) {
                System.err.println("❌ Please set AGENTBAY_API_KEY environment variable");
                return;
            }
            
            AgentBay agentBay = new AgentBay(apiKey);
            System.out.println("✅ AgentBay client initialized");
            
            // Example 1: Basic browser context with data persistence
            System.out.println("\n" + repeat("=", 60));
            basicBrowserContextPersistenceExample(agentBay);
            
            // Example 2: Browser context with extensions
            System.out.println("\n" + repeat("=", 60));
            browserContextWithExtensionsExample(agentBay);
            
            // Example 3: Browser context with fingerprint
            System.out.println("\n" + repeat("=", 60));
            browserContextWithFingerprintExample(agentBay);
            
            // Example 4: Complete workflow with context synchronization
            System.out.println("\n" + repeat("=", 60));
            completeBrowserContextWorkflowExample(agentBay);
            
            System.out.println("\n" + repeat("=", 60));
            System.out.println("🎉 All Browser Context examples completed!");
            
        } catch (Exception e) {
            System.err.println("❌ Error: " + e.getMessage());
            e.printStackTrace();
        }
    }
    
    /**
     * Example 1: Basic browser context with data persistence
     * 
     * This example demonstrates:
     * - Creating a persistent context for browser data
     * - Creating a session with BrowserContext
     * - Browser data (cookies, localStorage) will be saved to this context
     */
    private static void basicBrowserContextPersistenceExample(AgentBay agentBay) throws AgentBayException {
        System.out.println("Example 1: Basic Browser Context with Data Persistence");
        System.out.println(repeat("-", 60));
        
        // Step 1: Create a persistent context for browser data
        String contextName = "demo-browser-context-" + System.currentTimeMillis();
        System.out.println("📦 Step 1: Creating persistent context: " + contextName);
        
        ContextResult contextResult = agentBay.getContext().get(contextName, true);
        if (!contextResult.isSuccess() || contextResult.getContext() == null) {
            System.err.println("❌ Failed to create context: " + contextResult.getErrorMessage());
            return;
        }
        
        Context context = contextResult.getContext();
        System.out.println("✅ Context created with ID: " + context.getId());
        
        // Step 2: Create BrowserContext with auto-upload enabled
        System.out.println("\n🌐 Step 2: Creating session with BrowserContext");
        BrowserContext browserContext = new BrowserContext(
            context.getId(),  // Use context ID for browser data persistence
            true              // Auto-upload browser data when session ends
        );
        
        CreateSessionParams params = new CreateSessionParams();
        params.setBrowserContext(browserContext);
        params.setImageId("browser_latest");  // Use browser image
        
        SessionResult result = agentBay.create(params);
        
        if (result.isSuccess() && result.getSession() != null) {
            Session session = result.getSession();
            System.out.println("✅ Session created: " + session.getSessionId());
            System.out.println("💡 Browser data will be automatically saved to context: " + context.getName());
            System.out.println("💡 When you delete this session with sync_context=true, browser data");
            System.out.println("   (cookies, localStorage, etc.) will be uploaded to cloud storage.");
            System.out.println("💡 Next time you create a session with the same context ID,");
            System.out.println("   the browser data will be automatically restored!");
            
            // Clean up: Delete session WITHOUT context sync for this demo
            System.out.println("\n🧹 Cleaning up session...");
            session.delete();
            System.out.println("✅ Session deleted");
        } else {
            System.err.println("❌ Failed to create session: " + result.getErrorMessage());
        }
        
        // Clean up context
        try {
            agentBay.getContext().delete(context);
            System.out.println("🧹 Context cleaned up");
        } catch (Exception e) {
            System.err.println("⚠️  Warning: Failed to delete context: " + e.getMessage());
        }
    }
    
    /**
     * Example 2: Browser context with extension support
     * 
     * This example demonstrates:
     * - Creating a BrowserContext with browser extensions
     * - Extensions will be automatically loaded in the browser session
     */
    private static void browserContextWithExtensionsExample(AgentBay agentBay) throws AgentBayException {
        System.out.println("Example 2: Browser Context with Extensions");
        System.out.println(repeat("-", 60));
        
        System.out.println("🔌 Creating ExtensionOption with extension IDs...");
        
        // Create extension option with multiple extensions
        // Note: These extension IDs should be uploaded to your extension context first
        ExtensionOption extensionOption = new ExtensionOption(
            "my_extensions_context",                   // Extension context ID
            Arrays.asList("ext1.zip", "ext2.zip")      // Extension IDs (file names)
        );
        System.out.println("✅ ExtensionOption created: " + extensionOption);
        
        // Create browser context with extensions
        System.out.println("\n🌐 Creating session with extensions...");
        BrowserContext browserContext = new BrowserContext(
            "browser_with_extensions",  // Browser context ID for browser data
            true,                       // Auto-upload browser data
            extensionOption,            // Extension configuration
            null                        // No fingerprint
        );
        
        CreateSessionParams params = new CreateSessionParams();
        params.setBrowserContext(browserContext);
        params.setImageId("browser_latest");
        
        // Add labels to identify this session
        Map<String, String> labels = new HashMap<>();
        labels.put("purpose", "extension_demo");
        labels.put("extension_count", String.valueOf(extensionOption.getExtensionIds().size()));
        params.setLabels(labels);
        
        SessionResult result = agentBay.create(params);
        
        if (result.isSuccess() && result.getSession() != null) {
            Session session = result.getSession();
            System.out.println("✅ Session created: " + session.getSessionId());
            System.out.println("✅ Extensions loaded: " + extensionOption.getExtensionIds());
            System.out.println("💡 Extensions are available at: /tmp/extensions/");
            System.out.println("💡 Each extension will be extracted and loaded automatically");
            
            // Clean up
            System.out.println("\n🧹 Cleaning up...");
            session.delete();
            System.out.println("✅ Session deleted");
        } else {
            System.err.println("❌ Failed to create session: " + result.getErrorMessage());
        }
        
        System.out.println("\n💡 To use this example with real extensions:");
        System.out.println("   1. Upload your extension ZIP files to the cloud context");
        System.out.println("   2. Use the extension file names as extension_ids");
        System.out.println("   3. The extensions will be automatically loaded in the browser");
    }
    
    /**
     * Example 3: Browser context with fingerprint support
     * 
     * This example demonstrates:
     * - Creating a BrowserContext with browser fingerprint
     * - Fingerprint data will be persisted across sessions
     * - Useful for anti-detection scenarios
     */
    private static void browserContextWithFingerprintExample(AgentBay agentBay) throws AgentBayException {
        System.out.println("Example 3: Browser Context with Fingerprint");
        System.out.println(repeat("-", 60));
        
        System.out.println("🔐 Creating fingerprint context...");
        
        // Create fingerprint context for persistent fingerprint data
        BrowserFingerprintContext fingerprintContext = new BrowserFingerprintContext(
            "demo_fingerprint_context"  // Fingerprint context ID
        );
        System.out.println("✅ Fingerprint context created: " + fingerprintContext.getFingerprintContextId());
        
        // Create browser context with fingerprint
        System.out.println("\n🌐 Creating session with fingerprint...");
        BrowserContext browserContext = new BrowserContext(
            "browser_with_fingerprint",  // Browser context ID for browser data
            true,                        // Auto-upload browser data
            null,                        // No extensions
            fingerprintContext           // Fingerprint configuration
        );
        
        CreateSessionParams params = new CreateSessionParams();
        params.setBrowserContext(browserContext);
        params.setImageId("browser_latest");
        
        SessionResult result = agentBay.create(params);
        
        if (result.isSuccess() && result.getSession() != null) {
            Session session = result.getSession();
            System.out.println("✅ Session created: " + session.getSessionId());
            System.out.println("✅ Fingerprint context: " + fingerprintContext.getFingerprintContextId());
            System.out.println("💡 Browser fingerprint data will be saved to: /tmp/browser_fingerprint");
            System.out.println("💡 When you create another session with the same fingerprint context,");
            System.out.println("   the browser will use the same fingerprint (user agent, canvas, etc.)");
            
            // Clean up
            System.out.println("\n🧹 Cleaning up...");
            session.delete();
            System.out.println("✅ Session deleted");
        } else {
            System.err.println("❌ Failed to create session: " + result.getErrorMessage());
        }
        
        System.out.println("\n💡 Benefits of browser fingerprint persistence:");
        System.out.println("   - Consistent browser fingerprint across sessions");
        System.out.println("   - Better anti-detection for web automation");
        System.out.println("   - Reduced risk of being identified as a bot");
    }
    
    /**
     * Example 4: Complete workflow with context synchronization
     * 
     * This example demonstrates the complete workflow:
     * 1. Create a persistent context
     * 2. Create first session with BrowserContext
     * 3. Delete session WITH context sync (uploads browser data)
     * 4. Create second session with same BrowserContext
     * 5. Browser data is automatically restored in the second session
     * 
     * This is equivalent to Python's browser_context_cookie_persistence.py
     */
    private static void completeBrowserContextWorkflowExample(AgentBay agentBay) throws AgentBayException {
        System.out.println("Example 4: Complete Browser Context Workflow");
        System.out.println(repeat("-", 60));
        
        // Create a unique context name
        String contextName = "workflow-demo-" + System.currentTimeMillis();
        
        System.out.println("📦 Step 1: Creating persistent context...");
        ContextResult contextResult = agentBay.getContext().get(contextName, true);
        if (!contextResult.isSuccess() || contextResult.getContext() == null) {
            System.err.println("❌ Failed to create context");
            return;
        }
        
        Context context = contextResult.getContext();
        System.out.println("✅ Context created: " + context.getName() + " (ID: " + context.getId() + ")");
        
        try {
            // Create browser context with all features
            System.out.println("\n🔧 Step 2: Creating comprehensive BrowserContext...");
            
            ExtensionOption extensionOption = new ExtensionOption(
                "demo_extensions",
                Arrays.asList("extension1.zip", "extension2.zip")
            );
            
            BrowserFingerprintContext fingerprintContext = new BrowserFingerprintContext(
                "demo_fingerprint"
            );
            
            BrowserContext browserContext = new BrowserContext(
                context.getId(),      // Browser data context ID
                true,                // Auto-upload enabled
                extensionOption,     // Extensions
                fingerprintContext   // Fingerprint
            );
            
            System.out.println("✅ BrowserContext created with:");
            System.out.println("   - Browser data context: " + context.getId());
            System.out.println("   - Extensions: " + extensionOption.getExtensionIds());
            System.out.println("   - Fingerprint context: " + fingerprintContext.getFingerprintContextId());
            
            // Create first session
            System.out.println("\n🌐 Step 3: Creating first session...");
            CreateSessionParams params = new CreateSessionParams();
            params.setBrowserContext(browserContext);
            params.setImageId("browser_latest");
            
            SessionResult result1 = agentBay.create(params);
            if (!result1.isSuccess() || result1.getSession() == null) {
                System.err.println("❌ Failed to create first session: " + result1.getErrorMessage());
                return;
            }
            
            Session session1 = result1.getSession();
            System.out.println("✅ First session created: " + session1.getSessionId());
            System.out.println("💡 In a real scenario, you would:");
            System.out.println("   - Navigate to websites");
            System.out.println("   - Set cookies and localStorage");
            System.out.println("   - Use browser extensions");
            System.out.println("   - All this data will be saved when session is deleted with sync_context=true");
            
            // Delete first session WITH context sync
            System.out.println("\n📤 Step 4: Deleting first session WITH context sync...");
            DeleteResult deleteResult = agentBay.delete(session1, true);  // sync_context=true
            
            if (deleteResult.isSuccess()) {
                System.out.println("✅ First session deleted (RequestID: " + deleteResult.getRequestId() + ")");
                System.out.println("✅ Browser data uploaded to cloud storage");
            } else {
                System.err.println("❌ Failed to delete session: " + deleteResult.getErrorMessage());
                return;
            }
            
            // Wait for context sync to complete
            System.out.println("\n⏳ Waiting for context synchronization to complete...");
            Thread.sleep(3000);
            System.out.println("✅ Context sync completed");
            
            // Create second session with same context
            System.out.println("\n🌐 Step 5: Creating second session with same BrowserContext...");
            SessionResult result2 = agentBay.create(params);
            
            if (result2.isSuccess() && result2.getSession() != null) {
                Session session2 = result2.getSession();
                System.out.println("✅ Second session created: " + session2.getSessionId());
                System.out.println("✅ Browser data automatically restored from cloud storage!");
                System.out.println("💡 All cookies, localStorage, extensions, and fingerprint from");
                System.out.println("   the first session are now available in this session");
                
                // Clean up second session
                System.out.println("\n🧹 Cleaning up second session...");
                session2.delete();
                System.out.println("✅ Second session deleted");
            } else {
                System.err.println("❌ Failed to create second session");
            }
            
        } catch (InterruptedException e) {
            System.err.println("❌ Thread interrupted: " + e.getMessage());
            Thread.currentThread().interrupt();
        } finally {
            // Clean up context
            try {
                agentBay.getContext().delete(context);
                System.out.println("🧹 Context cleaned up");
            } catch (Exception e) {
                System.err.println("⚠️  Warning: Failed to delete context: " + e.getMessage());
            }
        }
        
        System.out.println("\n🎯 Key Takeaways:");
        System.out.println("   1. BrowserContext enables persistent browser data across sessions");
        System.out.println("   2. Set auto_upload=true to automatically save data when session ends");
        System.out.println("   3. Use sync_context=true when deleting session to upload data");
        System.out.println("   4. Next session with same context_id will restore all data");
        System.out.println("   5. Supports extensions and fingerprint persistence");
    }
}

