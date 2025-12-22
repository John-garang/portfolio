import re
import os
from pathlib import Path

def diagnose_html():
    html_file = "index.html"
    
    if not os.path.exists(html_file):
        print("❌ HTML file not found!")
        return
    
    with open(html_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    print("=== HTML DIAGNOSTIC REPORT ===\n")
    
    issues = []
    fixes = []
    
    # Check document structure
    print("1. Document Structure:")
    if "<!DOCTYPE html>" in content:
        print("   [OK] DOCTYPE present")
    else:
        issues.append("Missing DOCTYPE")
    
    if "<html" in content and "</html>" in content:
        print("   [OK] HTML tags present")
    else:
        issues.append("Missing HTML tags")
    
    # Check forms
    print("\n2. Form Elements:")
    forms = re.findall(r'<form[^>]*>', content)
    for form in forms:
        if 'action=' not in form:
            issues.append(f"Form missing action: {form[:50]}...")
            fixes.append("Add action attribute to forms")
        if 'method=' not in form:
            issues.append(f"Form missing method: {form[:50]}...")
            fixes.append("Add method attribute to forms")
    
    if forms:
        print(f"   Found {len(forms)} forms")
    
    # Check scripts
    print("\n3. Script References:")
    scripts = re.findall(r'<script[^>]*src=["\']([^"\']+)["\']', content)
    for script in scripts:
        if not script.startswith('http') and not os.path.exists(script):
            issues.append(f"Missing script: {script}")
            fixes.append("Create missing script files")
        else:
            print(f"   [OK] Script: {script}")
    
    # Check images
    print("\n4. Image Paths:")
    images = re.findall(r'<img[^>]*src=["\']([^"\']+)["\']', content)
    for img in images:
        if not img.startswith('http') and not os.path.exists(img):
            issues.append(f"Missing image: {img}")
            fixes.append("Create missing image files")
        else:
            print(f"   [OK] Image: {img}")
    
    # Check links
    print("\n5. Internal Links:")
    links = re.findall(r'<a[^>]*href=["\']([^"\']+)["\']', content)
    for link in links:
        if not link.startswith(('http', 'mailto:', '#')) and not os.path.exists(link):
            issues.append(f"Broken link: {link}")
            fixes.append("Create missing HTML files")
    
    # Summary
    print(f"\n=== SUMMARY ===")
    print(f"Issues found: {len(issues)}")
    
    if issues:
        print("\nISSUES:")
        for i, issue in enumerate(issues, 1):
            print(f"{i}. {issue}")
    
    if fixes:
        print("\nFIXES NEEDED:")
        for i, fix in enumerate(set(fixes), 1):
            print(f"{i}. {fix}")
    
    if not issues:
        print("[SUCCESS] No critical issues found!")
    
    # Apply basic fixes
    if issues:
        apply_fixes(content)

def apply_fixes(content):
    print("\n=== APPLYING FIXES ===")
    
    fixed_content = content
    modified = False
    
    # Fix forms without action/method
    if '<form class="contact-form">' in content:
        fixed_content = fixed_content.replace(
            '<form class="contact-form">',
            '<form class="contact-form" action="#" method="POST">'
        )
        modified = True
        print("[FIXED] Contact form attributes")
    
    if modified:
        with open("index_fixed.html", 'w', encoding='utf-8') as f:
            f.write(fixed_content)
        print("[SAVED] Fixed HTML saved as index_fixed.html")

if __name__ == "__main__":
    diagnose_html()