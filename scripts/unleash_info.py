from PIL import Image
from PIL.ExifTags import TAGS
import os

BASE = os.path.dirname(os.path.abspath(__file__))

folder = os.path.join(BASE, '..', 'templates', 'static', 'Pictures', 'UNLEASH Gallery')
files = sorted([f for f in os.listdir(folder) if f.upper().endswith('.JPG')])
lines = []
for f in files:
    path = os.path.join(folder, f)
    with Image.open(path) as img:
        exif = img._getexif() or {}
        dt = exif.get(36867, exif.get(306, 'no-date'))
        orient = exif.get(274, 1)
        w, h = img.size
        size_kb = os.path.getsize(path) // 1024
        lines.append(f"{f}|{dt}|orient={orient}|{w}x{h}|{size_kb}KB")

with open(os.path.join(BASE, 'unleash_info.txt'), 'w') as out:
    out.write('\n'.join(lines))
print("Done")
