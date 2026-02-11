---
name: ltx-i2v
description: Generate videos from images using LTX-2 Image-to-Video (I2V) via ComfyUI. Transform static images into animated videos with motion and effects. Use when the user wants to animate an existing image, add movement to photos, or create video content from image assets.
---

# LTX-2 Image-to-Video Generation

Transform static images into dynamic videos using the LTX-2 I2V model.

## Overview

The I2V (Image-to-Video) capability extends LTX-2 to animate existing images:
- Takes an input image as starting frame
- Generates subsequent frames based on motion prompt
- Maintains visual consistency with source image
- Integrated audio generation

## Quick Start

### Basic I2V Generation

```bash
/home/enric/ComfyUI/ltx.py i2v ./image.png "motion description" --resolution 720p --length 121
```

### Parameters

| Parameter | Required | Description | Default |
|-----------|----------|-------------|---------|
| `image` | ✅ | Path to input image (PNG/JPG) | - |
| `prompt` | ✅ | Motion/action description | - |
| `--output` | ❌ | Output filename prefix | `ltx_i2v` |
| `--resolution` | ❌ | Preset: `720p`, `540p`, `360p` | `720p` |
| `--width`/`--height` | ❌ | Custom dimensions | From image |
| `--length` | ❌ | Frame count (24fps) | `121` (~5s) |
| `--steps` | ❌ | Sampling steps | `25` |
| `--cfg` | ❌ | CFG scale | `4.0` |
| `--seed` | ❌ | Random seed | Random |

## Example Workflows

### Portrait Animation
```bash
/home/enric/ComfyUI/ltx.py i2v ./portrait.jpg "The person smiles gently and looks around" --resolution 720p --length 121
```

### Nature Scene
```bash
/home/enric/ComfyUI/ltx.py i2v ./landscape.png "Clouds moving across the sky, leaves rustling in wind" --resolution 720p --length 241
```

### Object Motion
```bash
/home/enric/ComfyUI/ltx.py i2v ./car.png "Sports car driving on highway, camera following from side" --resolution 720p --length 121
```

### Character Animation
```bash
/home/enric/ComfyUI/ltx.py i2v ./character.png "Character walking forward confidently, clothes moving naturally" --resolution 720p --length 121
```

## Prompt Engineering for I2V

### Motion Descriptors
- **Camera**: "camera pans left", "zoom in slowly", "dolly shot"
- **Subject**: "walking forward", "turning around", "gesturing"
- **Environment**: "wind blowing", "rain falling", "sunlight shifting"
- **Effects**: "glowing aura", "particles floating", "smoke rising"

### Best Practices
1. **Be specific about motion type**: walking, flying, rotating
2. **Describe speed**: slowly, rapidly, gently
3. **Include camera movement**: panning, zooming, tracking
4. **Add atmospheric effects**: lighting changes, particles
5. **Keep it natural**: avoid extreme deformations

## Combined T2V + I2V Workflow

For complex projects:

1. **Generate base image** with Qwen-Image:
   ```bash
   # Generate image first
   python gen_qwen.py "character description" --output character
   ```

2. **Animate with I2V**:
   ```bash
   # Animate the generated image
   /home/enric/ComfyUI/ltx.py i2v ./character.png "character performing action" --output animated
   ```

## Technical Details

### Model Configuration
- Uses same LTX-2 19B base model as T2V
- Gemma 3 12B text encoder for prompt understanding
- Image encoder processes input frame
- Maintains visual coherence across frames

### Resource Requirements
- **VRAM**: ~27GB for 720p (same as T2V)
- **RAM**: 16GB+ recommended
- **Time**: ~8-12 min for 121 frames at 720p

### Resolution Guidelines
- **720p**: Best quality, slower (~10-12 min)
- **540p**: Balanced quality/speed
- **360p**: Fast preview (~3-5 min)

## Troubleshooting

### Image Not Found
```bash
# Verify path
ls -la /path/to/image.png
```

### VRAM Issues
- Reduce to `360p`
- Decrease `--length`
- Close other GPU applications

### Motion Not as Expected
- Make prompt more specific
- Describe motion direction clearly
- Add "smooth", "natural" modifiers

### Server Issues
```bash
# Restart ComfyUI
pkill -f "python main.py"
```

## Script Helper

Use the provided helper script:

```bash
python /home/enric/ComfyUI/i2v_test.py ./image.png "motion prompt" --output name --length 121
```

See `references/i2v-examples.md` for more use cases.
