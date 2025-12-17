from flask import Flask, render_template_string
import sqlite3
import os

app = Flask(__name__)

# Create database if it doesn't exist
def init_db():
    conn = sqlite3.connect('portfolio.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS service_requests (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            service_type TEXT NOT NULL,
            budget TEXT,
            timeline TEXT,
            description TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS newsletter_subscribers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE NOT NULL,
            subscribed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    conn.commit()
    conn.close()

@app.route('/admin')
def admin_dashboard():
    conn = sqlite3.connect('portfolio.db')
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM service_requests ORDER BY created_at DESC')
    service_requests = cursor.fetchall()
    
    cursor.execute('SELECT * FROM newsletter_subscribers ORDER BY subscribed_at DESC')
    newsletter_subscribers = cursor.fetchall()
    
    conn.close()
    
    with open('admin_dashboard.html', 'r') as f:
        template = f.read()
    
    # Simple template replacement
    template = template.replace('{{ service_requests.count }}', str(len(service_requests)))
    template = template.replace('{{ blog_posts.count }}', '0')
    template = template.replace('{{ newsletter_subscribers.count }}', str(len(newsletter_subscribers)))
    
    return template

if __name__ == '__main__':
    init_db()
    app.run(debug=True, port=5000)