import requests

# Test Flask's static file endpoint
test_url = "https://johngarang.com/static/Pictures/Logo.png"
response = requests.get(test_url)
print(f"Logo test: {response.status_code}")

# List what's in static folder
import os
static_path = "static/Pictures"
if os.path.exists(static_path):
    files = os.listdir(static_path)
    print(f"Files in {static_path}:")
    for f in files[:10]:  # First 10 files
        if "About" in f:
            print(f"  FOUND: {f}")
        else:
            print(f"  {f}")