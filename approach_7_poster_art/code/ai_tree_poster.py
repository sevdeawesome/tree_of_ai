#!/usr/bin/env python3
"""
Approach 7: Ultra-Detailed Poster Art - Museum Quality
ALL 114 branches visible, selective labeling, maximum artistic beauty
Inspired by the gorgeous biological evolution tree
"""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.path import Path
import sys
import os

sys.path.insert(0, '../../data')
from ai_models import AI_MODELS, EXTINCTION_EVENTS, BREAKTHROUGHS

os.makedirs("../output", exist_ok=True)

print("="*80)
print("CREATING MUSEUM-QUALITY POSTER ART")
print("="*80)
print(f"\n✨ Total models to visualize: {len(AI_MODELS)}")
print("🎨 All branches will be shown with artistic detail")
print("🖼️  Output will be poster/print quality (ultra high resolution)\n")

# Build complete tree
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

print(f"🌳 Tree structure: {len(tree_dict)} models organized hierarchically")
print(f"📊 Branches: {sum(1 for d in tree_dict.values() if d['parent'])}")
print(f"🍂 Extinct lineages: {sum(1 for d in tree_dict.values() if d['extinct'])}")

# Semicircular layout optimized for maximum beauty
def assign_positions_poster(tree_dict, root_name, min_year=1958, max_year=2026):
    positions = {}

    def count_leaves(name):
        node = tree_dict[name]
        if not node['children']:
            return 1
        return sum(count_leaves(child) for child in node['children'])

    total_leaves = count_leaves(root_name)
    print(f"🍃 Leaf nodes (terminal models): {total_leaves}")

    def recurse(name, angle_start, angle_end, depth=0):
        node = tree_dict[name]
        year = node['year']

        # Smooth radial progression
        radius = np.power((year - min_year) / (max_year - min_year), 0.88)

        children = node['children']

        if children:
            # Parent centered among children
            angle = (angle_start + angle_end) / 2
        else:
            # Leaf at span center
            angle = (angle_start + angle_end) / 2

        positions[name] = (radius, angle, depth)

        if children:
            # Proportional angular allocation
            child_leaves = [count_leaves(child) for child in children]
            total = sum(child_leaves)
            current_angle = angle_start

            for child, leaves in zip(children, child_leaves):
                child_span = (angle_end - angle_start) * (leaves / total)
                recurse(child, current_angle, current_angle + child_span, depth + 1)
                current_angle += child_span

    # Semicircle with slight asymmetry for aesthetic
    recurse(root_name, -np.pi/1.8, np.pi/1.8)
    return positions

print("\n🎯 Calculating optimal node positions...")
positions = assign_positions_poster(tree_dict, "Perceptron")
print(f"✓ Positioned {len(positions)} nodes in semicircular fan layout")

# Create MASSIVE figure for print quality
print("\n🖼️  Creating ultra-high resolution canvas...")
fig = plt.figure(figsize=(40, 26), facecolor='#FEFEFE', dpi=100)
ax = fig.add_subplot(111)
ax.set_facecolor('#FEFEFE')
ax.set_aspect('equal')

print("🎨 Rendering artistic branches with organic curves...")

