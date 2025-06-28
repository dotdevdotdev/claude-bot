# Deployment Workflow

## 1. Pre-Deployment Checklist

### Code Quality
- [ ] All tests passing locally
- [ ] Linting passes with no errors
- [ ] Type checking passes
- [ ] Security audit clean (`npm audit`, `pip-audit`)
- [ ] No hardcoded secrets or credentials
- [ ] Environment variables documented

### Build Verification
```bash
# Clean build test
rm -rf dist/ build/
npm run build  # or equivalent
# Verify build output exists and is correct
```

### Database Migrations
- [ ] Migrations tested on staging
- [ ] Rollback plan documented
- [ ] Data backup completed
- [ ] Migration can run without downtime

## 2. Environment Configuration

### Environment Variables
```bash
# .env.production.example
NODE_ENV=production
DATABASE_URL=postgresql://user:pass@host:5432/db
REDIS_URL=redis://host:6379
API_KEY=your-production-key
SENTRY_DSN=https://key@sentry.io/project
LOG_LEVEL=info
CORS_ORIGIN=https://app.example.com
```

### Secrets Management
```bash
# Using dotenv-vault
npx dotenv-vault@latest push production

# AWS Secrets Manager
aws secretsmanager create-secret \
  --name prod/myapp/env \
  --secret-string file://.env.production

# GitHub Secrets (for Actions)
gh secret set DATABASE_URL --body "postgresql://..."
```

## 3. Deployment Strategies

### Blue-Green Deployment
```yaml
# Deploy new version alongside old
# Switch traffic when ready
# Keep old version for quick rollback

steps:
  1. Deploy to green environment
  2. Run smoke tests on green
  3. Switch load balancer to green
  4. Monitor for issues
  5. Terminate blue after stability confirmed
```

### Rolling Deployment
```yaml
# Gradually replace instances
# Zero downtime but slower

steps:
  1. Deploy to subset of instances (25%)
  2. Monitor health metrics
  3. Continue deployment in batches
  4. Rollback if errors spike
```

### Canary Deployment
```yaml
# Test with small traffic percentage
# Gradually increase if successful

steps:
  1. Deploy to canary instances (5% traffic)
  2. Monitor error rates and performance
  3. Increase traffic gradually (5% → 25% → 50% → 100%)
  4. Full rollback if metrics degrade
```

## 4. Platform-Specific Deployments

### Vercel
```bash
# Install CLI
npm i -g vercel

# Deploy
vercel --prod

# With GitHub Actions
# .github/workflows/deploy.yml
name: Deploy to Vercel
on:
  push:
    branches: [main]
jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: vercel/action@v1
        with:
          vercel-token: ${{ secrets.VERCEL_TOKEN }}
          vercel-org-id: ${{ secrets.VERCEL_ORG_ID }}
          vercel-project-id: ${{ secrets.VERCEL_PROJECT_ID }}
          production: true
```

### AWS (via CDK)
```typescript
// cdk/app-stack.ts
import * as cdk from 'aws-cdk-lib';
import * as ecs from 'aws-cdk-lib/aws-ecs';
import * as ec2 from 'aws-cdk-lib/aws-ec2';

export class AppStack extends cdk.Stack {
  constructor(scope: Construct, id: string, props?: cdk.StackProps) {
    super(scope, id, props);

    const vpc = new ec2.Vpc(this, 'AppVPC');
    
    const cluster = new ecs.Cluster(this, 'Cluster', { vpc });
    
    const taskDefinition = new ecs.FargateTaskDefinition(this, 'TaskDef');
    
    const container = taskDefinition.addContainer('app', {
      image: ecs.ContainerImage.fromRegistry('myapp:latest'),
      memoryLimitMiB: 512,
      environment: {
        NODE_ENV: 'production'
      }
    });
    
    container.addPortMappings({ containerPort: 3000 });
    
    new ecs.FargateService(this, 'Service', {
      cluster,
      taskDefinition,
      desiredCount: 2
    });
  }
}

// Deploy
// cdk deploy --require-approval never
```

### Docker Deployment
```dockerfile
# Dockerfile
FROM node:20-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production

FROM node:20-alpine
WORKDIR /app
COPY --from=builder /app/node_modules ./node_modules
COPY . .
EXPOSE 3000
CMD ["node", "dist/index.js"]
```

```yaml
# docker-compose.yml
version: '3.8'
services:
  app:
    build: .
    ports:
      - "3000:3000"
    environment:
      - NODE_ENV=production
    depends_on:
      - postgres
      - redis
  
  postgres:
    image: postgres:15
    environment:
      POSTGRES_PASSWORD: ${DB_PASSWORD}
    volumes:
      - pgdata:/var/lib/postgresql/data
  
  redis:
    image: redis:7-alpine
    command: redis-server --requirepass ${REDIS_PASSWORD}

volumes:
  pgdata:
```

