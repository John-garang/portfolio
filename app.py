from flask import Flask, request, jsonify
from flask_cors import CORS
import psycopg2
import psycopg2.extras
import os
import re
from datetime import datetime
from functools import wraps
import secrets
from dotenv import load_dotenv
import urllib.parse

load_dotenv()

app = Flask(__name__)

# CORS for frontend
ALLOWED_ORIGINS = os.getenv('ALLOWED_ORIGINS', 'https://johngarang.com,http://localhost:3000').split(',')
CORS(app, 
     origins=['*'],  # Temporarily allow all origins
     methods=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"],
     allow_headers=["Content-Type", "Authorization"],
     supports_credentials=False)

# Database config for PostgreSQL
DATABASE_URL = os.getenv('DATABASE_URL')
if DATABASE_URL:
    parsed = urllib.parse.urlparse(DATABASE_URL)
    DB_CONFIG = {
        'host': parsed.hostname,
        'user': parsed.username,
        'password': parsed.password,
        'database': parsed.path[1:],
        'port': parsed.port or 5432
    }
else:
    DB_CONFIG = {
        'host': os.getenv('DB_HOST', 'localhost'),
        'user': os.getenv('DB_USER', 'postgres'),
        'password': os.getenv('DB_PASSWORD'),
        'database': os.getenv('DB_NAME', 'portfolio_db'),
        'port': 5432
    }

# Secure admin credentials
ADMIN_USERNAME = os.getenv('ADMIN_USERNAME', 'dengjohn200@gmail.com')
ADMIN_PASSWORD = os.getenv('ADMIN_PASSWORD', 'John@Alustudent1')

# Simple token validation
import hashlib
import time

def generate_token(username):
    timestamp = str(int(time.time()))
    token_data = f"{username}:{timestamp}:{os.getenv('SECRET_KEY', 'default-secret')}"
    return hashlib.sha256(token_data.encode()).hexdigest()

def validate_token(token, username):
    if not token or not username:
        return False
    return len(token) == 64 and all(c in '0123456789abcdef' for c in token.lower())

def get_db():
    return psycopg2.connect(**DB_CONFIG)

def init_db():
    try:
        conn = get_db()
        cursor = conn.cursor()
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS articles (
                id SERIAL PRIMARY KEY,
                title VARCHAR(255),
                category VARCHAR(100),
                excerpt TEXT,
                content TEXT,
                image VARCHAR(255),
                slug VARCHAR(255),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS poems (
                id SERIAL PRIMARY KEY,
                title VARCHAR(255),
                excerpt TEXT,
                content TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS comments (
                id SERIAL PRIMARY KEY,
                poemId INTEGER,
                name VARCHAR(255),
                text TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS messages (
                id SERIAL PRIMARY KEY,
                name VARCHAR(255),
                email VARCHAR(255),
                phone VARCHAR(50),
                company VARCHAR(255),
                service VARCHAR(255),
                budget VARCHAR(100),
                timeline VARCHAR(100),
                message TEXT,
                status VARCHAR(50),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS subscribers (
                id SERIAL PRIMARY KEY,
                email VARCHAR(255) UNIQUE,
                firstName VARCHAR(255),
                lastName VARCHAR(255),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        conn.commit()
        cursor.close()
        conn.close()
        print("Database tables initialized")
    except Exception as e:
        print(f"Database initialization error: {e}")

def sanitize_input(text):
    if not isinstance(text, str):
        return text
    return text.replace('<', '&lt;').replace('>', '&gt;').replace('"', '&quot;').replace("'", '&#x27;').replace('/', '&#x2F;')

def sanitize_object(obj):
    if isinstance(obj, dict):
        return {k: sanitize_object(v) for k, v in obj.items()}
    elif isinstance(obj, str):
        return sanitize_input(obj)
    return obj

def validate_email(email):
    return re.match(r'^[^\s@]+@[^\s@]+\.[^\s@]+$', email) is not None

def require_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token or not token.startswith('Bearer '):
            return jsonify({'error': 'Unauthorized'}), 401
        token = token.replace('Bearer ', '')
        if not validate_token(token, ADMIN_USERNAME):
            return jsonify({'error': 'Invalid token'}), 401
        return f(*args, **kwargs)
    return decorated



@app.route('/')
def index():
    return jsonify({'message': 'Portfolio Backend API', 'status': 'running'})

@app.route('/api/login', methods=['POST'])
def login():
    data = request.json
    if data.get('username') == ADMIN_USERNAME and data.get('password') == ADMIN_PASSWORD:
        token = generate_token(ADMIN_USERNAME)
        return jsonify({'token': token})
    return jsonify({'error': 'Invalid credentials'}), 401

@app.route('/api/articles', methods=['GET'])
def get_articles():
    try:
        conn = get_db()
        cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        cursor.execute("SELECT id, title, category, excerpt, content, image, slug, created_at as date FROM articles ORDER BY created_at DESC")
        articles = cursor.fetchall()
        cursor.close()
        conn.close()
        return jsonify([dict(article) for article in articles])
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/analytics/track', methods=['POST'])
def track_analytics():
    return jsonify({'success': True})

@app.route('/api/subscribers', methods=['GET'])
@require_auth
def get_subscribers():
    try:
        conn = get_db()
        cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        cursor.execute("SELECT * FROM subscribers ORDER BY created_at DESC")
        subscribers = cursor.fetchall()
        cursor.close()
        conn.close()
        return jsonify([dict(sub) for sub in subscribers])
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/analytics/dashboard', methods=['GET'])
@require_auth
def get_analytics_dashboard():
    try:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM messages")
        total_messages = cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(*) FROM subscribers")
        total_subscribers = cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(*) FROM articles")
        total_articles = cursor.fetchone()[0]
        cursor.close()
        conn.close()
        return jsonify({
            'totalVisitors': 0,
            'totalPageViews': 0,
            'todayVisitors': 0,
            'topPages': [],
            'recentEvents': []
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/messages', methods=['GET'])
@require_auth
def get_messages():
    try:
        conn = get_db()
        cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        cursor.execute("SELECT *, created_at as date FROM messages ORDER BY created_at DESC")
        messages = cursor.fetchall()
        cursor.close()
        conn.close()
        return jsonify([dict(msg) for msg in messages])
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/profile', methods=['GET', 'POST'])
@require_auth
def handle_profile():
    if request.method == 'GET':
        return jsonify({
            'fullName': 'John Garang',
            'email': ADMIN_USERNAME,
            'phone': '',
            'username': ADMIN_USERNAME
        })
    elif request.method == 'POST':
        return jsonify({'success': True})

# Initialize database on startup
init_db()

if __name__ == '__main__':
    port = int(os.getenv('PORT', 3000))
    print(f'Portfolio Backend API Starting on port {port}')
    app.run(port=port, debug=False, host='0.0.0.0')