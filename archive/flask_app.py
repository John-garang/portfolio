from flask import Flask, render_template, request, jsonify, send_from_directory
from flask_cors import CORS
import os
import json
import sqlite3
from datetime import datetime
import hashlib
import time
from functools import wraps

app = Flask(__name__)
CORS(app)

# Configuration
DATABASE = '/home/yourusername/mysite/portfolio.db'
ADMIN_USERNAME = 'dengjohn200@gmail.com'
ADMIN_PASSWORD = 'John@Alustudent1'

def init_db():
    """Initialize SQLite database"""
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    # Create tables
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS articles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            category TEXT NOT NULL,
            excerpt TEXT NOT NULL,
            content TEXT NOT NULL,
            image TEXT,
            slug TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS poems (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            excerpt TEXT NOT NULL,
            content TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            phone TEXT,
            company TEXT,
            service TEXT,
            budget TEXT,
            timeline TEXT,
            message TEXT NOT NULL,
            status TEXT DEFAULT 'new',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS subscribers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE NOT NULL,
            firstName TEXT,
            lastName TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    conn.commit()
    conn.close()

def validate_token(token):
    """Simple token validation"""
    return len(token) == 64 and all(c in '0123456789abcdef' for c in token.lower())

def require_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token or not token.startswith('Bearer '):
            return jsonify({'error': 'Unauthorized'}), 401
        token = token.replace('Bearer ', '')
        if not validate_token(token):
            return jsonify({'error': 'Invalid token'}), 401
        return f(*args, **kwargs)
    return decorated

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/<path:filename>')
def serve_static(filename):
    if filename.endswith('.html'):
        return render_template(filename)
    return send_from_directory('.', filename)

@app.route('/api/login', methods=['POST'])
def login():
    data = request.json
    if data.get('username') == ADMIN_USERNAME and data.get('password') == ADMIN_PASSWORD:
        token = hashlib.sha256(f"{ADMIN_USERNAME}:{time.time()}".encode()).hexdigest()
        return jsonify({'token': token})
    return jsonify({'error': 'Invalid credentials'}), 401

@app.route('/api/articles', methods=['GET'])
def get_articles():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM articles ORDER BY created_at DESC')
    articles = [dict(zip([col[0] for col in cursor.description], row)) for row in cursor.fetchall()]
    conn.close()
    return jsonify(articles)

@app.route('/api/articles', methods=['POST'])
@require_auth
def create_article():
    data = request.json
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO articles (title, category, excerpt, content, image, slug)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (data['title'], data['category'], data['excerpt'], data['content'],
          data.get('image', ''), data['title'].lower().replace(' ', '-')))
    conn.commit()
    conn.close()
    return jsonify({'success': True})

@app.route('/api/articles/<int:article_id>', methods=['GET'])
def get_article(article_id):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM articles WHERE id = ?', (article_id,))
    article = cursor.fetchone()
    conn.close()
    if article:
        return jsonify(dict(zip([col[0] for col in cursor.description], article)))
    return jsonify({'error': 'Article not found'}), 404

@app.route('/api/messages', methods=['POST'])
def create_message():
    data = request.json
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO messages (name, email, phone, company, service, budget, timeline, message)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (data['name'], data['email'], data.get('phone', ''), data.get('company', ''),
          data.get('service', ''), data.get('budget', ''), data.get('timeline', ''), data['message']))
    conn.commit()
    conn.close()
    return jsonify({'success': True})

@app.route('/api/subscribers', methods=['POST'])
def create_subscriber():
    data = request.json
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    try:
        cursor.execute('''
            INSERT INTO subscribers (email, firstName, lastName)
            VALUES (?, ?, ?)
        ''', (data['email'], data.get('firstName', ''), data.get('lastName', '')))
        conn.commit()
        conn.close()
        return jsonify({'success': True})
    except sqlite3.IntegrityError:
        conn.close()
        return jsonify({'error': 'Email already subscribed'}), 400

# Initialize database on startup
init_db()

if __name__ == '__main__':
    app.run(debug=True)