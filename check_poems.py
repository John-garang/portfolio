import requests
import json

def check_poems():
    base_url = "https://portfolio-backend-1-53hz.onrender.com"
    
    print("Checking Available Poems...")
    print("=" * 30)
    
    # Get all poems
    try:
        response = requests.get(f"{base_url}/api/poems")
        if response.status_code == 200:
            poems = response.json()
            print(f"Found {len(poems)} poems:")
            for poem in poems:
                print(f"ID: {poem['id']}, Title: {poem['title']}")
                
                # Test individual poem endpoint
                print(f"\nTesting poem ID {poem['id']}:")
                poem_response = requests.get(f"{base_url}/api/poems/{poem['id']}")
                print(f"Status: {poem_response.status_code}")
                if poem_response.status_code != 200:
                    print(f"Error: {poem_response.text[:100]}...")
                
                # Test comments for this poem
                print(f"Testing comments for poem ID {poem['id']}:")
                comments_response = requests.get(f"{base_url}/api/comments/{poem['id']}")
                print(f"Comments Status: {comments_response.status_code}")
                if comments_response.status_code != 200:
                    print(f"Comments Error: {comments_response.text[:100]}...")
                print("-" * 30)
        else:
            print(f"Error getting poems: {response.text}")
    except Exception as e:
        print(f"Exception: {e}")

if __name__ == "__main__":
    check_poems()