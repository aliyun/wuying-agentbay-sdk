/**
 * Mobile GetAdbUrl Example
 * 
 * This example demonstrates how to use the getAdbUrl method to retrieve
 * an ADB (Android Debug Bridge) connection URL for a mobile session.
 */

import { AgentBay } from 'wuying-agentbay-sdk';

async function main() {
  // Get API key from environment variable
  const apiKey = process.env.AGENTBAY_API_KEY;
  if (!apiKey) {
    console.error('Error: AGENTBAY_API_KEY environment variable is not set');
    console.error('Please set it with: export AGENTBAY_API_KEY=your_api_key');
    process.exit(1);
  }

  console.log('=== Mobile GetAdbUrl Example ===\n');

  // Initialize AgentBay client
  const client = new AgentBay({ apiKey });

  // Create a mobile session
  console.log('Creating mobile session...');
  const sessionResult = await client.create({
    imageId: 'mobile_latest' // Must use mobile_latest for ADB functionality
  });

  if (!sessionResult.session) {
    console.error('Failed to create session');
    process.exit(1);
  }

  const session = sessionResult.session;
  console.log(`✅ Session created successfully`);
  console.log(`   Session ID: ${session.sessionId}`);
  console.log(`   Image ID: ${session.imageId}\n`);

  try {
    // Get ADB URL with public key
    // Note: In production, you should use your actual ADB public key
    // This is a desensitized example key
    const adbkeyPub = "QAAAAM0muSn7yQCY...your_adb_public_key...EAAQAA=";

    console.log('Getting ADB connection URL...');
    const result = await session.mobile.getAdbUrl(adbkeyPub);

    if (result.success) {
      console.log(`✅ ADB URL retrieved successfully`);
      console.log(`   URL: ${result.data}`);
      console.log(`   Request ID: ${result.requestId}\n`);
      console.log('You can now connect to the mobile device using:');
      console.log(`   ${result.data}`);
    } else {
      console.error(`❌ Failed to get ADB URL`);
      console.error(`   Error: ${result.errorMessage}`);
      console.error(`   Request ID: ${result.requestId}`);
      process.exit(1);
    }

    console.log('\n=== Example completed successfully ===');
  } finally {
    // Cleanup: Delete session
    console.log('\nCleaning up session...');
    const deleteResult = await session.delete();
    if (deleteResult.success) {
      console.log(`✅ Session deleted successfully (RequestID: ${deleteResult.requestId})`);
    } else {
      console.warn(`Warning: Failed to delete session: ${deleteResult.errorMessage}`);
    }
  }
}

// Run the example
main().catch((error) => {
  console.error('Error:', error);
  process.exit(1);
});

