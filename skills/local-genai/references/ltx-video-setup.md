# LTX-Video Setup Guide

## Model Information
- **File**: `ltx-video-2b-v0.9.1.safetensors` (5.4GB)
- **Location**: `/mnt/c/models/diffusion_models/`
- **Type**: DiT-based video generation
- **Capabilities**: Real-time 30 FPS at 1216×704

## Current Status
⚠️ **Experimental** - Model loaded, workflow needs refinement

## ComfyUI Nodes

Custom nodes installed at `~/ComfyUI/custom_nodes/ComfyUI-LTXVideo/`

### Available Nodes
- `LTXVConditioning` - Prepare conditioning for video
- `EmptyLTXVLatentVideo` - Create video latent space
- `LTXVScheduler` - Video-specific scheduling
- `ModelSamplingLTXV` - LTX-specific sampling

### Example Workflows

Full workflows available in:
`~/ComfyUI/custom_nodes/ComfyUI-LTXVideo/example_workflows/`

Key files:
- `LTX-2_T2V_Full_wLora.json` - Text to video (full)
- `LTX-2_T2V_Distilled_wLora.json` - Faster distilled version
- `LTX-2_I2V_Full_wLora.json` - Image to video

## Basic API Structure

```json
{
  "prompt": {
    "1": {
      "inputs": {"unet_name": "ltx-video-2b-v0.9.1.safetensors"},
      "class_type": "UNETLoader"
    },
    "2": {
      "inputs": {"clip_name": "clip_l.safetensors", "type": "ltxv"},
      "class_type": "CLIPLoader"
    },
    "latent": {
      "inputs": {"width": 768, "height": 512, "length": 25, "batch_size": 1},
      "class_type": "EmptyLTXVLatentVideo"
    },
    "conditioning": {
      "inputs": {
        "positive": [...],
        "negative": [...],
        "frame_rate": 25
      },
      "class_type": "LTXVConditioning"
    }
  }
}
```

## Parameters

| Parameter | Range | Default | Notes |
|-----------|-------|---------|-------|
| Width | 64-16384 | 768 | Must be divisible by 32 |
| Height | 64-16384 | 512 | Must be divisible by 32 |
| Length | 1-16384 | 97 | Frames (divisible by 8) |
| Frame Rate | 0-1000 | 25 | FPS |
| Steps | 1-100 | 30 | Denoising steps |
| CFG | 0-100 | 3.0 | Guidance scale |

## Prompt Examples

### Nature Scene
```
A serene Japanese garden in spring, cherry blossoms gently falling, 
a small koi pond with colorful fish swimming, sunlight filtering 
through the trees creating dappled light, peaceful atmosphere
```

### Urban Scene
```
A bustling city street at night, neon lights reflecting on wet pavement,
traffic flowing smoothly, pedestrians with umbrellas, cinematic shot
```

## Output

- Format: Video file (MP4/WebM)
- Location: `~/ComfyUI/output/`
- Frames: As specified in `length` parameter
- Duration: `length / frame_rate` seconds

## Known Issues

- Requires specific attention_mask handling
- Best results with example workflows from repo
- May need specific sampler configuration

## Resources

- Model: https://huggingface.co/Lightricks/LTX-Video
- GitHub: https://github.com/Lightricks/LTX-Video
- ComfyUI Nodes: https://github.com/Lightricks/ComfyUI-LTXVideo
