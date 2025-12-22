from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from functools import wraps
import os
from dotenv import load_dotenv
import hashlib
import time

load_dotenv()

app = Flask(__name__, static_folder='static')

# -----------------------------
# CORS Configuration
# -----------------------------
ALLOWED_ORIGINS = [
    'https://johngarang.com',
    'https://johngarangg.netlify.app',
    'http://localhost:3000'
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
    # Basic format check
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
# Static Files
# -----------------------------
@app.route('/static/<path:filename>')
def serve_static(filename):
    return send_from_directory(app.static_folder, filename)

# -----------------------------
# API Endpoints
# -----------------------------
@app.route('/')
def index():
    return jsonify({'status': 'running', 'message': 'Portfolio backend API'})

@app.route('/api/login', methods=['POST'])
def login():
    data = request.json
    if data.get('username') == ADMIN_USERNAME and data.get('password') == ADMIN_PASSWORD:
        token = generate_token(ADMIN_USERNAME)
        return jsonify({'token': token})
    return jsonify({'error': 'Invalid credentials'}), 401

# Dummy in-memory data for demonstration
MESSAGES = [
    {'id': 1, 'name': 'Alice', 'email': 'alice@example.com', 'message': 'Hello!', 'status': 'new', 'created_at': '2025-12-22'},
    {'id': 2, 'name': 'Bob', 'email': 'bob@example.com', 'message': 'Hi there!', 'status': 'new', 'created_at': '2025-12-22'}
]

SUBSCRIBERS = [
    {'id': 1, 'email': 'user1@example.com', 'firstName': 'John', 'lastName': 'Doe', 'created_at': '2025-12-22'},
    {'id': 2, 'email': 'user2@example.com', 'firstName': 'Jane', 'lastName': 'Smith', 'created_at': '2025-12-22'}
]

ARTICLES = [
    {'id': 1, 'title': 'My First Article', 'category': 'web', 'excerpt': 'Intro...', 'content': 'Full content', 'image': '', 'slug': 'my-first-article', 'created_at': '2025-12-22'}
]

# -----------------------------
# Dashboard Endpoints
# -----------------------------
@app.route('/api/subscribers', methods=['GET'])
@require_auth
def get_subscribers():
    return jsonify(SUBSCRIBERS)

@app.route('/api/messages', methods=['GET'])
@require_auth
def get_messages():
    return jsonify(MESSAGES)

@app.route('/api/analytics/dashboard', methods=['GET'])
@require_auth
def get_analytics_dashboard():
    return jsonify({
        'totalVisitors': 0,
        'totalPageViews': 0,
        'todayVisitors': 0,
        'totalMessages': len(MESSAGES),
        'totalSubscribers': len(SUBSCRIBERS),
        'totalArticles': len(ARTICLES),
        'topPages': [],
        'recentEvents': []
    })

@app.route('/api/profile', methods=['GET'])
@require_auth
def get_profile():
    return jsonify({
        'fullName': 'John Garang',
        'email': ADMIN_USERNAME,
        'phone': '',
        'username': ADMIN_USERNAME
    })

# -----------------------------
# Subscriber Management
# -----------------------------
@app.route('/api/subscribers/<int:subscriber_id>', methods=['DELETE'])
@require_auth
def delete_subscriber(subscriber_id):
    global SUBSCRIBERS
    SUBSCRIBERS = [s for s in SUBSCRIBERS if s['id'] != subscriber_id]
    return jsonify({'success': True})

# -----------------------------
# Messages Management
# -----------------------------
@app.route('/api/messages/<int:message_id>', methods=['PATCH', 'DELETE'])
@require_auth
def update_message(message_id):
    global MESSAGES
    if request.method == 'DELETE':
        MESSAGES = [m for m in MESSAGES if m['id'] != message_id]
        return jsonify({'success': True})
    elif request.method == 'PATCH':
        # Example: mark as read or update status
        for m in MESSAGES:
            if m['id'] == message_id:
                m['status'] = request.json.get('status', m['status'])
        return jsonify({'success': True})

# -----------------------------
# Run Server
# -----------------------------
if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
