import re

with open('styles.css', 'r', encoding='utf-8') as f:
    css = f.read()

# Find the 768px media query section
pattern = r'@media\s*\(max-width:\s*768px\)\s*\{(.*?)(?=@media|$)'
match = re.search(pattern, css, re.DOTALL)

if match:
    mobile_section = match.group(1)
    
    # Find all .navbar rules in this section
    navbar_rules = re.findall(r'(\.navbar[^{]*)\{([^}]+)\}', mobile_section, re.DOTALL)
    
    print("=" * 80)
    print("MOBILE (768px) NAVBAR CSS RULES")
    print("=" * 80)
    
    for selector, rules in navbar_rules:
        print(f"\nSelector: {selector.strip()}")
        print(f"Rules:")
        for line in rules.strip().split('\n'):
            if line.strip():
                print(f"  {line.strip()}")
        print("-" * 80)
else:
    print("No 768px media query found")
