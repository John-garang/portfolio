from PIL import Image, ImageOps
import os

src = r'C:\Portfolio\templates\static\Pictures\Tilting Futures Gallery'
dst = r'C:\Portfolio\templates\static\Pictures\Tilting Futures Gallery\web'
os.makedirs(dst, exist_ok=True)

# Chronological order, deduped (skip IMG_3733.jpeg, IMG_3735.jpeg, IMG_E3735.JPG — dupes of IMG_3733.JPG)
# Dates inferred from filenames where EXIF missing; PHOTO files = Mar 10, WhatsApp files = date in name
mapping = [
    # March 10 — arrival / first days
    ('PHOTO-2024-03-10-19-08-58 2024-03-10 21_10_13.jpg',  'john-ngor-deng-garang-take-action-lab-tilting-futures-south-africa-2024-1.jpg'),
    ('PHOTO-2024-03-10-19-09-01 2024-03-10 21_10_17.jpg',  'john-ngor-deng-garang-take-action-lab-tilting-futures-south-africa-2024-2.jpg'),
    ('PHOTO-2024-03-10-21-07-41 2024-03-10 21_13_50.jpg',  'john-ngor-deng-garang-take-action-lab-tilting-futures-south-africa-2024-3.jpg'),
    ('WhatsApp Image 2024-03-10 at 21.07.35_9543fd02.jpg', 'john-ngor-deng-garang-take-action-lab-tilting-futures-south-africa-2024-4.jpg'),
    ('WhatsApp Image 2024-03-10 at 21.07.42_69e84903.jpg', 'john-ngor-deng-garang-take-action-lab-tilting-futures-south-africa-2024-5.jpg'),
    ('WhatsApp Image 2024-03-10 at 21.07.51_daf931d6.jpg', 'john-ngor-deng-garang-take-action-lab-tilting-futures-south-africa-2024-6.jpg'),
    # March 11
    ('WhatsApp Image 2024-03-11 at 20.53.15_81e4221b.jpg', 'john-ngor-deng-garang-take-action-lab-tilting-futures-south-africa-2024-7.jpg'),
    ('WhatsApp Image 2024-03-11 at 20.53.17_a13805bf.jpg', 'john-ngor-deng-garang-take-action-lab-tilting-futures-south-africa-2024-8.jpg'),
    # No-date camera roll — grouped early (likely March/early April based on context)
    ('CRJB7663.JPG',   'john-ngor-deng-garang-take-action-lab-tilting-futures-south-africa-2024-9.jpg'),
    ('JNIF4071.JPG',   'john-ngor-deng-garang-take-action-lab-tilting-futures-south-africa-2024-10.jpg'),
    ('GKOJ7005.JPG',   'john-ngor-deng-garang-take-action-lab-tilting-futures-south-africa-2024-11.jpg'),
    ('HASM4999.JPG',   'john-ngor-deng-garang-take-action-lab-tilting-futures-south-africa-2024-12.jpg'),
    ('HRLN6353.JPG',   'john-ngor-deng-garang-take-action-lab-tilting-futures-south-africa-2024-13.jpg'),
    ('KHUJ3916.JPG',   'john-ngor-deng-garang-take-action-lab-tilting-futures-south-africa-2024-14.jpg'),
    ('UABR7037.JPG',   'john-ngor-deng-garang-take-action-lab-tilting-futures-south-africa-2024-15.jpg'),
    ('BWGH2619.JPG',   'john-ngor-deng-garang-take-action-lab-tilting-futures-south-africa-2024-16.jpg'),
    ('IMZK2128.JPG',   'john-ngor-deng-garang-take-action-lab-tilting-futures-south-africa-2024-17.jpg'),
    ('IOTV3373.JPG',   'john-ngor-deng-garang-take-action-lab-tilting-futures-south-africa-2024-18.jpg'),
    ('EPGM5044.JPG',   'john-ngor-deng-garang-take-action-lab-tilting-futures-south-africa-2024-19.jpg'),
    ('GOPY9510.JPG',   'john-ngor-deng-garang-take-action-lab-tilting-futures-south-africa-2024-20.jpg'),
    ('CQOC7318.JPG',   'john-ngor-deng-garang-take-action-lab-tilting-futures-south-africa-2024-21.jpg'),
    ('VBUI3204.JPG',   'john-ngor-deng-garang-take-action-lab-tilting-futures-south-africa-2024-22.jpg'),
    ('VYHC3875.JPG',   'john-ngor-deng-garang-take-action-lab-tilting-futures-south-africa-2024-23.jpg'),
    ('NLPV1781.JPG',   'john-ngor-deng-garang-take-action-lab-tilting-futures-south-africa-2024-24.jpg'),  # no-date large
    ('XUWN8253.JPG',   'john-ngor-deng-garang-take-action-lab-tilting-futures-south-africa-2024-25.jpg'),
    ('PHDO8742.JPG',   'john-ngor-deng-garang-take-action-lab-tilting-futures-south-africa-2024-26.jpg'),
    ('IMG_0269 (1).jpg', 'john-ngor-deng-garang-take-action-lab-tilting-futures-south-africa-2024-27.jpg'),
    # April 4
    ('20240404_133129.jpg', 'john-ngor-deng-garang-take-action-lab-tilting-futures-south-africa-2024-28.jpg'),
    # April 12
    ('WhatsApp Image 2024-04-12 at 20.21.32_48d651b1.jpg', 'john-ngor-deng-garang-take-action-lab-surplus-people-project-south-africa-2024-29.jpg'),
    ('IMG_0425.JPG',   'john-ngor-deng-garang-take-action-lab-surplus-people-project-south-africa-2024-30.jpg'),
    # April 20
    ('WhatsApp Image 2024-04-20 at 17.31.47_3db0726b.jpg', 'john-ngor-deng-garang-take-action-lab-surplus-people-project-south-africa-2024-31.jpg'),
    # April 24
    ('IMG_0519.JPG',   'john-ngor-deng-garang-take-action-lab-surplus-people-project-south-africa-2024-32.jpg'),
    # April 26
    ('WhatsApp Image 2024-04-26 at 12.26.52_01e29589.jpg', 'john-ngor-deng-garang-take-action-lab-surplus-people-project-south-africa-2024-33.jpg'),
    ('IMG_0630.JPG',   'john-ngor-deng-garang-take-action-lab-surplus-people-project-south-africa-2024-34.jpg'),
    ('IMG_0632.JPG',   'john-ngor-deng-garang-take-action-lab-surplus-people-project-south-africa-2024-35.jpg'),
    ('IMG_0637.JPG',   'john-ngor-deng-garang-take-action-lab-surplus-people-project-south-africa-2024-36.jpg'),
    ('HBZA8510.JPG',   'john-ngor-deng-garang-take-action-lab-surplus-people-project-south-africa-2024-37.jpg'),
    ('IMG_0805.JPG',   'john-ngor-deng-garang-take-action-lab-surplus-people-project-south-africa-2024-38.jpg'),
    # May 1
    ('EVTM7850.JPG',   'john-ngor-deng-garang-take-action-lab-safe-youth-workshop-south-africa-2024-39.jpg'),
    # May 6
    ('WhatsApp Image 2024-05-06 at 21.52.30_ab20ad3f.jpg', 'john-ngor-deng-garang-take-action-lab-safe-youth-workshop-south-africa-2024-40.jpg'),
    # May 9
    ('S1300052.JPG',   'john-ngor-deng-garang-take-action-lab-national-indaba-conference-south-africa-2024-41.jpg'),
    ('S1300053.JPG',   'john-ngor-deng-garang-take-action-lab-national-indaba-conference-south-africa-2024-42.jpg'),
    # May 15
    ('WhatsApp Image 2024-05-15 at 17.40.04_4134d6da.jpg', 'john-ngor-deng-garang-take-action-lab-national-indaba-conference-south-africa-2024-43.jpg'),
    ('WhatsApp Image 2024-05-15 at 17.40.10_b0c15c6a.jpg', 'john-ngor-deng-garang-take-action-lab-national-indaba-conference-south-africa-2024-44.jpg'),
    # No-date high-res portraits — likely formal/event shots
    ('IMG_3733.JPG',   'john-ngor-deng-garang-take-action-lab-tilting-futures-south-africa-2024-45.jpg'),
    ('PHDO8742.JPG',   None),  # already used as -26, skip
    # June 2
    ('WhatsApp Image 2024-06-02 at 17.05.08_4cf5e935.jpg', 'john-ngor-deng-garang-take-action-lab-food-sovereignty-workshop-paarl-2024-46.jpg'),
]

# Remove None entries (dupes)
mapping = [(orig, seo) for orig, seo in mapping if seo is not None]

MAX_DIMENSION = 1400
QUALITY = 82

for original, seo_name in mapping:
    in_path = os.path.join(src, original)
    out_path = os.path.join(dst, seo_name)
    if not os.path.exists(in_path):
        print(f'MISSING: {original}')
        continue

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
