/**
 * Integration tests for Mobile Simulate functionality.
 * Tests the complete E2E flow with real API.
 * 
 * Note: These tests create real sessions and should not be run concurrently
 * to avoid rate limiting and resource exhaustion.
 */

import { AgentBay } from '../../src/agent-bay';
import { MobileSimulateService } from '../../src/mobile-simulate';
import { MobileSimulateMode } from '../../src/types/extra-configs';
import { log } from "../../src/utils/logger";
import * as fs from 'fs';
import * as path from 'path';

const MOBILE_INFO_MODEL_A = "SM-A505F";
const MOBILE_INFO_MODEL_B = "moto g stylus 5G - 2024";

describe('Mobile Simulate Integration Tests', () => {
  let agentBay: AgentBay;
  const apiKey = process.env.AGENTBAY_API_KEY;

  beforeAll(() => {
    if (!apiKey) {
      console.warn('Warning: AGENTBAY_API_KEY not set. Tests will be skipped.');
    }
  });

  beforeEach(() => {
    if (apiKey) {
      agentBay = new AgentBay({ apiKey });
    }
  });

  /**
   * Test mobile simulate feature by model_a prop file
   * and check product model is "SM-A505F" after session created
   */
  describe('Mobile Simulate for Model A', () => {
    test('should simulate Model A mobile device', async () => {
      if (!apiKey) {
        log('Skipping test: AGENTBAY_API_KEY not set');
        return;
      }

      log('Upload mobile dev info file for model A...');
      // Use the service instance from agentBay or create a new one if needed
      // Here we create a new one as per original test, but we could use agentBay.mobileSimulate
      const simulateService = new MobileSimulateService(agentBay);
      simulateService.setSimulateEnable(true);
      simulateService.setSimulateMode(MobileSimulateMode.PropertiesOnly);

      // Read mobile info file
      const mobileInfoPath = path.join(__dirname, '..', '..', '..', 'resource', 'mobile_info_model_a.json');
      const mobileInfoContent = fs.readFileSync(mobileInfoPath, 'utf8');

      // Upload mobile info
      const uploadResult = await simulateService.uploadMobileInfo(mobileInfoContent);
      
      expect(uploadResult.success).toBe(true);
      expect(uploadResult.mobileSimulateContextId).toBeDefined();
      
      const mobileSimContextID = uploadResult.mobileSimulateContextId!;
      log(`Mobile dev info uploaded successfully: ${mobileSimContextID}`);

      // Create session with mobile simulate
      const sessionResult = await agentBay.create({
        imageId: 'mobile_latest',
        extraConfigs: {
          mobile: {
            lockResolution: false,
            hideNavigationBar: false,
            simulateConfig: simulateService.getSimulateConfig()
          } as any
        }
      });
      
      // Wait, I need to add simulateConfig to MobileExtraConfig interface!
      
      expect(sessionResult.success).toBe(true);
      expect(sessionResult.session).toBeDefined();
      
      const session = sessionResult.session!;
      log(`Session created successfully: ${session.sessionId}`);

      try {
        // Wait for mobile simulate to complete
        await new Promise(resolve => setTimeout(resolve, 5000));

        // Get device model after mobile simulate
        log('Getting device model after mobile simulate for model A...');
        const cmdResult = await (session as any).command.executeCommand('getprop ro.product.model');
        
        expect(cmdResult).toBeDefined();
        expect(cmdResult.success).toBe(true);
        
        const modelAProductModel = cmdResult.output.trim();
        log(`Simulated model A mobile product model: ${modelAProductModel}`);
        
        expect(modelAProductModel).toBe(MOBILE_INFO_MODEL_A);
      } finally {
        // Cleanup
        log('Deleting session...');
        const deleteResult = await session.delete();
        expect(deleteResult.success).toBe(true);
        log(`Session deleted successfully (RequestID: ${deleteResult.requestId})`);
      }
    }, 60000); // 60 second timeout
  });

  /**
   * Test mobile simulate feature by model_b prop file
   * and check product model is "moto g stylus 5G - 2024" after session created
   */
  describe('Mobile Simulate for Model B', () => {
    test('should simulate Model B mobile device', async () => {
      if (!apiKey) {
        log('Skipping test: AGENTBAY_API_KEY not set');
        return;
      }

      log('Upload mobile dev info file for model B...');

      const simulateService = new MobileSimulateService(agentBay);
      simulateService.setSimulateEnable(true);
      simulateService.setSimulateMode(MobileSimulateMode.PropertiesOnly);
      // Read mobile info file
      const mobileInfoPath = path.join(__dirname, '..', '..', '..', 'resource', 'mobile_info_model_b.json');
      const mobileInfoContent = fs.readFileSync(mobileInfoPath, 'utf8');

      // Upload mobile info
      const uploadResult = await simulateService.uploadMobileInfo(mobileInfoContent);
      
      expect(uploadResult.success).toBe(true);
      expect(uploadResult.mobileSimulateContextId).toBeDefined();
      
      const mobileSimContextID = uploadResult.mobileSimulateContextId!;
      log(`Mobile dev info uploaded successfully: ${mobileSimContextID}`);

      // Create session with mobile simulate
      const sessionResult = await agentBay.create({
        imageId: 'mobile_latest',
        extraConfigs: {
          mobile: {
            lockResolution: false,
            hideNavigationBar: false,
            simulateConfig: simulateService.getSimulateConfig()
          } as any
        }
      });

      expect(sessionResult.success).toBe(true);
      expect(sessionResult.session).toBeDefined();
      
      const session = sessionResult.session!;
      log(`Session created successfully: ${session.sessionId}`);

      try {
        // Wait for mobile simulate to complete
        await new Promise(resolve => setTimeout(resolve, 5000));

        // Get device model after mobile simulate
        log('Getting device model after mobile simulate for model B...');
        const cmdResult = await (session as any).command.executeCommand('getprop ro.product.model');
        
        expect(cmdResult).toBeDefined();
        expect(cmdResult.success).toBe(true);
        
        const modelBProductModel = cmdResult.output.trim();
        log(`Simulated model B mobile product model: ${modelBProductModel}`);
        
        expect(modelBProductModel).toBe(MOBILE_INFO_MODEL_B);
      } finally {
        // Cleanup
        log('Deleting session...');
        const deleteResult = await session.delete();
        expect(deleteResult.success).toBe(true);
        log(`Session deleted successfully (RequestID: ${deleteResult.requestId})`);
      }
    }, 60000); // 60 second timeout
  });

  /**
   * Test mobile simulate persistence feature
   * by using an existing mobile simulate context id, and check product model is
   * "SM-A505F" after session created
   */
  describe('Mobile Simulate Persistence', () => {
    test('should use persistent mobile simulate context', async () => {
      if (!apiKey) {
        log('Skipping test: AGENTBAY_API_KEY not set');
        return;
      }
      // For Session 1
      log('Upload mobile dev info file for model A...');
      // Use the service instance from agentBay or create a new one if needed
      // Here we create a new one as per original test, but we could use agentBay.mobileSimulate
      const simulateService = new MobileSimulateService(agentBay);
      simulateService.setSimulateEnable(true);
      simulateService.setSimulateMode(MobileSimulateMode.PropertiesOnly);

      // Read mobile info file
      const mobileInfoPath = path.join(__dirname, '..', '..', '..', 'resource', 'mobile_info_model_a.json');
      const mobileInfoContent = fs.readFileSync(mobileInfoPath, 'utf8');

      // Upload mobile info
      const uploadResult = await simulateService.uploadMobileInfo(mobileInfoContent);
      
      expect(uploadResult.success).toBe(true);
      expect(uploadResult.mobileSimulateContextId).toBeDefined();
      
      const mobileSimContextID = uploadResult.mobileSimulateContextId!;
      log(`Mobile dev info uploaded successfully: ${mobileSimContextID}`);

      // Create session with mobile simulate
      const sessionResult = await agentBay.create({
        imageId: 'mobile_latest',
        extraConfigs: {
          mobile: {
            lockResolution: false,
            hideNavigationBar: false,
            simulateConfig: simulateService.getSimulateConfig()
          } as any
        }
      });
      
      // Wait, I need to add simulateConfig to MobileExtraConfig interface!
      
      expect(sessionResult.success).toBe(true);
      expect(sessionResult.session).toBeDefined();
      
      const session = sessionResult.session!;
      log(`Session 1 created successfully: ${session.sessionId}`);

      try {
        // Wait for mobile simulate to complete
        await new Promise(resolve => setTimeout(resolve, 5000));

        // Get device model after mobile simulate
        log('Getting device model after mobile simulate for model A...');
        const cmdResult = await (session as any).command.executeCommand('getprop ro.product.model');
        
        expect(cmdResult).toBeDefined();
        expect(cmdResult.success).toBe(true);
        
        const modelAProductModel = cmdResult.output.trim();
        log(`Simulated model A mobile product model: ${modelAProductModel}`);
        
        expect(modelAProductModel).toBe(MOBILE_INFO_MODEL_A);
      } finally {
        // Cleanup
        log('Deleting session 1...');
        const deleteResult = await session.delete();
        expect(deleteResult.success).toBe(true);
        log(`Session 1 deleted successfully (RequestID: ${deleteResult.requestId})`);
      }

      // For Session 2
      log(`Using a persistent mobile simulate context id: ${mobileSimContextID}`);
      const simulateService2 = new MobileSimulateService(agentBay);
      simulateService2.setSimulateEnable(true);
      simulateService2.setSimulateMode(MobileSimulateMode.PropertiesOnly);
      simulateService2.setSimulateContextId(mobileSimContextID);

      // Create session with persistent mobile simulate context
      const sessionResult2 = await agentBay.create({
        imageId: 'mobile_latest',
        extraConfigs: {
          mobile: {
            lockResolution: false,
            hideNavigationBar: false,
            simulateConfig: simulateService2.getSimulateConfig()
          } as any
        }
      });

      expect(sessionResult2.success).toBe(true);
      expect(sessionResult2.session).toBeDefined();
      
      const session2 = sessionResult2.session!;
      log(`Session 2 created successfully: ${session2.sessionId}`);

      try {
        // Wait for mobile simulate to complete
        await new Promise(resolve => setTimeout(resolve, 5000));

        // Get device model after mobile simulate
        log('Getting device model after mobile simulate with user context...');
        const cmdResult2 = await (session2 as any).command.executeCommand('getprop ro.product.model');
        
        expect(cmdResult2).toBeDefined();
        expect(cmdResult2.success).toBe(true);
        
        const productModel2 = cmdResult2.output.trim();
        log(`Persistence simulated mobile product model: ${productModel2}`);
        
        expect(productModel2).toBe(MOBILE_INFO_MODEL_A);
      } finally {
        // Cleanup
        log('Deleting session 2...');
        const deleteResult = await session2.delete();
        expect(deleteResult.success).toBe(true);
        log(`Session 2 deleted successfully (RequestID: ${deleteResult.requestId})`);
      }
    }, 60000); // 60 second timeout
  });
});

