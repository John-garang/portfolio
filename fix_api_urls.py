import os
from pathlib import Path

def fix_api_urls():
    templates_dir = Path("templates")
    backend_url = "https://portfolio-backend-1-53hz.onrender.com"
    old_url = "https://johngarangg.netlify.app"
    
    fixed_count = 0
    
    for html_file in templates_dir.glob("*.html"):
        with open(html_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        if old_url in content:
            content = content.replace(old_url, backend_url)
            
            with open(html_file, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print(f"Fixed: {html_file.name}")
            fixed_count += 1
    
    print(f"\nTotal files fixed: {fixed_count}")
    print(f"Changed all API URLs from {old_url} to {backend_url}")

if __name__ == "__main__":
    fix_api_urls()