import os
import re

def fix_paths_in_html():
    templates_dir = "templates"
    
    # Patterns to replace
    patterns = [
        (r'href="([^"]*\.css)', r'href="static/\1'),
        (r'src="([^"]*\.js)', r'src="static/\1'),
        (r'src="Pictures/', r'src="static/Pictures/'),
        (r"url\('Pictures/", r"url('static/Pictures/"),
        (r'href="styles\.css"', r'href="static/styles.css"'),
        (r'src="script\.js"', r'src="static/script.js"'),
        (r'src="load-', r'src="static/load-'),
        (r'src="popup-', r'src="static/popup-'),
        (r'src="analytics\.js"', r'src="static/analytics.js"'),
        (r'src="config\.js"', r'src="static/config.js"'),
    ]
    
    for filename in os.listdir(templates_dir):
        if filename.endswith('.html'):
            filepath = os.path.join(templates_dir, filename)
            
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Apply all patterns
            for pattern, replacement in patterns:
                content = re.sub(pattern, replacement, content)
            
            # Avoid double static/ prefixes
            content = content.replace('static/static/', 'static/')
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print(f"Fixed paths in {filename}")

if __name__ == "__main__":
    fix_paths_in_html()
    print("All HTML files updated!")