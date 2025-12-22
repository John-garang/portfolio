import json
import psycopg2
import psycopg2.extras
import urllib.parse
import os
from dotenv import load_dotenv

load_dotenv()

# Database configuration
DATABASE_URL = os.getenv('DATABASE_URL') or \
    "postgresql://portfolio_db_twcn_user:Eu50hgLBOjV6HiunGOdNnvPiOqnilBBi@dpg-d52i2d95pdvs73fgtvl0-a.virginia-postgres.render.com/portfolio_db_twcn"

parsed = urllib.parse.urlparse(DATABASE_URL)
DB_CONFIG = {
    'host': parsed.hostname,
    'user': parsed.username,
    'password': parsed.password,
    'database': parsed.path[1:],
    'port': parsed.port or 5432
}

def migrate_data():
    try:
        # Load JSON data
        with open('database.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Connect to PostgreSQL
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()
        
        print("Migrating data to PostgreSQL...")
        
        # Migrate articles
        if 'articles' in data:
            print(f"Migrating {len(data['articles'])} articles...")
            for article in data['articles']:
                cursor.execute("""
                    INSERT INTO articles (id, title, category, excerpt, content, image, slug, created_at) 
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                    ON CONFLICT (id) DO UPDATE SET
                    title = EXCLUDED.title,
                    category = EXCLUDED.category,
                    excerpt = EXCLUDED.excerpt,
                    content = EXCLUDED.content,
                    image = EXCLUDED.image,
                    slug = EXCLUDED.slug
                """, (
                    article['id'], article['title'], article['category'], 
                    article['excerpt'], article['content'], article.get('image', ''),
                    article.get('slug', ''), article.get('date', '2025-01-01')
                ))
        
        # Migrate subscribers
        if 'subscribers' in data:
            print(f"Migrating {len(data['subscribers'])} subscribers...")
            for sub in data['subscribers']:
                cursor.execute("""
                    INSERT INTO subscribers (id, email, firstName, lastName, created_at) 
                    VALUES (%s, %s, %s, %s, %s)
                    ON CONFLICT (email) DO UPDATE SET
                    firstName = EXCLUDED.firstName,
                    lastName = EXCLUDED.lastName
                """, (
                    sub['id'], sub['email'], sub.get('firstName', ''),
                    sub.get('lastName', ''), sub.get('date', '2025-01-01')
                ))
        
        # Migrate messages
        if 'messages' in data:
            print(f"Migrating {len(data['messages'])} messages...")
            for msg in data['messages']:
                cursor.execute("""
                    INSERT INTO messages (id, name, email, phone, company, service, budget, timeline, message, status, created_at) 
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    ON CONFLICT (id) DO UPDATE SET
                    name = EXCLUDED.name,
                    email = EXCLUDED.email,
                    phone = EXCLUDED.phone,
                    company = EXCLUDED.company,
                    service = EXCLUDED.service,
                    budget = EXCLUDED.budget,
                    timeline = EXCLUDED.timeline,
                    message = EXCLUDED.message,
                    status = EXCLUDED.status
                """, (
                    msg['id'], msg['name'], msg['email'], msg.get('phone', ''),
                    msg.get('company', ''), msg.get('service', ''), msg.get('budget', ''),
                    msg.get('timeline', ''), msg['message'], msg.get('status', 'new'),
                    msg.get('date', '2025-01-01')
                ))
        
        conn.commit()
        cursor.close()
        conn.close()
        
        print("✅ Data migration completed successfully!")
        print("Your admin dashboard should now show the data.")
        
    except Exception as e:
        print(f"❌ Migration failed: {e}")

if __name__ == "__main__":
    migrate_data()