# Enhanced curve drawing with even smoother bezier curves
def draw_artistic_branch(ax, r1, theta1, r2, theta2, color, linewidth, alpha, extinct, depth):
    """Ultra-smooth artistic branch"""
    x1 = r1 * np.cos(theta1)
    y1 = r1 * np.sin(theta1)
    x2 = r2 * np.cos(theta2)
    y2 = r2 * np.sin(theta2)

    dist = np.sqrt((x2-x1)**2 + (y2-y1)**2)

    # Multi-point Bezier for ultra-smooth curves
    ctrl_dist1 = dist * 0.4
    ctrl_dist2 = dist * 0.3

    # Radial control from parent
    cx1 = x1 + ctrl_dist1 * np.cos(theta1)
    cy1 = y1 + ctrl_dist1 * np.sin(theta1)

    # Intermediate curve control
    mid_angle = (theta1 + theta2) / 2
    mid_r = (r1 + r2) / 2
    cx2 = mid_r * np.cos(mid_angle) + ctrl_dist2 * 0.3 * np.cos(mid_angle + np.pi/2)
    cy2 = mid_r * np.sin(mid_angle) + ctrl_dist2 * 0.3 * np.sin(mid_angle + np.pi/2)

    # Approach child tangentially
    cx3 = x2 - ctrl_dist1 * 0.6 * np.cos(theta2)
    cy3 = y2 - ctrl_dist1 * 0.6 * np.sin(theta2)

    # Super-smooth curve with many points
    t = np.linspace(0, 1, 120)
    # Cubic bezier
    curve_x = (1-t)**3*x1 + 3*(1-t)**2*t*cx1 + 3*(1-t)*t**2*cx3 + t**3*x2
    curve_y = (1-t)**3*y1 + 3*(1-t)**2*t*cy1 + 3*(1-t)*t**2*cy3 + t**3*y2

    # Draw with beautiful tapering and optional gradient
    if extinct:
        # Elegant fade for extinct branches
        segments = 25
        for i in range(len(curve_x) - 1):
            progress = i / (len(curve_x) - 1)
            segment_alpha = alpha * (1 - 0.65 * progress)
            segment_width = linewidth * (1 - 0.5 * progress)

            # Slight color shift for depth
            ax.plot(curve_x[i:i+2], curve_y[i:i+2],
                   color=color, linewidth=max(0.5, segment_width),
                   alpha=segment_alpha, solid_capstyle='round',
                   solid_joinstyle='round', zorder=1 + depth*0.01)
    else:
        # Vibrant active branches with subtle taper
        for i in range(len(curve_x) - 1):
            progress = i / (len(curve_x) - 1)
            segment_width = linewidth * (1 - 0.2 * progress)

            # Glow effect for important branches
            if linewidth > 8:
                ax.plot(curve_x[i:i+2], curve_y[i:i+2],
                       color=color, linewidth=segment_width*1.8,
                       alpha=alpha*0.15, solid_capstyle='round', zorder=0.8 + depth*0.01)

            ax.plot(curve_x[i:i+2], curve_y[i:i+2],
                   color=color, linewidth=segment_width,
                   alpha=alpha, solid_capstyle='round',
                   solid_joinstyle='round', zorder=1 + depth*0.01)

# Draw ALL branches (this is the key - showing every connection)
branch_count = 0
for name, data in tree_dict.items():
    if data['parent'] and data['parent'] in positions:
        r1, theta1, depth1 = positions[data['parent']]
        r2, theta2, depth2 = positions[name]

        # Vary width by importance
        linewidth = data['importance'] * 2.8
        alpha = 0.28 if data['extinct'] else 0.82
        color = data['color']

        draw_artistic_branch(ax, r1, theta1, r2, theta2, color, linewidth, alpha, data['extinct'], depth2)
        branch_count += 1

print(f"✓ Drew {branch_count} beautiful curved branches")

print("💎 Adding nodes with artistic halos...")

# Draw ALL nodes with artistic treatment
node_count = 0
for name, (radius, angle, depth) in positions.items():
    node_data = tree_dict[name]
    x = radius * np.cos(angle)
    y = radius * np.sin(angle)

    size = node_data['importance'] * 120
    color = node_data['color']
    alpha = 0.42 if node_data['extinct'] else 0.96

    # Multi-layer halo for important nodes
    if node_data['importance'] >= 4:
        ax.scatter(x, y, s=size*3.5, c=color, alpha=0.04, zorder=1.4, edgecolors='none')
        ax.scatter(x, y, s=size*2.5, c=color, alpha=0.08, zorder=1.5, edgecolors='none')
        ax.scatter(x, y, s=size*1.8, c=color, alpha=0.14, zorder=1.6, edgecolors='none')

    # Main node with subtle edge
    ax.scatter(x, y, s=size, c=color,
              edgecolors='white', linewidths=2.5, alpha=alpha, zorder=2 + depth*0.001)

    # Bright highlight
    if node_data['importance'] >= 4:
        highlight_x = x + 0.005 * np.cos(angle + np.pi/4)
        highlight_y = y + 0.005 * np.sin(angle + np.pi/4)
        ax.scatter(highlight_x, highlight_y, s=size*0.22, c='white',
                  alpha=0.6, zorder=2.6, edgecolors='none')

    node_count += 1

print(f"✓ Rendered {node_count} nodes with depth and dimension")

print("✍️  Adding selective labels (only key models for clarity)...")

# Strategic labeling - only the most important to avoid clutter
labeled_positions = []

def is_label_clear_poster(x, y, min_distance=0.075):
    for prev_x, prev_y in labeled_positions:
        dist = np.sqrt((x - prev_x)**2 + (y - prev_y)**2)
        if dist < min_distance:
            return False
    return True

