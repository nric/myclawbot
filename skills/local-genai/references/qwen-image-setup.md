# Qwen-Image-2512 Setup Guide

## Model Information
- **Type**: Diffusers format (not single safetensors)
- **Location**: `/mnt/c/models/Qwen/Qwen-Image-2512/`
- **Size**: ~39GB total
- **Components**:
  - `transformer/` - 14GB (9 shard files)
  - `text_encoder/` - 1.6GB
  - `vae/` - ~4GB
  - `scheduler/`, `tokenizer/` - Config files

## Current Status
⚠️ **In Progress** - Downloaded but needs conversion for ComfyUI

## ComfyUI Integration

### Option 1: Using QwenImage-ComfyUI Node

The node `QwenImage-ComfyUI` is installed at `~/ComfyUI/custom_nodes/QwenImage-ComfyUI/`

**Requirements**:
- Convert model to mmgp format
- Transformer mmgp: `qwen_image_2512_transformer_mmgp.safetensors`
- Text encoder mmgp: `qwen_image_2512_text_encoder_mmgp.safetensors`

### Option 2: Direct Diffusers Pipeline

More reliable approach:

```python
from diffusers import QwenImagePipeline, QwenImageTransformer2DModel
from transformers import Qwen2_5_VLForConditionalGeneration
import torch

# Load components
transformer = QwenImageTransformer2DModel.from_pretrained(
    "/mnt/c/models/Qwen/Qwen-Image-2512/transformer",
    torch_dtype=torch.bfloat16
)

text_encoder = Qwen2_5_VLForConditionalGeneration.from_pretrained(
    "/mnt/c/models/Qwen/Qwen-Image-2512/text_encoder",
    torch_dtype=torch.bfloat16
)

# Create pipeline
pipe = QwenImagePipeline.from_pretrained(
    "/mnt/c/models/Qwen/Qwen-Image-2512",
    transformer=transformer,
    text_encoder=text_encoder,
    torch_dtype=torch.bfloat16
)
pipe.to("cuda")

# Generate
image = pipe(
    "A serene Japanese garden with cherry blossoms",
    num_inference_steps=20,
    guidance_scale=4.5
).images[0]
```

## Features

- Enhanced human realism (reduces "AI-generated" look)
- Finer natural detail (landscapes, animal fur)
- Text-in-image capabilities
- Improved December 2025 version

## Model Card
- **Base**: Qwen-Image architecture
- **Training**: Large-scale image-text pairs
- **Resolution**: Up to 1024x1024
- **License**: Apache 2.0

## Resources

- HuggingFace: https://huggingface.co/Qwen/Qwen-Image-2512
- Demo: https://chat.qwen.ai/
- Paper: https://qianwen-res.oss-cn-beijing.aliyuncs.com/Qwen-Image/Qwen_Image.pdf
