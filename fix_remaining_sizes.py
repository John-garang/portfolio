import re

with open('templates/static/styles.css', 'r', encoding='utf-8') as f:
    content = f.read()

# Targeted fixes for remaining oversized elements
fixes = [
    # Stat numbers - reduce from 2rem to 1.75rem
    (r'\.stat-number\s*\{\s*\n\s*font-size:\s*2rem', '.stat-number {\n    font-size: 1.75rem'),
    
    # Section titles - reduce from 2.5rem to 1.5rem
    (r'\.section-title\s*\{\s*\n\s*font-size:\s*2\.5rem', '.section-title {\n    font-size: 1.5rem'),
    
    # Featured article h3 - reduce from 1.5rem to 1.2rem
    (r'\.featured-article\s+h3\s*\{\s*\n\s*font-size:\s*1\.5rem', '.featured-article h3 {\n    font-size: 1.2rem'),
    
    # Welcome intro h3 - reduce from 1.5rem to 1.2rem
    (r'\.welcome-intro\s+h3\s*\{\s*\n\s*font-size:\s*1\.5rem', '.welcome-intro h3 {\n    font-size: 1.2rem'),
]

for pattern, replacement in fixes:
    content = re.sub(pattern, replacement, content)

with open('templates/static/styles.css', 'w', encoding='utf-8') as f:
    f.write(content)

print('Fixed remaining oversized elements')