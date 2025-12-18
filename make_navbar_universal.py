import os
import glob

# Find all HTML files
html_files = glob.glob('*.html')

for filename in html_files:
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Skip if already using header placeholder
    if 'header-placeholder' in content:
        print(f"[SKIP] {filename} - already using dynamic header")
        continue
    
    # Check if has navigation
    if '<nav' not in content.lower():
        print(f"[SKIP] {filename} - no navigation found")
        continue
    
    # Replace hardcoded navigation with placeholder
    # Find the nav section (from <nav to </nav>)
    import re
    nav_pattern = r'<nav[^>]*>.*?</nav>'
    
    if re.search(nav_pattern, content, re.DOTALL):
        # Replace with placeholder
        new_content = re.sub(
            nav_pattern,
            '<!-- Header Placeholder -->\n    <div id="header-placeholder"></div>\n    <script src="load-header.js"></script>',
            content,
            count=1,
            flags=re.DOTALL
        )
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        print(f"[UPDATED] {filename}")
    else:
        print(f"[SKIP] {filename} - nav pattern not found")

print("\nDone! All pages now use universal header.")
