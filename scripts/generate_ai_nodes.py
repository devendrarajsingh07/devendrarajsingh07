import os

def generate_ai_nodes_svg(output_path, config):
    theme = config.get("theme", {})
    bg_color = theme.get("background", "#1a1b26")
    title_color = theme.get("title", "#7aa2f7")      # blue
    label_color = theme.get("label", "#bb9af7")      # purple
    cursor_color = theme.get("cursor", "#ff007f")    # pink
    accent_color = "#7dcfff"                          # cyan
    
    width = 600
    height = 200
    
    svg = []
    svg.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="{width}" height="{height}">')
    
    # Styles for pulsing and glowing
    svg.append('  <style>')
    svg.append('    .node {')
    svg.append('      animation: pulse 3s ease-in-out infinite;')
    svg.append('      transform-origin: center;')
    svg.append('    }')
    svg.append('    .pulse-slow { animation-duration: 4s; }')
    svg.append('    .pulse-fast { animation-duration: 2s; }')
    
    svg.append('    @keyframes pulse {')
    svg.append('      0%, 100% { r: 5px; opacity: 0.7; }')
    svg.append('      50% { r: 8px; opacity: 1; filter: drop-shadow(0 0 4px currentColor); }')
    svg.append('    }')
    
    svg.append('    .connection {')
    svg.append('      stroke-opacity: 0.15;')
    svg.append('      stroke-width: 1;')
    svg.append('    }')
    
    svg.append('    .signal {')
    svg.append('      stroke-dasharray: 8 50;')
    svg.append('      stroke-width: 1.5;')
    svg.append('      animation: signal-run 3s linear infinite;')
    svg.append('    }')
    
    svg.append('    @keyframes signal-run {')
    svg.append('      from { stroke-dashoffset: 58; }')
    svg.append('      to { stroke-dashoffset: 0; }')
    svg.append('    }')
    svg.append('  </style>')
    
    # Glow filter
    svg.append('  <defs>')
    svg.append('    <filter id="glow" x="-20%" y="-20%" width="140%" height="140%">')
    svg.append('      <feGaussianBlur stdDeviation="3" result="blur" />')
    svg.append('      <feComposite in="SourceGraphic" in2="blur" operator="over" />')
    svg.append('    </filter>')
    svg.append('  </defs>')
    
    # Background Card
    svg.append(f'  <rect width="100%" height="100%" fill="{bg_color}" rx="8" />')
    
    # Title
    svg.append(f'  <text x="20" y="25" fill="{title_color}" font-family="monospace" font-size="11" font-weight="bold">neural_network_simulation.py</text>')
    
    # Define Nodes (3 layers: Input (3), Hidden1 (4), Hidden2 (3), Output (2))
    layers = [
        # Input Layer
        [(80, 50), (80, 100), (80, 150)],
        # Hidden Layer 1
        [(220, 40), (220, 80), (220, 120), (220, 160)],
        # Hidden Layer 2
        [(380, 50), (380, 100), (380, 150)],
        # Output Layer
        [(520, 75), (520, 125)]
    ]
    
    # Colors for layers
    layer_colors = [title_color, label_color, accent_color, cursor_color]
    
    # Draw connections & signal flows between layers
    import math
    signal_idx = 0
    for l in range(len(layers) - 1):
        curr_layer = layers[l]
        next_layer = layers[l+1]
        
        for n1 in curr_layer:
            for n2 in next_layer:
                # Basic connection line
                svg.append(f'  <line class="connection" x1="{n1[0]}" y1="{n1[1]}" x2="{n2[0]}" y2="{n2[1]}" stroke="{layer_colors[l]}" />')
                
                # Add animated signals on a subset of connections to avoid clutter
                if (n1[1] + n2[1]) % 3 == 0:
                    # Stagger duration of signals
                    dur = 2.0 + (signal_idx % 3) * 0.5
                    color = layer_colors[l+1]
                    svg.append(f'  <line class="signal" x1="{n1[0]}" y1="{n1[1]}" x2="{n2[0]}" y2="{n2[1]}" stroke="{color}" style="animation-duration: {dur}s;" />')
                    signal_idx += 1
                    
    # Draw nodes on top of connections
    for l_idx, layer in enumerate(layers):
        color = layer_colors[l_idx]
        for n_idx, (x, y) in enumerate(layer):
            pulse_class = "pulse-slow" if n_idx % 3 == 0 else ("pulse-fast" if n_idx % 3 == 1 else "")
            svg.append(f'  <circle class="node {pulse_class}" cx="{x}" cy="{y}" r="6" fill="{color}" style="color: {color};" />')
            
    svg.append('</svg>')
    
    # Save file
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(svg))
        
    print(f"Successfully generated AI Nodes SVG: {output_path}")
    return True

if __name__ == "__main__":
    import yaml
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_dir = os.path.dirname(script_dir)
    
    config_path = os.path.join(project_dir, "config.yml")
    with open(config_path, "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)
        
    output_path = os.path.join(project_dir, "assets", "ai_nodes.svg")
    generate_ai_nodes_svg(output_path, config)
