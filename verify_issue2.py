import re

# Read HTML
with open('cnn-academy.html', 'r', encoding='utf-8') as f:
    html = f.read()

print("=" * 80)
print("SEARCHING FOR HERO CLASSES IN cnn-academy.html")
print("=" * 80)

# Find all class attributes
class_pattern = r'class=["\']([^"\']+)["\']'
matches = re.findall(class_pattern, html)

hero_related = [m for m in matches if 'hero' in m.lower()]

print("\nAll classes containing 'hero':")
for cls in hero_related:
    print(f"  - {cls}")

# Check for specific hero sections
print("\n" + "=" * 80)
print("CHECKING FOR SPECIFIC HERO SECTIONS")
print("=" * 80)

hero_checks = [
    ('alu-hero', r'<section[^>]+class=["\'][^"\']*alu-hero[^"\']*["\']'),
    ('hero (exact)', r'<section[^>]+class=["\']hero["\']'),
    ('about', r'<section[^>]+class=["\'][^"\']*about[^"\']*["\']'),
]

for name, pattern in hero_checks:
    match = re.search(pattern, html)
    if match:
        print(f"\n[FOUND] {name}")
        print(f"  {match.group(0)[:100]}...")
    else:
        print(f"\n[NOT FOUND] {name}")

# The real test: what would querySelector actually match?
print("\n" + "=" * 80)
print("WHAT querySelector('.hero') WOULD MATCH")
print("=" * 80)
print("\nIn JavaScript, querySelector('.hero') matches elements with class='hero' EXACTLY")
print("It does NOT match 'hero-subtitle' or 'alu-hero'")
print("\nLet's check if there's a standalone 'hero' class:")

# More precise check
standalone_hero = re.search(r'class=["\']hero["\']', html)
if standalone_hero:
    print("\n[ISSUE FOUND] There IS an element with class='hero' (standalone)")
    print(f"  {standalone_hero.group(0)}")
else:
    print("\n[OK] No standalone class='hero' found")
    print("The querySelector('.hero') should NOT match anything in this file")
