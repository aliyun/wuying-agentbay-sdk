/**
 * Browser Extension Management Example (TypeScript)
 *
 * This example demonstrates how to use the ExtensionsService to manage browser extensions
 * and integrate them with browser sessions in TypeScript. It shows the complete workflow of:
 * 1. Uploading browser extensions to the cloud
 * 2. Creating extension options for browser integration
 * 3. Creating browser sessions with extensions
 * 4. Testing extension functionality
 * 5. Managing extension lifecycle
 */

import { AgentBay, ExtensionsService, CreateSessionParams, BrowserContext, BrowserOption } from 'wuying-agentbay-sdk';
import { chromium } from 'playwright';

async function extensionManagementDemo(): Promise<boolean> {
    // Get API key from environment
    const apiKey = process.env.AGENTBAY_API_KEY;
    if (!apiKey) {
        console.error("Error: AGENTBAY_API_KEY environment variable not set");
        return false;
    }

    // Initialize AgentBay client
    const agentBay = new AgentBay({ apiKey });
    console.log("AgentBay client initialized");

    // Create a unique context name for extension management
    const extensionContextName = `extension-demo-${Date.now()}`;
    
    try {
        // Initialize Extensions Service with named context
        console.log(`Initializing Extensions Service with context: ${extensionContextName}`);
        const extensionsService = new ExtensionsService(agentBay, extensionContextName);
        
        // For this demo, we'll show the code structure without actually uploading files
        // In a real scenario, you would have actual extension ZIP files
        console.log("Note: This demo shows the code structure. Replace '/path/to/your-extension.zip' with actual extension files.");
        
        // Example 1: Basic extension upload and usage
        console.log("\n=== Example 1: Basic Extension Usage ===");
        
        // In a real implementation, you would uncomment these lines:
        // const extension = await extensionsService.create("/path/to/your-extension.zip");
        // console.log(`Extension uploaded: ${extension.name} (ID: ${extension.id})`);
        
        // For demo purposes, we'll simulate an extension ID
        const simulatedExtensionId = "ext_demo_12345";
        console.log(`Simulated extension ID: ${simulatedExtensionId}`);
        
        // Create extension option for browser integration
        const extOption = extensionsService.createExtensionOption([simulatedExtensionId]);
        console.log("Extension option created successfully");
        
        // Create browser session with extension
        const browserContext = new BrowserContext(
            `extension-session-${Date.now()}`,
            true,
            extOption
        );
        
        const params = new CreateSessionParams()
            .withLabels({ purpose: "extension_demo", type: "example" })
            .withBrowserContext(browserContext);
        
        console.log("Browser session with extension would be created here");
        // In a real implementation:
        // const sessionResult = await agentBay.create(params);
        // const session = sessionResult.session;
        // console.log("Extension session created successfully!");
        
        // Example 2: Working with multiple extensions
        console.log("\n=== Example 2: Multiple Extensions ===");
        
        // Simulate multiple extensions
        const simulatedExtensionIds = [
            "ext_demo_12345",
            "ext_demo_67890",
            "ext_demo_abcde"
        ];
        
        // Create session with all extensions
        const extOptionMulti = extensionsService.createExtensionOption(simulatedExtensionIds);
        console.log(`Created extension option with ${simulatedExtensionIds.length} extensions`);
        
        const browserContextMulti = new BrowserContext(
            `multi-extension-session-${Date.now()}`,
            true,
            extOptionMulti
        );
        
        const paramsMulti = new CreateSessionParams()
            .withBrowserContext(browserContextMulti);
        
        console.log("Multi-extension session would be created here");
        
        // Example 3: Extension development workflow
        console.log("\n=== Example 3: Extension Development Workflow ===");
        
        class ExtensionDevelopmentWorkflow {
            private agentBay: AgentBay;
            private extensionsService: ExtensionsService;
            private extensionId: string | null = null;
            
            constructor(agentBayClient: AgentBay, contextName: string) {
                this.agentBay = agentBayClient;
                this.extensionsService = new ExtensionsService(agentBayClient, contextName);
            }
            
            async uploadExtension(extensionPath: string): Promise<string> {
                /** Upload extension for development testing. */
                console.log(`Uploading extension from: ${extensionPath}`);
                // In real implementation:
                // const extension = await this.extensionsService.create(extensionPath);
                // this.extensionId = extension.id;
                // console.log(`Extension uploaded: ${extension.name}`);
                
                // For demo, simulate success
                this.extensionId = "ext_dev_12345";
                console.log(`Simulated extension uploaded with ID: ${this.extensionId}`);
                return this.extensionId;
            }
            
            async createTestSession() {
                /** Create a browser session for testing. */
                if (!this.extensionId) {
                    console.log("No extension uploaded yet");
                    return null;
                }
                
                const extOption = this.extensionsService.createExtensionOption([this.extensionId]);
                
                const sessionParams = new CreateSessionParams()
                    .withLabels({ purpose: "extension_development", type: "test" })
                    .withBrowserContext(new BrowserContext(
                        `dev-session-${Date.now()}`,
                        true,
                        extOption
                    ));
                
                console.log("Test session would be created here");
                // In real implementation:
                // return await this.agentBay.create(sessionParams);
                return { sessionId: `session_${Date.now()}` };
            }
            
            async updateAndTest(newExtensionPath: string) {
                /** Update extension and create new test session. */
                if (!this.extensionId) {
                    console.log("No extension to update");
                    return null;
                }
                
                console.log(`Updating extension with: ${newExtensionPath}`);
                // In real implementation:
                // const updatedExt = await this.extensionsService.update(this.extensionId, newExtensionPath);
                // console.log(`Extension updated: ${updatedExt.name}`);
                
                console.log("Simulated extension update completed");
                
                // Create new test session with updated extension
                return await this.createTestSession();
            }
            
            async cleanup() {
                /** Clean up development resources. */
                if (this.extensionId) {
                    console.log(`Deleting extension: ${this.extensionId}`);
                    // In real implementation:
                    // await this.extensionsService.delete(this.extensionId);
                }
                
                console.log("Cleaning up extension service");
                // In real implementation:
                // await this.extensionsService.cleanup();
            }
        }
        
        // Usage of ExtensionDevelopmentWorkflow
        const workflow = new ExtensionDevelopmentWorkflow(agentBay, `dev-context-${Date.now()}`);
        
        // Development cycle
        console.log("Starting extension development cycle...");
        await workflow.uploadExtension("/path/to/extension-v1.zip");
        const session1 = await workflow.createTestSession();
        console.log(`Created test session: ${JSON.stringify(session1)}`);
        
        // Update and test again
        const session2 = await workflow.updateAndTest("/path/to/extension-v2.zip");
        console.log(`Created updated test session: ${JSON.stringify(session2)}`);
        
        // Clean up
        await workflow.cleanup();
        console.log("Development workflow completed");
        
        // Example 4: Automated extension testing
        console.log("\n=== Example 4: Automated Extension Testing ===");
        
        async function runExtensionTests(extensionPaths: string[]): Promise<boolean> {
            /** Run automated tests on multiple extensions. */
            console.log("Running automated extension tests...");
            
            // In real implementation:
            // const extensionsService = new ExtensionsService(agentBay);
            
            try {
                // Upload all test extensions
                const extensionIds: string[] = [];
                for (let i = 0; i < extensionPaths.length; i++) {
                    const path = extensionPaths[i];
                    console.log(`Uploading extension: ${path}`);
                    // In real implementation:
                    // const ext = await extensionsService.create(path);
                    // extensionIds.push(ext.id);
                    
                    // For demo, simulate extension IDs
                    const extId = `ext_test_${i}_${Date.now()}`;
                    extensionIds.push(extId);
                    console.log(`Simulated extension uploaded: ${extId}`);
                }
                
                // Create test session
                const extOption = extensionsService.createExtensionOption(extensionIds);
                
                const sessionParams = new CreateSessionParams()
                    .withLabels({ purpose: "automated_testing", type: "extension_test" })
                    .withBrowserContext(new BrowserContext(
                        `test-session-${Date.now()}`,
                        true,
                        extOption
                    ));
                
                console.log("Test session with all extensions would be created here");
                // In real implementation:
                // const sessionResult = await agentBay.create(sessionParams);
                // const session = sessionResult.session;
                
                console.log(`Testing ${extensionIds.length} extensions in session`);
                return true;
                
            } catch (error) {
                console.error(`Error during extension testing: ${error}`);
                return false;
            } finally {
                console.log("Cleaning up test resources");
                // In real implementation:
                // await extensionsService.cleanup();
            }
        }
        
        // Run automated tests
        const testExtensionPaths = [
            "/path/to/test-extension-1.zip",
            "/path/to/test-extension-2.zip",
            "/path/to/test-extension-3.zip"
        ];
        
        const testSuccess = await runExtensionTests(testExtensionPaths);
        if (testSuccess) {
            console.log("Automated extension tests completed successfully!");
        } else {
            console.log("Automated extension tests failed!");
        }
        
        console.log("\nDemo completed successfully!");
        return true;
        
    } catch (error) {
        console.error("An error occurred:", error);
        return false;
    } finally {
        // Clean up - in a real implementation you might want to keep the context
        // for future use, but for demo purposes we'll show how to clean up
        console.log("\n=== Cleanup ===");
        console.log("In a real implementation, you would call await extensionsService.cleanup() here");
        // await extensionsService.cleanup();
    }
}

// Run the demo
extensionManagementDemo().then(success => {
    if (success) {
        console.log("Extension management demo completed successfully!");
    } else {
        console.log("Extension management demo failed!");
    }
}).catch(console.error);