from flask import Flask, render_template_string, request, redirect, url_for
import sqlite3
import os

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect('portfolio.db')
    cursor = conn.cursor()
    
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
    
    conn.commit()
    conn.close()

@app.route('/admin')
def admin_dashboard():
    conn = sqlite3.connect('portfolio.db')
    cursor = conn.cursor()
    
    cursor.execute('SELECT COUNT(*) FROM blog_posts')
    blog_count = cursor.fetchone()[0]
    
    cursor.execute('SELECT COUNT(*) FROM academic_works')
    academic_count = cursor.fetchone()[0]
    
    cursor.execute('SELECT COUNT(*) FROM travel_stories')
    travel_count = cursor.fetchone()[0]
    
    conn.close()
    
    return render_template_string('''
<!DOCTYPE html>
<html>
<head>
    <title>Admin Dashboard</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: Arial, sans-serif; background: #f5f5f5; }
        .container { max-width: 1200px; margin: 0 auto; padding: 20px; }
        .header { background: #333; color: white; padding: 20px; text-align: center; margin-bottom: 20px; }
        .stats { display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 20px; margin-bottom: 30px; }
        .stat-card { background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); text-align: center; }
        .stat-number { font-size: 2em; color: #007cba; font-weight: bold; }
        .forms { display: grid; grid-template-columns: repeat(auto-fit, minmax(400px, 1fr)); gap: 20px; }
        .form-section { background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
        .form-group { margin-bottom: 15px; }
        .form-group label { display: block; margin-bottom: 5px; font-weight: bold; }
        .form-group input, .form-group textarea { width: 100%; padding: 10px; border: 1px solid #ddd; border-radius: 4px; }
        .btn { background: #007cba; color: white; padding: 10px 20px; border: none; border-radius: 4px; cursor: pointer; width: 100%; }
        .btn:hover { background: #005a87; }
        .success { background: #d4edda; color: #155724; padding: 10px; border-radius: 4px; margin-bottom: 15px; }
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
                <div class="stat-number">{{ blog_count }}</div>
            </div>
            <div class="stat-card">
                <h3>Academic Works</h3>
                <div class="stat-number">{{ academic_count }}</div>
            </div>
            <div class="stat-card">
                <h3>Travel Stories</h3>
                <div class="stat-number">{{ travel_count }}</div>
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
    ''', blog_count=blog_count, academic_count=academic_count, travel_count=travel_count)

@app.route('/add-blog', methods=['POST'])
def add_blog():
    conn = sqlite3.connect('portfolio.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        INSERT INTO blog_posts (title, content, category)
        VALUES (?, ?, ?)
    ''', (request.form['title'], request.form['content'], request.form['category']))
    
    conn.commit()
    conn.close()
    
    return redirect('/admin')

@app.route('/add-academic', methods=['POST'])
def add_academic():
    conn = sqlite3.connect('portfolio.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        INSERT INTO academic_works (title, abstract, publication)
        VALUES (?, ?, ?)
    ''', (request.form['title'], request.form['abstract'], request.form.get('publication', '')))
    
    conn.commit()
    conn.close()
    
    return redirect('/admin')

@app.route('/add-travel', methods=['POST'])
def add_travel():
    conn = sqlite3.connect('portfolio.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        INSERT INTO travel_stories (title, location, content)
        VALUES (?, ?, ?)
    ''', (request.form['title'], request.form['location'], request.form['content']))
    
    conn.commit()
    conn.close()
    
    return redirect('/admin')

if __name__ == '__main__':
    init_db()
    app.run(debug=True, port=5001)