/**
 * Test setup file to configure the test environment
 * This file is executed before running tests
 */

// Jest setup file to handle Playwright compatibility issues
// Mock Node.js built-in modules that cause issues with Jest
const mockNodeModules: Record<string, any> = {
  'node:events': require('events'),
  'node:fs': require('fs'),
  'node:path': require('path'),
  'node:util': require('util'),
  'node:stream': require('stream'),
  'node:crypto': require('crypto'),
  'node:os': require('os'),
  'node:url': require('url'),
  'node:buffer': require('buffer'),
  'node:process': require('process')
};

// Override require to handle node: protocol
const originalRequire = require;
(global as any).require = function(id: string) {
  if (id.startsWith('node:')) {
    const moduleName = id.replace('node:', '');
    if (mockNodeModules[id]) {
      return mockNodeModules[id];
    }
    return originalRequire(moduleName);
  }
  return originalRequire.apply(originalRequire, arguments as any);
};

// Set up global test environment
// Only suppress console methods if explicitly requested
if (process.env.SUPPRESS_TEST_LOGS === 'true') {
  global.console = {
    ...console,
    // Suppress Playwright warnings during tests
    warn: jest.fn(),
    error: jest.fn(),
    log: jest.fn(),
    info: jest.fn(),
    debug: jest.fn()
  };
}

// Mock Playwright if it's causing issues
jest.mock('playwright', () => ({
  chromium: {
    launch: jest.fn(),
    connect: jest.fn()
  },
  firefox: {
    launch: jest.fn(),
    connect: jest.fn()
  },
  webkit: {
    launch: jest.fn(),
    connect: jest.fn()
  }
}), { virtual: true });

// Increase timeout for async operations
jest.setTimeout(60000 * 3);

import { setupLogger } from '../src/utils/logger';

// Check if we should suppress logs (can be controlled via environment variable)
// Default to false for integration tests to see logs
// For unit tests, set SUPPRESS_TEST_LOGS=true to reduce noise
const suppressLogs = process.env.SUPPRESS_TEST_LOGS === 'true';

if (suppressLogs) {
  // Disable console logging during tests to avoid noise in test output
  // This prevents expected error messages from appearing as test failures in CI/CD
  setupLogger({
    enableConsole: false,
    level: 'ERROR' // Only log critical errors
  });
} else {
  // Enable console logging for integration tests when explicitly requested
  setupLogger({
    enableConsole: true,
    level: 'INFO' // Show INFO level and above
  });
}
