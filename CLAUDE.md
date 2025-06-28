# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a comprehensive template repository for starting new Claude Code projects. It contains an extensive `.claude/` directory with reusable commands, MCP server configurations, prompts, workflows, and best practices.

## Purpose

This repository serves as a starter template that can be cloned when beginning any new project with Claude Code. It provides:
- Common command references
- MCP server configuration examples
- Reusable prompt templates
- Standard development workflows
- Best practices and patterns

## Repository Structure

```
.claude/
├── commands/          # Command references
│   ├── common-dev.md      # Common development commands
│   └── project-specific.md # Template for project commands
├── mcp/              # MCP server configurations
│   ├── README.md          # MCP overview and available servers
│   ├── example-configs.json # Example configurations
│   └── use-cases.md       # When to use each server
├── prompts/          # Reusable prompts
│   ├── code-review.md     # Code review prompts
│   ├── implementation.md  # Feature implementation prompts
│   └── analysis.md        # Code analysis prompts
├── workflows/        # Development workflows
│   ├── new-project-setup.md # Project initialization
│   ├── debugging-workflow.md # Debugging strategies
│   ├── testing-workflow.md   # Testing approaches
│   └── deployment-workflow.md # Deployment procedures
└── instructions/     # Best practices
    ├── best-practices.md   # Claude Code best practices
    └── common-patterns.md  # Common code patterns
```

## Using This Template

1. **Clone for New Projects**: Clone this repository as a starting point for new projects
2. **Customize**: Update the `.claude/` directory contents based on your project's needs
3. **Maintain**: Keep the CLAUDE.md file updated with project-specific information

## Key Resources

- **Commands**: Check `.claude/commands/` for common development commands
- **MCP Servers**: See `.claude/mcp/` for server configurations and use cases
- **Prompts**: Use `.claude/prompts/` for consistent, effective prompts
- **Workflows**: Follow `.claude/workflows/` for standard procedures
- **Best Practices**: Review `.claude/instructions/` for optimal Claude Code usage

## Repository Information

- **Remote**: ssh://git@github.com/dotdevdotdev/claude-bot.git
- **Default Branch**: master
- **Purpose**: Template repository for Claude Code projects