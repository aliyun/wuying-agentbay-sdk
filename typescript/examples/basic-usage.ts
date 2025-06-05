import { AgentBay } from '../src';
async function main() {
  try {
    // In a real environment, you would get this from process.env.AGENTBAY_API_KEY
    const apiKey = 'your_api_key_here';
    console.log('Note: In a production environment, use an environment variable for the API key.');

    // Initialize the AgentBay client
    const agentBay = new AgentBay({ apiKey });

    // Create a new session
    console.log('Creating a new session...');
    const session = await agentBay.create();
    console.log(`Session created with ID: ${session.sessionId}`);

    // Execute a command
    console.log('\nExecuting a command...');
    const result = await session.command.executeCommand('ls -la');
    console.log('Command result:', result);

    // Read a file
    console.log('\nReading a file...');
    const content = await session.filesystem.readFile('/etc/hosts');
    console.log(`File content: ${content}`);

    // Execute an ADB shell command (for mobile environments)
    console.log('\nExecuting an ADB shell command...');
    const adbResult = await session.adb.shell('ls /sdcard');
    console.log(`ADB shell result: ${adbResult}`);

    // List all sessions
    console.log('\nListing all sessions...');
    const sessions = await agentBay.list();
    console.log('Available sessions:', sessions);

    // Delete the session
    console.log('\nDeleting the session...');
    await agentBay.delete(session.sessionId);
    console.log('Session deleted successfully');

  } catch (error) {
    console.error('Error:', error);
    // In a Node.js environment, you would use process.exit(1) here
    throw error;
  }
}

main();
