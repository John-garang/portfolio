import re

with open(r"c:\John's tech projects\Portfolio\styles.css", 'r', encoding='utf-8') as f:
    content = f.read()

# Find .alu-hero block
match = re.search(r'(\.alu-hero\s*\{[^}]+\})', content, re.DOTALL)
if match:
    print("FOUND .alu-hero CSS:")
    print(match.group(1))
    print("\n" + "="*80)
    print("LINE POSITION:")
    start = match.start()
    line_num = content[:start].count('\n') + 1
    print(f"Starts at line: {line_num}")
