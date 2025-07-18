# Changelog

All notable changes to the Wuying AgentBay SDK will be documented in this file.

## [0.4.0] - 2025-07-18

### Added

- **Enhanced Configuration**: Support for setting SDK configuration via three methods (environment variables, config files, code parameters) in Python, Golang, and TypeScript.
- **API Response Improvements**: All API responses now include a `request_id` field for better traceability and debugging.
- **Session Label Pagination**: `listByLabels` now supports pagination parameters.
- **GetLink API**: Added support for specifying protocol type and port when retrieving links.
- **OSS Persistence**: Added support for persistent storage with OSS.
- **Ticket Parameter**: Some APIs now support a ticket parameter.
- **Context Sync & Management**: Introduced context manager and context sync APIs and implementations.
- **Automated Quality Scripts**: Added one-click quality check scripts (lint/format/security scan) and multi-language automated testing.
- **Comprehensive Unit & Integration Tests**: Significantly expanded and improved tests for TypeScript, Go, and Python SDKs.
- **Documentation Restructure**: API reference is now split by language, with many new tutorials and examples.
- **Type/Interface Enhancements**: Many new interfaces and type definitions for better IDE support across Golang, TypeScript, and Python.

### Changed

- **API Compatibility**: Standardized some API parameters and response formats.
- **Error Handling**: Improved error handling and logging across SDKs.
- **Default Timeout**: Default timeout changed to 60 seconds.
- **Documentation**: Major updates to README, Getting Started, API Reference, and Tutorials.
- **Code Structure**: Refactored directory structure; examples, tests, and scripts are now modularized.

### Fixed

- **Session Deletion/Management**: Fixed issues with session deletion and state management.
- **File System**: Fixed issues with large file chunking and read/write consistency.
- **Unit Tests**: Fixed compatibility and edge cases in multi-language unit tests.
- **CI/CD**: Fixed cross-platform line endings and environment variable loading issues.
- **API Responses**: Fixed incomplete response structures in some APIs.

## [0.3.0] - 2025-06-16

### Added

- **Session Labels**: Added support for organizing and filtering sessions with labels
  - Set and get session labels
  - List sessions by label filters
- **Code Execution**: Added support for running code in multiple languages (Python, JavaScript, etc.)
- **Window Management**: 
  - Added support for listing, activating, and manipulating windows
  - Window resizing, focusing, and positioning
  - Get window properties and child windows
- **OSS Integration**: Added Object Storage Service functionality
  - File upload/download to/from OSS buckets
  - Anonymous upload/download via URLs
  - OSS environment initialization
- **Context Management**: 
  - Create, list, and delete contexts
  - Bind sessions to contexts for persistence
  - Get context information
- **UI Enhancement**: 
  - Added support for screenshots
  - UI element detection and interaction
  - Mobile-specific operations (click, swipe, send keys)
- **Enhanced Image ID Support**: Added ability to specify custom image IDs when creating sessions
- **Application Management**: Added support for listing, launching, and stopping applications

### Changed

- Updated API client to support the latest AgentBay backend features
- Improved error handling and reporting across all SDK components
- Enhanced documentation with examples for new features
- Enhanced TypeScript type definitions for better IDE support
- Standardized response formats across all operations

### Fixed

- Various bug fixes and performance improvements
- Type compatibility issues in filesystem operations
- Session management edge cases
- Command execution timeouts
- File reading/writing inconsistencies

## [0.1.0] - 2025-05-15

### Added

- **Core SDK Implementation**: Initial implementation for Python, TypeScript, and Golang
- **Session Management**: 
  - Create, list, and delete sessions
  - Get session information
- **Command Execution**: 
  - Execute basic shell commands
- **Basic File Operations**: 
  - Read and write files
  - Create and delete directories
  - List directory contents
- **Authentication**: API key-based authentication
- **Configuration**: Environment-based configuration
- **Documentation**: Initial API reference and examples