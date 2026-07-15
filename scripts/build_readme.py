import os
import sys
import yaml
from jinja2 import Template

# Import generators
from generate_ascii import generate_ascii_svg
from generate_neofetch import generate_neofetch_svg
from generate_contrib import generate_contrib_svg
from generate_typing_header import generate_typing_header_svg
from generate_wave import generate_wave_svg
from generate_ai_nodes import generate_ai_nodes_svg

def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_dir = os.path.dirname(script_dir)
    
    config_path = os.path.join(project_dir, "config.yml")
    template_path = os.path.join(project_dir, "README.template")
    output_readme_path = os.path.join(project_dir, "README.md")
    
    # 1. Load config
    if not os.path.exists(config_path):
        print(f"Error: {config_path} not found!")
        sys.exit(1)
        
    with open(config_path, "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)
        
    print("--- 1. Generating SVG Assets ---")
    
    # Paths for output SVGs
    photo_path = os.path.join(project_dir, "assets", "photo.jpg")
    ascii_svg_path = os.path.join(project_dir, "assets", "ascii_portrait.svg")
    neofetch_svg_path = os.path.join(project_dir, "assets", "neofetch_panel.svg")
    contrib_svg_path = os.path.join(project_dir, "assets", "contrib_graph.svg")
    typing_svg_path = os.path.join(project_dir, "assets", "typing_header.svg")
    wave_svg_path = os.path.join(project_dir, "assets", "wave_divider.svg")
    ai_nodes_svg_path = os.path.join(project_dir, "assets", "ai_nodes.svg")
    
    # Run ASCII generator if photo exists
    if os.path.exists(photo_path):
        generate_ascii_svg(photo_path, ascii_svg_path, config)
    else:
        print(f"Warning: Photo not found at {photo_path}. Skipping ASCII portrait generation.")
        
    # Run Neofetch generator
    generate_neofetch_svg(neofetch_svg_path, config)
    
    # Run Contribution Graph generator
    generate_contrib_svg(contrib_svg_path, config)
    
    # Run Typing Header generator
    generate_typing_header_svg(typing_svg_path, config)
    
    # Run Wave Divider generator
    generate_wave_svg(wave_svg_path, config)
    
    # Run AI Nodes generator
    generate_ai_nodes_svg(ai_nodes_svg_path, config)
    
    print("\n--- 2. Assembling README.md ---")
    
    # Load template
    if not os.path.exists(template_path):
        print(f"Error: Template not found at {template_path}!")
        sys.exit(1)
        
    with open(template_path, "r", encoding="utf-8") as f:
        template_content = f.read()
        
    # Compile template using Jinja2
    template = Template(template_content)
    
    # Add helper for current date/time to template variables
    import datetime
    now_str = datetime.datetime.now().strftime("%B %d, %Y")
    
    rendered_readme = template.render(
        **config,
        last_updated=now_str
    )
    
    # Save the output README.md
    with open(output_readme_path, "w", encoding="utf-8") as f:
        f.write(rendered_readme)
        
    print(f"Successfully generated README.md at: {output_readme_path}")

if __name__ == "__main__":
    main()
