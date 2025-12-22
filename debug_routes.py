import requests

def debug_routes():
    base_url = "https://portfolio-backend-1-53hz.onrender.com"
    
    routes_to_test = [
        "/",
        "/api/test",
        "/api/articles",
        "/api/articles/6",
        "/api/poems", 
        "/api/poems/6",
        "/api/comments/6"
    ]
    
    print("Testing all routes...")
    print("=" * 50)
    
    for route in routes_to_test:
        try:
            response = requests.get(f"{base_url}{route}")
            print(f"{route}: {response.status_code}")
            if response.status_code == 404:
                print(f"  Error: {response.text[:100]}...")
            elif response.status_code == 200:
                try:
                    data = response.json()
                    if isinstance(data, list):
                        print(f"  Success: {len(data)} items")
                    else:
                        print(f"  Success: {list(data.keys())}")
                except:
                    print(f"  Success: {response.text[:50]}...")
        except Exception as e:
            print(f"{route}: ERROR - {e}")
        print()

if __name__ == "__main__":
    debug_routes()