"""
Complete AI Evolution Dataset
All major AI models from 1958-2025 with relationships
"""

# Format: (name, parent, year, color, importance, branch_type, extinct)
AI_MODELS = [
    # ROOT
    ("Perceptron", None, 1958, '#2F4F4F', 5, 'root', False),

    # SYMBOLIC AI BRANCH - Brown/tan (mostly extinct)
    ("Symbolic AI", "Perceptron", 1960, '#8B7355', 3, 'symbolic', True),
    ("ELIZA", "Symbolic AI", 1966, '#8B7355', 2, 'symbolic', True),
    ("Expert Systems", "Symbolic AI", 1975, '#8B7355', 2, 'symbolic', True),

    # EARLY NEURAL NETWORKS
    ("Backpropagation", "Perceptron", 1986, '#FF6347', 5, 'innovation', False),
    ("Neocognitron", "Perceptron", 1980, '#DDA0DD', 2, 'cnn', True),

    # CNN BRANCH - Purple/pink
    ("CNNs", "Backpropagation", 1989, '#9370DB', 4, 'cnn', False),
    ("LeNet-1", "CNNs", 1989, '#9370DB', 2, 'cnn', False),
    ("LeNet-5", "LeNet-1", 1998, '#9370DB', 3, 'cnn', False),
    ("AlexNet", "LeNet-5", 2012, '#9370DB', 5, 'cnn', False),
    ("VGGNet", "AlexNet", 2014, '#9370DB', 3, 'cnn', False),
    ("GoogLeNet", "AlexNet", 2014, '#9370DB', 3, 'cnn', False),
    ("ResNet", "AlexNet", 2015, '#9370DB', 5, 'cnn', False),
    ("EfficientNet", "ResNet", 2019, '#9370DB', 3, 'cnn', False),

    # RNN BRANCH - Blue (mostly extinct)
    ("RNNs", "Backpropagation", 1990, '#4169E1', 3, 'rnn', True),
    ("LSTM", "RNNs", 1997, '#4169E1', 4, 'rnn', True),
    ("GRU", "LSTM", 2014, '#4169E1', 2, 'rnn', True),
    ("Seq2Seq", "LSTM", 2014, '#4169E1', 3, 'rnn', True),

    # Word Embeddings
    ("Word2Vec", "RNNs", 2013, '#87CEEB', 3, 'embedding', False),
    ("GloVe", "Word2Vec", 2014, '#87CEEB', 2, 'embedding', False),

    # GAN BRANCH - Yellow-orange (extinct)
    ("GANs", "Backpropagation", 2014, '#FFA500', 4, 'gan', True),
    ("Progressive GAN", "GANs", 2017, '#FFA500', 2, 'gan', True),
    ("StyleGAN", "Progressive GAN", 2018, '#FFA500', 3, 'gan', True),
    ("StyleGAN2", "StyleGAN", 2019, '#FFA500', 3, 'gan', True),
    ("BigGAN", "GANs", 2018, '#FFA500', 2, 'gan', True),

    # RL BRANCH - Green
    ("Q-Learning", "Perceptron", 1989, '#228B22', 3, 'rl', False),
    ("DQN", "Q-Learning", 2013, '#228B22', 3, 'rl', False),
    ("AlphaGo", "DQN", 2016, '#228B22', 5, 'rl', False),
    ("AlphaGo Zero", "AlphaGo", 2017, '#228B22', 4, 'rl', False),
    ("PPO", "DQN", 2017, '#228B22', 3, 'rl', False),
    ("RLHF", "PPO", 2020, '#228B22', 4, 'rl', False),

    # TRANSFORMER REVOLUTION - 2017
    ("Transformers", "Backpropagation", 2017, '#00CED1', 5, 'transformer', False),

    # Encoder-Only Branch - Vibrant purple
    ("BERT", "Transformers", 2018, '#8B008B', 5, 'encoder', False),
    ("RoBERTa", "BERT", 2019, '#8B008B', 3, 'encoder', False),
    ("ALBERT", "BERT", 2019, '#8B008B', 2, 'encoder', False),
    ("DistilBERT", "BERT", 2019, '#8B008B', 2, 'encoder', False),
    ("ELECTRA", "BERT", 2020, '#8B008B', 2, 'encoder', False),
    ("ModernBERT", "BERT", 2024, '#8B008B', 2, 'encoder', False),

    # Decoder-Only Branch - Bright blue/cyan (DOMINANT)
    ("GPT", "Transformers", 2018, '#00BFFF', 4, 'decoder', False),
    ("GPT-2", "GPT", 2019, '#00BFFF', 4, 'decoder', False),
    ("GPT-3", "GPT-2", 2020, '#00BFFF', 5, 'decoder', False),
    ("GPT-3.5", "GPT-3", 2022, '#00BFFF', 4, 'decoder', False),
    ("ChatGPT", "GPT-3.5", 2022, '#00BFFF', 5, 'decoder', False),
    ("GPT-4", "ChatGPT", 2023, '#00BFFF', 5, 'decoder', False),
    ("GPT-4 Turbo", "GPT-4", 2023, '#00BFFF', 3, 'decoder', False),
    ("GPT-4o", "GPT-4 Turbo", 2024, '#00BFFF', 4, 'decoder', False),
    ("o1", "GPT-4o", 2024, '#00BFFF', 5, 'decoder', False),

    # Anthropic Claude Branch - Purple-blue
    ("Claude", "Transformers", 2023, '#7B68EE', 4, 'claude', False),
    ("Claude 2", "Claude", 2023, '#7B68EE', 3, 'claude', False),
    ("Claude 3 Haiku", "Claude 2", 2024, '#7B68EE', 3, 'claude', False),
    ("Claude 3 Sonnet", "Claude 2", 2024, '#7B68EE', 4, 'claude', False),
    ("Claude 3 Opus", "Claude 2", 2024, '#7B68EE', 4, 'claude', False),
    ("Claude 3.5 Sonnet", "Claude 3 Sonnet", 2024, '#7B68EE', 5, 'claude', False),
    ("Claude 4 Sonnet", "Claude 3.5 Sonnet", 2025, '#7B68EE', 5, 'claude', False),

    # Google Branch - Teal
    ("PaLM", "Transformers", 2022, '#008B8B', 4, 'google', False),
    ("PaLM 2", "PaLM", 2023, '#008B8B', 4, 'google', False),
    ("Gemini 1.0", "PaLM 2", 2023, '#008B8B', 4, 'google', False),
    ("Gemini 1.5", "Gemini 1.0", 2024, '#008B8B', 4, 'google', False),
    ("Gemini 2.0", "Gemini 1.5", 2024, '#008B8B', 4, 'google', False),
    ("Gemini 2.5", "Gemini 2.0", 2025, '#008B8B', 4, 'google', False),
    ("Gemma", "PaLM", 2024, '#20B2AA', 3, 'google', False),
    ("Gemma 2", "Gemma", 2024, '#20B2AA', 3, 'google', False),

    # Meta LLaMA Branch - Orange-red (MOST INFLUENTIAL OPEN SOURCE)
    ("LLaMA", "Transformers", 2023, '#FF4500', 5, 'llama', False),
    ("LLaMA 2", "LLaMA", 2023, '#FF4500', 4, 'llama', False),
    ("LLaMA 3", "LLaMA 2", 2024, '#FF4500', 5, 'llama', False),
    ("LLaMA 3.1", "LLaMA 3", 2024, '#FF4500', 4, 'llama', False),
    ("LLaMA 3.2", "LLaMA 3.1", 2024, '#FF4500', 3, 'llama', False),
    ("LLaMA 4", "LLaMA 3.2", 2025, '#FF4500', 4, 'llama', False),
    ("Code Llama", "LLaMA", 2023, '#FF6347', 3, 'llama', False),

    # Microsoft Phi Branch - Silver
    ("Phi-1", "Transformers", 2023, '#C0C0C0', 2, 'microsoft', False),
    ("Phi-2", "Phi-1", 2023, '#C0C0C0', 3, 'microsoft', False),
    ("Phi-3", "Phi-2", 2024, '#C0C0C0', 3, 'microsoft', False),
    ("Phi-4", "Phi-3", 2025, '#C0C0C0', 3, 'microsoft', False),

    # Cohere Branch - Bronze
    ("Command", "Transformers", 2023, '#CD7F32', 3, 'cohere', False),
    ("Command R", "Command", 2024, '#CD7F32', 3, 'cohere', False),
    ("Command R+", "Command R", 2024, '#CD7F32', 3, 'cohere', False),

    # Encoder-Decoder Branch - Green-yellow
    ("T5", "Transformers", 2019, '#9ACD32', 4, 'enc-dec', False),
    ("BART", "Transformers", 2019, '#9ACD32', 3, 'enc-dec', False),
    ("FLAN-T5", "T5", 2022, '#9ACD32', 3, 'enc-dec', False),

    # Multimodal - Rainbow gradient
    ("CLIP", "Transformers", 2021, '#DA70D6', 4, 'multimodal', False),
    ("DALL-E", "CLIP", 2021, '#DA70D6', 4, 'multimodal', False),
    ("Flamingo", "CLIP", 2022, '#DA70D6', 3, 'multimodal', False),
    ("GPT-4V", "GPT-4", 2023, '#DA70D6', 4, 'multimodal', False),

    # Vision Transformer - Convergent evolution
    ("ViT", "Transformers", 2020, '#BA55D3', 4, 'vit', False),
    ("DeiT", "ViT", 2020, '#BA55D3', 2, 'vit', False),
    ("Swin Transformer", "ViT", 2021, '#BA55D3', 3, 'vit', False),
    ("BEiT", "ViT", 2021, '#BA55D3', 2, 'vit', False),

    # DIFFUSION MODELS - Pink/Magenta (DOMINANT for images)
    ("DDPM", "Backpropagation", 2020, '#FF1493', 4, 'diffusion', False),
    ("DALL-E 2", "DDPM", 2022, '#FF1493', 5, 'diffusion', False),
    ("Stable Diffusion", "DDPM", 2022, '#FF1493', 5, 'diffusion', False),
    ("SD 2.x", "Stable Diffusion", 2022, '#FF1493', 3, 'diffusion', False),
    ("SDXL", "SD 2.x", 2023, '#FF1493', 4, 'diffusion', False),
    ("Midjourney", "DDPM", 2022, '#FF69B4', 5, 'diffusion', False),
    ("SD 3", "SDXL", 2024, '#FF1493', 4, 'diffusion', False),
    ("SD 3.5", "SD 3", 2024, '#FF1493', 3, 'diffusion', False),
    ("Imagen 3", "DDPM", 2024, '#FF1493', 3, 'diffusion', False),

    # CHINESE AI BRANCH - Red/Gold (EXPLOSIVE GROWTH)
    # Alibaba Qwen
    ("Qwen", "Transformers", 2023, '#DC143C', 4, 'chinese', False),
    ("Qwen-2", "Qwen", 2024, '#DC143C', 4, 'chinese', False),
    ("Qwen-2.5", "Qwen-2", 2024, '#DC143C', 4, 'chinese', False),
    ("Qwen-2.5-Max", "Qwen-2.5", 2025, '#DC143C', 4, 'chinese', False),

    # Baidu ERNIE
    ("ERNIE", "Transformers", 2019, '#FFD700', 3, 'chinese', False),
    ("ERNIE 3.0", "ERNIE", 2021, '#FFD700', 3, 'chinese', False),
    ("ERNIE Bot", "ERNIE 3.0", 2023, '#FFD700', 3, 'chinese', False),
    ("ERNIE 4.0", "ERNIE Bot", 2023, '#FFD700', 3, 'chinese', False),

    # ByteDance Doubao
    ("Doubao", "Transformers", 2024, '#FF8C00', 3, 'chinese', False),
    ("Doubao-1.5-Pro", "Doubao", 2025, '#FF8C00', 3, 'chinese', False),

    # Zhipu GLM
    ("ChatGLM", "Transformers", 2023, '#B22222', 3, 'chinese', False),
    ("GLM-4", "ChatGLM", 2024, '#B22222', 3, 'chinese', False),

    # 01.AI Yi
    ("Yi", "Transformers", 2023, '#8B0000', 3, 'chinese', False),
    ("Yi-VL", "Yi", 2024, '#8B0000', 3, 'chinese', False),

    # DeepSeek - MAJOR DISRUPTION
    ("DeepSeek", "Transformers", 2023, '#800000', 4, 'chinese', False),
    ("DeepSeek-V2", "DeepSeek", 2024, '#800000', 4, 'chinese', False),
    ("DeepSeek-R1", "DeepSeek-V2", 2025, '#800000', 5, 'chinese', False),

    # Moonshot Kimi
    ("Kimi", "Transformers", 2023, '#CD5C5C', 3, 'chinese', False),
]

