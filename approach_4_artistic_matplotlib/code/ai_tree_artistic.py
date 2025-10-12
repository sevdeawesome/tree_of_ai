#!/usr/bin/env python3
"""
Approach 4: Artistic Matplotlib with Bezier Curves & Beautiful Styling
Creating publication-quality art inspired by biological phylogenetic trees
"""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.path import Path
from matplotlib.patches import PathPatch, Circle, Wedge
from matplotlib.collections import PatchCollection
import sys
import os

sys.path.insert(0, '../../data')
from ai_models import AI_MODELS, EXTINCTION_EVENTS, BREAKTHROUGHS

os.makedirs("../output", exist_ok=True)

print("Creating artistic AI evolution tree with Bezier curves...")
print(f"Total models: {len(AI_MODELS)}")

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

print("Calculating elegant layout...")

# Position calculation with better weighting
def assign_positions_artistic(tree_dict, root_name, start_angle, end_angle, min_year=1958, max_year=2026):
    positions = {}

    def count_descendants(name):
        node = tree_dict[name]
        if not node['children']:
            return 1
        return sum(count_descendants(child) for child in node['children']) + 1

    def recurse(name, angle_start, angle_end, depth=0):
        node = tree_dict[name]
        year = node['year']

        # Smoother radial scaling
        radius = np.power((year - min_year) / (max_year - min_year), 0.9)

        children = node['children']
        if children:
            angle = (angle_start + angle_end) / 2
        else:
            angle = (angle_start + angle_end) / 2

        positions[name] = (radius, angle)

        if children:
            total_descendants = sum(count_descendants(child) for child in children)
            current_angle = angle_start

            for child in children:
                child_descendants = count_descendants(child)
                child_span = (angle_end - angle_start) * (child_descendants / total_descendants)
                recurse(child, current_angle, current_angle + child_span, depth + 1)
                current_angle += child_span

    recurse(root_name, start_angle, end_angle)
    return positions

positions = assign_positions_artistic(tree_dict, "Perceptron", -np.pi, np.pi)

# Create figure with artistic styling
fig = plt.figure(figsize=(26, 26), facecolor='#FAFAF8')
ax = fig.add_subplot(111, projection='polar')
ax.set_facecolor('#FAFAF8')

print("Drawing artistic branches with Bezier curves...")

