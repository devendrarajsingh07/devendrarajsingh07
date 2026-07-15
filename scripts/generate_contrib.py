import os
import sys
import yaml
import requests
import datetime
import random

def get_mock_contributions():
    """Generate realistic mock contribution data for local development/testing."""
    print("No GITHUB_TOKEN found or API call failed. Generating premium mock contribution data...")
    today = datetime.date.today()
    start_date = today - datetime.timedelta(days=364)
    
    total_days = 365
    contributions = []
    
    # Generate mock dates and count
    current_date = start_date
    total_count = 0
    longest_streak = 0
    current_streak = 0
    
    for i in range(total_days):
        # Weekdays have higher probability of contributions
        weekday = current_date.weekday()
        if weekday < 5: # Mon-Fri
            prob = 0.7
            max_val = 12
        else: # Sat-Sun
            prob = 0.3
            max_val = 4
            
        if random.random() < prob:
            count = random.randint(1, max_val)
            current_streak += 1
            if current_streak > longest_streak:
                longest_streak = current_streak
        else:
            count = 0
            current_streak = 0
            
        total_count += count
        contributions.append({
            "date": current_date.strftime("%Y-%m-%d"),
            "count": count
        })
        current_date += datetime.timedelta(days=1)
        
    return {
        "total": total_count,
        "days": contributions,
        "longest_streak": longest_streak,
        "current_streak": current_streak
    }

def fetch_github_contributions(username, token):
    """Fetch user contributions from GitHub GraphQL API."""
    url = "https://api.github.com/graphql"
    headers = {"Authorization": f"Bearer {token}"}
    
    query = """
    query($username: String!) {
      user(login: $username) {
        contributionsCollection {
          contributionCalendar {
            totalContributions
            weeks {
              contributionDays {
                contributionCount
                date
              }
            }
          }
        }
      }
    }
    """
    
    variables = {"username": username}
    
    try:
        response = requests.post(url, json={"query": query, "variables": variables}, headers=headers, timeout=10)
        if response.status_code != 200:
            print(f"GraphQL request failed with status {response.status_code}")
            return None
            
        data = response.json()
        if "errors" in data:
            print(f"GraphQL errors: {data['errors']}")
            return None
            
        calendar = data["data"]["user"]["contributionsCollection"]["contributionCalendar"]
        
        # Flatten days
        days = []
        longest_streak = 0
        current_streak = 0
        
        for week in calendar["weeks"]:
            for day in week["contributionDays"]:
                count = day["contributionCount"]
                days.append({
                    "date": day["date"],
                    "count": count
                })
                
                # Simple streak calculation
                if count > 0:
                    current_streak += 1
                    if current_streak > longest_streak:
                        longest_streak = current_streak
                else:
                    current_streak = 0
                    
        return {
            "total": calendar["totalContributions"],
            "days": days,
            "longest_streak": longest_streak,
            "current_streak": current_streak
        }
    except Exception as e:
        print(f"Network error fetching contributions: {e}")
        return None

