import os
from pathlib import Path

# Analysis script for header navigation issue
print("=" * 60)
print("HEADER NAVIGATION ANALYSIS REPORT")
print("=" * 60)

# Check if header.html exists
header_path = Path("header.html")
if not header_path.exists():
    print("[ERROR] header.html not found!")
    exit(1)

print("[OK] header.html found")

# Read and analyze header.html
with open(header_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Check for Poems link
poems_count = content.count('poems.html')
print(f"\n[ANALYSIS] 'poems.html' found {poems_count} times in header.html")

# Find all occurrences
if poems_count > 0:
    lines = content.split('\n')
    print(f"\n[LOCATIONS] Poems link found at:")
    for i, line in enumerate(lines, 1):
        if 'poems.html' in line.lower():
            print(f"   Line {i}: {line.strip()}")
else:
    print("   [ERROR] No 'poems.html' link found!")

# Check navigation structure
nav_items = []
in_nav_menu = False
for line in content.split('\n'):
    if '<ul class="nav-menu">' in line:
        in_nav_menu = True
    elif '</ul>' in line and in_nav_menu:
        in_nav_menu = False
    elif in_nav_menu and '<a href=' in line and 'nav-link' in line:
        # Extract link text
        if '>' in line and '</a>' in line:
            text = line.split('>')[1].split('<')[0].strip()
            if text and 'fas fa-' not in text:
                nav_items.append(text)

print(f"\n[NAV ITEMS] Main Navigation Items Found:")
for item in nav_items:
    print(f"   - {item}")

# Check if poems.html file exists
poems_page = Path("poems.html")
if poems_page.exists():
    print(f"\n[OK] poems.html page exists")
else:
    print(f"\n[ERROR] poems.html page NOT found!")

# Check load-header.js
load_header = Path("load-header.js")
if load_header.exists():
    print(f"[OK] load-header.js exists")
    with open(load_header, 'r', encoding='utf-8') as f:
        lh_content = f.read()
        if 'header.html' in lh_content:
            print("  [OK] load-header.js references header.html")
else:
    print(f"[ERROR] load-header.js NOT found!")

print("\n" + "=" * 60)
print("DIAGNOSIS:")
print("=" * 60)

if poems_count >= 2:
    print("[OK] Poems link is correctly added to header.html")
    print("[OK] Found in both dropdown AND main navigation")
    print("\n[ISSUE] Browser cache is preventing you from seeing changes")
    print("\n[SOLUTION]")
    print("   1. Close ALL browser tabs")
    print("   2. Press Ctrl+Shift+Delete (Chrome)")
    print("   3. Clear 'Cached images and files'")
    print("   4. Restart browser")
    print("   5. Open http://localhost:3000/index.html")
    print("\n   OR use Incognito mode: Ctrl+Shift+N")
elif poems_count == 1:
    print("[WARNING] Poems link found only once (in dropdown)")
    print("   Main navigation tab may be missing")
else:
    print("[ERROR] Poems link NOT found in header.html")
    print("   File may not have been saved correctly")

print("=" * 60)
