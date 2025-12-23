package com.aliyun.agentbay.examples;

import com.aliyun.agentbay.AgentBay;
import com.aliyun.agentbay.model.AppOperationResult;
import com.aliyun.agentbay.model.BoolResult;
import com.aliyun.agentbay.model.InstalledAppListResult;
import com.aliyun.agentbay.model.ProcessListResult;
import com.aliyun.agentbay.model.SessionResult;
import com.aliyun.agentbay.session.CreateSessionParams;
import com.aliyun.agentbay.session.Session;

/**
 * Example demonstrating Computer application lifecycle management in AgentBay Java SDK
 * 
 * This example shows how to:
 * 1. Get installed applications
 * 2. Start applications with different methods
 * 3. List visible/running applications
 * 4. Stop applications by process name or PID
 * 
 * Note: Some commands may fail if:
 * - The work directory doesn't exist
 * - The command requires dependencies that aren't installed
 * - The command format is incompatible with systemd service tracking
 * 
 * For best results, use simple commands or ensure the work directory and dependencies exist.
 */
public class ComputerStartAppExample {

    public static void main(String[] args) {
        try {
            String apiKey = System.getenv("AGENTBAY_API_KEY");
            if (apiKey == null || apiKey.trim().isEmpty()) {
                System.err.println("Error: AGENTBAY_API_KEY environment variable not set");
                return;
            }

            // Create AgentBay client
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

            // Example 1: Get installed apps
            System.out.println("\n📋 Getting installed applications...");
            InstalledAppListResult installedApps = session.getComputer().getInstalledApps();
            if (installedApps.isSuccess()) {
                System.out.println("✅ Found " + installedApps.getData().size() + " installed app(s)");
                if (!installedApps.getData().isEmpty()) {
                    System.out.println("   First app: " + installedApps.getData().get(0).getName());
                }
            } else {
                System.err.println("❌ Failed to get installed apps: " + installedApps.getErrorMessage());
            }

            // Example 2: Start a simple application (recommended for testing)
            // This is more reliable than complex commands with work directories
            System.out.println("\n🚀 Example 2: Starting a simple application...");
            System.out.println("   Command: sleep 30");
            ProcessListResult simpleStartResult = session.getComputer().startApp("sleep 30");
            
            if (simpleStartResult.isSuccess()) {
                System.out.println("✅ Simple application started successfully!");
                System.out.println("   Request ID: " + simpleStartResult.getRequestId());
                System.out.println("   Started " + simpleStartResult.getData().size() + " process(es)");
                
                // Print process information
                for (int i = 0; i < simpleStartResult.getData().size(); i++) {
                    com.aliyun.agentbay.model.Process process = simpleStartResult.getData().get(i);
                    System.out.println("   Process " + (i + 1) + ":");
                    System.out.println("     PID: " + process.getPid());
                    System.out.println("     Name: " + process.getPname());
                    if (process.getCmdline() != null) {
                        System.out.println("     Command: " + process.getCmdline());
                    }
                }
            } else {
                System.err.println("❌ Failed to start simple application: " + simpleStartResult.getErrorMessage());
                System.err.println("   Error details: " + simpleStartResult.getErrorMessage());
            }

            // Example 3: Start an application with command and work directory
            // First, we need to ensure the directory exists and npm project is initialized
            System.out.println("\n🚀 Example 3: Starting application with work directory...");
            String workDir = "/tmp/app/react-site-demo-1";
            
            // Step 3.1: Create the work directory
            System.out.println("   📁 Step 3.1: Creating work directory: " + workDir);
            BoolResult mkdirResult = session.getFileSystem().createDirectory(workDir);
            if (mkdirResult.isSuccess()) {
                System.out.println("   ✅ Directory created successfully");
            } else {
                System.err.println("   ⚠️  Failed to create directory: " + mkdirResult.getErrorMessage());
            }
            
            // Step 3.2: Create a minimal package.json with a simple dev script
            System.out.println("   📄 Step 3.2: Creating package.json...");
            String packageJson = "{\n" +
                "  \"name\": \"react-site-demo\",\n" +
                "  \"version\": \"1.0.0\",\n" +
                "  \"scripts\": {\n" +
                "    \"dev\": \"node -e \\\"console.log('Dev server started'); setInterval(() => console.log('Running...'), 5000);\\\"\"\n" +
                "  }\n" +
                "}";
            BoolResult writeResult = session.getFileSystem().writeFile(workDir + "/package.json", packageJson);
            if (writeResult.isSuccess()) {
                System.out.println("   ✅ package.json created successfully");
            } else {
                System.err.println("   ⚠️  Failed to create package.json: " + writeResult.getErrorMessage());
            }
            
            // Step 3.3: Now start the application
            System.out.println("   🚀 Step 3.3: Starting application...");
            System.out.println("   Command: npm run dev");
            System.out.println("   Work Directory: " + workDir);
            
            ProcessListResult startResult = session.getComputer().startApp(
                "npm run dev",
                workDir
            );

            if (startResult.isSuccess()) {
                System.out.println("✅ Application started successfully!");
                System.out.println("   Request ID: " + startResult.getRequestId());
                System.out.println("   Started " + startResult.getData().size() + " process(es)");
                
                // Print process information
                for (int i = 0; i < startResult.getData().size(); i++) {
                    com.aliyun.agentbay.model.Process process = startResult.getData().get(i);
                    System.out.println("   Process " + (i + 1) + ":");
                    System.out.println("     PID: " + process.getPid());
                    System.out.println("     Name: " + process.getPname());
                    if (process.getCmdline() != null) {
                        System.out.println("     Command: " + process.getCmdline());
                    }
                }
            } else {
                System.err.println("❌ Failed to start application: " + startResult.getErrorMessage());
                System.err.println("   Note: The directory and package.json were created, but npm run dev might still fail");
                System.err.println("   if npm is not installed or the command format is incompatible with systemd.");
            }

            // Example 4: List visible apps
            System.out.println("\n👀 Example 4: Listing visible applications...");
            ProcessListResult visibleApps = session.getComputer().listVisibleApps();
            if (visibleApps.isSuccess()) {
                System.out.println("✅ Found " + visibleApps.getData().size() + " visible app(s)");
                if (!visibleApps.getData().isEmpty()) {
                    System.out.println("   First visible app: " + visibleApps.getData().get(0).getPname());
                }
            } else {
                System.err.println("❌ Failed to list visible apps: " + visibleApps.getErrorMessage());
            }

            // Example 5: Stop application by process name (if we started one)
            if (simpleStartResult.isSuccess() && !simpleStartResult.getData().isEmpty()) {
                String processName = simpleStartResult.getData().get(0).getPname();
                System.out.println("\n🛑 Example 5: Stopping application by process name: " + processName);
                AppOperationResult stopResult = session.getComputer().stopAppByPName(processName);
                if (stopResult.isSuccess()) {
                    System.out.println("✅ Application stopped successfully!");
                } else {
                    System.out.println("⚠️  Stop result: " + stopResult.getErrorMessage());
                }
            }

            // Example 6: Stop application by PID (alternative method)
            if (simpleStartResult.isSuccess() && !simpleStartResult.getData().isEmpty()) {
                int pid = simpleStartResult.getData().get(0).getPid();
                System.out.println("\n🛑 Example 6: Stopping application by PID: " + pid);
                AppOperationResult stopResult = session.getComputer().stopAppByPID(pid);
                if (stopResult.isSuccess()) {
                    System.out.println("✅ Application stopped successfully!");
                } else {
                    System.out.println("⚠️  Stop result: " + stopResult.getErrorMessage());
                }
            }

            // Clean up
            System.out.println("\n🧹 Cleaning up...");
            session.delete();
            System.out.println("✅ Session deleted");

        } catch (Exception e) {
            System.err.println("Error: " + e.getMessage());
            e.printStackTrace();
        }
    }
}

