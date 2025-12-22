import re

# Read both HTML files
with open(r"c:\John's tech projects\Portfolio\unleash-innovation-lab.html", 'r', encoding='utf-8') as f:
    unleash = f.read()

with open(r"c:\John's tech projects\Portfolio\cnn-academy.html", 'r', encoding='utf-8') as f:
    cnn = f.read()

print("=" * 80)
print("COMPARISON: UNLEASH vs CNN ACADEMY")
print("=" * 80)

# Extract hero sections
unleash_hero = re.search(r'<section[^>]*class="[^"]*hero[^"]*"[^>]*>(.*?)</section>', unleash, re.DOTALL)
cnn_hero = re.search(r'<section[^>]*class="[^"]*hero[^"]*"[^>]*>(.*?)</section>', cnn, re.DOTALL)

print("\n1. HERO SECTION CLASS:")
unleash_class = re.search(r'<section[^>]*class="([^"]*)"', unleash_hero.group(0) if unleash_hero else "")
cnn_class = re.search(r'<section[^>]*class="([^"]*)"', cnn_hero.group(0) if cnn_hero else "")

print(f"   UNLEASH: {unleash_class.group(1) if unleash_class else 'NOT FOUND'}")
print(f"   CNN:     {cnn_class.group(1) if cnn_class else 'NOT FOUND'}")

# Check CSS file for both classes
with open(r"c:\John's tech projects\Portfolio\styles.css", 'r', encoding='utf-8') as f:
    css = f.read()

print("\n2. CSS DEFINITIONS:")
for cls in ['unleash-hero', 'cnn-hero']:
    pattern = f'\\.{cls}\\s*{{([^}}]*)}}'
    match = re.search(pattern, css, re.DOTALL)
    if match:
        print(f"\n   .{cls} {{")
        lines = [l.strip() for l in match.group(1).split(';') if l.strip()]
        for line in lines[:5]:
            print(f"      {line};")
        if len(lines) > 5:
            print(f"      ... ({len(lines) - 5} more)")
        print(f"   }}")
    else:
        print(f"\n   .{cls} - NOT FOUND IN CSS")

print("\n3. BACKGROUND IMAGE CHECK:")
# Check if images exist
import os
unleash_img = r"c:\John's tech projects\Portfolio\Pictures\UNLEASH Lab Heroe Photo.jpg"
cnn_img = r"c:\John's tech projects\Portfolio\Pictures\CNN ACademy Heroe image.jpg"

print(f"   UNLEASH image exists: {os.path.exists(unleash_img)}")
print(f"   CNN image exists:     {os.path.exists(cnn_img)}")

print("\n4. DIAGNOSIS:")
print("=" * 80)

if unleash_class and cnn_class:
    if unleash_class.group(1) == cnn_class.group(1):
        print("   ✗ PROBLEM: Both pages use the same class")
        print("   ✓ SOLUTION: Already fixed - UNLEASH uses 'unleash-hero', CNN uses 'cnn-hero'")
    else:
        print("   ✓ Both pages use different classes")
        
    # Check if CSS exists for both
    unleash_css_exists = bool(re.search(r'\.unleash-hero\s*\{', css))
    cnn_css_exists = bool(re.search(r'\.cnn-hero\s*\{', css))
    
    if not unleash_css_exists:
        print("   ✗ PROBLEM: .unleash-hero CSS not found")
    else:
        print("   ✓ .unleash-hero CSS exists")
        
    if not cnn_css_exists:
        print("   ✗ PROBLEM: .cnn-hero CSS not found")
    else:
        print("   ✓ .cnn-hero CSS exists")

print("\n5. NAVBAR TRANSPARENCY:")
print("   Both pages should have transparent navbar over hero background")
print("   This is controlled by .navbar { background: transparent; }")

print("=" * 80)
