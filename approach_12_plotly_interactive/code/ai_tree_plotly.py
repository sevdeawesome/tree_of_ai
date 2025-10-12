#!/usr/bin/env python3
"""
AI Evolution Tree - Interactive Plotly Visualization
Approach 12: Interactive web-based tree with zoom, pan, and hover details
"""

import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np
from math import radians, cos, sin, pi
import sys
import os

# Add parent directory to path to import data
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
from data.ai_models import AI_MODELS, COLOR_SCHEME, EXTINCTION_EVENTS, BREAKTHROUGHS

class PlotlyAITree:
    def __init__(self):
        self.models = AI_MODELS
        self.color_scheme = COLOR_SCHEME
        self.extinction_events = EXTINCTION_EVENTS
        self.breakthroughs = BREAKTHROUGHS
        
        # Layout parameters
        self.max_radius = 10
        self.min_radius = 1
        self.center_x = 0
        self.center_y = 0
        
    def build_tree_structure(self):
        """Build hierarchical tree structure from models data"""
        # Create model lookup
        model_dict = {name: {'parent': parent, 'year': year, 'color': color, 
                           'importance': importance, 'branch_type': branch_type, 
                           'extinct': extinct}
                     for name, parent, year, color, importance, branch_type, extinct in self.models}
        
        # Build tree structure
        tree = {}
        for name, data in model_dict.items():
            tree[name] = {
                'parent': data['parent'],
                'children': [],
                'year': data['year'],
                'color': data['color'],
                'importance': data['importance'],
                'branch_type': data['branch_type'],
                'extinct': data['extinct']
            }
        
        # Add children relationships
        for name, data in tree.items():
            if data['parent']:
                tree[data['parent']]['children'].append(name)
        
        return tree
    
    def calculate_positions(self, tree):
        """Calculate radial positions for all nodes"""
        positions = {}
        
        # Get root node
        root = None
        for name, data in tree.items():
            if data['parent'] is None:
                root = name
                break
        
        if not root:
            raise ValueError("No root node found")
        
        # Calculate angular distribution for children
        def assign_angles(node_name, start_angle, angle_span):
            if node_name not in tree:
                return
            
            children = tree[node_name]['children']
            if not children:
                return
            
            # Distribute children evenly in the angle span
            child_angles = []
            for i, child in enumerate(children):
                angle = start_angle + (i / (len(children) - 1)) * angle_span if len(children) > 1 else start_angle + angle_span / 2
                child_angles.append(angle)
            
            # Recursively assign angles to grandchildren
            for child, angle in zip(children, child_angles):
                positions[child] = angle
                # Calculate how much space this subtree needs
                subtree_size = self._count_descendants(tree, child)
                child_span = (angle_span / len(children)) * (subtree_size / sum(self._count_descendants(tree, c) for c in children))
                assign_angles(child, angle - child_span/2, child_span)
        
        # Start with full circle for root
        positions[root] = 0
        assign_angles(root, -pi/2, pi)  # Start from top, span half circle
        
        return positions
    
    def _count_descendants(self, tree, node_name):
        """Count total descendants of a node"""
        if node_name not in tree:
            return 0
        
        count = 1  # Count self
        for child in tree[node_name]['children']:
            count += self._count_descendants(tree, child)
        return count
    
    def calculate_radial_positions(self, tree):
        """Calculate radial distances based on years"""
        # Normalize years to radial distances
        years = [data['year'] for data in tree.values()]
        min_year, max_year = min(years), max(years)
        
        radial_positions = {}
        for name, data in tree.items():
            # Map year to radius (1958 = min_radius, 2025 = max_radius)
            normalized_year = (data['year'] - min_year) / (max_year - min_year)
            radius = self.min_radius + normalized_year * (self.max_radius - self.min_radius)
            radial_positions[name] = radius
        
        return radial_positions
    
    def create_interactive_tree(self):
        """Create interactive Plotly tree visualization"""
        tree = self.build_tree_structure()
        angular_positions = self.calculate_positions(tree)
        radial_positions = self.calculate_radial_positions(tree)
        
        # Prepare data for plotting
        nodes_x = []
        nodes_y = []
        node_text = []
        node_colors = []
        node_sizes = []
        hover_text = []
        
        # Add nodes
        for name, data in tree.items():
            angle = angular_positions[name]
            radius = radial_positions[name]
            
            x = self.center_x + radius * cos(angle)
            y = self.center_y + radius * sin(angle)
            
            nodes_x.append(x)
            nodes_y.append(y)
            node_text.append(name)
            node_colors.append(data['color'])
            
            # Size based on importance
            size = 8 + data['importance'] * 3
            node_sizes.append(size)
            
            # Hover information
            status = "Extinct" if data['extinct'] else "Active"
            hover = f"<b>{name}</b><br>"
            hover += f"Year: {data['year']}<br>"
            hover += f"Branch: {data['branch_type']}<br>"
            hover += f"Importance: {data['importance']}/5<br>"
            hover += f"Status: {status}<br>"
            if data['parent']:
                hover += f"Parent: {data['parent']}"
            
            hover_text.append(hover)
        
        # Create edge data
        edge_x = []
        edge_y = []
        edge_colors = []
        
        for name, data in tree.items():
            if data['parent']:
                # Parent position
                parent_angle = angular_positions[data['parent']]
                parent_radius = radial_positions[data['parent']]
                parent_x = self.center_x + parent_radius * cos(parent_angle)
                parent_y = self.center_y + parent_radius * sin(parent_angle)
                
                # Child position
                child_angle = angular_positions[name]
                child_radius = radial_positions[name]
                child_x = self.center_x + child_radius * cos(child_angle)
                child_y = self.center_y + child_radius * sin(child_angle)
                
                # Add edge (line from parent to child)
                edge_x.extend([parent_x, child_x, None])
                edge_y.extend([parent_y, child_y, None])
                
                # Edge color (faded if extinct)
                edge_color = data['color']
                if data['extinct']:
                    edge_color = f"rgba({int(edge_color[1:3], 16)}, {int(edge_color[3:5], 16)}, {int(edge_color[5:7], 16)}, 0.3)"
                else:
                    edge_color = f"rgba({int(edge_color[1:3], 16)}, {int(edge_color[3:5], 16)}, {int(edge_color[5:7], 16)}, 0.8)"
                
                edge_colors.append(edge_color)
        
        # Create timeline rings
        timeline_rings_x = []
        timeline_rings_y = []
        
        years = [1958, 1960, 1970, 1980, 1990, 2000, 2010, 2015, 2020, 2025]
        for year in years:
            normalized_year = (year - 1958) / (2025 - 1958)
            radius = self.min_radius + normalized_year * (self.max_radius - self.min_radius)
            
            # Create circle
            angles = np.linspace(0, 2*pi, 100)
            ring_x = [self.center_x + radius * cos(a) for a in angles]
            ring_y = [self.center_y + radius * sin(a) for a in angles]
            
            timeline_rings_x.extend(ring_x + [None])
            timeline_rings_y.extend(ring_y + [None])
        
        # Create the plot
        fig = go.Figure()
        
        # Add timeline rings
        fig.add_trace(go.Scatter(
            x=timeline_rings_x,
            y=timeline_rings_y,
            mode='lines',
            line=dict(color='lightgray', width=1, dash='dot'),
            showlegend=False,
            hoverinfo='skip'
        ))
        
        # Add edges
        fig.add_trace(go.Scatter(
            x=edge_x,
            y=edge_y,
            mode='lines',
            line=dict(color='gray', width=2),
            showlegend=False,
            hoverinfo='skip'
        ))
        
        # Add nodes
        fig.add_trace(go.Scatter(
            x=nodes_x,
            y=nodes_y,
            mode='markers+text',
            marker=dict(
                size=node_sizes,
                color=node_colors,
                line=dict(width=2, color='white'),
                opacity=0.8
            ),
            text=node_text,
            textposition="middle center",
            textfont=dict(size=10, color='white'),
            hovertext=hover_text,
            hoverinfo='text',
            showlegend=False
        ))
        
        # Add breakthrough markers
        breakthrough_x = []
        breakthrough_y = []
        breakthrough_text = []
        
        for breakthrough, year, emoji in self.breakthroughs:
            if breakthrough in angular_positions:
                angle = angular_positions[breakthrough]
                radius = radial_positions[breakthrough]
                
                x = self.center_x + radius * cos(angle)
                y = self.center_y + radius * sin(angle)
                
                breakthrough_x.append(x)
                breakthrough_y.append(y)
                breakthrough_text.append(emoji)
        
        if breakthrough_x:
            fig.add_trace(go.Scatter(
                x=breakthrough_x,
                y=breakthrough_y,
                mode='markers+text',
                marker=dict(size=20, color='gold', symbol='star'),
                text=breakthrough_text,
                textposition="middle center",
                textfont=dict(size=16),
                showlegend=False,
                hoverinfo='skip'
            ))
        
        # Update layout
        fig.update_layout(
            title=dict(
                text="AI Evolution Tree (1958-2025) - Interactive",
                x=0.5,
                font=dict(size=20)
            ),
            showlegend=False,
            plot_bgcolor='white',
            paper_bgcolor='white',
            xaxis=dict(
                showgrid=False,
                zeroline=False,
                showticklabels=False,
                scaleanchor="y",
                scaleratio=1
            ),
            yaxis=dict(
                showgrid=False,
                zeroline=False,
                showticklabels=False
            ),
            width=1000,
            height=800,
            margin=dict(l=50, r=50, t=80, b=50)
        )
        
        return fig
    
    def save_interactive_html(self, filename="ai_tree_plotly.html"):
        """Save interactive tree as HTML file"""
        fig = self.create_interactive_tree()
        
        output_path = os.path.join(os.path.dirname(__file__), '..', 'output', filename)
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        fig.write_html(output_path, config={'displayModeBar': True})
        print(f"Interactive tree saved to: {output_path}")
        
        return output_path

def main():
    """Create interactive Plotly AI evolution tree"""
    print("Creating interactive Plotly AI evolution tree...")
    
    tree_viz = PlotlyAITree()
    output_path = tree_viz.save_interactive_html()
    
    print("✅ Interactive tree created successfully!")
    print(f"📁 Output: {output_path}")
    print("🌐 Open in browser to interact (zoom, pan, hover for details)")

if __name__ == "__main__":
    main()

