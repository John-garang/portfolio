import re

print("=" * 80)
print("FULL DIAGNOSTIC FOR NAVBAR TRANSPARENCY ISSUE")
print("=" * 80)

# 1. Check load-header.js setTimeout value
with open('load-header.js', 'r', encoding='utf-8') as f:
    js = f.read()

timeout_match = re.search(r'setTimeout\([^,]+,\s*(\d+)\)', js)
print(f"\n1. setTimeout delay: {timeout_match.group(1) if timeout_match else 'NOT FOUND'}ms")

# 2. Check if the logic correctly identifies hero pages
hasHero_line = re.search(r'const hasHero = ([^;]+);', js)
needsWhite_line = re.search(r'const needsWhiteNav = ([^;]+);', js)

print(f"\n2. Hero detection logic:")
print(f"   hasHero = {hasHero_line.group(1) if hasHero_line else 'NOT FOUND'}")
print(f"   needsWhiteNav = {needsWhite_line.group(1) if needsWhite_line else 'NOT FOUND'}")

# 3. Check CSS for navbar background rules
with open('styles.css', 'r', encoding='utf-8') as f:
    css = f.read()

# Find the default navbar background
default_bg = re.search(r'\.navbar\s*\{[^}]*background:\s*([^;]+);', css)
print(f"\n3. Default .navbar background: {default_bg.group(1) if default_bg else 'NOT FOUND'}")

# Find scrolled navbar background
scrolled_bg = re.search(r'\.navbar\.scrolled\s*\{[^}]*background:\s*([^;]+);', css)
print(f"   .navbar.scrolled background: {scrolled_bg.group(1) if scrolled_bg else 'NOT FOUND'}")

# 4. Check for media query overrides
media_queries = re.findall(r'@media\s*\([^)]+\)\s*\{[^}]*\.navbar[^}]*background[^}]*\}', css, re.DOTALL)
print(f"\n4. Media queries affecting navbar background: {len(media_queries)}")

# Find the specific 768px media query
mobile_media = re.search(r'@media\s*\(max-width:\s*768px\)\s*\{(.*?)(?=@media|$)', css, re.DOTALL)
if mobile_media:
    mobile_content = mobile_media.group(1)
    # Check for navbar rules in mobile
    mobile_navbar = re.search(r'\.navbar\s*\{([^}]+)\}', mobile_content)
    if mobile_navbar:
        rules = mobile_navbar.group(1)
        if 'background' in rules:
            bg_match = re.search(r'background:\s*([^;]+);', rules)
            print(f"   Mobile (768px) .navbar background: {bg_match.group(1) if bg_match else 'FOUND BUT CANT PARSE'}")
        else:
            print(f"   Mobile (768px) .navbar: NO background property")
    
    # Check for .navbar.scrolled in mobile
    mobile_scrolled = re.search(r'\.navbar\.scrolled\s*\{([^}]+)\}', mobile_content)
    if mobile_scrolled:
        rules = mobile_scrolled.group(1)
        if 'background' in rules:
            bg_match = re.search(r'background:\s*([^;]+);', rules)
            print(f"   Mobile (768px) .navbar.scrolled background: {bg_match.group(1) if bg_match else 'FOUND BUT CANT PARSE'}")

# 5. Check cnn-academy.html structure
with open('cnn-academy.html', 'r', encoding='utf-8') as f:
    html = f.read()

has_alu_hero = bool(re.search(r'class=["\']alu-hero["\']', html))
has_header_placeholder = bool(re.search(r'<div id=["\']header-placeholder["\']', html))
loads_header_js = bool(re.search(r'<script src=["\']load-header\.js["\']', html))

print(f"\n5. cnn-academy.html structure:")
print(f"   Has .alu-hero section: {has_alu_hero}")
print(f"   Has header-placeholder div: {has_header_placeholder}")
print(f"   Loads load-header.js: {loads_header_js}")

# 6. Final diagnosis
print("\n" + "=" * 80)
print("DIAGNOSIS")
print("=" * 80)

issues = []

if timeout_match and timeout_match.group(1) == "0":
    issues.append("setTimeout delay is 0ms - may be too fast")

if not has_alu_hero:
    issues.append("cnn-academy.html missing .alu-hero section")

if not has_header_placeholder or not loads_header_js:
    issues.append("cnn-academy.html not properly set up for dynamic header")

# Check if mobile CSS has background
if mobile_navbar and 'background' in mobile_navbar.group(1):
    issues.append("Mobile CSS (.navbar) has background property - should be removed")

if issues:
    print("\nISSUES FOUND:")
    for i, issue in enumerate(issues, 1):
        print(f"  {i}. {issue}")
else:
    print("\nNo obvious issues found in code.")
    print("Possible causes:")
    print("  - Browser cache (try Ctrl+Shift+R)")
    print("  - JavaScript not executing (check browser console)")
    print("  - Timing issue (increase setTimeout delay)")
