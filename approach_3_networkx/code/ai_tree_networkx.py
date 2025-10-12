#!/usr/bin/env python3
"""
Approach 3: NetworkX with Custom Radial Layout
Using NetworkX for graph structure and custom layout algorithm
"""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import sys
import os

# Add data directory to path
sys.path.insert(0, '../../data')
from ai_models import AI_MODELS, EXTINCTION_EVENTS, BREAKTHROUGHS

# Create output directory
os.makedirs("../output", exist_ok=True)

print("Building AI evolution tree with NetworkX...")
print(f"Total models: {len(AI_MODELS)}")

# Create directed graph
G = nx.DiGraph()

# Add nodes with attributes
for model_data in AI_MODELS:
    name, parent, year, color, importance, branch_type, extinct = model_data
    G.add_node(name,
              year=year,
              color=color,
              importance=importance,
              branch_type=branch_type,
              extinct=extinct,
              parent=parent)

    # Add edge from parent
    if parent:
        G.add_edge(parent, name)

print(f"Graph created: {G.number_of_nodes()} nodes, {G.number_of_edges()} edges")

# Custom radial layout based on tree hierarchy
def hierarchical_radial_layout(G, root, min_year=1958, max_year=2026):
    """
    Create radial layout where:
    - Radius = year (temporal position)
    - Angle = hierarchical position in tree
    """
    pos = {}

    # Get all descendants for angular allocation
    def get_leaf_count(node):
        """Count leaf nodes in subtree"""
        successors = list(G.successors(node))
        if not successors:
            return 1
        return sum(get_leaf_count(s) for s in successors)

    # Recursive position assignment
    def assign_positions(node, angle_start, angle_span, depth=0):
        # Get node attributes
        year = G.nodes[node].get('year', 1958)

        # Radial position based on year
        radius = (year - min_year) / (max_year - min_year)

        # Get children
        children = list(G.successors(node))

        if not children:
            # Leaf node - use center of span
            angle = angle_start + angle_span / 2
            pos[node] = (radius * np.cos(angle), radius * np.sin(angle))
        else:
            # Internal node - calculate weighted position
            total_leaves = sum(get_leaf_count(child) for child in children)

            # Assign angular space to children proportionally
            current_angle = angle_start
            child_positions = []

            for child in children:
                child_leaves = get_leaf_count(child)
                child_span = angle_span * (child_leaves / total_leaves)
                child_angle = assign_positions(child, current_angle, child_span, depth + 1)
                child_positions.append(child_angle)
                current_angle += child_span

            # Position parent at weighted average of children angles
            avg_angle = np.mean([np.arctan2(pos[c][1], pos[c][0]) for c in children])
            pos[node] = (radius * np.cos(avg_angle), radius * np.sin(avg_angle))

            return avg_angle

        return angle_start + angle_span / 2

    # Start from root
    assign_positions(root, -np.pi, 2 * np.pi)

    return pos

print("Calculating layout...")
pos = hierarchical_radial_layout(G, 'Perceptron')

# Create figure
fig, ax = plt.subplots(figsize=(24, 24))

print("Drawing graph...")

# Draw edges with custom styling
for edge in G.edges():
    parent, child = edge
    x_coords = [pos[parent][0], pos[child][0]]
    y_coords = [pos[parent][1], pos[child][1]]

    # Get child attributes for styling
    child_data = G.nodes[child]
    color = child_data['color']
    importance = child_data['importance']
    extinct = child_data['extinct']

    linewidth = importance * 1.5
    alpha = 0.3 if extinct else 0.7

    ax.plot(x_coords, y_coords,
           color=color, linewidth=linewidth, alpha=alpha,
           solid_capstyle='round', zorder=1)

# Draw nodes
for node in G.nodes():
    node_data = G.nodes[node]
    x, y = pos[node]

    size = node_data['importance'] * 80
    color = node_data['color']
    alpha = 0.4 if node_data['extinct'] else 0.9

    ax.scatter(x, y, s=size, c=color,
              edgecolors='black', linewidths=0.5,
              alpha=alpha, zorder=2)

# Add timeline rings
print("Adding timeline rings...")
year_labels = [1960, 1970, 1980, 1990, 2000, 2010, 2015, 2020, 2025]
for year in year_labels:
    r = (year - 1958) / (2026 - 1958)
    circle = plt.Circle((0, 0), r, fill=False, color='gray',
                       linestyle='--', linewidth=0.5, alpha=0.3)
    ax.add_patch(circle)

    # Year label
    ax.text(0, r + 0.03, str(year), fontsize=9, color='gray',
           ha='center', va='bottom', alpha=0.6)

