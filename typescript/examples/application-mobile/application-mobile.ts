import { AgentBay } from '../../src';
import { log, logError } from '../../src/utils/logger';
import { getTestApiKey } from '../../tests/utils/test-helpers';

// Mobile App represents a mobile application in the system
interface MobileApp {
  name: string;
  start_cmd: string;
  stop_cmd?: string;
  work_directory?: string;
}

// Mobile Process represents a running mobile process in the system
interface MobileProcess {
  pid: number;
  pname: string;
  cmdline?: string;
  path?: string;
}

async function main() {
  // Get API key from environment variable or use default value for testing
  const apiKey = getTestApiKey();

  // Initialize the AgentBay client
  const agentBay = new AgentBay({ apiKey });

  // Create a new mobile session
  log('\nCreating a new mobile session...');
  const createResponse = await agentBay.create({imageId:'mobile_latest'});
  const session = createResponse.session;
  log(`\nMobile session created with ID: ${session.sessionId}`);
  log(`Create Session RequestId: ${createResponse.requestId}`);

  try {
    // Mobile Application Management Examples
    log('\n=== Mobile Application Management Examples ===');

    // Get installed mobile applications
    log('\nGetting installed mobile applications...');
    try {
      const appsResponse = await session.application.getInstalledApps(true, false, true);
      log(`Found ${appsResponse.data.length} installed mobile applications`);
      log(`Get Installed Apps RequestId: ${appsResponse.requestId}`);

      // Print the first 5 mobile apps or fewer if less than 5 are available
      const count = Math.min(appsResponse.data.length, 5);
      for (let i = 0; i < count; i++) {
        const app = appsResponse.data[i];
        log(`Mobile App ${i + 1}: ${app.name}`);
        if (app.start_cmd) {
          log(`  Start Command: ${app.start_cmd}`);
        }
        if (app.stop_cmd) {
          log(`  Stop Command: ${app.stop_cmd}`);
        }
      }
    } catch (error) {
      log(`Error getting installed mobile apps: ${error}`);
    }

    // Start mobile application with simple command (Python example style)
    log('\nStarting mobile application with simple command...');
    try {
      // This matches the Python example: session.application.start_app("monkey -p com.autonavi.minimap -c android.intent.category.LAUNCHER 1")
      const startCmd = "monkey -p com.autonavi.minimap -c android.intent.category.LAUNCHER 1";
      log(`Starting mobile app with command: ${startCmd}`);

      const startResponse = await session.application.startApp(startCmd);
      log(`Start Mobile App RequestId: ${startResponse.requestId}`);
      log(`Started ${startResponse.data.length} mobile processes`);

      // Print started processes
      if (startResponse.data.length > 0) {
        startResponse.data.forEach((proc: MobileProcess, index: number) => {
          log(`Mobile Process ${index + 1}: ${proc.pname} (PID: ${proc.pid})`);
          if (proc.cmdline) {
            log(`  Command Line: ${proc.cmdline}`);
          }
        });
      }
    } catch (error) {
      log(`Error starting mobile app: ${error}`);
    }

    // Start mobile application with activity (Python example style)
    log('\nStarting mobile application with activity...');
    try {
      // This matches the Python example with activity parameter
      const appPackage = "com.xingin.xhs";
      const appActivity = "com.xingin.outside.activity.VivoOutsideFeedActivity";
      const activityStartCmd = `monkey -p ${appPackage} -c android.intent.category.LAUNCHER 1`;

      log(`Starting mobile app with activity: ${appActivity}`);
      log(`Start command: ${activityStartCmd}`);

      const activityStartResponse = await session.application.startApp(
        activityStartCmd,
        "", // empty work_directory like Python example
        appActivity
      );
      log(`Start Mobile App with Activity RequestId: ${activityStartResponse.requestId}`);
      log(`Started ${activityStartResponse.data.length} mobile processes with activity`);

      // Print started processes with activity
      if (activityStartResponse.data.length > 0) {
        activityStartResponse.data.forEach((proc: MobileProcess, index: number) => {
          log(`Mobile Process with Activity ${index + 1}: ${proc.pname} (PID: ${proc.pid})`);
        });
      }
    } catch (error) {
      log(`Error starting mobile app with activity: ${error}`);
    }

    // Stop mobile application by command (Python example style)
    log('\nStopping mobile application by command...');
    try {
      // This matches the Python example: session.application.stop_app_by_cmd("am force-stop com.sankuai.meituan")
      const stopCmd = "am force-stop com.sankuai.meituan";
      log(`Stopping mobile app with command: ${stopCmd}`);

      const stopResponse = await session.application.stopAppByCmd(stopCmd);
      log('Mobile application stopped by command successfully');
      log(`Stop Mobile App by Cmd RequestId: ${stopResponse.requestId}`);
    } catch (error) {
      log(`Error stopping mobile app by command: ${error}`);
    }

    // Demonstrate complete mobile workflow
    log('\n=== Complete Mobile Workflow Example ===');
    try {
      // Step 1: Get installed apps
      log('Step 1: Getting mobile installed applications...');
      const workflowAppsResponse = await session.application.getInstalledApps(true, false, true);
      log(`Found ${workflowAppsResponse.data.length} mobile apps in workflow`);

      // Step 2: Start mobile app (simple command)
      log('Step 2: Starting mobile app with simple command...');
      const workflowStartCmd = "monkey -p com.autonavi.minimap -c android.intent.category.LAUNCHER 1";
      const workflowStartResponse = await session.application.startApp(workflowStartCmd);
      log(`Started mobile app in workflow: ${workflowStartResponse.data.length} processes`);

      // Step 3: Start mobile app with activity
      log('Step 3: Starting mobile app with activity...');
      const workflowAppPackage = "com.xingin.xhs";
      const workflowAppActivity = "com.xingin.outside.activity.VivoOutsideFeedActivity";
      const workflowActivityStartCmd = `monkey -p ${workflowAppPackage} -c android.intent.category.LAUNCHER 1`;

      const workflowActivityStartResponse = await session.application.startApp(
        workflowActivityStartCmd,
        "",
        workflowAppActivity
      );
      log(`Started mobile app with activity in workflow: ${workflowActivityStartResponse.data.length} processes`);

      // Step 4: Stop mobile app
      log('Step 4: Stopping mobile app...');
      const workflowStopCmd = "am force-stop com.sankuai.meituan";
      const workflowStopResponse = await session.application.stopAppByCmd(workflowStopCmd);
      log('Mobile app stopped successfully in workflow');

      log('Mobile workflow completed successfully!');
    } catch (error) {
      log(`Error in mobile workflow: ${error}`);
    }


  } finally {
    // Clean up by deleting the mobile session when we're done
    log('\nDeleting the mobile session...');
    try {
      const deleteResponse = await agentBay.delete(session);
      log('Mobile session deleted successfully');
      log(`Delete Session RequestId: ${deleteResponse.requestId}`);
    } catch (error) {
      log(`Error deleting mobile session: ${error}`);
    }
  }
}

main().catch(error => {
  logError('Error in mobile application example execution:', error);
  process.exit(1);
});
