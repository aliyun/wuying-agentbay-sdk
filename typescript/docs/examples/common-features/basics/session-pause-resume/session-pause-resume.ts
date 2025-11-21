import { AgentBay, Session, log, logError, newCreateSessionParams } from 'wuying-agentbay-sdk'

/**
 * Pause and resume a session
 * 
 * This example demonstrates how to pause and resume a session using the AgentBay SDK.
 * Pausing a session puts it into a dormant state, consuming fewer resources while
 * maintaining its state. Resuming a session brings it back to an active state.
 */
async function pauseAndResumeSession() {
  // Initialize the AgentBay client
  const agentBay = new AgentBay({ apiKey: process.env.AGENTBAY_API_KEY });

  try {
    // Create a session with labels for identification
    const params = newCreateSessionParams().withLabels({
      project: 'pause-resume-example',
      environment: 'development',
      purpose: 'demonstration'
    });

    log('Creating session...');
    const createResult = await agentBay.create(params);

    if (createResult.success && createResult.session) {
      const session = createResult.session;
      log(`✅ Session created successfully with ID: ${session.sessionId}`);
      log(`📎 Request ID: ${createResult.requestId}`);

      // Perform some work in the session before pausing
      log('Performing some work in the session...');
      const commandResult = await session.command.executeCommand('echo "Hello from paused session!"');
      if (commandResult.success) {
        log(`💻 Command output: ${commandResult.output}`);
      }

      // Pause the session
      log('\n⏸️  Pausing session...');
      const pauseResult = await agentBay.pauseAsync(session);
      
      if (pauseResult.success) {
        log(`✅ Session pause initiated successfully`);
        log(`📎 Pause Request ID: ${pauseResult.requestId}`);
        
        // Check session status after pause
        const sessionStatusAfterPause = await agentBay.getSession(session.sessionId);
        if (sessionStatusAfterPause.success && sessionStatusAfterPause.data) {
          log(`📊 Session status after pause: ${sessionStatusAfterPause.data.status || 'Unknown'}`);
        }
      } else {
        log(`❌ Failed to pause session: ${pauseResult.errorMessage}`);
        // Continue with the example even if pause fails
      }

      // Wait a bit for the pause to complete
      log('\n⏳ Waiting for session to pause...');
      await new Promise(resolve => setTimeout(resolve, 5000));

      // Resume the session
      log('\n▶️  Resuming session...');
      const resumeResult = await agentBay.resumeAsync(session);
      
      if (resumeResult.success) {
        log(`✅ Session resume initiated successfully`);
        log(`📎 Resume Request ID: ${resumeResult.requestId}`);
        
        // Check session status after resume
        const sessionStatusAfterResume = await agentBay.getSession(session.sessionId);
        if (sessionStatusAfterResume.success && sessionStatusAfterResume.data) {
          log(`📊 Session status after resume: ${sessionStatusAfterResume.data.status || 'Unknown'}`);
        }
      } else {
        log(`❌ Failed to resume session: ${resumeResult.errorMessage}`);
        // Continue with the example even if resume fails
      }

      // Wait a bit for the resume to complete
      log('\n⏳ Waiting for session to resume...');
      await new Promise(resolve => setTimeout(resolve, 5000));

      // Perform some work in the session after resuming
      log('\nPerforming some work in the resumed session...');
      const commandResultAfterResume = await session.command.executeCommand('echo "Hello from resumed session!"');
      if (commandResultAfterResume.success) {
        log(`💻 Command output: ${commandResultAfterResume.output}`);
      }

      // Clean up by deleting the session
      log('\n🧹 Cleaning up - deleting session...');
      const deleteResult = await agentBay.delete(session);
      if (deleteResult.success) {
        log('✅ Session deleted successfully');
      } else {
        log(`❌ Failed to delete session: ${deleteResult.errorMessage}`);
      }
    } else {
      log(`❌ Failed to create session: ${createResult.errorMessage}`);
    }
  } catch (error) {
    logError('Error in pause and resume example:', error);
  }
}

/**
 * Handle non-existent session pause/resume
 * 
 * This example demonstrates how the SDK handles attempts to pause or resume
 * sessions that don't exist.
 */
