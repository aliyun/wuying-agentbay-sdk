# Changelog

All notable changes to the Wuying AgentBay SDK will be documented in this file.

## [0.7.0] - 2025-09-02

### Added

- **AI Browser Extension**: New browser extension capabilities for enhanced automation
  - **Python Extension Support**: Added `extention.py` module for browser extension functionality
  - **TypeScript Extension Support**: Complete extension API implementation with examples
  - **Extension Integration**: Seamless integration with browser automation workflows
  - **Extension Testing**: Comprehensive test coverage for extension functionality
- **Enhanced File System API**: Major improvements to file operations across all SDKs
  - **Streamlined API**: Updated method signatures for better consistency
  - **Session Integration**: Better integration with session management for file operations
  - **Comprehensive Testing**: Expanded test coverage with integration and unit tests
- **Documentation & Guides**: Comprehensive documentation improvements
  - **Large File Handling Guide**: Detailed guide for handling large files efficiently
  - **File Operations Guide**: Updated comprehensive guide with session usage examples
  - **API Documentation**: Complete API reference updates across all SDKs
  - **Usage Examples**: Updated examples and documentation for better developer experience

### Changed

- **File System API**: Breaking changes to improve consistency and usability
  - **Method Naming**: Standardized method names across Python, TypeScript, and Golang SDKs
  - **Return Types**: Enhanced return types for better type safety and error handling
  - **Session Context**: Improved integration with session management for file operations
- **Documentation Structure**: Major documentation reorganization
  - **API Reference**: Updated API documentation to match actual implementation
  - **Command API**: Updated method names and return value references across all documentation
  - **Context Manager**: Enhanced documentation with detailed return object information

### Fixed

- **Browser Automation**: Resolved browser-related issues
  - **Page Variables**: Fixed support for variables in page_use_act functionality
- **Python Package**: Resolved Python-specific issues
  - **Module Imports**: Added missing `__init__.py` in agentbay models directory
  - **API Examples**: Fixed incorrect API usage examples in Python README
- **Test Infrastructure**: Improved test reliability and organization
  - **Test Organization**: Moved test files to appropriate integration directories
  - **Deprecated Tests**: Removed outdated integration tests
  - **Test Coverage**: Enhanced test coverage for new features

### Documentation

- **Comprehensive Updates**: Major documentation improvements across all areas
  - **Getting Started**: Updated quickstart documentation and first session guides
  - **API Reference**: Complete API documentation updates for all modules
  - **Examples**: Updated SDK usage examples and documentation
  - **Guides**: New and updated guides for file operations and large file handling

## [0.6.0] - 2025-08-23

### Added

- **Browser Proxy Support**: New proxy configuration for browser automation across Python and TypeScript
  - **BrowserProxy Class**: Support for custom and wuying proxy types
    - Custom proxy with server, username, password configuration
    - Wuying proxy with "restricted" and "polling" strategies
    - Configurable pool size for polling strategy
  - **Proxy Integration**: Seamless integration with browser initialization
    - Automatic proxy configuration during browser setup
    - Support for both authenticated and anonymous proxy connections
- **Browser Stealth Mode & Fingerprinting**: Enhanced browser automation capabilities
  - **Stealth Mode**: Browser stealth mode support to avoid detection
  - **Browser Fingerprinting**: Configurable browser fingerprint options
    - Custom user agent, viewport, timezone, and locale settings
    - Enhanced privacy and anti-detection capabilities
- **Context File Management APIs**: Complete file operations within contexts across all SDKs
  - **File URL Operations**: Presigned URL support for secure file access
    - `get_file_download_url()` / `GetFileDownloadUrl()` for secure file downloads
    - `get_file_upload_url()` / `GetFileUploadUrl()` for secure file uploads
  - **File Management**: Full CRUD operations for context files
    - `list_files()` / `ListFiles()` with pagination support for context file listing
    - `delete_file()` / `DeleteFile()` for context file deletion
    - Enhanced error handling and response parsing for all file operations
- **Session Management Enhancements**: Improved session creation and management
  - **MCP Policy Support**: Optional `mcp_policy_id` parameter in session creation
  - **Session List Response Models**: Enhanced session listing with proper response models
- **Browser Agent Improvements**: Enhanced AI-powered browser interactions
  - **Direct ObserveResult Support**: PageUse act API can now accept ObserveResult directly
  - **TypeScript Browser Agent**: Merged browser agent functionality to TypeScript SDK
  - **Enhanced Parameter Handling**: Improved parameter type conversion and validation
- **Development & Testing Infrastructure**: Enhanced development experience
  - **Pre-commit Hooks**: Added secret detection in pre-commit hooks
  - **Local Benchmark Testing**: Added local benchmark test support for PageUseAgent API
  - **Page Task Framework**: Initial version of page task framework
  - **Auto Publishing**: Enhanced CI/CD with auto publishing workflows

### Changed

- **Browser Configuration**: Enhanced browser setup with advanced options
  - **Breaking Change**: `BrowserOption` now supports proxy, stealth mode, and fingerprinting
  - Automatic proxy validation and configuration during browser initialization
  - Better error handling for proxy connection and stealth mode issues
- **Browser Agent API**: Improved browser automation interface
  - Enhanced parameter naming and validation in ExtractOptions, ObserveOptions, and ActOptions
  - Better timeout handling with default MCP tool call timeout for PageUseAgent
  - Improved error handling and response parsing
- **Context API Enhancement**: Improved context service implementation
  - Enhanced error handling and response parsing across all context operations
  - Better pagination support with `ContextListParams` for large context lists
  - Improved integration with session creation and context synchronization
