import requests
import json

def test_endpoints():
    base_url = "https://portfolio-backend-1-53hz.onrender.com"
    
    print("Testing Backend API Endpoints...")
    print("=" * 50)
    
    # Test articles endpoint
    print("\n1. Testing Articles Endpoint:")
    try:
        response = requests.get(f"{base_url}/api/articles")
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            articles = response.json()
            print(f"Found {len(articles)} articles")
            if articles:
                print(f"First article: {articles[0]['title']}")
        else:
            print(f"Error: {response.text}")
    except Exception as e:
        print(f"Exception: {e}")
    
    # Test poems endpoint
    print("\n2. Testing Poems Endpoint:")
    try:
        response = requests.get(f"{base_url}/api/poems")
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            poems = response.json()
            print(f"Found {len(poems)} poems")
            if poems:
                print(f"First poem: {poems[0]['title']}")
        else:
            print(f"Error: {response.text}")
    except Exception as e:
        print(f"Exception: {e}")
    
    # Test specific poem endpoint
    print("\n3. Testing Specific Poem (ID: 9):")
    try:
        response = requests.get(f"{base_url}/api/poems/9")
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            poem = response.json()
            print(f"Poem title: {poem['title']}")
        else:
            print(f"Error: {response.text}")
    except Exception as e:
        print(f"Exception: {e}")
    
    # Test comments endpoint
    print("\n4. Testing Comments Endpoint (Poem ID: 9):")
    try:
        response = requests.get(f"{base_url}/api/comments/9")
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            comments = response.json()
            print(f"Found {len(comments)} comments")
        else:
            print(f"Error: {response.text}")
    except Exception as e:
        print(f"Exception: {e}")
    
    # Test root endpoint
    print("\n5. Testing Root Endpoint:")
    try:
        response = requests.get(f"{base_url}/")
        print(f"Status: {response.status_code}")
        print(f"Response: {response.text}")
    except Exception as e:
        print(f"Exception: {e}")

if __name__ == "__main__":
    test_endpoints()