# Project: Create a Phylogenetic Tree of AI Evolution (1958-2025)

## Goal
Create a beautiful, publication-quality evolutionary tree visualization of artificial intelligence models from the Perceptron (1958) to modern AGI race (2025), styled like a scientific phylogenetic tree similar to biological "Tree of Life" diagrams.

## Reference Style
I'm attaching an image of a biological evolutionary tree as a visual reference for the style, layout, and aesthetic we're aiming for. Study its:
- Radial/semicircular branching layout
- Timeline rings at the bottom
- Color-coding of major branches
- Branch thickness varying by importance/activity
- Clean labeling of terminal nodes
- Extinction event markers
- Professional scientific illustration quality

## Your Task
Experiment with multiple approaches to find the best visualization. Try at least 3-4 different methods:

### Approach 1: Python with ETE3 Toolkit
- Use ETE3 (specifically designed for phylogenetic trees)
- Create a radial/circular layout matching the reference image
- Install: `pip install ete3 PyQt5 --break-system-packages`
- Generate high-resolution SVG/PDF output

### Approach 2: Python with Matplotlib/Plotly
- Use polar coordinates for radial layout
- Custom drawing of branches, nodes, and labels
- May give more control over styling
- Libraries: matplotlib, plotly, or both

### Approach 3: Python with NetworkX + Custom Layout
- Build graph structure with NetworkX
- Implement custom radial layout algorithm
- Use matplotlib for rendering
- Good for fine-grained control

### Approach 4: D3.js (if the above don't work well)
- Create an interactive HTML visualization
- Use D3's tree layout with radial projection
- Fallback if Python approaches fail

## Data Structure to Visualize

Here's the evolutionary tree structure organized by major branches:

### ROOT (1950s-1960s): Origin of Artificial Intelligence
- **Symbolic AI Branch** (brown/tan colors)
  - Perceptron (1958) - THE ORIGIN POINT
  - ELIZA (1966)
  - Expert Systems (1970s-1980s)
  - [EXTINCTION EVENT: AI Winter 1974-1980]
  
- **Early Neural Networks Branch** (light purple)
  - Perceptron → Backpropagation (1986) ← MAJOR INNOVATION MARKER
  - Neocognitron (1980)

### THE CAMBRIAN EXPLOSION (1989-2017)

#### CNN Branch (evolving from backpropagation) - Purple/Pink
- LeNet-1 (1989) → LeNet-5 (1998)
- AlexNet (2012) ← MAJOR BREAKTHROUGH MARKER (ImageNet moment)
- VGGNet (2014)
- GoogLeNet/Inception (2014)
- ResNet (2015) ← Another major innovation
- EfficientNet (2019)
- Vision Transformer (2020) ← Convergent evolution, "re-fills CNN niche"

#### RNN Branch (from backpropagation) - Blue, MOSTLY EXTINCT by 2020
- Vanilla RNN (1990s)
- LSTM (1997) ← Major innovation
- GRU (2014)
- Seq2Seq (2014)
- [EXTINCTION EVENT: RNN Decline 2018-2020] - branch thins/fades

#### Word Embeddings Sub-branch (light blue)
- Word2Vec (2013)
- GloVe (2014)
- [Merges into Transformer branch]

#### GAN Branch (yellow-orange) - EXTINCT by 2023
- GAN (2014)
- Progressive GAN (2017)
- StyleGAN (2018)
- StyleGAN 2 (2019)
- BigGAN (2018)
- [EXTINCTION EVENT: Displaced by Diffusion Models 2022-2023]

#### Reinforcement Learning Branch (green)
- Q-Learning (1989)
- DQN (2013-2015)
- AlphaGo (2016) ← Mark as major milestone
- AlphaGo Zero (2017)
- PPO (2017)
- RLHF (2020) → connects to LLM branch

### THE TRANSFORMER REVOLUTION (2017-Present) - Iridescent/Metallic colors

#### Main Transformer Trunk (2017) ← MASSIVE RADIATION EVENT
- Attention Is All You Need (June 2017) ← CRITICAL INNOVATION

##### Encoder-Only Branch (vibrant purple)
- BERT (October 2018) ← Major split
  - RoBERTa (2019)
  - ALBERT (2019)
  - DistilBERT (2019)
  - ELECTRA (2020)
  - Domain-specific: BioBERT, SciBERT, FinBERT (2019)
  - ModernBERT (2024)

##### Decoder-Only Branch (bright blue/cyan) - DOMINANT LINEAGE
- GPT (June 2018) ← Major split
  - GPT-2 (Feb 2019)
  - GPT-3 (May 2020) ← MAJOR EXPANSION
    - GPT-3.5 (2022)
    - ChatGPT (Nov 2022) ← CULTURAL BREAKTHROUGH MARKER
    - GPT-4 (March 2023)
    - GPT-4 Turbo (Nov 2023)
    - GPT-4o (May 2024)
    - o1 series (Sept 2024) ← Reasoning breakthrough

