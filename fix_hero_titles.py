import re

with open('templates/static/styles.css', 'r', encoding='utf-8') as f:
    content = f.read()

# Fix hero titles to use clamp for responsive scaling
hero_title_replacements = [
    # Company header h1
    (r'\.company-header h1 \{\s*\n\s*font-size: 2rem', 
     '.company-header h1 {\n    font-size: clamp(1.75rem, 4vw, 2.5rem)'),
    
    # Contact form section h2
    (r'\.contact-form-section h2 \{\s*\n\s*font-size: 2rem',
     '.contact-form-section h2 {\n    font-size: clamp(1.75rem, 4vw, 2.5rem)'),
    
    # Blog header h1
    (r'\.blog-header h1 \{\s*\n\s*font-size: 2rem',
     '.blog-header h1 {\n    font-size: clamp(1.75rem, 4vw, 2.5rem)'),
    
    # Search results section h1
    (r'\.search-results-section h1 \{\s*\n\s*font-size: 2rem',
     '.search-results-section h1 {\n    font-size: clamp(1.75rem, 4vw, 2.5rem)'),
]

for pattern, replacement in hero_title_replacements:
    content = re.sub(pattern, replacement, content)

with open('templates/static/styles.css', 'w', encoding='utf-8') as f:
    f.write(content)

print('Hero titles normalized to use clamp')