### Kubernetes
```yaml
# k8s/deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: myapp
spec:
  replicas: 3
  selector:
    matchLabels:
      app: myapp
  template:
    metadata:
      labels:
        app: myapp
    spec:
      containers:
      - name: app
        image: myapp:latest
        ports:
        - containerPort: 3000
        env:
        - name: NODE_ENV
          value: "production"
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: myapp-secrets
              key: database-url
        resources:
          requests:
            memory: "256Mi"
            cpu: "250m"
          limits:
            memory: "512Mi"
            cpu: "500m"
        livenessProbe:
          httpGet:
            path: /health
            port: 3000
          initialDelaySeconds: 30
          periodSeconds: 10
---
apiVersion: v1
kind: Service
metadata:
  name: myapp-service
spec:
  selector:
    app: myapp
  ports:
    - protocol: TCP
      port: 80
      targetPort: 3000
  type: LoadBalancer
```

## 5. Database Deployment

### Migration Strategy
```bash
# Safe migration workflow
1. Backup production database
2. Test migration on staging
3. Run migration in transaction
4. Verify data integrity
5. Have rollback script ready

# Example migration script
#!/bin/bash
set -e

echo "Starting database migration..."

# Backup
pg_dump $DATABASE_URL > backup-$(date +%Y%m%d-%H%M%S).sql

# Run migrations
npm run migrate:up

# Verify
npm run migrate:verify

echo "Migration completed successfully"
```

## 6. Monitoring Setup

### Health Checks
```javascript
// health.js
app.get('/health', async (req, res) => {
  const checks = {
    database: await checkDatabase(),
    redis: await checkRedis(),
    disk: await checkDiskSpace(),
    memory: process.memoryUsage()
  };
  
  const healthy = Object.values(checks).every(c => c.status === 'ok');
  res.status(healthy ? 200 : 503).json(checks);
});
```

### Logging
```javascript
// Production logging setup
import winston from 'winston';

const logger = winston.createLogger({
  level: process.env.LOG_LEVEL || 'info',
  format: winston.format.json(),
  transports: [
    new winston.transports.File({ filename: 'error.log', level: 'error' }),
    new winston.transports.File({ filename: 'combined.log' })
  ]
});

// Structured logging
logger.info('User action', {
  userId: user.id,
  action: 'login',
  timestamp: new Date().toISOString(),
  metadata: { ip: req.ip }
});
```

### Metrics
```javascript
// Prometheus metrics
import { register, Counter, Histogram } from 'prom-client';

const httpRequestDuration = new Histogram({
  name: 'http_request_duration_seconds',
  help: 'Duration of HTTP requests in seconds',
  labelNames: ['method', 'route', 'status']
});

const httpRequestTotal = new Counter({
  name: 'http_requests_total',
  help: 'Total number of HTTP requests',
  labelNames: ['method', 'route', 'status']
});

// Expose metrics endpoint
app.get('/metrics', async (req, res) => {
  res.set('Content-Type', register.contentType);
  res.end(await register.metrics());
});
```

## 7. Post-Deployment

### Smoke Tests
```javascript
// smoke-tests.js
const smokeTests = [
  {
    name: 'Homepage loads',
    test: async () => {
      const res = await fetch('https://app.example.com');
      assert(res.status === 200);
    }
  },
  {
    name: 'API health check',
    test: async () => {
      const res = await fetch('https://api.example.com/health');
      const data = await res.json();
      assert(data.status === 'healthy');
    }
  },
  {
    name: 'Database connectivity',
    test: async () => {
      const res = await fetch('https://api.example.com/api/test-db');
      assert(res.status === 200);
    }
  }
];

// Run all smoke tests
for (const test of smokeTests) {
  try {
    await test.test();
    console.log(`✓ ${test.name}`);
  } catch (error) {
    console.error(`✗ ${test.name}:`, error.message);
    process.exit(1);
  }
}
```

### Rollback Plan
```bash
#!/bin/bash
# rollback.sh

echo "Starting rollback..."

# 1. Revert code deployment
kubectl rollout undo deployment/myapp
# or
git revert HEAD && git push

# 2. Revert database if needed
psql $DATABASE_URL < backup-latest.sql

# 3. Clear caches
redis-cli FLUSHALL

# 4. Notify team
curl -X POST $SLACK_WEBHOOK -d '{"text":"Rollback completed"}'
```

## 8. Deployment Checklist

### Before Deployment
- [ ] All tests passing
- [ ] Code reviewed and approved
- [ ] CHANGELOG.md updated
- [ ] Database migrations tested
- [ ] Environment variables configured
- [ ] Monitoring alerts configured
- [ ] Rollback plan documented

### During Deployment
- [ ] Monitor deployment progress
- [ ] Watch error rates
- [ ] Check resource utilization
- [ ] Verify health checks passing
- [ ] Run smoke tests

### After Deployment
- [ ] Verify all features working
- [ ] Check performance metrics
- [ ] Monitor error logs
- [ ] Update status page
- [ ] Notify stakeholders
- [ ] Document any issues
- [ ] Schedule retrospective if needed