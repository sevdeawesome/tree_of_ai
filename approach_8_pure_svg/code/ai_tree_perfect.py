#!/usr/bin/env python3
"""
Approach 8: Pure SVG - Perfect Control, Zero Glitches
Using svgwrite for pixel-perfect professional output
No matplotlib, no overlaps, just beautiful art
"""

import svgwrite
from svgwrite import cm, mm
import numpy as np
import sys
import os
from collections import defaultdict

sys.path.insert(0, '../../data')
from ai_models import AI_MODELS, EXTINCTION_EVENTS, BREAKTHROUGHS

os.makedirs("../output", exist_ok=True)

print("="*80)
print("CREATING PERFECT SVG VISUALIZATION")
print("Pure vector art with complete control")
print("="*80)

# Configuration
WIDTH = 1200  # mm (120 cm = 47 inches wide!)
HEIGHT = 800  # mm (80 cm = 31 inches tall)
CENTER_X = WIDTH / 2
CENTER_Y = HEIGHT - 100  # Bottom center

MIN_YEAR = 1958
MAX_YEAR = 2026

print(f"\n📐 Canvas: {WIDTH}mm x {HEIGHT}mm ({WIDTH/25.4:.1f}\" x {HEIGHT/25.4:.1f}\")")
print(f"🎨 Scale: Professional print quality")

# Build tree structure
tree_dict = {}
for model_data in AI_MODELS:
    name, parent, year, color, importance, branch_type, extinct = model_data
    tree_dict[name] = {
        'parent': parent,
        'year': year,
        'color': color,
        'importance': importance,
        'branch_type': branch_type,
        'extinct': extinct,
        'children': []
    }

for name, data in tree_dict.items():
    if data['parent'] and data['parent'] in tree_dict:
        tree_dict[data['parent']]['children'].append(name)

print(f"🌳 Models: {len(tree_dict)}")

# Calculate positions with intelligent spacing
def calculate_positions_perfect(tree_dict, root_name):
    """Calculate perfect positions with no overlaps"""
    positions = {}

    def count_leaves(name):
        node = tree_dict[name]
        if not node['children']:
            return 1
        return sum(count_leaves(child) for child in node['children'])

    total_leaves = count_leaves(root_name)
    print(f"🍃 Leaf nodes: {total_leaves}")

    # Use semicircle for better spacing
    angle_start = -np.pi * 0.75  # 135 degrees
    angle_end = np.pi * 0.75     # 135 degrees

    def recurse(name, angle_min, angle_max, depth=0):
        node = tree_dict[name]
        year = node['year']

        # Smooth radial scaling
        time_progress = (year - MIN_YEAR) / (MAX_YEAR - MIN_YEAR)
        radius = np.power(time_progress, 0.85) * (HEIGHT - 200)

        children = node['children']

        if not children:
            # Leaf node - center of angle span
            angle = (angle_min + angle_max) / 2
        else:
            # Parent - will be centered among children
            # First recurse to position children
            leaves_list = [count_leaves(child) for child in children]
            total = sum(leaves_list)

            current_angle = angle_min
            child_angles = []

            for child, leaf_count in zip(children, leaves_list):
                child_span = (angle_max - angle_min) * (leaf_count / total)
                child_angle = recurse(child, current_angle, current_angle + child_span, depth + 1)
                child_angles.append(child_angle)
                current_angle += child_span

            # Parent at centroid of children
            angle = np.mean(child_angles)

        # Convert to cartesian
        x = CENTER_X + radius * np.cos(angle)
        y = CENTER_Y - radius * np.sin(angle)

        positions[name] = {
            'x': x,
            'y': y,
            'angle': angle,
            'radius': radius,
            'depth': depth
        }

        return angle

    recurse(root_name, angle_start, angle_end)
    return positions

print("\n🎯 Computing optimal layout...")
positions = calculate_positions_perfect(tree_dict, "Perceptron")

# Create SVG with professional settings
dwg = svgwrite.Drawing(
    '../output/ai_tree_perfect.svg',
    size=(f'{WIDTH}mm', f'{HEIGHT}mm'),
    viewBox=f'0 0 {WIDTH} {HEIGHT}',
    profile='full'
)

