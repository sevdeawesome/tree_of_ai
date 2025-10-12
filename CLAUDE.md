# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This project creates a publication-quality phylogenetic tree visualization of AI evolution from the Perceptron (1958) to modern AGI race (2025), styled like biological "Tree of Life" diagrams.

**Visual Reference**: The `evolution.png` file shows the target aesthetic - a radial/semicircular biological phylogenetic tree with:
- **Radial fountain explosion**: Narrow at bottom (1958), dramatically wide at top (2025)
- **Organic sweeping curves**: Branches curve outward as they rise, not straight lines
- **Temporal expansion**: Later periods 5-10x wider than early periods
- **Dense branching**: Hundreds of species/models packed beautifully
- **Color-coded families**: Easy visual distinction
- **Timeline progression**: Clear vertical time flow
- **Natural aesthetic**: Feels like a living organism growing and spreading

The key insight: This is NOT a radial/circular layout - it's a **vertical fountain explosion** where branches spread horizontally as time progresses upward.

## New Systematic Approach (Feb 2025)

After exploring 10+ visualization approaches, we're building a proper **flexible system**:

### Two-Part Architecture:

1. **Data Layer** (`ai_tree_data.json`):
   - Clean JSON format with all 114 models
   - Parent-child relationships
   - Metadata (year, family, importance, extinct status)
   - Families with colors and descriptions
   - Breakthrough markers

2. **Interactive Visualization Layer** (`tree_viewer.html`):
   - Reads JSON data
   - Dynamic controls for layout, style, density
   - Multiple layout algorithms (radial fountain, vertical, horizontal, force-directed)
   - Real-time adjustments (colors, fonts, curves, spacing)
   - Filters (families, date ranges, extinct/active)
   - Export functionality (SVG, PNG, high-res)

### Why This Approach:

- **Separation of concerns**: Data vs presentation
- **Iterability**: Change data without touching code
- **Flexibility**: Try different visual styles instantly
- **Maintainability**: Easy to add new models
- **Exportability**: Generate high-res versions in any style

## Project Structure

Organize code and outputs in clearly labeled folders:

```
tree_of_ai/
├── approach_1_ete3/          # ETE3 toolkit implementation
│   ├── code/                 # Source code (.py files)
│   ├── output/               # Generated visualizations
│   └── README.md             # Approach-specific notes, pros/cons
├── approach_2_matplotlib/    # Matplotlib/Plotly implementation
│   ├── code/
│   ├── output/
│   └── README.md
├── approach_3_networkx/      # NetworkX custom layout implementation
│   ├── code/
│   ├── output/
│   └── README.md
├── approach_4_d3js/          # D3.js implementation (if needed)
│   ├── src/                  # JavaScript/HTML/CSS
│   ├── output/
│   └── README.md
├── data/                     # Shared data files (tree structure, metadata)
├── utils/                    # Shared utility functions
├── final_output/             # Best/final visualizations
├── evolution.png             # Reference image
├── evolution.pdf             # Reference image
├── instructions.md           # Full project specification
└── CLAUDE.md                 # This file
```

