require('dotenv').config();
const express = require('express');
const cors = require('cors');
const path = require('path');
const rateLimit = require('express-rate-limit');
const helmet = require('helmet');
const crypto = require('crypto');
const mailchimp = require('@mailchimp/mailchimp_marketing');
const Database = require('./database');

mailchimp.setConfig({
    apiKey: process.env.MAILCHIMP_API_KEY,
    server: process.env.MAILCHIMP_SERVER_PREFIX
});

const app = express();
const PORT = process.env.PORT || 3000;
const db = new Database();

const limiter = rateLimit({
    windowMs: 15 * 60 * 1000,
    max: 100,
    message: 'Too many requests, please try again later.'
});

const strictLimiter = rateLimit({
    windowMs: 15 * 60 * 1000,
    max: 10,
    message: 'Too many submissions, please try again later.'
});

function sanitizeInput(input) {
    if (typeof input !== 'string') return input;
    return input
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;')
        .replace(/"/g, '&quot;')
        .replace(/'/g, '&#x27;')
        .replace(/\//g, '&#x2F;')
        .replace(/javascript:/gi, '')
        .replace(/on\w+=/gi, '')
        .replace(/<script/gi, '')
        .replace(/<iframe/gi, '')
        .replace(/<object/gi, '')
        .replace(/<embed/gi, '');
}

function sanitizeObject(obj) {
    const sanitized = {};
    for (const key in obj) {
        if (typeof obj[key] === 'string') {
            sanitized[key] = sanitizeInput(obj[key]);
        } else if (typeof obj[key] === 'object' && obj[key] !== null) {
            sanitized[key] = sanitizeObject(obj[key]);
        } else {
            sanitized[key] = obj[key];
        }
    }
    return sanitized;
}

function validateEmail(email) {
    const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return re.test(email);
}

function validateInput(data, required = []) {
    for (const field of required) {
        if (!data[field] || data[field].trim() === '') {
            return { valid: false, message: `${field} is required` };
        }
    }
    if (data.email && !validateEmail(data.email)) {
        return { valid: false, message: 'Invalid email format' };
    }
    return { valid: true };
}

const ADMIN_USER = process.env.ADMIN_USER || 'admin';
const ADMIN_PASS = process.env.ADMIN_PASS || 'admin123';

let adminProfile = {
    username: ADMIN_USER,
    password: ADMIN_PASS,
    fullName: 'John Ngor Deng Garang',
    email: 'dengjohn200@gmail.com',
    phone: '+256 768 741 070'
};

function authenticateToken(req, res, next) {
    const authHeader = req.headers['authorization'];
    const token = authHeader && authHeader.split(' ')[1];
    
    if (!token) {
        return res.status(401).json({ error: 'Access denied. No token provided.' });
    }
    
    if (!token.startsWith('admin-token-')) {
        return res.status(403).json({ error: 'Invalid token' });
    }
    
    const timestamp = parseInt(token.replace('admin-token-', ''));
    const tokenAge = Date.now() - timestamp;
    const maxAge = 24 * 60 * 60 * 1000;
    
    if (tokenAge > maxAge) {
        return res.status(403).json({ error: 'Token expired' });
    }
    
    next();
}

app.use(helmet({
    contentSecurityPolicy: {
        directives: {
            defaultSrc: ["'self'"],
            scriptSrc: ["'self'", "'unsafe-inline'", "'unsafe-eval'", "https://cdnjs.cloudflare.com"],
            scriptSrcAttr: ["'unsafe-inline'"],
            styleSrc: ["'self'", "'unsafe-inline'", "https://cdnjs.cloudflare.com", "https://fonts.googleapis.com"],
            fontSrc: ["'self'", "https://cdnjs.cloudflare.com", "https://fonts.gstatic.com"],
            imgSrc: ["'self'", "data:", "https:"],
            connectSrc: ["'self'", "https://portfolio-backend-1-53hz.onrender.com"],
            frameSrc: ["'none'"],
            objectSrc: ["'none'"],
        }
    },
    xssFilter: true,
    noSniff: true,
    referrerPolicy: { policy: 'strict-origin-when-cross-origin' }
}));

const allowedOrigins = [
    'http://localhost:3000',
    'http://127.0.0.1:3000',
    'https://portfolio-backend-1-53hz.onrender.com'
];

app.use(cors({
    origin: function(origin, callback) {
        if (!origin || allowedOrigins.includes(origin)) {
            callback(null, true);
        } else {
            callback(new Error('Not allowed by CORS'));
        }
    },
    credentials: true,
    methods: ['GET', 'POST', 'PUT', 'PATCH', 'DELETE'],
    allowedHeaders: ['Content-Type', 'Authorization', 'X-CSRF-Token']
}));
app.use(express.json({ limit: '10mb' }));
app.use(express.static(__dirname));

const csrfTokens = new Map();

function generateCSRFToken() {
    return crypto.randomBytes(32).toString('hex');
}

function validateCSRFToken(req, res, next) {
    const token = req.headers['x-csrf-token'];
    const authHeader = req.headers['authorization'];
    const userToken = authHeader && authHeader.split(' ')[1];
    
    if (!token || !userToken) {
        return res.status(403).json({ error: 'CSRF token required' });
    }
    
    const storedToken = csrfTokens.get(userToken);
    if (!storedToken || storedToken !== token) {
        return res.status(403).json({ error: 'Invalid CSRF token' });
    }
    
    next();
}

// Login Route
app.post('/api/login', (req, res) => {
    const { username, password } = req.body;
    if (username === adminProfile.username && password === adminProfile.password) {
        const token = 'admin-token-' + Date.now();
        const csrfToken = generateCSRFToken();
        csrfTokens.set(token, csrfToken);
        res.json({ token, csrfToken });
    } else {
        res.status(401).json({ error: 'Invalid credentials' });
    }
});

// Profile Routes
app.get('/api/profile', authenticateToken, (req, res) => {
    res.json({
        fullName: adminProfile.fullName,
        email: adminProfile.email,
        phone: adminProfile.phone,
        username: adminProfile.username
    });
});

app.post('/api/profile', authenticateToken, validateCSRFToken, (req, res) => {
    const { fullName, email, phone, username, password } = req.body;
    if (fullName) adminProfile.fullName = fullName;
    if (email) adminProfile.email = email;
    if (phone) adminProfile.phone = phone;
    if (username) adminProfile.username = username;
    if (password) adminProfile.password = password;
    res.json({ success: true });
});

// Messages API
app.get('/api/messages', authenticateToken, (req, res) => {
    db.getMessages((err, messages) => {
        if (err) {
            res.status(500).json({ error: 'Database error' });
        } else {
            res.json(messages || []);
        }
    });
});

app.post('/api/messages', (req, res) => {
    const validation = validateInput(req.body, ['name', 'email', 'message']);
    if (!validation.valid) {
        return res.status(400).json({ error: validation.message });
    }
    
    const sanitizedBody = sanitizeObject(req.body);
    const message = {
        ...sanitizedBody,
        date: new Date().toISOString().split('T')[0],
        status: 'new'
    };
    
    db.addMessage(message, (err, result) => {
        if (err) {
            res.status(500).json({ error: 'Database error' });
        } else {
            db.incrementAnalytics('contactForms', () => {});
            res.json(result);
        }
    });
});

app.delete('/api/messages/:id', authenticateToken, validateCSRFToken, (req, res) => {
    db.deleteMessage(parseInt(req.params.id), (err) => {
        if (err) {
            res.status(500).json({ error: 'Database error' });
        } else {
            res.json({ success: true });
        }
    });
});

app.patch('/api/messages/:id', authenticateToken, validateCSRFToken, (req, res) => {
    db.updateMessage(parseInt(req.params.id), req.body, (err) => {
        if (err) {
            res.status(500).json({ error: 'Database error' });
        } else {
            res.json({ success: true });
        }
    });
});

// Analytics API
app.get('/api/analytics', authenticateToken, (req, res) => {
    db.getAnalytics((err, analytics) => {
        if (err) {
            res.status(500).json({ error: 'Database error' });
        } else {
            res.json(analytics || { visitors: 0, pageViews: 0, contactForms: 0, subscribers: 0 });
        }
    });
});

app.patch('/api/analytics', authenticateToken, validateCSRFToken, (req, res) => {
    db.updateAnalytics(req.body, (err) => {
        if (err) {
            res.status(500).json({ error: 'Database error' });
        } else {
            res.json({ success: true });
        }
    });
});

// Blog Posts API
app.get('/api/blog-posts', authenticateToken, (req, res) => {
    db.getBlogPosts((err, posts) => {
        if (err) {
            res.status(500).json({ error: 'Database error' });
        } else {
            res.json(posts || []);
        }
    });
});

app.post('/api/blog-posts', authenticateToken, validateCSRFToken, (req, res) => {
    const post = {
        ...req.body,
        date: new Date().toISOString().split('T')[0]
    };
    
    db.addBlogPost(post, (err, result) => {
        if (err) {
            res.status(500).json({ error: 'Database error' });
        } else {
            res.json(result);
        }
    });
});

app.delete('/api/blog-posts/:id', authenticateToken, validateCSRFToken, (req, res) => {
    db.deleteBlogPost(parseInt(req.params.id), (err) => {
        if (err) {
            res.status(500).json({ error: 'Database error' });
        } else {
            res.json({ success: true });
        }
    });
});

// Projects API
app.get('/api/projects', authenticateToken, (req, res) => {
    db.getProjects((err, projects) => {
        if (err) {
            res.status(500).json({ error: 'Database error' });
        } else {
            res.json(projects || []);
        }
    });
});

app.post('/api/projects', authenticateToken, validateCSRFToken, (req, res) => {
    const project = {
        ...req.body,
        date: new Date().toISOString().split('T')[0]
    };
    
    db.addProject(project, (err, result) => {
        if (err) {
            res.status(500).json({ error: 'Database error' });
        } else {
            res.json(result);
        }
    });
});

app.delete('/api/projects/:id', authenticateToken, validateCSRFToken, (req, res) => {
    db.deleteProject(parseInt(req.params.id), (err) => {
        if (err) {
            res.status(500).json({ error: 'Database error' });
        } else {
            res.json({ success: true });
        }
    });
});

// Articles API
app.get('/api/articles', authenticateToken, (req, res) => {
    db.getArticles((err, articles) => {
        if (err) {
            res.status(500).json({ error: 'Database error' });
        } else {
            res.json(articles || []);
        }
    });
});

app.post('/api/articles', authenticateToken, validateCSRFToken, (req, res) => {
    const sanitizedBody = sanitizeObject(req.body);
    const article = {
        ...sanitizedBody,
        date: new Date().toISOString().split('T')[0],
        slug: sanitizedBody.title.toLowerCase().replace(/[^a-z0-9]+/g, '-')
    };
    
    db.addArticle(article, (err, result) => {
        if (err) {
            res.status(500).json({ error: 'Database error' });
        } else {
            res.json(result);
        }
    });
});

app.put('/api/articles/:id', authenticateToken, validateCSRFToken, (req, res) => {
    const sanitizedBody = sanitizeObject(req.body);
    const article = {
        ...sanitizedBody,
        slug: sanitizedBody.title.toLowerCase().replace(/[^a-z0-9]+/g, '-')
    };
    
    db.updateArticle(parseInt(req.params.id), article, (err) => {
        if (err) {
            res.status(500).json({ error: 'Database error' });
        } else {
            res.json({ success: true });
        }
    });
});

app.delete('/api/articles/:id', authenticateToken, validateCSRFToken, (req, res) => {
    db.deleteArticle(parseInt(req.params.id), (err) => {
        if (err) {
            res.status(500).json({ error: 'Database error' });
        } else {
            res.json({ success: true });
        }
    });
});

app.get('/api/articles/:id', (req, res) => {
    db.getArticleById(parseInt(req.params.id), (err, article) => {
        if (err) {
            res.status(500).json({ error: 'Database error' });
        } else if (!article) {
            res.status(404).json({ error: 'Article not found' });
        } else {
            res.json(article);
        }
    });
});

// Subscribers API
app.get('/api/subscribers', authenticateToken, (req, res) => {
    db.getSubscribers((err, subscribers) => {
        if (err) {
            res.status(500).json({ error: 'Database error' });
        } else {
            res.json(subscribers || []);
        }
    });
});

app.post('/api/subscribers', (req, res) => {
    const validation = validateInput(req.body, ['email']);
    if (!validation.valid) {
        return res.status(400).json({ error: validation.message });
    }
    
    const sanitizedBody = sanitizeObject(req.body);
    const subscriber = {
        email: sanitizedBody.email,
        firstName: sanitizedBody.firstName || '',
        lastName: sanitizedBody.lastName || '',
        date: new Date().toISOString().split('T')[0]
    };
    
    db.addSubscriber(subscriber, (err, result) => {
        if (err) {
            if (err.message.includes('UNIQUE constraint failed')) {
                res.status(400).json({ error: 'Email already subscribed' });
            } else {
                res.status(500).json({ error: 'Database error' });
            }
        } else {
            // Try to add to Mailchimp
            if (process.env.MAILCHIMP_API_KEY && process.env.MAILCHIMP_AUDIENCE_ID) {
                mailchimp.lists.addListMember(process.env.MAILCHIMP_AUDIENCE_ID, {
                    email_address: subscriber.email,
                    status: 'subscribed',
                    merge_fields: {
                        FNAME: subscriber.firstName,
                        LNAME: subscriber.lastName
                    }
                }).catch(error => {
                    console.log('Mailchimp error:', error.message);
                });
            }
            
            db.incrementAnalytics('subscribers', () => {});
            res.json(result);
        }
    });
});

app.delete('/api/subscribers/:id', authenticateToken, validateCSRFToken, (req, res) => {
    db.deleteSubscriber(parseInt(req.params.id), (err) => {
        if (err) {
            res.status(500).json({ error: 'Database error' });
        } else {
            res.json({ success: true });
        }
    });
});

// Analytics tracking
app.post('/api/analytics/track', (req, res) => {
    const event = {
        ...req.body,
        ip: req.ip || req.connection.remoteAddress
    };
    
    db.addEvent(event, (err) => {
        if (err) {
            console.error('Error tracking event:', err);
        }
    });
    
    if (event.eventType === 'page_view') {
        db.incrementAnalytics('pageViews', () => {});
    }
    
    res.json({ success: true });
});

app.get('/api/analytics/dashboard', authenticateToken, (req, res) => {
    db.getAnalytics((err, analytics) => {
        if (err) {
            res.status(500).json({ error: 'Database error' });
        } else {
            db.getRecentEvents(50, (err, events) => {
                const dashboardData = {
                    totalVisitors: analytics?.visitors || 0,
                    totalPageViews: analytics?.pageViews || 0,
                    totalContactForms: analytics?.contactForms || 0,
                    totalSubscribers: analytics?.subscribers || 0,
                    recentEvents: events || []
                };
                res.json(dashboardData);
            });
        }
    });
});

// Graceful shutdown
process.on('SIGINT', () => {
    console.log('Shutting down server...');
    db.close();
    process.exit(0);
});

process.on('SIGTERM', () => {
    console.log('Shutting down server...');
    db.close();
    process.exit(0);
});

app.listen(PORT, () => {
    console.log(`Server running at https://portfolio-backend-1-53hz.onrender.com:${PORT}`);
    console.log('Using SQLite database for persistent storage');
});
