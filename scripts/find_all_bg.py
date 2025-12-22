import re

with open('styles.css', 'r', encoding='utf-8') as f:
    css = f.read()

# Find ALL rules that could affect navbar background
patterns = [
    (r'nav\s*\{([^}]*background[^}]*)\}', 'nav element'),
    (r'\.navbar[^{]*\{([^}]*background[^}]*)\}', '.navbar class'),
    (r'\*\s*\{([^}]*background[^}]*)\}', 'universal selector'),
]

print("=" * 80)
print("ALL BACKGROUND RULES THAT COULD AFFECT NAVBAR")
print("=" * 80)

for pattern, desc in patterns:
    matches = re.findall(pattern, css, re.DOTALL | re.IGNORECASE)
    if matches:
        print(f"\n{desc.upper()}:")
        for i, match in enumerate(matches, 1):
            bg_lines = [line.strip() for line in match.split('\n') if 'background' in line.lower() and line.strip()]
            if bg_lines:
                print(f"  Match {i}:")
                for line in bg_lines:
                    print(f"    {line}")

# Check for any inline styles or !important
print("\n" + "=" * 80)
print("CHECKING FOR !important DECLARATIONS")
print("=" * 80)

important_matches = re.findall(r'\.navbar[^}]*\{[^}]*background[^;]*!important[^}]*\}', css, re.DOTALL)
if important_matches:
    print("FOUND !important rules:")
    for match in important_matches:
        print(f"  {match[:100]}...")
else:
    print("No !important rules found affecting navbar background")