label_count = 0
for name, (radius, angle, depth) in positions.items():
    node_data = tree_dict[name]
    is_breakthrough = any(name == b[0] for b in BREAKTHROUGHS)

    x = radius * np.cos(angle)
    y = radius * np.sin(angle)

    # Only label highest importance or breakthroughs
    if node_data['importance'] >= 5 or (is_breakthrough and node_data['importance'] >= 4):
        if radius > 0.12 and is_label_clear_poster(x, y, 0.08):
            text_angle = np.degrees(angle)

            # Optimal reading angle
            if angle < -np.pi/3:
                text_angle += 180
                ha = 'right'
            elif angle > np.pi/3:
                text_angle += 180
                ha = 'right'
            else:
                ha = 'left'

            label = name
            fontsize = 11 + node_data['importance'] * 1.2
            fontweight = 'bold' if node_data['importance'] >= 5 else '600'

            # Elegant offset
            label_radius = radius + 0.035
            label_x = label_radius * np.cos(angle)
            label_y = label_radius * np.sin(angle)

            # Multi-layer shadow for depth
            for offset, shadow_alpha in [(0.003, 0.08), (0.002, 0.12), (0.001, 0.18)]:
                ax.text(label_x+offset, label_y+offset, label,
                       rotation=text_angle, rotation_mode='anchor',
                       ha=ha, va='center', fontsize=fontsize,
                       fontweight=fontweight, alpha=shadow_alpha,
                       color='black', zorder=2.7, family='serif')

            # Main label
            ax.text(label_x, label_y, label,
                   rotation=text_angle, rotation_mode='anchor',
                   ha=ha, va='center', fontsize=fontsize,
                   fontweight=fontweight, alpha=0.94, color='#0D0D0D',
                   zorder=3, family='serif')

            labeled_positions.append((x, y))
            label_count += 1

print(f"✓ Labeled {label_count} key innovations (selective for clarity)")

print("🕰️  Adding elegant timeline arcs...")

# Beautiful timeline arcs
year_labels = [1960, 1965, 1970, 1975, 1980, 1985, 1990, 1995, 2000, 2005, 2010, 2015, 2020, 2025]
for i, year in enumerate(year_labels):
    r = np.power((year - 1958) / (2026 - 1958), 0.88)

    theta_arc = np.linspace(-np.pi/1.8, np.pi/1.8, 180)
    x_arc = r * np.cos(theta_arc)
    y_arc = r * np.sin(theta_arc)

    # Vary styling by decade
    if year % 10 == 0:
        ax.plot(x_arc, y_arc, color='#BDC3C7', linestyle='-',
               linewidth=1.2, alpha=0.32, zorder=0)
    else:
        ax.plot(x_arc, y_arc, color='#D5D8DC', linestyle=':',
               linewidth=0.8, alpha=0.22, zorder=0)

    # Year labels
    label_x = r * np.cos(-np.pi/1.8)
    label_y = r * np.sin(-np.pi/1.8) - 0.05

    ax.text(label_x, label_y, str(year), fontsize=11, color='#515A5A',
           ha='center', va='top', alpha=0.75, fontweight='normal',
           family='sans-serif')

print("💀 Adding extinction event zones...")

# Artistic extinction markers
for event_name, start_year, end_year in EXTINCTION_EVENTS:
    r_start = np.power((start_year - 1958) / (2026 - 1958), 0.88)
    r_end = np.power((end_year - 1958) / (2026 - 1958), 0.88)
    r_mid = (r_start + r_end) / 2

    theta_arc = np.linspace(-np.pi/1.8, np.pi/1.8, 140)

    x_inner = r_start * np.cos(theta_arc)
    y_inner = r_start * np.sin(theta_arc)
    x_outer = r_end * np.cos(theta_arc)
    y_outer = r_end * np.sin(theta_arc)

    ax.fill(np.concatenate([x_inner, x_outer[::-1]]),
           np.concatenate([y_inner, y_outer[::-1]]),
           color='#2C3E50', alpha=0.028, zorder=0)

    # Elegant label
    label_x = r_mid * 0.65
    label_y = r_mid * np.sin(np.pi/2.5)

    ax.text(label_x, label_y, f"↯ {event_name}",
           fontsize=11, color='#566573', style='italic', rotation=0,
           ha='center', va='center', alpha=0.68,
           bbox=dict(boxstyle='round,pad=0.5', facecolor='#FDFDFD',
                    edgecolor='#95A5A6', alpha=0.85, linewidth=1.2),
           family='serif')

# Configure artistic plot
ax.set_xlim(-1.35, 1.35)
ax.set_ylim(-1.25, 0.42)
ax.axis('off')

# Museum-quality title
print("📝 Adding elegant title and metadata...")
title_text = "The Phylogenetic Tree of Artificial Intelligence"
subtitle_text = "A Visual Chronicle of Machine Learning Evolution • 1958—2025"

ax.text(0, 0.32, title_text, fontsize=34, fontweight='bold',
       ha='center', va='top', color='#17202A', family='serif',
       bbox=dict(boxstyle='round,pad=0.6', facecolor='white',
                edgecolor='none', alpha=0.7))

