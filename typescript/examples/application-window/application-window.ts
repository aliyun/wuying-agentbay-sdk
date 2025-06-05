import { AgentBay } from '../../src/agent-bay';
import { Session } from '../../src/session';

// Helper function to get the minimum of two numbers
function min(x: number, y: number): number {
  return x < y ? x : y;
}

async function main() {
  try {
    // Get API key from environment variable or use a default value for testing
    const apiKey = process.env.AGENTBAY_API_KEY || 'akm-xxx'; // Replace with your actual API key for testing
    if (!process.env.AGENTBAY_API_KEY) {
      console.log('Warning: Using default API key. Set AGENTBAY_API_KEY environment variable for production use.');
    }

    // Initialize the AgentBay client
    const agentBay = new AgentBay({ apiKey });

    // Create a new session with default parameters
    console.log('\nCreating a new session...');
    const session = await agentBay.create();
    console.log(`\nSession created with ID: ${session.sessionId}`);

    // Application Management Examples
    console.log('\n=== Application Management Examples ===');

    // Get installed applications
    console.log('\nGetting installed applications...');
    try {
      const apps = await session.application.getInstalledApps(true, false, true);
      console.log(`Found ${apps.length} installed applications`);
      // Print the first 3 apps or fewer if less than 3 are available
      const count = min(apps.length, 3);
      for (let i = 0; i < count; i++) {
        console.log(`App ${i + 1}: ${apps[i].name}`);
      }
    } catch (error) {
      console.log(`Error getting installed apps: ${error}`);
    }

    // List visible applications
    console.log('\nListing visible applications...');
    try {
      const visibleApps = await session.application.listVisibleApps();
      console.log(`Found ${visibleApps.length} visible applications`);
      // Print the first 3 apps or fewer if less than 3 are available
      const count = min(visibleApps.length, 3);
      for (let i = 0; i < count; i++) {
        console.log(`Process ${i + 1}: ${visibleApps[i].pname} (PID: ${visibleApps[i].pid})`);
      }
    } catch (error) {
      console.log(`Error listing visible apps: ${error}`);
    }

    // Window Management Examples
    console.log('\n=== Window Management Examples ===');

    // List root windows
    console.log('\nListing root windows...');
    let rootWindows: any[] = [];
    try {
      rootWindows = await session.window.listRootWindows();
      console.log(`Found ${rootWindows.length} root windows`);
      // Print the first 3 windows or fewer if less than 3 are available
      const count = min(rootWindows.length, 3);
      for (let i = 0; i < count; i++) {
        console.log(`Window ${i + 1}: ${rootWindows[i].title} (ID: ${rootWindows[i].window_id})`);
      }
    } catch (error) {
      console.log(`Error listing root windows: ${error}`);
    }

    // Get active window
    console.log('\nGetting active window...');
    try {
      const activeWindow = await session.window.getActiveWindow();
      console.log(`Active window: ${activeWindow.title} (ID: ${activeWindow.window_id}, Process: ${activeWindow.pname}, PID: ${activeWindow.pid})`);
    } catch (error) {
      console.log(`Error getting active window: ${error}`);
    }

    // Window operations
    if (rootWindows.length > 0) {
      const windowId = rootWindows[0].window_id;

      // Activate window
      console.log(`\nActivating window with ID ${windowId}...`);
      try {
        await session.window.activateWindow(windowId);
        console.log('Window activated successfully');
      } catch (error) {
        console.log(`Error activating window: ${error}`);
      }

      // Maximize window
      console.log(`\nMaximizing window with ID ${windowId}...`);
      try {
        await session.window.maximizeWindow(windowId);
        console.log('Window maximized successfully');
      } catch (error) {
        console.log(`Error maximizing window: ${error}`);
      }

      // Minimize window
      console.log(`\nMinimizing window with ID ${windowId}...`);
      try {
        await session.window.minimizeWindow(windowId);
        console.log('Window minimized successfully');
      } catch (error) {
        console.log(`Error minimizing window: ${error}`);
      }

      // Restore window
      console.log(`\nRestoring window with ID ${windowId}...`);
      try {
        await session.window.restoreWindow(windowId);
        console.log('Window restored successfully');
      } catch (error) {
        console.log(`Error restoring window: ${error}`);
      }

      // Resize window
      console.log(`\nResizing window with ID ${windowId} to 800x600...`);
      try {
        await session.window.resizeWindow(windowId, 800, 600);
        console.log('Window resized successfully');
      } catch (error) {
        console.log(`Error resizing window: ${error}`);
      }
    }

    // Focus mode
    // Enable focus mode
    console.log('\nEnabling focus mode...');
    try {
      await session.window.focusMode(true);
      console.log('Focus mode enabled successfully');
    } catch (error) {
      console.log(`Error enabling focus mode: ${error}`);
    }

    // Disable focus mode
    console.log('\nDisabling focus mode...');
    try {
      await session.window.focusMode(false);
      console.log('Focus mode disabled successfully');
    } catch (error) {
      console.log(`Error disabling focus mode: ${error}`);
    }

    // Delete the session
    console.log('\nDeleting the session...');
    try {
      await agentBay.delete(session.sessionId);
      console.log('Session deleted successfully');
    } catch (error) {
      console.log(`Error deleting session: ${error}`);
      process.exit(1);
    }
  } catch (error) {
    console.log(`Error: ${error}`);
    process.exit(1);
  }
}

main();