# Draw branches with smooth curves
def draw_curved_branch(ax, r1, theta1, r2, theta2, color, linewidth, alpha, extinct):
    """Draw smooth curved branch using Bezier curves"""
    # Convert polar to cartesian
    x1 = r1 * np.cos(theta1)
    y1 = r1 * np.sin(theta1)
    x2 = r2 * np.cos(theta2)
    y2 = r2 * np.sin(theta2)

    # Calculate control points for smooth curve
    dist = np.sqrt((x2-x1)**2 + (y2-y1)**2)
    ctrl_dist = dist * 0.3

    # Control point 1 - extend from parent
    angle1 = theta1
    cx1 = x1 + ctrl_dist * np.cos(angle1)
    cy1 = y1 + ctrl_dist * np.sin(angle1)

    # Control point 2 - approach child
    angle2 = np.arctan2(y2 - y1, x2 - x1)
    cx2 = x2 - ctrl_dist * np.cos(angle2)
    cy2 = y2 - ctrl_dist * np.sin(angle2)

    # Create Bezier curve path
    vertices = [
        (x1, y1),
        (cx1, cy1),
        (cx2, cy2),
        (x2, y2)
    ]

    codes = [
        Path.MOVETO,
        Path.CURVE4,
        Path.CURVE4,
        Path.CURVE4
    ]

    path = Path(vertices, codes)

    # Convert back to polar for plotting
    t = np.linspace(0, 1, 100)
    points = path.interpolated(100).vertices

    r_curve = np.sqrt(points[:, 0]**2 + points[:, 1]**2)
    theta_curve = np.arctan2(points[:, 1], points[:, 0])

    # Gradient effect for extinct branches
    if extinct:
        # Draw with gradient fade
        segments = 20
        for i in range(segments):
            start_idx = i * (len(r_curve) // segments)
            end_idx = min((i + 1) * (len(r_curve) // segments), len(r_curve))

            segment_alpha = alpha * (1 - 0.6 * (i / segments))

            ax.plot(theta_curve[start_idx:end_idx], r_curve[start_idx:end_idx],
                   color=color, linewidth=linewidth * (1 - 0.3 * (i/segments)),
                   alpha=segment_alpha, solid_capstyle='round', zorder=1)
    else:
        ax.plot(theta_curve, r_curve,
               color=color, linewidth=linewidth, alpha=alpha,
               solid_capstyle='round', zorder=1)

# Draw all branches with curves
for name, data in tree_dict.items():
    if data['parent'] and data['parent'] in positions:
        r1, theta1 = positions[data['parent']]
        r2, theta2 = positions[name]

        linewidth = data['importance'] * 2.0
        alpha = 0.35 if data['extinct'] else 0.75
        color = data['color']

        draw_curved_branch(ax, r1, theta1, r2, theta2, color, linewidth, alpha, data['extinct'])

print("Adding beautiful nodes with halos...")

# Draw nodes with artistic halos
for name, (radius, angle) in positions.items():
    node_data = tree_dict[name]

    size = node_data['importance'] * 100
    color = node_data['color']
    alpha = 0.5 if node_data['extinct'] else 0.95

    # Draw halo (outer glow)
    if node_data['importance'] >= 4:
        halo_size = size * 1.8
        ax.scatter(angle, radius, s=halo_size, c=color,
                  alpha=0.1, zorder=1.5, edgecolors='none')

    # Draw main node
    ax.scatter(angle, radius, s=size, c=color,
              edgecolors='white', linewidths=1.5, alpha=alpha, zorder=2)

    # Draw inner highlight
    if node_data['importance'] >= 4:
        highlight_size = size * 0.3
        ax.scatter(angle, radius, s=highlight_size, c='white',
                  alpha=0.4, zorder=2.5, edgecolors='none')

print("Adding elegant labels...")

# Selective, artistic labeling
labeled_positions = []

def is_label_clear(angle, radius, min_distance=0.08):
    for prev_angle, prev_radius in labeled_positions:
        angle_diff = abs(angle - prev_angle)
        if angle_diff > np.pi:
            angle_diff = 2 * np.pi - angle_diff
        dist = np.sqrt((radius - prev_radius)**2 + (radius * angle_diff)**2)
        if dist < min_distance:
            return False
    return True

# Label only the most important nodes
for name, (radius, angle) in positions.items():
    node_data = tree_dict[name]
    is_breakthrough = any(name == b[0] for b in BREAKTHROUGHS)

    if node_data['importance'] >= 4 or is_breakthrough:
        if radius > 0.08 and is_label_clear(angle, radius, 0.09):
            text_angle = np.degrees(angle)
            if text_angle > 90 and text_angle < 270:
                text_angle += 180
                ha = 'right'
            else:
                ha = 'left'

            label = name
            fontsize = 8 + node_data['importance'] * 0.8
            fontweight = 'bold' if node_data['importance'] >= 5 else 'normal'

            # Add subtle shadow for readability
            ax.text(angle, radius + 0.025, label,
                   rotation=text_angle, rotation_mode='anchor',
                   ha=ha, va='center', fontsize=fontsize,
                   fontweight=fontweight, alpha=0.15, color='black',
                   zorder=2.8)

            ax.text(angle, radius + 0.024, label,
                   rotation=text_angle, rotation_mode='anchor',
                   ha=ha, va='center', fontsize=fontsize,
                   fontweight=fontweight, alpha=0.9, color='#2C3E50',
                   zorder=3)

            labeled_positions.append((angle, radius))

print("Adding timeline rings with elegant styling...")

# Artistic timeline rings
year_labels = [1960, 1970, 1980, 1990, 2000, 2010, 2015, 2020, 2025]
for i, year in enumerate(year_labels):
    r = np.power((year - 1958) / (2026 - 1958), 0.9)

    theta_full = np.linspace(0, 2*np.pi, 200)

    # Alternating ring styles
    if i % 2 == 0:
        ax.plot(theta_full, [r]*len(theta_full), color='#D5D8DC',
               linestyle='-', linewidth=0.8, alpha=0.25, zorder=0)
    else:
        ax.plot(theta_full, [r]*len(theta_full), color='#BDC3C7',
               linestyle=':', linewidth=0.6, alpha=0.2, zorder=0)

    # Year labels with background
    ax.text(0, r, f"  {year}  ", fontsize=10, color='#5D6D7E',
           ha='left', va='center', alpha=0.7,
           bbox=dict(boxstyle='round,pad=0.3', facecolor='white',
                    edgecolor='none', alpha=0.6))

print("Adding extinction event markers...")

# Artistic extinction zones
for event_name, start_year, end_year in EXTINCTION_EVENTS:
    r_start = np.power((start_year - 1958) / (2026 - 1958), 0.9)
    r_end = np.power((end_year - 1958) / (2026 - 1958), 0.9)
    r_mid = (r_start + r_end) / 2

    theta_full = np.linspace(-np.pi, np.pi, 150)
    ax.fill_between(theta_full, r_start, r_end,
                    color='#2C3E50', alpha=0.04, zorder=0)

    # Elegant label
    ax.text(np.pi * 0.75, r_mid, f"↯ {event_name}",
           fontsize=9, color='#7F8C8D', style='italic',
           ha='center', va='center', alpha=0.7,
           bbox=dict(boxstyle='round,pad=0.4', facecolor='#FDFEFE',
                    edgecolor='#BDC3C7', alpha=0.8, linewidth=1))

# Configure artistic plot style
ax.set_ylim(0, 1.2)
ax.set_theta_zero_location('N')
ax.set_theta_direction(-1)
ax.grid(False)
ax.set_yticks([])
ax.set_xticks([])
ax.spines['polar'].set_visible(False)

# Beautiful title
title_text = "The Phylogenetic Tree of Artificial Intelligence"
subtitle_text = "From Perceptrons to AGI • 1958—2025"
ax.text(0.5, 1.15, title_text, transform=ax.transAxes,
       fontsize=24, fontweight='bold', ha='center', va='top',
       color='#2C3E50', family='serif')
ax.text(0.5, 1.11, subtitle_text, transform=ax.transAxes,
       fontsize=14, ha='center', va='top', style='italic',
       color='#5D6D7E', family='serif')

# Elegant legend
from matplotlib.patches import Patch
legend_elements = [
    Patch(facecolor='#8B7355', alpha=0.7, label='Symbolic AI'),
    Patch(facecolor='#9370DB', alpha=0.7, label='Convolutional Neural Networks'),
    Patch(facecolor='#4169E1', alpha=0.4, label='Recurrent Networks (extinct)'),
    Patch(facecolor='#228B22', alpha=0.7, label='Reinforcement Learning'),
    Patch(facecolor='#00CED1', alpha=0.7, label='Transformer Revolution'),
    Patch(facecolor='#00BFFF', alpha=0.7, label='GPT Lineage (OpenAI)'),
    Patch(facecolor='#7B68EE', alpha=0.7, label='Claude (Anthropic)'),
    Patch(facecolor='#FF4500', alpha=0.7, label='LLaMA (Meta)'),
    Patch(facecolor='#008B8B', alpha=0.7, label='Gemini (Google)'),
    Patch(facecolor='#FF1493', alpha=0.7, label='Diffusion Models'),
    Patch(facecolor='#DC143C', alpha=0.7, label='Chinese AI Revolution'),
]

legend = ax.legend(handles=legend_elements, loc='upper left',
                  bbox_to_anchor=(-0.15, 1.0), fontsize=10,
                  frameon=True, fancybox=True, shadow=False,
                  facecolor='white', edgecolor='#BDC3C7', framealpha=0.9)

# Artistic caption
caption = "Branch thickness reflects model importance  •  Faded branches show deprecated approaches  •  Smooth curves trace evolutionary paths"
fig.text(0.5, 0.015, caption, ha='center', fontsize=9,
        style='italic', color='#7F8C8D', family='serif')

print("Rendering artistic outputs...")
output_base = "../output/ai_tree_artistic"

plt.savefig(f"{output_base}.png", dpi=300, bbox_inches='tight',
           facecolor='#FAFAF8', edgecolor='none')
print(f"✓ Rendered PNG: {output_base}.png")

plt.savefig(f"{output_base}.pdf", bbox_inches='tight',
           facecolor='#FAFAF8', edgecolor='none')
print(f"✓ Rendered PDF: {output_base}.pdf")

plt.savefig(f"{output_base}.svg", bbox_inches='tight',
           facecolor='#FAFAF8', edgecolor='none')
print(f"✓ Rendered SVG: {output_base}.svg")

# Also create high-res version for printing
plt.savefig(f"{output_base}_highres.png", dpi=600, bbox_inches='tight',
           facecolor='#FAFAF8', edgecolor='none')
print(f"✓ Rendered High-Res PNG: {output_base}_highres.png")

plt.close()

print("\n" + "="*70)
print("ARTISTIC VISUALIZATION COMPLETE")
print("="*70)
print("\nArtistic Features:")
print("✓ Smooth Bezier curved branches")
print("✓ Gradient fade for extinct lineages")
print("✓ Node halos for important models")
print("✓ Elegant typography and spacing")
print("✓ Soft color palette")
print("✓ Publication-quality styling")
print(f"\nRendered {len(AI_MODELS)} models with artistic beauty")
print(f"Labeled {len(labeled_positions)} key innovations")
print("\nReady for framing! 🎨")
