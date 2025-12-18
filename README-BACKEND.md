# Portfolio Backend Setup Guide

## 🚀 Quick Start

### 1. Install Node.js
Download and install from: https://nodejs.org/

### 2. Install Dependencies
```bash
cd "c:\John's tech projects\Portfolio"
npm install
```

### 3. Start the Server
```bash
npm start
```

Server will run at: http://localhost:3000

### 4. Access Admin Dashboard
Open in browser: http://localhost:3000/admin-server.html

## 📁 Files Created

- **server.js** - Node.js Express backend server
- **package.json** - Dependencies configuration
- **api-client.js** - Frontend API client
- **admin-server.html** - Server-connected admin dashboard
- **database.json** - JSON file database (auto-created)

## 🔌 API Endpoints

### Messages
- GET `/api/messages` - Get all messages
- POST `/api/messages` - Create new message
- DELETE `/api/messages/:id` - Delete message
- PATCH `/api/messages/:id` - Update message

### Analytics
- GET `/api/analytics` - Get analytics data
- PATCH `/api/analytics` - Update analytics

### Blog Posts
- GET `/api/blog-posts` - Get all blog posts
- POST `/api/blog-posts` - Create blog post
- DELETE `/api/blog-posts/:id` - Delete blog post

### Projects
- GET `/api/projects` - Get all projects
- POST `/api/projects` - Create project
- DELETE `/api/projects/:id` - Delete project

## 🔄 Update Contact Form

Add to contact.html before closing `</body>`:
```html
<script src="api-client.js"></script>
<script>
document.querySelector('.professional-contact-form').addEventListener('submit', async function(e) {
    e.preventDefault();
    const formData = {
        name: this.querySelector('#firstName').value + ' ' + this.querySelector('#lastName').value,
        email: this.querySelector('#email').value,
        subject: this.querySelector('#service').value || 'General Inquiry',
        message: this.querySelector('#message').value
    };
    await API.addMessage(formData);
    alert('Thank you! Your message has been sent successfully.');
    this.reset();
});
</script>
```

## 🌐 Production Deployment

### Option 1: Heroku
```bash
heroku create your-portfolio-backend
git push heroku main
```

### Option 2: Vercel
```bash
vercel deploy
```

### Option 3: Railway
```bash
railway up
```

Update `API_BASE` in api-client.js to your production URL.

## 💾 Database Options

Current: JSON file (simple, no setup)

Upgrade to:
- **MongoDB** - For scalability
- **PostgreSQL** - For relational data
- **Firebase** - For real-time features

## 🔐 Security (Add Later)

- JWT authentication
- Rate limiting
- Input validation
- HTTPS only
- Environment variables

## 📊 Features

✅ REST API with full CRUD operations
✅ Real-time data persistence
✅ Contact form submissions
✅ Analytics tracking
✅ Blog post management
✅ Project management
✅ Email integration (mailto)
