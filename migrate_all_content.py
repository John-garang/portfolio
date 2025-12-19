import requests
import json

API_BASE = 'https://portfolio-backend-1-53hz.onrender.com/api'
ADMIN_USERNAME = 'dengjohn200@gmail.com'
ADMIN_PASSWORD = 'John@Alustudent1'

def get_admin_token():
    response = requests.post(f'{API_BASE}/login', json={
        'username': ADMIN_USERNAME,
        'password': ADMIN_PASSWORD
    })
    if response.status_code == 200:
        return response.json()['token']
    return None

def migrate_all_articles(token):
    articles = [
        {
            "title": "The Making of a Dinka Woman: A Survival Manual Disguised as Culture",
            "category": "personal-writings",
            "excerpt": "Even though I don't agree with feminists in most cases, we can agree on one thing; the closest living thing to a donkey isn't four-legged. It's a Dinka woman.",
            "content": "<p>A critical examination of cultural practices and their impact on women in Dinka society...</p>",
            "image": ""
        },
        {
            "title": "When an Educated Woman Says No",
            "category": "personal-writings", 
            "excerpt": "Educated women can read through you like the book you never finished.",
            "content": "<p>An exploration of the dynamics between education and relationships...</p>",
            "image": ""
        },
        {
            "title": "A First-time Traveller's Guide to Cape Town",
            "category": "travels",
            "excerpt": "My first ever trip to Cape Town, South Africa - experiences, tips, and memorable moments",
            "content": "<p>Cape Town welcomed me with open arms and stunning views...</p>",
            "image": ""
        },
        {
            "title": "Addressing Entrepreneurial Gaps in South Sudan",
            "category": "academia",
            "excerpt": "South Sudanese students, particularly from low-income backgrounds, have limited access to entrepreneurial resources such as mentorship, funding, and business training.",
            "content": "<p>An academic analysis of entrepreneurship challenges in South Sudan...</p>",
            "image": ""
        },
        {
            "title": "Development Trajectory of South Sudan",
            "category": "academia",
            "excerpt": "South Sudan, the world's youngest nation, has already had a long political history...",
            "content": "<p>A comprehensive study of South Sudan's development path...</p>",
            "image": ""
        }
    ]
    
    headers = {'Authorization': f'Bearer {token}', 'Content-Type': 'application/json'}
    
    for article in articles:
        response = requests.post(f'{API_BASE}/articles', json=article, headers=headers)
        if response.status_code == 200:
            print(f"Migrated: {article['title']}")
        else:
            print(f"Failed: {article['title']} - {response.status_code}")

def migrate_poems(token):
    poems = [
        {
            "title": "Reflections on Home",
            "excerpt": "A poem about longing for home and the memories that bind us",
            "content": "In the quiet of the evening,\nWhen the world has settled down,\nI think of home and all its meaning,\nOf the love that can be found..."
        },
        {
            "title": "The Journey Within",
            "excerpt": "An introspective piece about self-discovery and growth",
            "content": "Through valleys deep and mountains high,\nThe journey leads us to the sky,\nNot outward bound but deep within,\nWhere true adventures can begin..."
        }
    ]
    
    headers = {'Authorization': f'Bearer {token}', 'Content-Type': 'application/json'}
    
    for poem in poems:
        response = requests.post(f'{API_BASE}/poems', json=poem, headers=headers)
        if response.status_code == 200:
            print(f"Added poem: {poem['title']}")
        else:
            print(f"Failed poem: {poem['title']} - {response.status_code}")

def main():
    print("Migrating all content to database...")
    
    token = get_admin_token()
    if not token:
        print("Authentication failed")
        return
    
    print("Authentication successful")
    migrate_all_articles(token)
    migrate_poems(token)
    print("Migration complete!")

if __name__ == "__main__":
    main()