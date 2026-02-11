# Flux Image Generation Workflow

## Overview
Flux 1 Dev (fp8) is the most reliable model currently available for local image generation.

## Model Location
- **Checkpoint**: `/mnt/c/models/checkpoints/flux1-dev-fp8.safetensors` (17GB)
- **CLIP**: Uses `clip_l.safetensors` from `/mnt/c/models/clip/`
- **VAE**: Uses `ae.safetensors` from `/mnt/c/models/vae/`

## API Workflow

```json
{
  "prompt": {
    "1": {
      "inputs": {
        "ckpt_name": "flux1-dev-fp8.safetensors"
      },
      "class_type": "CheckpointLoaderSimple"
    },
    "2": {
      "inputs": {
        "text": "YOUR_PROMPT_HERE",
        "clip": ["1", 1]
      },
      "class_type": "CLIPTextEncode"
    },
    "3": {
      "inputs": {
        "text": "blurry, low quality, distorted",
        "clip": ["1", 1]
      },
      "class_type": "CLIPTextEncode"
    },
    "4": {
      "inputs": {
        "width": 1024,
        "height": 1024,
        "batch_size": 1
      },
      "class_type": "EmptyLatentImage"
    },
    "5": {
      "inputs": {
        "seed": 42,
        "steps": 20,
        "cfg": 1.0,
        "sampler_name": "euler",
        "scheduler": "normal",
        "denoise": 1,
        "model": ["1", 0],
        "positive": ["2", 0],
        "negative": ["3", 0],
        "latent_image": ["4", 0]
      },
      "class_type": "KSampler"
    },
    "6": {
      "inputs": {
        "samples": ["5", 0],
        "vae": ["1", 2]
      },
      "class_type": "VAEDecode"
    },
    "7": {
      "inputs": {
        "filename_prefix": "flux_output",
        "images": ["6", 0]
      },
      "class_type": "SaveImage"
    }
  }
}
```

## Usage

1. Start ComfyUI
2. Send POST request to `http://127.0.0.1:8188/prompt`
3. Check history at `http://127.0.0.1:8188/history/{prompt_id}`
4. Find outputs in `~/ComfyUI/output/`

## Recommended Settings

| Parameter | Value | Notes |
|-----------|-------|-------|
| Steps | 20-30 | Higher = better quality, slower |
| CFG | 1.0-3.5 | Flux works well with low CFG |
| Resolution | 1024x1024 | Native resolution |
| Sampler | euler | Reliable choice |

## Creative Prompt Examples

### Fantasy
```
A luminous bioluminescent forest at midnight, ethereal glowing mushrooms and plants casting soft blue and purple light, crystal clear stream, fireflies dancing in the mist, highly detailed, 8k quality
```

### Portrait
```
Professional portrait of a wise elderly scientist in a modern laboratory, warm lighting reflecting off glass equipment, bokeh background, photorealistic, cinematic composition
```

### Abstract
```
Abstract geometric patterns flowing like liquid mercury, iridescent colors shifting between gold and purple, dark background, sharp focus, high contrast
```
