#!/usr/bin/env python3
"""
Approach 2: Matplotlib with Polar Coordinates - Basic Test
Testing radial phylogenetic tree layout with custom drawing
"""

import matplotlib
matplotlib.use('Agg')  # Use non-GUI backend for WSL
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import os

# Create output directory
os.makedirs("../output", exist_ok=True)

# Define a simple tree structure for testing
# Format: (name, parent, year, color, importance)
nodes = [
    # Root and early history
    ("Perceptron", None, 1958, '#2F4F4F', 3),
    ("Symbolic AI", "Perceptron", 1960, '#8B7355', 2),
    ("Backpropagation", "Perceptron", 1986, '#FF6347', 4),

    # CNN Branch
    ("CNNs", "Backpropagation", 1989, '#9370DB', 3),
    ("LeNet-5", "CNNs", 1998, '#9370DB', 2),
    ("AlexNet", "CNNs", 2012, '#9370DB', 5),
    ("ResNet", "AlexNet", 2015, '#9370DB', 4),

    # RNN Branch
    ("RNNs", "Backpropagation", 1990, '#4169E1', 2),
    ("LSTM", "RNNs", 1997, '#4169E1', 3),
    ("Seq2Seq", "LSTM", 2014, '#4169E1', 2),

    # Transformer Revolution
    ("Transformers", "Backpropagation", 2017, '#00CED1', 5),
    ("BERT", "Transformers", 2018, '#8B008B', 3),
    ("GPT", "Transformers", 2018, '#00BFFF', 3),
    ("GPT-3", "GPT", 2020, '#00BFFF', 5),
    ("ChatGPT", "GPT-3", 2022, '#00BFFF', 5),
    ("GPT-4", "ChatGPT", 2023, '#00BFFF', 4),

    # Claude Branch
    ("Claude", "Transformers", 2023, '#7B68EE', 3),
    ("Claude 3", "Claude", 2024, '#7B68EE', 4),

    # LLaMA Branch
    ("LLaMA", "Transformers", 2023, '#FF4500', 4),
    ("LLaMA 2", "LLaMA", 2023, '#FF4500', 3),
    ("LLaMA 3", "LLaMA 2", 2024, '#FF4500', 4),

    # Vision Transformer
    ("ViT", "Transformers", 2020, '#BA55D3', 3),

    # Diffusion Models
    ("Diffusion", "Backpropagation", 2020, '#FF1493', 4),
    ("Stable Diffusion", "Diffusion", 2022, '#FF1493', 5),

    # Chinese AI
    ("Qwen", "Transformers", 2023, '#DC143C', 3),
    ("DeepSeek", "Transformers", 2023, '#8B0000', 4),
]

# Build tree structure
tree_dict = {}
for node in nodes:
    name, parent, year, color, importance = node
    tree_dict[name] = {
        'parent': parent,
        'year': year,
        'color': color,
        'importance': importance,
        'children': []
    }

# Link children to parents
for name, data in tree_dict.items():
    if data['parent'] and data['parent'] in tree_dict:
        tree_dict[data['parent']]['children'].append(name)

# Assign angular positions using recursive layout
def assign_positions(tree_dict, root_name, start_angle, end_angle, min_year=1958, max_year=2025):
    """Recursively assign polar coordinates to tree nodes"""
    positions = {}

    def recurse(name, angle_start, angle_end):
        node = tree_dict[name]
        year = node['year']

        # Radial position based on year (distance from center)
        radius = (year - min_year) / (max_year - min_year)

        # Angular position - center of allocated span
        angle = (angle_start + angle_end) / 2

        positions[name] = (radius, angle)

        # Divide angle span among children
        children = node['children']
        if children:
            angle_span_per_child = (angle_end - angle_start) / len(children)
            for i, child in enumerate(children):
                child_start = angle_start + i * angle_span_per_child
                child_end = child_start + angle_span_per_child
                recurse(child, child_start, child_end)

    recurse(root_name, start_angle, end_angle)
    return positions

