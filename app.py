from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import psycopg2
import psycopg2.extras
import os
import re
from datetime import datetime
from functools import wraps
import secrets
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__, static_folder='.')

# CORS for frontend - Force specific origin
ALLOWED_ORIGINS = ['https://portfolio-cmwe.onrender.com']
CORS(app, origins=ALLOWED_ORIGINS, methods=["GET", "POST", "PUT", "DELETE", "PATCH"], allow_headers=["Content-Type", "Authorization"])

# Secure admin credentials - use environment variables
ADMIN_USERNAME = os.getenv('ADMIN_USERNAME', 'admin')
ADMIN_PASSWORD = os.getenv('ADMIN_PASSWORD')

# Store valid tokens in memory (use Redis in production)
valid_tokens = set()

# Database connection using PostgreSQL
def get_db():
    return psycopg2.connect(os.getenv('DATABASE_URL'))

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

# Authentication decorator
def require_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token or not token.startswith('Bearer '):
            return jsonify({'error': 'Unauthorized'}), 401
        token = token.replace('Bearer ', '')
        if token not in valid_tokens:
            return jsonify({'error': 'Invalid token'}), 401
        return f(*args, **kwargs)
    return decorated

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory('.', path)

# Public routes (no auth required)
@app.route('/api/articles', methods=['GET'])
def get_articles():
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM articles ORDER BY created_at DESC")
    articles = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(articles)

@app.route('/api/articles/<int:id>', methods=['GET'])
def get_article(id):
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM articles WHERE id = %s", (id,))
    article = cursor.fetchone()
    cursor.close()
    conn.close()
    return jsonify(article) if article else ('', 404)

@app.route('/api/poems', methods=['GET'])
def get_poems():
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM poems ORDER BY created_at DESC")
    poems = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(poems)

@app.route('/api/poems/<int:id>', methods=['GET'])
def get_poem(id):
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM poems WHERE id = %s", (id,))
    poem = cursor.fetchone()
    cursor.close()
    conn.close()
    return jsonify(poem) if poem else ('', 404)

@app.route('/api/comments/<poem_id>', methods=['GET'])
def get_comments(poem_id):
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM comments WHERE poemId = %s ORDER BY created_at DESC", (poem_id,))
    comments = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(comments)

@app.route('/api/comments', methods=['POST'])
def add_comment():
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    data = sanitize_object(request.json)
    cursor.execute("INSERT INTO comments (poemId, name, text) VALUES (%s, %s, %s)",
                  (data['poemId'], data['name'], data['text']))
    conn.commit()
    comment_id = cursor.lastrowid
    cursor.execute("SELECT * FROM comments WHERE id = %s", (comment_id,))
    comment = cursor.fetchone()
    cursor.close()
    conn.close()
    return jsonify(comment)

@app.route('/api/messages', methods=['POST'])
def add_message():
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    data = sanitize_object(request.json)
    if not validate_email(data.get('email', '')):
        return jsonify({'error': 'Invalid email'}), 400
    cursor.execute("""INSERT INTO messages (name, email, phone, company, service, budget, 
                     timeline, message, status) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)""",
                  (data.get('name'), data['email'], data.get('phone'), data.get('company'),
                   data.get('service'), data.get('budget'), data.get('timeline'), 
                   data.get('message'), 'new'))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({'success': True})

@app.route('/api/subscribers', methods=['POST'])
def add_subscriber():
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    data = sanitize_object(request.json)
    if not validate_email(data.get('email', '')):
        return jsonify({'error': 'Invalid email'}), 400
    cursor.execute("SELECT * FROM subscribers WHERE email = %s", (data['email'],))
    if cursor.fetchone():
        cursor.close()
        conn.close()
        return jsonify({'error': 'Email already subscribed'}), 400
    cursor.execute("INSERT INTO subscribers (email, firstName, lastName) VALUES (%s, %s, %s)",
                  (data['email'], data.get('firstName', ''), data.get('lastName', '')))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({'success': True})

# Protected admin routes (auth required)
@app.route('/api/articles', methods=['POST'])
@require_auth
def create_article():
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    data = sanitize_object(request.json)
    cursor.execute("""INSERT INTO articles (title, category, excerpt, content, image, slug) 
                     VALUES (%s, %s, %s, %s, %s, %s)""",
                  (data['title'], data['category'], data['excerpt'], data['content'], 
                   data.get('image', ''), re.sub(r'[^a-z0-9]+', '-', data['title'].lower())))
    conn.commit()
    article_id = cursor.lastrowid
    cursor.execute("SELECT * FROM articles WHERE id = %s", (article_id,))
    article = cursor.fetchone()
    cursor.close()
    conn.close()
    return jsonify(article)

@app.route('/api/articles/<int:id>', methods=['PUT', 'DELETE'])
@require_auth
def modify_article(id):
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    if request.method == 'DELETE':
        cursor.execute("DELETE FROM articles WHERE id = %s", (id,))
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({'success': True})
    data = sanitize_object(request.json)
    cursor.execute("""UPDATE articles SET title=%s, category=%s, excerpt=%s, content=%s, 
                     image=%s, slug=%s WHERE id=%s""",
                  (data['title'], data['category'], data['excerpt'], data['content'],
                   data.get('image', ''), re.sub(r'[^a-z0-9]+', '-', data['title'].lower()), id))
    conn.commit()
    cursor.execute("SELECT * FROM articles WHERE id = %s", (id,))
    article = cursor.fetchone()
    cursor.close()
    conn.close()
    return jsonify(article)

