import os

def generate_wave_svg(output_path, config):
    theme = config.get("theme", {})
    bg_color = theme.get("background", "#1a1b26")
    title_color = theme.get("title", "#7aa2f7")      # blue
    label_color = theme.get("label", "#bb9af7")      # purple
    cursor_color = theme.get("cursor", "#ff007f")    # pink
    
    width = 900
    height = 100
    
    svg = []
    svg.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="{width}" height="{height}">')
    
    # Define linear gradients
    svg.append('  <defs>')
    # Gradient 1: Purple to transparent
    svg.append('    <linearGradient id="grad-wave1" x1="0%" y1="0%" x2="100%" y2="0%">')
    svg.append(f'      <stop offset="0%" stop-color="{label_color}" stop-opacity="0.2" />')
    svg.append(f'      <stop offset="50%" stop-color="{cursor_color}" stop-opacity="0.1" />')
    svg.append(f'      <stop offset="100%" stop-color="{title_color}" stop-opacity="0.2" />')
    svg.append('    </linearGradient>')
    
    # Gradient 2: Cyan/Blue to transparent
    svg.append('    <linearGradient id="grad-wave2" x1="0%" y1="0%" x2="100%" y2="0%">')
    svg.append(f'      <stop offset="0%" stop-color="{title_color}" stop-opacity="0.3" />')
    svg.append(f'      <stop offset="100%" stop-color="{label_color}" stop-opacity="0.2" />')
    svg.append('    </linearGradient>')
    
    # Gradient 3: Solid Tokyo Night transition
    svg.append('    <linearGradient id="grad-wave3" x1="0%" y1="0%" x2="100%" y2="0%">')
    svg.append(f'      <stop offset="0%" stop-color="{bg_color}" />')
    svg.append(f'      <stop offset="50%" stop-color="#24283b" />')
    svg.append(f'      <stop offset="100%" stop-color="{bg_color}" />')
    svg.append('    </linearGradient>')
    svg.append('  </defs>')
    
    # Background wave layer (Wave 1) - slow animation
    svg.append(f'  <path fill="url(#grad-wave1)">')
    svg.append(f'    <animate attributeName="d" dur="12s" repeatCount="indefinite"')
    svg.append(f'      values="')
    svg.append(f'        M0 30 Q 225 70, 450 30 T 900 30 L 900 {height} L 0 {height} Z;')
    svg.append(f'        M0 30 Q 225 10, 450 50 T 900 30 L 900 {height} L 0 {height} Z;')
    svg.append(f'        M0 30 Q 225 50, 450 20 T 900 30 L 900 {height} L 0 {height} Z;')
    svg.append(f'        M0 30 Q 225 70, 450 30 T 900 30 L 900 {height} L 0 {height} Z')
    svg.append(f'      " />')
    svg.append(f'  </path>')
    
    # Middle wave layer (Wave 2) - offset timing
    svg.append(f'  <path fill="url(#grad-wave2)">')
    svg.append(f'    <animate attributeName="d" dur="8s" repeatCount="indefinite"')
    svg.append(f'      values="')
    svg.append(f'        M0 50 Q 225 20, 450 60 T 900 50 L 900 {height} L 0 {height} Z;')
    svg.append(f'        M0 50 Q 225 70, 450 30 T 900 50 L 900 {height} L 0 {height} Z;')
    svg.append(f'        M0 50 Q 225 30, 450 50 T 900 50 L 900 {height} L 0 {height} Z;')
    svg.append(f'        M0 50 Q 225 20, 450 60 T 900 50 L 900 {height} L 0 {height} Z')
    svg.append(f'      " />')
    svg.append(f'  </path>')
    
    # Foreground wave layer (Wave 3) - solid transition wave
    svg.append(f'  <path fill="url(#grad-wave3)">')
    svg.append(f'    <animate attributeName="d" dur="10s" repeatCount="indefinite"')
    svg.append(f'      values="')
    svg.append(f'        M0 70 Q 225 90, 450 60 T 900 70 L 900 {height} L 0 {height} Z;')
    svg.append(f'        M0 70 Q 225 50, 450 80 T 900 70 L 900 {height} L 0 {height} Z;')
    svg.append(f'        M0 70 Q 225 80, 450 70 T 900 70 L 900 {height} L 0 {height} Z;')
    svg.append(f'        M0 70 Q 225 90, 450 60 T 900 70 L 900 {height} L 0 {height} Z')
    svg.append(f'      " />')
    svg.append(f'  </path>')
    
    svg.append('</svg>')
    
    # Save file
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(svg))
        
    print(f"Successfully generated Wave Divider SVG: {output_path}")
    return True

if __name__ == "__main__":
    import yaml
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_dir = os.path.dirname(script_dir)
    
    config_path = os.path.join(project_dir, "config.yml")
    with open(config_path, "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)
        
    output_path = os.path.join(project_dir, "assets", "wave_divider.svg")
    generate_wave_svg(output_path, config)
