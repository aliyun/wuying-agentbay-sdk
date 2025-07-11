import { AgentBay } from 'wuying-agentbay-sdk';

/**
 * Helper function to truncate long output text
 */
function truncateOutput(output: string, maxLines: number): string {
  const lines = output.split('\n');
  if (lines.length <= maxLines) {
    return output;
  }

  const truncated = lines.slice(0, maxLines);
  return truncated.join('\n') + '\n... (output truncated)';
}

async function main() {
  // Get API key from environment variable or use a placeholder value
  const apiKey = process.env.AGENTBAY_API_KEY || 'akm-xxx'; // Replace with your actual API key
  if (!process.env.AGENTBAY_API_KEY) {
    console.log('Warning: Using placeholder API key. Set AGENTBAY_API_KEY environment variable for production use.');
  }

  // Initialize the AgentBay client
  const agentBay = new AgentBay({ apiKey });

  // Create session parameters with imageId set to code_latest to support code execution
  const params = {
    imageId: 'code_latest'
  };

  // Create a new session
  console.log('\nCreating a new session with code_latest image...');
  const createResponse = await agentBay.create(params);
  const session = createResponse.session;
  console.log(`\nSession created with ID: ${session.sessionId}`);
  console.log(`Create Session RequestId: ${createResponse.requestId}`);

  try {
    // 1. Execute simple shell command
    console.log('\n1. Executing simple shell command (echo)...');
    try {
      const echoCommand = "echo 'Hello from AgentBay SDK!'";
      const echoResponse = await session.command.executeCommand(echoCommand);
      console.log(`Echo command output:\n${echoResponse.output}`);
      console.log(`Execute Command RequestId: ${echoResponse.requestId}`);
    } catch (error) {
      console.log(`Error executing echo command: ${error}`);
    }

    // 2. Execute command with longer timeout
    console.log('\n2. Executing command with custom timeout...');
    try {
      const lsCommand = "ls -la /etc";
      const timeoutMs = 5000; // 5 seconds timeout
      const lsResponse = await session.command.executeCommand(lsCommand, timeoutMs);
      console.log(`Directory listing (first few lines):\n${truncateOutput(lsResponse.output, 5)}`);
      console.log(`Execute Command with Timeout RequestId: ${lsResponse.requestId}`);
    } catch (error) {
      console.log(`Error executing ls command: ${error}`);
    }

    // 3. Execute Python code
    console.log('\n3. Running Python code...');
    try {
      const pythonCode = `
import platform
import sys

print(f"Python version: {platform.python_version()}")
print(f"System info: {platform.system()} {platform.release()}")
print("Working with numbers in Python:")
for i in range(1, 6):
    print(f"{i} squared is {i*i}")
`;
      const pythonResponse = await session.command.runCode(pythonCode, "python");
      console.log(`Python code output:\n${pythonResponse.result}`);
      console.log(`Run Python Code RequestId: ${pythonResponse.requestId}`);

      if (!pythonResponse.result || pythonResponse.result.trim() === '') {
        console.log('Warning: Python code execution returned empty result');
        if (pythonResponse.errorMessage) {
          console.log(`Error message: ${pythonResponse.errorMessage}`);
        }
      }
    } catch (error) {
      console.log(`Error running Python code: ${error}`);
    }

    // 4. Execute JavaScript code with custom timeout
    console.log('\n4. Running JavaScript code with custom timeout...');
    try {
      const jsCode = `
console.log("JavaScript execution in AgentBay");
console.log("Basic operations:");

// Simple array operations
const numbers = [1, 2, 3, 4, 5];
console.log("Original array:", numbers);

const doubled = numbers.map(n => n * 2);
console.log("Doubled values:", doubled);

const sum = numbers.reduce((total, n) => total + n, 0);
console.log("Sum of array:", sum);
`;
      const timeoutS = 10; // 10 seconds timeout
      const jsResponse = await session.command.runCode(jsCode, "javascript", timeoutS);
      console.log(`JavaScript code output:\n${jsResponse.result}`);
      console.log(`Run JavaScript Code RequestId: ${jsResponse.requestId}`);
    } catch (error) {
      console.log(`Error running JavaScript code: ${error}`);
    }

    // 5. Execute a more complex shell command sequence
    console.log('\n5. Executing a sequence of shell commands...');
    try {
      const complexCommand = `
echo "Current working directory:"
pwd
echo "\nSystem information:"
uname -a
echo "\nMemory usage:"
free -h 2>/dev/null || vm_stat 2>/dev/null || echo "Memory info not available"
echo "\nDisk usage:"
df -h | head -5
`;
      const complexResponse = await session.command.executeCommand(complexCommand);
      console.log(`Complex command output:\n${truncateOutput(complexResponse.output, 15)}`);
      console.log(`Execute Complex Command RequestId: ${complexResponse.requestId}`);
    } catch (error) {
      console.log(`Error executing complex command: ${error}`);
    }

    console.log('\nCommand examples completed successfully!');

  } finally {
    // Clean up by deleting the session when we're done
    console.log('\nDeleting the session...');
    try {
      const deleteResponse = await agentBay.delete(session);
      console.log('Session deleted successfully');
      console.log(`Delete Session RequestId: ${deleteResponse.requestId}`);
    } catch (error) {
      console.log(`Error deleting session: ${error}`);
    }
  }
}

// Execute the main function
main().catch(error => {
  console.error('Error in main execution:', error);
  process.exit(1);
}); 