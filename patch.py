import re

with open("index.html", "r", encoding="utf-8") as f:
    html = f.read()

with open("hero.html", "r", encoding="utf-8") as f:
    hero_html = f.read()

# 1. Remove Hero Background Animation
html = re.sub(r'<!-- Hero Background Animation -->\s*<div class="hero-bg-wrapper">.*?</div>\s*', '', html, flags=re.DOTALL)

# 2. Replace Hero Section and Video Explainer Section with the new Hero HTML
html = re.sub(r'<!-- Hero Section -->.*?<!-- Core Technologies Grid -->', hero_html + '\n\n    <!-- Core Technologies Grid -->', html, flags=re.DOTALL)

# 3. Add JS
js_code = """
        /* Generate twinkling stars */
        const starsEl = document.getElementById('arStars');
        if (starsEl) {
            for (let i = 0; i < 120; i++) {
                const s = document.createElement('div');
                s.className = 'ar-star';
                const size = Math.random() * 2.5 + 1;
                s.style.cssText = `
                left:${Math.random()*100}%;
                top:${Math.random()*100}%;
                width:${size}px;
                height:${size}px;
                --d:${(Math.random()*4+2).toFixed(1)}s;
                --o:${(Math.random()*0.5+0.1).toFixed(2)};
                animation-delay:${(Math.random()*5).toFixed(1)}s;
                `;
                starsEl.appendChild(s);
            }
        }
    </script>
</body>"""

html = html.replace('</script>\n</body>', js_code)

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html)

print("Patch applied successfully.")