# Color scheme reference
COLOR_SCHEME = {
    'root': '#2F4F4F',  # Dark slate gray
    'symbolic': '#8B7355',  # Brown/tan
    'innovation': '#FF6347',  # Tomato
    'cnn': '#9370DB',  # Purple
    'rnn': '#4169E1',  # Blue
    'embedding': '#87CEEB',  # Sky blue
    'gan': '#FFA500',  # Orange
    'rl': '#228B22',  # Forest green
    'transformer': '#00CED1',  # Dark turquoise
    'encoder': '#8B008B',  # Dark magenta
    'decoder': '#00BFFF',  # Deep sky blue
    'claude': '#7B68EE',  # Medium slate blue
    'google': '#008B8B',  # Dark cyan
    'llama': '#FF4500',  # Orange-red
    'microsoft': '#C0C0C0',  # Silver
    'cohere': '#CD7F32',  # Bronze
    'enc-dec': '#9ACD32',  # Yellow green
    'multimodal': '#DA70D6',  # Orchid
    'vit': '#BA55D3',  # Medium orchid
    'diffusion': '#FF1493',  # Deep pink
    'chinese': '#DC143C',  # Crimson
}

# Extinction events
EXTINCTION_EVENTS = [
    ("AI Winter", 1974, 1980),
    ("RNN Decline", 2018, 2020),
    ("GAN Displacement", 2022, 2023),
]

# Major breakthroughs
BREAKTHROUGHS = [
    ("Backpropagation", 1986, "⭐"),
    ("AlexNet", 2012, "💥"),
    ("ResNet", 2015, "⭐"),
    ("Transformers", 2017, "💥"),
    ("GPT-3", 2020, "⭐"),
    ("ChatGPT", 2022, "💥"),
    ("DeepSeek-R1", 2025, "💥"),
]