**Anthropic Claude Branch** (splits from GPT lineage, purple-blue)
- Claude 1 (March 2023)
- Claude 2 (July 2023)
- Claude 3 family (March 2024): Haiku, Sonnet, Opus
- Claude 3.5 Sonnet (June 2024, updated Oct 2024)
- Claude 4 family (May 2025): Sonnet 4.5, Opus 4

**Google Branch** (splits from BERT/GPT, teal)
- PaLM (April 2022)
- PaLM 2 (May 2023)
- Gemini 1.0 (Dec 2023)
- Gemini 1.5 (Feb 2024)
- Gemini 2.0 (Dec 2024)
- Gemini 2.5 (March 2025)
- Gemma family: 2B/7B (Feb 2024), Gemma 2 (June 2024), Gemma 3 (March 2025)

**Meta LLaMA Branch** (splits from GPT, orange-red) - MOST INFLUENTIAL OPEN SOURCE
- LLaMA 1 (Feb 2023) → [Leak March 2023] → thousands of derivatives
- LLaMA 2 (July 2023)
- LLaMA 3 (April 2024)
- LLaMA 3.1 (July 2024)
- LLaMA 3.2 (Sept 2024)
- LLaMA 4 (April 2025)
- Code Llama (Aug 2023)

**Microsoft Phi Branch** (from GPT, silver)
- Phi-1 (June 2023)
- Phi-2 (Dec 2023)
- Phi-3 (April 2024)
- Phi-4 (2025)
- MAI-1 (2024-2025)

**Cohere Branch** (from GPT, bronze)
- Command (2023)
- Command R (March 2024)
- Command R+ (March 2024)
- Command R 08-2024 (Aug 2024)
- Command A (March 2025)

##### Encoder-Decoder Branch (green-yellow)
- T5 (Oct 2019)
- BART (Oct 2019)
- FLAN-T5 (2022)

##### Multimodal Sub-Branch (rainbow gradient)
- CLIP (Jan 2021)
- DALL-E (Jan 2021)
- Flamingo (2022)
- GPT-4V (Sept 2023)

#### Vision Transformer Branch (converging back, purple)
- ViT (Oct 2020) ← "Convergent evolution" fills CNN niche
- DeiT (2020)
- Swin Transformer (2021)
- BEiT (2021)

### DIFFUSION MODELS BRANCH (2020-Present) - Pink/Magenta, DOMINANT for images

From VAE/GAN roots:
- DDPM (2020)
- DALL-E 2 (April 2022)
- Stable Diffusion 1.x (Aug 2022) ← BREAKTHROUGH for accessibility
- Stable Diffusion 2.x (Nov 2022)
- SDXL (July 2023)
- Midjourney V1-V6 (Feb 2022 - Dec 2023)
- Stable Diffusion 3 (June 2024)
- Stable Diffusion 3.5 (Oct 2024)
- Imagen 3 (Aug 2024)
- Veo/Veo 2/Veo 3 (2024-2025)

### CHINESE AI BRANCH (2023-Present) - Red/Gold colors, EXPLOSIVE GROWTH

#### Alibaba Qwen Branch (bright red)
- Qwen/Tongyi Qianwen (April 2023)
- Qwen-2 (June 2024)
- Qwen-2.5 (Sept 2024)
- Qwen-2.5-Max (Jan 2025)
- Qwen3 (April 2025)

#### Baidu ERNIE Branch (gold)
- ERNIE 1.0/2.0 (2019)
- ERNIE 3.0 Titan (2021)
- ERNIE Bot (March 2023)
- ERNIE 4.0 (Oct 2023)
- ERNIE 4.5 (March 2025)
- ERNIE X1 (2025)

#### ByteDance Doubao Branch (orange-red)
- Doubao (May 2024)
- Doubao-1.5-Pro (Jan 2025)

#### Tencent Hunyuan Branch (dark red)
- Hunyuan-Large (Nov 2024)
- HunyuanImage 3.0 (Sept 2025)

#### Zhipu GLM Branch (crimson)
- ChatGLM-130B (March 2023)
- GLM-4 (2024)
- GLM-4.5 (July 2025)
- GLM-4.6 (Sept 2025)

#### 01.AI Yi Branch (burgundy)
- Yi (Nov 2023)
- Yi-VL (Jan 2024)
- Yi-Lightning (May 2024)