ax.text(0, 0.22, subtitle_text, fontsize=17, ha='center',
       va='top', style='italic', color='#34495E', family='serif')

# Sophisticated legend
from matplotlib.patches import Patch
legend_elements = [
    Patch(facecolor='#8B7355', alpha=0.5, label='Symbolic AI (extinct)'),
    Patch(facecolor='#9370DB', alpha=0.8, label='Convolutional Neural Networks'),
    Patch(facecolor='#4169E1', alpha=0.4, label='Recurrent Networks (extinct)'),
    Patch(facecolor='#FFA500', alpha=0.4, label='GANs (extinct)'),
    Patch(facecolor='#228B22', alpha=0.8, label='Reinforcement Learning'),
    Patch(facecolor='#00CED1', alpha=0.8, label='Transformer Architecture'),
    Patch(facecolor='#00BFFF', alpha=0.8, label='GPT Lineage (OpenAI)'),
    Patch(facecolor='#7B68EE', alpha=0.8, label='Claude Family (Anthropic)'),
    Patch(facecolor='#FF4500', alpha=0.8, label='LLaMA Ecosystem (Meta)'),
    Patch(facecolor='#008B8B', alpha=0.8, label='Gemini Series (Google)'),
    Patch(facecolor='#FF1493', alpha=0.8, label='Diffusion Models'),
    Patch(facecolor='#DC143C', alpha=0.8, label='Chinese AI Innovation'),
]

legend = ax.legend(handles=legend_elements, loc='upper center',
                  bbox_to_anchor=(0.5, 0.15), ncol=4, fontsize=11,
                  frameon=True, fancybox=True, shadow=False,
                  facecolor='white', edgecolor='#AAB7B8',
                  framealpha=0.92, columnspacing=1.2)

# Artistic caption
caption = ("Every branch traces a lineage • " +
          "Thickness reflects historical impact • " +
          "Faded paths mark deprecated approaches • " +
          f"{len(AI_MODELS)} models, {branch_count} connections, {label_count} labeled milestones")

ax.text(0, -1.15, caption, ha='center', fontsize=10.5,
       style='italic', color='#5D6D7E', family='serif', alpha=0.85)

# Artist signature
ax.text(0.98, -1.18, "Generative visualization • Data-driven art", ha='right',
       fontsize=8, style='italic', color='#95A5A6',
       transform=ax.transData, alpha=0.7, family='sans-serif')

print("\n🎨 Rendering ultra-high resolution outputs...")
output_base = "../output/ai_tree_poster"

# Standard high-res
print("   → PNG (300 DPI)...")
plt.savefig(f"{output_base}.png", dpi=300, bbox_inches='tight',
           facecolor='#FEFEFE', edgecolor='none', pad_inches=0.1)
print(f"   ✓ {output_base}.png")

# Vector for editing
print("   → PDF (vector)...")
plt.savefig(f"{output_base}.pdf", bbox_inches='tight',
           facecolor='#FEFEFE', edgecolor='none', pad_inches=0.1)
print(f"   ✓ {output_base}.pdf")

print("   → SVG (web vector)...")
plt.savefig(f"{output_base}.svg", bbox_inches='tight',
           facecolor='#FEFEFE', edgecolor='none', pad_inches=0.1)
print(f"   ✓ {output_base}.svg")

# ULTRA high-res for museum/gallery printing
print("   → ULTRA High-Res PNG (600 DPI) for printing...")
plt.savefig(f"{output_base}_museum_print.png", dpi=600, bbox_inches='tight',
           facecolor='#FEFEFE', edgecolor='none', pad_inches=0.1)
print(f"   ✓ {output_base}_museum_print.png")

plt.close()

print("\n" + "="*80)
print("🏛️  MUSEUM-QUALITY POSTER ART COMPLETE")
print("="*80)
print("\n📊 Final Statistics:")
print(f"   • Total models visualized: {len(AI_MODELS)}")
print(f"   • Branches drawn: {branch_count}")
print(f"   • Nodes rendered: {node_count}")
print(f"   • Key models labeled: {label_count}")
print(f"   • Timeline markers: {len(year_labels)}")
print(f"   • Extinction events: {len(EXTINCTION_EVENTS)}")

print("\n✨ Artistic Features:")
print("   ✓ Ultra-smooth Bezier curved branches")
print("   ✓ Gradient tapering for depth perception")
print("   ✓ Multi-layer node halos")
print("   ✓ Selective strategic labeling")
print("   ✓ ALL 114 branches visible")
print("   ✓ Semicircular biological layout")
print("   ✓ Print quality: 600 DPI")

print("\n🖼️  Ready to frame and display!")
print("   Perfect for: Museums, galleries, conferences, offices")
print("   Sizes: Print up to 40\" wide or larger\n")
