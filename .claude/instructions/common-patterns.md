# Common Development Patterns

## 1. API Patterns

### RESTful CRUD Operations
```javascript
// Express.js example
const router = express.Router();

// Create
router.post('/users', async (req, res) => {
  try {
    const user = await User.create(req.body);
    res.status(201).json(user);
  } catch (error) {
    res.status(400).json({ error: error.message });
  }
});

// Read (List)
router.get('/users', async (req, res) => {
  const { page = 1, limit = 10, sort = '-createdAt' } = req.query;
  const users = await User.find()
    .limit(limit * 1)
    .skip((page - 1) * limit)
    .sort(sort);
  res.json({ users, page, limit });
});

// Read (Single)
router.get('/users/:id', async (req, res) => {
  const user = await User.findById(req.params.id);
  if (!user) return res.status(404).json({ error: 'User not found' });
  res.json(user);
});

// Update
router.put('/users/:id', async (req, res) => {
  const user = await User.findByIdAndUpdate(
    req.params.id,
    req.body,
    { new: true, runValidators: true }
  );
  if (!user) return res.status(404).json({ error: 'User not found' });
  res.json(user);
});

// Delete
router.delete('/users/:id', async (req, res) => {
  const user = await User.findByIdAndDelete(req.params.id);
  if (!user) return res.status(404).json({ error: 'User not found' });
  res.status(204).send();
});
```

### Error Handling Middleware
```javascript
// Error handler
class AppError extends Error {
  constructor(message, statusCode) {
    super(message);
    this.statusCode = statusCode;
    this.isOperational = true;
  }
}

// Async handler wrapper
const asyncHandler = (fn) => (req, res, next) => {
  Promise.resolve(fn(req, res, next)).catch(next);
};

// Global error middleware
app.use((err, req, res, next) => {
  const { statusCode = 500, message } = err;
  res.status(statusCode).json({
    error: {
      message,
      ...(process.env.NODE_ENV === 'development' && { stack: err.stack })
    }
  });
});
```

## 2. Authentication Patterns

### JWT Authentication
```javascript
// auth.middleware.js
const jwt = require('jsonwebtoken');

const generateToken = (user) => {
  return jwt.sign(
    { id: user.id, email: user.email },
    process.env.JWT_SECRET,
    { expiresIn: '7d' }
  );
};

const verifyToken = asyncHandler(async (req, res, next) => {
  const token = req.headers.authorization?.replace('Bearer ', '');
  
  if (!token) {
    throw new AppError('No token provided', 401);
  }
  
  try {
    const decoded = jwt.verify(token, process.env.JWT_SECRET);
    req.user = await User.findById(decoded.id).select('-password');
    next();
  } catch (error) {
    throw new AppError('Invalid token', 401);
  }
});

// Usage
router.post('/login', async (req, res) => {
  const { email, password } = req.body;
  const user = await User.findOne({ email });
  
  if (!user || !(await user.comparePassword(password))) {
    throw new AppError('Invalid credentials', 401);
  }
  
  res.json({
    token: generateToken(user),
    user: user.toJSON()
  });
});
```

### Role-Based Access Control
```javascript
const authorize = (...roles) => {
  return (req, res, next) => {
    if (!roles.includes(req.user.role)) {
      throw new AppError('Insufficient permissions', 403);
    }
    next();
  };
};

// Usage
router.delete(
  '/users/:id',
  verifyToken,
  authorize('admin'),
  deleteUser
);
```

## 3. Database Patterns

### Repository Pattern
```javascript
// user.repository.js
class UserRepository {
  async create(userData) {
    const user = new User(userData);
    return user.save();
  }
  
  async findById(id) {
    return User.findById(id);
  }
  
  async findByEmail(email) {
    return User.findOne({ email });
  }
  
  async update(id, updates) {
    return User.findByIdAndUpdate(id, updates, {
      new: true,
      runValidators: true
    });
  }
  
  async delete(id) {
    return User.findByIdAndDelete(id);
  }
  
  async findWithPagination({ page = 1, limit = 10, sort = '-createdAt' }) {
    const skip = (page - 1) * limit;
    const [users, total] = await Promise.all([
      User.find().sort(sort).limit(limit).skip(skip),
      User.countDocuments()
    ]);
    
    return {
      users,
      pagination: {
        page,
        limit,
        total,
        pages: Math.ceil(total / limit)
      }
    };
  }
}

module.exports = new UserRepository();
```

### Transaction Pattern
```javascript
// MongoDB transactions
const session = await mongoose.startSession();
session.startTransaction();

try {
  const order = await Order.create([orderData], { session });
  await Product.updateMany(
    { _id: { $in: productIds } },
    { $inc: { stock: -1 } },
    { session }
  );
  
  await session.commitTransaction();
  return order;
} catch (error) {
  await session.abortTransaction();
  throw error;
} finally {
  session.endSession();
}
```

## 4. State Management Patterns

### React Context Pattern
```javascript
// AuthContext.jsx
const AuthContext = createContext(null);

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);
  
  useEffect(() => {
    const token = localStorage.getItem('token');
    if (token) {
      fetchUser(token).then(setUser).finally(() => setLoading(false));
    } else {
      setLoading(false);
    }
  }, []);
  
  const login = async (credentials) => {
    const { user, token } = await authService.login(credentials);
    localStorage.setItem('token', token);
    setUser(user);
    return user;
  };
  
  const logout = () => {
    localStorage.removeItem('token');
    setUser(null);
  };
  
  return (
    <AuthContext.Provider value={{ user, login, logout, loading }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within AuthProvider');
  }
  return context;
};
```

