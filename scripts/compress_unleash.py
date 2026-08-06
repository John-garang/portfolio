from PIL import Image, ImageOps
import os

src = r'C:\Portfolio\templates\static\Pictures\UNLEASH Gallery'
dst = r'C:\Portfolio\templates\static\Pictures\UNLEASH Gallery\web'
os.makedirs(dst, exist_ok=True)

# Ordered by date (chronological), mapped to SEO name
mapping = [
    ('GYRFE2685.JPG',  'john-ngor-deng-garang-unleash-global-innovation-lab-kigali-rwanda-2023-1.jpg'),
    ('DVWM3221.JPG',   'john-ngor-deng-garang-unleash-global-innovation-lab-kigali-rwanda-2023-2.jpg'),
    ('QNKO0506.JPG',   'john-ngor-deng-garang-unleash-global-innovation-lab-kigali-rwanda-2023-3.jpg'),
    ('UFTSE7875.JPG',  'john-ngor-deng-garang-unleash-global-innovation-lab-kigali-rwanda-2023-4.jpg'),
    ('IMG_6946.JPG',   'john-ngor-deng-garang-unleash-global-innovation-lab-kigali-rwanda-2023-5.jpg'),
    ('IMG_6941.JPG',   'john-ngor-deng-garang-unleash-global-innovation-lab-kigali-rwanda-2023-6.jpg'),
    ('SJTM1583.JPG',   'john-ngor-deng-garang-unleash-global-innovation-lab-kigali-rwanda-2023-7.jpg'),
    ('KBAC4251.JPG',   'john-ngor-deng-garang-unleash-global-innovation-lab-kigali-rwanda-2023-8.jpg'),
    ('PZOR5170.JPG',   'john-ngor-deng-garang-unleash-global-innovation-lab-kigali-rwanda-2023-9.jpg'),
    ('XEQF3762.JPG',   'john-ngor-deng-garang-unleash-global-innovation-lab-kigali-rwanda-2023-10.jpg'),
    ('CQRA7412.JPG',   'john-ngor-deng-garang-unleash-global-innovation-lab-kigali-rwanda-2023-11.jpg'),
    ('IMG_6942.JPG',   'john-ngor-deng-garang-unleash-global-innovation-lab-kigali-rwanda-2023-12.jpg'),
    ('IMG_6943.JPG',   'john-ngor-deng-garang-unleash-global-innovation-lab-kigali-rwanda-2023-13.jpg'),
    ('IMG_6944.JPG',   'john-ngor-deng-garang-unleash-global-innovation-lab-kigali-rwanda-2023-14.jpg'),
    ('ARYBE2198.JPG',  'john-ngor-deng-garang-unleash-global-innovation-lab-kigali-rwanda-2023-15.jpg'),
    ('FGLTE4338.JPG',  'john-ngor-deng-garang-unleash-global-innovation-lab-kigali-rwanda-2023-16.jpg'),
    ('NBYZ4138.JPG',   'john-ngor-deng-garang-unleash-global-innovation-lab-kigali-rwanda-2023-17.jpg'),
]

MAX_DIMENSION = 1400  # max width or height in px
QUALITY = 82          # JPEG quality — good balance of size vs clarity

for original, seo_name in mapping:
    in_path = os.path.join(src, original)
    out_path = os.path.join(dst, seo_name)

    with Image.open(in_path) as img:
        img = ImageOps.exif_transpose(img)

        w, h = img.size
        if max(w, h) > MAX_DIMENSION:
            if w >= h:
                new_w = MAX_DIMENSION
                new_h = int(h * MAX_DIMENSION / w)
            else:
                new_h = MAX_DIMENSION
                new_w = int(w * MAX_DIMENSION / h)
            img = img.resize((new_w, new_h), Image.LANCZOS)

        img.save(out_path, 'JPEG', quality=QUALITY, optimize=True, progressive=True)
        orig_kb = os.path.getsize(in_path) // 1024
        new_kb = os.path.getsize(out_path) // 1024
        print(f'{original} -> {seo_name} | {orig_kb}KB -> {new_kb}KB | {img.size}')

print('\nDone.')
