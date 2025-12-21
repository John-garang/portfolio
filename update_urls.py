import os
import re

def update_urls_in_file(file_path):
    """Update localhost URLs to Netlify URL in a single file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Replace localhost:3000 with Netlify URL
        content = re.sub(r'http://localhost:3000', 'https://portfolio-cmwe.onrender.com', content)
        content = re.sub(r'localhost:3000', 'portfolio-cmwe.onrender.com', content)
        
        # Replace any other localhost variations
        content = re.sub(r'http://localhost', 'https://portfolio-cmwe.onrender.com', content)
        content = re.sub(r'localhost', 'portfolio-cmwe.onrender.com', content)
        
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            return True
        return False
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return False

def scan_and_update():
    """Scan all HTML and CSS files and update URLs"""
    portfolio_dir = r"g:\My Drive\John's tech projects\Portfolio"
    updated_files = []
    
    for root, dirs, files in os.walk(portfolio_dir):
        for file in files:
            if file.endswith(('.html', '.css')):
                file_path = os.path.join(root, file)
                if update_urls_in_file(file_path):
                    updated_files.append(file_path)
    
    print(f"Updated {len(updated_files)} files:")
    for file_path in updated_files:
        print(f"  - {os.path.relpath(file_path, portfolio_dir)}")

if __name__ == "__main__":
    scan_and_update()