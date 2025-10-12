#!/usr/bin/env python3
"""
Approach 5: Semicircular Layout - Matching Biological Evolution Tree Style
Fan-shaped radial tree like the evolution.png reference
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

print("Creating semicircular AI evolution tree (biological style)...")
print(f"Total models: {len(AI_MODELS)}")

# Build tree
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

print("Calculating semicircular fan layout...")

# SEMICIRCULAR layout (180 degrees)
def assign_positions_semicircular(tree_dict, root_name, min_year=1958, max_year=2026):
    positions = {}

    def count_descendants(name):
        node = tree_dict[name]
        if not node['children']:
            return 1
        return sum(count_descendants(child) for child in node['children']) + 1

    def recurse(name, angle_start, angle_end, depth=0):
        node = tree_dict[name]
        year = node['year']

        # Radial position with slight curve for visual appeal
        radius = np.power((year - min_year) / (max_year - min_year), 0.85)

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

    # Semicircle: -π/2 to π/2 (bottom half of circle, opening upward)
    recurse(root_name, -np.pi/2, np.pi/2)
    return positions

positions = assign_positions_semicircular(tree_dict, "Perceptron")

# Create figure - rectangular for semicircular layout
fig = plt.figure(figsize=(30, 18), facecolor='#FCFCFA')
ax = fig.add_subplot(111)
ax.set_facecolor('#FCFCFA')
ax.set_aspect('equal')

print("Drawing branches with organic curves...")

# Draw branches with smooth curves
def draw_organic_branch(ax, r1, theta1, r2, theta2, color, linewidth, alpha, extinct):
    """Draw organic-looking branch"""
    x1 = r1 * np.cos(theta1)
    y1 = r1 * np.sin(theta1)
    x2 = r2 * np.cos(theta2)
    y2 = r2 * np.sin(theta2)

    # Control points for natural curve
    dist = np.sqrt((x2-x1)**2 + (y2-y1)**2)
    ctrl_dist = dist * 0.35

    # Radial control point
    cx1 = x1 + ctrl_dist * np.cos(theta1)
    cy1 = y1 + ctrl_dist * np.sin(theta1)

    # Approach angle control point
    mid_angle = (theta1 + theta2) / 2
    cx2 = x2 - ctrl_dist * 0.8 * np.cos(mid_angle)
    cy2 = y2 - ctrl_dist * 0.8 * np.sin(mid_angle)

    # Bezier curve
    t = np.linspace(0, 1, 80)
    curve_x = (1-t)**3 * x1 + 3*(1-t)**2*t * cx1 + 3*(1-t)*t**2 * cx2 + t**3 * x2
    curve_y = (1-t)**3 * y1 + 3*(1-t)**2*t * cy1 + 3*(1-t)*t**2 * cy2 + t**3 * y2

    # Tapering effect - branches get thinner toward tips
    if extinct:
        # Fading extinct branches
        for i in range(len(curve_x) - 1):
            progress = i / len(curve_x)
            segment_alpha = alpha * (1 - 0.5 * progress)
            segment_width = linewidth * (1 - 0.4 * progress)

            ax.plot(curve_x[i:i+2], curve_y[i:i+2],
                   color=color, linewidth=segment_width,
                   alpha=segment_alpha, solid_capstyle='round', zorder=1)
    else:
        # Vibrant active branches with slight taper
        for i in range(len(curve_x) - 1):
            progress = i / len(curve_x)
            segment_width = linewidth * (1 - 0.15 * progress)

            ax.plot(curve_x[i:i+2], curve_y[i:i+2],
                   color=color, linewidth=segment_width,
                   alpha=alpha, solid_capstyle='round', zorder=1)

# Draw all branches
for name, data in tree_dict.items():
    if data['parent'] and data['parent'] in positions:
        r1, theta1 = positions[data['parent']]
        r2, theta2 = positions[name]

        linewidth = data['importance'] * 2.5
        alpha = 0.3 if data['extinct'] else 0.8
        color = data['color']

        draw_organic_branch(ax, r1, theta1, r2, theta2, color, linewidth, alpha, data['extinct'])

print("Adding elegant nodes...")

# Draw nodes with artistic styling
for name, (radius, angle) in positions.items():
    node_data = tree_dict[name]
    x = radius * np.cos(angle)
    y = radius * np.sin(angle)

    size = node_data['importance'] * 100
    color = node_data['color']
    alpha = 0.45 if node_data['extinct'] else 0.95

    # Outer glow for important nodes
    if node_data['importance'] >= 4:
        ax.scatter(x, y, s=size*2.2, c=color, alpha=0.08, zorder=1.5, edgecolors='none')
        ax.scatter(x, y, s=size*1.6, c=color, alpha=0.12, zorder=1.6, edgecolors='none')

    # Main node
    ax.scatter(x, y, s=size, c=color,
              edgecolors='white', linewidths=2, alpha=alpha, zorder=2)

    # Highlight for depth
    if node_data['importance'] >= 4:
        ax.scatter(x, y, s=size*0.25, c='white', alpha=0.5, zorder=2.5, edgecolors='none')

print("Adding labels with optimal placement...")

# Smart labeling
labeled_positions = []

def is_label_clear_cart(x, y, min_distance=0.08):
    for prev_x, prev_y in labeled_positions:
        dist = np.sqrt((x - prev_x)**2 + (y - prev_y)**2)
        if dist < min_distance:
            return False
    return True

for name, (radius, angle) in positions.items():
    node_data = tree_dict[name]
    is_breakthrough = any(name == b[0] for b in BREAKTHROUGHS)

    x = radius * np.cos(angle)
    y = radius * np.sin(angle)

    if node_data['importance'] >= 4 or is_breakthrough:
        if radius > 0.1 and is_label_clear_cart(x, y, 0.085):
            # Text angle for fan layout
            text_angle = np.degrees(angle)

            # Adjust for readability in semicircle
            if angle < -np.pi/4:
                text_angle += 180
                ha = 'right'
            elif angle > np.pi/4:
                text_angle += 180
                ha = 'right'
            else:
                ha = 'left'

            label = name
            fontsize = 9 + node_data['importance'] * 0.7
            fontweight = 'bold' if node_data['importance'] >= 5 else 'normal'

            # Radial offset for label
            label_radius = radius + 0.03
            label_x = label_radius * np.cos(angle)
            label_y = label_radius * np.sin(angle)

            # Subtle shadow
            ax.text(label_x, label_y, label,
                   rotation=text_angle, rotation_mode='anchor',
                   ha=ha, va='center', fontsize=fontsize,
                   fontweight=fontweight, alpha=0.12, color='black', zorder=2.8)

            ax.text(label_x-0.001, label_y-0.001, label,
                   rotation=text_angle, rotation_mode='anchor',
                   ha=ha, va='center', fontsize=fontsize,
                   fontweight=fontweight, alpha=0.92, color='#1A1A1A', zorder=3)

            labeled_positions.append((x, y))

print("Adding timeline arcs...")

# Timeline arcs (semicircular)
year_labels = [1960, 1970, 1980, 1990, 2000, 2010, 2015, 2020, 2025]
for i, year in enumerate(year_labels):
    r = np.power((year - 1958) / (2026 - 1958), 0.85)

    theta_arc = np.linspace(-np.pi/2, np.pi/2, 100)
    x_arc = r * np.cos(theta_arc)
    y_arc = r * np.sin(theta_arc)

    # Alternating styles
    if i % 2 == 0:
        ax.plot(x_arc, y_arc, color='#D0D3D4', linestyle='-',
               linewidth=0.9, alpha=0.28, zorder=0)
    else:
        ax.plot(x_arc, y_arc, color='#BFC2C3', linestyle=':',
               linewidth=0.7, alpha=0.22, zorder=0)

    # Year label at bottom
    label_x = r * np.cos(-np.pi/2)
    label_y = r * np.sin(-np.pi/2) - 0.04

    ax.text(label_x, label_y, str(year), fontsize=10, color='#566573',
           ha='center', va='top', alpha=0.7, fontweight='normal')

print("Adding extinction zones...")

# Extinction event shading
for event_name, start_year, end_year in EXTINCTION_EVENTS:
    r_start = np.power((start_year - 1958) / (2026 - 1958), 0.85)
    r_end = np.power((end_year - 1958) / (2026 - 1958), 0.85)
    r_mid = (r_start + r_end) / 2

    theta_arc = np.linspace(-np.pi/2, np.pi/2, 80)

    x_inner = r_start * np.cos(theta_arc)
    y_inner = r_start * np.sin(theta_arc)
    x_outer = r_end * np.cos(theta_arc)
    y_outer = r_end * np.sin(theta_arc)

    ax.fill(np.concatenate([x_inner, x_outer[::-1]]),
           np.concatenate([y_inner, y_outer[::-1]]),
           color='#34495E', alpha=0.035, zorder=0)

    # Label
    label_x = r_mid * 0.7
    label_y = r_mid * np.sin(np.pi/3)

    ax.text(label_x, label_y, f"Extinction: {event_name}",
           fontsize=9, color='#5D6D7E', style='italic', rotation=0,
           ha='center', va='center', alpha=0.65,
           bbox=dict(boxstyle='round,pad=0.4', facecolor='white',
                    edgecolor='#AAB7B8', alpha=0.75, linewidth=0.8))

# Configure plot
ax.set_xlim(-1.25, 1.25)
ax.set_ylim(-1.15, 0.35)
ax.axis('off')

# Title
title_text = "The Phylogenetic Tree of Artificial Intelligence"
subtitle_text = "Evolution from Perceptrons to AGI • 1958—2025"
ax.text(0, 0.25, title_text, fontsize=26, fontweight='bold',
       ha='center', va='top', color='#1C2833', family='serif')
ax.text(0, 0.18, subtitle_text, fontsize=15, ha='center',
       va='top', style='italic', color='#515A5A', family='serif')

# Legend at top
from matplotlib.patches import Patch
legend_elements = [
    Patch(facecolor='#8B7355', alpha=0.6, label='Symbolic AI'),
    Patch(facecolor='#9370DB', alpha=0.8, label='CNNs'),
    Patch(facecolor='#228B22', alpha=0.8, label='Reinforcement Learning'),
    Patch(facecolor='#00CED1', alpha=0.8, label='Transformers'),
    Patch(facecolor='#00BFFF', alpha=0.8, label='GPT (OpenAI)'),
    Patch(facecolor='#7B68EE', alpha=0.8, label='Claude (Anthropic)'),
    Patch(facecolor='#FF4500', alpha=0.8, label='LLaMA (Meta)'),
    Patch(facecolor='#008B8B', alpha=0.8, label='Gemini (Google)'),
    Patch(facecolor='#FF1493', alpha=0.8, label='Diffusion Models'),
    Patch(facecolor='#DC143C', alpha=0.8, label='Chinese AI'),
]

legend = ax.legend(handles=legend_elements, loc='upper center',
                  bbox_to_anchor=(0.5, 0.12), ncol=5, fontsize=10,
                  frameon=True, fancybox=True, shadow=False,
                  facecolor='white', edgecolor='#BDC3C7', framealpha=0.9)

# Caption
caption = "A biological-style phylogenetic visualization • Branch thickness = importance • Curved paths trace evolutionary lineages"
ax.text(0, -1.08, caption, ha='center', fontsize=9.5,
       style='italic', color='#7F8C8D', family='serif')

print("Rendering beautiful outputs...")
output_base = "../output/ai_tree_semicircular"

plt.savefig(f"{output_base}.png", dpi=300, bbox_inches='tight',
           facecolor='#FCFCFA', edgecolor='none')
print(f"✓ Rendered PNG: {output_base}.png")

plt.savefig(f"{output_base}.pdf", bbox_inches='tight',
           facecolor='#FCFCFA', edgecolor='none')
print(f"✓ Rendered PDF: {output_base}.pdf")

plt.savefig(f"{output_base}.svg", bbox_inches='tight',
           facecolor='#FCFCFA', edgecolor='none')
print(f"✓ Rendered SVG: {output_base}.svg")

# Ultra high-res for printing
plt.savefig(f"{output_base}_print.png", dpi=600, bbox_inches='tight',
           facecolor='#FCFCFA', edgecolor='none')
print(f"✓ Rendered Print-Quality PNG: {output_base}_print.png")

plt.close()

print("\n" + "="*70)
print("SEMICIRCULAR BIOLOGICAL-STYLE TREE COMPLETE")
print("="*70)
print("\nFeatures:")
print("✓ Fan-shaped semicircular layout (like evolution.png)")
print("✓ Organic curved branches with natural taper")
print("✓ Gradient fading for extinct lineages")
print("✓ Timeline arcs at bottom")
print("✓ Elegant node halos")
print("✓ Professional biological aesthetic")
print(f"\nLabeled {len(labeled_positions)} key models")
print("\nPerfect for museum display! 🏛️")
