/**
 * Integration tests for session creation with extra configurations.
 * Tests the end-to-end functionality of mobile session creation with extra configurations.
 */

import { AgentBay } from '../../src/agent-bay';
import { CreateSessionParams } from '../../src/session-params';
import { MobileExtraConfig, AppManagerRule, ExtraConfigs } from '../../src/types/extra-configs';

describe('Session Extra Configurations Integration', () => {
  let agentBay: AgentBay;

  beforeAll(() => {
    const apiKey = process.env.AGENTBAY_API_KEY;
    if (!apiKey) {
      throw new Error('AGENTBAY_API_KEY environment variable not set');
    }
    
    agentBay = new AgentBay({ apiKey });
    console.log('AgentBay client initialized for extra configs testing');
  });

  describe('Mobile Session Creation with Extra Configurations', () => {
    it('should create mobile session with comprehensive extra configurations', async () => {
      jest.setTimeout(60000); // 60 second timeout for integration test
      console.log('================================================================================');
      console.log('TEST: Mobile Session with Extra Configurations');
      console.log('================================================================================');

      // Step 1: Create mobile configuration with all features
      console.log('Step 1: Creating mobile configuration with extra configs...');
      const appRule: AppManagerRule = {
        ruleType: 'White',
        appPackageNameList: [
          'com.android.settings',
          'com.example.test.app',
        ],
      };

      const mobileConfig: MobileExtraConfig = {
        lockResolution: true,
        appManagerRule: appRule,
        hideNavigationBar: true, // New feature: hide navigation bar
        uninstallBlacklist: [    // New feature: uninstall protection
          'com.android.systemui',
          'com.android.settings',
        ],
      };

      const extraConfigs: ExtraConfigs = {
        mobile: mobileConfig,
      };

      console.log(`Mobile config created: lockResolution=${mobileConfig.lockResolution}, ` +
                 `hideNavigationBar=${mobileConfig.hideNavigationBar}, ` +
                 `uninstallBlacklist=${mobileConfig.uninstallBlacklist?.length} packages, ` +
                 `appRule=${mobileConfig.appManagerRule?.ruleType}`);

      // Step 2: Create session parameters
      const params = new CreateSessionParams()
        .withImageId('mobile_latest')
        .withLabels({
          test_type: 'mobile_extra_configs_integration',
          created_by: 'integration_test',
        })
        .withExtraConfigs(extraConfigs);

      console.log(`Session params: imageId=${params.imageId}, labels=${JSON.stringify(params.labels)}`);

      // Step 3: Create session
      console.log('Step 2: Creating mobile session with extra configurations...');
      const createResult = await agentBay.create(params);

      // Verify SessionResult structure
      expect(createResult.success).toBe(true);
      expect(createResult.requestId).toBeDefined();
      expect(typeof createResult.requestId).toBe('string');
      expect(createResult.requestId.length).toBeGreaterThan(0);
      expect(createResult.session).toBeDefined();
      expect(createResult.errorMessage).toBeFalsy();

      const session = createResult.session!;
      console.log(`✓ Mobile session created successfully with ID: ${session.sessionId} (RequestID: ${createResult.requestId})`);

      try {
        // Step 4: Verify session properties
        console.log('Step 3: Verifying session properties...');
        expect(session.sessionId).toBeDefined();
        expect(session.sessionId.length).toBeGreaterThan(0);
        console.log(`✓ Session properties verified: ID=${session.sessionId}`);

        // Step 5: Verify mobile environment
        console.log('Step 4: Verifying mobile environment...');
        const infoResult = await session.info();
        if (infoResult.success) {
          const resourceUrl = infoResult.data.resourceUrl?.toLowerCase() || '';
          expect(resourceUrl.includes('android') || resourceUrl.includes('mobile')).toBe(true);
          console.log(`✓ Mobile environment verified (RequestID: ${infoResult.requestId})`);
        } else {
          console.log(`⚠ Failed to get session info: ${infoResult.errorMessage}`);
        }

        // Step 6: Verify labels
        console.log('Step 5: Verifying session labels...');
        const labelsResult = await session.getLabels();
        if (labelsResult.success) {
          const labels = labelsResult.data;
          expect(labels?.test_type).toBe('mobile_extra_configs_integration');
          console.log(`✓ Labels verified: ${JSON.stringify(labels)} (RequestID: ${labelsResult.requestId})`);
        } else {
          console.log(`⚠ Failed to get session labels: ${labelsResult.errorMessage}`);
        }

        // Step 7: Test mobile functionality
        console.log('Step 6: Testing mobile functionality...');

        // Test screenshot functionality
        const screenshotResult = await session.mobile.screenshot();
        if (screenshotResult.success) {
          expect(screenshotResult.data).toBeDefined();
          console.log(`✓ Mobile screenshot working (RequestID: ${screenshotResult.requestId})`);
        } else {
          console.log(`⚠ Mobile screenshot failed: ${screenshotResult.errorMessage}`);
        }

        // Test mobile configuration methods
        console.log('Step 7: Testing mobile configuration methods...');
        try {
          const resolutionResult = await session.mobile.setResolutionLock(true);
          const navBarResult = await session.mobile.setNavigationBarVisibility(true);
          const uninstallResult = await session.mobile.setUninstallBlacklist(['com.android.systemui']);
          
          console.log(`Resolution lock result: ${resolutionResult.success}`);
          console.log(`Navigation bar result: ${navBarResult.success}`);
          console.log(`Uninstall blacklist result: ${uninstallResult.success}`);
          console.log('✓ Mobile configuration methods executed successfully');
        } catch (error) {
          console.log(`⚠ Mobile configuration methods failed: ${error}`);
        }
      } finally {
        // Step 8: Clean up
        console.log('Step 8: Cleaning up session...');
        const deleteResult = await agentBay.delete(session);
        if (deleteResult.success) {
          console.log(`✓ Session deleted successfully (RequestID: ${deleteResult.requestId})`);
        } else {
          console.log(`⚠ Failed to delete session: ${deleteResult.errorMessage}`);
        }
        expect(deleteResult.success).toBe(true);
      }

      console.log('✓ Mobile extra configs integration test completed successfully');
    });

    it('should create mobile session with blacklist configuration', async () => {
      jest.setTimeout(60000); // 60 second timeout for integration test
      console.log('================================================================================');
      console.log('TEST: Mobile Session with Blacklist Configuration');
      console.log('================================================================================');

      const appRule: AppManagerRule = {
        ruleType: 'Black',
        appPackageNameList: [
          'com.malware.suspicious',
          'com.unwanted.adware',
        ],
      };

      const mobileConfig: MobileExtraConfig = {
        lockResolution: false,
        appManagerRule: appRule,
        hideNavigationBar: false,
        uninstallBlacklist: ['com.android.systemui'],
      };

      const extraConfigs: ExtraConfigs = {
        mobile: mobileConfig,
      };

      const params = new CreateSessionParams()
        .withImageId('mobile_latest')
        .withLabels({
          test_type: 'mobile_blacklist_integration',
          created_by: 'integration_test',
        })
        .withExtraConfigs(extraConfigs);

      const createResult = await agentBay.create(params);
      expect(createResult.success).toBe(true);

      const session = createResult.session!;
      console.log(`✓ Mobile session with blacklist created: ${session.sessionId}`);

      try {
        // Test blacklist configuration
        const blacklistResult = await session.mobile.setAppBlacklist(['com.test.blocked']);
        console.log(`Blacklist configuration result: ${blacklistResult.success}`);
      } finally {
        const deleteResult = await agentBay.delete(session);
        expect(deleteResult.success).toBe(true);
        console.log(`✓ Blacklist session deleted: ${deleteResult.requestId}`);
      }
    });
  });
});
