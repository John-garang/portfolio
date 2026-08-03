from PIL import Image
import os

SRC = r"C:\Portfolio\templates\static\Pictures\Hackathon at Google Gallery"
DST = os.path.join(SRC, "web")
os.makedirs(DST, exist_ok=True)

base = "john-ngor-deng-garang-nairobi-nexus-hackathon-google-africa-nairobi-2025"

originals = sorted([
    f for f in os.listdir(SRC)
    if f.lower().endswith(('.jpg', '.jpeg', '.png'))
    and f != 'john-ngor-deng-garang-hackathon-google.png'
    and not os.path.isdir(os.path.join(SRC, f))
])

for i, fname in enumerate(originals, 1):
    src_path = os.path.join(SRC, fname)
    new_name = f"{base}-{i}.jpg"
    renamed = os.path.join(SRC, new_name)
    if not os.path.exists(renamed):
        os.rename(src_path, renamed)
    with Image.open(renamed) as img:
        img = img.convert("RGB")
        w, h = img.size
        if w > 1400:
            img = img.resize((1400, int(h * 1400 / w)), Image.LANCZOS)
        img.save(os.path.join(DST, new_name), "JPEG", quality=82, optimize=True)
    print(f"  {new_name}")

print(f"\nDone. {len(originals)} images processed.")
