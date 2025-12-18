from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import mysql.connector
import json
import os
import re
from datetime import datetime

app = Flask(__name__, static_folder='.')
CORS(app, resources={r"/api/*": {"origins": "*", "methods": ["GET", "POST", "PUT", "DELETE", "PATCH"]}})

DB_CONFIG = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'user': os.getenv('DB_USER', 'root'),
    'password': os.getenv('DB_PASSWORD', 'John@Alustudent1'),
    'database': os.getenv('DB_NAME', 'portfolio_db')
}

def get_db():
    return mysql.connector.connect(**DB_CONFIG)

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

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory('.', path)

# Articles
@app.route('/api/articles', methods=['GET', 'POST'])
def articles():
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    if request.method == 'POST':
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
    cursor.execute("SELECT * FROM articles ORDER BY created_at DESC")
    articles = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(articles)

@app.route('/api/articles/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def article(id):
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    if request.method == 'DELETE':
        cursor.execute("DELETE FROM articles WHERE id = %s", (id,))
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({'success': True})
    if request.method == 'PUT':
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
    return jsonify(article) if article else ('', 404)

# Poems
@app.route('/api/poems', methods=['GET', 'POST'])
def poems():
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    if request.method == 'POST':
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
    cursor.execute("SELECT * FROM poems ORDER BY created_at DESC")
    poems = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(poems)

@app.route('/api/poems/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def poem(id):
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    if request.method == 'DELETE':
        cursor.execute("DELETE FROM poems WHERE id = %s", (id,))
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({'success': True})
    if request.method == 'PUT':
        data = sanitize_object(request.json)
        cursor.execute("UPDATE poems SET title=%s, excerpt=%s, content=%s WHERE id=%s",
                      (data['title'], data['excerpt'], data['content'], id))
        conn.commit()
    cursor.execute("SELECT * FROM poems WHERE id = %s", (id,))
    poem = cursor.fetchone()
    cursor.close()
    conn.close()
    return jsonify(poem) if poem else ('', 404)

# Messages
@app.route('/api/messages', methods=['GET', 'POST'])
def messages():
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    if request.method == 'POST':
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
    cursor.execute("SELECT * FROM messages ORDER BY created_at DESC")
    messages = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(messages)

@app.route('/api/messages/<int:id>', methods=['DELETE', 'PATCH'])
def message(id):
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    if request.method == 'DELETE':
        cursor.execute("DELETE FROM messages WHERE id = %s", (id,))
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({'success': True})
    if request.method == 'PATCH':
        data = request.json
        cursor.execute("UPDATE messages SET status=%s WHERE id=%s", (data.get('status'), id))
        conn.commit()
    cursor.close()
    conn.close()
    return jsonify({'success': True})

# Subscribers
@app.route('/api/subscribers', methods=['GET', 'POST'])
def subscribers():
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    if request.method == 'POST':
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
    cursor.execute("SELECT * FROM subscribers ORDER BY created_at DESC")
    subscribers = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(subscribers)

@app.route('/api/subscribers/<int:id>', methods=['DELETE'])
def subscriber(id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM subscribers WHERE id = %s", (id,))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({'success': True})

# Comments
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

@app.route('/api/comments/<poem_id>', methods=['GET'])
def get_comments(poem_id):
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM comments WHERE poemId = %s ORDER BY created_at DESC", (poem_id,))
    comments = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(comments)

# Analytics
@app.route('/api/analytics', methods=['GET'])
def analytics():
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM analytics WHERE id = 1")
    analytics = cursor.fetchone()
    cursor.close()
    conn.close()
    return jsonify(analytics or {})

# Profile
@app.route('/api/profile', methods=['GET'])
def profile():
    return jsonify({
        'fullName': 'John Ngor Deng Garang',
        'email': 'dengjohn200@gmail.com',
        'phone': '+256 768 741 070',
        'username': 'admin'
    })

# Login
@app.route('/api/login', methods=['POST'])
def login():
    data = request.json
    if data.get('username') == 'admin' and data.get('password') == 'admin123':
        return jsonify({'token': f"admin-token-{int(datetime.now().timestamp())}"})
    return jsonify({'error': 'Invalid credentials'}), 401

if __name__ == '__main__':
    print('MySQL Flask Server Starting on port 3000')
    app.run(port=3000, debug=False)
