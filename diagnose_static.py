import os
import requests

# Check local file exists
image_path = "static/Pictures/About me picture.jpg"
print(f"Local file exists: {os.path.exists(image_path)}")
if os.path.exists(image_path):
    print(f"File size: {os.path.getsize(image_path)} bytes")

# Check remote URLs
urls = [
    "https://johngarang.com/static/Pictures/About%20me%20picture.jpg",
    "https://johngarang.com/about",
    "https://johngarang.com/"
]

for url in urls:
    try:
        response = requests.get(url, timeout=10)
        print(f"{url}: {response.status_code}")
        if response.status_code != 200:
            print(f"  Error: {response.text[:200]}")
    except Exception as e:
        print(f"{url}: ERROR - {e}")