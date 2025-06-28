# Debugging Workflow

## 1. Initial Error Analysis

### Understand the Error
1. **Read the full error message** - Don't skip any part
2. **Identify error type** - Syntax, runtime, logic, or build error
3. **Note the stack trace** - File paths and line numbers
4. **Check error timing** - When does it occur (build, runtime, test)

### Quick Checks
```bash
# Check for syntax errors
npm run typecheck  # TypeScript
python -m py_compile file.py  # Python

# Check dependencies
npm ls  # List installed packages
pip freeze  # Python packages

# Check environment
node --version
npm --version
echo $NODE_ENV
```

## 2. Reproduction Steps

### Isolate the Problem
1. **Minimal reproduction** - Reduce code to smallest failing case
2. **Environment consistency** - Same Node/Python version, OS
3. **Clean state** - Clear cache, fresh install
4. **Document steps** - Exact commands to reproduce

### Common Reset Commands
```bash
# Node.js
rm -rf node_modules package-lock.json
npm cache clean --force
npm install

# Python
deactivate
rm -rf venv
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# General
git clean -xfd  # Remove all untracked files (careful!)
```

## 3. Debugging Tools

### Node.js Debugging
```bash
# Basic debugging
node --inspect index.js
node --inspect-brk index.js  # Break on first line

# With TypeScript
node --inspect -r tsx src/index.ts

# VS Code launch.json
{
  "type": "node",
  "request": "launch",
  "name": "Debug TypeScript",
  "runtimeArgs": ["-r", "tsx"],
  "args": ["${workspaceFolder}/src/index.ts"]
}
```

### Python Debugging
```python
# Using pdb
import pdb; pdb.set_trace()  # Breakpoint

# Using ipdb (better interface)
import ipdb; ipdb.set_trace()

# Print debugging with context
print(f"DEBUG: {variable=}")  # Python 3.8+
```

### Browser Debugging
```javascript
// Breakpoints
debugger;  // Pauses execution

// Console methods
console.log('Basic log');
console.error('Error log');
console.table(data);  // Tabular data
console.time('timer');  // Performance
console.timeEnd('timer');
console.trace();  // Stack trace
```

## 4. Common Debug Scenarios

### API/Network Issues
```bash
# Test endpoints
curl -X GET http://localhost:3000/api/endpoint
curl -X POST http://localhost:3000/api/endpoint \
  -H "Content-Type: application/json" \
  -d '{"key": "value"}'

# Network debugging
# Browser DevTools Network tab
# Use Postman/Insomnia for API testing
```

### Database Issues
```sql
-- Check connections
SELECT * FROM pg_stat_activity;  -- PostgreSQL
SHOW PROCESSLIST;  -- MySQL

-- Enable query logging
SET log_statement = 'all';  -- PostgreSQL
SET GLOBAL general_log = 'ON';  -- MySQL
```

### Memory/Performance Issues
```bash
# Node.js memory
node --inspect --max-old-space-size=4096 index.js
# Use Chrome DevTools Memory Profiler

# Python memory
pip install memory_profiler
python -m memory_profiler script.py
```

## 5. Logging Strategies

### Structured Logging
```javascript
// Node.js with Winston
const winston = require('winston');
const logger = winston.createLogger({
  level: process.env.LOG_LEVEL || 'info',
  format: winston.format.json(),
  transports: [
    new winston.transports.File({ filename: 'error.log', level: 'error' }),
    new winston.transports.File({ filename: 'combined.log' })
  ]
});

// Usage
logger.error('Error message', { error: err, context: { userId: 123 } });
```

### Debug Namespaces
```bash
# Using debug package
DEBUG=app:* npm start  # All app logs
DEBUG=app:db npm start  # Only database logs
DEBUG=* npm start  # Everything
```

## 6. Testing for Bugs

### Unit Test Debugging
```bash
# Run specific test
npm test -- --grep "specific test name"
pytest -k "test_name"

# Verbose output
npm test -- --verbose
pytest -v

# With debugging
node --inspect ./node_modules/.bin/jest
pytest --pdb  # Drop into debugger on failure
```

### Integration Test Debugging
```javascript
// Add detailed logging
beforeEach(() => {
  console.log('Test setup state:', testData);
});

afterEach(() => {
  console.log('Test end state:', result);
});
```

## 7. Common Fixes

### Dependency Issues
```bash
# Clear all caches
npm cache clean --force
yarn cache clean
pip cache purge

# Check for conflicts
npm ls  # Look for UNMET PEER DEPENDENCY
pip check  # Check for incompatibilities

# Lock file issues
rm package-lock.json && npm install
rm yarn.lock && yarn install
```

### Environment Issues
```bash
# Verify environment variables
printenv | grep MY_APP
node -e "console.log(process.env)"

# Common fixes
export NODE_ENV=development
export DEBUG=*
```

### Permission Issues
```bash
# File permissions
ls -la problematic-file
chmod 644 file  # Read for all, write for owner
chmod 755 directory  # Execute needed for directories

# npm permissions
npm config set prefix ~/.npm-global
export PATH=~/.npm-global/bin:$PATH
```

## 8. Debug Checklist

- [ ] Error message fully read and understood
- [ ] Stack trace analyzed for root cause
- [ ] Problem reproduced in isolation
- [ ] Environment variables checked
- [ ] Dependencies up to date and compatible
- [ ] Logs examined at appropriate verbosity
- [ ] Network requests inspected if applicable
- [ ] Database queries logged and analyzed
- [ ] Memory usage profiled if performance issue
- [ ] Tests written to prevent regression