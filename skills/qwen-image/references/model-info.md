# Qwen-Image-2512 Model Information

## Architecture

Qwen-Image-2512 is a transformer-based text-to-image diffusion model developed by Alibaba Cloud (Qwen series).

### Key Features

- **Base Architecture**: Diffusion transformer (similar to SD3)
- **Text Encoder**: Qwen2.5-VL (Vision-Language)
- **VAE**: Custom Qwen VAE
- **Context Length**: 512 tokens
- **Resolution**: Up to 2048×2048 (recommended: 1328×1328)

## Model Components

### FP8 Quantized Version (Recommended)

Optimized for consumer GPUs:

| Component | File | Size | VRAM Usage |
|-----------|------|------|------------|
| VAE | `qwen_image_vae.safetensors` | ~500MB | ~1GB |
| Text Encoder | `qwen_2.5_vl_7b_fp8_scaled.safetensors` | ~7GB | ~8GB |
| Diffusion Model | `qwen_image_2512_fp8_e4m3fn.safetensors` | ~15GB | ~16GB |
| **Total** | | **~22.5GB** | **~25GB** |

### Lightning Version (Fast)

4-step generation with LoRA:

| Component | File | Size |
|-----------|------|------|
| Lightning LoRA | `Qwen-Image-Lightning-4steps-V1.0.safetensors` | ~5GB |

**Speed improvement**: ~5x faster (4 steps vs 20 steps)

### Full Precision (BF16)

For maximum quality:

| Component | File | Size | VRAM Usage |
|-----------|------|------|------------|
| Diffusion Model | `qwen_image_2512_bf16.safetensors` | ~30GB | ~32GB |

**Note**: Requires 48GB+ VRAM or model parallelism.

## Performance Benchmarks

### RTX 5090 (32GB)

| Mode | Resolution | Steps | Time | VRAM |
|------|------------|-------|------|------|
| Standard | 1024×1024 | 20 | ~25s | ~24GB |
| Standard | 1328×1328 | 20 | ~35s | ~26GB |
| Lightning | 1024×1024 | 4 | ~6s | ~24GB |
| Lightning | 1328×1328 | 4 | ~8s | ~26GB |

### Quality Comparison

- **FP8**: 98% quality of BF16 (virtually indistinguishable)
- **Lightning**: 95% quality with 5x speedup

## Technical Details

### Sampling

- **Recommended**: Euler with ModelSamplingAuraFlow
- **CFG Scale**: 4.5 (optimal for Qwen-Image)
- **Scheduler**: Normal or Karras

### Tokenization

- Max tokens: 512
- Supports: English, Chinese, multilingual
- Special tokens for style control

## Model Sources

### Official
- [Qwen/Qwen-Image-2512](https://huggingface.co/Qwen/Qwen-Image-2512) - Original model
- [QwenLM/Qwen-Image](https://github.com/QwenLM/Qwen-Image) - GitHub repository

### ComfyUI Optimized
- [Comfy-Org/Qwen-Image_ComfyUI](https://huggingface.co/Comfy-Org/Qwen-Image_ComfyUI) - FP8/BF16 splits
- [lightx2v/Qwen-Image-Lightning](https://huggingface.co/lightx2v/Qwen-Image-Lightning) - Fast generation

## Citation

```bibtex
@article{qwen-image-2512,
  title={Qwen-Image-2512: Advanced Text-to-Image Generation},
  author={Qwen Team},
  year={2025}
}
```
