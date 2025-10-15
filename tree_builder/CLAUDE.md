# CLAUDE.md - AI Tree Viewer

This file provides guidance to Claude Code when working with the AI Phylogenetic Tree interactive viewer.

## Project Overview

This is an **interactive web-based visualization tool** for exploring the evolution of AI from 1958 (Perceptron) to 2025 (AGI race). It's designed to create publication-quality phylogenetic trees inspired by biological "Tree of Life" diagrams.

**Status**: ✅ Production-ready interactive tool with extensive customization options

**Visual Reference**: `evolution.png` and `evolution.pdf` show the target aesthetic - radial biological phylogenetic tree with organic curves, perimeter labels, and natural "Tree of Life" appearance.

## Key Files

- `tree_viewer.html` - Single-file web application (no build process needed)
  - Embedded JSON data (114 AI models with parent-child relationships)
  - D3.js v7 for rendering
  - Interactive controls for all visualization parameters
  - Export to SVG and high-res PNG

## Architecture

### Data Structure (Embedded in HTML)

```javascript
const data = {
  metadata: {
    title, subtitle, version, totalModels, yearRange
  },
  families: {
    // 17 AI families with colors and descriptions
    "decoder": { label: "Decoder Transformers (GPT)", color: "#00BFFF", ... },
    "diffusion": { label: "Diffusion Models", color: "#FF1493", ... },
    ...
  },
  models: [
    // 114 models with relationships
    {
      id: "gpt-4",
      name: "GPT-4",
      year: 2023,
      family: "decoder",
      parents: ["chatgpt"],
      importance: 5,
      extinct: false,
      description: "...",
      breakthrough: false
    },
    ...
  ]
}
```

### Layout Algorithms

1. **Radial** (Primary) - Biological tree style matching `evolution.png` reference
   - Concentric rings for years
   - Angles distributed by descendant count
   - Customizable inner/outer radius, angle span, rotation
   - **Relative spacing system** - each year's spacing from previous year

2. **Fountain** - Vertical explosion with expanding width
3. **Vertical** - Traditional dendrogram
4. **Horizontal** - Left-to-right tree

### Control System

All parameters exposed via sidebar controls:
- **Layout**: Algorithm selection, canvas dimensions
- **Foundational**: Horizontal/vertical spread, center offsets, node repulsion
- **Radial**: Angle span, start angle, inner/outer radius
- **Timeline Ring Spacing**: Per-year relative spacing controls
- **Branch**: Curve style (bezier/step/diagonal/organic), curve intensity
- **Visual Style**: Opacity, thickness, node size, colors
- **Text Styling**: 10 Google Fonts, size, weight, opacity, per-family colors
- **Label Positioning**: At node, on perimeter, extended from perimeter (radial only)
- **Filters**: Extinct models, labels, timeline, date range, importance threshold
- **Family Colors**: Per-family color customization with live preview

### Interactive Features

1. **Keyboard Navigation**
   - WASD or Arrow keys: Pan canvas
   - Z / X: Zoom in / out
   - Disabled when typing in input fields

2. **Dragging**
   - Nodes: Click and drag to reposition (stores custom positions)
   - Timeline rings: Drag to adjust spacing (updates relative spacing values)

3. **Export**
   - SVG: Vector format for editing in Illustrator
   - PNG: 2x resolution for print quality

## Implementation Notes

### Important Patterns

