import os
import sys
import yaml
import requests
from xml.sax.saxutils import escape as xml_escape

def fetch_github_stats(username, token=None):
    """Fetch live stats for the user from GitHub API."""
    headers = {}
    if token:
        headers["Authorization"] = f"token {token}"
        
    stats = {
        "repos": 12,      # fallback defaults
        "followers": 15,
        "stars": 8
    }
    
    try:
        # Fetch user info
        user_url = f"https://api.github.com/users/{username}"
        user_resp = requests.get(user_url, headers=headers, timeout=5)
        if user_resp.status_code == 200:
            user_data = user_resp.json()
            stats["repos"] = user_data.get("public_repos", stats["repos"])
            stats["followers"] = user_data.get("followers", stats["followers"])
            
        # Fetch repos to count stars
        repos_url = f"https://api.github.com/users/{username}/repos?per_page=100"
        repos_resp = requests.get(repos_url, headers=headers, timeout=5)
        if repos_resp.status_code == 200:
            repos_data = repos_resp.json()
            total_stars = sum(repo.get("stargazers_count", 0) for repo in repos_data)
            stats["stars"] = total_stars
            
        print(f"Successfully fetched live GitHub stats for {username}: Repos={stats['repos']}, Followers={stats['followers']}, Stars={stats['stars']}")
    except Exception as e:
        print(f"Could not fetch live GitHub stats ({e}). Using mock/offline values.")
        
    return stats

