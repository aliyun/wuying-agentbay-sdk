module.exports = {
  preset: 'ts-jest/presets/default-esm',
  extensionsToTreatAsEsm: ['.ts'],
    testEnvironment: 'node',
    testTimeout: 300000, // Set global timeout to 300 seconds for all tests
    moduleFileExtensions: ['ts', 'js', 'json'],
    globals: {
      'ts-jest': {
        useESM: true,
      },
    },
    transform: {
      '^.+\\.ts$': 'ts-jest'
    },
    transformIgnorePatterns: [
      'node_modules/(?!(chai)/)' // Exclude chai from transform ignore
    ],
    testMatch: ['**/tests/**/*.test.ts'],
    collectCoverageFrom: [
      'src/**/*.ts',
      '!src/**/*.d.ts',
      '!src/**/index.ts'
    ],
    coverageDirectory: 'coverage',
    coverageReporters: ['text', 'lcov', 'html'],
    testPathIgnorePatterns: [
      '/node_modules/',
      '/dist/'
    ],
    globals: {
      'ts-jest': {
        tsconfig: 'tsconfig.json'
      }
    }
  };
