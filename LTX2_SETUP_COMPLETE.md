# LTX-2 I2V Setup - Completion Report

Date: 2026-02-04
Status: ✅ COMPLETE

## Summary

Successfully debugged and fixed the LTX-2 Image-to-Video (I2V) setup, generated the first video, and delivered it to the user via WhatsApp.

## Issues Fixed

### 1. Gemma Tokenizer Path Issue (RESOLVED)

**Problem**: 
```
FileNotFoundError: No files matching pattern 'tokenizer.model' found under /mnt/c/models
```

**Root Cause**: 
The ComfyUI-LTXVideo plugin expected a specific directory structure:
- `path = Path(folder_paths.get_full_path("text_encoders", gemma_path))`
- `model_root = path.parents[1]`
- Search for tokenizer.model under model_root

**Solution**: 
Created a properly structured directory at `/mnt/c/models/gemma-for-ltxv/`:
```
gemma-for-ltxv/
├── model.safetensors -> /mnt/c/models/LLM/gemma-3-12b-it/model.safetensors
├── tokenizer.model -> /mnt/c/models/tokenizer.model
├── config.json (downloaded from unsloth/gemma-3-12b-it)
├── tokenizer.json (downloaded from unsloth/gemma-3-12b-it)
├── tokenizer_config.json (downloaded from unsloth/gemma-3-12b-it)
└── preprocessor_config.json (downloaded from unsloth/gemma-3-12b-it)
```

Created symlink in text_encoders:
```
/mnt/c/models/text_encoders/gemma-for-ltxv.safetensors -> /mnt/c/models/gemma-for-ltxv/model.safetensors
```

## Video Generation

### Input Image
- File: `/home/enric/ComfyUI/output/qwen_image_00002_.png`
- Description: Cute robot reading "How to make Humans Happy" book in a library

### Generation Parameters
- **Model**: LTX-Video 2 19B (FP8 quantized)
- **Text Encoder**: Gemma 3 12B IT
- **Prompt**: "A cute robot reading a book in a cozy library, gentle lighting, cinematic atmosphere, the robot slowly looks up from the book with a curious expression and smiles warmly"
- **Resolution**: 768x512
- **Duration**: 4 seconds (97 frames @ 24fps)
- **Steps**: 30
- **CFG**: 3.0
- **Sampler**: euler
- **Scheduler**: normal

### Results
- **Output File**: `/home/enric/ComfyUI/output/ltxv_first_i2v_video.webp`
- **File Size**: 5.5 MB
- **Generation Time**: 207.92 seconds (~3.5 minutes)
- **Status**: Successfully generated and saved

## Deliverables

1. ✅ Fixed Gemma tokenizer path issue
2. ✅ Generated first I2V video
3. ✅ Saved video to output directory
4. ✅ Sent video via WhatsApp to +4917620160561
5. ✅ Created ltx-2 skill package:
   - `/home/enric/.openclaw/workspace/skills/ltx-2/README.md`
   - `/home/enric/.openclaw/workspace/skills/ltx-2/skill.yaml`

## Workflow File

API workflow saved at:
`/home/enric/ComfyUI/user_workflows/ltxv_i2v_final.json`

## Key Technical Details

- **VRAM Usage**: ~32GB (RTX 5090)
- **Model Loading**: 
  - Gemma 3 12B: 27.6 GB loaded
  - Video VAE: 2.3 GB loaded
  - LTX-AV: 20.5 GB loaded
- **Inference Speed**: ~1.18s per step (30 steps total)

## Next Steps

The LTX-2 I2V system is now fully operational and ready for:
- Generating videos from any input image
- Experimenting with different prompts and parameters
- Creating longer or higher resolution videos (VRAM permitting)
- Using prompt enhancement with Gemma 3

## References

- ComfyUI running at: http://localhost:8188
- Output directory: /home/enric/ComfyUI/output/
- Model directory: /mnt/c/models/