---
name: qwen-image
description: Generate high-quality images using Qwen-Image-2512 model locally via ComfyUI. Optimized for RTX 5090 with FP8 quantized models for efficient VRAM usage. Supports both standard and lightning (4-step) generation modes. Use when the user wants to create detailed, photorealistic images with excellent text rendering capabilities.
---

# Qwen-Image-2512 Local Generation

This skill provides workflows for generating high-quality images using Alibaba's Qwen-Image-2512 model through ComfyUI.

## Features

- **High Quality**: State-of-the-art text-to-image generation
- **Text Rendering**: Excellent at rendering text within images
- **FP8 Optimized**: Quantized models for efficient VRAM usage (~23GB total)
- **Fast Mode**: Lightning variant for 4-step generation
- **Multiple Aspect Ratios**: 1:1, 16:9, 9:16, 4:3, 3:4, 3:2, 2:3

## Quick Start

### Prerequisites

Models are automatically managed in `/mnt/c/models/`:

| Component | File | Size | Location |
|-----------|------|------|----------|
| VAE | `qwen_image_vae.safetensors` | ~500MB | `models/vae/` |
| Text Encoder | `qwen_2.5_vl_7b_fp8_scaled.safetensors` | ~7GB | `models/text_encoders/` |
| Diffusion Model | `qwen_image_2512_fp8_e4m3fn.safetensors` | ~15GB | `models/diffusion_models/` |
| Lightning LoRA (opt.) | `Qwen-Image-Lightning-4steps-V1.0.safetensors` | ~5GB | `models/loras/` |

### Usage

#### Option 1: ComfyUI Web Interface

1. Start ComfyUI: `cd ~/ComfyUI && python main.py`
2. Load workflow: Drag `assets/qwen_image_2512.json` into ComfyUI
3. Enter prompt and click "Queue Prompt"

#### Option 2: Command Line Script

```bash
cd ~/ComfyUI
source venv/bin/activate
python scripts/generate_qwen.py "your prompt here" --width 1024 --height 1024
```

#### Option 3: Python API

```python
from scripts.generate_qwen import generate_image

image = generate_image(
    prompt="A majestic dragon soaring through clouds",
    width=1328,
    height=1328,
    steps=20,
    use_lightning=False
)
```

## Recommended Settings

| Setting | Value | Notes |
|---------|-------|-------|
| Resolution | 1328x1328 (1:1) | Native resolution |
| Steps | 20-30 | Standard quality |
| Lightning Steps | 4 | Fast mode with LoRA |
| CFG Scale | 4.5 | Guidance scale |
| Sampler | euler | Reliable choice |

## Aspect Ratios

| Ratio | Resolution | Use Case |
|-------|------------|----------|
| 1:1 | 1328×1328 | Square images, portraits |
| 16:9 | 1664×928 | Landscapes, wallpapers |
| 9:16 | 928×1664 | Mobile wallpapers, tall portraits |
| 4:3 | 1472×1104 | Standard photos |
| 3:4 | 1104×1472 | Portraits |
| 3:2 | 1584×1056 | DSLR-style photos |
| 2:3 | 1056×1584 | Portrait orientation |

## Prompting Tips

Qwen-Image responds well to detailed prompts:

- **Style descriptors**: "photorealistic", "cinematic", "oil painting", "watercolor"
- **Lighting**: "golden hour", "dramatic lighting", "soft diffused light"
- **Camera**: "wide angle", "portrait lens", "aerial view", "macro"
- **Quality tags**: "highly detailed", "8k", "masterpiece"

### Example Prompts

```
Urban alleyway at dusk. High-fashion model striding elegantly, 
rose-gold metallic trench coat, cinematic lighting, photorealistic, 8k
```

```
A serene Japanese garden in spring, cherry blossoms falling, 
koi pond, sunlight filtering through trees, peaceful atmosphere
```

## Troubleshooting

### CUDA Out of Memory

- Use FP8 models (automatically configured)
- Reduce resolution
- Close other GPU applications

### Model Not Found

Run `scripts/check_qwen_models.py` to verify all models are present.

### Slow Generation

- Enable Lightning mode for 4-step generation
- Ensure models are on SSD/NVMe

## Resources

- [ComfyUI Workflow](assets/qwen_image_2512.json) - Ready-to-use workflow
- [Model Details](references/model-info.md) - Technical specifications
- [Prompt Guide](references/prompting.md) - Advanced prompting techniques

## Links

- [Qwen-Image HuggingFace](https://huggingface.co/Qwen/Qwen-Image-2512)
- [Comfy-Org Models](https://huggingface.co/Comfy-Org/Qwen-Image_ComfyUI)
- [Lightning LoRA](https://huggingface.co/lightx2v/Qwen-Image-Lightning)
