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

def restore_sample_data():
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()
        
        print("Restoring sample data...")
        
        # Add sample articles
        articles = [
            (1, "When an Educated Woman Says No", "personal-writings", 
             "Educated women can read through you like the book you never finished.", 
             "I can't date an educated woman...", "When an Educated Woman Says No.jpg"),
            (2, "The Making of a Dinka Woman", "personal-writings",
             "Even though I don't agree with feminists in most cases, we can agree on one thing; the closest living thing to a donkey isn't four-legged. It's a Dinka woman.",
             "Let's unpack this, shall we?...", "The Making of a Dinka Woman.jpg"),
            (3, "Addressing Entrepreneurial Gaps in South Sudan", "academia",
             "South Sudanese students, particularly from low-income backgrounds, have limited access to entrepreneurial resources.",
             "This limits their ability to scale their ideas and sustain their businesses...", ""),
            (4, "If Equality Means This, Burn the World Already", "personal-writings",
             "When violence wears a skirt and puts on lipstick, it suddenly becomes excused.",
             "Today in Aweil, Northern Bahr El Ghazal, South Sudan...", "If Equality Means This.jpg")
        ]
        
        for article in articles:
            cursor.execute("""
                INSERT INTO articles (id, title, category, excerpt, content, image) 
                VALUES (%s, %s, %s, %s, %s, %s)
                ON CONFLICT (id) DO UPDATE SET
                title = EXCLUDED.title,
                category = EXCLUDED.category,
                excerpt = EXCLUDED.excerpt,
                content = EXCLUDED.content,
                image = EXCLUDED.image
            """, article)
        
        # Add sample subscribers
        subscribers = [
            (1, "j.garang@alustudent.com", "John", "Garang"),
            (2, "ataakdengg@gmail.com", "John", "Garang"),
            (3, "socialmedia@spp.org.za", "John Ngor Deng", "Garang")
        ]
        
        for sub in subscribers:
            cursor.execute("""
                INSERT INTO subscribers (id, email, firstName, lastName) 
                VALUES (%s, %s, %s, %s)
                ON CONFLICT (email) DO UPDATE SET
                firstName = EXCLUDED.firstName,
                lastName = EXCLUDED.lastName
            """, sub)
        
        # Add sample message
        cursor.execute("""
            INSERT INTO messages (id, name, email, phone, company, service, budget, timeline, message, status) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (id) DO UPDATE SET
            name = EXCLUDED.name,
            email = EXCLUDED.email,
            message = EXCLUDED.message,
            status = EXCLUDED.status
        """, (1, "John Garang", "j.garang@alustudent.com", "", "Education Bridge", 
              "consultation", "under-1000", "asap", "Test message", "new"))
        
        conn.commit()
        cursor.close()
        conn.close()
        
        print("Data restored successfully!")
        print("Your admin dashboard should now show the data.")
        
    except Exception as e:
        print(f"Restore failed: {e}")

if __name__ == "__main__":
    restore_sample_data()