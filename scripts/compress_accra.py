from PIL import Image, ImageOps
import os

src = r'C:\Portfolio\templates\static\Pictures\Accra Fusion Gallery'
dst = r'C:\Portfolio\templates\static\Pictures\Accra Fusion Gallery\web'
os.makedirs(dst, exist_ok=True)

# Chronological by EXIF date, no-date files grouped by context
mapping = [
    # March 1 — main program day
    ('TLVP8606.JPG',    'john-ngor-deng-garang-accra-fusion-alu-ghana-immersion-2025-1.jpg'),
    ('IGZW8401.JPG',    'john-ngor-deng-garang-accra-fusion-alu-ghana-immersion-2025-2.jpg'),
    ('AXLQ3000.JPG',    'john-ngor-deng-garang-accra-fusion-alu-ghana-immersion-2025-3.jpg'),
    ('AYVH4991.JPG',    'john-ngor-deng-garang-accra-fusion-alu-ghana-immersion-2025-4.jpg'),
    ('AZHT4020.JPG',    'john-ngor-deng-garang-accra-fusion-alu-ghana-immersion-2025-5.jpg'),
    ('GAED8389.JPG',    'john-ngor-deng-garang-accra-fusion-alu-ghana-immersion-2025-6.jpg'),
    ('GJRE2469.JPG',    'john-ngor-deng-garang-accra-fusion-alu-ghana-immersion-2025-7.jpg'),
    ('SNMO2356.JPG',    'john-ngor-deng-garang-accra-fusion-alu-ghana-immersion-2025-8.jpg'),
    ('WRWX1099.JPG',    'john-ngor-deng-garang-accra-fusion-alu-ghana-immersion-2025-9.jpg'),
    ('FWWG1484.JPG',    'john-ngor-deng-garang-accra-fusion-alu-ghana-immersion-2025-10.jpg'),
    ('NLQM8725.JPG',    'john-ngor-deng-garang-accra-fusion-alu-ghana-immersion-2025-11.jpg'),
    ('BDOZ0052.JPG',    'john-ngor-deng-garang-accra-fusion-alu-ghana-immersion-2025-12.jpg'),
    ('JSHW5882.JPG',    'john-ngor-deng-garang-accra-fusion-alu-ghana-immersion-2025-13.jpg'),
    ('DRJD1847.JPG',    'john-ngor-deng-garang-accra-fusion-alu-ghana-immersion-2025-14.jpg'),
    # March 27
    ('HMNY4397.JPG',    'john-ngor-deng-garang-accra-fusion-alu-ghana-immersion-2025-15.jpg'),
    # March 28
    ('DDFV3374.JPG',    'john-ngor-deng-garang-accra-fusion-alu-ghana-immersion-2025-16.jpg'),
    # March 29
    ('AAHH8303.JPG',    'john-ngor-deng-garang-accra-fusion-alu-ghana-immersion-2025-17.jpg'),
    # No-date — professional/event shots
    ('Accra Fusion.png',   'john-ngor-deng-garang-accra-fusion-alu-ghana-immersion-2025-18.jpg'),
    ('Accra Fusion 1.png', 'john-ngor-deng-garang-accra-fusion-alu-ghana-immersion-2025-19.jpg'),
    ('Accra Fusion 3.png', 'john-ngor-deng-garang-accra-fusion-alu-ghana-immersion-2025-20.jpg'),
    ('Accra Fusion 4.png', 'john-ngor-deng-garang-accra-fusion-alu-ghana-immersion-2025-21.jpg'),
    ('BIKU2267.JPG',    'john-ngor-deng-garang-accra-fusion-alu-ghana-immersion-2025-22.jpg'),
    ('EDUC0889.JPG',    'john-ngor-deng-garang-accra-fusion-alu-ghana-immersion-2025-23.jpg'),
    ('MDUZ8580.JPG',    'john-ngor-deng-garang-accra-fusion-alu-ghana-immersion-2025-24.jpg'),
    ('MZSP6439.JPG',    'john-ngor-deng-garang-accra-fusion-alu-ghana-immersion-2025-25.jpg'),
    ('NNXJ9579.JPG',    'john-ngor-deng-garang-accra-fusion-alu-ghana-immersion-2025-26.jpg'),
    ('SMNB0931.JPG',    'john-ngor-deng-garang-accra-fusion-alu-ghana-immersion-2025-27.jpg'),
    ('TWCJ1079.JPG',    'john-ngor-deng-garang-accra-fusion-alu-ghana-immersion-2025-28.jpg'),
    ('TXKB0498.JPG',    'john-ngor-deng-garang-accra-fusion-alu-ghana-immersion-2025-29.jpg'),
    ('VQEX6571.JPG',    'john-ngor-deng-garang-accra-fusion-alu-ghana-immersion-2025-30.jpg'),
    ('VUAU3444.JPG',    'john-ngor-deng-garang-accra-fusion-alu-ghana-immersion-2025-31.jpg'),
    ('XCOA7118.JPG',    'john-ngor-deng-garang-accra-fusion-alu-ghana-immersion-2025-32.jpg'),
    ('XPHBE1242.JPG',   'john-ngor-deng-garang-accra-fusion-alu-ghana-immersion-2025-33.jpg'),
]

MAX_DIMENSION = 1400
QUALITY = 82

for original, seo_name in mapping:
    in_path = os.path.join(src, original)
    out_path = os.path.join(dst, seo_name)
    if not os.path.exists(in_path):
        print(f'MISSING: {original}')
        continue

    img = Image.open(in_path).convert('RGB')
    img = ImageOps.exif_transpose(img)

    w, h = img.size
    if max(w, h) > MAX_DIMENSION:
        if w >= h:
            new_w, new_h = MAX_DIMENSION, int(h * MAX_DIMENSION / w)
        else:
            new_h, new_w = MAX_DIMENSION, int(w * MAX_DIMENSION / h)
        img = img.resize((new_w, new_h), Image.LANCZOS)

    img.save(out_path, 'JPEG', quality=QUALITY, optimize=True, progressive=True)
    orig_kb = os.path.getsize(in_path) // 1024
    new_kb = os.path.getsize(out_path) // 1024
    print(f'{original} -> {seo_name} | {orig_kb}KB -> {new_kb}KB | {img.size}')

print('\nDone.')
