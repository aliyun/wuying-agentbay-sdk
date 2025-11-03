// @ts-nocheck
/**
 * Browser Type Selection Example
 *
 * This example demonstrates how to select between Chrome and Chromium browsers
 * when using computer use images in AgentBay.
 *
 * Features demonstrated:
 * - Chrome browser selection
 * - Chromium browser selection
 * - Default browser (undefined)
 * - Browser type verification
 * - Configuration comparison
 *
 * Note: The browserType option is only available for computer use images.
 */

import { AgentBay, CreateSessionParams, BrowserOption } from 'wuying-agentbay-sdk';
import { chromium } from 'playwright';

/**
 * Test a specific browser type configuration
 */
async function testBrowserType(
  browserType: 'chrome' | 'chromium' | undefined,
  description: string
): Promise<void> {
  console.log('\n' + '='.repeat(60));
  console.log(`Testing: ${description}`);
  console.log('='.repeat(60));

  const apiKey = process.env.AGENTBAY_API_KEY;
  if (!apiKey) {
    throw new Error('AGENTBAY_API_KEY environment variable not set');
  }

  const agentBay = new AgentBay({ apiKey });

  // Create session with computer use image
  console.log('\n1. Creating session with computer use image...');
  const params: CreateSessionParams = { imageId: 'browser_latest' };
  const result = await agentBay.create(params);

  if (!result.success || !result.session) {
    throw new Error('Failed to create session');
  }

  const session = result.session;
  console.log(`   ✓ Session created: ${session.getSessionId()}`);

  try {
    // Initialize browser with specified type
    console.log(`\n2. Initializing browser with type: ${browserType || 'default (undefined)'}...`);
    
    // Using plain object (recommended)
    const option: BrowserOption = {
      browserType: browserType,
      viewport: { width: 1920, height: 1080 }
    };

    const success = await session.browser.initializeAsync(option);
    if (!success) {
      throw new Error('Browser initialization failed');
    }

    console.log('   ✓ Browser initialized successfully');

    // Get endpoint URL
    const endpointUrl = session.browser.getEndpointUrl();
    console.log(`\n3. CDP endpoint: ${String(endpointUrl).substring(0, 50)}...`);

    // Connect Playwright and verify browser
    console.log('\n4. Connecting to browser via CDP...');
    const browser = await chromium.connectOverCDP(endpointUrl);
    const context = browser.contexts()[0];
    const page = await context.newPage();

    console.log('   ✓ Connected successfully');
    console.log('\n5. Verifying browser configuration...');

    // Navigate to a page that shows browser info
    await page.goto('https://www.whatismybrowser.com/');
    await page.waitForLoadState('networkidle');

    // Get browser information
    const userAgent = await page.evaluate(() => (navigator as any).userAgent);
    const viewportWidth = await page.evaluate(() => (window as any).innerWidth);
    const viewportHeight = await page.evaluate(() => (window as any).innerHeight);

    console.log('\n   Browser Information:');
    console.log(`   - User Agent: ${userAgent.substring(0, 80)}...`);
    console.log(`   - Viewport: ${viewportWidth} x ${viewportHeight}`);
    console.log(`   - Configured Type: ${browserType || 'default'}`);

    // Check if Chrome or Chromium is in user agent
    if (userAgent.includes('Chrome')) {
      const detected = userAgent.includes('Chromium') ? 'Chromium' : 'Chrome';
      console.log(`   - Detected Browser: ${detected}`);
    }

    await browser.close();

    console.log(`\n   ✓ Test completed successfully for ${description}`);

  } finally {
    console.log('\n6. Cleaning up...');
    session.delete();
    console.log('   ✓ Session deleted');
  }
}

/**
 * Main function to run all browser type examples
 */