### Code Organization Standards
- **One approach per folder** - Keep implementations isolated
- **Separate code from output** - Never mix .py files with .png/.svg files
- **Include approach README** - Document pros, cons, and evaluation scores
- **Shared code in utils/** - Common functions (color mapping, data parsing)
- **Final outputs centralized** - Copy best visualizations to `final_output/`

## Development Commands

### Environment Setup
```bash
pip install ete3 PyQt5 --break-system-packages
pip install matplotlib plotly networkx pandas
```

### Testing Approach
1. Create basic radial tree with subset of data to test feasibility
2. Expand to full dataset
3. Iterate on visual quality and styling
4. Save all outputs to approach-specific `output/` folder

## Data Architecture

The visualization encodes 67 years of AI history with complex relationships:

### Major Branches & Color Scheme
- **Symbolic AI**: Brown/tan (1950s-1980s, extinct after AI Winter)
- **CNNs**: Purple/pink (1989-2020, then convergent with Transformers)
- **RNNs**: Blue → gray (mostly extinct by 2020)
- **GANs**: Yellow-orange → gray (extinct by 2023, displaced by Diffusion)
- **Reinforcement Learning**: Green (ongoing)
- **Transformers - Encoder**: Vibrant purple (BERT lineage)
- **Transformers - Decoder**: Bright cyan/blue (GPT lineage, DOMINANT)
- **Diffusion Models**: Pink/magenta (dominant for images)
- **Chinese AI**: Red/gold spectrum (explosive growth 2023+)
- **Future/AGI**: Iridescent/glowing

### Critical Evolutionary Events
- **Extinction Events**: AI Winter (1974-1980), RNN Decline (2018-2020), GAN Displacement (2022-2023)
- **Major Innovations**: Backpropagation (1986), AlexNet (2012), ResNet (2015), Attention mechanism (2017), GPT-3 (2020)
- **Breakthrough Moments**: AlexNet ImageNet win, ChatGPT launch (Nov 2022), DeepSeek R1 ($6M training, Jan 2025)
- **Radiation Events**: Transformer Revolution (2017), LLaMA leak creating thousands of derivatives (March 2023)

### Key Lineages
- **Decoder-Only Transformers** (DOMINANT): GPT → GPT-2 → GPT-3 → ChatGPT → GPT-4 series
- **Anthropic Claude**: Splits from GPT lineage, purple-blue coloring
- **Meta LLaMA**: Most influential open source, spawns massive derivative ecosystem
- **Chinese AI Explosion**: 10+ major competing branches (Qwen, ERNIE, DeepSeek, etc.)
- **Convergent Evolution**: Vision Transformers (2020) filling CNN niche

### Visual Encoding Rules
- **Branch Thickness**: Thicker = currently dominant/active; Thinner/faded = deprecated/extinct
- **Timeline Rings**: 1950, 1960, 1970, 1980, 1990, 2000, 2010, 2015, 2020, 2025, 2030
- **Markers**: ⭐ innovations, 💀 extinctions, 💥 breakthroughs

## Technical Requirements

### Output Specifications
- **Resolution**: Minimum 3000x3000 pixels for print quality
- **Format**: SVG (vector) preferred, or high-res PNG/PDF
- **Aspect Ratio**: Square or landscape
- **Font**: Clean sans-serif (Arial, Helvetica) or scientific serif (Times, Palatino)
- **Layout**: Radial/semicircular matching reference image
- **Exportable**: Must be editable in Adobe Illustrator

### Evaluation Criteria
Rate each approach on:
1. Visual Quality (professional, publication-ready?)
2. Readability (clear, non-overlapping labels?)
3. Accuracy (correct evolutionary relationships?)
4. Aesthetic (matches reference beauty?)
5. Extensibility (easy to update with new models?)

## Complete Data Structure

Full evolutionary tree organized by branch is documented in `instructions.md` lines 42-258, including:
- ROOT: Perceptron (1958) as origin point
- 6 major branch systems (Symbolic, Neural, Transformer, Diffusion, RL, Chinese AI)
- 100+ individual models with dates and relationships
- Future projections to AGI/ASI (2027-2030+)

## Deliverables

For each visualization approach:
1. Generated visualization file(s)
2. Explanation of pros/cons
3. Complete source code
4. Documentation for updating/extending with new models

Final recommendation should include reasoning based on evaluation criteria.

## Key Insights for Implementation

- This is a **narrative visualization** - it tells the story of AI from humble beginnings to AGI precipice
- **Lineage matters**: Show clear parent-child relationships (e.g., GPT → GPT-2 → GPT-3)
- **Extinction is part of evolution**: Faded/thin branches for RNNs and GANs are intentional
- **Time is exponential**: More crowded near 2020-2025 than 1958-2000
- **Chinese AI explosion** (2023+) is a major recent radiation event, comparable to Transformer revolution (2017)
