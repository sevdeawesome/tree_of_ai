#!/usr/bin/env python3
"""
ETE3 Beautiful Phylogenetic Tree - Truly Artistic
Using ETE3's built-in phylogenetic tree rendering for maximum beauty
"""

from ete3 import Tree, TreeStyle, NodeStyle, TextFace, faces, AttrFace
import sys
import os

sys.path.insert(0, '../../data')
from ai_models import AI_MODELS

os.makedirs("../output", exist_ok=True)

print("="*80)
print("CREATING BEAUTIFUL PHYLOGENETIC TREE WITH ETE3")
print("Scientific-grade visualization library")
print("="*80)

# Build tree in Newick format (ETE3's native format)
def build_newick_tree(models):
    """Convert our data to Newick tree format"""

    # Build dictionary
    tree_dict = {}
    for model_data in models:
        name, parent, year, color, importance, branch_type, extinct = model_data
        # Clean name for Newick (no spaces, special chars)
        clean_name = name.replace(' ', '_').replace('-', '_').replace('.', '_')
        tree_dict[clean_name] = {
            'parent': parent.replace(' ', '_').replace('-', '_').replace('.', '_') if parent else None,
            'year': year,
            'color': color,
            'importance': importance,
            'branch_type': branch_type,
            'extinct': extinct,
            'original_name': name,
            'children': []
        }

    # Link children
    for name, data in tree_dict.items():
        if data['parent'] and data['parent'] in tree_dict:
            tree_dict[data['parent']]['children'].append(name)

    # Build Newick recursively
    def build_newick(name):
        node = tree_dict[name]
        branch_length = (node['year'] - 1958) / 10.0  # Scale years

        if not node['children']:
            return f"{name}:{branch_length}"
        else:
            children_newick = ','.join([build_newick(child) for child in node['children']])
            return f"({children_newick}){name}:{branch_length}"

    newick = build_newick("Perceptron") + ";"
    return newick, tree_dict

print("\n🌳 Building tree structure...")
newick_str, tree_metadata = build_newick_tree(AI_MODELS)
print(f"✓ Created Newick tree with {len(AI_MODELS)} models")

# Load tree
t = Tree(newick_str, format=1)

# Apply beautiful styling
def style_tree_beautifully(tree, metadata):
    """Apply gorgeous styling to every node"""

    print("\n🎨 Applying beautiful styling...")

    for node in tree.traverse():
        # Get metadata
        node_name = node.name if node.name else "root"
        if node_name in metadata:
            data = metadata[node_name]

            # Node style
            nstyle = NodeStyle()
            nstyle["size"] = 0  # Hide default node

            # Branch color and width based on importance
            nstyle["hz_line_color"] = data['color']
            nstyle["vt_line_color"] = data['color']
            nstyle["hz_line_width"] = data['importance'] * 2
            nstyle["vt_line_width"] = data['importance'] * 2

            # Lighter color for extinct branches
            if data['extinct']:
                # ETE3 doesn't support opacity, use lighter color
                import matplotlib.colors as mcolors
                rgb = mcolors.hex2color(data['color'])
                lighter = tuple(min(1, c + 0.5) for c in rgb)
                nstyle["hz_line_color"] = mcolors.rgb2hex(lighter)
                nstyle["vt_line_color"] = mcolors.rgb2hex(lighter)

            # Make branches smooth
            nstyle["hz_line_type"] = 0  # Solid
            nstyle["vt_line_type"] = 0

            node.set_style(nstyle)

            # Add custom face for node (circle)
            if node.is_leaf():
                # Colored circle for terminal nodes
                circle_size = data['importance'] * 8
                circle = faces.CircleFace(
                    radius=circle_size,
                    color=data['color'],
                    style="sphere",
                    label={"text": "", "color": "black"}
                )
                node.add_face(circle, column=0, position="branch-right")

                # Beautiful label
                label_face = TextFace(
                    data['original_name'],
                    fsize=10 if data['importance'] >= 4 else 8,
                    fgcolor="#1A1A1A",
                    ftype="Georgia",
                    bold=data['importance'] >= 5
                )
                node.add_face(label_face, column=1, position="branch-right")
            else:
                # Internal nodes - smaller circles
                if data['importance'] >= 4:
                    circle = faces.CircleFace(
                        radius=data['importance'] * 6,
                        color=data['color'],
                        style="sphere"
                    )
                    node.add_face(circle, column=0, position="branch-bottom")

