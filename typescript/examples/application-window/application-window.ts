import { AgentBay } from '../../src';
import { log, logError } from '../../src/utils/logger';
import { getTestApiKey } from '../../tests/utils/test-helpers';

// Window represents a window in the system
interface Window {
  window_id: number;
  title: string;
  absolute_upper_left_x?: number;
  absolute_upper_left_y?: number;
  width?: number;
  height?: number;
  pid?: number;
  pname?: string;
  child_windows?: Window[];
}

// App represents an application in the system
interface App {
  name: string;
  path?: string;
  description?: string;
}

// Process represents a running process in the system
interface Process {
  pid: number;
  pname: string;
}

async function main() {
  // Get API key from environment variable or use default value for testing
  const apiKey = getTestApiKey();

  // Initialize the AgentBay client
  const agentBay = new AgentBay({ apiKey });

  // Create a new session with default parameters
  log('\nCreating a new session...');
  const createResponse = await agentBay.create({imageId:'linux_latest'});
  const session = createResponse.data;
  log(`\nSession created with ID: ${session.sessionId}`);
  log(`Create Session RequestId: ${createResponse.requestId}`);

  try {
    // Application Management Examples
    log('\n=== Application Management Examples ===');

    // Get installed applications
    log('\nGetting installed applications...');
    try {
      const appsResponse = await session.Application.getInstalledApps(true, false, true);
      log(`Found ${appsResponse.data.length} installed applications`);
      log(`Get Installed Apps RequestId: ${appsResponse.requestId}`);

      // Print the first 3 apps or fewer if less than 3 are available
      const count = Math.min(appsResponse.data.length, 3);
      for (let i = 0; i < count; i++) {
        log(`App ${i + 1}: ${appsResponse.data[i].name}`);
      }
    } catch (error) {
      log(`Error getting installed apps: ${error}`);
    }

    // List visible applications
    log('\nListing visible applications...');
    try {
      const visibleAppsResponse = await session.Application.listVisibleApps();
      log(`Found ${visibleAppsResponse.data.length} visible applications`);
      log(`List Visible Apps RequestId: ${visibleAppsResponse.requestId}`);

      // Print the first 3 apps or fewer if less than 3 are available
      const count = Math.min(visibleAppsResponse.data.length, 3);
      for (let i = 0; i < count; i++) {
        log(`Process ${i + 1}: ${visibleAppsResponse.data[i].pname} (PID: ${visibleAppsResponse.data[i].pid})`);
      }
    } catch (error) {
      log(`Error listing visible apps: ${error}`);
    }

    // Window Management Examples
    log('\n=== Window Management Examples ===');

    // List root windows
    log('\nListing root windows...');
    try {
      const rootWindowsResponse = await session.window.listRootWindows();
      log(`Found ${rootWindowsResponse.data.length} root windows`);
      log(`List Root Windows RequestId: ${rootWindowsResponse.requestId}`);

      // Print the first 3 windows or fewer if less than 3 are available
      const count = Math.min(rootWindowsResponse.data.length, 3);
      for (let i = 0; i < count; i++) {
        log(`Window ${i + 1}: ${rootWindowsResponse.data[i].title} (ID: ${rootWindowsResponse.data[i].window_id})`);
      }
    } catch (error) {
      log(`Error listing root windows: ${error}`);
    }

    // Get active window
    log('\nGetting active window...');
    try {
      const activeWindowResponse = await session.window.getActiveWindow();
      log(`Get Active Window RequestId: ${activeWindowResponse.requestId}`);
      if (activeWindowResponse.data) {
        log(`Active window: ${activeWindowResponse.data.title} (ID: ${activeWindowResponse.data.window_id})`);
      } else {
        log('No active window found');
      }
    } catch (error) {
      log(`Error getting active window: ${error}`);
    }

    // Use the active window info instead of trying to get window by ID
    log('\nGetting window details from active window...');
    try {
      const activeWindowResponse = await session.window.getActiveWindow();
      log(`Get Active Window Details RequestId: ${activeWindowResponse.requestId}`);

      if (activeWindowResponse.data) {
        log(`Window details: ${activeWindowResponse.data.title} (ID: ${activeWindowResponse.data.window_id})`);
        if (activeWindowResponse.data.width && activeWindowResponse.data.height) {
          log(`Window dimensions: ${activeWindowResponse.data.width}x${activeWindowResponse.data.height}`);
        }
      } else {
        log('No active window details available');
      }
    } catch (error) {
      log(`Error getting window details: ${error}`);
    }

  } finally {
    // Clean up by deleting the session when we're done
    log('\nDeleting the session...');
    try {
      const deleteResponse = await agentBay.delete(session);
      log('Session deleted successfully');
      log(`Delete Session RequestId: ${deleteResponse.requestId}`);
    } catch (error) {
      log(`Error deleting session: ${error}`);
    }
  }
}

main().catch(error => {
  logError('Error in main execution:', error);
  process.exit(1);
});
