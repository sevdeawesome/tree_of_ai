#!/usr/bin/env python3
"""
Approach 2: Matplotlib - Full Dataset with Advanced Styling
Complete phylogenetic tree of AI evolution (1958-2025)
"""

import matplotlib
matplotlib.use('Agg')  # Use non-GUI backend
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Wedge, Circle
from matplotlib.collections import LineCollection
import sys
import os

# Add data directory to path
sys.path.insert(0, '../../data')
from ai_models import AI_MODELS, EXTINCTION_EVENTS, BREAKTHROUGHS

# Create output directory
os.makedirs("../output", exist_ok=True)

print("Building complete AI evolution tree...")
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

# Link children to parents
for name, data in tree_dict.items():
    if data['parent'] and data['parent'] in tree_dict:
        tree_dict[data['parent']]['children'].append(name)

print(f"Tree structure built. Root: Perceptron with {len(tree_dict['Perceptron']['children'])} main branches")

# Assign positions with improved algorithm
def assign_positions(tree_dict, root_name, start_angle, end_angle, min_year=1958, max_year=2026):
    """Recursively assign polar coordinates with better angular distribution"""
    positions = {}

    def count_descendants(name):
        """Count total descendants to weight angular space"""
        node = tree_dict[name]
        if not node['children']:
            return 1
        return sum(count_descendants(child) for child in node['children']) + 1

    def recurse(name, angle_start, angle_end, depth=0):
        node = tree_dict[name]
        year = node['year']

        # Radial position based on year
        radius = (year - min_year) / (max_year - min_year)

        # Angular position
        children = node['children']
        if children:
            # Center parent between children
            angle = (angle_start + angle_end) / 2
        else:
            # Leaf node - use middle of span
            angle = (angle_start + angle_end) / 2

        positions[name] = (radius, angle)

        # Allocate angular space to children based on their descendant counts
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

print("Calculating node positions...")
positions = assign_positions(tree_dict, "Perceptron", -np.pi, np.pi)

# Create figure with high resolution
fig = plt.figure(figsize=(24, 24))
ax = fig.add_subplot(111, projection='polar')

print("Rendering branches and nodes...")

# Draw branches first (background layer)
for name, data in tree_dict.items():
    if data['parent'] and data['parent'] in positions:
        r1, theta1 = positions[data['parent']]
        r2, theta2 = positions[name]

        # Line properties
        linewidth = data['importance'] * 1.5
        alpha = 0.3 if data['extinct'] else 0.7
        color = data['color']

        # Draw branch
        ax.plot([theta1, theta2], [r1, r2],
                color=color, linewidth=linewidth, alpha=alpha,
                solid_capstyle='round', zorder=1)

# Draw nodes (middle layer)
for name, (radius, angle) in positions.items():
    node_data = tree_dict[name]

    # Node size based on importance
    size = node_data['importance'] * 80
    alpha = 0.4 if node_data['extinct'] else 0.9

    # Draw node
    ax.scatter(angle, radius, s=size, c=node_data['color'],
              edgecolors='black', linewidths=0.5, alpha=alpha, zorder=2)

# Add labels (top layer) - selective labeling to avoid clutter
print("Adding labels...")
LABEL_THRESHOLD = 3  # Only label important nodes
labeled_positions = []

def is_label_clear(angle, radius, min_distance=0.08):
    """Check if label position is clear of other labels"""
    for prev_angle, prev_radius in labeled_positions:
        # Calculate angular distance (handle wraparound)
        angle_diff = abs(angle - prev_angle)
        if angle_diff > np.pi:
            angle_diff = 2 * np.pi - angle_diff

        # Euclidean-ish distance in polar space
        dist = np.sqrt((radius - prev_radius)**2 + (radius * angle_diff)**2)
        if dist < min_distance:
            return False
    return True

for name, (radius, angle) in positions.items():
    node_data = tree_dict[name]

    # Only label important nodes or breakthroughs
    is_breakthrough = any(name == b[0] for b in BREAKTHROUGHS)

    if node_data['importance'] >= LABEL_THRESHOLD or is_breakthrough:
        if radius > 0.05 and is_label_clear(angle, radius):
            # Text angle for readability
            text_angle = np.degrees(angle)
            if text_angle > 90 and text_angle < 270:
                text_angle += 180
                ha = 'right'
            else:
                ha = 'left'

            # Add breakthrough marker if applicable
            label = name
            if is_breakthrough:
                marker = next((b[2] for b in BREAKTHROUGHS if b[0] == name), '')
                label = f"{marker} {name}"

            # Font size based on importance
            fontsize = 7 + node_data['importance'] * 0.5
            fontweight = 'bold' if node_data['importance'] >= 5 else 'normal'

            ax.text(angle, radius + 0.02, label,
                   rotation=text_angle, rotation_mode='anchor',
                   ha=ha, va='center', fontsize=fontsize,
                   fontweight=fontweight, alpha=0.9)

            labeled_positions.append((angle, radius))

