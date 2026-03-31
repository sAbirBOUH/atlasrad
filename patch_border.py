import re

with open("index.html", "r", encoding="utf-8") as f:
    html = f.read()

top_border_svg = """    <svg width="100%" height="100%" xmlns="http://www.w3.org/2000/svg">
      <defs>
        <g id="nav-star">
          <polygon points="0,-12 2,-2 12,0 2,2 0,12 -2,2 -12,0 -2,-2" fill="#9c7a38" />
          <polygon points="0,-8 1.5,-1.5 8,0 1.5,1.5 0,8 -1.5,1.5 -8,0 -1.5,-1.5" fill="#9c7a38" transform="rotate(45)" />
        </g>
        <pattern id="star-pattern" x="0" y="0" width="80" height="52" patternUnits="userSpaceOnUse">
          <use href="#nav-star" x="40" y="26" />
        </pattern>
      </defs>
      <rect x="0" y="0" width="100%" height="100%" fill="#0B1E3D"/>
      <rect x="0" y="0" width="100%" height="100%" fill="url(#star-pattern)"/>
      <line x1="0" y1="51" x2="100%" y2="51" stroke="#C5922A" stroke-width="2" opacity="0.8"/>
    </svg>"""

bottom_border_svg = """    <svg width="100%" height="100%" xmlns="http://www.w3.org/2000/svg">
      <defs>
        <g id="nav-star">
          <polygon points="0,-12 2,-2 12,0 2,2 0,12 -2,2 -12,0 -2,-2" fill="#9c7a38" />
          <polygon points="0,-8 1.5,-1.5 8,0 1.5,1.5 0,8 -1.5,1.5 -8,0 -1.5,-1.5" fill="#9c7a38" transform="rotate(45)" />
        </g>
        <pattern id="star-pattern" x="0" y="0" width="80" height="52" patternUnits="userSpaceOnUse">
          <use href="#nav-star" x="40" y="26" />
        </pattern>
      </defs>
      <rect x="0" y="0" width="100%" height="100%" fill="#0B1E3D"/>
      <rect x="0" y="0" width="100%" height="100%" fill="url(#star-pattern)"/>
      <line x1="0" y1="1" x2="100%" y2="1" stroke="#C5922A" stroke-width="2" opacity="0.8"/>
    </svg>"""

# Replace top border
html = re.sub(r'<!-- Moroccan border top -->\s*<div class="ar-border-top">.*?</div>',
              f'<!-- Moroccan border top -->\n  <div class="ar-border-top">\n{top_border_svg}\n  </div>',
              html, flags=re.DOTALL)

# Replace bottom border
html = re.sub(r'<!-- Moroccan border bottom -->\s*<div class="ar-border-bottom">.*?</div>',
              f'<!-- Moroccan border bottom -->\n  <div class="ar-border-bottom">\n{bottom_border_svg}\n  </div>',
              html, flags=re.DOTALL)

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html)

print("Border patched successfully.")