1. **Single-file architecture** - Everything embedded in one HTML file for portability
2. **No build process** - Open directly in browser (file:// or http://)
3. **Declarative config** - All settings flow through `getConfig()` → `render()`
4. **State management**:
   - `nodePositions` - Map of manually repositioned nodes
   - `yearRadii` - Map of custom year spacings (relative, not absolute!)
   - `familyColors` - Map of custom family colors

### Timeline Ring Spacing System

**Critical**: The `yearRadii` object stores **RELATIVE spacing** (distance from previous year), NOT absolute radii.

```javascript
// In layoutRadial() and drawTimelineRadial():
let currentRadius = config.innerRadius * config.verticalSpread;
years.forEach((year, i) => {
  if (i === 0) {
    yearRadiusMap[year] = currentRadius; // First year = inner radius
  } else {
    const autoSpacing = radiusScale(year) - radiusScale(prevYear);
    const customSpacing = yearRadii[year]; // Relative spacing!
    const spacing = customSpacing !== undefined ? customSpacing : autoSpacing;
    currentRadius += spacing; // Cumulative
    yearRadiusMap[year] = currentRadius;
  }
});
```

### Radial Label Positioning

Three modes (radial layout only):
- **node**: Labels at node position (default)
- **perimeter**: Labels float at node's radius + distance
- **extended**: Labels all align at outer perimeter ring
  - Draws connector lines from node to label
  - Text rotates radially, flips on left side for readability

### Font System

10 Google Fonts pre-loaded:
- Serif: Crimson Text, Playfair Display, EB Garamond, Libre Baskerville, Lora, Merriweather
- Sans-serif: Inter, Source Sans Pro, Roboto, Montserrat

Applied via `font-family` attribute on text elements.

### Color System

Two modes:
1. **Family colors** (default) - Each model colored by its family
2. **Uniform color** - Single text color for all labels

Family colors customizable via sidebar color pickers → updates `familyColors` map → re-render.

## Development Workflow

### Making Changes

1. Edit `tree_viewer.html` directly
2. Refresh browser to see changes
3. All JavaScript in `<script>` tag at bottom
4. All CSS in `<style>` tag in `<head>`

### Adding New Controls

```javascript
// 1. Add HTML control in sidebar
<div class="control-group">
  <label>New Setting</label>
  <input type="number" id="newSetting" value="42">
</div>

// 2. Add to getConfig()
newSetting: parseInt(document.getElementById('newSetting').value)

// 3. Use in render pipeline
function drawSomething(svg, nodes, config) {
  // Access via config.newSetting
}

// 4. Add to resetSettings() if needed
document.getElementById('newSetting').value = 42;
```

### Adding New Models

Edit the embedded data object (line ~610):
```javascript
const data = {
  families: { ... },
  models: [
    // Add new model
    {
      id: "new-model",
      name: "New Model",
      year: 2025,
      family: "decoder",
      parents: ["gpt-4o"],
      importance: 4,
      extinct: false,
      description: "Description here"
    },
    ...
  ]
}
```

### Adding New Families

```javascript
// 1. Add to data.families
"new_family": {
  label: "New AI Family",
  color: "#FF5733",
  description: "Description of this AI family"
}

// 2. Models will auto-inherit color
// 3. Family color picker auto-generates in sidebar
```

## Visual Design Philosophy

### Goal: Museum-Quality Biological Phylogeny

Inspired by `evolution.png` and `evolution.pdf` reference images in this folder:
- **Organic, sweeping curves** - Not rigid geometric lines
- **Temporal expansion** - Recent years (2020-2025) much denser than early years
- **Extinction visible** - Faded branches/nodes for deprecated models (RNNs, GANs)
- **Color-coded families** - Easy visual distinction
- **Radial fountain** - Narrow at origin (1958), wide at present (2025)
- **Text on perimeter** - Labels float at outer edge for clean aesthetic

### Branch Styling

- **Thickness** = Importance (1-5 scale)
- **Opacity** = Active (0.7) vs Extinct (0.3)
- **Dashed lines** = Extinct branches
- **Colors** = Family inheritance

### Node Styling

- **Size** = Importance × multiplier
- **Color** = Family color
- **Stroke** = White outline for contrast
- **Hover** = Glow effect + tooltip

## Common Tasks

### Adjust overall tree size
Change "Vertical Spread" and "Horizontal Spread" in Foundational Layout section.

### Make tree more/less compact
- Radial: Adjust "Outer Radius" or "Vertical Spread"
- All layouts: Adjust "Node Repulsion" (higher = more spread out)

### Change time period density
Use "Timeline Ring Spacing" controls - type spacing values for each year.

### Export for publication
1. Set canvas to 6000×6000 for ultra-high resolution
2. Adjust layout until perfect
3. Export PNG (2x resolution) or SVG (vector, editable)

### Create custom color scheme
Use "Family Colors" section - click color pickers to customize all 17 families.

### Focus on specific time period
Use "Year Range" filter to show only models from specific years.

### Hide less important models
Increase "Label Threshold" to show only high-importance models (3-5).

## Keyboard Shortcuts

- **W / ↑** - Pan up
- **A / ←** - Pan left
- **S / ↓** - Pan down
- **D / →** - Pan right
- **Z** - Zoom in
- **X** - Zoom out

## Technical Constraints

### Browser Requirements
- Modern browser with ES6+ support
- D3.js v7 loaded from CDN
- Google Fonts loaded from CDN

### Performance
- 114 models renders smoothly
- Redraw on every control change (intentional for live preview)
- Heavy operations (drag, zoom) trigger full re-render

### Known Limitations
- No undo/redo (use "Reset All Settings" button)
- Custom node positions lost on layout change
- PNG export limited by canvas size (browser memory)

## Future Enhancement Ideas

- [ ] Save/load configuration presets
- [ ] Animation between layouts
- [ ] Search/highlight specific models
- [ ] Family filtering (show/hide families)
- [ ] Edge bundling for dense regions
- [ ] Minimap for navigation
- [ ] Undo/redo stack
- [ ] URL parameter encoding (shareable links)
- [ ] Dark mode

## Debugging Tips

### Tree not rendering
- Check browser console for JavaScript errors
- Verify data structure is valid JSON
- Ensure all parent IDs reference existing models

### Labels overlapping
- Increase "Horizontal Spread" or "Node Repulsion"
- Use "Extended from Perimeter" label positioning
- Increase "Label Threshold" to show fewer labels

### Weird spacing in radial mode
- Reset timeline ring spacing with "Reset to Auto" button
- Check for negative or zero spacing values
- Verify "Inner Radius" < "Outer Radius"

### Export not working
- Check browser popup blocker
- Verify canvas size isn't too large (memory limit)
- Try SVG export instead of PNG

## Code Style

- **Function naming**: camelCase (`drawNodes`, `layoutRadial`)
- **Config passing**: Pass `config` object, don't access global state
- **D3 patterns**: Use method chaining, `join()` for enter/update/exit
- **Comments**: Explain "why" not "what"
- **Modularity**: Each layout/drawing function is independent

## Important: Don't Break These

1. **Single-file architecture** - Keep everything in one HTML file
2. **Relative spacing system** - `yearRadii` stores deltas, not absolutes
3. **Event listener setup** - Call `setupEventListeners()` after DOM ready
4. **Config flow** - Always `getConfig()` → `render()` → draw functions
5. **Data immutability** - Never modify `data` object, only `nodePositions`, `yearRadii`, `familyColors`

## Questions?

This is a mature, feature-complete tool. Most changes should be:
- Adding new controls to sidebar
- Tweaking layout algorithms
- Adding new models/families to data
- Adjusting visual styling

Avoid changing the core architecture unless absolutely necessary.