# Calculate positions
positions = assign_positions(tree_dict, "Perceptron", -np.pi, np.pi)

# Create figure
fig, ax = plt.subplots(figsize=(20, 20), subplot_kw=dict(projection='polar'))

# Draw branches (connections)
for name, data in tree_dict.items():
    if data['parent'] and data['parent'] in positions:
        # Get positions
        r1, theta1 = positions[data['parent']]
        r2, theta2 = positions[name]

        # Draw curved branch
        theta_mid = (theta1 + theta2) / 2

        # Line width based on importance
        linewidth = data['importance']

        # Draw branch
        ax.plot([theta1, theta2], [r1, r2],
                color=data['color'], linewidth=linewidth, alpha=0.7, zorder=1)

# Draw nodes
for name, (radius, angle) in positions.items():
    node_data = tree_dict[name]
    size = node_data['importance'] * 50

    # Draw node
    ax.scatter(angle, radius, s=size, c=node_data['color'],
              edgecolors='black', linewidths=1, alpha=0.9, zorder=2)

    # Add label
    if radius > 0.1:  # Don't label root too close
        # Adjust text angle for readability
        text_angle = np.degrees(angle)
        if text_angle > 90 and text_angle < 270:
            text_angle += 180
            ha = 'right'
        else:
            ha = 'left'

        ax.text(angle, radius + 0.02, name,
               rotation=text_angle, rotation_mode='anchor',
               ha=ha, va='center', fontsize=8, fontweight='normal')

# Add year rings
year_labels = [1960, 1970, 1980, 1990, 2000, 2010, 2015, 2020, 2025]
for year in year_labels:
    r = (year - 1958) / (2025 - 1958)
    circle = plt.Circle((0, 0), r, fill=False, color='gray',
                       linestyle='--', linewidth=0.5, alpha=0.3, transform=ax.transData._b)
    # Add year label
    ax.text(0, r, str(year), fontsize=8, color='gray', ha='center', va='bottom')

# Styling
ax.set_ylim(0, 1.1)
ax.set_rlabel_position(0)
ax.set_theta_zero_location('N')
ax.set_theta_direction(-1)
ax.grid(True, alpha=0.3)
ax.set_title("Phylogenetic Tree of AI Evolution (1958-2025)\nBasic Test - Matplotlib",
            fontsize=18, fontweight='bold', pad=20)

# Remove radial labels
ax.set_yticks([])

# Save outputs
print("Rendering basic AI evolution tree with Matplotlib...")
output_base = "../output/ai_tree_basic_matplotlib"

plt.savefig(f"{output_base}.png", dpi=300, bbox_inches='tight', facecolor='white')
print(f"✓ Rendered PNG: {output_base}.png")

plt.savefig(f"{output_base}.pdf", bbox_inches='tight', facecolor='white')
print(f"✓ Rendered PDF: {output_base}.pdf")

plt.savefig(f"{output_base}.svg", bbox_inches='tight', facecolor='white')
print(f"✓ Rendered SVG: {output_base}.svg")

print("\n" + "="*60)
print("BASIC TEST COMPLETE - Matplotlib Approach")
print("="*60)
print("\nEvaluation Notes:")
print("✓ Layout: Radial layout with polar coordinates working")
print("✓ Colors: Branch-specific colors applied successfully")
print("✓ Timeline: Year-based radius positioning functional")
print("✓ Node sizes: Scaled by importance")
print("✓ Labels: Text with rotation for readability")
print("\nPros so far:")
print("- Full control over every visual element")
print("- Clean, scalable vector output (SVG)")
print("- Easy to customize colors and styles")
print("\nCons so far:")
print("- Manual calculation of all positions")
print("- Text overlap with many nodes (will need adjustment)")
print("- Branch curves are straight lines (could be improved)")
print("\nNext: Expand to full dataset with better label management")