@app.route('/api/poems', methods=['POST'])
@require_auth
def create_poem():
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    data = sanitize_object(request.json)
    cursor.execute("INSERT INTO poems (title, excerpt, content) VALUES (%s, %s, %s)",
                  (data['title'], data['excerpt'], data['content']))
    conn.commit()
    poem_id = cursor.lastrowid
    cursor.execute("SELECT * FROM poems WHERE id = %s", (poem_id,))
    poem = cursor.fetchone()
    cursor.close()
    conn.close()
    return jsonify(poem)

@app.route('/api/poems/<int:id>', methods=['PUT', 'DELETE'])
@require_auth
def modify_poem(id):
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    if request.method == 'DELETE':
        cursor.execute("DELETE FROM poems WHERE id = %s", (id,))
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({'success': True})
    data = sanitize_object(request.json)
    cursor.execute("UPDATE poems SET title=%s, excerpt=%s, content=%s WHERE id=%s",
                  (data['title'], data['excerpt'], data['content'], id))
    conn.commit()
    cursor.execute("SELECT * FROM poems WHERE id = %s", (id,))
    poem = cursor.fetchone()
    cursor.close()
    conn.close()
    return jsonify(poem)

@app.route('/api/messages', methods=['GET'])
@require_auth
def get_messages():
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM messages ORDER BY created_at DESC")
    messages = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(messages)

@app.route('/api/messages/<int:id>', methods=['DELETE', 'PATCH'])
@require_auth
def modify_message(id):
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    if request.method == 'DELETE':
        cursor.execute("DELETE FROM messages WHERE id = %s", (id,))
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({'success': True})
    data = request.json
    cursor.execute("UPDATE messages SET status=%s WHERE id=%s", (data.get('status'), id))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({'success': True})

@app.route('/api/subscribers', methods=['GET'])
@require_auth
def get_subscribers():
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM subscribers ORDER BY created_at DESC")
    subscribers = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(subscribers)

@app.route('/api/subscribers/<int:id>', methods=['DELETE'])
@require_auth
def delete_subscriber(id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM subscribers WHERE id = %s", (id,))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({'success': True})

@app.route('/api/analytics', methods=['GET'])
@app.route('/api/analytics/dashboard', methods=['GET'])
@require_auth
def analytics():
    return jsonify({
        'totalVisitors': 0,
        'totalPageViews': 0,
        'todayVisitors': 0,
        'topPages': [],
        'recentEvents': []
    })

@app.route('/api/profile', methods=['GET', 'POST'])
@require_auth
def profile():
    if request.method == 'GET':
        return jsonify({
            'fullName': 'John Ngor Deng Garang',
            'email': 'dengjohn200@gmail.com',
            'phone': '+256 768 741 070',
            'username': ADMIN_USERNAME
        })
    
    # POST - Update password
    try:
        data = request.json
        new_password = data.get('newPassword', '').strip()
        if new_password:
            env_path = '.env'
            with open(env_path, 'r') as f:
                lines = f.readlines()
            with open(env_path, 'w') as f:
                for line in lines:
                    if line.startswith('ADMIN_PASSWORD='):
                        f.write(f'ADMIN_PASSWORD={new_password}\n')
                    else:
                        f.write(line)
            print(f"Password updated to: {new_password}")
            return jsonify({'success': True, 'message': 'Password updated'})
        return jsonify({'success': True})
    except Exception as e:
        print(f"Error updating password: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/test-credentials', methods=['GET'])
def test_credentials():
    return jsonify({
        'username': ADMIN_USERNAME,
        'password_length': len(ADMIN_PASSWORD) if ADMIN_PASSWORD else 0,
        'password_first_char': ADMIN_PASSWORD[0] if ADMIN_PASSWORD else None
    })

@app.route('/api/login', methods=['POST'])
def login():
    data = request.json
    print(f"Login attempt - Username: {data.get('username')}")
    print(f"Expected username: {ADMIN_USERNAME}")
    print(f"Expected password: {ADMIN_PASSWORD}")
    if data.get('username') == ADMIN_USERNAME and data.get('password') == ADMIN_PASSWORD:
        token = secrets.token_urlsafe(32)
        valid_tokens.add(token)
        print("Login successful!")
        return jsonify({'token': token})
    print("Login failed - Invalid credentials")
    return jsonify({'error': 'Invalid credentials'}), 401

if __name__ == '__main__':
    port = int(os.getenv('PORT', 3000))
    if not os.getenv('DATABASE_URL'):
        print("ERROR: DATABASE_URL environment variable not set!")
        exit(1)
    if not ADMIN_PASSWORD:
        print("ERROR: ADMIN_PASSWORD environment variable not set!")
        exit(1)
    print(f'Portfolio Backend Server Starting on port {port}')
    print(f'CORS allowed origins: {ALLOWED_ORIGINS}')
    app.run(port=port, debug=False, host='0.0.0.0')
