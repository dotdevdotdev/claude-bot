# Testing Workflow

## 1. Test Strategy Planning

### Test Pyramid
```
         /\
        /  \  E2E Tests (UI/Integration)
       /    \ 
      /------\ Integration Tests (API/Service)
     /        \
    /----------\ Unit Tests (Functions/Components)
```

### Coverage Goals
- **Unit Tests**: 80%+ coverage
- **Integration Tests**: Critical paths
- **E2E Tests**: Key user journeys
- **Performance Tests**: Load-sensitive operations

## 2. Unit Testing

### JavaScript/TypeScript (Vitest/Jest)
```javascript
// Basic test structure
import { describe, it, expect, beforeEach, vi } from 'vitest';
import { functionToTest } from './module';

describe('functionToTest', () => {
  beforeEach(() => {
    // Reset mocks
    vi.clearAllMocks();
  });

  it('should handle normal case', () => {
    const result = functionToTest('input');
    expect(result).toBe('expected');
  });

  it('should handle edge case', () => {
    expect(() => functionToTest(null)).toThrow('Invalid input');
  });
});

// Mocking
vi.mock('./dependency', () => ({
  externalFunction: vi.fn().mockReturnValue('mocked value')
}));
```

### Python (pytest)
```python
import pytest
from unittest.mock import Mock, patch
from mymodule import function_to_test

class TestFunction:
    @pytest.fixture
    def setup_data(self):
        """Fixture for test data"""
        return {"key": "value"}
    
    def test_normal_case(self, setup_data):
        result = function_to_test(setup_data)
        assert result == "expected"
    
    def test_edge_case(self):
        with pytest.raises(ValueError, match="Invalid input"):
            function_to_test(None)
    
    @patch('mymodule.external_function')
    def test_with_mock(self, mock_func):
        mock_func.return_value = "mocked"
        result = function_to_test("input")
        mock_func.assert_called_once_with("input")
```

## 3. Integration Testing

### API Testing (Supertest)
```javascript
import { describe, it, expect, beforeAll, afterAll } from 'vitest';
import request from 'supertest';
import { app } from '../app';
import { db } from '../db';

describe('API Endpoints', () => {
  beforeAll(async () => {
    await db.migrate.latest();
    await db.seed.run();
  });

  afterAll(async () => {
    await db.destroy();
  });

  it('POST /api/users', async () => {
    const response = await request(app)
      .post('/api/users')
      .send({ name: 'Test User', email: 'test@example.com' })
      .expect(201);

    expect(response.body).toMatchObject({
      id: expect.any(Number),
      name: 'Test User',
      email: 'test@example.com'
    });
  });
});
```

### Database Testing
```javascript
// Test with real database (test environment)
describe('UserRepository', () => {
  beforeEach(async () => {
    await db('users').truncate();
  });

  it('should create and retrieve user', async () => {
    const user = await UserRepository.create({
      name: 'Test',
      email: 'test@example.com'
    });

    const found = await UserRepository.findById(user.id);
    expect(found.email).toBe('test@example.com');
  });
});
```

## 4. Component Testing

### React Testing Library
```javascript
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { UserForm } from './UserForm';

describe('UserForm', () => {
  it('should submit form with valid data', async () => {
    const onSubmit = vi.fn();
    const user = userEvent.setup();
    
    render(<UserForm onSubmit={onSubmit} />);
    
    await user.type(screen.getByLabelText('Name'), 'John Doe');
    await user.type(screen.getByLabelText('Email'), 'john@example.com');
    await user.click(screen.getByRole('button', { name: 'Submit' }));
    
    await waitFor(() => {
      expect(onSubmit).toHaveBeenCalledWith({
        name: 'John Doe',
        email: 'john@example.com'
      });
    });
  });
});
```

## 5. E2E Testing

### Playwright
```javascript
import { test, expect } from '@playwright/test';

test.describe('User Journey', () => {
  test('complete signup flow', async ({ page }) => {
    await page.goto('/signup');
    
    // Fill form
    await page.fill('[name="email"]', 'test@example.com');
    await page.fill('[name="password"]', 'securePassword123');
    await page.click('button[type="submit"]');
    
    // Verify redirect
    await expect(page).toHaveURL('/dashboard');
    await expect(page.locator('h1')).toContainText('Welcome');
  });
});
```

