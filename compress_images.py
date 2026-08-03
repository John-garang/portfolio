#!/usr/bin/env python3
"""
Compress images in the Graphic Design Portfolio folder
Maintains quality while reducing file size for faster loading
"""
from PIL import Image
import os
from pathlib import Path

# Configuration
GRAPHIC_DESIGN_FOLDER = Path("templates/static/Pictures/Graphic Design Portfolio")
QUALITY = 85  # High quality, good compression
MAX_WIDTH = 1920  # Max width for large images
MAX_HEIGHT = 1920  # Max height for large images

def compress_image(image_path):
    """Compress a single image while maintaining quality"""
    try:
        # Open image
        img = Image.open(image_path)
        
        # Get original size
        original_size = image_path.stat().st_size
        
        # Convert RGBA to RGB if needed (for PNG with transparency)
        if img.mode in ('RGBA', 'LA') or (img.mode == 'P' and 'transparency' in img.info):
            # Create white background
            background = Image.new('RGB', img.size, (255, 255, 255))
            if img.mode == 'P':
                img = img.convert('RGBA')
            background.paste(img, mask=img.split()[-1] if img.mode in ('RGBA', 'LA') else None)
            img = background
        
        # Resize if too large (maintain aspect ratio)
        if img.width > MAX_WIDTH or img.height > MAX_HEIGHT:
            img.thumbnail((MAX_WIDTH, MAX_HEIGHT), Image.Resampling.LANCZOS)
        
        # Determine output format
        if image_path.suffix.lower() in ['.jpg', '.jpeg']:
            # Save as high-quality JPEG
            output_path = image_path.with_suffix('.jpg')
            img.save(output_path, 'JPEG', quality=QUALITY, optimize=True, progressive=True)
        elif image_path.suffix.lower() == '.png':
            # Save as optimized PNG
            output_path = image_path
            img.save(output_path, 'PNG', optimize=True)
        elif image_path.suffix.lower() == '.webp':
            # Convert WebP to PNG for better compatibility
            output_path = image_path.with_suffix('.png')
            img.save(output_path, 'PNG', optimize=True)
        else:
            print(f"  Skipping unsupported format: {image_path.suffix}")
            return
        
        # Get new size
        new_size = output_path.stat().st_size
        reduction = ((original_size - new_size) / original_size) * 100
        
        print(f"  ✓ {image_path.name}: {original_size/1024:.1f}KB → {new_size/1024:.1f}KB ({reduction:.1f}% reduction)")
        
    except Exception as e:
        print(f"  ✗ Error processing {image_path.name}: {e}")

def main():
    print("=" * 70)
    print("Compressing Graphic Design Portfolio Images")
    print("=" * 70)
    print(f"Folder: {GRAPHIC_DESIGN_FOLDER}")
    print(f"Quality: {QUALITY}%")
    print(f"Max dimensions: {MAX_WIDTH}x{MAX_HEIGHT}")
    print("=" * 70)
    
    if not GRAPHIC_DESIGN_FOLDER.exists():
        print(f"Error: Folder not found: {GRAPHIC_DESIGN_FOLDER}")
        return
    
    # Get all image files
    image_extensions = ['.png', '.jpg', '.jpeg', '.webp']
    image_files = []
    for ext in image_extensions:
        image_files.extend(GRAPHIC_DESIGN_FOLDER.glob(f"*{ext}"))
    
    if not image_files:
        print("No images found!")
        return
    
    print(f"\nFound {len(image_files)} images to process\n")
    
    # Process each image
    for i, image_path in enumerate(sorted(image_files), 1):
        print(f"[{i}/{len(image_files)}] Processing {image_path.name}...")
        compress_image(image_path)
    
    print("\n" + "=" * 70)
    print("Compression complete!")
    print("=" * 70)

if __name__ == "__main__":
    main()