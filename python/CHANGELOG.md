# Changelog

## [0.3.0] - 2024-06-16
### Added

- **Port Forwarding Interface**: Added support for port forwarding between local and remote environments
- **Enhanced Image ID Support**: Added support for specifying custom image IDs when creating sessions
- **CodeSpace SDK Integration**: Added compatibility with CodeSpace environments
- **FileSystem Enhancements**:
  - Added large file operations with automatic chunking
  - Improved file read/write performance
  - Added support for reading multiple files in a single operation
- **Mobile Tools API Support**: Added support for mobile-specific tool APIs
- **Process Management**: Added APIs for process management and monitoring
- **Window Task Management**: Added support for window task management
- **OSS Integration**: Added Object Storage Service (OSS) functionality for cloud storage operations
- **Command Execution Improvements**: Migrated to new MCP tool interface for command execution

### Changed

- Updated API client to support the latest AgentBay backend features
- Improved error handling and reporting across all SDK components
- Enhanced documentation with examples for new features

### Fixed

- Various bug fixes and performance improvements
- Type compatibility issues in filesystem operations
- Session management edge cases

## [0.1.0] - 2024-05-15

Initial public release of the Wuying AgentBay SDK with support for:

- Session management
- Basic file operations
- Command execution
- Application management
- Window operations
- Label management
- Context persistence