### Redux Toolkit Pattern
```javascript
// userSlice.js
import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';

export const fetchUsers = createAsyncThunk(
  'users/fetchUsers',
  async ({ page, limit }) => {
    const response = await api.get('/users', { params: { page, limit } });
    return response.data;
  }
);

const userSlice = createSlice({
  name: 'users',
  initialState: {
    items: [],
    status: 'idle',
    error: null,
    pagination: null
  },
  reducers: {
    userAdded: (state, action) => {
      state.items.push(action.payload);
    },
    userUpdated: (state, action) => {
      const index = state.items.findIndex(u => u.id === action.payload.id);
      if (index !== -1) {
        state.items[index] = action.payload;
      }
    }
  },
  extraReducers: (builder) => {
    builder
      .addCase(fetchUsers.pending, (state) => {
        state.status = 'loading';
      })
      .addCase(fetchUsers.fulfilled, (state, action) => {
        state.status = 'succeeded';
        state.items = action.payload.users;
        state.pagination = action.payload.pagination;
      })
      .addCase(fetchUsers.rejected, (state, action) => {
        state.status = 'failed';
        state.error = action.error.message;
      });
  }
});

export const { userAdded, userUpdated } = userSlice.actions;
export default userSlice.reducer;
```

## 5. Testing Patterns

### Test Utilities
```javascript
// test-utils.js
export const createMockUser = (overrides = {}) => ({
  id: faker.datatype.uuid(),
  email: faker.internet.email(),
  name: faker.name.fullName(),
  role: 'user',
  createdAt: new Date(),
  ...overrides
});

export const setupTestDb = () => {
  beforeAll(async () => {
    await mongoose.connect(process.env.TEST_DATABASE_URL);
  });
  
  beforeEach(async () => {
    await Promise.all(
      Object.values(mongoose.models).map(model => model.deleteMany())
    );
  });
  
  afterAll(async () => {
    await mongoose.connection.close();
  });
};

export const createAuthenticatedRequest = (user) => {
  const token = jwt.sign({ id: user.id }, process.env.JWT_SECRET);
  return request(app).set('Authorization', `Bearer ${token}`);
};
```

### Integration Test Pattern
```javascript
describe('User API', () => {
  setupTestDb();
  
  describe('POST /users', () => {
    it('should create a new user', async () => {
      const userData = {
        email: 'test@example.com',
        password: 'password123',
        name: 'Test User'
      };
      
      const response = await request(app)
        .post('/users')
        .send(userData)
        .expect(201);
      
      expect(response.body).toMatchObject({
        id: expect.any(String),
        email: userData.email,
        name: userData.name
      });
      expect(response.body.password).toBeUndefined();
      
      const user = await User.findById(response.body.id);
      expect(user).toBeTruthy();
    });
  });
});
```

## 6. Performance Patterns

### Caching Pattern
```javascript
// Redis caching
const redis = require('redis');
const client = redis.createClient();

const cache = {
  async get(key) {
    const value = await client.get(key);
    return value ? JSON.parse(value) : null;
  },
  
  async set(key, value, ttl = 3600) {
    await client.setex(key, ttl, JSON.stringify(value));
  },
  
  async invalidate(pattern) {
    const keys = await client.keys(pattern);
    if (keys.length) {
      await client.del(keys);
    }
  }
};

// Cache middleware
const cacheMiddleware = (keyFn, ttl = 3600) => {
  return async (req, res, next) => {
    const key = keyFn(req);
    const cached = await cache.get(key);
    
    if (cached) {
      return res.json(cached);
    }
    
    // Store original json method
    const originalJson = res.json;
    res.json = function(data) {
      cache.set(key, data, ttl);
      return originalJson.call(this, data);
    };
    
    next();
  };
};

// Usage
router.get(
  '/users',
  cacheMiddleware(req => `users:${req.query.page || 1}`),
  getUsers
);
```

### Batch Processing Pattern
```javascript
// Process large datasets in batches
async function processBatch(items, batchSize = 100) {
  const results = [];
  
  for (let i = 0; i < items.length; i += batchSize) {
    const batch = items.slice(i, i + batchSize);
    const batchResults = await Promise.all(
      batch.map(item => processItem(item))
    );
    results.push(...batchResults);
    
    // Optional: Add delay to prevent overwhelming the system
    if (i + batchSize < items.length) {
      await new Promise(resolve => setTimeout(resolve, 100));
    }
  }
  
  return results;
}
```

## 7. Security Patterns

### Input Validation
```javascript
// Using Joi
const Joi = require('joi');

const schemas = {
  createUser: Joi.object({
    email: Joi.string().email().required(),
    password: Joi.string().min(8).required(),
    name: Joi.string().min(2).max(50).required(),
    role: Joi.string().valid('user', 'admin').default('user')
  }),
  
  updateUser: Joi.object({
    email: Joi.string().email(),
    name: Joi.string().min(2).max(50),
    role: Joi.string().valid('user', 'admin')
  }).min(1)
};

const validate = (schema) => {
  return (req, res, next) => {
    const { error, value } = schema.validate(req.body);
    if (error) {
      return res.status(400).json({
        error: error.details[0].message
      });
    }
    req.body = value;
    next();
  };
};

// Usage
router.post('/users', validate(schemas.createUser), createUser);
```

### Rate Limiting
```javascript
const rateLimit = require('express-rate-limit');

const createRateLimiter = (options) => {
  return rateLimit({
    windowMs: 15 * 60 * 1000, // 15 minutes
    max: 100, // limit each IP to 100 requests per windowMs
    message: 'Too many requests, please try again later.',
    standardHeaders: true,
    legacyHeaders: false,
    ...options
  });
};

// Different limits for different endpoints
const authLimiter = createRateLimiter({ max: 5 });
const apiLimiter = createRateLimiter({ max: 100 });

app.use('/auth', authLimiter);
app.use('/api', apiLimiter);
```