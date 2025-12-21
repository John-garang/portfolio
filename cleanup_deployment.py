import os
import re
from pathlib import Path

def scan_and_clean_files():
    print("SCANNING FOR     print("=" * 60)
    
    # Patterns to search for
    patterns = [
        r'        r'netlify',
        r'johngarangg\.netlify\.app',
        r'\.        r'requirements_        r'        r'netlify\.toml',
        r'\
    ]
    
    # Files to check
    file_extensions = ['.py', '.html', '.js', '.css', '.md', '.txt', '.toml', '.json']
    
    found_files = []
    
    # Scan all files
    for root, dirs, files in os.walk('.'):
        # Skip .git directory
        if '.git' in dirs:
            dirs.remove('.git')
            
        for file in files:
            if any(file.endswith(ext) for ext in file_extensions):
                file_path = Path(root) / file
                
                try:
                    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                        content = f.read()
                    
                    # Check for patterns
                    for pattern in patterns:
                        if re.search(pattern, content, re.IGNORECASE):
                            found_files.append((file_path, pattern, content))
                            print(f"FOUND: {pattern} in {file_path}")
                            break
                            
                except Exception as e:
                    print(f"Error reading {file_path}: {e}")
    
    print(f"\nFOUND {len(found_files)} FILES WITH REFERENCES")
    
    # Clean files
    print("\nCLEANING FILES...")
    cleaned_count = 0
    
    for file_path, pattern, content in found_files:
        original_content = content
        
        # Remove or replace problematic content
        replacements = [
            # Remove             (r'netlify\.toml.*?\n', ''),
            # Remove             (r'requirements_            # Replace netlify URLs with render URLs
            (r'https://johngarangg\.netlify\.app', 'https://portfolio-cmwe.onrender.com'),
            (r'johngarangg\.netlify\.app', 'portfolio-cmwe.onrender.com'),
            # Remove             (r'\.            (r'            # Remove netlify-specific files mentions
            (r'\ ''),
        ]
        
        for old_pattern, replacement in replacements:
            content = re.sub(old_pattern, replacement, content, flags=re.IGNORECASE)
        
        # Write back if changed
        if content != original_content:
            try:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                print(f"CLEANED: {file_path}")
                cleaned_count += 1
            except Exception as e:
                print(f"Error writing {file_path}: {e}")
    
    # Remove specific files that are not needed for Render
    files_to_remove = [
        '        '
        '        '    ]
    
    removed_count = 0
    for file_name in files_to_remove:
        if os.path.exists(file_name):
            try:
                os.remove(file_name)
                print(f"REMOVED: {file_name}")
                removed_count += 1
            except Exception as e:
                print(f"Error removing {file_name}: {e}")
    
    print("\n" + "=" * 60)
    print("CLEANUP SUMMARY:")
    print(f"Files cleaned: {cleaned_count}")
    print(f"Files removed: {removed_count}")
    print("All     
    return cleaned_count + removed_count > 0

if __name__ == "__main__":
    scan_and_clean_files()