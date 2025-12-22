from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from functools import wraps
import os
from dotenv import load_dotenv
import hashlib
import time
import psycopg2
import psycopg2.extras
import urllib.parse

load_dotenv()

app = Flask(__name__, static_folder='static', static_url_path='/static')

# -----------------------------
# CORS Configuration
# -----------------------------
ALLOWED_ORIGINS = [
    'https://johngarang.com',
    'http://localhost:3000',
    '*'  # Allow all origins for testing
]

CORS(app, origins=ALLOWED_ORIGINS,
     methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
     allow_headers=["Content-Type", "Authorization"],
     supports_credentials=True)

@app.before_request
def handle_options():
    """Handle OPTIONS preflight requests"""
    if request.method == 'OPTIONS':
        response = app.make_default_options_response()
        response.headers['Access-Control-Allow-Origin'] = request.headers.get('Origin', '*')
        response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
        response.headers['Access-Control-Allow-Methods'] = 'GET,POST,PUT,PATCH,DELETE,OPTIONS'
        return response

# -----------------------------
# Admin Authentication
# -----------------------------
ADMIN_USERNAME = os.getenv('ADMIN_USERNAME', 'dengjohn200@gmail.com')
ADMIN_PASSWORD = os.getenv('ADMIN_PASSWORD', 'John@Alustudent1')
SECRET_KEY = os.getenv('SECRET_KEY', 'default-secret')

def generate_token(username):
    timestamp = str(int(time.time()))
    token_data = f"{username}:{timestamp}:{SECRET_KEY}"
    return hashlib.sha256(token_data.encode()).hexdigest()

def validate_token(token, username):
    if not token or not username:
        return False
    return len(token) == 64 and all(c in '0123456789abcdef' for c in token.lower())

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

# -----------------------------
# PostgreSQL Configuration
# -----------------------------
DATABASE_URL = os.getenv('DATABASE_URL') or \
    "postgresql://postgres:John%40Alustudent1@db.fxigmaaeoqeqjszucosw.supabase.co:5432/postgres"

parsed = urllib.parse.urlparse(DATABASE_URL)
DB_CONFIG = {
    'host': parsed.hostname,
    'user': parsed.username,
    'password': parsed.password,
    'database': parsed.path[1:],
    'port': parsed.port or 5432
}

def get_db():
    return psycopg2.connect(**DB_CONFIG)

# -----------------------------
# Initialize Database Tables
# -----------------------------
def init_db():
    try:
        conn = get_db()
        cursor = conn.cursor()
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
                status VARCHAR(50) DEFAULT 'new',
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
        conn.commit()
        cursor.close()
        conn.close()
        print("Database initialized")
    except Exception as e:
        print(f"DB init error: {e}")

init_db()

# -----------------------------
# Static Files
# -----------------------------
@app.route('/static/<path:filename>')
def serve_static(filename):
    response = send_from_directory('static', filename)
    if filename.endswith('.js'):
        response.headers['Content-Type'] = 'application/javascript'
    elif filename.endswith('.css'):
        response.headers['Content-Type'] = 'text/css'
    return response

@app.route('/load-header.js')
def serve_load_header():
    return send_from_directory('static', 'load-header.js', mimetype='application/javascript')

@app.route('/admin-config.js')
def serve_admin_config():
    return send_from_directory('static', 'admin-config.js', mimetype='application/javascript')

# -----------------------------
# API Endpoints
# -----------------------------
@app.route('/')
def index():
    return send_from_directory('templates', 'index.html')

@app.route('/about')
def about():
    return send_from_directory('templates/about', 'index.html')

@app.route('/api/test', methods=['GET'])
def test():
    return jsonify({'status': 'ok', 'message': 'Backend is working', 'timestamp': time.time()})

@app.route('/api/login', methods=['POST'])
def login():
    data = request.json
    if data.get('username') == ADMIN_USERNAME and data.get('password') == ADMIN_PASSWORD:
        token = generate_token(ADMIN_USERNAME)
        return jsonify({'token': token})
    return jsonify({'error': 'Invalid credentials'}), 401

# -----------------------------
# Messages Endpoints
# -----------------------------
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
        return jsonify(messages)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/messages/<int:message_id>', methods=['PATCH', 'DELETE'])
@require_auth
def modify_message(message_id):
    try:
        conn = get_db()
        cursor = conn.cursor()
        if request.method == 'DELETE':
            cursor.execute("DELETE FROM messages WHERE id=%s", (message_id,))
        elif request.method == 'PATCH':
            status = request.json.get('status', 'new')
            cursor.execute("UPDATE messages SET status=%s WHERE id=%s", (status, message_id))
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# -----------------------------
# Subscribers Endpoints
# -----------------------------
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
        return jsonify(subscribers)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/subscribers/<int:subscriber_id>', methods=['DELETE'])
@require_auth
def delete_subscriber(subscriber_id):
    try:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM subscribers WHERE id=%s", (subscriber_id,))
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# -----------------------------
# Articles Endpoints
# -----------------------------
@app.route('/api/articles', methods=['GET'])
def get_articles_public():
    try:
        conn = get_db()
        cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        cursor.execute("SELECT id, title, category, excerpt, created_at::date as date FROM articles ORDER BY created_at DESC")
        articles = cursor.fetchall()
        cursor.close()
        conn.close()
        return jsonify(articles)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/admin/articles', methods=['GET', 'POST'])
