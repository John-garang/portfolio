import mysql.connector
import json
import sys

print("=== Portfolio Dashboard Diagnostic & Restore ===\n")

# Database connection
try:
    conn = mysql.connector.connect(
        host='localhost',
        user='root',
        password='John@Alustudent1',
        database='portfolio_db'
    )
    cursor = conn.cursor(dictionary=True)
    print("[OK] MySQL connection successful")
except Exception as e:
    print(f"[ERROR] MySQL connection failed: {e}")
    sys.exit(1)

# Check current data
print("\n--- Current Database Status ---")
cursor.execute("SELECT COUNT(*) as count FROM articles")
articles_count = cursor.fetchone()['count']
print(f"Articles: {articles_count}")

cursor.execute("SELECT COUNT(*) as count FROM messages")
messages_count = cursor.fetchone()['count']
print(f"Messages: {messages_count}")

cursor.execute("SELECT COUNT(*) as count FROM subscribers")
subscribers_count = cursor.fetchone()['count']
print(f"Subscribers: {subscribers_count}")

# Load backup
print("\n--- Loading Backup Data ---")
try:
    with open('database.json.backup', 'r', encoding='utf-8') as f:
        backup = json.load(f)
    print(f"[OK] Backup loaded: {len(backup['articles'])} articles, {len(backup['messages'])} messages, {len(backup['subscribers'])} subscribers")
except Exception as e:
    print(f"[ERROR] Failed to load backup: {e}")
    sys.exit(1)

# Ask user
print("\n--- Restore Options ---")
print("1. Clear and restore all data from backup")
print("2. Keep existing data (no restore)")
print("3. Exit")
choice = input("\nEnter choice (1-3): ").strip()

if choice == '1':
    print("\n--- Restoring Data ---")
    
    # Clear existing
    cursor.execute("DELETE FROM articles")
    cursor.execute("DELETE FROM messages")
    cursor.execute("DELETE FROM subscribers")
    print("[OK] Cleared existing data")
    
    # Restore articles
    for article in backup['articles']:
        cursor.execute("""
            INSERT INTO articles (title, category, excerpt, content, image, slug, created_at)
            VALUES (%s, %s, %s, %s, %s, %s, NOW())
        """, (article['title'], article['category'], article['excerpt'], 
              article['content'], article.get('image', ''), article['slug']))
    print(f"[OK] Restored {len(backup['articles'])} articles")
    
    # Restore messages
    for msg in backup['messages']:
        cursor.execute("""
            INSERT INTO messages (name, email, phone, company, service, budget, timeline, message, status, created_at)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, NOW())
        """, (msg['name'], msg['email'], msg.get('phone', ''), msg.get('company', ''),
              msg.get('service', ''), msg.get('budget', ''), msg.get('timeline', ''), 
              msg['message'], msg.get('status', 'new')))
    print(f"[OK] Restored {len(backup['messages'])} messages")
    
    # Restore subscribers
    for sub in backup['subscribers']:
        cursor.execute("""
            INSERT INTO subscribers (email, firstName, lastName, created_at)
            VALUES (%s, %s, %s, NOW())
        """, (sub['email'], sub.get('firstName', ''), sub.get('lastName', '')))
    print(f"[OK] Restored {len(backup['subscribers'])} subscribers")
    
    conn.commit()
    print("\n[SUCCESS] Data restored successfully!")

elif choice == '2':
    print("\n[INFO] No changes made")
else:
    print("\n[INFO] Exiting")

# Final status
print("\n--- Final Database Status ---")
cursor.execute("SELECT COUNT(*) as count FROM articles")
print(f"Articles: {cursor.fetchone()['count']}")
cursor.execute("SELECT COUNT(*) as count FROM messages")
print(f"Messages: {cursor.fetchone()['count']}")
cursor.execute("SELECT COUNT(*) as count FROM subscribers")
print(f"Subscribers: {cursor.fetchone()['count']}")

cursor.close()
conn.close()

print("\n=== Diagnostic Complete ===")
print("\nNext steps:")
print("1. Ensure Flask server is running: python app.py")
print("2. Login at: http://localhost:3000/admin-login.html")
print("3. Credentials: admin / JohnGarang@2024!SecureAdmin")
