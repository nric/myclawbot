---
name: local-genai
description: Local image and video generation using ComfyUI with Z-Image, Qwen-Image, LTX-Video, and Flux models. Use when the user wants to generate images or videos locally without API costs, or when working with the local ComfyUI setup at ~/ComfyUI with models in /mnt/c/models/. Handles model management, workflow execution, and troubleshooting for RTX 5090 CUDA compatibility.
---

# Local Generative AI (ComfyUI)

This skill provides workflows for local image and video generation using ComfyUI with state-of-the-art open source models.

## Quick Start

### Available Models

| Model | Type | Location | Size | Status |
|-------|------|----------|------|--------|
| Flux 1 Dev | Image | `/mnt/c/models/checkpoints/` | 17GB | ✅ Fully working |
| Z-Image Turbo | Image | `/mnt/c/models/diffusion_models/` | 12GB | ⚠️ Needs custom workflow |
| Qwen-Image-2512 | Image | `/mnt/c/models/Qwen/Qwen-Image-2512/` | 39GB | ⚠️ Needs conversion |
| LTX-Video 2B | Video | `/mnt/c/models/diffusion_models/` | 5.4GB | ⚠️ Needs custom workflow |

### ComfyUI Setup

```bash
# Start ComfyUI
cd ~/ComfyUI
source venv/bin/activate
python main.py --listen 127.0.0.1 --port 8188

# API available at http://127.0.0.1:8188
```

### Model Paths Configuration

Configured in `~/ComfyUI/extra_model_paths.yaml`:
- Checkpoints: `/mnt/c/models/checkpoints/`
- Diffusion models: `/mnt/c/models/diffusion_models/`
- CLIP: `/mnt/c/models/clip/`
- VAE: `/mnt/c/models/vae/`

## Workflows

### 1. Flux Image Generation (Working)

Most reliable for immediate results. See [references/flux-workflow.md](references/flux-workflow.md).

### 2. Z-Image (Experimental)

Requires specific text encoder. See [references/z-image-setup.md](references/z-image-setup.md).

### 3. Qwen-Image-2512 (In Progress)

Diffusers format model needs conversion or direct pipeline usage. See [references/qwen-image-setup.md](references/qwen-image-setup.md).

### 4. LTX-Video (Experimental)

Text-to-video generation. See [references/ltx-video-setup.md](references/ltx-video-setup.md).

## System Requirements

- **GPU**: NVIDIA RTX 5090 (32GB VRAM)
- **CUDA**: 12.8+
- **PyTorch**: 2.11.0.dev20260203+cu128 (installed in venv)
- **Storage**: 100GB+ for models

## Troubleshooting

### CUDA Errors

If you see `CUDA error: no kernel image is available`:
```bash
cd ~/ComfyUI
source venv/bin/activate
pip install --pre torch torchvision torchaudio --index-url https://download.pytorch.org/whl/nightly/cu128 --force-reinstall
```

### Model Loading Issues

Check available models via API:
```bash
curl -s http://127.0.0.1:8188/object_info | python3 -c "import sys,json; d=json.load(sys.stdin); print(json.dumps(list(d.keys())[:20], indent=2))"
```

## Scripts

- `scripts/generate_image.py` - Direct image generation
- `scripts/check_system.py` - Verify setup and models

## Resources

- [references/flux-workflow.md](references/flux-workflow.md) - Flux generation guide
- [references/z-image-setup.md](references/z-image-setup.md) - Z-Image configuration
- [references/qwen-image-setup.md](references/qwen-image-setup.md) - Qwen-Image setup
- [references/ltx-video-setup.md](references/ltx-video-setup.md) - LTX-Video workflow
- [references/api-examples.md](references/api-examples.md) - ComfyUI API examples