- **Documentation & Examples**: Updated documentation and examples
  - Updated Python examples with session params
  - Aligned TypeScript examples with latest API changes
  - Updated README and examples documentation

### Fixed

- **Browser VPC Environment**: Resolved VPC-specific browser issues
  - Fixed browser endpoint URL population for VPC environment
  - Better CDP endpoint management for VPC and non-VPC sessions
- **Browser Agent API**: Enhanced browser automation reliability
  - Fixed parameter type conversion in observation API
  - Fixed bad naming in browser agent methods and options
  - Improved error handling for browser agent operations
- **PageUseAgent Integration**: Resolved PageUseAgent API issues
  - Fixed run_sudoku functionality
  - Aligned examples with latest PageUseAgent API revision
  - Fixed benchmark test integration with PageAgent
- **Context File Operations**: Enhanced context file management reliability
  - Fixed presigned URL generation and expiration handling
  - Improved file listing pagination and response parsing
  - Better error handling for file upload/download operations
- **Cross-Platform Compatibility**: Improved SDK consistency
  - Standardized method signatures across Python, TypeScript, and Golang
  - Fixed async/await patterns in TypeScript and Python implementations
  - Better error handling and response structure consistency

## [0.5.0] - 2025-08-06

### Added

- **Browser Automation & AI Browser**: Comprehensive browser automation capabilities with AI-powered interactions
  - AIBrowser interface with Playwright integration
  - Browser Context for persistent data across sessions (cookies, local storage, session storage)
  - Browser Agent with natural language operations (Act, Observe, Extract)
  - Support for complex web automation tasks through Agent module integration
- **VPC Session Support**: Enhanced security and networking capabilities
  - VPC-based session creation with `is_vpc` parameter
  - Specialized system tools (get_resource, system_screenshot, release_resource)
  - Browser tools availability in VPC sessions (cdp, pageuse-mcp-server, playwright)
  - Network isolation for sensitive operations
- **Agent Module**: AI-powered task execution framework
  - Natural language task execution with `ExecuteTask()` method
  - Task status monitoring and management
  - Task termination capabilities
  - Integration with browser automation for complex web operations
- **Unified MCP Tool Interface**: Standardized tool calling mechanism across all modules
  - `CallMcpTool()` method for unified tool invocation
  - Support for both VPC and non-VPC tool calling patterns
  - Automatic server discovery for tools
  - Enhanced error handling and debugging capabilities
- **Comprehensive Interface Architecture**: Complete interface definitions for better modularity
  - FileSystemInterface, SessionInterface, WindowInterface, ApplicationInterface
  - CommandInterface, CodeInterface, UIInterface, OSSInterface
  - AgentBayInterface for main client operations
  - Mock generation support for all interfaces
- **Enhanced Context Management**: Improved context synchronization and pagination
  - Context list pagination with `ListContexts` API
  - Enhanced context binding and persistence
  - Better error handling for context operations
- **Quality Assurance Infrastructure**: Automated quality check scripts for all languages
  - One-click quality check scripts (`quality-check.sh`) for Python, TypeScript, and Golang
  - Comprehensive linting, formatting, and security scanning
  - Automated unit and integration testing
  - CI/CD integration support
- **Documentation & Examples**: Comprehensive documentation and example improvements
  - Agent module documentation and examples for all languages
  - VPC session tutorials and API reference
  - Browser automation architecture documentation
  - AI-powered web interactions tutorial
  - Updated API reference with new modules and interfaces

### Changed

- **Architecture Refactoring**: Major structural improvements for better maintainability
  - Interfaces-first design with dependency injection
  - Removal of circular dependencies between modules
  - Unified MCP tool calling across all components
- **Session Management**: Enhanced session capabilities and VPC support
  - VPC session detection and handling
  - Network interface IP and HTTP port management for VPC sessions
  - Improved session lifecycle management
- **Error Handling**: Improved error handling and logging across all SDKs
  - Better error messages for VPC configuration issues
  - Enhanced debugging information with request IDs
  - Sanitized error reporting for security
- **Testing Infrastructure**: Significantly expanded test coverage
  - Comprehensive unit tests for all modules
  - Integration tests for VPC sessions and browser automation
  - API-level comprehensive testing for command and filesystem operations
- **Module Separation**: Code execution moved from Command to dedicated Code module
  - `RunCode` method moved from Command module to Code module
  - Clear separation of concerns between shell commands and code execution
  - Improved API consistency across all language implementations

### Fixed

- **VPC Session Compatibility**: Fixed issues with VPC-based tool calling
  - Proper HTTP endpoint construction for VPC sessions
  - Network configuration validation
  - Server discovery for VPC environments
- **Browser Context Persistence**: Fixed browser data persistence across sessions
  - Cookie synchronization improvements
  - Context cleanup on session termination
  - Resource management for browser instances
- **Interface Consistency**: Fixed inconsistencies across language implementations
  - Standardized method signatures across Python, TypeScript, and Golang
  - Consistent error handling patterns
  - Unified response structures

### Security

- **Enhanced Security Scanning**: Improved security measures across all SDKs
  - Dependency vulnerability scanning with pip-audit, npm audit, and govulncheck
  - Code security analysis with bandit, snyk, and gosec
  - Secure credential handling for VPC sessions
- **Network Isolation**: VPC sessions provide enhanced security through network isolation
  - Private network environments for sensitive operations
  - Controlled access policies
  - Secure resource access patterns

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