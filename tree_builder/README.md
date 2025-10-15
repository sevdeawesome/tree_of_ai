# AI Phylogenetic Tree Viewer

Interactive web-based visualization of AI evolution from 1958 (Perceptron) to 2025 (AGI race), styled as a biological phylogenetic tree.

## Visual Reference

**Design Inspiration**: See `evolution.png` and `evolution.pdf` - biological phylogenetic trees with:
- Radial/semicircular layout
- Narrow base expanding to wide canopy
- Organic, sweeping branch curves
- Text labels on outer perimeter
- Natural "Tree of Life" aesthetic

The goal is to match this museum-quality biological appearance.

## Quick Start

Open `tree_viewer.html` in a modern browser. No build process, no server required.

## Features

### Layouts
- **Radial** - Biological tree with concentric year rings (matches evolution.png)
- **Fountain** - Vertical explosion with expanding width
- **Vertical** - Traditional dendrogram
- **Horizontal** - Left-to-right timeline

### Controls
- **Text Styling** - 10 Google Fonts, sizes, weights, per-family colors
- **Label Positioning** - At nodes, on perimeter, extended from perimeter
- **Timeline Ring Spacing** - Adjust relative spacing between years
- **Family Colors** - Customize all 17 AI families
- **Visual Style** - Opacity, thickness, curves, node sizes
- **Filters** - Date ranges, importance, extinct models

### Keyboard Navigation
- **WASD/Arrows** - Pan canvas
- **Z/X** - Zoom in/out

### Export
- **SVG** - Vector (editable in Illustrator)
- **PNG** - High-res 2x

## Data

114 models across 17 families:
- Symbolic AI, Neural Networks, CNNs, RNNs (extinct)
- GANs (extinct), Reinforcement Learning
- Transformers, BERT, GPT, Claude, Gemini
- LLaMA, Chinese AI, Diffusion, Multimodal

## Common Tasks

**Publication-ready export**: Set canvas to 6000×6000, use radial + extended perimeter labels, export PNG

**Focus modern AI**: Filter 2020-2025, adjust year spacing, threshold 3+

**Custom colors**: Family Colors section → customize all 17 families

## Technical

- Single-file HTML app
- D3.js v7 rendering
- Embedded JSON data (114 models)
- Real-time updates

## Troubleshooting

- **Overlapping labels?** Increase spread/repulsion, use perimeter positioning
- **Squashed tree?** Increase vertical spread or outer radius
- **Export fails?** Check popup blocker, try smaller canvas or SVG

## Files

```
tree_builder/
├── tree_viewer.html    # Main application
├── README.md           # This file
└── CLAUDE.md           # Developer docs
```

See CLAUDE.md for implementation details.