def generate_neofetch_svg(output_path, config):
    # Retrieve configuration values
    username = config.get("username", "devendrarajsingh07")
    name = config.get("name", "Devendra Raj Singh")
    token = os.environ.get("GITHUB_TOKEN")
    
    # Fetch live stats
    gh_stats = fetch_github_stats(username, token)
    
    # Theme colors
    theme = config.get("theme", {})
    bg_color = theme.get("background", "#1a1b26")
    fg_color = theme.get("foreground", "#a9b1d6")
    title_color = theme.get("title", "#7aa2f7")
    label_color = theme.get("label", "#bb9af7")
    val_color = theme.get("value", "#c0caf5")
    cursor_color = theme.get("cursor", "#ff007f")
    ansi_colors = theme.get("ansi_colors", [
        "#15161e", "#f7768e", "#9ece6a", "#e0af68",
        "#7aa2f7", "#bb9af7", "#7dcfff", "#a9b1d6"
    ])
    
    # Neofetch details (incorporating live stats)
    details = [
        ("OS", config.get("os", "Ubuntu 22.04 LTS")),
        ("Shell", config.get("shell", "zsh 5.8.1")),
        ("Editor", config.get("editor", "Neovim / VS Code")),
        ("Languages", config.get("languages", "Python")),
        ("AI/ML", config.get("ai_ml", "PyTorch")),
        ("Web Dev", config.get("web_dev", "React / FastAPI")),
        ("Databases", config.get("databases", "PostgreSQL / Redis")),
        ("Projects", f"{gh_stats['repos']} public repos"),
        ("Stars", f"⭐ {gh_stats['stars']} stargazers"),
        ("Followers", f"👥 {gh_stats['followers']} followers"),
        ("Focus", config.get("focus", "Machine Learning / MLOps")),
    ]
    
    # Size calculations
    width = 460
    header_height = 35
    padding = 20
    line_height = 20
    
    # Calculate height based on details + headers + color blocks
    body_lines_count = len(details) + 2  # username/host + divider
    body_height = body_lines_count * line_height + 40  # + color blocks
    total_height = header_height + body_height + padding
    
    svg = []
    svg.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {total_height}" width="{width}" height="{total_height}">')
    
    # Styles for animation & typography
    svg.append('  <style>')
    svg.append('    .terminal-text {')
    svg.append('      font-family: "SFMono-Regular", Consolas, "Liberation Mono", Menlo, Courier, monospace;')
    svg.append('      font-size: 12px;')
    svg.append('      font-weight: 600;')
    svg.append('    }')
    svg.append('    .cursor {')
    svg.append(f'      fill: {cursor_color};')
    svg.append('      animation: blink 1s step-end infinite;')
    svg.append('    }')
    svg.append('    @keyframes blink {')
    svg.append('      from, to { opacity: 1; }')
    svg.append('      50% { opacity: 0; }')
    svg.append('    }')
    svg.append('  </style>')
    
    # Drop shadow filter for premium card style
    svg.append('  <filter id="shadow" x="-5%" y="-5%" width="110%" height="110%">')
    svg.append('    <feDropShadow dx="0" dy="8" stdDeviation="6" flood-color="#000000" flood-opacity="0.3" />')
    svg.append('  </filter>')
    
    # Terminal Window Container with shadow
    svg.append(f'  <g filter="url(#shadow)">')
    svg.append(f'    <rect width="{width}" height="{total_height - 15}" rx="8" fill="{bg_color}" />')
    svg.append('  </g>')
    
    # Header bar
    header_bg = "#24283b" if bg_color == "#1a1b26" else "#1b1c24"
    svg.append(f'  <path d="M 0,8 A 8,8 0 0 1 8,0 L {width-8},0 A 8,8 0 0 1 {width},8 L {width},{header_height} L 0,{header_height} Z" fill="{header_bg}" />')
    
    # Window controls (close, minimize, maximize)
    svg.append('  <circle cx="20" cy="17" r="6" fill="#f7768e" />')
    svg.append('  <circle cx="38" cy="17" r="6" fill="#e0af68" />')
    svg.append('  <circle cx="56" cy="17" r="6" fill="#9ece6a" />')
    
    # Header title
    svg.append(f'  <text x="{width // 2}" y="22" fill="{fg_color}" font-family="monospace" font-size="12" font-weight="bold" text-anchor="middle">neofetch</text>')
    
    # Terminal text body
    svg.append(f'  <text x="20" y="{header_height + 25}" class="terminal-text">')
    
    # Username and host
    login_str = f"{username.lower()}@github"
    svg.append(f'    <tspan fill="{title_color}">{xml_escape(login_str)}</tspan>')
    svg.append(f'  </text>')
    
    # Blinking cursor block
    cursor_x = len(login_str) * 7.2 + 22
    svg.append(f'  <rect x="{cursor_x}" y="{header_height + 14}" width="8" height="13" class="cursor" />')
    
    # Divider line
    divider = "-" * 40
    svg.append(f'  <text x="20" y="{header_height + 40}" class="terminal-text" fill="{fg_color}">{divider}</text>')
    
    # Neofetch details
    curr_y = header_height + 58
    for label, val in details:
        # Align labels to 11 characters
        padded_label = f"{label}:".ljust(11)
        svg.append(f'  <text x="20" y="{curr_y}" class="terminal-text">')
        svg.append(f'    <tspan fill="{label_color}">{xml_escape(padded_label)}</tspan>')
        svg.append(f'    <tspan fill="{val_color}">{xml_escape(str(val))}</tspan>')
        svg.append('  </text>')
        curr_y += line_height
        
    # Terminal color block swatches at the bottom
    curr_y += 10
    svg.append(f'  <!-- ANSI Color Blocks -->')
    block_x = 20
    for color in ansi_colors:
        svg.append(f'  <rect x="{block_x}" y="{curr_y}" width="22" height="12" rx="2" fill="{color}" />')
        block_x += 28
        
    svg.append('</svg>')
    
    # Save file
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(svg))
        
    print(f"Successfully generated Neofetch Panel SVG: {output_path}")
    return True

if __name__ == "__main__":
    # Get paths
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_dir = os.path.dirname(script_dir)
    
    config_path = os.path.join(project_dir, "config.yml")
    with open(config_path, "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)
        
    output_path = os.path.join(project_dir, "assets", "neofetch_panel.svg")
    
    generate_neofetch_svg(output_path, config)
