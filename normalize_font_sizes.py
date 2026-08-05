import os
import re

# Files with inline font-size styles
html_files = [
    'templates/about/index.html',
    'templates/blog.html',
    'templates/experience-overview/index.html',
    'templates/my-shelf.html',
    'templates/programs-overview/index.html',
    'templates/travels.html'
]

# Type scale mapping for inline styles
size_map = {
    '0.72rem': '0.8rem',
    '0.75rem': '0.8rem',
    '0.78rem': '0.8rem',
    '0.85rem': '0.8rem',
    '0.88rem': '0.95rem',
    '0.9rem': '0.95rem',
    '1.1rem': '1.05rem',
    '1.9rem': '2rem',
    '4rem': 'clamp(1.75rem, 4vw, 2.5rem)',
}

for filepath in html_files:
    if not os.path.exists(filepath):
        continue
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Replace font-size values in inline styles
    for old_size, new_size in size_map.items():
        pattern = r'(font-size:\s*)' + re.escape(old_size)
        replacement = r'\g<1>' + new_size
        content = re.sub(pattern, replacement, content)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f'Normalized: {filepath}')

print('All HTML inline styles normalized')