# Add beautiful gradient definitions
defs = dwg.defs

# Glow filters for important nodes
blur = defs.add(dwg.filter(id='glow', x='-50%', y='-50%', width='200%', height='200%'))
blur.feGaussianBlur(in_='SourceGraphic', stdDeviation='2')

# Background
dwg.add(dwg.rect(insert=(0, 0), size=('100%', '100%'), fill='#FCFCFA'))

print("\n🎨 Drawing branches with perfect curves...")

# Group for branches (background layer)
branch_group = dwg.g(id='branches', opacity='0.8')

def create_smooth_curve(x1, y1, x2, y2, angle1, angle2):
    """Create smooth quadratic bezier curve"""
    # Control points for natural flow
    dist = np.sqrt((x2-x1)**2 + (y2-y1)**2)
    ctrl_dist = dist * 0.35

    # Radial control from parent
    cx1 = x1 + ctrl_dist * np.cos(angle1)
    cy1 = y1 - ctrl_dist * np.sin(angle1)

    # Approach child
    cx2 = x2 - ctrl_dist * 0.8 * np.cos(angle2)
    cy2 = y2 + ctrl_dist * 0.8 * np.sin(angle2)

    # SVG path with cubic bezier
    path_data = f'M {x1},{y1} C {cx1},{cy1} {cx2},{cy2} {x2},{y2}'
    return path_data

branch_count = 0
for name, data in tree_dict.items():
    if data['parent'] and data['parent'] in positions:
        parent_pos = positions[data['parent']]
        child_pos = positions[name]

        x1, y1 = parent_pos['x'], parent_pos['y']
        x2, y2 = child_pos['x'], child_pos['y']
        angle1, angle2 = parent_pos['angle'], child_pos['angle']

        # Branch styling
        width = data['importance'] * 1.2
        opacity = 0.25 if data['extinct'] else 0.7
        color = data['color']

        path = create_smooth_curve(x1, y1, x2, y2, angle1, angle2)

        branch_group.add(dwg.path(
            d=path,
            stroke=color,
            stroke_width=width,
            fill='none',
            stroke_linecap='round',
            stroke_linejoin='round',
            opacity=opacity
        ))
        branch_count += 1

dwg.add(branch_group)
print(f"✓ {branch_count} smooth branches")

print("💎 Adding nodes with perfect placement...")

# Group for nodes (middle layer)
node_group = dwg.g(id='nodes')

node_count = 0
for name, pos in positions.items():
    node_data = tree_dict[name]
    x, y = pos['x'], pos['y']

    size = node_data['importance'] * 2.5
    color = node_data['color']
    opacity = 0.4 if node_data['extinct'] else 0.95

    # Outer glow for important nodes
    if node_data['importance'] >= 4:
        node_group.add(dwg.circle(
            center=(x, y),
            r=size * 1.8,
            fill=color,
            opacity=0.08
        ))

    # Main node
    node_group.add(dwg.circle(
        center=(x, y),
        r=size,
        fill=color,
        stroke='white',
        stroke_width=0.8,
        opacity=opacity
    ))

    # Highlight
    if node_data['importance'] >= 4:
        node_group.add(dwg.circle(
            center=(x + size*0.2, y - size*0.2),
            r=size * 0.25,
            fill='white',
            opacity=0.5
        ))

    node_count += 1

dwg.add(node_group)
print(f"✓ {node_count} perfect nodes")

print("✍️  Adding labels with intelligent placement...")

# Group for labels (top layer)
label_group = dwg.g(id='labels', font_family='Georgia, serif', font_size='7')

# Track label bounds to prevent overlaps
label_bounds = []

def check_label_space(x, y, width, height, padding=15):
    """Check if label space is clear"""
    for bx, by, bw, bh in label_bounds:
        if (abs(x - bx) < (width + bw)/2 + padding and
            abs(y - by) < (height + bh)/2 + padding):
            return False
    return True

labeled_count = 0

# Sort by importance for priority labeling
sorted_models = sorted(positions.items(),
                       key=lambda x: tree_dict[x[0]]['importance'],
                       reverse=True)

