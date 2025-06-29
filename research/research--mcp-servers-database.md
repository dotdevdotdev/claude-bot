# MCP Servers Reference Database

A comprehensive collection of MCP server configurations, conversion examples, and setup patterns for Claude Code CLI.

## Table of Contents
1. [Command Syntax Patterns](#command-syntax-patterns)
2. [Conversion Examples](#conversion-examples)
3. [Task Management Servers](#task-management-servers)
4. [Platform Integration Servers](#platform-integration-servers)
5. [Development Tools](#development-tools)
6. [Configuration Examples](#configuration-examples)
7. [Troubleshooting](#troubleshooting)

---

## Command Syntax Patterns

### Basic Structure
```bash
claude mcp add <name> <command> [claude-flags] -- [command-args]
```

### Available Claude Flags
- `-s, --scope <scope>`: Configuration scope (local, user, or project) - default: "local"
- `-t, --transport <transport>`: Transport type (stdio, sse, http) - default: "stdio"
- `-e, --env <env...>`: Set environment variables (e.g. -e KEY=value)
- `-H, --header <header...>`: Set HTTP headers for SSE and HTTP transports

### Scope Usage
- `-s local`: Available only in current directory (default)
- `-s user`: Available globally for the user account
- `-s project`: Available only in current project

### Common Command Patterns

#### NPX Commands
```bash
# Basic NPX package
claude mcp add server-name npx -s user -- -y package-name

# NPX with environment variables
claude mcp add server-name npx -s user -e API_KEY=value -- -y package-name

# NPX with package flag and arguments
claude mcp add server-name npx -s user -- -y --package=package-name command-name
```

#### UV/Python Commands
```bash
# UV with directory
claude mcp add server-name uv -s user -- --directory /path/to/project run command

# UV with multiple arguments
claude mcp add server-name uv -s user -- --directory /path run script --args
```

#### Docker Commands
```bash
# Docker with environment variables
claude mcp add server-name docker -s user -e API_KEY=value -- run -i --rm image-name

# Docker with multiple env vars
claude mcp add server-name docker -s user \
  -e API_KEY=value \
  -e OTHER_KEY=value \
  -- run -i --rm image-name
```

#### Node Commands
```bash
# Direct node script
claude mcp add server-name node -s user -- /path/to/script.js

# Node with arguments
claude mcp add server-name node -s user -- /path/to/script.js --arg value
```

---

## Conversion Examples

### From JSON Configuration

#### Taskmaster AI (Full Configuration)
**Original JSON:**
```json
{
  "mcpServers": {
    "taskmaster-ai": {
      "command": "npx",
      "args": ["-y", "--package=task-master-ai", "task-master-ai"],
      "env": {
        "ANTHROPIC_API_KEY": "YOUR_ANTHROPIC_API_KEY_HERE",
        "PERPLEXITY_API_KEY": "YOUR_PERPLEXITY_API_KEY_HERE",
        "OPENAI_API_KEY": "YOUR_OPENAI_KEY_HERE",
        "GOOGLE_API_KEY": "YOUR_GOOGLE_KEY_HERE",
        "MISTRAL_API_KEY": "YOUR_MISTRAL_KEY_HERE",
        "OPENROUTER_API_KEY": "YOUR_OPENROUTER_KEY_HERE",
        "XAI_API_KEY": "YOUR_XAI_KEY_HERE",
        "AZURE_OPENAI_API_KEY": "YOUR_AZURE_KEY_HERE",
        "OLLAMA_API_KEY": "YOUR_OLLAMA_API_KEY_HERE"
      }
    }
  }
}
```

**Converted Commands:**

Full version:
```bash
claude mcp add taskmaster-ai npx -s user \
  -e ANTHROPIC_API_KEY="YOUR_ANTHROPIC_API_KEY_HERE" \
  -e PERPLEXITY_API_KEY="YOUR_PERPLEXITY_API_KEY_HERE" \
  -e OPENAI_API_KEY="YOUR_OPENAI_KEY_HERE" \
  -e GOOGLE_API_KEY="YOUR_GOOGLE_KEY_HERE" \
  -e MISTRAL_API_KEY="YOUR_MISTRAL_KEY_HERE" \
  -e OPENROUTER_API_KEY="YOUR_OPENROUTER_KEY_HERE" \
  -e XAI_API_KEY="YOUR_XAI_KEY_HERE" \
  -e AZURE_OPENAI_API_KEY="YOUR_AZURE_KEY_HERE" \
  -e OLLAMA_API_KEY="YOUR_OLLAMA_API_KEY_HERE" \
  -- -y --package=task-master-ai task-master-ai
```

Minimal version (Anthropic only):
```bash
claude mcp add taskmaster-ai npx -s user \
  -e ANTHROPIC_API_KEY="YOUR_ANTHROPIC_API_KEY_HERE" \
  -- -y --package=task-master-ai task-master-ai
```

No API keys (for Claude Code):
```bash
claude mcp add taskmaster-ai npx -s user -- -y --package=task-master-ai task-master-ai
```

#### Pandoc Server
**Original JSON:**
```json
{
  "command": "uv",
  "args": [
    "--directory",
    "/Users/vivekvells/Desktop/code/ai/mcp-pandoc",
    "run",
    "mcp-pandoc"
  ],
  "env": {
    "HOME": "/home/dotdev",
    "LOGNAME": "dotdev",
    "PATH": "/home/dotdev/.npm/_npx/5a9d879542beca3a/node_modules/.bin:...",
    "SHELL": "/bin/bash",
    "TERM": "xterm-256color",
    "USER": "dotdev"
  }
}
```

**Converted Command:**
```bash
claude mcp add mcp-pandoc uv -s user -- --directory /Users/vivekvells/Desktop/code/ai/mcp-pandoc run mcp-pandoc
```

#### Meta Prompt Server
**Original JSON:**
```json
{
  "command": "uv",
  "args": [
    "--directory",
    "path/to/your/meta-prompt-mcp",
    "run",
    "mcp-meta-prompt"
  ]
}
```

**Converted Command:**
```bash
claude mcp add meta-prompting uv -s user -- --directory /path/to/your/meta-prompt-mcp run mcp-meta-prompt
```

---

## Task Management Servers

### Comprehensive Local Solutions

#### MCP Task Manager Server
**Description:** SQLite-powered task management with project organization and dependency tracking.

**Installation:**
```bash
claude mcp add task-manager npx -s user -- -y mcp-task-manager-server
```

**Features:**
- Project organization with hierarchical tasks
- Dependency tracking and resolution
- Priority management (high/medium/low)
- Status progression (todo/in-progress/review/done)
- Automatic next-task identification
- JSON import/export
- Persistent SQLite storage

**Usage:**
- Create projects and organize tasks
- Set dependencies between tasks
- Track progress through multiple stages
- Export/import project data

#### ATLAS MCP Server
**Description:** Neo4j-powered task management with graph-based relationships.

**Installation:**
```bash
claude mcp add atlas npx -s user -- -y atlas-mcp-server
```

**Features:**
- Graph database for complex relationships
- Three-tier architecture (Projects → Tasks → Knowledge)
- Cross-entity fuzzy search
- Deep research capabilities
- Web UI for visualization
- Complex dependency modeling

**Requirements:**
- Neo4j database instance
- More complex setup but powerful relationships

#### Shrimp Task Manager
**Description:** AI-driven task management with chain-of-thought reasoning.

**Installation:**
```bash
claude mcp add shrimp npx -s user -- -y @smithery/cli install @cjo4m06/mcp-shrimp-task-manager --client claude
```

**Features:**
- Chain-of-thought task analysis
- Automatic task decomposition
- Long-term memory with backup
- English and Chinese interfaces
- Task complexity analysis
- Iterative refinement

### Workflow-Oriented Solutions

#### TaskQueue MCP
**Description:** Approval-based workflow management.

**Installation:**
```bash
claude mcp add taskqueue npx -s user -- -y taskqueue-mcp
```

**Features:**
- User approval workflows
- Multi-step planning with checkpoints
- State management for complex workflows
- Human oversight in automation

#### TaskFlow MCP
**Description:** Visual task management with approval stages.

**Installation:**
```bash
claude mcp add taskflow npx -s user -- -y taskflow-mcp
```

**Features:**
- Visual progress tracking
- Dependency management
- Multi-format export (Markdown, JSON, HTML)
- Stage-based approvals

---

## Platform Integration Servers

### Todoist Integration

#### Primary Todoist Server
**Installation:**
```bash
claude mcp add todoist npx -s user -e TODOIST_API_TOKEN="YOUR_TOKEN_HERE" -- -y @abhiz123/todoist-mcp-server
```

**Features:**
- Full REST API implementation
- Natural language task creation
- Project and section management
- Priority and due date handling
- Comments and labels
- Bulk operations

**Setup:**
- Get API token from Todoist Settings → Integrations
- Supports Todoist's filter syntax

### Linear Integration

#### Official Linear Server
**Installation:**
```bash
claude mcp add linear-remote remote -s user -t sse -- https://mcp.linear.app/sse
```

**Features:**
- Official hosted server
- OAuth authentication
- No API key management
- Full issue lifecycle

#### Community Linear Server
**Installation:**
```bash
claude mcp add linear npx -s user -e LINEAR_API_KEY="YOUR_KEY_HERE" -- -y @tacticlaunch/mcp-linear
```

**Features:**
- GraphQL integration
- Parent-child relationships
- Cross-project dependencies
- Team management

### Atlassian Ecosystem

#### Official Atlassian Server
**Installation:**
```bash
claude mcp add atlassian remote -s user -t http -- https://api.atlassian.com/mcp/
```

**Features:**
- Enterprise-grade security
- OAuth authentication
- Jira and Confluence integration
- Permission respect

#### Community Atlassian Server
**Installation:**
```bash
claude mcp add atlassian-community npx -s user \
  -e JIRA_HOST="your-domain.atlassian.net" \
  -e JIRA_EMAIL="your-email@domain.com" \
  -e JIRA_API_TOKEN="YOUR_TOKEN" \
  -- -y @sooperset/mcp-atlassian
```

**Features:**
- Cloud and Server support
- JQL queries
- Issue tracking
- Project management

### Other Platform Integrations

#### Notion
**Installation:**
```bash
claude mcp add notion npx -s user -e NOTION_API_KEY="YOUR_KEY_HERE" -- -y @makenotion/notion-mcp-server
```

#### Asana
**Installation:**
```bash
claude mcp add asana npx -s user -e ASANA_ACCESS_TOKEN="YOUR_TOKEN_HERE" -- -y @roychri/asana-mcp-server
```

#### Trello
**Installation:**
```bash
claude mcp add trello npx -s user \
  -e TRELLO_API_KEY="YOUR_KEY" \
  -e TRELLO_TOKEN="YOUR_TOKEN" \
  -- -y @delorenj/mcp-server-trello
```

#### ClickUp
**Installation:**
```bash
claude mcp add clickup npx -s user -e CLICKUP_API_TOKEN="YOUR_TOKEN_HERE" -- -y @taazkareem/clickup-mcp-server
```

#### Microsoft To Do
**Installation:**
```bash
claude mcp add microsoft-todo npx -s user \
  -e MICROSOFT_CLIENT_ID="YOUR_CLIENT_ID" \
  -e MICROSOFT_CLIENT_SECRET="YOUR_SECRET" \
  -- -y @jhirono/microsoft-todo-mcp-server
```

---

## Development Tools

### Task Master AI (Development Focus)
**Installation:**
```bash
claude mcp add taskmaster-ai npx -s user -- -y --package=task-master-ai task-master-ai
```

**Features:**
- PRD parsing into actionable tasks
- Development workflow optimization
- Complexity estimation
- File template generation
- Context-aware next steps

**Configuration for Claude Code:**
After installation, configure models:
```
Change the main model to claude-code/sonnet
```

**Usage Pattern:**
1. Initialize: "Initialize taskmaster-ai in my project"
2. Create PRD at `.taskmaster/docs/prd.txt`
3. Parse: "Can you parse my PRD?"
4. Work: "What's the next task I should work on?"

### Meta Prompt Server
**Installation:**
```bash
claude mcp add meta-prompt uv -s user -- --directory /path/to/meta-prompt-mcp-server run mcp-meta-prompt
```

**Features:**
- Prompt template management
- Meta-prompting capabilities
- Template versioning

---

## Configuration Examples

### Claude Desktop Config to MCP Commands

#### From claude_desktop_config.json
```json
{
  "mcpServers": {
    "server-name": {
      "command": "npx",
      "args": ["-y", "package-name"],
      "env": {
        "API_KEY": "value"
      }
    }
  }
}
```

#### To Claude Code Command
```bash
claude mcp add server-name npx -s user -e API_KEY=value -- -y package-name
```

### VS Code Configuration
```json
{
  "servers": {
    "server-name": {
      "command": "npx",
      "args": ["-y", "package-name"],
      "env": {
        "API_KEY": "value"
      },
      "type": "stdio"
    }
  }
}
```

### Docker-based Servers
```bash
# GitHub MCP Server
claude mcp add github docker -s user \
  -e GITHUB_PERSONAL_ACCESS_TOKEN="YOUR_TOKEN" \
  -- run -i --rm ghcr.io/github/github-mcp-server
```

### Remote Servers
```bash
# Linear Remote
claude mcp add linear-remote remote -s user -t sse -- https://mcp.linear.app/sse

# GitHub Remote
claude mcp add github-remote remote -s user -t http \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -- https://api.githubcopilot.com/mcp/
```

---

## Troubleshooting

### Common Issues and Solutions

#### Timeout Errors
**Problem:** `Connection to MCP server timed out after 30000ms`

**Solutions:**
1. Install package globally first:
   ```bash
   npm install -g package-name
   claude mcp add server-name package-name -s user
   ```

2. Remove `--package=` flag if causing issues:
   ```bash
   claude mcp add server-name npx -s user -- -y package-name
   ```

3. Test manually first:
   ```bash
   npx -y package-name
   ```

#### Environment Variables
**Problem:** API keys not working

**Solutions:**
1. Use existing environment variables:
   ```bash
   claude mcp add server npx -s user -e API_KEY="$EXISTING_VAR" -- -y package
   ```

2. Check variable syntax:
   ```bash
   # Correct
   -e KEY=value
   
   # Incorrect
   -e KEY value
   ```

#### Path Issues
**Problem:** `command not found` or path errors

**Solutions:**
1. Use absolute paths:
   ```bash
   claude mcp add server uv -s user -- --directory /absolute/path/to/project run command
   ```

2. Verify file exists:
   ```bash
   ls -la /path/to/file
   ```

3. Check permissions:
   ```bash
   chmod +x /path/to/script
   ```

#### Argument Separator Issues
**Problem:** Arguments not parsed correctly

**Solutions:**
1. Ensure proper `--` placement:
   ```bash
   # Correct
   claude mcp add name command -s user -e KEY=value -- arg1 arg2
   
   # Incorrect
   claude mcp add name command -- -s user -e KEY=value arg1 arg2
   ```

2. Quote complex arguments:
   ```bash
   claude mcp add name command -s user -- --arg "complex value"
   ```

### Command Reference

#### List servers:
```bash
claude mcp list
```

#### Get server details:
```bash
claude mcp get server-name
```

#### Remove server:
```bash
claude mcp remove server-name -s user
```

#### Available commands:
```bash
claude mcp --help
```

### File Locations

#### User scope configs:
- Linux/macOS: `~/.claude/mcp_servers.json`
- Windows: `%USERPROFILE%\.claude\mcp_servers.json`

#### Project scope configs:
- `.mcp.json` in project root

#### Logs and debugging:
```bash
# Check logs (if available)
claude mcp logs server-name

# Test connection manually
npx -y package-name  # For npx servers
uv --directory /path run command  # For uv servers
```

---

## Quick Reference Card

### Most Common Patterns
```bash
# NPX with API key
claude mcp add name npx -s user -e API_KEY=value -- -y package-name

# UV with directory
claude mcp add name uv -s user -- --directory /path run command

# Docker with env vars
claude mcp add name docker -s user -e KEY=value -- run -i --rm image

# Remote server
claude mcp add name remote -s user -t sse -- https://server.url/sse
```

### Essential Flags
- `-s user`: Global availability
- `-e KEY=value`: Environment variables
- `--`: Separator between Claude flags and command args

### Troubleshooting Checklist
1. ✅ Proper `--` placement
2. ✅ Environment variables set
3. ✅ Paths are absolute and exist
4. ✅ Packages are installed
5. ✅ API keys are valid
6. ✅ Permissions are correct

This reference covers all the patterns and examples from our conversation, organized for easy lookup and reuse.