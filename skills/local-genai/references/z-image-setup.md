# Z-Image Setup Guide

## Model Information
- **File**: `z_image_turbo_bf16.safetensors` (12GB)
- **Location**: `/mnt/c/models/diffusion_models/`
- **Architecture**: Custom transformer-based (not SD/Flux)

## Current Status
⚠️ **Experimental** - Requires specific text encoder configuration

## Known Issues

### Shape Mismatch Error
```
Given normalized_shape=[2560], expected input with shape [*2560], but got input of size[2, 77, 768]
```

This indicates Z-Image expects a different CLIP/text encoder dimension than standard CLIP_L (768).

## Required Setup

### Text Encoder
Z-Image likely requires one of:
1. `qwen_3_4b.safetensors` (available in `/mnt/c/models/text_encoders/`)
2. Custom text encoder with 2560-dimensional output

### Recommended Workflow

Instead of standard CLIP encoding, try:

```json
{
  "2": {
    "inputs": {
      "clip_name": "qwen_3_4b.safetensors",
      "type": "qwen_image"
    },
    "class_type": "CLIPLoader"
  }
}
```

## Alternative: Direct Diffusers Usage

If ComfyUI workflow fails, use directly:

```python
from diffusers import DiffusionPipeline
import torch

pipe = DiffusionPipeline.from_pretrained(
    "/mnt/c/models/diffusion_models/z_image_turbo_bf16.safetensors",
    torch_dtype=torch.bfloat16
)
pipe.to("cuda")

image = pipe("your prompt here").images[0]
```

## Resources

- Model metadata inspection shows `cap_embedder` and `context_refiner` layers
- Not compatible with standard SD/SDXL/Flux workflows
- May require custom ComfyUI node

## Next Steps

1. Test with `qwen_3_4b` text encoder
2. If that fails, create custom pipeline using diffusers
3. Consider using Z-Image via Python script instead of ComfyUI
