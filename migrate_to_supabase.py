import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

# Current Render DB
RENDER_DB = "postgresql://portfolio_db_twcn_user:Eu50hgLBOjV6HiunGOdNnvPiOqnilBBi@dpg-d52i2d95pdvs73fgtvl0-a.virginia-postgres.render.com/portfolio_db_twcn"

# New Supabase DB (@ symbol encoded as %40)
SUPABASE_DB = "postgresql://postgres:John%40Alustudent1@db.dynharywcbwznknrvetq.supabase.co:5432/postgres"

def migrate_to_supabase():
    # Connect to both databases
    render_conn = psycopg2.connect(RENDER_DB)
    supabase_conn = psycopg2.connect(SUPABASE_DB)
    
    render_cur = render_conn.cursor()
    supabase_cur = supabase_conn.cursor()
    
    # Create tables in Supabase
    tables = [
        """CREATE TABLE IF NOT EXISTS messages (
            id SERIAL PRIMARY KEY,
            name VARCHAR(255), email VARCHAR(255), phone VARCHAR(50),
            company VARCHAR(255), service VARCHAR(255), budget VARCHAR(100),
            timeline VARCHAR(100), message TEXT, status VARCHAR(50) DEFAULT 'new',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )""",
        """CREATE TABLE IF NOT EXISTS subscribers (
            id SERIAL PRIMARY KEY, email VARCHAR(255) UNIQUE,
            firstName VARCHAR(255), lastName VARCHAR(255),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )""",
        """CREATE TABLE IF NOT EXISTS articles (
            id SERIAL PRIMARY KEY, title VARCHAR(255), category VARCHAR(100),
            excerpt TEXT, content TEXT, image VARCHAR(255), slug VARCHAR(255),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )""",
        """CREATE TABLE IF NOT EXISTS poems (
            id SERIAL PRIMARY KEY, title VARCHAR(255),
            excerpt TEXT, content TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )"""
    ]
    
    for table in tables:
        supabase_cur.execute(table)
    
    # Copy data
    for table_name in ['messages', 'subscribers', 'articles', 'poems']:
        render_cur.execute(f"SELECT * FROM {table_name}")
        rows = render_cur.fetchall()
        
        if rows:
            render_cur.execute(f"SELECT column_name FROM information_schema.columns WHERE table_name='{table_name}'")
            columns = [row[0] for row in render_cur.fetchall()]
            
            placeholders = ','.join(['%s'] * len(columns))
            supabase_cur.executemany(
                f"INSERT INTO {table_name} ({','.join(columns)}) VALUES ({placeholders})",
                rows
            )
        
        print(f"Migrated {len(rows)} rows from {table_name}")
    
    supabase_conn.commit()
    print("Migration complete!")

if __name__ == "__main__":
    migrate_to_supabase()