import requests

# Your admin credentials
ADMIN_USERNAME = "dengjohn200@gmail.com"
ADMIN_PASSWORD = "John@Alustudent1"
API_BASE = "https://johngarang.com"

# Articles extracted from database.json
articles = [
    {
        "title": "When an Educated Woman Says No nm",
        "category": "personal-writings",
        "excerpt": "bnm",
        "content": "hjk"
    },
    {
        "title": "Addressing Entrepreneurial Gaps in South Sudan",
        "category": "academia",
        "excerpt": "South Sudanese students, particularly from low-income backgrounds, have limited access to entrepreneurial resources such as mentorship, funding, and business training.",
        "content": "This limits their ability to scale their ideas and sustain their businesses, exacerbating unemployment and poverty nationwide..."
    },
    {
        "title": "The Making of a Dinka Woman: A Survival Manual Disguised as Culture",
        "category": "personal-writings",
        "excerpt": "Even though I don't agree with feminists in most cases, we can agree on one thing; the closest living thing to a donkey isn't four-legged. It's a Dinka woman.",
        "content": "Let's unpack this, shall we?..."
    },
    {
        "title": "When an Educated Woman Says No",
        "category": "personal-writings",
        "excerpt": "Educated women can read through you like the book you never finished.",
        "content": "I can't date an educated woman..."
    },
    {
        "title": "If Equality Means This, Burn the World Already",
        "category": "personal-writings",
        "excerpt": "When violence wears a skirt and puts on lipstick, it suddenly becomes excused.",
        "content": "Today in Aweil, Northern Bahr El Ghazal, South Sudan..."
    }
]

def restore_articles():
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
    print(f"Restoring {len(articles)} articles...")
    for article in articles:
        response = requests.post(f"{API_BASE}/api/admin/articles", 
                               json=article, headers=headers)
        if response.status_code == 201:
            print(f"✓ Added: {article['title']}")
        else:
            print(f"✗ Failed: {article['title']} - {response.status_code}")
    
    print("Articles restored! Check your admin dashboard.")

if __name__ == "__main__":
    restore_articles()