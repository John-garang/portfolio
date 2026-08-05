import re

with open('templates/static/styles.css', 'r', encoding='utf-8') as f:
    content = f.read()

# Simple string replacements for remaining large sizes
replacements = [
    # Replace all 2.5rem with 1.5rem (section titles)
    ('font-size: 2.5rem', 'font-size: 1.5rem'),
    # Replace all 2.8rem with clamp
    ('font-size: 2.8rem', 'font-size: clamp(1.75rem, 4vw, 2.5rem)'),
    # Replace all 3rem with clamp
    ('font-size: 3rem', 'font-size: clamp(1.75rem, 4vw, 2.5rem)'),
    # Replace all 3.5rem with clamp
    ('font-size: 3.5rem', 'font-size: clamp(1.75rem, 4vw, 2.5rem)'),
]

for old, new in replacements:
    content = content.replace(old, new)

with open('templates/static/styles.css', 'w', encoding='utf-8') as f:
    f.write(content)

print('Final font size normalization complete')