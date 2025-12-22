import os
import re

def fix_localhost_urls(file_path):
    """Fix localhost URLs in a file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Replace localhost:3000 with Render backend URL
        content = re.sub(r'http://localhost:3000', 'https://portfolio-backend-1-53hz.onrender.com', content)
        content = re.sub(r'localhost:3000', 'portfolio-backend-1-53hz.onrender.com', content)
        
        # Replace any other localhost variations with Render backend
        content = re.sub(r'http://localhost(?::\d+)?', 'https://portfolio-backend-1-53hz.onrender.com', content)
        content = re.sub(r'localhost(?::\d+)?(?!/)', 'portfolio-backend-1-53hz.onrender.com', content)
        
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            return True
        return False
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return False

def scan_and_fix():
    """Scan all files and fix localhost URLs"""
    portfolio_dir = r"g:\My Drive\John's tech projects\Portfolio"
    updated_files = []
    
    # File extensions to check
    extensions = ['.html', '.js', '.css', '.json', '.md', '.txt']
    
    for root, dirs, files in os.walk(portfolio_dir):
        # Skip node_modules and other build directories
        dirs[:] = [d for d in dirs if d not in ['node_modules', '.git', 'dist', 'build']]
        
        for file in files:
            if any(file.endswith(ext) for ext in extensions):
                file_path = os.path.join(root, file)
                if fix_localhost_urls(file_path):
                    updated_files.append(file_path)
    
    print(f"Updated {len(updated_files)} files:")
    for file_path in updated_files:
        print(f"  - {os.path.relpath(file_path, portfolio_dir)}")

if __name__ == "__main__":
    scan_and_fix()