# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Model Context Protocol (MCP) server test project that provides multiple specialized MCP services for different functionalities including file system operations, database access, template management, and knowledge base services.

## Development Setup

### Package Management
- Uses `uv` as the package manager
- Install `uv` on Windows: `powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"`
- Sync project: `uv sync`

### Python Version
- Requires Python >=3.13
- Configure in `.python-version` file

### Code Quality
- Uses `ruff` for linting and formatting
- Pre-commit hooks configured in `.pre-commit-config.yaml`
- Configuration in `.ruff.toml` with 120 character line length
- Run linting: `uv run ruff check`
- Run formatting: `uv run ruff format`

## Available MCP Servers

### 1. File System Server (`fs_mcp`)
- **Port**: 3001
- **Purpose**: File system operations (read, write, create, search, etc.)
- **Start**: `uv run fs_mcp`
- **Key Features**:
  - File read/write operations with encoding support
  - Directory listing and creation
  - File search with pattern matching
  - Media file support (images, audio) with base64 encoding
  - File editing with git-style diff output
  - ZIP compression functionality
  - Path validation and security restrictions

### 2. Element Plus Server (`element_plus_mcp`)
- **Port**: 3003
- **Purpose**: Element Plus component documentation and examples
- **Start**: `uv run element_plus_mcp`

### 3. MySQL Server (`mysql_mcp`)
- **Port**: 3004
- **Purpose**: MySQL database operations
- **Start**: `uv run mysql_mcp`
- **Configuration**: Requires environment variables (`MYSQL_HOST`, `MYSQL_USER`, `MYSQL_PASSWORD`, `MYSQL_DATABASE`)
- **Key Features**:
  - List tables with comments
  - Describe table structure
  - Execute SELECT queries
  - Template context preparation for code generation
  - Query result caching

### 4. Template Server (`template_mcp`)
- **Port**: 3005
- **Purpose**: Code template management and generation
- **Start**: `uv run template_mcp`
- **Key Features**:
  - Template categories (backend, frontend, database scripts)
  - Template content retrieval
  - Sample code examples
  - Support for Velocity templates
  - Cached template access

### 5. Knowledge Base Server (`knowledge_mcp`)
- **Purpose**: Knowledge base and documentation services

### 6. Demo Server (`demo_mcp`)
- **Purpose**: Demonstration and testing MCP functionality

### 7. Embedding Tools
- **Embed**: `uv run embed`
- **Test Search**: `uv run test_search`

## Architecture

### Common Components (`src/common/`)
- **mcp_cli.py**: CLI utilities for MCP servers with transport options and CORS support
- **cache.py**: Simple TTL-based caching implementation

### Server Architecture
Each MCP server follows a consistent pattern:
- Uses `FastMCP` from the MCP framework
- Supports multiple transport protocols (`stdio`, `streamable`, `sse`)
- Implements CORS middleware for web-based transports
- Uses `@with_mcp_options()` decorator for CLI arguments
- Implements proper error handling and logging

### Transport Support
All servers support three transport protocols:
1. **stdio**: Standard input/output (default)
2. **streamable**: HTTP streaming with CORS
3. **sse**: Server-Sent Events with CORS

## Configuration

### Environment Variables
- `MCP_ALLOWED_DIRECTORIES`: Semicolon-separated list of directories for file system access
- MySQL configuration: `MYSQL_HOST`, `MYSQL_PORT`, `MYSQL_USER`, `MYSQL_PASSWORD`, `MYSQL_DATABASE`

### .env Support
- Servers load configuration from `.env` file in project root
- Use `.env.example` as template

## Usage in Clients

### Trae Configuration Example

**streamable-http protocol**:
```json
{
  "mcpServers": {
    "ServerName": {
      "url": "http://localhost:3001/mcp",
      "headers": {
        "X-API-KEY": "application/json"
      }
    }
  }
}
```

**stdio protocol**:
```json
{
  "mcpServers": {
    "FileSystem": {
      "command": "uv",
      "args": [
        "--directory",
        "E:/GitHub/All_in_Ai/test_mcp_server",
        "run",
        "fs_mcp"
      ],
      "env": {
        "MCP_ALLOWED_DIRECTORIES": "D:\\dev;E:\\app;"
      }
    }
  }
}
```

## Debugging

Use MCP Inspector for debugging:
```bash
npx @modelcontextprotocol/inspector uv --directory E:/GitHub/All_in_Ai/test_mcp_server run fs_mcp
```

## Key Development Patterns

### Error Handling
- Consistent error response format across all tools
- Detailed logging with structured information
- Graceful handling of missing files and permissions

### Caching Strategy
- Simple TTL-based cache for frequently accessed data
- Used in template and MySQL servers for performance
- Cache key generation includes database/table names for uniqueness

### Security
- Path validation for file system operations
- Directory access restrictions
- SQL injection protection (only SELECT queries allowed)
- Environment-based configuration for sensitive data

### Cross-Platform Support
- Windows-specific stdout handling for stdio transport
- Path normalization for different operating systems
- Proper handling of file permissions and symlinks