module.exports = {
    preset: 'ts-jest',
    testEnvironment: 'node',
    testTimeout: 60000, // Set global timeout to 60 seconds for all tests
    moduleFileExtensions: ['ts', 'tsx', 'js', 'jsx', 'json'],
    transform: {
        '^.+\\.ts$': ['ts-jest', {
            tsconfig: 'tsconfig.json',
            diagnostics: {
                ignoreCodes: [151001]
            }
        }]
    },
    transformIgnorePatterns: [
        'node_modules/(?!(zod|zod-to-json-schema)/)' // Transform zod and zod-to-json-schema to handle ES modules
    ],
    testMatch: ['**/tests/**/*.test.ts', '**/tests/**/*.test.js'],
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
    // Add moduleNameMapper to handle Node.js built-in modules and ES modules
    moduleNameMapper: {
        '^node:(.*)$': '$1',
        // Map zod ES modules to CommonJS versions
        '^zod$': '<rootDir>/node_modules/zod/index.cjs',
        '^zod/v3$': '<rootDir>/node_modules/zod/v3/index.cjs',
        '^zod-to-json-schema$': '<rootDir>/node_modules/zod-to-json-schema/dist/cjs/index.js'
    },
    // Suppress console output during tests to avoid test noise
    // Set log level to only show critical errors
    setupFilesAfterEnv: ['<rootDir>/tests/setup.ts'],
    // globals configuration moved to transform options above
};
