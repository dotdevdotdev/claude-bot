# Claude Code Best Practices

## 1. Effective Communication

### Be Specific with Requests
```
❌ "Fix the bug"
✅ "Fix the TypeError on line 42 of user.service.ts when user is null"

❌ "Make it faster"
✅ "Optimize the database query in getUsersByRole() - it's taking 5+ seconds"
```

### Provide Context
- Share error messages completely
- Include relevant code snippets
- Mention what you've already tried
- Specify your environment (OS, versions)

## 2. Project Structure

### Use CLAUDE.md
Always maintain an up-to-date `CLAUDE.md` file that includes:
- Common commands for your project
- Architecture overview
- Key design decisions
- Testing approach
- Deployment process

### Organize .claude Directory
```
.claude/
├── commands/       # Project-specific commands
├── instructions/   # Coding standards, patterns
├── prompts/        # Reusable prompt templates
├── workflows/      # Multi-step procedures
└── context/        # Additional context files
```

## 3. Working with Code

### Small, Focused Changes
- Request one feature or fix at a time
- Break large tasks into smaller steps
- Test each change before moving to the next

### Review Generated Code
- Always review code before running
- Check for security implications
- Ensure it follows your project's patterns
- Verify test coverage

## 4. Debugging Efficiently

### Provide Error Context
```
✅ Good:
"Getting 'Cannot read property x of undefined' at line 15 in processUser()
when calling with an empty array. Here's the function: [code]"

❌ Bad:
"It's throwing an error"
```

### Use Incremental Debugging
1. Start with minimal reproduction
2. Add complexity gradually
3. Test each step
4. Document what works/fails

## 5. Security Practices

### Never Share Secrets
- Use environment variables
- Provide example values only
- Mask sensitive data in logs/errors
- Use `.env.example` files

### Code Review for Security
- Check for SQL injection risks
- Validate all inputs
- Review authentication logic
- Ensure proper error handling

## 6. Performance Optimization

### Measure First
```bash
# Profile before optimizing
npm run profile
# or
python -m cProfile script.py
```

### Optimize Systematically
1. Identify bottlenecks with profiling
2. Focus on biggest impact areas
3. Measure improvements
4. Document optimizations

## 7. Testing Strategies

### Test-Driven Requests
```
"Create a function that:
- Takes an array of users
- Returns users older than 18
- Handles null/undefined gracefully
- Include unit tests for edge cases"
```

### Maintain Test Coverage
- Request tests with new features
- Update tests when changing code
- Run tests before deployment

## 8. Using MCP Servers

### Choose the Right Tool
- File operations → Built-in tools
- GitHub operations → GitHub MCP server
- Web scraping → Playwright MCP server
- Database work → PostgreSQL/SQLite MCP

### Configure Properly
- Set up authentication tokens
- Use appropriate permissions
- Test configurations locally

## 9. Workflow Automation

### Create Reusable Workflows
Document common tasks in `.claude/workflows/`:
- New feature workflow
- Bug fix workflow
- Release workflow
- Deployment checklist

### Use Todo Lists
For complex tasks, ask Claude to:
- Create a todo list
- Track progress
- Update as tasks complete

## 10. Common Patterns

### Feature Development
1. Understand requirements
2. Research existing code
3. Plan implementation
4. Write tests first
5. Implement feature
6. Refactor if needed
7. Update documentation

### Bug Fixing
1. Reproduce the issue
2. Isolate the problem
3. Understand root cause
4. Implement fix
5. Add regression test
6. Verify related functionality

### Code Refactoring
1. Ensure tests exist
2. Make small changes
3. Run tests frequently
4. Commit working states
5. Document improvements

## 11. Productivity Tips

### Use Keyboard Shortcuts
- `Ctrl+K`: Clear terminal
- `Ctrl+U`: Navigate up in output
- `Ctrl+D`: Navigate down
- `/undo`: Undo last change

### Batch Related Tasks
```
"Please:
1. Add input validation to createUser()
2. Add error handling for database failures
3. Write tests for both scenarios"
```

### Save Common Prompts
Store frequently used prompts in `.claude/prompts/` for reuse

## 12. Troubleshooting

### When Things Go Wrong
1. Check the full error message
2. Verify file paths are correct
3. Ensure dependencies are installed
4. Check environment variables
5. Look for typos in commands

### Getting Help
- Use `/help` for Claude Code help
- Check docs.anthropic.com/claude-code
- Report issues on GitHub
- Provide minimal reproductions

## 13. Advanced Usage

### Multi-File Operations
```
"Rename UserService to UserManager across all files,
update imports, and fix any TypeScript errors"
```

### Complex Refactoring
```
"Convert this callback-based code to use async/await,
maintain error handling, and update all callers"
```

### Architecture Changes
```
"Restructure this monolithic service into separate
domain services following clean architecture"
```

## 14. Collaboration

### Document Decisions
```markdown
<!-- CLAUDE.md -->
## Architecture Decisions

### 2024-01-15: Chose PostgreSQL over MongoDB
- Need ACID compliance
- Complex relationships
- Strong consistency requirements
```

### Maintain Standards
- Follow existing code style
- Use project's naming conventions
- Match testing patterns
- Keep documentation updated