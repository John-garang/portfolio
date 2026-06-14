#!/usr/bin/env python3
"""
Image Compression Script for Portfolio Site
Compresses all images > 500KB to optimize load times
"""
import os
from pathlib import Path
from PIL import Image
import sys

def compress_image(image_path, max_size_kb=500):
    """Compress image if it's larger than max_size_kb"""
    file_size_kb = os.path.getsize(image_path) / 1024
    
    if file_size_kb <= max_size_kb:
        return False, file_size_kb, file_size_kb
    
    img = None
    background = None
    try:
        img = Image.open(image_path)
        
        # Convert RGBA to RGB if necessary
        if img.mode in ('RGBA', 'LA', 'P'):
            background = Image.new('RGB', img.size, (255, 255, 255))
            if img.mode == 'P':
                img = img.convert('RGBA')
            background.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
            img.close()
            img = background
            background = None
        
        # Resize if too large (max 1920px width)
        max_width = 1920
        if img.width > max_width:
            ratio = max_width / img.width
            new_height = int(img.height * ratio)
            resized_img = img.resize((max_width, new_height), Image.Resampling.LANCZOS)
            img.close()
            img = resized_img
        
        # Save with optimization
        ext = image_path.suffix.lower()
        if ext in ['.jpg', '.jpeg']:
            img.save(image_path, 'JPEG', quality=85, optimize=True)
        elif ext == '.png':
            img.save(image_path, 'PNG', optimize=True, compress_level=9)
        
        new_size_kb = os.path.getsize(image_path) / 1024
        return True, file_size_kb, new_size_kb
    
    except Exception as e:
        print(f"Error compressing {image_path.name}: {e}")
        return False, file_size_kb, file_size_kb
    
    finally:
        if img is not None:
            img.close()
        if background is not None:
            background.close()

def main():
    pictures_dir = Path('static/Pictures')
    if not pictures_dir.exists():
        print("Error: static/Pictures directory not found!")
        sys.exit(1)
    
    print("=" * 60)
    print("IMAGE COMPRESSION SCRIPT")
    print("=" * 60)
    print(f"Scanning: {pictures_dir}")
    print()
    
    total_before = 0
    total_after = 0
    compressed_count = 0
    
    # Get all images
    image_extensions = ['.jpg', '.jpeg', '.png', '.JPG', '.JPEG', '.PNG']
    images = []
    for ext in image_extensions:
        images.extend(pictures_dir.rglob(f'*{ext}'))
    
    print(f"Found {len(images)} images")
    print()
    
    for img_path in images:
        compressed, before_kb, after_kb = compress_image(img_path)
        total_before += before_kb
        total_after += after_kb
        
        if compressed:
            compressed_count += 1
            reduction = ((before_kb - after_kb) / before_kb) * 100
            print(f"[OK] {img_path.name}")
            print(f"  {before_kb:.1f}KB -> {after_kb:.1f}KB ({reduction:.1f}% reduction)")
    
    print()
    print("=" * 60)
    print("COMPRESSION SUMMARY")
    print("=" * 60)
    print(f"Images compressed: {compressed_count}/{len(images)}")
    print(f"Total before: {total_before/1024:.1f}MB")
    print(f"Total after: {total_after/1024:.1f}MB")
    print(f"Space saved: {(total_before-total_after)/1024:.1f}MB")
    print(f"Overall reduction: {((total_before-total_after)/total_before)*100:.1f}%")
    print()

if __name__ == '__main__':
    try:
        from PIL import Image
    except ImportError:
        print("ERROR: Pillow library not installed!")
        print("Run: pip install Pillow")
        sys.exit(1)
    
    main()
