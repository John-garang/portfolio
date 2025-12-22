import os
import re

# Read the HTML file
with open(r"c:\John's tech projects\Portfolio\unleash-innovation-lab.html", 'r', encoding='utf-8') as f:
    html_content = f.read()

# Read the CSS file
with open(r"c:\John's tech projects\Portfolio\styles.css", 'r', encoding='utf-8') as f:
    css_content = f.read()

print("=" * 80)
print("UNLEASH INNOVATION LAB BACKGROUND IMAGE DIAGNOSIS")
print("=" * 80)

# 1. Check if image file exists
image_path = r"c:\John's tech projects\Portfolio\Pictures\UNLEASH Lab Heroe Photo.jpg"
print(f"\n1. IMAGE FILE CHECK:")
print(f"   Path: {image_path}")
print(f"   Exists: {os.path.exists(image_path)}")
if os.path.exists(image_path):
    print(f"   Size: {os.path.getsize(image_path):,} bytes")

# 2. Extract hero section from HTML
print(f"\n2. HERO SECTION IN HTML:")
hero_match = re.search(r'<section[^>]*class="[^"]*hero[^"]*"[^>]*>(.*?)</section>', html_content, re.DOTALL)
if hero_match:
    hero_section = hero_match.group(0)
    print(f"   Found hero section ({len(hero_section)} chars)")
    
    # Check for inline styles
    inline_style = re.search(r'style="([^"]*)"', hero_section)
    if inline_style:
        print(f"\n   INLINE STYLES FOUND:")
        styles = inline_style.group(1).split(';')
        for style in styles:
            if style.strip():
                print(f"      {style.strip()}")
    else:
        print(f"   No inline styles found")
    
    # Check class names
    class_match = re.search(r'class="([^"]*)"', hero_section)
    if class_match:
        classes = class_match.group(1).split()
        print(f"\n   CLASSES: {', '.join(classes)}")

# 3. Check CSS for hero classes
print(f"\n3. CSS RULES FOR HERO CLASSES:")
hero_patterns = ['.hero', '.alu-hero', '.about']
for pattern in hero_patterns:
    # Find CSS rule
    css_pattern = re.escape(pattern) + r'\s*\{([^}]*)\}'
    matches = re.findall(css_pattern, css_content)
    if matches:
        print(f"\n   {pattern} {{")
        for match in matches:
            lines = [line.strip() for line in match.split(';') if line.strip()]
            for line in lines[:10]:  # Show first 10 properties
                if 'background' in line.lower():
                    print(f"      {line};  <-- BACKGROUND PROPERTY")
                else:
                    print(f"      {line};")
            if len(lines) > 10:
                print(f"      ... ({len(lines) - 10} more properties)")
        print(f"   }}")

# 4. Check for conflicting styles
print(f"\n4. POTENTIAL CONFLICTS:")
conflicts = []

# Check if there are multiple background definitions
bg_in_inline = 'background' in hero_section if hero_match else False
bg_in_css = any([re.search(r'\.hero\s*\{[^}]*background', css_content), 
                re.search(r'\.alu-hero\s*\{[^}]*background', css_content)])

if bg_in_inline and bg_in_css:
    conflicts.append("Both inline and CSS background definitions found")

# Check for !important in CSS
important_matches = re.findall(r'(background[^;]*!important)', css_content)
if important_matches:
    conflicts.append(f"Found {len(important_matches)} !important declarations in CSS")

if conflicts:
    for conflict in conflicts:
        print(f"   - {conflict}")
else:
    print(f"   No obvious conflicts detected")

# 5. Compare with working page (about.html)
print(f"\n5. COMPARISON WITH WORKING PAGE (about.html):")
with open(r"c:\John's tech projects\Portfolio\about.html", 'r', encoding='utf-8') as f:
    about_content = f.read()

about_hero = re.search(r'<section[^>]*class="[^"]*about[^"]*"[^>]*>(.*?)</section>', about_content, re.DOTALL)
if about_hero:
    about_section = about_hero.group(0)
    about_class = re.search(r'class="([^"]*)"', about_section)
    about_inline = re.search(r'style="([^"]*)"', about_section)
    
    print(f"   about.html uses class: {about_class.group(1) if about_class else 'N/A'}")
    print(f"   about.html has inline styles: {bool(about_inline)}")

# 6. Recommendation
print(f"\n6. DIAGNOSIS & RECOMMENDATION:")
print("=" * 80)

if hero_match:
    if 'style=' in hero_section and 'background-image' in hero_section:
        if '!important' in hero_section:
            print("   ✓ Inline background-image with !important found")
            print("   ✗ ISSUE: CSS may still be overriding or image path is wrong")
            print("\n   SOLUTION:")
            print("   - Remove ALL background properties from .hero in CSS")
            print("   - Keep only inline styles on the section element")
        else:
            print("   ✗ ISSUE: Inline background without !important")
            print("\n   SOLUTION:")
            print("   - Add !important to all background properties in inline style")
    else:
        print("   ✗ ISSUE: No inline background-image found")
        print("\n   SOLUTION:")
        print("   - Add inline style with background-image to section element")
else:
    print("   ✗ CRITICAL: No hero section found in HTML")

print("=" * 80)
