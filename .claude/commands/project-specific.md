# Project-Specific Commands Template

This file should be customized for each project. Below are examples of how to document project-specific commands.

## Build Commands

```bash
# Example: Next.js project
npm run build:staging    # Build for staging environment
npm run build:prod      # Build for production with optimizations

# Example: Monorepo
npm run build:all       # Build all packages
npm run build:api       # Build API only
npm run build:web       # Build web app only
```

## Database Commands

```bash
# Example: Prisma
npm run db:migrate      # Run database migrations
npm run db:seed         # Seed database with test data
npm run db:reset        # Reset database and re-seed

# Example: TypeORM
npm run migration:run    # Run pending migrations
npm run migration:revert # Revert last migration
npm run migration:generate -- -n MigrationName
```

## Deployment Commands

```bash
# Example: Vercel
vercel --prod           # Deploy to production
vercel --env preview    # Deploy preview

# Example: AWS
npm run deploy:staging  # Deploy to staging
npm run deploy:prod     # Deploy to production
```

## Development Workflows

```bash
# Start all services
npm run dev:all

# Start specific services
npm run dev:api
npm run dev:web
npm run dev:worker

# Watch mode commands
npm run watch:css
npm run watch:types
```

## Testing Workflows

```bash
# Run tests for specific features
npm run test:auth
npm run test:api
npm run test:components

# Integration tests
npm run test:integration
npm run test:integration:docker  # With Docker dependencies
```

## Maintenance Commands

```bash
# Clean and rebuild
npm run clean           # Remove build artifacts
npm run clean:all       # Remove all generated files
npm run rebuild         # Clean and build

# Dependency management
npm run deps:check      # Check for outdated dependencies
npm run deps:update     # Update dependencies
npm run deps:audit      # Security audit
```

## Environment-Specific Commands

```bash
# Development
NODE_ENV=development npm run start

# Staging
NODE_ENV=staging npm run start

# Production
NODE_ENV=production npm run start
```

## Debugging Commands

```bash
# Node.js debugging
node --inspect index.js
node --inspect-brk index.js  # Break on first line

# Verbose logging
DEBUG=app:* npm run dev
VERBOSE=true npm run test
```

## Performance Commands

```bash
# Profiling
npm run profile         # Run performance profiling
npm run bundle:analyze  # Analyze bundle size

# Benchmarks
npm run benchmark       # Run performance benchmarks
npm run lighthouse      # Run Lighthouse audit
```