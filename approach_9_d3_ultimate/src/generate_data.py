#!/usr/bin/env python3
"""Generate JSON data for D3.js visualization"""

import json
import sys
sys.path.insert(0, '../../data')
from ai_models import AI_MODELS

# Build hierarchical structure for D3
def build_hierarchy(models, root_name="Perceptron"):
    """Build D3-compatible hierarchy"""
    model_dict = {}
    for model_data in models:
        name, parent, year, color, importance, branch_type, extinct = model_data
        model_dict[name] = {
            "name": name,
            "parent": parent,
            "year": year,
            "color": color,
            "importance": importance,
            "branch_type": branch_type,
            "extinct": extinct,
            "children": []
        }

    # Link children
    for name, data in model_dict.items():
        if data['parent'] and data['parent'] in model_dict:
            model_dict[data['parent']]['children'].append(data)

    # Remove parent keys and return root
    def clean_node(node):
        node.pop('parent', None)
        if node['children']:
            for child in node['children']:
                clean_node(child)
        else:
            node.pop('children', None)
        return node

    return clean_node(model_dict[root_name])

hierarchy = build_hierarchy(AI_MODELS)

# Save to JSON
with open('../src/ai_data.json', 'w') as f:
    json.dump(hierarchy, f, indent=2)

print(f"✓ Generated ai_data.json with {len(AI_MODELS)} models")