# Add timeline rings
print("Adding timeline rings...")
year_labels = [1960, 1970, 1980, 1990, 2000, 2010, 2015, 2020, 2025]
for year in year_labels:
    r = (year - 1958) / (2026 - 1958)

    # Draw ring
    theta_full = np.linspace(0, 2*np.pi, 100)
    ax.plot(theta_full, [r]*len(theta_full), color='gray',
           linestyle='--', linewidth=0.5, alpha=0.3, zorder=0)

    # Year label
    ax.text(0, r, f" {year}", fontsize=9, color='gray',
           ha='left', va='center', alpha=0.6)

# Add extinction event markers
print("Adding extinction event markers...")
for event_name, start_year, end_year in EXTINCTION_EVENTS:
    r_start = (start_year - 1958) / (2026 - 1958)
    r_end = (end_year - 1958) / (2026 - 1958)
    r_mid = (r_start + r_end) / 2

    # Add subtle shading
    theta_full = np.linspace(-np.pi, np.pi, 100)
    ax.fill_between(theta_full, r_start, r_end,
                    color='gray', alpha=0.05, zorder=0)

    # Label
    ax.text(np.pi * 0.7, r_mid, f"💀 {event_name}",
           fontsize=8, color='darkgray', style='italic',
           ha='center', va='center', alpha=0.6,
           bbox=dict(boxstyle='round,pad=0.3', facecolor='white',
                    edgecolor='none', alpha=0.7))

# Configure plot style
ax.set_ylim(0, 1.15)
ax.set_theta_zero_location('N')
ax.set_theta_direction(-1)
ax.grid(True, alpha=0.2, color='gray', linestyle=':')
ax.set_yticks([])  # Remove radial labels
ax.set_xticks([])  # Remove angular labels

# Title
title_text = "Phylogenetic Tree of Artificial Intelligence\nFrom Perceptrons to AGI (1958-2025)"
ax.set_title(title_text, fontsize=22, fontweight='bold', pad=30, loc='center')

# Add legend for major branches
print("Adding legend...")
from matplotlib.patches import Patch
legend_elements = [
    Patch(facecolor='#8B7355', label='Symbolic AI (extinct)'),
    Patch(facecolor='#9370DB', label='CNNs'),
    Patch(facecolor='#4169E1', label='RNNs (extinct)'),
    Patch(facecolor='#FFA500', label='GANs (extinct)'),
    Patch(facecolor='#228B22', label='Reinforcement Learning'),
    Patch(facecolor='#00CED1', label='Transformer Revolution'),
    Patch(facecolor='#00BFFF', label='GPT Lineage'),
    Patch(facecolor='#7B68EE', label='Claude (Anthropic)'),
    Patch(facecolor='#FF4500', label='LLaMA (Meta)'),
    Patch(facecolor='#008B8B', label='Gemini (Google)'),
    Patch(facecolor='#FF1493', label='Diffusion Models'),
    Patch(facecolor='#DC143C', label='Chinese AI'),
]

legend = ax.legend(handles=legend_elements, loc='upper left',
                  bbox_to_anchor=(0.85, 1.05), fontsize=10,
                  frameon=True, fancybox=True, shadow=True)

# Add subtitle with metadata
subtitle = "Branch thickness = model importance  |  Faded = deprecated/extinct  |  ⭐ = major innovation  |  💥 = breakthrough  |  💀 = extinction event"
fig.text(0.5, 0.02, subtitle, ha='center', fontsize=9, style='italic', color='gray')

print("Saving outputs...")
output_base = "../output/ai_tree_full_matplotlib"

plt.savefig(f"{output_base}.png", dpi=300, bbox_inches='tight', facecolor='white')
print(f"✓ Rendered PNG: {output_base}.png")

plt.savefig(f"{output_base}.pdf", bbox_inches='tight', facecolor='white')
print(f"✓ Rendered PDF: {output_base}.pdf")

plt.savefig(f"{output_base}.svg", bbox_inches='tight', facecolor='white')
print(f"✓ Rendered SVG: {output_base}.svg")

print("\n" + "="*70)
print("FULL DATASET VISUALIZATION COMPLETE - Matplotlib Approach")
print("="*70)
print(f"\nRendered {len(AI_MODELS)} AI models across 67 years of history")
print(f"Labeled {len(labeled_positions)} key models to avoid clutter")
print(f"Highlighted {len(BREAKTHROUGHS)} major breakthroughs")
print(f"Marked {len(EXTINCTION_EVENTS)} extinction events")
print("\nOutput files ready in approach_2_matplotlib/output/")
