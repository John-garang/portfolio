from PIL import Image
from PIL.ExifTags import TAGS
import os

folder = r'C:\Portfolio\templates\static\Pictures\Tilting Futures Gallery'
files = sorted([f for f in os.listdir(folder) if f.lower().endswith(('.jpg', '.jpeg')) and os.path.isfile(os.path.join(folder, f))])
lines = []
for f in files:
    path = os.path.join(folder, f)
    img = Image.open(path)
    exif = img._getexif() or {}
    dt = exif.get(36867, exif.get(306, 'no-date'))
    orient = exif.get(274, 1)
    w, h = img.size
    size_kb = os.path.getsize(path) // 1024
    lines.append(f"{f}|{dt}|orient={orient}|{w}x{h}|{size_kb}KB")

with open(r'C:\Portfolio\scripts\tal_info.txt', 'w', encoding='utf-8') as out:
    out.write('\n'.join(lines))
print("Done")
