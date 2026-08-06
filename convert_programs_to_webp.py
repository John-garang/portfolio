#!/usr/bin/env python3
from PIL import Image
from pathlib import Path

QUALITY = 85
MAX_DIM = 1920

FOLDERS = [
    Path("templates/static/Pictures/Accra Fusion Gallery/web"),
    Path("templates/static/Pictures/E4BEH Gallery/web"),
    Path("templates/static/Pictures/Hackathon at Google Gallery/web"),
    Path("templates/static/Pictures/Tilting Futures Gallery/web"),
    Path("templates/static/Pictures/UNLEASH Gallery/web"),
]

def convert(path):
    try:
        with Image.open(path) as img:
            orig_size = path.stat().st_size
            if img.mode in ('RGBA', 'LA', 'P'):
                img = img.convert('RGBA')
            else:
                img = img.convert('RGB')
            if img.width > MAX_DIM or img.height > MAX_DIM:
                img.thumbnail((MAX_DIM, MAX_DIM), Image.Resampling.LANCZOS)
            out = path.with_suffix('.webp')
            img.save(out, 'WEBP', quality=QUALITY, method=6)
            new_size = out.stat().st_size
            print("OK " + path.name + " -> " + str(orig_size//1024) + "KB -> " + str(new_size//1024) + "KB")
    except Exception as e:
        print("ERR " + str(path.name) + ": " + str(e))

for folder in FOLDERS:
    if not folder.exists():
        print("SKIP (not found): " + str(folder))
        continue
    print("\n--- " + str(folder) + " ---")
    for ext in ['*.jpg', '*.jpeg', '*.JPG', '*.png']:
        for f in sorted(folder.glob(ext)):
            convert(f)

print("\nDone.")