### Cypress
```javascript
describe('User Journey', () => {
  it('completes signup flow', () => {
    cy.visit('/signup');
    
    cy.get('[name="email"]').type('test@example.com');
    cy.get('[name="password"]').type('securePassword123');
    cy.get('button[type="submit"]').click();
    
    cy.url().should('include', '/dashboard');
    cy.contains('h1', 'Welcome').should('be.visible');
  });
});
```

## 6. Test Data Management

### Fixtures
```javascript
// fixtures/users.json
{
  "validUser": {
    "name": "John Doe",
    "email": "john@example.com",
    "role": "user"
  },
  "adminUser": {
    "name": "Admin User",
    "email": "admin@example.com",
    "role": "admin"
  }
}

// Using fixtures
import users from './fixtures/users.json';

test('user permissions', () => {
  const result = checkPermissions(users.validUser);
  expect(result).toBe(false);
});
```

### Factories
```javascript
// factories/user.factory.js
import { faker } from '@faker-js/faker';

export const createUser = (overrides = {}) => ({
  id: faker.number.int(),
  name: faker.person.fullName(),
  email: faker.internet.email(),
  createdAt: faker.date.past(),
  ...overrides
});

// Usage
const testUser = createUser({ role: 'admin' });
```

## 7. Performance Testing

### Load Testing with k6
```javascript
import http from 'k6/http';
import { check, sleep } from 'k6';

export const options = {
  stages: [
    { duration: '30s', target: 20 },  // Ramp up
    { duration: '1m', target: 20 },   // Stay at 20 users
    { duration: '30s', target: 0 },   // Ramp down
  ],
  thresholds: {
    http_req_duration: ['p(95)<500'], // 95% of requests under 500ms
  },
};

export default function () {
  const res = http.get('http://localhost:3000/api/users');
  check(res, {
    'status is 200': (r) => r.status === 200,
    'response time < 500ms': (r) => r.timings.duration < 500,
  });
  sleep(1);
}
```

## 8. Test Commands

### package.json Scripts
```json
{
  "scripts": {
    "test": "vitest",
    "test:ui": "vitest --ui",
    "test:watch": "vitest --watch",
    "test:coverage": "vitest --coverage",
    "test:e2e": "playwright test",
    "test:e2e:ui": "playwright test --ui",
    "test:integration": "vitest --config vitest.integration.config.ts",
    "test:unit": "vitest src/**/*.unit.test.ts",
    "test:ci": "vitest --run --coverage"
  }
}
```

## 9. CI Testing Strategy

### GitHub Actions
```yaml
name: Tests

on: [push, pull_request]

jobs:
  unit-tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
      - run: npm ci
      - run: npm run test:unit
      
  integration-tests:
    runs-on: ubuntu-latest
    services:
      postgres:
        image: postgres:15
        env:
          POSTGRES_PASSWORD: postgres
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
      - run: npm ci
      - run: npm run test:integration
        env:
          DATABASE_URL: postgresql://postgres:postgres@localhost/test
          
  e2e-tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
      - run: npm ci
      - run: npx playwright install --with-deps
      - run: npm run build
      - run: npm run test:e2e
```

## 10. Testing Best Practices

### Test Organization
```
tests/
├── unit/           # Unit tests
├── integration/    # Integration tests
├── e2e/           # End-to-end tests
├── fixtures/      # Test data
├── helpers/       # Test utilities
└── setup.ts       # Test configuration
```

### Naming Conventions
- **Files**: `*.test.ts`, `*.spec.ts`
- **Test suites**: Describe what is being tested
- **Test cases**: Should describe expected behavior
- **Use AAA pattern**: Arrange, Act, Assert

### Test Quality Checklist
- [ ] Tests are independent (no shared state)
- [ ] Tests are deterministic (same result every time)
- [ ] Tests are fast (mock external dependencies)
- [ ] Tests are readable (clear descriptions)
- [ ] Tests cover happy path and edge cases
- [ ] Tests verify behavior, not implementation
- [ ] Mocks are properly cleaned up
- [ ] Async operations are properly handled