import json
import requests
import time

# Your admin credentials
ADMIN_USERNAME = "dengjohn200@gmail.com"
ADMIN_PASSWORD = "John@Alustudent1"
API_BASE = "https://johngarang.com"

def restore_database():
    # Load data from database.json
    with open('database.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Login to get token
    login_response = requests.post(f"{API_BASE}/api/login", json={
        "username": ADMIN_USERNAME,
        "password": ADMIN_PASSWORD
    })
    
    if login_response.status_code != 200:
        print("Login failed!")
        return
    
    token = login_response.json()['token']
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    
    # Restore articles
    if 'articles' in data:
        print(f"Restoring {len(data['articles'])} articles...")
        for article in data['articles']:
            response = requests.post(f"{API_BASE}/api/admin/articles", 
                                   json=article, headers=headers)
            if response.status_code == 201:
                print(f"✓ Added article: {article.get('title', 'Untitled')}")
            else:
                print(f"✗ Failed to add article: {article.get('title', 'Untitled')}")
            time.sleep(0.5)  # Rate limiting
    
    # Restore subscribers
    if 'subscribers' in data:
        print(f"Restoring {len(data['subscribers'])} subscribers...")
        # Note: Subscribers endpoint might need to be created for POST
        for subscriber in data['subscribers']:
            print(f"Subscriber: {subscriber.get('email', 'No email')}")
    
    # Restore messages (if any)
    if 'messages' in data:
        print(f"Found {len(data['messages'])} messages (manual restore needed)")
    
    print("Restore complete!")

if __name__ == "__main__":
    restore_database()