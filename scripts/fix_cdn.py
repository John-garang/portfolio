import os
import re

def fix_cdn_links():
    templates_dir = "templates"
    
    # Fix broken CDN links
    patterns = [
        (r'href="static/https://', r'href="https://'),
        (r'src="static/https://', r'src="https://'),
    ]
    
    for filename in os.listdir(templates_dir):
        if filename.endswith('.html'):
            filepath = os.path.join(templates_dir, filename)
            
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Apply patterns
            for pattern, replacement in patterns:
                content = re.sub(pattern, replacement, content)
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print(f"Fixed CDN links in {filename}")

if __name__ == "__main__":
    fix_cdn_links()
    print("CDN links fixed!")