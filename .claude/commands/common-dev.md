# Common Development Commands

## Node.js/JavaScript Projects

### Setup
```bash
npm install  # Install dependencies
npm ci       # Clean install from package-lock.json
yarn install # Alternative with Yarn
pnpm install # Alternative with pnpm
```

### Development
```bash
npm run dev      # Start development server
npm run start    # Start production server
npm run build    # Build for production
npm run preview  # Preview production build
```

### Testing
```bash
npm test              # Run all tests
npm run test:watch    # Run tests in watch mode
npm run test:coverage # Run tests with coverage
npm run test:unit     # Run unit tests only
npm run test:e2e      # Run end-to-end tests
```

### Code Quality
```bash
npm run lint        # Run linter
npm run lint:fix    # Fix linting issues
npm run format      # Format code with Prettier
npm run typecheck   # TypeScript type checking
```

## Python Projects

### Setup
```bash
python -m venv venv           # Create virtual environment
source venv/bin/activate      # Activate (Linux/Mac)
venv\Scripts\activate         # Activate (Windows)
pip install -r requirements.txt
pip install -e .              # Install in editable mode
```

### Development
```bash
python main.py          # Run main script
python -m mypackage     # Run as module
uvicorn app:app --reload # FastAPI development server
flask run --debug       # Flask development server
```

### Testing
```bash
pytest                  # Run all tests
pytest -v              # Verbose output
pytest --cov           # With coverage
pytest -k "test_name"  # Run specific test
pytest -x              # Stop on first failure
```

### Code Quality
```bash
ruff check .           # Run ruff linter
ruff format .          # Format with ruff
black .                # Format with black
mypy .                 # Type checking
flake8                 # Alternative linter
```

## Git Commands

### Basic Operations
```bash
git status            # Check status
git add .            # Stage all changes
git commit -m "msg"  # Commit with message
git push             # Push to remote
git pull             # Pull from remote
```

### Branching
```bash
git checkout -b feature/name  # Create and switch branch
git checkout main            # Switch to main
git merge feature/name       # Merge branch
git branch -d feature/name   # Delete local branch
```

### GitHub CLI
```bash
gh pr create --title "Title" --body "Description"  # Create PR
gh pr list                                         # List PRs
gh pr checkout 123                                 # Checkout PR
gh issue create --title "Title"                    # Create issue
```

## Docker Commands

```bash
docker build -t app .         # Build image
docker run -p 3000:3000 app  # Run container
docker-compose up            # Start services
docker-compose down          # Stop services
docker ps                    # List containers
docker logs container-id     # View logs
```

## Database Commands

### PostgreSQL
```bash
psql -U username -d database  # Connect to database
pg_dump database > backup.sql # Backup database
psql database < backup.sql    # Restore database
```

### MongoDB
```bash
mongosh                      # Connect to MongoDB
mongodump --db database      # Backup database
mongorestore --db database   # Restore database
```

## Useful Shell Commands

```bash
find . -name "*.js"          # Find files by pattern
grep -r "pattern" .          # Search in files
rg "pattern"                 # Faster search with ripgrep
tree -I node_modules         # Show directory tree
watch -n 2 'command'         # Run command every 2 seconds
```