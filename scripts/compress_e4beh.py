from PIL import Image
import os, shutil

SRC = r"C:\Portfolio\templates\static\Pictures\E4BEH Gallery"
DST = os.path.join(SRC, "web")
os.makedirs(DST, exist_ok=True)

# Map original filenames to sequential numbered names (skip E4BEHackathon.png — that's the hero)
originals = sorted([
    f for f in os.listdir(SRC)
    if f.lower().endswith(('.jpg', '.jpeg', '.png')) and f != 'E4BEHackathon.png'
        and not os.path.isdir(os.path.join(SRC, f))
])

base = "john-ngor-deng-garang-e4be-hackathon-arusha-tanzania-2025"

for i, fname in enumerate(originals, 1):
    src_path = os.path.join(SRC, fname)
    new_name = f"{base}-{i}.jpg"
    dst_path = os.path.join(DST, new_name)

    # Rename original in place
    renamed = os.path.join(SRC, new_name)
    if not os.path.exists(renamed):
        os.rename(src_path, renamed)
    else:
        renamed = src_path  # already renamed

    # Compress to web/
    with Image.open(renamed) as img:
        img = img.convert("RGB")
        w, h = img.size
        if w > 1400:
            img = img.resize((1400, int(h * 1400 / w)), Image.LANCZOS)
        img.save(dst_path, "JPEG", quality=82, optimize=True)
    print(f"  {new_name}")

# Also copy/compress the hero image
hero_src = os.path.join(SRC, "E4BEHackathon.png")
hero_dst = os.path.join(SRC, "john-ngor-deng-garang-e4be-hackathon.png")
if os.path.exists(hero_src) and not os.path.exists(hero_dst):
    os.rename(hero_src, hero_dst)

print(f"\nDone. {len(originals)} gallery images processed.")
