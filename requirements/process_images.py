import os
import argparse
from PIL import Image, ImageEnhance
from concurrent.futures import ThreadPoolExecutor

def process_image(input_path, output_path, size=(800, 800), brightness=1.0, contrast=1.0):
    try:
        with Image.open(input_path) as img:
            # Convert to RGB mode
            img = img.convert('RGB')
            
            # Resize image
            img.thumbnail(size, Image.Resampling.LANCZOS)
            
            # Adjust brightness
            enhancer = ImageEnhance.Brightness(img)
            img = enhancer.enhance(brightness)
            
            # Adjust contrast
            enhancer = ImageEnhance.Contrast(img)
            img = enhancer.enhance(contrast)
            
            # Save the processed image
            img.save(output_path, 'JPEG', quality=85)
        print(f"Processed: {input_path} -> {output_path}")
    except Exception as e:
        print(f"Error processing {input_path}: {str(e)}")

def main(input_dir, output_dir, size, brightness, contrast):
    os.makedirs(output_dir, exist_ok=True)
    
    image_files = [f for f in os.listdir(input_dir) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif'))]
    
    with ThreadPoolExecutor() as executor:
        futures = []
        for filename in image_files:
            input_path = os.path.join(input_dir, filename)
            output_path = os.path.join(output_dir, os.path.splitext(filename)[0] + '.jpg')
            futures.append(executor.submit(process_image, input_path, output_path, size, brightness, contrast))
        
        for future in futures:
            future.result()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Batch process images for face recognition training.")
    parser.add_argument("input_dir", help="Input directory containing images")
    parser.add_argument("output_dir", help="Output directory for processed images")
    parser.add_argument("--size", type=int, nargs=2, default=(800, 800), help="Output image size (width height)")
    parser.add_argument("--brightness", type=float, default=1.0, help="Brightness adjustment factor")
    parser.add_argument("--contrast", type=float, default=1.0, help="Contrast adjustment factor")
    
    args = parser.parse_args()
    
    main(args.input_dir, args.output_dir, tuple(args.size), args.brightness, args.contrast)
