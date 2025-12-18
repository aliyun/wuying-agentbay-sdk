/**
 * Integration tests for Computer window management functionality
 * This test requires:
 * 1. AGENTBAY_API_KEY environment variable
 * 2. Real AgentBay session (windows_latest image preferred for window tests)
 */

import * as fs from 'fs';
import * as path from 'path';
import * as https from 'https';
import * as http from 'http';
import { AgentBay } from '../../src/agent-bay';
import { logInfo } from '../../src/utils/logger';
import { Computer } from '../../src/computer/computer';
import { any, object } from 'zod';

// Helper function to save screenshot from URL
async function saveScreenshotFromURL(screenshotURL: string, filename: string): Promise<void> {
  // Get the project root directory (go up from tests/integration to typescript root)
  const currentDir = process.cwd();
  const typescriptRoot = path.resolve(currentDir, 'typescript');
  const screenshotDir = path.join(typescriptRoot, 'screenshots');
  
  // Create screenshots directory if it doesn't exist
  if (!fs.existsSync(screenshotDir)) {
    fs.mkdirSync(screenshotDir, { recursive: true });
  }

  logInfo(`DEBUG: Downloading screenshot from URL: ${screenshotURL}`);

  return new Promise((resolve, reject) => {
    const client = screenshotURL.startsWith('https:') ? https : http;
    
    client.get(screenshotURL, (response) => {
      if (response.statusCode !== 200) {
        reject(new Error(`Failed to download screenshot: HTTP ${response.statusCode}`));
        return;
      }

      const chunks: Buffer[] = [];
      
      response.on('data', (chunk) => {
        chunks.push(chunk);
      });
      
      response.on('end', () => {
        const imageData = Buffer.concat(chunks);
        
        // Validate that we have some image data
        if (imageData.length === 0) {
          reject(new Error('Downloaded image data is empty'));
          return;
        }

        // Write to file
        const filePath = path.join(screenshotDir, filename);
        fs.writeFileSync(filePath, imageData);
        resolve();
      });
      
      response.on('error', (error) => {
        reject(new Error(`Failed to download screenshot: ${error.message}`));
      });
    }).on('error', (error) => {
      reject(new Error(`Failed to download screenshot from URL: ${error.message}`));
    });
  });
}

