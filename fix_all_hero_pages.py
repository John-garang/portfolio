import os
import re

# List of files to fix
files = [
    'cnn-academy.html',
    'take-action-lab.html',
    'unleash-innovation.html',
    'accra-fusion.html',
    'yali-east-africa.html',
    'african-leadership-university.html',
    'education-bridge.html',
    'african-leadership-academy.html',
    'ashinaga-foundation.html',
    'uganics-repellents.html',
    'africa-inventor-alliance.html',
    'surplus-people-project.html',
    'creative-connect.html',
    'nalafem-collective.html'
]

for filename in files:
    if not os.path.exists(filename):
        print(f"Skipping {filename} - not found")
        continue
    
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check if has alu-hero class
    has_hero = 'alu-hero' in content
    
    # Remove script.js line
    original = content
    content = re.sub(r'\s*<script src="script\.js"></script>\s*', '\n', content)
    
    if content != original:
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"[FIXED] {filename} (has alu-hero: {has_hero})")
    else:
        print(f"[OK] {filename} already fixed (has alu-hero: {has_hero})")