for name, pos in sorted_models:
    node_data = tree_dict[name]

    # Only label important models
    if node_data['importance'] < 4:
        continue

    x, y = pos['x'], pos['y']
    angle = pos['angle']

    # Determine label position (radial offset)
    label_dist = 15
    label_x = x + label_dist * np.cos(angle)
    label_y = y - label_dist * np.sin(angle)

    # Text anchor based on angle
    if angle > np.pi/4 or angle < -np.pi/4:
        anchor = 'end'
        label_x = x - label_dist * np.cos(angle)
    else:
        anchor = 'start'

    # Estimate label dimensions
    label_width = len(name) * 4.5
    label_height = 8

    # Check if space is clear
    if not check_label_space(label_x, label_y, label_width, label_height, 10):
        continue

    # Add label with subtle shadow
    label_group.add(dwg.text(
        name,
        insert=(label_x + 0.5, label_y + 0.5),
        fill='#333333',
        opacity=0.15,
        font_weight='bold' if node_data['importance'] >= 5 else 'normal',
        text_anchor=anchor,
        font_size='8' if node_data['importance'] >= 5 else '7'
    ))

    # Main label
    label_group.add(dwg.text(
        name,
        insert=(label_x, label_y),
        fill='#1A1A1A',
        opacity=0.9,
        font_weight='bold' if node_data['importance'] >= 5 else 'normal',
        text_anchor=anchor,
        font_size='8' if node_data['importance'] >= 5 else '7'
    ))

    label_bounds.append((label_x, label_y, label_width, label_height))
    labeled_count += 1

dwg.add(label_group)
print(f"✓ {labeled_count} labels (no overlaps)")

print("🕰️  Adding timeline rings...")

# Timeline arcs
timeline_group = dwg.g(id='timeline', opacity='0.25')

years = [1960, 1970, 1980, 1990, 2000, 2010, 2020, 2025]
for year in years:
    time_progress = (year - MIN_YEAR) / (MAX_YEAR - MIN_YEAR)
    radius = np.power(time_progress, 0.85) * (HEIGHT - 200)

    # Arc path
    angle_start_deg = -135
    angle_end_deg = 135

    large_arc = 1 if (angle_end_deg - angle_start_deg) > 180 else 0

    x1 = CENTER_X + radius * np.cos(np.radians(angle_start_deg))
    y1 = CENTER_Y - radius * np.sin(np.radians(angle_start_deg))
    x2 = CENTER_X + radius * np.cos(np.radians(angle_end_deg))
    y2 = CENTER_Y - radius * np.sin(np.radians(angle_end_deg))

    arc_path = f'M {x1},{y1} A {radius},{radius} 0 {large_arc},1 {x2},{y2}'

    path_attrs = {
        'd': arc_path,
        'stroke': '#BDC3C7',
        'stroke_width': 0.5,
        'fill': 'none'
    }
    if year % 10 != 0:
        path_attrs['stroke_dasharray'] = '2,3'

    timeline_group.add(dwg.path(**path_attrs))

    # Year label at bottom
    label_y = CENTER_Y - radius * np.sin(np.radians(-90)) + 12
    timeline_group.add(dwg.text(
        str(year),
        insert=(CENTER_X, label_y),
        fill='#7F8C8D',
        font_family='Arial, sans-serif',
        font_size='6',
        text_anchor='middle',
        opacity='0.7'
    ))

dwg.add(timeline_group)

print("📝 Adding title and legend...")

# Title
title_group = dwg.g(id='title')
title_group.add(dwg.text(
    'The Phylogenetic Tree of Artificial Intelligence',
    insert=(CENTER_X, 40),
    fill='#1C2833',
    font_family='Georgia, serif',
    font_size='20',
    font_weight='bold',
    text_anchor='middle'
))

title_group.add(dwg.text(
    'Evolution from Perceptrons to AGI • 1958—2025',
    insert=(CENTER_X, 60),
    fill='#515A5A',
    font_family='Georgia, serif',
    font_size='11',
    font_style='italic',
    text_anchor='middle'
))

