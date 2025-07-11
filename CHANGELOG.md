# Changelog

All notable changes to the Wuying AgentBay SDK will be documented in this file.

## [0.3.0] - 2024-06-16

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

## [0.1.0] - 2024-05-15

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