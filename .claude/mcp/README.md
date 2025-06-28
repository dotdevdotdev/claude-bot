# MCP (Model Context Protocol) Servers

This directory contains configurations and examples for MCP servers that can be used with Claude Code.

## What is MCP?

MCP (Model Context Protocol) is a protocol that allows Claude to interact with external tools and services through standardized server implementations.

## Available MCP Servers

### Official Servers

1. **Filesystem** - File operations beyond Claude's built-in capabilities
2. **Git** - Advanced git operations
3. **GitHub** - GitHub API interactions
4. **Brave Search** - Web search capabilities
5. **Google Maps** - Location and mapping services
6. **Memory** - Persistent memory across conversations
7. **Playwright** - Browser automation
8. **Puppeteer** - Alternative browser automation
9. **Slack** - Slack integration
10. **PostgreSQL** - Database operations
11. **SQLite** - Lightweight database operations

### Community Servers

- **Spotify** - Music playback control
- **AWS** - AWS service interactions
- **Docker** - Container management
- **Kubernetes** - K8s cluster management
- **Notion** - Notion workspace integration
- **Linear** - Issue tracking
- **Stripe** - Payment processing

## Configuration

MCP servers are configured in your Claude Desktop settings. See the example configurations in this directory for common setups.

## Creating Custom MCP Servers

You can create custom MCP servers for your specific needs. See `custom-server-template/` for a starting template.