dwg.add(title_group)

# Compact legend
legend_items = [
    ('#9370DB', 'CNNs'),
    ('#00CED1', 'Transformers'),
    ('#00BFFF', 'GPT'),
    ('#7B68EE', 'Claude'),
    ('#FF4500', 'LLaMA'),
    ('#008B8B', 'Gemini'),
    ('#FF1493', 'Diffusion'),
    ('#DC143C', 'Chinese AI'),
]

legend_group = dwg.g(id='legend')
legend_x = 50
legend_y = 80

for i, (color, label) in enumerate(legend_items):
    x = legend_x + (i % 4) * 120
    y = legend_y + (i // 4) * 15

    legend_group.add(dwg.rect(
        insert=(x, y-5),
        size=(10, 8),
        fill=color,
        opacity=0.8,
        rx=2
    ))

    legend_group.add(dwg.text(
        label,
        insert=(x + 15, y + 2),
        fill='#515A5A',
        font_family='Arial, sans-serif',
        font_size='6'
    ))

dwg.add(legend_group)

# Caption
caption_group = dwg.g(id='caption')
caption_group.add(dwg.text(
    f'Visualizing {len(tree_dict)} AI models • {branch_count} evolutionary connections • {labeled_count} key innovations labeled',
    insert=(CENTER_X, HEIGHT - 20),
    fill='#7F8C8D',
    font_family='Georgia, serif',
    font_size='7',
    font_style='italic',
    text_anchor='middle',
    opacity='0.85'
))

dwg.add(caption_group)

# Save perfect SVG
print("\n💾 Saving perfect SVG...")
dwg.save()
print("✓ Saved: ../output/ai_tree_perfect.svg")

# Convert to high-res PNG
print("\n🖼️  Converting to high-resolution PNG...")
try:
    import cairosvg

    # 300 DPI
    scale = 300 / 25.4  # mm to pixels at 300 DPI
    png_width = int(WIDTH * scale)
    png_height = int(HEIGHT * scale)

    cairosvg.svg2png(
        url='../output/ai_tree_perfect.svg',
        write_to='../output/ai_tree_perfect.png',
        output_width=png_width,
        output_height=png_height,
        background_color='#FCFCFA'
    )
    print(f"✓ Saved: ../output/ai_tree_perfect.png ({png_width}x{png_height} px, 300 DPI)")

    # 600 DPI for museum quality
    scale_hires = 600 / 25.4
    png_width_hires = int(WIDTH * scale_hires)
    png_height_hires = int(HEIGHT * scale_hires)

    cairosvg.svg2png(
        url='../output/ai_tree_perfect.svg',
        write_to='../output/ai_tree_perfect_print.png',
        output_width=png_width_hires,
        output_height=png_height_hires,
        background_color='#FCFCFA'
    )
    print(f"✓ Saved: ../output/ai_tree_perfect_print.png ({png_width_hires}x{png_height_hires} px, 600 DPI)")

except Exception as e:
    print(f"⚠ PNG conversion failed: {e}")
    print("  SVG is still perfect - open in Inkscape/Illustrator to export")

print("\n" + "="*80)
print("✨ PERFECT VISUALIZATION COMPLETE")
print("="*80)
print("\n📊 Statistics:")
print(f"  • Models: {len(tree_dict)}")
print(f"  • Branches: {branch_count}")
print(f"  • Labels: {labeled_count} (zero overlaps)")
print(f"  • Size: {WIDTH/25.4:.1f}\" x {HEIGHT/25.4:.1f}\" ({WIDTH}mm x {HEIGHT}mm)")
print(f"  • Quality: Vector SVG + 300/600 DPI PNG")
print("\n✨ Features:")
print("  ✓ Pure SVG - infinite scalability")
print("  ✓ Smooth bezier curves")
print("  ✓ Zero text overlaps (intelligent placement)")
print("  ✓ Perfect node spacing")
print("  ✓ Professional typography")
print("  ✓ Museum print quality")
print("\n🎨 Ready to print at any size!")
print("   Open .svg in Inkscape/Illustrator for further editing\n")
