# New Project Setup Workflow

## 1. Project Initialization

### For Node.js/TypeScript Projects
```bash
# Initialize package.json
npm init -y

# Install TypeScript and essential dev dependencies
npm install -D typescript @types/node tsx
npm install -D eslint prettier eslint-config-prettier
npm install -D @typescript-eslint/parser @typescript-eslint/eslint-plugin
npm install -D vitest @vitest/ui @vitest/coverage-v8
npm install -D husky lint-staged

# Initialize TypeScript
npx tsc --init

# Initialize ESLint
npx eslint --init
```

### For Python Projects
```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # or `venv\Scripts\activate` on Windows

# Create requirements files
touch requirements.txt requirements-dev.txt

# Install development tools
pip install -r requirements-dev.txt
# Contents: pytest pytest-cov black ruff mypy pre-commit
```

### For React Projects
```bash
# Using Vite
npm create vite@latest my-app -- --template react-ts
cd my-app
npm install

# Additional setup
npm install -D @testing-library/react @testing-library/jest-dom
npm install -D @types/react @types/react-dom
```

## 2. Project Structure Creation

```bash
# Common directories
mkdir -p src tests docs .github/workflows

# Config files
touch .gitignore .env.example .editorconfig

# Documentation
touch README.md CONTRIBUTING.md LICENSE
```

## 3. Git Configuration

```bash
# Initialize git
git init

# Create .gitignore
cat > .gitignore << 'EOF'
# Dependencies
node_modules/
venv/
__pycache__/

# Environment
.env
.env.local
*.log

# Build outputs
dist/
build/
*.egg-info/

# IDE
.vscode/
.idea/
*.swp
.DS_Store

# Testing
coverage/
.coverage
.pytest_cache/
EOF

# Set up pre-commit hooks
npx husky init
npm pkg set scripts.prepare="husky"
```

## 4. Development Scripts Setup

### package.json scripts (Node.js)
```json
{
  "scripts": {
    "dev": "tsx watch src/index.ts",
    "build": "tsc",
    "start": "node dist/index.js",
    "test": "vitest",
    "test:ui": "vitest --ui",
    "test:coverage": "vitest --coverage",
    "lint": "eslint src --ext .ts,.tsx",
    "lint:fix": "eslint src --ext .ts,.tsx --fix",
    "format": "prettier --write \"src/**/*.{ts,tsx,js,jsx,json,md}\"",
    "typecheck": "tsc --noEmit",
    "prepare": "husky"
  }
}
```

## 5. CI/CD Setup

### GitHub Actions
```yaml
# .github/workflows/ci.yml
name: CI

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'npm'
      - run: npm ci
      - run: npm run lint
      - run: npm run typecheck
      - run: npm test
      - run: npm run build
```

## 6. Environment Configuration

```bash
# Create .env.example
cat > .env.example << 'EOF'
# Application
NODE_ENV=development
PORT=3000

# Database
DATABASE_URL=postgresql://user:password@localhost:5432/dbname

# API Keys (obtain from respective services)
API_KEY=your-api-key-here

# Feature Flags
ENABLE_FEATURE_X=false
EOF
```

## 7. Documentation Templates

### README.md
```markdown
# Project Name

Brief description of what this project does.

## Prerequisites

- Node.js >= 18
- npm >= 9

## Installation

\`\`\`bash
npm install
cp .env.example .env
# Edit .env with your configuration
\`\`\`

## Development

\`\`\`bash
npm run dev
\`\`\`

## Testing

\`\`\`bash
npm test
\`\`\`

## Building

\`\`\`bash
npm run build
\`\`\`

## License

MIT
```

## 8. VS Code Configuration

```json
// .vscode/settings.json
{
  "editor.formatOnSave": true,
  "editor.codeActionsOnSave": {
    "source.fixAll.eslint": true
  },
  "typescript.tsdk": "node_modules/typescript/lib"
}
```

## 9. Final Steps

1. Run initial format and lint
2. Create initial commit
3. Set up remote repository
4. Configure branch protection rules
5. Set up environment secrets
6. Create initial issues/project board