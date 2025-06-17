module.exports = {
    preset: 'ts-jest',
    testEnvironment: 'node',
    moduleFileExtensions: ['ts', 'js', 'json'],
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
