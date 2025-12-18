from flask import Flask, request, jsonify, redirect, send_from_directory
from flask_cors import CORS
import json
import os
import re
import shutil
from datetime import datetime

app = Flask(__name__, static_folder='.')
CORS(app, resources={r"/api/*": {"origins": "*", "methods": ["GET", "POST", "PUT", "DELETE", "PATCH"]}})

DB_FILE = 'database.json'
BACKUP_DIR = 'database_backups'

def sanitize_input(text):
    if not isinstance(text, str):
        return text
    return (text.replace('<', '&lt;').replace('>', '&gt;').replace('"', '&quot;')
            .replace("'", '&#x27;').replace('/', '&#x2F;'))

def sanitize_object(obj):
    if isinstance(obj, dict):
        return {k: sanitize_object(v) for k, v in obj.items()}
    elif isinstance(obj, str):
        return sanitize_input(obj)
    return obj

def validate_email(email):
    return re.match(r'^[^\s@]+@[^\s@]+\.[^\s@]+$', email) is not None

def read_db():
    with open(DB_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def backup_db():
    if not os.path.exists(BACKUP_DIR):
        os.makedirs(BACKUP_DIR)
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    backup_file = os.path.join(BACKUP_DIR, f'database_{timestamp}.json')
    shutil.copy2(DB_FILE, backup_file)
    return backup_file

def write_db(data):
    backup_db()
    with open(DB_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory('.', path)

# Articles
@app.route('/api/articles', methods=['GET', 'POST'])
def articles():
    db = read_db()
    if request.method == 'POST':
        data = sanitize_object(request.json)
        article = {
            'id': int(datetime.now().timestamp() * 1000),
            'title': data['title'],
            'category': data['category'],
            'excerpt': data['excerpt'],
            'content': data['content'],
            'image': data.get('image', ''),
            'date': datetime.now().strftime('%Y-%m-%d'),
            'slug': re.sub(r'[^a-z0-9]+', '-', data['title'].lower())
        }
        db['articles'].insert(0, article)
        write_db(db)
        return jsonify(article)
    return jsonify(db.get('articles', []))

@app.route('/api/articles/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def article(id):
    if not id or id <= 0:
        return jsonify({'error': 'Valid ID required'}), 400
    db = read_db()
    if request.method == 'DELETE':
        article_to_delete = next((a for a in db.get('articles', []) if a['id'] == id), None)
        if not article_to_delete:
            return jsonify({'error': 'Article not found'}), 404
        pass
        db['articles'] = [a for a in db.get('articles', []) if a['id'] != id]
        write_db(db)
        return jsonify({'success': True})
    if request.method == 'PUT':
        for a in db.get('articles', []):
            if a['id'] == id:
                data = sanitize_object(request.json)
                a.update({
                    'title': data['title'],
                    'category': data['category'],
                    'excerpt': data['excerpt'],
                    'content': data['content'],
                    'image': data.get('image', ''),
                    'slug': re.sub(r'[^a-z0-9]+', '-', data['title'].lower())
                })
                write_db(db)
                return jsonify(a)
    article = next((a for a in db.get('articles', []) if a['id'] == id), None)
    return jsonify(article) if article else ('', 404)

@app.route('/delete_article', methods=['POST'])
def delete_article_form():
    db = read_db()
    article_id = int(request.form.get('article_id'))
    db['articles'] = [a for a in db['articles'] if a['id'] != article_id]
    write_db(db)
    return redirect('/admin-dashboard.html')

# Poems
@app.route('/api/poems', methods=['GET', 'POST'])
def poems():
    db = read_db()
    if request.method == 'POST':
        data = sanitize_object(request.json)
        poem = {
            'id': int(datetime.now().timestamp() * 1000),
            'title': data['title'],
            'excerpt': data['excerpt'],
            'content': data['content'],
            'date': datetime.now().strftime('%Y-%m-%d')
        }
        db['poems'].insert(0, poem)
        write_db(db)
        return jsonify(poem)
    return jsonify(db.get('poems', []))

@app.route('/api/poems/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def poem(id):
    if not id or id <= 0:
        return jsonify({'error': 'Valid ID required'}), 400
    db = read_db()
    if request.method == 'DELETE':
        poem_to_delete = next((p for p in db.get('poems', []) if p['id'] == id), None)
        if not poem_to_delete:
            return jsonify({'error': 'Poem not found'}), 404
        pass
        db['poems'] = [p for p in db.get('poems', []) if p['id'] != id]
        write_db(db)
        return jsonify({'success': True})
    if request.method == 'PUT':
        for p in db.get('poems', []):
            if p['id'] == id:
                p.update(sanitize_object(request.json))
                write_db(db)
                return jsonify(p)
    poem = next((p for p in db.get('poems', []) if p['id'] == id), None)
    return jsonify(poem) if poem else ('', 404)

# Messages
@app.route('/api/messages', methods=['GET', 'POST'])
def messages():
    db = read_db()
    if request.method == 'POST':
        data = sanitize_object(request.json)
        if not data.get('email') or not validate_email(data['email']):
            return jsonify({'error': 'Invalid email'}), 400
        msg = {
            'id': int(datetime.now().timestamp() * 1000),
            **data,
            'date': datetime.now().strftime('%Y-%m-%d'),
            'status': 'new'
        }
        db['messages'].insert(0, msg)
        db['analytics']['contactForms'] = db['analytics'].get('contactForms', 0) + 1
        write_db(db)
        return jsonify(msg)
    return jsonify(db.get('messages', []))

@app.route('/api/messages/<int:id>', methods=['DELETE', 'PATCH'])
def message(id):
    if not id or id <= 0:
        return jsonify({'error': 'Valid ID required'}), 400
    db = read_db()
    if request.method == 'DELETE':
        msg_to_delete = next((m for m in db.get('messages', []) if m['id'] == id), None)
        if not msg_to_delete:
            return jsonify({'error': 'Message not found'}), 404
        pass
        db['messages'] = [m for m in db['messages'] if m['id'] != id]
        write_db(db)
        return jsonify({'success': True})
    if request.method == 'PATCH':
        for m in db['messages']:
            if m['id'] == id:
                m.update(request.json)
                write_db(db)
                return jsonify(m)
    return jsonify({'success': False})

# Subscribers
@app.route('/api/subscribers', methods=['GET', 'POST'])
def subscribers():
    db = read_db()
    if request.method == 'POST':
        data = sanitize_object(request.json)
        if not data.get('email') or not validate_email(data['email']):
            return jsonify({'error': 'Invalid email'}), 400
        if any(s['email'] == data['email'] for s in db.get('subscribers', [])):
            return jsonify({'error': 'Email already subscribed'}), 400
        sub = {
            'id': int(datetime.now().timestamp() * 1000),
            'email': data['email'],
            'firstName': data.get('firstName', ''),
            'lastName': data.get('lastName', ''),
            'date': datetime.now().strftime('%Y-%m-%d')
        }
        db['subscribers'].append(sub)
        db['analytics']['subscribers'] = db['analytics'].get('subscribers', 0) + 1
        write_db(db)
        return jsonify(sub)
    return jsonify(db.get('subscribers', []))

@app.route('/api/subscribers/<int:id>', methods=['DELETE'])
def subscriber(id):
    if not id or id <= 0:
        return jsonify({'error': 'Valid ID required'}), 400
    db = read_db()
    sub_to_delete = next((s for s in db.get('subscribers', []) if s['id'] == id), None)
    if not sub_to_delete:
        return jsonify({'error': 'Subscriber not found'}), 404
    pass
    db['subscribers'] = [s for s in db['subscribers'] if s['id'] != id]
    write_db(db)
    return jsonify({'success': True})

# Analytics
@app.route('/api/analytics', methods=['GET', 'PATCH'])
def analytics():
    db = read_db()
    if request.method == 'PATCH':
        db['analytics'].update(request.json)
        write_db(db)
    return jsonify(db.get('analytics', {}))

@app.route('/api/analytics/track', methods=['POST'])
def track_analytics():
    db = read_db()
    if 'events' not in db:
        db['events'] = []
    if 'sessions' not in db:
        db['sessions'] = []
    
    event = {
        'id': int(datetime.now().timestamp() * 1000),
        **request.json,
        'ip': request.remote_addr
    }
    db['events'].append(event)
    
    if event.get('eventType') == 'page_view':
        session_id = event.get('sessionId')
        existing = next((s for s in db['sessions'] if s['sessionId'] == session_id), None)
        if not existing:
            db['sessions'].append({
                'sessionId': session_id,
                'startTime': event.get('timestamp'),
                'pages': [event.get('page')],
                'events': 1
            })
            db['analytics']['visitors'] = db['analytics'].get('visitors', 0) + 1
        else:
            if event.get('page') not in existing['pages']:
                existing['pages'].append(event.get('page'))
            existing['events'] += 1
        db['analytics']['pageViews'] = db['analytics'].get('pageViews', 0) + 1
    
    write_db(db)
    return jsonify({'success': True})

@app.route('/api/analytics/dashboard')
def analytics_dashboard():
    db = read_db()
    events = db.get('events', [])
    today = datetime.now().strftime('%Y-%m-%d')
    today_events = [e for e in events if e.get('timestamp', '').startswith(today)]
    
    page_counts = {}
    for e in events[-100:]:
        if e.get('eventType') == 'page_view':
            page = e.get('page', 'Unknown')
            page_counts[page] = page_counts.get(page, 0) + 1
    
    top_pages = [{'page': p, 'count': c} for p, c in sorted(page_counts.items(), key=lambda x: x[1], reverse=True)[:5]]
    
    return jsonify({
        'totalVisitors': db.get('analytics', {}).get('visitors', 0),
        'totalPageViews': db.get('analytics', {}).get('pageViews', 0),
        'todayVisitors': len(set(e.get('sessionId') for e in today_events if e.get('eventType') == 'page_view')),
        'topPages': top_pages,
        'recentEvents': events[-50:]
    })

# Profile
@app.route('/api/profile', methods=['GET', 'POST'])
def profile():
    if request.method == 'POST':
        return jsonify({'success': True})
    return jsonify({
        'fullName': 'John Ngor Deng Garang',
        'email': 'dengjohn200@gmail.com',
        'phone': '+256 768 741 070',
        'username': 'admin'
    })

# Comments
@app.route('/api/comments', methods=['POST'])
def add_comment():
    db = read_db()
    if 'comments' not in db:
        db['comments'] = []
    data = sanitize_object(request.json)
    comment = {
        'id': int(datetime.now().timestamp() * 1000),
        'poemId': data['poemId'],
        'name': data['name'],
        'text': data['text'],
        'date': data['date']
    }
    db['comments'].append(comment)
    write_db(db)
    return jsonify(comment)

@app.route('/api/comments/<poem_id>', methods=['GET'])
def get_comments(poem_id):
    db = read_db()
    comments = [c for c in db.get('comments', []) if c['poemId'] == poem_id]
    return jsonify(comments)

# Login
@app.route('/api/login', methods=['POST'])
def login():
    data = request.json
    if data.get('username') == 'admin' and data.get('password') == 'admin123':
        return jsonify({'token': f"admin-token-{int(datetime.now().timestamp())}"})
    return jsonify({'error': 'Invalid credentials'}), 401

@app.route('/api/restore-backup', methods=['POST'])
def restore_backup():
    data = request.json
    backup_file = data.get('backup_file')
    if backup_file and os.path.exists(backup_file):
        shutil.copy2(backup_file, DB_FILE)
        return jsonify({'success': True, 'message': 'Database restored'})
    return jsonify({'success': False, 'error': 'Backup file not found'}), 404

@app.route('/api/list-backups', methods=['GET'])
def list_backups():
    if not os.path.exists(BACKUP_DIR):
        return jsonify([])
    backups = [f for f in os.listdir(BACKUP_DIR) if f.endswith('.json')]
    backups.sort(reverse=True)
    return jsonify([{'file': os.path.join(BACKUP_DIR, b), 'name': b} for b in backups[:10]])

if __name__ == '__main__':
    print('\n' + '='*60)
    print('Flask Server Starting')
    print('='*60)
    print(f'Database: {DB_FILE}')
    print(f'Backups: {BACKUP_DIR}/')
    print(f'Auto-backup: ENABLED (before every write)')
    print('='*60 + '\n')
    app.run(port=3000, debug=True)
