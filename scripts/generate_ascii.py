import os
import sys
import yaml
from PIL import Image, ImageEnhance

# ASCII character ramp from dark to light (since we render on dark backgrounds)
# When rendering on a dark background, lighter pixels should get denser/brighter characters.
ASCII_RAMP = " .:-=+*#%@"

def get_char_for_brightness(brightness):
    """Map brightness (0-255) to ASCII character."""
    index = int((brightness / 255.0) * (len(ASCII_RAMP) - 1))
    return ASCII_RAMP[index]

def rgb_to_hex(rgb):
    """Convert RGB tuple to hex string."""
    return f"#{rgb[0]:02x}{rgb[1]:02x}{rgb[2]:02x}"

def generate_ascii_svg(image_path, output_path, config):
    # Load configuration
    theme = config.get("theme", {})
    bg_color = theme.get("background", "#1a1b26")
    
    # Target columns
    cols = 65
    
    # Load image
    try:
        img = Image.open(image_path)
    except Exception as e:
        print(f"Error opening image {image_path}: {e}")
        return False
        
    # Convert to RGB
    img = img.convert("RGB")
    
    # Enhance contrast and brightness slightly to make the portrait pop
    enhancer = ImageEnhance.Contrast(img)
    img = enhancer.enhance(1.3)
    enhancer = ImageEnhance.Brightness(img)
    img = enhancer.enhance(1.1)
    
    # Calculate rows based on character aspect ratio (usually ~0.55 width/height)
    char_aspect = 0.55
    width, height = img.size
    img_aspect = height / width
    rows = int(cols * img_aspect * char_aspect)
    
    # Resize image
    img = img.resize((cols, rows), Image.Resampling.LANCZOS)
    
    # Grid/Font dimensions for SVG
    font_size = 11
    line_height = 13
    char_width = 7.0
    
    svg_width = int(cols * char_width + 30)
    svg_height = int(rows * line_height + 30)
    
    svg_content = []
    svg_content.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {svg_width} {svg_height}" width="{svg_width}" height="{svg_height}">')
    svg_content.append(f'  <rect width="100%" height="100%" fill="{bg_color}" rx="8" />')
    
    # Use standard monospace fonts
    svg_content.append('  <style>')
    svg_content.append('    .ascii-text {')
    svg_content.append('      font-family: "SFMono-Regular", Consolas, "Liberation Mono", Menlo, Courier, monospace;')
    svg_content.append(f'      font-size: {font_size}px;')
    svg_content.append('      font-weight: 700;')
    svg_content.append('      letter-spacing: 0.5px;')
    svg_content.append('    }')
    svg_content.append('  </style>')
    
    svg_content.append(f'  <text x="15" y="20" class="ascii-text" xml:space="preserve">')
    
    # Generate colored spans for each character
    for y in range(rows):
        svg_content.append(f'    <tspan x="15" dy="{line_height}">')
        for x in range(cols):
            r, g, b = img.getpixel((x, y))
            # Calculate perceived brightness
            brightness = int(0.299 * r + 0.587 * g + 0.114 * b)
            char = get_char_for_brightness(brightness)
            
            # Avoid empty space span to save space (use simple spacing)
            if char == " ":
                svg_content.append(' ')
            else:
                # Escape XML special chars
                if char == "<": char = "&lt;"
                elif char == ">": char = "&gt;"
                elif char == "&": char = "&amp;"
                
                color_hex = rgb_to_hex((r, g, b))
                svg_content.append(f'<tspan fill="{color_hex}">{char}</tspan>')
        svg_content.append('</tspan>')
        
    svg_content.append('  </text>')
    svg_content.append('</svg>')
    
    # Save to output path
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(svg_content))
        
    print(f"Successfully generated ASCII SVG: {output_path}")
    return True

if __name__ == "__main__":
    # Get paths
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_dir = os.path.dirname(script_dir)
    
    config_path = os.path.join(project_dir, "config.yml")
    with open(config_path, "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)
        
    photo_path = os.path.join(project_dir, "assets", "photo.jpg")
    output_path = os.path.join(project_dir, "assets", "ascii_portrait.svg")
    
    generate_ascii_svg(photo_path, output_path, config)
