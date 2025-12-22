import json
import requests

# Your admin credentials
ADMIN_USERNAME = "dengjohn200@gmail.com"
ADMIN_PASSWORD = "John@Alustudent1"
API_BASE = "https://johngarang.com"

def restore_data():
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
            # Clean article data for API
            clean_article = {
                'title': article.get('title', ''),
                'category': article.get('category', ''),
                'excerpt': article.get('excerpt', ''),
                'content': article.get('content', '')
            }
            
            response = requests.post(f"{API_BASE}/api/admin/articles", 
                                   json=clean_article, headers=headers)
            if response.status_code == 201:
                print(f"✓ Added: {article.get('title', 'Untitled')}")
            else:
                print(f"✗ Failed: {article.get('title', 'Untitled')} - {response.status_code}")
    
    print("Restore complete! Check your admin dashboard.")

if __name__ == "__main__":
    restore_data()