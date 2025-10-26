"""
Demo Generator - Create screenshots and demo content for GitHub
"""

import numpy as np
from PIL import Image, ImageDraw, ImageFont
from upscaler import AMDUpscaler
import time

def create_demo_image():
    """Create a test image for demonstration"""
    # Create 512x512 image with pattern
    img = Image.new('RGB', (512, 512), color=(20, 20, 40))
    draw = ImageDraw.Draw(img)
    
    # Draw grid pattern
    for i in range(0, 512, 64):
        draw.line([(i, 0), (i, 512)], fill=(40, 40, 60), width=2)
        draw.line([(0, i), (512, i)], fill=(40, 40, 60), width=2)
    
    # Draw text
    try:
        font = ImageFont.truetype("arial.ttf", 48)
    except:
        font = ImageFont.load_default()
    
    draw.text((256, 200), "AI", anchor="mm", fill=(0, 255, 0), font=font)
    draw.text((256, 280), "UPSCALER", anchor="mm", fill=(0, 255, 0), font=font)
    draw.text((256, 340), "TEST", anchor="mm", fill=(100, 200, 255), font=font)
    
    return img

def generate_comparison():
    """Generate before/after comparison"""
    print("="*60)
    print("GENERATING DEMO COMPARISON")
    print("="*60)
    
    # Create original image
    print("\n[1/4] Creating test image...")
    original = create_demo_image()
    original.save("demo_original.png")
    print(f"  ✓ Saved: demo_original.png ({original.size[0]}x{original.size[1]})")
    
    # Initialize upscaler
    print("\n[2/4] Loading AI model...")
    upscaler = AMDUpscaler()
    
    # Upscale
    print("\n[3/4] Running AI upscaling...")
    start = time.time()
    upscaled = upscaler.upscale_image("demo_original.png", "demo_upscaled.png")
    elapsed = time.time() - start
    
    print(f"  ✓ Upscaled in {elapsed*1000:.2f}ms")
    print(f"  ✓ Output: {upscaled.size[0]}x{upscaled.size[1]}")
    
    # Create side-by-side comparison
    print("\n[4/4] Creating comparison image...")
    comparison = Image.new('RGB', (original.width * 2 + 40, original.height + 100), color=(30, 30, 30))
    draw = ImageDraw.Draw(comparison)
    
    # Paste images
    comparison.paste(original, (20, 60))
    comparison.paste(upscaled.resize(original.size, Image.Resampling.LANCZOS), (original.width + 20, 60))
    
    # Add labels
    try:
        font_large = ImageFont.truetype("arial.ttf", 36)
        font_small = ImageFont.truetype("arial.ttf", 24)
    except:
        font_large = ImageFont.load_default()
        font_small = ImageFont.load_default()
    
    draw.text((original.width//2 + 20, 20), "ORIGINAL", anchor="mm", fill=(255, 255, 255), font=font_large)
    draw.text((original.width + original.width//2 + 20, 20), "AI UPSCALED 2X", anchor="mm", fill=(0, 255, 0), font=font_large)
    
    # Add specs
    draw.text((original.width//2 + 20, original.height + 80), 
              f"{original.width}x{original.height}", anchor="mm", fill=(150, 150, 150), font=font_small)
    draw.text((original.width + original.width//2 + 20, original.height + 80), 
              f"{upscaled.width}x{upscaled.height}", anchor="mm", fill=(0, 200, 0), font=font_small)
    
    comparison.save("demo_comparison.png")
    print(f"  ✓ Saved: demo_comparison.png")
    
    print("\n" + "="*60)
    print("DEMO GENERATION COMPLETE")
    print("="*60)
    print("\nGenerated files:")
    print("  - demo_original.png")
    print("  - demo_upscaled.png")
    print("  - demo_comparison.png")
    print("\nUse these for GitHub README screenshots!")

if __name__ == "__main__":
    generate_comparison()
