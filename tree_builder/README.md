# AI Phylogenetic Tree Builder

An interactive web application for visualizing the evolution of artificial intelligence from the Perceptron (1958) to modern AGI (2025).

## Files

- **tree_viewer.html** - Complete standalone HTML file with embedded data (opens directly in browser!)
- **ai_tree_data.json** - Structured data for all 114 AI models (optional reference)

## Quick Start

Simply open `tree_viewer.html` in any modern web browser - no server or setup required!

## Features

### Layout Algorithms
- **Fountain Explosion** - Narrow at bottom (1958), dramatically wide at top (2025)
- **Vertical Dendrogram** - Traditional top-to-bottom tree
- **Horizontal Tree** - Left-to-right time flow
- **Radial (Semicircle)** - Polar coordinate layout

### Interactive Controls
- Canvas dimensions (1200-4800px width, 1000-4000px height)
- Width expansion (2x-20x fountain effect)
- Curve strength (0-1 for organic sweeping branches)
- Branch spacing, opacity, thickness
- Node size and font size
- Filter extinct models, toggle labels and timeline
- Label threshold by importance

### Export Options
- SVG (vector, editable in Adobe Illustrator)
- PNG (high-res raster, 2x resolution)

## Data Structure

The visualization includes:
- **114 AI models** from 1958-2025
- **17 family categories** (Transformers, CNNs, RNNs, GANs, RL, Diffusion, etc.)
- **Parent-child relationships** showing evolutionary lineages
- **Importance ratings** (1-5 stars)
- **Extinction status** for deprecated technologies
- **Breakthrough markers** for revolutionary moments

## Usage Tips

1. **Start with Fountain Explosion layout** - This matches the biological evolution tree aesthetic
2. **Adjust width expansion** (10x-15x) for dramatic spreading effect
3. **Toggle extinct models** to focus on active technologies
4. **Adjust label threshold** to reduce clutter (show only 4-5 star importance)
5. **Export high-res** by increasing canvas dimensions before exporting PNG

## Color-Coded Families

- **Dark Slate**: Origin (Perceptron)
- **Brown**: Symbolic AI (extinct)
- **Steel Blue**: Neural Networks
- **Purple**: CNNs
- **Royal Blue**: RNNs (mostly extinct)
- **Orange**: GANs (extinct)
- **Green**: Reinforcement Learning
- **Cyan**: Transformers
- **Dark Magenta**: Encoder Transformers (BERT)
- **Deep Sky Blue**: Decoder Transformers (GPT)
- **Medium Slate Blue**: Claude (Anthropic)
- **Dark Cyan**: Google AI (PaLM, Gemini)
- **Orange Red**: LLaMA (Meta)
- **Crimson**: Chinese AI
- **Deep Pink**: Diffusion Models
- **Orchid**: Multimodal Models
- **Silver**: Other

## Technical Details

- Built with D3.js v7
- Pure JavaScript, no build tools
- All data embedded (no CORS issues)
- Responsive SVG rendering
- Interactive tooltips on hover
- Real-time parameter adjustments

## Future Enhancements

To add new models, edit the embedded `data` object in tree_viewer.html or update `ai_tree_data.json` and rebuild.

---

Created for the AI Evolution Visualization Project • 2025
