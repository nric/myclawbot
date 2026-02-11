# LTX-2 Video Generation Examples

## Common Use Cases

### Cinematic Shots
```bash
/home/enric/ComfyUI/ltx.py t2v "A cinematic aerial shot of a futuristic city at sunset, neon lights reflecting off wet streets" --resolution 720p --length 241
```

### Character Animation
```bash
/home/enric/ComfyUI/ltx.py t2v "A cute animated robot dancing in a colorful room, smooth movements, Pixar style" --resolution 720p --length 121
```

### Nature Scenes
```bash
/home/enric/ComfyUI/ltx.py t2v "Waves crashing against rocky cliffs during a storm, dramatic lighting, slow motion" --resolution 720p --length 241
```

### Abstract/Artistic
```bash
/home/enric/ComfyUI/ltx.py t2v "Colorful ink swirling in water, forming abstract patterns, vibrant colors" --resolution 720p --length 121
```

## Frame Length Reference

| Duration | Frames (24fps) | Use Case |
|----------|----------------|----------|
| 2s | 49 | Quick gestures |
| 5s | 121 | Short clips |
| 10s | 241 | Standard short video |
| 20s | 481 | Longer narrative |

## Resolution Guidelines

- **720p**: Best quality, slower generation (~8-12 min for 241 frames)
- **540p**: Balanced quality and speed
- **360p**: Fast generation, good for testing (~2-3 min for 121 frames)

## Prompt Engineering Tips

1. **Be specific about motion**: "walking slowly", "spinning rapidly"
2. **Include style keywords**: "cinematic", "animated", "photorealistic"
3. **Describe lighting**: "golden hour", "dramatic shadows", "soft ambient"
4. **Add quality modifiers**: "high quality", "detailed", "smooth animation"
