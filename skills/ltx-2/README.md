# LTX-2 Video Generation Skill

This skill package provides Image-to-Video (I2V) generation capabilities using the LTX-Video 2 model with Gemma 3 text encoding.

## Overview

LTX-Video 2 is a state-of-the-art video generation model that creates smooth, high-quality videos from static images. This skill integrates with ComfyUI to provide an automated I2V pipeline.

## Model Information

- **Base Model**: LTX-Video 2 (19B parameters)
- **Text Encoder**: Gemma 3 12B IT
- **Quantization**: FP8 (for efficient inference)
- **VRAM Requirements**: ~32GB for optimal performance

## Directory Structure

```
/mnt/c/models/
├── checkpoints/
│   └── ltx-2-19b-dev-fp8.safetensors -> ../diffusion_models/ltx-2-19b-dev-fp8.safetensors
├── text_encoders/
│   └── gemma-for-ltxv.safetensors -> ../gemma-for-ltxv/model.safetensors
└── gemma-for-ltxv/
    ├── model.safetensors -> LLM/gemma-3-12b-it/model.safetensors
    ├── tokenizer.model
    ├── config.json
    ├── tokenizer.json
    ├── tokenizer_config.json
    └── preprocessor_config.json
```

## Usage

### API Workflow

The I2V workflow uses the following node structure:

1. **CheckpointLoaderSimple**: Loads the LTX-2 model
2. **LTXVGemmaCLIPModelLoader**: Loads Gemma 3 text encoder
3. **LoadImage**: Loads the input image
4. **CLIPTextEncode**: Encodes positive and negative prompts
5. **LTXVImgToVideo**: Creates video conditioning from image
6. **KSampler**: Generates video latents
7. **VAEDecode**: Decodes latents to video frames
8. **SaveAnimatedWEBP**: Saves the final video

### Example Prompts

**For the robot reading book image:**
- Positive: "A cute robot reading a book in a cozy library, gentle lighting, cinematic atmosphere, the robot slowly looks up from the book with a curious expression and smiles warmly"
- Negative: "" (empty for best results)

### Recommended Settings

- **Resolution**: 768x512 (width x height)
- **Frame Count**: 97 frames (4 seconds at 24fps)
- **Steps**: 30
- **CFG**: 3.0
- **Sampler**: euler
- **Scheduler**: normal
- **Strength**: 1.0 (full image adherence)

## Configuration

The skill is configured via ComfyUI's extra_model_paths.yaml:

```yaml
comfyui:
    base_path: /home/enric/ComfyUI/
    checkpoints: /mnt/c/models/checkpoints/
    text_encoders: /mnt/c/models/text_encoders/
```

## Files

- **Workflow**: `/home/enric/ComfyUI/user_workflows/ltxv_i2v_final.json`
- **Output**: `/home/enric/ComfyUI/output/ltxv_first_i2v_video.webp`

## Notes

- First run may take longer due to model loading
- Gemma 3 tokenizer fix was required: proper directory structure with tokenizer.model and config files
- The model supports both T2V (text-to-video) and I2V (image-to-video) modes
- WebP format provides good compression while maintaining quality

## Troubleshooting

**Issue**: "No files matching pattern 'tokenizer.model' found"
**Solution**: Ensure the gemma-for-ltxv directory has both tokenizer.model and model*.safetensors files

**Issue**: Out of memory
**Solution**: The FP8 quantized model requires ~32GB VRAM. Ensure no other GPU processes are running.

## References

- LTX-Video: https://github.com/Lightricks/LTX-Video
- ComfyUI-LTXVideo: https://github.com/Lightricks/ComfyUI-LTXVideo
- Gemma 3: https://ai.google.dev/gemma