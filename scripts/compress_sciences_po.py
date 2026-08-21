from PIL import Image, ImageOps
import os

src = r'C:\Portfolio\templates\static\Pictures\Graphic Design Portfolio\Etudiant Parliament Sciences Po'
dst = r'C:\Portfolio\templates\static\Pictures\Graphic Design Portfolio\Etudiant Parliament Sciences Po\web'
os.makedirs(dst, exist_ok=True)

# Mapping of original files to webp output names
mapping = [
    ('Modèle Café Carriéré 1.png', 'sciences-po-cafe-carriere-1.webp'),
    ('Modèle Café Carriéré 2.png', 'sciences-po-cafe-carriere-2.webp'),
    ('Modèle de flyer de conférence 1 (1).png', 'sciences-po-flyer-conference-1.webp'),
    ('Modèle de flyer de conférence 1.png', 'sciences-po-flyer-conference-2.webp'),
    ('Modèle de masterclass 3.png', 'sciences-po-masterclass-3.webp'),
    ('Modèle de visite 1.png', 'sciences-po-visite-1.webp'),
    ('Modèle de visite 2.png', 'sciences-po-visite-2.webp'),
    ('Modèle de visite 3.png', 'sciences-po-visite-3.webp'),
    ('Modèle de visite 4.png', 'sciences-po-visite-4.webp'),
]

MAX_DIMENSION = 1400
QUALITY = 82

for original, seo_name in mapping:
    in_path = os.path.join(src, original)
    out_path = os.path.join(dst, seo_name)
    if not os.path.exists(in_path):
        print(f'MISSING: {original}')
        continue

    with Image.open(in_path) as img:
        img = ImageOps.exif_transpose(img.convert('RGB'))

        w, h = img.size
        if max(w, h) > MAX_DIMENSION:
            if w >= h:
                new_w, new_h = MAX_DIMENSION, int(h * MAX_DIMENSION / w)
            else:
                new_h, new_w = MAX_DIMENSION, int(w * MAX_DIMENSION / h)
            img = img.resize((new_w, new_h), Image.LANCZOS)

        img.save(out_path, 'WEBP', quality=QUALITY, method=6)
        orig_kb = os.path.getsize(in_path) // 1024
        new_kb = os.path.getsize(out_path) // 1024
        print(f'{original} -> {seo_name} | {orig_kb}KB -> {new_kb}KB | {img.size}')

print('\nDone.')