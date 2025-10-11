#!/usr/bin/env python3
"""
Approach 1: ETE3 Toolkit - Basic Test with Subset of Data
Testing radial phylogenetic tree layout with key AI models
"""

from ete3 import Tree, TreeStyle, NodeStyle, TextFace, CircleFace
import os

# Create output directory
os.makedirs("../output", exist_ok=True)

# Build a basic tree structure with key milestones (Newick format)
# Using a simplified subset to test layout and styling
newick_tree = """
(
    (
        (ELIZA:8,Expert_Systems:14)Symbolic_AI:0,
        (
            (LeNet5:40,(AlexNet:14,(VGGNet:2,ResNet:3)ImageNet_Era:0)CNN_Revolution:0)CNNs:30,
            (LSTM:15,Seq2Seq:17)RNNs:23,
            (
                (
                    (BERT:1,RoBERTa:1)Encoder:0,
                    (
                        (GPT2:1,(GPT3:2,ChatGPT:2)GPT3_Era:0)GPT:0,
                        (Claude1:5,Claude3:1)Claude:0,
                        (LLaMA1:0,(LLaMA2:4,LLaMA3:9)LLaMA:0)
                    )Decoder:0
                )Transformers:1,
                ViT:3
            )Transformer_Revolution:20
        )Deep_Learning:31
    )Neural_Networks:10,
    Backpropagation:28
)Perceptron:0;
"""

# Load the tree
tree = Tree(newick_tree, format=1)

# Define color scheme for different branches
color_scheme = {
    'Symbolic_AI': '#8B7355',  # Brown/tan
    'CNNs': '#9370DB',  # Purple
    'RNNs': '#4169E1',  # Blue
    'Transformers': '#00CED1',  # Cyan
    'Encoder': '#8B008B',  # Dark purple
    'Decoder': '#00BFFF',  # Bright blue
    'GPT': '#1E90FF',  # Dodger blue
    'Claude': '#7B68EE',  # Medium slate blue
    'LLaMA': '#FF4500',  # Orange-red
    'ViT': '#BA55D3',  # Medium orchid
    'Deep_Learning': '#663399',  # Rebecca purple
}

# Apply styling to nodes
def style_tree(tree):
    """Apply custom styling to tree nodes"""
    for node in tree.traverse():
        nstyle = NodeStyle()
        nstyle["size"] = 0  # Hide default circles

        # Get node color based on lineage
        node_color = '#2F4F4F'  # Default dark slate gray
        for key in color_scheme:
            if key in node.name:
                node_color = color_scheme[key]
                break

        # Branch styling
        if node.is_leaf():
            nstyle["size"] = 8
            nstyle["fgcolor"] = node_color
            nstyle["shape"] = "circle"
            # Add text face
            tf = TextFace(node.name.replace('_', ' '), fsize=10)
            node.add_face(tf, column=0, position="branch-right")
        else:
            nstyle["size"] = 4
            nstyle["fgcolor"] = node_color
            nstyle["hz_line_width"] = 3
            nstyle["vt_line_width"] = 3
            nstyle["hz_line_color"] = node_color
            nstyle["vt_line_color"] = node_color

        node.set_style(nstyle)

# Apply styling
style_tree(tree)

# Configure tree style
ts = TreeStyle()
ts.mode = "c"  # Circular mode
ts.arc_start = -180  # Start angle
ts.arc_span = 180    # Span 180 degrees (semicircle)
ts.show_leaf_name = False  # We're using custom faces
ts.show_scale = False
ts.title.add_face(TextFace("AI Evolution Tree (Basic Test - ETE3)", fsize=20, bold=True), column=0)

# Render the tree
print("Rendering basic AI evolution tree with ETE3...")
output_file = "../output/ai_tree_basic"

# Try rendering to different formats
try:
    tree.render(f"{output_file}.png", w=2000, h=2000, tree_style=ts, dpi=300)
    print(f"✓ Rendered PNG: {output_file}.png")
except Exception as e:
    print(f"✗ PNG rendering failed: {e}")

try:
    tree.render(f"{output_file}.pdf", tree_style=ts)
    print(f"✓ Rendered PDF: {output_file}.pdf")
except Exception as e:
    print(f"✗ PDF rendering failed: {e}")

try:
    tree.render(f"{output_file}.svg", tree_style=ts)
    print(f"✓ Rendered SVG: {output_file}.svg")
except Exception as e:
    print(f"✗ SVG rendering failed: {e}")

print("\n" + "="*60)
print("BASIC TEST COMPLETE")
print("="*60)
print("\nEvaluation Notes:")
print("- Layout: Testing radial/circular layout")
print("- Colors: Basic color scheme applied to branches")
print("- Labels: Testing leaf node labeling")
print("- Formats: Attempting PNG, PDF, and SVG exports")
print("\nNext: Expand to full dataset with advanced styling")
