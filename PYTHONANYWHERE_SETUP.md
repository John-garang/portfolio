# PythonAnywhere Deployment Guide

## 1. Upload Files
1. Go to PythonAnywhere Dashboard
2. Open Files tab
3. Upload all files to `/home/yourusername/mysite/`

## 2. Install Requirements
In PythonAnywhere Bash console:
```bash
pip3.10 install --user Flask==2.3.3 Flask-CORS==4.0.0
```

## 3. Configure Web App
1. Go to Web tab
2. Create new web app
3. Choose Flask
4. Set source code: `/home/yourusername/mysite/flask_app.py`
5. Set working directory: `/home/yourusername/mysite/`

## 4. Update Database Path
Edit flask_app.py line 12:
```python
DATABASE = '/home/yourusername/mysite/portfolio.db'
```
Replace 'yourusername' with your actual PythonAnywhere username.

## 5. Static Files Configuration
In Web tab, add static files mapping:
- URL: `/static/`
- Directory: `/home/yourusername/mysite/static/`

## 6. Reload Web App
Click "Reload" button in Web tab.

Your portfolio will be available at: `https://yourusername.pythonanywhere.com`