# Common Features Examples

This directory contains examples demonstrating features available across all AgentBay environment types (browser, computer, mobile, and codespace).

## Directory Structure

```
common-features/
├── basics/          # Fundamental features for all users
└── advanced/        # Advanced features and integrations
```

## Basics

Essential features that every AgentBay user should know:

### [session_creation](basics/session_creation/)
Session lifecycle management examples:
- Creating sessions with default parameters
- Session creation with labels
- Session creation with context synchronization
- Browser context for cookie persistence
- Mobile configuration with app management

### [file_system](basics/file_system/)
File operations in cloud environments:
- Reading and writing files
- Directory operations
- File information retrieval
- File editing and moving
- File searching
- Large file operations with chunking
- Practical filesystem use cases:
  - **file_transfer_example.py**: File transfer between local and cloud
  - **watch_directory_example.py**: Directory monitoring and change detection

### [context_management](basics/context_management/)
Context creation and management:
- Creating and managing contexts
- Data storage and retrieval
- Cross-session data sharing

### [data_persistence](basics/data_persistence/)
Data persistence across sessions:
- Storing data across sessions
- Data retrieval patterns
- Context synchronization demonstration
- Recycle policy configuration

### [label_management](basics/label_management/)
Session organization with labels:
- Adding labels to sessions
- Filtering and searching sessions
- Label-based session management

### [list_sessions](basics/list_sessions/)
Session listing and filtering:
- Listing all sessions
- Filtering by labels
- Session status monitoring

### [get](basics/get/)
Session retrieval:
- Getting session by ID
- Session information retrieval

## Advanced

Advanced features for power users and integrations:

### [agent_module](advanced/agent_module/)
AI-powered automation:
- Using Agent for task execution
- Natural language task descriptions
- Intelligent automation workflows

### [oss_management](advanced/oss_management/)
Object Storage Service integration:
- OSS environment initialization
- File upload to OSS
- File download from OSS
- Anonymous upload/download

### [vpc_session](advanced/vpc_session/)
Secure isolated network environments:
- Creating VPC sessions
- VPC network configuration
- Secure session management

### [screenshot_download](advanced/screenshot_download/)
Screenshot capture and download:
- Taking screenshots
- Downloading screenshots locally
- Image format handling

## Prerequisites

- Python 3.8 or later
- AgentBay SDK installed: `pip install wuying-agentbay-sdk`
- Valid `AGENTBAY_API_KEY` environment variable

## Quick Start

```bash
# Set your API key
export AGENTBAY_API_KEY=your_api_key_here

# Run any example
cd basics/session_creation
python main.py

cd ../file_system
python main.py
```

## Usage

Each subdirectory contains specific examples with detailed documentation. Check the individual README files and Python scripts for complete usage examples.

## Best Practices

1. **Always Clean Up**: Delete sessions when done to free resources
2. **Error Handling**: Check `result.success` before using data
3. **Use Labels**: Organize sessions with meaningful labels
4. **Context Sync**: Use context synchronization for data persistence
5. **Resource Limits**: Be aware of concurrent session limits

## Related Documentation

- [Session Management Guide](../../../../../docs/guides/common-features/basics/session-management.md)
- [File Operations Guide](../../../../../docs/guides/common-features/basics/file-operations.md)
- [Data Persistence Guide](../../../../../docs/guides/common-features/basics/data-persistence.md)
- [Agent Modules Guide](../../../../../docs/guides/common-features/advanced/agent-modules.md)

## Troubleshooting

### Resource Creation Delay

If you see "The system is creating resources" message:
- Wait 90 seconds and retry
- This is normal for resource initialization
- Consider using session pooling for production

### API Key Issues

Ensure your API key is properly set:
```bash
export AGENTBAY_API_KEY=your_api_key_here
# Verify
echo $AGENTBAY_API_KEY
```

### Context Synchronization Timeout

For large contexts:
- Increase timeout settings
- Use selective synchronization
- Consider splitting into smaller contexts

