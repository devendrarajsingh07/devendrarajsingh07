import os
from xml.sax.saxutils import escape as xml_escape

def generate_typing_header_svg(output_path, config):
    theme = config.get("theme", {})
    title_color = theme.get("title", "#7aa2f7")
    label_color = theme.get("label", "#bb9af7")
    cursor_color = theme.get("cursor", "#ff007f")
    
    width = 800
    height = 110
    
    line1_text = "Hi, I'm Devendra Raj Singh 👋"
    line2_text = "AI/ML & Software Developer"
    
    # Calculate widths based on monospaced character size estimates
    # For font-size 26px, width is ~15.6px per char. 28 chars = 437px.
    # For font-size 18px, width is ~10.8px per char. 26 chars = 281px.
    l1_width = 445
    l2_width = 285
    
    svg = []
    svg.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="{width}" height="{height}">')
    
    # Style definitions
    svg.append('  <style>')
    svg.append('    .typing-text {')
    svg.append('      font-family: "SFMono-Regular", Consolas, "Liberation Mono", Menlo, Courier, monospace;')
    svg.append('      font-weight: 700;')
    svg.append('      dominant-baseline: middle;')
    svg.append('    }')
    svg.append('    .line1 {')
    svg.append(f'      font-size: 26px;')
    svg.append(f'      fill: {title_color};')
    svg.append('    }')
    svg.append('    .line2 {')
    svg.append(f'      font-size: 18px;')
    svg.append(f'      fill: {label_color};')
    svg.append('    }')
    svg.append('  </style>')
    
    # Clip paths for the typewriter effect
    svg.append('  <defs>')
    svg.append('    <clipPath id="clip-line1">')
    svg.append(f'      <rect x="0" y="0" width="0" height="{height}">')
    svg.append(f'        <animate attributeName="width" from="0" to="{l1_width}" dur="2s" begin="0.5s" fill="freeze" calcMode="linear" />')
    svg.append('      </rect>')
    svg.append('    </clipPath>')
    
    svg.append('    <clipPath id="clip-line2">')
    svg.append(f'      <rect x="0" y="0" width="0" height="{height}">')
    svg.append(f'        <animate attributeName="width" from="0" to="{l2_width}" dur="1.5s" begin="2.7s" fill="freeze" calcMode="linear" />')
    svg.append('      </rect>')
    svg.append('    </clipPath>')
    svg.append('  </defs>')
    
    # Render Text Elements with Clip Paths
    svg.append(f'  <g clip-path="url(#clip-line1)">')
    svg.append(f'    <text x="15" y="35" class="typing-text line1">{xml_escape(line1_text)}</text>')
    svg.append('  </g>')
    
    svg.append(f'  <g clip-path="url(#clip-line2)">')
    svg.append(f'    <text x="15" y="75" class="typing-text line2">{xml_escape(line2_text)}</text>')
    svg.append('  </g>')
    
    # Cursor 1 Animation (active from 0.5s to 2.5s, then hidden)
    svg.append(f'  <rect x="15" y="20" width="3" height="28" fill="{cursor_color}" opacity="0">')
    # Move cursor matching the typing speed
    svg.append(f'    <animate attributeName="x" from="15" to="{l1_width + 12}" dur="2s" begin="0.5s" fill="freeze" calcMode="linear" />')
    # Blink cursor
    svg.append('    <animate attributeName="opacity" values="1;1;0;0;1" keyTimes="0;0.4;0.5;0.9;1" dur="0.8s" repeatCount="indefinite" />')
    # Hide after line 1 is typed
    svg.append('    <animate attributeName="visibility" to="hidden" begin="2.5s" fill="freeze" />')
    svg.append('  </rect>')
    
    # Cursor 2 Animation (blinks at start location, active from 2.5s onwards, continues blinking at end)
    svg.append(f'  <rect x="15" y="62" width="3" height="22" fill="{cursor_color}" opacity="0">')
    # Make visible when line 2 starts
    svg.append('    <animate attributeName="visibility" to="visible" begin="2.5s" fill="freeze" />')
    # Move cursor matching the typing speed of line 2
    svg.append(f'    <animate attributeName="x" from="15" to="{l2_width + 12}" dur="1.5s" begin="2.7s" fill="freeze" calcMode="linear" />')
    # Blink cursor indefinitely
    svg.append('    <animate attributeName="opacity" values="1;1;0;0;1" keyTimes="0;0.4;0.5;0.9;1" dur="0.8s" begin="2.5s" repeatCount="indefinite" />')
    svg.append('  </rect>')
    
    svg.append('</svg>')
    
    # Save file
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(svg))
        
    print(f"Successfully generated Typing Header SVG: {output_path}")
    return True

if __name__ == "__main__":
    import yaml
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_dir = os.path.dirname(script_dir)
    
    config_path = os.path.join(project_dir, "config.yml")
    with open(config_path, "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)
        
    output_path = os.path.join(project_dir, "assets", "typing_header.svg")
    generate_typing_header_svg(output_path, config)
