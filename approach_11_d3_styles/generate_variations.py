#!/usr/bin/env python3
"""
Generate multiple phylogenetic tree variations for comparison
Each variation uses a different layout algorithm and aesthetic
"""

import json

# Base HTML template
BASE_TEMPLATE = '''<!DOCTYPE html>
<html><head><meta charset="UTF-8">
<title>AI Evolution - {title}</title>
<script src="https://d3js.org/d3.v7.min.js"></script>
<style>{styles}</style>
</head><body>
<div class="info">{info}</div>
<div id="viz"></div>
<script>{script}</script>
</body></html>'''

# Variation B: Horizontal Dense Timeline
variation_b = {
    "title": "Variation B: Horizontal Dense Timeline",
    "styles": """
body {{margin:0;padding:20px;font-family:Georgia,serif;background:#faf8f5;}}
.info {{position:fixed;top:20px;left:20px;background:rgba(255,255,255,0.95);padding:15px;border-radius:6px;max-width:250px;font-size:11px;box-shadow:0 2px 8px rgba(0,0,0,0.1);}}
svg {{display:block;}}
.branch {{fill:none;stroke-linecap:round;}}
.node circle {{stroke:#fff;stroke-width:1;}}
.label {{font-size:9px;fill:#333;}}
""",
    "info": "<h3>Horizontal Timeline</h3><p>Time flows left→right. Dense vertical packing. Traditional phylogenetic tree structure.</p>",
    "layout": "horizontal"
}

# Variation C: Ultra-Dense Circular
variation_c = {
    "title": "Variation C: Ultra-Dense Circular",
    "styles": """
body {{margin:0;padding:40px;font-family:Georgia,serif;background:#0a0a0a;display:flex;justify-content:center;align-items:center;min-height:100vh;}}
.info {{position:fixed;top:30px;right:30px;background:rgba(255,255,255,0.1);padding:15px;border-radius:6px;max-width:250px;font-size:11px;color:#fff;border:1px solid rgba(255,255,255,0.2);}}
svg {{display:block;}}
.branch {{fill:none;stroke-linecap:round;opacity:0.7;}}
.node circle {{stroke:#fff;stroke-width:0.5;}}
.label {{font-size:8px;fill:#fff;text-shadow:0 0 3px #000;}}
""",
    "info": "<h3>Ultra-Dense Circular</h3><p>Maximum density. Full 360° layout. All 114 models visible. Emphasizes explosive growth post-2017.</p>",
    "layout": "circular_dense"
}

# Variation D: Vertical Dendrogram
variation_d = {
    "title": "Variation D: Vertical Dendrogram",
    "styles": """
body {{margin:0;padding:30px;font-family:'Palatino',serif;background:linear-gradient(to bottom,#f5f5f5,#e8e8e8);}}
.info {{position:fixed;top:30px;left:30px;background:rgba(255,255,255,0.95);padding:15px;border-radius:6px;max-width:250px;font-size:11px;box-shadow:0 2px 8px rgba(0,0,0,0.1);}}
svg {{display:block;margin:0 auto;}}
.branch {{fill:none;stroke-linecap:round;opacity:0.8;}}
.node circle {{stroke:#fff;stroke-width:1.5;}}
.label {{font-size:9px;fill:#2c3e50;font-weight:500;}}
""",
    "info": "<h3>Vertical Dendrogram</h3><p>Time flows bottom→top. Strict hierarchical structure. Clean, organized branching.</p>",
    "layout": "vertical_dendro"
}

# Variation E: Organic Hand-Drawn
variation_e = {
    "title": "Variation E: Organic Hand-Drawn",
    "styles": """
body {{margin:0;padding:40px;font-family:'Brush Script MT',cursive;background:#fffef9;}}
.info {{position:fixed;top:30px;right:30px;background:rgba(255,255,255,0.9);padding:18px;border-radius:8px;max-width:260px;font-size:11px;box-shadow:0 3px 12px rgba(0,0,0,0.15);border:2px solid #d4c5a9;font-family:Georgia,serif;}}
svg {{display:block;filter:url(#paper-texture);}}
.branch {{fill:none;stroke-linecap:round;stroke-linejoin:round;opacity:0.75;}}
.node circle {{stroke:#444;stroke-width:1.2;filter:url(#sketch);}}
.label {{font-size:10px;fill:#2a2a2a;font-family:Georgia,serif;font-style:italic;}}
""",
    "info": "<h3>Organic Hand-Drawn</h3><p>Artistic, sketch-like aesthetic. Natural flowing curves. Museum illustration style.</p>",
    "layout": "organic"
}

# Variation F: Transformer Explosion
variation_f = {
    "title": "Variation F: Transformer Explosion",
    "styles": """
body {{margin:0;padding:40px;font-family:'Futura',sans-serif;background:radial-gradient(circle,#1a1a2e,#0f0f1e);display:flex;justify-content:center;align-items:center;min-height:100vh;}}
.info {{position:fixed;top:30px;left:30px;background:rgba(0,0,0,0.8);padding:15px;border-radius:6px;max-width:250px;font-size:11px;color:#fff;border:1px solid rgba(255,255,255,0.3);}}
svg {{display:block;}}
.branch {{fill:none;stroke-linecap:round;opacity:0.8;filter:drop-shadow(0 0 2px currentColor);}}
.node circle {{stroke:#fff;stroke-width:1;}}
.label {{font-size:9px;fill:#fff;text-shadow:0 0 5px #000;}}
""",
    "info": "<h3>Transformer Explosion</h3><p>Dramatic starburst radiating from 2017 transformer revolution. High visual impact.</p>",
    "layout": "explosion"
}

variations = [variation_b, variation_c, variation_d, variation_e, variation_f]

print(f"Will generate {len(variations)} variations")
print("Ready to create HTML files...")
