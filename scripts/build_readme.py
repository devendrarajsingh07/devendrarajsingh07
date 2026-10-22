import os
import sys
import yaml
from jinja2 import Template

# Import generators used by the current profile layout
from generate_neofetch import generate_neofetch_svg
from generate_showcase import (
    generate_banner_svg,
    generate_footer_svg,
    generate_icons,
    generate_project_card_svg,
    generate_orbit_svg,
)

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
    
    assets = os.path.join(project_dir, "assets")
    generate_banner_svg(os.path.join(assets, "banner.svg"), config, project_dir)
    generate_neofetch_svg(os.path.join(assets, "neofetch_panel.svg"), config)
    generate_orbit_svg(os.path.join(assets, "stack_orbit_dark.svg"), config, mode="dark")
    generate_orbit_svg(os.path.join(assets, "stack_orbit_light.svg"), config, mode="light")
    generate_project_card_svg(os.path.join(assets, "latest_project.svg"), config)
    generate_icons(os.path.join(assets, "icons"), config)
    generate_footer_svg(os.path.join(assets, "footer_wave.svg"), config)

    print("\n--- 2. Assembling README.md ---")
    
    # Load template
    if not os.path.exists(template_path):
        print(f"Error: Template not found at {template_path}!")
        sys.exit(1)
        
    with open(template_path, "r", encoding="utf-8") as f:
        template_content = f.read()
        
    # Compile template using Jinja2
    template = Template(template_content)
    
    rendered_readme = template.render(**config)
    
    # Save the output README.md
    with open(output_readme_path, "w", encoding="utf-8") as f:
        f.write(rendered_readme.rstrip() + "\n")
        
    print(f"Successfully generated README.md at: {output_readme_path}")

if __name__ == "__main__":
    main()
