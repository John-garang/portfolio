import http.server
import socketserver
import urllib.parse
import sqlite3
import json
from datetime import datetime

class AdminHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/admin' or self.path == '/admin/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            
            # Get counts from database
            conn = sqlite3.connect('portfolio.db')
            cursor = conn.cursor()
            
            try:
                cursor.execute('SELECT COUNT(*) FROM blog_posts')
                blog_count = cursor.fetchone()[0]
            except:
                blog_count = 0
                
            try:
                cursor.execute('SELECT COUNT(*) FROM academic_works')
                academic_count = cursor.fetchone()[0]
            except:
                academic_count = 0
                
            try:
                cursor.execute('SELECT COUNT(*) FROM travel_stories')
                travel_count = cursor.fetchone()[0]
            except:
                travel_count = 0
            
            conn.close()
            
            html = f'''
<!DOCTYPE html>
<html>
<head>
    <title>Admin Dashboard</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: Arial, sans-serif; background: #f5f5f5; }}
        .container {{ max-width: 1200px; margin: 0 auto; padding: 20px; }}
        .header {{ background: #333; color: white; padding: 20px; text-align: center; margin-bottom: 20px; }}
        .stats {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 20px; margin-bottom: 30px; }}
        .stat-card {{ background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); text-align: center; }}
        .stat-number {{ font-size: 2em; color: #007cba; font-weight: bold; }}
        .forms {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(400px, 1fr)); gap: 20px; }}
        .form-section {{ background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }}
        .form-group {{ margin-bottom: 15px; }}
        .form-group label {{ display: block; margin-bottom: 5px; font-weight: bold; }}
        .form-group input, .form-group textarea {{ width: 100%; padding: 10px; border: 1px solid #ddd; border-radius: 4px; }}
        .btn {{ background: #007cba; color: white; padding: 10px 20px; border: none; border-radius: 4px; cursor: pointer; width: 100%; }}
        .btn:hover {{ background: #005a87; }}
        .success {{ background: #d4edda; color: #155724; padding: 10px; border-radius: 4px; margin-bottom: 15px; }}
    </style>
</head>
<body>
    <div class="header">
        <h1>Portfolio Admin Dashboard</h1>
        <p>Manage your content</p>
    </div>

    <div class="container">
        <div class="stats">
            <div class="stat-card">
                <h3>Blog Posts</h3>
                <div class="stat-number">{blog_count}</div>
            </div>
            <div class="stat-card">
                <h3>Academic Works</h3>
                <div class="stat-number">{academic_count}</div>
            </div>
            <div class="stat-card">
                <h3>Travel Stories</h3>
                <div class="stat-number">{travel_count}</div>
            </div>
        </div>

        <div class="forms">
            <div class="form-section">
                <h2>Add Blog Post</h2>
                <form action="/add-blog" method="post">
                    <div class="form-group">
                        <label>Title</label>
                        <input type="text" name="title" required>
                    </div>
                    <div class="form-group">
                        <label>Content</label>
                        <textarea name="content" rows="6" required></textarea>
                    </div>
                    <div class="form-group">
                        <label>Category</label>
                        <input type="text" name="category" required>
                    </div>
                    <button type="submit" class="btn">Create Blog Post</button>
                </form>
            </div>

            <div class="form-section">
                <h2>Add Academic Work</h2>
                <form action="/add-academic" method="post">
                    <div class="form-group">
                        <label>Title</label>
                        <input type="text" name="title" required>
                    </div>
                    <div class="form-group">
                        <label>Abstract</label>
                        <textarea name="abstract" rows="4" required></textarea>
                    </div>
                    <div class="form-group">
                        <label>Publication</label>
                        <input type="text" name="publication">
                    </div>
                    <button type="submit" class="btn">Add Academic Work</button>
                </form>
            </div>

            <div class="form-section">
                <h2>Add Travel Story</h2>
                <form action="/add-travel" method="post">
                    <div class="form-group">
                        <label>Title</label>
                        <input type="text" name="title" required>
                    </div>
                    <div class="form-group">
                        <label>Location</label>
                        <input type="text" name="location" required>
                    </div>
                    <div class="form-group">
                        <label>Content</label>
                        <textarea name="content" rows="6" required></textarea>
                    </div>
                    <button type="submit" class="btn">Add Travel Story</button>
                </form>
            </div>
        </div>
    </div>
</body>
</html>
            '''
            self.wfile.write(html.encode())
        else:
            super().do_GET()
    
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        form_data = urllib.parse.parse_qs(post_data.decode('utf-8'))
        
        # Initialize database
        conn = sqlite3.connect('portfolio.db')
        cursor = conn.cursor()
        
        # Create tables if they don't exist
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS blog_posts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                content TEXT NOT NULL,
                category TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS academic_works (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                abstract TEXT NOT NULL,
                publication TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS travel_stories (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                location TEXT NOT NULL,
                content TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        if self.path == '/add-blog':
            cursor.execute('''
                INSERT INTO blog_posts (title, content, category)
                VALUES (?, ?, ?)
            ''', (form_data['title'][0], form_data['content'][0], form_data['category'][0]))
            
        elif self.path == '/add-academic':
            cursor.execute('''
                INSERT INTO academic_works (title, abstract, publication)
                VALUES (?, ?, ?)
            ''', (form_data['title'][0], form_data['abstract'][0], form_data.get('publication', [''])[0]))
            
        elif self.path == '/add-travel':
            cursor.execute('''
                INSERT INTO travel_stories (title, location, content)
                VALUES (?, ?, ?)
            ''', (form_data['title'][0], form_data['location'][0], form_data['content'][0]))
        
        conn.commit()
        conn.close()
        
        # Redirect back to admin
        self.send_response(302)
        self.send_header('Location', '/admin')
        self.end_headers()

if __name__ == '__main__':
    PORT = 8888
    
    class ReusableTCPServer(socketserver.TCPServer):
        allow_reuse_address = True
    
    with ReusableTCPServer(("", PORT), AdminHandler) as httpd:
        print(f"Admin dashboard running at http://localhost:{PORT}/admin")
        httpd.serve_forever()