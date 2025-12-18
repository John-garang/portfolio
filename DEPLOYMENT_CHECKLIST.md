# Pre-Deployment Security Checklist

## ⚠️ CRITICAL - Must Complete Before Publishing

### 1. Switch to Secure Version
```bash
ren app.py app_insecure_backup.py
ren app_secure.py app.py
```

### 2. Set Environment Variables
Create `.env` file (copy from `.env.example`):
```bash
copy .env.example .env
```

Edit `.env` and change:
- `ADMIN_PASSWORD` - Use strong password (min 12 chars, mixed case, numbers, symbols)
- `ALLOWED_ORIGINS` - Set to your domain (e.g., https://yourdomain.com)

### 3. Install python-dotenv
```bash
pip install python-dotenv
```

### 4. Update app.py to Load .env
Add at top of app.py:
```python
from dotenv import load_dotenv
load_dotenv()
```

### 5. Enable HTTPS
- Get SSL certificate (Let's Encrypt, Cloudflare, etc.)
- Configure your hosting to use HTTPS
- Redirect all HTTP to HTTPS

### 6. Update CORS
After deployment, update `.env`:
```
ALLOWED_ORIGINS=https://yourdomain.com
```

### 7. Secure MySQL
```sql
-- Change root password
ALTER USER 'root'@'localhost' IDENTIFIED BY 'NewStrongPassword123!';

-- Create dedicated user for app
CREATE USER 'portfolio_user'@'localhost' IDENTIFIED BY 'AnotherStrongPassword123!';
GRANT SELECT, INSERT, UPDATE, DELETE ON portfolio_db.* TO 'portfolio_user'@'localhost';
FLUSH PRIVILEGES;
```

Update `.env`:
```
DB_USER=portfolio_user
DB_PASSWORD=AnotherStrongPassword123!
```

### 8. Add Rate Limiting (Optional but Recommended)
```bash
pip install Flask-Limiter
```

### 9. Hide Sensitive Files
Create `.gitignore`:
```
.env
*.pyc
__pycache__/
database.json
database.json.backup
*.log
```

### 10. Test Everything
- [ ] Login works with new password
- [ ] Admin dashboard loads
- [ ] Can create/edit/delete articles
- [ ] Public pages work without auth
- [ ] Comments work
- [ ] Contact form works

## Current Status
- ✅ MySQL database configured
- ✅ Input sanitization enabled
- ✅ SQL injection protection
- ❌ Authentication not enabled (using insecure version)
- ❌ Weak admin password
- ❌ Database password in code
- ❌ CORS wide open
- ❌ No HTTPS

## After Completing Checklist
- ✅ All routes protected
- ✅ Strong passwords
- ✅ Environment variables
- ✅ CORS restricted
- ✅ HTTPS enabled
- ✅ Ready for production
