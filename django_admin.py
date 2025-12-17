#!/usr/bin/env python3
"""
Simple Django-like admin dashboard using Flask
Run with: python django_admin.py
"""

from flask import Flask, render_template_string, request, jsonify, redirect, url_for
import sqlite3
import json
from datetime import datetime, timedelta

app = Flask(__name__)

# Database setup
def init_db():
    conn = sqlite3.connect('portfolio.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS service_requests (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            full_name TEXT NOT NULL,
            email TEXT NOT NULL,
            phone TEXT,
            company TEXT,
            service TEXT NOT NULL,
            budget TEXT,
            timeline TEXT,
            description TEXT NOT NULL,
            status TEXT DEFAULT 'new',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS newsletter_subscribers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE NOT NULL,
            subscribed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            is_active BOOLEAN DEFAULT 1
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS blog_posts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            excerpt TEXT NOT NULL,
            content TEXT NOT NULL,
            date DATE NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    conn.commit()
    conn.close()

@app.route('/admin')
def admin_dashboard():
    conn = sqlite3.connect('portfolio.db')
    cursor = conn.cursor()
    
    # Get service requests
    cursor.execute('SELECT * FROM service_requests ORDER BY created_at DESC')
    requests = cursor.fetchall()
    
    # Get newsletter stats
    cursor.execute('SELECT COUNT(*) FROM newsletter_subscribers WHERE is_active = 1')
    total_subscribers = cursor.fetchone()[0]
    
    month_ago = (datetime.now() - timedelta(days=30)).isoformat()
    cursor.execute('SELECT COUNT(*) FROM newsletter_subscribers WHERE subscribed_at > ?', (month_ago,))
    this_month = cursor.fetchone()[0]
    
    week_ago = (datetime.now() - timedelta(days=7)).isoformat()
    cursor.execute('SELECT COUNT(*) FROM newsletter_subscribers WHERE subscribed_at > ?', (week_ago,))
    this_week = cursor.fetchone()[0]
    
    cursor.execute('SELECT email, subscribed_at FROM newsletter_subscribers ORDER BY subscribed_at DESC LIMIT 5')
    recent_subscribers = cursor.fetchall()
    
    conn.close()
    
    return render_template_string(ADMIN_TEMPLATE, 
                                requests=requests,
                                total_subscribers=total_subscribers,
                                this_month=this_month,
                                this_week=this_week,
                                recent_subscribers=recent_subscribers)

@app.route('/api/add-blog', methods=['POST'])
def add_blog():
    data = request.get_json()
    conn = sqlite3.connect('portfolio.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO blog_posts (title, excerpt, content, date)
        VALUES (?, ?, ?, ?)
    ''', (data['title'], data['excerpt'], data['content'], data['date']))
    conn.commit()
    conn.close()
    return jsonify({'success': True})

@app.route('/api/subscribe', methods=['POST'])
def subscribe():
    data = request.get_json()
    conn = sqlite3.connect('portfolio.db')
    cursor = conn.cursor()
    try:
        cursor.execute('INSERT INTO newsletter_subscribers (email) VALUES (?)', (data['email'],))
        conn.commit()
        conn.close()
        return jsonify({'success': True})
    except sqlite3.IntegrityError:
        conn.close()
        return jsonify({'success': False, 'error': 'Already subscribed'})

ADMIN_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>Admin Dashboard</title>
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: Arial, sans-serif; background: #f5f5f5; }
        .header { background: #2d3436; color: white; padding: 1rem; }
        .nav { background: #636e72; padding: 1rem; }
        .nav a { color: white; text-decoration: none; margin-right: 2rem; }
        .container { max-width: 1200px; margin: 0 auto; padding: 2rem; }
        .stats { display: grid; grid-template-columns: repeat(3, 1fr); gap: 1rem; margin-bottom: 2rem; }
        .stat-card { background: white; padding: 1.5rem; border-radius: 8px; text-align: center; }
        .stat-number { font-size: 2rem; font-weight: bold; color: #16b2dc; }
        .requests { background: white; padding: 1.5rem; border-radius: 8px; margin-bottom: 2rem; }
        .request-item { border-bottom: 1px solid #eee; padding: 1rem 0; }
        .status { padding: 0.25rem 0.75rem; border-radius: 15px; font-size: 0.8rem; }
        .status.new { background: #00b894; color: white; }
        .subscribers { background: white; padding: 1.5rem; border-radius: 8px; }
        .subscriber-item { display: flex; justify-content: space-between; padding: 0.5rem 0; border-bottom: 1px solid #eee; }
    </style>
</head>
<body>
    <div class="header">
        <h1><i class="fas fa-tachometer-alt"></i> Admin Dashboard</h1>
    </div>
    
    <div class="nav">
        <a href="#requests">Service Requests</a>
        <a href="#newsletter">Newsletter</a>
        <a href="../index.html">Back to Site</a>
    </div>
    
    <div class="container">
        <div class="stats">
            <div class="stat-card">
                <div class="stat-number">{{ requests|length }}</div>
                <div>Service Requests</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">{{ total_subscribers }}</div>
                <div>Total Subscribers</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">{{ this_week }}</div>
                <div>This Week</div>
            </div>
        </div>
        
        <div class="requests">
            <h2>Recent Service Requests</h2>
            {% for request in requests %}
            <div class="request-item">
                <h3>{{ request[1] }} - {{ request[5] }}</h3>
                <p><strong>Email:</strong> {{ request[2] }}</p>
                <p><strong>Service:</strong> {{ request[5] }}</p>
                <p><strong>Description:</strong> {{ request[8][:100] }}...</p>
                <span class="status {{ request[9] }}">{{ request[9] }}</span>
            </div>
            {% endfor %}
        </div>
        
        <div class="subscribers">
            <h2>Recent Newsletter Subscribers</h2>
            {% for subscriber in recent_subscribers %}
            <div class="subscriber-item">
                <span>{{ subscriber[0] }}</span>
                <span>{{ subscriber[1][:10] }}</span>
            </div>
            {% endfor %}
        </div>
    </div>
</body>
</html>
'''

if __name__ == '__main__':
    init_db()
    print("Admin dashboard running at: http://localhost:5000/admin")
    app.run(debug=True, port=5000)