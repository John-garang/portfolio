import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

def init_database():
    conn = psycopg2.connect(os.getenv('DATABASE_URL'))
    cursor = conn.cursor()
    
    # Create tables
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS articles (
            id SERIAL PRIMARY KEY,
            title VARCHAR(255) NOT NULL,
            category VARCHAR(100),
            excerpt TEXT,
            content TEXT,
            image VARCHAR(255),
            slug VARCHAR(255),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS poems (
            id SERIAL PRIMARY KEY,
            title VARCHAR(255) NOT NULL,
            excerpt TEXT,
            content TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS comments (
            id SERIAL PRIMARY KEY,
            poemId INTEGER REFERENCES poems(id),
            name VARCHAR(100),
            text TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS messages (
            id SERIAL PRIMARY KEY,
            name VARCHAR(100),
            email VARCHAR(255),
            phone VARCHAR(50),
            company VARCHAR(255),
            service VARCHAR(100),
            budget VARCHAR(100),
            timeline VARCHAR(100),
            message TEXT,
            status VARCHAR(50) DEFAULT 'new',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS subscribers (
            id SERIAL PRIMARY KEY,
            email VARCHAR(255) UNIQUE,
            firstName VARCHAR(100),
            lastName VARCHAR(100),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    conn.commit()
    cursor.close()
    conn.close()
    print("Database initialized successfully!")

if __name__ == '__main__':
    init_database()