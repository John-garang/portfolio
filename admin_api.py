#!/usr/bin/env python3
"""
Standalone Python script to handle admin dashboard functionality
Run with: python admin_api.py
"""

import sqlite3
import json
from datetime import datetime, timedelta
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import cgi

class AdminAPI:
    def __init__(self, db_path='portfolio.db'):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """Initialize SQLite database with required tables"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Service Requests table
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
        
        # Blog Posts table
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
        
        # Academic Works table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS academic_works (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                abstract TEXT NOT NULL,
                content TEXT NOT NULL,
                work_type TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Travel Stories table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS travel_stories (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                location TEXT NOT NULL,
                excerpt TEXT NOT NULL,
                content TEXT NOT NULL,
                travel_date DATE NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Newsletter Subscribers table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS newsletter_subscribers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                email TEXT UNIQUE NOT NULL,
                subscribed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                is_active BOOLEAN DEFAULT 1
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def get_service_requests(self):
        """Get all service requests"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM service_requests ORDER BY created_at DESC')
        requests = cursor.fetchall()
        conn.close()
        return requests
    
    def add_service_request(self, data):
        """Add new service request"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO service_requests 
            (full_name, email, phone, company, service, budget, timeline, description)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            data['full_name'], data['email'], data.get('phone', ''),
            data.get('company', ''), data['service'], data.get('budget', ''),
            data.get('timeline', ''), data['description']
        ))
        conn.commit()
        conn.close()
        return True
    
    def add_blog_post(self, data):
        """Add new blog post"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO blog_posts (title, excerpt, content, date)
            VALUES (?, ?, ?, ?)
        ''', (data['title'], data['excerpt'], data['content'], data['date']))
        conn.commit()
        conn.close()
        return True
    
    def add_newsletter_subscriber(self, email):
        """Add newsletter subscriber"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        try:
            cursor.execute('INSERT INTO newsletter_subscribers (email) VALUES (?)', (email,))
            conn.commit()
            conn.close()
            return True
        except sqlite3.IntegrityError:
            conn.close()
            return False
    
    def get_newsletter_stats(self):
        """Get newsletter statistics"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Total subscribers
        cursor.execute('SELECT COUNT(*) FROM newsletter_subscribers WHERE is_active = 1')
        total = cursor.fetchone()[0]
        
        # This month
        month_ago = (datetime.now() - timedelta(days=30)).isoformat()
        cursor.execute('SELECT COUNT(*) FROM newsletter_subscribers WHERE subscribed_at > ?', (month_ago,))
        this_month = cursor.fetchone()[0]
        
        # This week
        week_ago = (datetime.now() - timedelta(days=7)).isoformat()
        cursor.execute('SELECT COUNT(*) FROM newsletter_subscribers WHERE subscribed_at > ?', (week_ago,))
        this_week = cursor.fetchone()[0]
        
        # Recent subscribers
        cursor.execute('SELECT email, subscribed_at FROM newsletter_subscribers ORDER BY subscribed_at DESC LIMIT 5')
        recent = cursor.fetchall()
        
        conn.close()
        
        return {
            'total': total,
            'this_month': this_month,
            'this_week': this_week,
            'recent': recent
        }

class AdminHandler(BaseHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        self.api = AdminAPI()
        super().__init__(*args, **kwargs)
    
    def do_GET(self):
        """Handle GET requests"""
        path = urlparse(self.path).path
        
        if path == '/api/service-requests':
            requests = self.api.get_service_requests()
            self.send_json_response({'requests': requests})
        
        elif path == '/api/newsletter-stats':
            stats = self.api.get_newsletter_stats()
            self.send_json_response(stats)
        
        else:
            self.send_error(404)
    
    def do_POST(self):
        """Handle POST requests"""
        path = urlparse(self.path).path
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        
        try:
            data = json.loads(post_data.decode('utf-8'))
        except:
            self.send_error(400)
            return
        
        if path == '/api/add-service-request':
            success = self.api.add_service_request(data)
            self.send_json_response({'success': success})
        
        elif path == '/api/add-blog-post':
            success = self.api.add_blog_post(data)
            self.send_json_response({'success': success})
        
        elif path == '/api/subscribe-newsletter':
            success = self.api.add_newsletter_subscriber(data['email'])
            self.send_json_response({'success': success})
        
        else:
            self.send_error(404)
    
    def send_json_response(self, data):
        """Send JSON response"""
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())

def run_server(port=8000):
    """Run the admin API server"""
    server_address = ('', port)
    httpd = HTTPServer(server_address, AdminHandler)
    print(f"Admin API server running on port {port}")
    print(f"Access at: http://localhost:{port}")
    httpd.serve_forever()

if __name__ == '__main__':
    run_server()