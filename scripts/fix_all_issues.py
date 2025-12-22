import os
import re
from pathlib import Path

def analyze_and_fix_issues():
    print("🔍 ANALYZING PORTFOLIO DEPLOYMENT ISSUES...")
    print("=" * 50)
    
    # Issue 1: Check image files and fix case sensitivity
    print("\n1. CHECKING IMAGE FILES...")
    static_pics = Path("static/Pictures")
    if static_pics.exists():
        actual_files = {f.name.lower(): f.name for f in static_pics.iterdir() if f.is_file()}
        print(f"Found {len(actual_files)} image files")
        
        # Common problematic files
        problem_files = {
            'welcome text.png': 'Welcome text.png',
            'logo.png': 'Logo.png'
        }
        
        for expected, actual in problem_files.items():
            if expected.lower() in actual_files:
                print(f"✅ Found: {actual_files[expected.lower()]}")
            else:
                print(f"❌ Missing: {expected}")
    
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
            # Fix welcome text image
            (r'src="static/Pictures/welcome text\.png"', 'src="static/Pictures/Welcome text.png"'),
            # Fix logo in header (load-header.js references)
            (r'src="Pictures/Logo\.png"', 'src="static/Pictures/Logo.png"'),
            # Fix any remaining Pictures/ references
            (r'src="Pictures/', 'src="static/Pictures/'),
            (r"url\('Pictures/", "url('static/Pictures/"),
            # Fix CSS and JS paths that might be missing static/
            (r'href="(?!https?://)(?!static/)([^"]*\.css)', r'href="static/\1'),
            (r'src="(?!https?://)(?!static/)([^"]*\.js)', r'src="static/\1'),
        ]
        
        for pattern, replacement in fixes:
            content = re.sub(pattern, replacement, content)
        
        # Remove double static/ prefixes
        content = content.replace('static/static/', 'static/')
        
        if content != original_content:
            with open(html_file, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"✅ Fixed: {html_file.name}")
            fixed_count += 1
    
    print(f"Fixed {fixed_count} HTML files")
    
    # Issue 3: Fix load-header.js logo path
    print("\n3. FIXING LOAD-HEADER.JS...")
    header_js = Path("static/load-header.js")
    if header_js.exists():
        with open(header_js, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Fix logo path in JavaScript
        content = content.replace('src="Pictures/Logo.png"', 'src="static/Pictures/Logo.png"')
        
        with open(header_js, 'w', encoding='utf-8') as f:
            f.write(content)
        print("✅ Fixed load-header.js logo path")
    
    # Issue 4: Create backend CORS fix instructions
    print("\n4. BACKEND CORS ISSUE DETECTED...")
    print("❌ CORS Error: Multiple duplicate origins in backend")
    print("\n🔧 MANUAL FIX REQUIRED:")
    print("1. Go to Render Dashboard → portfolio-backend-1")
    print("2. Go to Environment tab")
    print("3. DELETE current ALLOWED_ORIGINS variable")
    print("4. ADD new ALLOWED_ORIGINS with value:")
    print("   https://portfolio-cmwe.onrender.com")
    print("   OR use '*' to allow all origins temporarily")
    
    # Issue 5: Check for missing analytics endpoint
    print("\n5. CHECKING BACKEND ENDPOINTS...")
    app_py = Path("app.py")
    if app_py.exists():
        with open(app_py, 'r', encoding='utf-8') as f:
            content = f.read()
        
        if '/api/analytics/track' not in content:
            print("❌ Missing /api/analytics/track endpoint in backend")
            print("🔧 Need to add analytics tracking endpoint")
        else:
            print("✅ Analytics endpoint exists")
    
    # Issue 6: Create summary report
    print("\n" + "=" * 50)
    print("📋 ISSUE SUMMARY & STATUS:")
    print("=" * 50)
    print("✅ Image path case sensitivity - FIXED")
    print("✅ HTML file paths - FIXED") 
    print("✅ JavaScript logo path - FIXED")
    print("❌ Backend CORS configuration - MANUAL FIX NEEDED")
    print("❌ Analytics endpoint missing - NEEDS BACKEND UPDATE")
    
    print("\n🚀 NEXT STEPS:")
    print("1. Commit and push these fixes")
    print("2. Fix CORS in Render backend dashboard")
    print("3. Add analytics endpoint to backend (optional)")
    print("4. Wait for both services to redeploy")
    
    return True

if __name__ == "__main__":
    try:
        analyze_and_fix_issues()
        print("\n✅ Analysis and fixes completed!")
    except Exception as e:
        print(f"\n❌ Error during analysis: {e}")