import json
import mysql.connector
import os

DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'John@Alustudent1',
    'database': 'portfolio_db'
}

def create_database():
    conn = mysql.connector.connect(host=DB_CONFIG['host'], user=DB_CONFIG['user'], password=DB_CONFIG['password'])
    cursor = conn.cursor()
    cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_CONFIG['database']}")
    cursor.close()
    conn.close()

def create_tables():
    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor()
    
    cursor.execute("""CREATE TABLE IF NOT EXISTS articles (
        id INT AUTO_INCREMENT PRIMARY KEY,
        title VARCHAR(500),
        category VARCHAR(100),
        excerpt TEXT,
        content TEXT,
        image VARCHAR(500),
        slug VARCHAR(500),
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )""")
    
    cursor.execute("""CREATE TABLE IF NOT EXISTS poems (
        id INT AUTO_INCREMENT PRIMARY KEY,
        title VARCHAR(500),
        excerpt TEXT,
        content TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )""")
    
    cursor.execute("""CREATE TABLE IF NOT EXISTS messages (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(200),
        email VARCHAR(200),
        phone VARCHAR(50),
        company VARCHAR(200),
        service VARCHAR(100),
        budget VARCHAR(50),
        timeline VARCHAR(50),
        message TEXT,
        status VARCHAR(50),
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )""")
    
    cursor.execute("""CREATE TABLE IF NOT EXISTS subscribers (
        id INT AUTO_INCREMENT PRIMARY KEY,
        email VARCHAR(200) UNIQUE,
        firstName VARCHAR(100),
        lastName VARCHAR(100),
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )""")
    
    cursor.execute("""CREATE TABLE IF NOT EXISTS comments (
        id INT AUTO_INCREMENT PRIMARY KEY,
        poemId VARCHAR(50),
        name VARCHAR(200),
        text TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )""")
    
    cursor.execute("""CREATE TABLE IF NOT EXISTS analytics (
        id INT PRIMARY KEY,
        visitors INT DEFAULT 0,
        pageViews INT DEFAULT 0,
        contactForms INT DEFAULT 0,
        subscribers INT DEFAULT 0
    )""")
    
    conn.commit()
    cursor.close()
    conn.close()

def migrate_data():
    try:
        with open('database.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
    except:
        print('Using backup database...')
        with open('database.json.backup', 'r', encoding='utf-8') as f:
            data = json.load(f)
    
    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor()
    
    # Migrate articles
    for article in data.get('articles', []):
        cursor.execute("""INSERT INTO articles (title, category, excerpt, content, image, slug, created_at) 
                         VALUES (%s, %s, %s, %s, %s, %s, %s)""",
                      (article['title'], article['category'], article['excerpt'], article['content'],
                       article.get('image', ''), article['slug'], article['date']))
    
    # Migrate poems
    for poem in data.get('poems', []):
        cursor.execute("INSERT INTO poems (title, excerpt, content, created_at) VALUES (%s, %s, %s, %s)",
                      (poem['title'], poem['excerpt'], poem['content'], poem['date']))
    
    # Migrate messages
    for msg in data.get('messages', []):
        cursor.execute("""INSERT INTO messages (name, email, phone, company, service, budget, timeline, message, status, created_at) 
                         VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""",
                      (msg.get('name'), msg['email'], msg.get('phone'), msg.get('company'),
                       msg.get('service'), msg.get('budget'), msg.get('timeline'), 
                       msg.get('message'), msg.get('status', 'new'), msg['date']))
    
    # Migrate subscribers
    for sub in data.get('subscribers', []):
        try:
            cursor.execute("INSERT INTO subscribers (email, firstName, lastName, created_at) VALUES (%s, %s, %s, %s)",
                          (sub['email'], sub.get('firstName', ''), sub.get('lastName', ''), sub['date']))
        except:
            pass  # Skip duplicates
    
    # Migrate analytics
    analytics = data.get('analytics', {})
    cursor.execute("INSERT INTO analytics (id, visitors, pageViews, contactForms, subscribers) VALUES (1, %s, %s, %s, %s)",
                  (analytics.get('visitors', 0), analytics.get('pageViews', 0), 
                   analytics.get('contactForms', 0), analytics.get('subscribers', 0)))
    
    conn.commit()
    cursor.close()
    conn.close()

if __name__ == '__main__':
    print('Creating database...')
    create_database()
    print('Creating tables...')
    create_tables()
    print('Migrating data...')
    migrate_data()
    print('Migration complete!')