async function handleNonExistentSession() {
  // Initialize the AgentBay client
  const agentBay = new AgentBay({ apiKey: process.env.AGENTBAY_API_KEY });

  log('\n' + '='.repeat(50));
  log('Handling Non-Existent Session Example');
  log('='.repeat(50));

  // Create a session object with invalid ID
  const fakeSessionId = 'session-nonexistent-12345';
  log(`\nCreating session object for non-existent session: ${fakeSessionId}`);
  
  // Create a real session object with invalid ID
  const fakeSession = new Session(agentBay, fakeSessionId);

  try {
    // Try to pause the non-existent session
    log('⏸️  Attempting to pause non-existent session...');
    const pauseResult = await agentBay.pauseAsync(fakeSession);
    log(`Pause result: Success=${pauseResult.success}, Error=${pauseResult.errorMessage || 'None'}`);
    
    log('▶️  Attempting to resume non-existent session...');
    const resumeResult = await agentBay.resumeAsync(fakeSession);
    log(`Resume result: Success=${resumeResult.success}, Error=${resumeResult.errorMessage || 'None'}`);
  } catch (error) {
    log(`Expected error when handling non-existent session: ${error}`);
  }
}

/**
 * Pause and resume with custom parameters
 * 
 * This example demonstrates how to use custom timeout and polling interval
 * parameters when pausing and resuming sessions.
 */
async function pauseAndResumeWithCustomParameters() {
  // Initialize the AgentBay client
  const agentBay = new AgentBay({ apiKey: process.env.AGENTBAY_API_KEY });

  log('\n' + '='.repeat(50));
  log('Custom Parameters Example');
  log('='.repeat(50));

  try {
    // Create a session
    const params = newCreateSessionParams().withLabels({
      project: 'pause-resume-custom-example',
      environment: 'development',
      purpose: 'custom-parameters'
    });

    log('Creating session with custom parameters example...');
    const createResult = await agentBay.create(params);

    if (createResult.success && createResult.session) {
      const session = createResult.session;
      log(`✅ Session created successfully with ID: ${session.sessionId}`);

      // Pause the session with custom parameters
      // Using shorter timeout and poll interval for demonstration
      log('\n⏸️  Pausing session with custom parameters (timeout=30s, pollInterval=1s)...');
      const pauseResult = await agentBay.pauseAsync(session, 30, 1);
      
      if (pauseResult.success) {
        log(`✅ Session pause with custom parameters initiated successfully`);
        log(`📎 Request ID: ${pauseResult.requestId}`);
        
        // Check session status after pause
        const sessionStatusAfterPause = await agentBay.getSession(session.sessionId);
        if (sessionStatusAfterPause.success && sessionStatusAfterPause.data) {
          log(`📊 Session status after pause: ${sessionStatusAfterPause.data.status || 'Unknown'}`);
        }
      } else {
        log(`❌ Failed to pause session with custom parameters: ${pauseResult.errorMessage}`);
      }

      // Wait a bit
      await new Promise(resolve => setTimeout(resolve, 3000));

      // Resume the session with custom parameters
      log('\n▶️  Resuming session with custom parameters (timeout=30s, pollInterval=1s)...');
      const resumeResult = await agentBay.resumeAsync(session, 30, 1);
      
      if (resumeResult.success) {
        log(`✅ Session resume with custom parameters initiated successfully`);
        log(`📎 Request ID: ${resumeResult.requestId}`);
        
        // Check session status after resume
        const sessionStatusAfterResume = await agentBay.getSession(session.sessionId);
        if (sessionStatusAfterResume.success && sessionStatusAfterResume.data) {
          log(`📊 Session status after resume: ${sessionStatusAfterResume.data.status || 'Unknown'}`);
        }
      } else {
        log(`❌ Failed to resume session with custom parameters: ${resumeResult.errorMessage}`);
      }

      // Clean up
      log('\n🧹 Cleaning up - deleting session...');
      const deleteResult = await agentBay.delete(session);
      if (deleteResult.success) {
        log('✅ Session deleted successfully');
      } else {
        log(`❌ Failed to delete session: ${deleteResult.errorMessage}`);
      }
    } else {
      log(`❌ Failed to create session: ${createResult.errorMessage}`);
    }
  } catch (error) {
    logError('Error in custom parameters example:', error);
  }
}

/**
 * Run all examples
 */
async function main() {
  log('Session Pause and Resume Examples');
  log('=================================');

  await pauseAndResumeSession();
  await handleNonExistentSession();
  await pauseAndResumeWithCustomParameters();
}

main().catch(error => {
  logError('Error in main:', error);
  process.exit(1);
});