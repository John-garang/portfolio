import mysql.connector
import json

# Connect to MySQL
conn = mysql.connector.connect(
    host='localhost',
    user='root',
    password='John@Alustudent1',
    database='portfolio_db'
)
cursor = conn.cursor()

# Load backup data
with open('database.json.backup', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Clear existing data
cursor.execute("DELETE FROM articles")
cursor.execute("DELETE FROM messages")
cursor.execute("DELETE FROM subscribers")

# Restore articles
for article in data['articles']:
    cursor.execute("""
        INSERT INTO articles (title, category, excerpt, content, image, slug, created_at)
        VALUES (%s, %s, %s, %s, %s, %s, NOW())
    """, (article['title'], article['category'], article['excerpt'], 
          article['content'], article.get('image', ''), article['slug']))

# Restore messages
for msg in data['messages']:
    cursor.execute("""
        INSERT INTO messages (name, email, phone, company, service, budget, timeline, message, status, created_at)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, NOW())
    """, (msg['name'], msg['email'], msg.get('phone', ''), msg.get('company', ''),
          msg.get('service', ''), msg.get('budget', ''), msg.get('timeline', ''), 
          msg['message'], msg.get('status', 'new')))

# Restore subscribers
for sub in data['subscribers']:
    cursor.execute("""
        INSERT INTO subscribers (email, firstName, lastName, created_at)
        VALUES (%s, %s, %s, NOW())
    """, (sub['email'], sub.get('firstName', ''), sub.get('lastName', '')))


conn.commit()
cursor.close()
conn.close()

print("Data restored successfully!")
print(f"Articles: {len(data['articles'])}")
print(f"Messages: {len(data['messages'])}")
print(f"Subscribers: {len(data['subscribers'])}")