@require_auth
def get_articles_admin():
    try:
        conn = get_db()
        cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        if request.method == 'POST':
            data = request.json
            cursor.execute("INSERT INTO articles (title, category, excerpt, content) VALUES (%s,%s,%s,%s) RETURNING *",
                           (data['title'], data['category'], data['excerpt'], data['content']))
            article = cursor.fetchone()
            conn.commit()
            cursor.close()
            conn.close()
            return jsonify(article), 201
        else:
            cursor.execute("SELECT * FROM articles ORDER BY created_at DESC")
            articles = cursor.fetchall()
            cursor.close()
            conn.close()
            return jsonify(articles)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/articles/<int:article_id>', methods=['GET'])
def get_article_public(article_id):
    try:
        conn = get_db()
        cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        cursor.execute("SELECT * FROM articles WHERE id=%s", (article_id,))
        article = cursor.fetchone()
        cursor.close()
        conn.close()
        if article:
            return jsonify(article)
        return jsonify({'error': 'Article not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/admin/articles/<int:article_id>', methods=['PUT', 'DELETE'])
@require_auth
def modify_article(article_id):
    try:
        conn = get_db()
        cursor = conn.cursor()
        if request.method == 'DELETE':
            cursor.execute("DELETE FROM articles WHERE id=%s", (article_id,))
        elif request.method == 'PUT':
            data = request.json
            cursor.execute("""
                UPDATE articles SET title=%s, category=%s, excerpt=%s, content=%s WHERE id=%s
            """, (data.get('title'), data.get('category'), data.get('excerpt'), data.get('content'), article_id))
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# -----------------------------
# Poems Endpoints
# -----------------------------
@app.route('/api/poems', methods=['GET'])
def get_poems_public():
    try:
        conn = get_db()
        cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        cursor.execute("SELECT id, title, excerpt, created_at::date as date FROM poems ORDER BY created_at DESC")
        poems = cursor.fetchall()
        cursor.close()
        conn.close()
        return jsonify(poems)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/poems/<int:poem_id>', methods=['GET'])
def get_poem_public(poem_id):
    try:
        conn = get_db()
        cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        cursor.execute("SELECT * FROM poems WHERE id=%s", (poem_id,))
        poem = cursor.fetchone()
        cursor.close()
        conn.close()
        if poem:
            return jsonify(poem)
        return jsonify({'error': 'Poem not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/admin/poems', methods=['GET', 'POST'])
@require_auth
def poems_admin():
    try:
        conn = get_db()
        cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        if request.method == 'POST':
            data = request.json
            cursor.execute("INSERT INTO poems (title, excerpt, content) VALUES (%s,%s,%s) RETURNING *",
                           (data['title'], data['excerpt'], data['content']))
            poem = cursor.fetchone()
            conn.commit()
            cursor.close()
            conn.close()
            return jsonify(poem), 201
        else:
            cursor.execute("SELECT * FROM poems ORDER BY created_at DESC")
            poems_list = cursor.fetchall()
            cursor.close()
            conn.close()
            return jsonify(poems_list)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/admin/poems/<int:poem_id>', methods=['PUT', 'DELETE'])
@require_auth
def modify_poem_admin(poem_id):
    try:
        conn = get_db()
        cursor = conn.cursor()
        if request.method == 'DELETE':
            cursor.execute("DELETE FROM poems WHERE id=%s", (poem_id,))
        elif request.method == 'PUT':
            data = request.json
            cursor.execute("UPDATE poems SET title=%s, excerpt=%s, content=%s WHERE id=%s",
                           (data.get('title'), data.get('excerpt'), data.get('content'), poem_id))
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# -----------------------------
# Analytics
# -----------------------------
@app.route('/api/analytics/dashboard', methods=['GET'])
@require_auth
def analytics_dashboard():
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
            'totalMessages': total_messages,
            'totalSubscribers': total_subscribers,
            'totalArticles': total_articles,
            'topPages': [],
            'recentEvents': []
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# -----------------------------
# Profile Endpoint
# -----------------------------
@app.route('/api/profile', methods=['GET', 'POST'])
@require_auth
def get_profile():
    if request.method == 'POST':
        return jsonify({'success': True, 'message': 'Profile updated'})
    return jsonify({
        'fullName': 'John Garang',
        'email': ADMIN_USERNAME,
        'phone': '',
        'username': ADMIN_USERNAME
    })

# -----------------------------
# Comments Endpoints
# -----------------------------
@app.route('/api/comments/<int:poem_id>', methods=['GET'])
def get_comments(poem_id):
    try:
        conn = get_db()
        cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        cursor.execute("SELECT * FROM comments WHERE poemId=%s ORDER BY created_at DESC", (poem_id,))
        comments = cursor.fetchall()
        cursor.close()
        conn.close()
        return jsonify(comments)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/comments', methods=['POST'])
def add_comment():
    data = request.json
    try:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO comments (poemId, name, text) VALUES (%s,%s,%s) RETURNING id",
            (data['poemId'], data['name'], data['text'])
        )
        conn.commit()
        new_id = cursor.fetchone()[0]
        cursor.close()
        conn.close()
        return jsonify({'success': True, 'id': new_id})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# -----------------------------
# Run Server
# -----------------------------
if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    print("Starting server with all routes...")
    print(f"Available routes: {len(app.url_map._rules)} routes")
    app.run(host='0.0.0.0', port=port, debug=True)