style_tree_beautifully(t, tree_metadata)

# Create beautiful tree style
ts = TreeStyle()

# Circular/radial mode for phylogenetic beauty
ts.mode = "c"  # Circular
ts.arc_start = -180
ts.arc_span = 360

# Layout
ts.show_leaf_name = False  # We added custom faces
ts.show_branch_length = False
ts.show_branch_support = False
ts.draw_guiding_lines = False
ts.allow_face_overlap = False  # Prevent label overlap!

# Beautiful background
ts.bgcolor = "#FCFCFA"

# Increase scale for better spacing
ts.scale = 120

# Optimal layout
ts.optimal_scale_level = "full"
ts.branch_vertical_margin = 15

# Title
title = TextFace("The Phylogenetic Tree of Artificial Intelligence", fsize=24, bold=True, fgcolor="#1C2833")
ts.title.add_face(title, column=0)

subtitle = TextFace("1958—2025 • Scientific Phylogenetic Visualization", fsize=14, fgcolor="#515A5A")
ts.title.add_face(subtitle, column=0)

# Legend
legend_html = """
<div style='font-family:Arial; font-size:10px; padding:10px; background:#FFF; border-radius:5px;'>
<b>Branch Colors:</b><br/>
<span style='color:#9370DB'>■</span> CNNs &nbsp;
<span style='color:#00CED1'>■</span> Transformers &nbsp;
<span style='color:#00BFFF'>■</span> GPT &nbsp;
<span style='color:#7B68EE'>■</span> Claude &nbsp;
<span style='color:#FF4500'>■</span> LLaMA<br/>
<span style='color:#008B8B'>■</span> Gemini &nbsp;
<span style='color:#FF1493'>■</span> Diffusion &nbsp;
<span style='color:#DC143C'>■</span> Chinese AI &nbsp;
<span style='color:#228B22'>■</span> RL
</div>
"""

print("\n🖼️  Rendering beautiful tree...")

try:
    # Render to PNG at high resolution
    t.render("../output/ai_tree_ete3_beautiful.png", w=4000, h=4000, dpi=300, tree_style=ts)
    print("✓ Saved: ai_tree_ete3_beautiful.png (4000x4000, 300 DPI)")

    # PDF for vector
    t.render("../output/ai_tree_ete3_beautiful.pdf", tree_style=ts)
    print("✓ Saved: ai_tree_ete3_beautiful.pdf (vector)")

    # SVG for web
    t.render("../output/ai_tree_ete3_beautiful.svg", tree_style=ts)
    print("✓ Saved: ai_tree_ete3_beautiful.svg (vector)")

except Exception as e:
    print(f"⚠️  Rendering error: {e}")
    print("Trying alternative rendering...")

    # Fallback - render with display mode
    t.render("../output/ai_tree_ete3_beautiful.png", tree_style=ts)
    print("✓ Saved: ai_tree_ete3_beautiful.png")

print("\n" + "="*80)
print("✨ ETE3 BEAUTIFUL TREE COMPLETE")
print("="*80)
print("\nFeatures:")
print("  ✓ Phylogenetic-grade visualization")
print("  ✓ Circular radial layout")
print("  ✓ Color-coded branches")
print("  ✓ Variable branch thickness")
print("  ✓ Beautiful node styling")
print("  ✓ Professional typography")
print("  ✓ 4000x4000 px, 300 DPI")
print("\n🎨 ETE3 is THE tool for phylogenetic trees!")
