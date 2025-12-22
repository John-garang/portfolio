import re

# Read the CSS file
with open('styles.css', 'r', encoding='utf-8') as f:
    css_content = f.read()

# Find all navbar-related background rules
print("=" * 80)
print("NAVBAR BACKGROUND RULES ANALYSIS")
print("=" * 80)

# Split CSS into sections by media queries
sections = re.split(r'(@media[^{]+\{)', css_content)

current_media = "DEFAULT (No Media Query)"
for i, section in enumerate(sections):
    if section.strip().startswith('@media'):
        current_media = section.strip()
        continue
    
    # Find navbar rules with background in this section
    navbar_rules = re.finditer(r'(\.navbar[^{]*)\{([^}]+)\}', section, re.DOTALL)
    
    for match in navbar_rules:
        selector = match.group(1).strip()
        rules = match.group(2).strip()
        
        # Check if this rule contains background
        if 'background' in rules.lower():
            print(f"\n{current_media}")
            print(f"Selector: {selector}")
            print(f"Rules: {rules[:200]}...")
            print("-" * 80)

# Check for any !important rules
print("\n" + "=" * 80)
print("CHECKING FOR !important OVERRIDES")
print("=" * 80)
important_rules = re.findall(r'\.navbar[^{]*\{[^}]*background[^;]*!important[^}]*\}', css_content, re.DOTALL)
if important_rules:
    for rule in important_rules:
        print(rule)
else:
    print("No !important rules found")

# Check the specific order of navbar rules
print("\n" + "=" * 80)
print("ORDER OF NAVBAR BACKGROUND DECLARATIONS")
print("=" * 80)

navbar_bg_pattern = r'(\.navbar[^{]*)\{([^}]*background[^}]*)\}'
matches = list(re.finditer(navbar_bg_pattern, css_content, re.DOTALL))

for idx, match in enumerate(matches, 1):
    selector = match.group(1).strip()
    bg_line = [line for line in match.group(2).split('\n') if 'background' in line.lower()]
    print(f"\n{idx}. Position in file: char {match.start()}")
    print(f"   Selector: {selector}")
    for line in bg_line:
        print(f"   {line.strip()}")