describe('Computer Windows Integration Tests', () => {
  let agentBay: AgentBay;
  let session: any;
  let calculatorWindowID: number = 0;

  beforeAll(async () => {
    // Skip if no API key provided
    const apiKey = process.env.AGENTBAY_API_KEY;
    if (!apiKey) {
      logInfo('Skipping integration test: AGENTBAY_API_KEY not set');
      return;
    }

    // Create AgentBay client
    agentBay = new AgentBay({ apiKey });

    // Create session with windows image for window testing
    logInfo('Creating session for window integration test...');
    const sessionResult = await agentBay.create({ imageId: 'linux_latest' });
    
    expect(sessionResult.success).toBe(true);
    expect(sessionResult.session).toBeDefined();
    
    session = sessionResult.session;
    logInfo(`Created session: ${session.sessionId}`);

    // Wait for session to be fully ready (desktop environment)
    await new Promise(resolve => setTimeout(resolve, 10000));
  });

  afterAll(async () => {
    if (session) {
      logInfo('Cleaning up: Deleting session...');
      const deleteResult = await session.delete();
      if (deleteResult?.success) {
        logInfo(`Session ${session.sessionId} deleted successfully`);
      }
    }
  });

  test('Computer Windows Integration Test', async () => {
    if (!session) return;

    // Step 1: Start Calculator App
    logInfo('Step 1: Testing StartApp - Finding Calculator in installed apps...');
    
    let startCmd = '', pname = ''; // Default fallback
    
    try {
      const installedApps = await session.computer.getInstalledApps(true, false, true);
      
      if (installedApps.success && installedApps.data) {
        
        // Look for Calculator app
        for (const app of installedApps.data) {
          if (app.name && (app.name.toLowerCase().includes('calculator'))) {
            startCmd = app.startCmd;
            pname = app.name;
            logInfo(`Found Calculator app: ${app.name} (${app.startCmd})`);
            break;
          }
        }
        if(!startCmd){
          startCmd = installedApps.data[0].startCmd
          pname = installedApps.data[0].name
        }
      }
    } catch (error) {
      logInfo(`GetInstalledApps failed: ${error}, using default calc.exe`);
    }
    
    logInfo(`Starting Calculator with command: ${startCmd}`);
    const startResult = await session.computer.startApp(startCmd, '', '');

    expect(startResult.success).toBe(true);
    expect(startResult.data).toBeDefined();
    expect(Array.isArray(startResult.data)).toBe(true);
    expect(startResult.data.length).toBeGreaterThan(0);

    if (startResult.data.length > 0) {
      const process = startResult.data[0];
      logInfo(`Started Calculator process: ${process.pname} (PID: ${process.pid})`);
      expect(process.pname.toLowerCase()).toBeDefined();
      expect(process.pid).toBeGreaterThan(0);
    }

    // Wait for app to be fully loaded
    await new Promise(resolve => setTimeout(resolve, 3000));

    // Step 2: List Root Windows
    logInfo('Step 2: Testing ListRootWindows...');
    const windowsResult = await session.computer.listRootWindows();

    expect(windowsResult.success).toBe(true);
    expect(windowsResult.windows).toBeDefined();
    expect(Array.isArray(windowsResult.windows)).toBe(true);
    for(const window of windowsResult.windows) {
      logInfo(`Window: ${window.title} (ID: ${window.windowId})`);
    }

    // Find Calculator window
    expect(windowsResult.windows.length).toBeGreaterThan(0)
    calculatorWindowID = windowsResult.windows[0].windowId
    expect(calculatorWindowID).toBeDefined();
    expect(calculatorWindowID).toBeGreaterThan(0);

    // Step 3: Activate Window
    logInfo('Step 3: Testing ActivateWindow...');
    const activateResult = await session.computer.activateWindow(calculatorWindowID);
    
    expect(activateResult.success).toBe(true);
    logInfo(`Successfully activated Calculator window (ID: ${calculatorWindowID})`);

    // Wait for activation to take effect
    await new Promise(resolve => setTimeout(resolve, 1000));

    // Step 4: Get Active Window Validation
    logInfo('Step 4: Testing GetActiveWindow validation...');
    const activeWindowResult = await session.computer.getActiveWindow();
    
    expect(activeWindowResult.success).toBe(true);
    expect(activeWindowResult.window).toBeDefined();

    if (activeWindowResult.window) {
      logInfo(`Active window: ${activeWindowResult.window.title} (ID: ${activeWindowResult.window.windowId})`);
      // The active window should be Calculator (though title might vary by locale)
      const isCalculator = activeWindowResult.window.title.toLowerCase().includes('calculator')||
                          activeWindowResult.window.windowId === calculatorWindowID;
      expect(isCalculator).toBe(true);
    }

    // Step 5: Focus Mode
    logInfo('Step 5: Testing FocusMode...');

    // Enable focus mode
    let focusResult = await session.computer.focusMode(true);
    expect(focusResult.success).toBe(true);
    logInfo('Focus mode enabled successfully');

    // Wait a moment
    await new Promise(resolve => setTimeout(resolve, 1000));

    // Disable focus mode
    focusResult = await session.computer.focusMode(false);
    expect(focusResult.success).toBe(true);
    logInfo('Focus mode disabled successfully');

    // Step 6: Maximize Window and Screenshot
    logInfo('Step 6: Testing MaximizeWindow and Screenshot...');

    // Maximize window
    const maximizeResult = await session.computer.maximizeWindow(calculatorWindowID);
    expect(maximizeResult.success).toBe(true);
    logInfo('Calculator window maximized successfully');

    // Wait for maximize to take effect
    await new Promise(resolve => setTimeout(resolve, 2000));

    // Take screenshot
    let screenshot = await session.computer.screenshot();
    expect(screenshot.success).toBe(true);
    
    if (screenshot.success && screenshot.data) {
      try {
        await saveScreenshotFromURL(screenshot.data, 'calculator_maximized.png');
        logInfo('Maximized screenshot saved as calculator_maximized.png');
      } catch (error) {
        logInfo(`Warning: Failed to save maximized screenshot: ${error}`);
      }
    } else {
      logInfo(`Screenshot failed or returned empty data: ${screenshot.errorMessage}`);
    }

    // Step 7: Minimize Window and Screenshot
    logInfo('Step 7: Testing MinimizeWindow and Screenshot...');

    // Minimize window
    const minimizeResult = await session.computer.minimizeWindow(calculatorWindowID);
    expect(minimizeResult.success).toBe(true);
    logInfo('Calculator window minimized successfully');

    // Wait for minimize to take effect
    await new Promise(resolve => setTimeout(resolve, 2000));

    // Take screenshot
    screenshot = await session.computer.screenshot();
    expect(screenshot.success).toBe(true);
    
    if (screenshot.success && screenshot.data) {
      try {
        await saveScreenshotFromURL(screenshot.data, 'calculator_minimized.png');
        logInfo('Minimized screenshot saved as calculator_minimized.png');
      } catch (error) {
        logInfo(`Warning: Failed to save minimized screenshot: ${error}`);
      }
    } else {
      logInfo(`Screenshot failed or returned empty data: ${screenshot.errorMessage}`);
    }

    // Step 8: Restore Window and Screenshot
    logInfo('Step 8: Testing RestoreWindow and Screenshot...');

    // Restore window
    const restoreResult = await session.computer.restoreWindow(calculatorWindowID);
    expect(restoreResult.success).toBe(true);
    logInfo('Calculator window restored successfully');

    // Wait for restore to take effect
    await new Promise(resolve => setTimeout(resolve, 2000));

    // Take screenshot
    screenshot = await session.computer.screenshot();
    expect(screenshot.success).toBe(true);
    
    if (screenshot.success && screenshot.data) {
      try {
        await saveScreenshotFromURL(screenshot.data, 'calculator_restored.png');
        logInfo('Restored screenshot saved as calculator_restored.png');
      } catch (error) {
        logInfo(`Warning: Failed to save restored screenshot: ${error}`);
      }
    } else {
      logInfo(`Screenshot failed or returned empty data: ${screenshot.errorMessage}`);
    }

    // Step 9: Resize Window and Screenshot
    logInfo('Step 9: Testing ResizeWindow and Screenshot...');

    // Resize window to 600x400
    const resizeResult = await session.computer.resizeWindow(calculatorWindowID, 600, 400);
    expect(resizeResult.success).toBe(true);
    logInfo('Calculator window resized to 600x400 successfully');

    // Wait for resize to take effect
    await new Promise(resolve => setTimeout(resolve, 2000));

    // Take screenshot
    screenshot = await session.computer.screenshot();
    expect(screenshot.success).toBe(true);
    
    if (screenshot.success && screenshot.data) {
      try {
        await saveScreenshotFromURL(screenshot.data, 'calculator_resized.png');
        logInfo('Resized screenshot saved as calculator_resized.png');
      } catch (error) {
        logInfo(`Warning: Failed to save resized screenshot: ${error}`);
      }
    } else {
      logInfo(`Screenshot failed or returned empty data: ${screenshot.errorMessage}`);
    }

    // Step 10: Fullscreen Window and Screenshot
    logInfo('Step 10: Testing FullscreenWindow and Screenshot...');

    // Make window fullscreen
    const fullscreenResult = await session.computer.fullscreenWindow(calculatorWindowID);
    expect(fullscreenResult.success).toBe(true);
    logInfo('Calculator window set to fullscreen successfully');

    // Wait for fullscreen to take effect
    await new Promise(resolve => setTimeout(resolve, 2000));

    // Take screenshot
    screenshot = await session.computer.screenshot();
    expect(screenshot.success).toBe(true);
    
    if (screenshot.success && screenshot.data) {
      try {
        await saveScreenshotFromURL(screenshot.data, 'calculator_fullscreen.png');
        logInfo('Fullscreen screenshot saved as calculator_fullscreen.png');
      } catch (error) {
        logInfo(`Warning: Failed to save fullscreen screenshot: ${error}`);
      }
    } else {
      logInfo(`Screenshot failed or returned empty data: ${screenshot.errorMessage}`);
    }

    // Step 11: Test ListVisibleApps
    logInfo('Step 11: Testing ListVisibleApps...');
    const visibleAppsResult = await session.computer.listVisibleApps();
    
    expect(visibleAppsResult.success).toBe(true);
    expect(visibleAppsResult.data).toBeDefined();
    expect(Array.isArray(visibleAppsResult.data)).toBe(true);
    for (const app of visibleAppsResult.data) {
      logInfo(`  - ${app.pname} (PID: ${app.pid})`);
      
      // Verify that each app has the expected properties with camelCase naming
      expect(app.pname).toBeDefined();
      expect(typeof app.pname).toBe('string');
      expect(app.pid).toBeDefined();
      expect(typeof app.pid).toBe('number');
      expect(app.pid).toBeGreaterThan(0);
      
      // cmdLine is optional but should be string if present
      if (app.cmdLine !== undefined) {
        expect(typeof app.cmdLine).toBe('string');
      }
    }
    
    // Verify that Calculator is in the visible apps list (since it should still be running)
    const calculatorApp = visibleAppsResult.data.find((app: any) => 
      app.pname.toLowerCase().includes('calc') || 
      app.pname.toLowerCase().includes('calculator') ||
      app.pname === pname.toLowerCase()
    );
    
    if (calculatorApp) {
      logInfo(`Calculator found in visible apps: ${calculatorApp.pname} (PID: ${calculatorApp.pid})`);
      expect(calculatorApp.pname).toBeDefined();
      expect(calculatorApp.pid).toBeGreaterThan(0);
    } else {
      logInfo('Note: Calculator not found in visible apps (may have been closed or minimized)');
    }

    // Step 12: Cleanup Calculator
    logInfo('Step 12: Cleaning up - Closing Calculator...');
    try {
      const closeResult = await session.computer.closeWindow(calculatorWindowID);
      if (closeResult.success) {
        logInfo('Calculator window closed successfully');
      } else {
        logInfo('Warning: CloseWindow returned false');
      }
    } catch (error) {
      logInfo(`Warning: Failed to close Calculator window: ${error}`);
    }
  }, 120000); // Increased timeout for the complete test
});
