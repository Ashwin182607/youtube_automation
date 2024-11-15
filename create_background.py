cat > /home/warp/CascadeProjects/youtube_automation/create_background.py << 'EOL'
from PIL import Image, ImageDraw, ImageFilter
import os
from config import BACKGROUNDS_DIR

def create_gradient_background():
    # Create a new image with a dark gradient
    width = 1920
    height = 1080
    image = Image.new('RGB', (width, height))
    draw = ImageDraw.Draw(image)
    
    # Create a dark gradient
    for y in range(height):
        r = int(20 * (1 - y/height))  # Dark blue-ish gradient
        g = int(25 * (1 - y/height))
        b = int(35 * (1 - y/height))
        draw.line([(0, y), (width, y)], fill=(r, g, b))
    
    # Apply slight blur for smoothness
    image = image.filter(ImageFilter.GaussianBlur(radius=2))
    
    # Save the image
    os.makedirs(BACKGROUNDS_DIR, exist_ok=True)
    output_path = os.path.join(BACKGROUNDS_DIR, 'default_bg.jpg')
    image.save(output_path, quality=95)
    print(f"Background created at: {output_path}")

if __name__ == "__main__":
    create_gradient_background()
EOL