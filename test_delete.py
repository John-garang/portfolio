import requests
import json

# Test DELETE endpoint
article_id = 1766068053808

print("Testing DELETE request...")
print(f"URL: http://localhost:3000/api/articles/{article_id}")

try:
    response = requests.delete(f"http://localhost:3000/api/articles/{article_id}")
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.text}")
    
    if response.status_code == 200:
        print("✓ DELETE request successful")
    else:
        print("✗ DELETE request failed")
        
except Exception as e:
    print(f"✗ Error: {e}")