# Add labels for important nodes
print("Adding labels...")
labeled_positions = []

def is_label_clear(x, y, min_distance=0.08):
    """Check if label position is clear"""
    for prev_x, prev_y in labeled_positions:
        dist = np.sqrt((x - prev_x)**2 + (y - prev_y)**2)
        if dist < min_distance:
            return False
    return True

for node in G.nodes():
    node_data = G.nodes[node]
    x, y = pos[node]

    # Label important nodes
    is_breakthrough = any(node == b[0] for b in BREAKTHROUGHS)

    if node_data['importance'] >= 3 or is_breakthrough:
        if is_label_clear(x, y):
            # Calculate angle for text rotation
            angle = np.arctan2(y, x)
            text_angle = np.degrees(angle)

            if text_angle > 90 and text_angle < 270:
                text_angle += 180
                ha = 'right'
            else:
                ha = 'left'

            # Add breakthrough marker
            label = node
            if is_breakthrough:
                marker = next((b[2] for b in BREAKTHROUGHS if b[0] == node), '')
                label = f"{marker} {node}"

            fontsize = 7 + node_data['importance'] * 0.5
            fontweight = 'bold' if node_data['importance'] >= 5 else 'normal'

            # Offset label slightly from node
            r = np.sqrt(x**2 + y**2)
            offset = 0.02
            label_x = x + offset * np.cos(angle) if x != 0 else x
            label_y = y + offset * np.sin(angle) if y != 0 else y + offset

            ax.text(label_x, label_y, label,
                   rotation=text_angle, rotation_mode='anchor',
                   ha=ha, va='center', fontsize=fontsize,
                   fontweight=fontweight, alpha=0.9)

            labeled_positions.append((x, y))

# Add extinction event markers
print("Adding extinction events...")
for event_name, start_year, end_year in EXTINCTION_EVENTS:
    r_start = (start_year - 1958) / (2026 - 1958)
    r_end = (end_year - 1958) / (2026 - 1958)
    r_mid = (r_start + r_end) / 2

    # Add shading ring
    theta_full = np.linspace(0, 2*np.pi, 100)
    x_inner = r_start * np.cos(theta_full)
    y_inner = r_start * np.sin(theta_full)
    x_outer = r_end * np.cos(theta_full)
    y_outer = r_end * np.sin(theta_full)

    ax.fill(np.concatenate([x_inner, x_outer[::-1]]),
           np.concatenate([y_inner, y_outer[::-1]]),
           color='gray', alpha=0.05, zorder=0)

    # Label
    ax.text(0.7, r_mid, f"Extinction: {event_name}",
           fontsize=8, color='darkgray', style='italic',
           ha='center', va='center', alpha=0.6,
           bbox=dict(boxstyle='round,pad=0.3', facecolor='white',
                    edgecolor='none', alpha=0.7))

# Configure plot
ax.set_aspect('equal')
ax.set_xlim(-1.2, 1.2)
ax.set_ylim(-1.2, 1.2)
ax.axis('off')

# Title
title_text = "Phylogenetic Tree of Artificial Intelligence\nFrom Perceptrons to AGI (1958-2025)\nNetworkX Implementation"
ax.set_title(title_text, fontsize=22, fontweight='bold', pad=30)

# Add legend
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

ax.legend(handles=legend_elements, loc='upper right',
         fontsize=10, frameon=True, fancybox=True, shadow=True)

# Subtitle
subtitle = "Branch thickness = importance  |  Faded = extinct  |  NetworkX graph library"
fig.text(0.5, 0.02, subtitle, ha='center', fontsize=9, style='italic', color='gray')

print("Saving outputs...")
output_base = "../output/ai_tree_networkx"

plt.savefig(f"{output_base}.png", dpi=300, bbox_inches='tight', facecolor='white')
print(f"✓ Rendered PNG: {output_base}.png")

plt.savefig(f"{output_base}.pdf", bbox_inches='tight', facecolor='white')
print(f"✓ Rendered PDF: {output_base}.pdf")

plt.savefig(f"{output_base}.svg", bbox_inches='tight', facecolor='white')
print(f"✓ Rendered SVG: {output_base}.svg")

plt.close()

print("\n" + "="*70)
print("NETWORKX IMPLEMENTATION COMPLETE")
print("="*70)
print(f"\nRendered {G.number_of_nodes()} nodes and {G.number_of_edges()} edges")
print(f"Labeled {len(labeled_positions)} important nodes")
print("\nNetworkX provides:")
print("✓ Built-in graph algorithms")
print("✓ Clean tree structure representation")
print("✓ Easy to compute graph metrics (depth, centrality, etc.)")
print("\nOutput files ready in approach_3_networkx/output/")