#### DeepSeek Branch (deep red) ← MAJOR DISRUPTION MARKER
- DeepSeek-Coder (Nov 2023)
- DeepSeek-V2 (May 2024)
- DeepSeek-R1 (Jan 2025) ← BREAKTHROUGH: $6M training, o1-level performance

#### Moonshot Kimi Branch (red-orange)
- Kimi (2023)
- Kimi K2 (July 2025)

#### SenseTime SenseNova Branch (amber)
- SenseNova suite (April 2023)
- SenseNova 4.0 (Feb 2024)
- SenseNova V6 (April 2025)

#### iFlytek Spark Branch (yellow-orange)
- Spark V1.0 (May 2023)
- Spark V4.0 (June 2024)
- Xinghuo X1 (April 2025)

#### MiniMax Branch (coral)
- ABAB 6.5 (April 2024)
- MiniMax-Text-01 (Jan 2025)
- MiniMax-M1 (June 2025)

### FUTURE PROJECTIONS (2025-2030+) - Glowing/ethereal colors
- AGI (2027-2030?) - show as emerging branches
- ASI variants (2030+?)
  - Embodied AI
  - Quantum-AI hybrids
  - Space-faring AI
  - Simulation creators
- Mark "The Singularity?" as major transition event

## Key Visual Elements to Include

1. **Timeline Rings**: Show years radiating from center (1950, 1960, 1970, 1980, 1990, 2000, 2010, 2015, 2020, 2025, 2030)

2. **Color Coding**:
   - Symbolic AI: Brown/tan
   - CNNs: Purple/pink
   - RNNs: Blue (fading to gray)
   - GANs: Yellow-orange (fading to gray)
   - RL: Green
   - Transformers-Encoder: Vibrant purple
   - Transformers-Decoder: Bright cyan/blue
   - Diffusion: Pink/magenta
   - Chinese models: Red/gold spectrum
   - Future: Iridescent/glowing

3. **Branch Thickness**: 
   - Thicker = currently dominant/active
   - Thinner/faded = deprecated/extinct

4. **Special Markers**:
   - ⭐ Major innovations: Backpropagation, AlexNet, ResNet, Attention mechanism, GPT-3
   - 💀 Extinction events: AI Winter, RNN Decline, GAN Displacement
   - 💥 Breakthrough moments: AlexNet ImageNet, ChatGPT launch, DeepSeek R1

5. **Labels**: 
   - Model names at branch tips
   - Dates in parentheses
   - Parameter counts for major models
   - Innovation descriptions for key nodes

6. **Legend**: Color key and explanation of visual elements

7. **Title**: "The Phylogenetic Tree of Artificial Intelligence: From Perceptrons to AGI (1958-2025)"

8. **Notes**: 
   - "All major architectures shown"
   - "Branch thickness indicates current adoption"
   - "Faded branches represent deprecated approaches"

## Technical Requirements

- **Resolution**: At least 3000x3000 pixels for print quality
- **Format**: SVG (vector) preferred, or high-res PNG/PDF
- **Aspect ratio**: Square or landscape
- **Font**: Clean sans-serif (Arial, Helvetica) or scientific serif (Times, Palatino)
- **Layout**: Radial/semicircular like the reference image
- **Exportable**: Should be easy to open in Illustrator for final touches

## Evaluation Criteria

Rate each approach on:
1. **Visual Quality**: Does it look professional and publication-ready?
2. **Readability**: Are labels clear and non-overlapping?
3. **Accuracy**: Does it correctly represent the relationships?
4. **Aesthetic**: Does it match the reference image's beauty?
5. **Extensibility**: Can it be easily updated with new models?

## Deliverables

1. Try at least 3 different visualization approaches
2. For each approach, show the result and explain pros/cons
3. Recommend the best approach with reasoning
4. Provide the final visualization file(s) in multiple formats
5. Include the complete source code for the best approach
6. Document how to update/extend the tree with new models

## Additional Context

This represents 67 years of AI evolution compressed into a single visualization. The goal is to show:
- How early approaches (symbolic AI, perceptrons) laid dormant for decades
- The slow build through CNNs/RNNs (1990s-2010s)
- The explosive Transformer revolution (2017+)
- The modern AGI race with US vs China competition (2023-2025)
- Clear lineages and derivative relationships (e.g., LLaMA spawning hundreds of variants)
- Extinction events (AI Winter, RNN decline, GAN displacement)
- Convergent evolution (ViT filling CNN niche)

The tree should tell a story: from humble beginnings to the precipice of AGI, showing both dead ends and dominant lineages.

## Start Here

Begin by exploring the ETE3 approach first, as it's most specialized for this task. Create a basic radial tree with a subset of the data to test feasibility, then expand to the full dataset. Show me the results and we'll iterate!

Good luck! Remember: the goal is publication-quality beauty combined with scientific accuracy.