def generate_contrib_svg(output_path, config):
    username = config.get("username", "devendrarajsingh07")
    token = os.environ.get("GITHUB_TOKEN")
    
    data = None
    if token:
        data = fetch_github_contributions(username, token)
        
    if not data:
        data = get_mock_contributions()
        
    # Get config theme
    theme = config.get("theme", {})
    bg_color = theme.get("background", "#1a1b26")
    fg_color = theme.get("foreground", "#a9b1d6")
    title_color = theme.get("title", "#7aa2f7")
    
    # Define a color ramp based on theme settings
    # Levels of contribution: 0, 1, 2, 3, 4+
    # Tokyonight colors: bg, blue_dim, purple, cyan, pink
    color_levels = [
        "#1e2030", # Level 0
        "#3b4261", # Level 1
        "#7aa2f7", # Level 2
        "#bb9af7", # Level 3
        "#ff007f"  # Level 4 (peak)
    ]
    
    # Build the calendar grid
    # A standard contribution graph shows 53 columns (weeks) of 7 rows (days, Sunday to Saturday)
    # Convert flat list of days to columns
    # Find weekday of the first element to align it correctly
    first_date_str = data["days"][0]["date"]
    first_date = datetime.datetime.strptime(first_date_str, "%Y-%m-%d").date()
    # first_date.strftime("%w") returns '0' for Sunday, '6' for Saturday
    start_offset = (first_date.weekday() + 1) % 7  # 0 = Sunday, 1 = Monday ... 6 = Saturday
    
    # Pad the start with empty slots
    grid_days = [{"count": -1} for _ in range(start_offset)]
    for d in data["days"]:
        grid_days.append(d)
        
    # Chunk into weeks (7 days each)
    weeks = [grid_days[i:i+7] for i in range(0, len(grid_days), 7)]
    
    # SVG Configuration
    box_size = 10
    gap = 3
    padding_x = 20
    padding_y = 25
    
    graph_width = len(weeks) * (box_size + gap) - gap
    svg_width = graph_width + padding_x * 2
    
    # Height details: days (7 * 13) + headers + footer
    graph_height = 7 * (box_size + gap) - gap
    svg_height = graph_height + padding_y * 2 + 35
    
    svg = []
    svg.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {svg_width} {svg_height}" width="{svg_width}" height="{svg_height}">')
    
    # Styles for animation
    svg.append('  <style>')
    svg.append('    .text {')
    svg.append('      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif;')
    svg.append('      font-size: 11px;')
    svg.append(f'      fill: {fg_color};')
    svg.append('    }')
    svg.append('    .title {')
    svg.append('      font-weight: 600;')
    svg.append('      font-size: 13px;')
    svg.append(f'      fill: {title_color};')
    svg.append('    }')
    svg.append('    .day {')
    svg.append('      transform-origin: center;')
    svg.append('      animation: scaleIn 0.4s ease-out both;')
    svg.append('    }')
    svg.append('    @keyframes scaleIn {')
    svg.append('      from { opacity: 0; transform: scale(0.3); }')
    svg.append('      to { opacity: 1; transform: scale(1); }')
    svg.append('    }')
    svg.append('  </style>')
    
    # Background
    svg.append(f'  <rect width="100%" height="100%" fill="{bg_color}" rx="8" />')
    
    # Title
    svg.append(f'  <text x="{padding_x}" y="20" class="text title">Contribution Heatmap ({username})</text>')
    
    # Grid container
    svg.append(f'  <g transform="translate({padding_x}, {padding_y + 15})">')
    
    # Render cells
    for col_idx, week in enumerate(weeks):
        for row_idx, day in enumerate(week):
            if day["count"] == -1: # Padding
                continue
                
            count = day["count"]
            # Map count to color level
            if count == 0:
                color = color_levels[0]
            elif count <= 2:
                color = color_levels[1]
            elif count <= 5:
                color = color_levels[2]
            elif count <= 9:
                color = color_levels[3]
            else:
                color = color_levels[4]
                
            x = col_idx * (box_size + gap)
            y = row_idx * (box_size + gap)
            
            # Staggered animation delay based on x coordinate
            delay = col_idx * 0.015 + row_idx * 0.005
            
            svg.append(f'    <rect class="day" x="{x}" y="{y}" width="{box_size}" height="{box_size}" rx="2" fill="{color}" style="animation-delay: {delay:.3f}s;">')
            svg.append(f'      <title>{day.get("date", "")}: {count} contributions</title>')
            svg.append(f'    </rect>')
            
    svg.append('  </g>')
    
    # Footer info
    footer_y = svg_height - 15
    svg.append(f'  <text x="{padding_x}" y="{footer_y}" class="text">')
    svg.append(f'    Total: <tspan font-weight="bold" fill="{title_color}">{data["total"]}</tspan> | ')
    svg.append(f'    Longest Streak: <tspan font-weight="bold" fill="{title_color}">{data["longest_streak"]} days</tspan>')
    svg.append(f'  </text>')
    
    # Legend
    legend_start_x = svg_width - padding_x - 110
    svg.append(f'  <g transform="translate({legend_start_x}, {footer_y - 9})">')
    svg.append(f'    <text x="0" y="8" class="text" font-size="9">Less</text>')
    for idx, color in enumerate(color_levels):
        lx = 28 + idx * (box_size + 2)
        svg.append(f'    <rect x="{lx}" y="0" width="{box_size}" height="{box_size}" rx="2" fill="{color}" />')
    svg.append(f'    <text x="92" y="8" class="text" font-size="9">More</text>')
    svg.append('  </g>')
    
    svg.append('</svg>')
    
    # Save file
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(svg))
        
    print(f"Successfully generated Contributions Graph SVG: {output_path}")
    return True

if __name__ == "__main__":
    # Get paths
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_dir = os.path.dirname(script_dir)
    
    config_path = os.path.join(project_dir, "config.yml")
    with open(config_path, "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)
        
    output_path = os.path.join(project_dir, "assets", "contrib_graph.svg")
    
    generate_contrib_svg(output_path, config)
