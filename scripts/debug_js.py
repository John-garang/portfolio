import re

# Read the HTML file
with open('cnn-academy.html', 'r', encoding='utf-8') as f:
    html_content = f.read()

# Read the JS file
with open('load-header.js', 'r', encoding='utf-8') as f:
    js_content = f.read()

print("=" * 80)
print("CHECKING cnn-academy.html")
print("=" * 80)

# Check for hero classes
hero_classes = ['.hero', '.about', '.alu-hero', '.blog-hero', '.shelf-hero']
white_nav_classes = ['.category-hero', '.contact-hero', '.services-hero']

print("\nHero classes that should trigger transparent navbar:")
for cls in hero_classes:
    if cls.replace('.', '') in html_content:
        print(f"  [YES] Found: {cls}")
    else:
        print(f"  [NO] Not found: {cls}")

print("\nClasses that should trigger white navbar:")
for cls in white_nav_classes:
    if cls.replace('.', '') in html_content:
        print(f"  [YES] Found: {cls}")
    else:
        print(f"  [NO] Not found: {cls}")

print("\n" + "=" * 80)
print("CHECKING load-header.js LOGIC")
print("=" * 80)

# Extract the hero detection logic
hero_detection = re.search(r'const hasHero = ([^;]+);', js_content)
if hero_detection:
    print(f"\nhasHero detection: {hero_detection.group(1)}")

needs_white = re.search(r'const needsWhiteNav = ([^;]+);', js_content)
if needs_white:
    print(f"needsWhiteNav logic: {needs_white.group(1)}")

# Check if scrolled class is being removed
remove_scrolled = re.search(r'navbar\.classList\.remove\([\'"]scrolled[\'"]\)', js_content)
if remove_scrolled:
    print("\n[YES] Code to remove 'scrolled' class exists")
else:
    print("\n[NO] No code to remove 'scrolled' class found")

# Check if scrolled class is being added
add_scrolled = re.findall(r'navbar\.classList\.add\([\'"]scrolled[\'"]\)', js_content)
print(f"\nNumber of places 'scrolled' class is added: {len(add_scrolled)}")

print("\n" + "=" * 80)
print("POTENTIAL ISSUE ANALYSIS")
print("=" * 80)

# Check if header.html has scrolled class by default
with open('header.html', 'r', encoding='utf-8') as f:
    header_content = f.read()

if 'class="navbar scrolled"' in header_content or "class='navbar scrolled'" in header_content:
    print("\n[WARNING] header.html has 'scrolled' class in navbar by default!")
    print("  This would cause white background to show immediately.")
else:
    print("\n[OK] header.html navbar does not have 'scrolled' class by default")

# Check the setTimeout delay
timeout_match = re.search(r'setTimeout\([^,]+,\s*(\d+)\)', js_content)
if timeout_match:
    delay = timeout_match.group(1)
    print(f"\n[OK] setTimeout delay: {delay}ms")
    if delay == "0":
        print("  Note: 0ms delay may not be enough for DOM to be ready")
