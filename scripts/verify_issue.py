from bs4 import BeautifulSoup

# Read HTML
with open('cnn-academy.html', 'r', encoding='utf-8') as f:
    html = f.read()

soup = BeautifulSoup(html, 'html.parser')

print("=" * 80)
print("ELEMENTS MATCHING querySelector('.hero')")
print("=" * 80)

# Find all elements with class containing 'hero'
elements = soup.find_all(class_=lambda x: x and 'hero' in x)

for elem in elements:
    classes = elem.get('class', [])
    print(f"\nTag: <{elem.name}>")
    print(f"Classes: {classes}")
    print(f"Would match '.hero'? {any(cls == 'hero' for cls in classes)}")
    print(f"Would match '.alu-hero'? {any(cls == 'alu-hero' for cls in classes)}")
    print(f"Would match '.hero-subtitle'? {any(cls == 'hero-subtitle' for cls in classes)}")

print("\n" + "=" * 80)
print("CONCLUSION")
print("=" * 80)
print("\nThe querySelector('.hero') should ONLY match elements with class='hero'")
print("NOT elements with class='hero-subtitle' or class='alu-hero'")
print("\nHowever, if there's a <section class='hero'> somewhere, that's the issue.")

# Check for actual hero section
hero_section = soup.find('section', class_='hero')
alu_hero_section = soup.find('section', class_='alu-hero')

print(f"\n<section class='hero'> exists: {hero_section is not None}")
print(f"<section class='alu-hero'> exists: {alu_hero_section is not None}")
