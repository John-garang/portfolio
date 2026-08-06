#!/usr/bin/env python3
from PIL import Image
from pathlib import Path

FOLDER = Path("templates/static/Pictures/Graphic Design Portfolio")
QUALITY = 85
MAX_DIM = 1920

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
            print("OK " + path.name + " -> " + out.name + "  " + str(orig_size//1024) + "KB -> " + str(new_size//1024) + "KB")
    except Exception as e:
        print("ERR " + str(path.name) + ": " + str(e))

for ext in ['*.png', '*.jpg', '*.jpeg']:
    for f in sorted(FOLDER.glob(ext)):
        convert(f)

print("Done.")