async function main(): Promise<void> {
  console.log('Browser Type Selection Example');
  console.log('='.repeat(60));
  console.log('\nThis example demonstrates browser type selection in AgentBay.');
  console.log('Note: browserType is only available for computer use images.');

  // Test 1: Chrome browser
  await testBrowserType('chrome', 'Chrome Browser (Google Chrome)');

  await new Promise(resolve => setTimeout(resolve, 2000)); // Brief pause

  // Test 2: Chromium browser
  await testBrowserType('chromium', 'Chromium Browser (Open Source)');

  await new Promise(resolve => setTimeout(resolve, 2000)); // Brief pause

  // Test 3: Default (undefined)
  await testBrowserType(undefined, 'Default Browser (Platform decides)');

  console.log('\n' + '='.repeat(60));
  console.log('All browser type tests completed successfully!');
  console.log('='.repeat(60));

  // Summary
  console.log('\nSummary:');
  console.log('- Chrome: Use when you need Google Chrome specific features');
  console.log('- Chromium: Use for open-source, lighter resource usage');
  console.log('- Default (undefined): Let the platform choose the optimal browser');
  console.log('\nBest Practice: Use undefined unless you have a specific requirement');
}

/**
 * Quick example showing the most common usage
 */
async function quickExample(): Promise<void> {
  console.log('\n' + '='.repeat(60));
  console.log('Quick Example: Using Chrome Browser');
  console.log('='.repeat(60));

  const apiKey = process.env.AGENTBAY_API_KEY;
  if (!apiKey) {
    throw new Error('AGENTBAY_API_KEY not set');
  }

  const agentBay = new AgentBay({ apiKey });

  // Create session
  const params: CreateSessionParams = { imageId: 'browser_latest' };
  const result = await agentBay.create(params);
  if (!result.success || !result.session) {
    throw new Error('Failed to create session');
  }

  const session = result.session;

  try {
    // Simply specify browserType in BrowserOption
    const option: BrowserOption = {
      browserType: 'chrome'
    };

    const success = await session.browser.initializeAsync(option);

    if (success) {
      console.log('✓ Chrome browser initialized successfully');

      // Get endpoint and use with Playwright
      const endpointUrl = session.browser.getEndpointUrl();
      const browser = await chromium.connectOverCDP(endpointUrl);
      const page = await browser.contexts()[0].newPage();

      await page.goto('https://example.com');
      const title = await page.title();
      console.log(`✓ Page title: ${title}`);

      await browser.close();
    }
  } finally {
    session.delete();
  }
}

/**
 * Type-safe example showing all options
 */
async function typeSafeExample(): Promise<void> {
  console.log('\n' + '='.repeat(60));
  console.log('Type-Safe Example: Using TypeScript Types');
  console.log('='.repeat(60));

  const apiKey = process.env.AGENTBAY_API_KEY;
  if (!apiKey) {
    throw new Error('AGENTBAY_API_KEY not set');
  }

  const agentBay = new AgentBay({ apiKey });
  const params: CreateSessionParams = { imageId: 'browser_latest' };
  const result = await agentBay.create(params);

  if (!result.success || !result.session) {
    throw new Error('Failed to create session');
  }

  const session = result.session;

  try {
    // TypeScript ensures type safety
    const browserTypes: Array<'chrome' | 'chromium' | undefined> = [
      'chrome',
      'chromium',
      undefined
    ];

    for (const type of browserTypes) {
      console.log(`\nTesting with type: ${type || 'undefined'}`);
      
      // Type-safe option creation
      const option: BrowserOption = {
        browserType: type,
        viewport: { width: 1920, height: 1080 }
      };

      const success = await session.browser.initializeAsync(option);
      console.log(`  ✓ Initialization: ${success ? 'Success' : 'Failed'}`);

      if (success) {
        // Verify configuration
        const currentOption = session.browser.getOption();
        if (currentOption) {
          console.log(`  ✓ Configured type: ${currentOption.browserType || 'undefined'}`);
        }
      }

      // Brief pause between iterations
      await new Promise(resolve => setTimeout(resolve, 1000));
    }

    console.log('\n✓ Type-safe example completed');

  } finally {
    session.delete();
  }
}

// Run the main example
main()
  .then(() => process.exit(0))
  .catch(error => {
    console.error('Error:', error.message);
    process.exit(1);
  });

