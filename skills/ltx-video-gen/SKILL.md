---
name: ltx-video-gen
description: Generate high-quality videos using LTX-2 19B model via ComfyUI. Supports text-to-video generation with integrated audio. Use when the user wants to create AI-generated videos, especially for creative content, animations, or cinematic shots. Optimized for RTX 5090 with FP8 quantization.
---

# LTX-2 Video Generation

Generate high-quality videos using the LTX-2 19B model with integrated audio generation.

## System Requirements

- **GPU:** RTX 5090 (or equivalent VRAM)
- **Environment:** `comfy_5090` conda environment
- **Server:** ComfyUI running on port 8188

## Quick Start

```bash
# Basic 720p video (10 seconds @ 24fps = 241 frames)
/home/enric/ComfyUI/ltx.py t2v "Your prompt here" --resolution 720p --length 241

# Faster 360p generation
/home/enric/ComfyUI/ltx.py t2v "Your prompt" --resolution 360p --length 121 --steps 15
```

## CLI Parameters

| Parameter | Description | Default |
|-----------|-------------|---------|
| `prompt` | Text description of the video | Required |
| `--output` | Output filename prefix | `ltx_t2v` |
| `--resolution` | Preset: `720p`, `540p`, `360p` | None |
| `--width` / `--height` | Custom dimensions | Ignored if `--resolution` set |
| `--length` | Number of frames (24fps) | `121` (~5s) |
| `--steps` | Sampling steps | `25` |
| `--cfg` | CFG scale | `4.0` |
| `--seed` | Manual seed | Random |

## Model Configuration

- **Checkpoint:** `checkpoints/ltx-2-19b-dev-fp8.safetensors`
- **Text Encoder:** `text_encoders/gemma_3_12B_it_fp4_mixed.safetensors` (4-bit, CPU)
- **LoRA:** `loras/ltx-2-19b-distilled-lora-384.safetensors`
- **Upscaler:** `latent_upscale_models/ltx-2-spatial-upscaler-x2-1.0.safetensors`

## Important: Resource Management

After generation, ALWAYS clean up to free VRAM/RAM:

```bash
# Stop ComfyUI server completely
pkill -f "python main.py"

# Verify resources freed
nvidia-smi
free -h
```

## Monitoring Generation Progress

Check progress every 60 seconds:

```bash
# Watch logs
tail -f /tmp/ltx_job.log

# Check GPU usage
watch -n 5 nvidia-smi

# Check if process running
ps aux | grep ltx.py | grep -v grep
```

## Troubleshooting

- **Port 8188 in use:** Run `pkill -f "python main.py"` to stop existing server
- **VRAM OOM:** Lower resolution to 360p or reduce frame count
- **Model not found:** Check `/mnt/c/models` mount and `extra_model_paths.yaml`
- **Stuck/hanging:** Check `nvidia-smi` - if GPU idle but process running, restart

## Script Helper

Use `scripts/generate.py` for simplified batch generation with automatic output handling and cleanup.

```bash
python scripts/generate.py "Prompt" --output name --length 241 --cleanup
```
