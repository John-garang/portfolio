import os
import re
from pathlib import Path

def analyze_and_fix_issues():
    print("ANALYZING PORTFOLIO DEPLOYMENT ISSUES...")
    print("=" * 50)
    
    # Issue 1: Check image files and fix case sensitivity
    print("\n1. CHECKING IMAGE FILES...")
    static_pics = Path("static/Pictures")
    if static_pics.exists():
        actual_files = {f.name.lower(): f.name for f in static_pics.iterdir() if f.is_file()}
        print(f"Found {len(actual_files)} image files")
        
        # Check for welcome text image
        if 'welcome text.png' in actual_files:
            print(f"FOUND: {actual_files['welcome text.png']}")
        else:
            print("MISSING: welcome text.png")
    
    # Issue 2: Fix all HTML files with incorrect paths
    print("\n2. FIXING HTML FILE PATHS...")
    templates_dir = Path("templates")
    fixed_count = 0
    
    for html_file in templates_dir.glob("*.html"):
        with open(html_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Fix image paths - case sensitive
        fixes = [
            # Fix welcome text image case
            (r'src="static/Pictures/welcome text\.png"', 'src="static/Pictures/Welcome text.png"'),
            # Fix logo in header
            (r'src="Pictures/Logo\.png"', 'src="static/Pictures/Logo.png"'),
            # Fix any remaining Pictures/ references
            (r'src="Pictures/', 'src="static/Pictures/'),
            (r"url\('Pictures/", "url('static/Pictures/"),
        ]
        
        for pattern, replacement in fixes:
            content = re.sub(pattern, replacement, content)
        
        # Remove double static/ prefixes
        content = content.replace('static/static/', 'static/')
        
        if content != original_content:
            with open(html_file, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"FIXED: {html_file.name}")
            fixed_count += 1
    
    print(f"Fixed {fixed_count} HTML files")
    
    # Issue 3: Fix load-header.js logo path
    print("\n3. FIXING LOAD-HEADER.JS...")
    header_js = Path("static/load-header.js")
    if header_js.exists():
        with open(header_js, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original = content
        # Fix logo path in JavaScript
        content = content.replace('src="Pictures/Logo.png"', 'src="static/Pictures/Logo.png"')
        
        if content != original:
            with open(header_js, 'w', encoding='utf-8') as f:
                f.write(content)
            print("FIXED: load-header.js logo path")
        else:
            print("ALREADY FIXED: load-header.js")
    
    # Issue 4: Backend CORS fix instructions
    print("\n4. BACKEND CORS ISSUE DETECTED...")
    print("CORS Error: Multiple duplicate origins in backend")
    print("\nMANUAL FIX REQUIRED:")
    print("1. Go to Render Dashboard -> portfolio-backend-1")
    print("2. Go to Environment tab")
    print("3. DELETE current ALLOWED_ORIGINS variable")
    print("4. ADD new ALLOWED_ORIGINS with value:")
    print("   https://portfolio-cmwe.onrender.com")
    
    print("\n" + "=" * 50)
    print("ISSUE SUMMARY:")
    print("=" * 50)
    print("FIXED: Image path case sensitivity")
    print("FIXED: HTML file paths") 
    print("FIXED: JavaScript logo path")
    print("MANUAL: Backend CORS configuration needed")
    
    print("\nNEXT STEPS:")
    print("1. Commit and push these fixes")
    print("2. Fix CORS in Render backend dashboard")
    print("3. Wait for both services to redeploy")
    
    return True

if __name__ == "__main__":
    try:
        analyze_and_fix_issues()
        print("\nAnalysis and fixes completed!")
    except Exception as e:
        print(f"\nError during analysis: {e}")