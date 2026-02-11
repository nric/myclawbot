# LTX-2 Image-to-Video Examples

## Creative Use Cases

### Portrait Photography
Transform still portraits into living photos:
```bash
ltx.py i2v ./portrait.jpg "Subject blinks and smiles naturally, subtle head movement, maintaining eye contact with camera" --length 121
```

### Product Showcase
Create dynamic product videos from catalog images:
```bash
ltx.py i2v ./product.png "Product rotates 360 degrees on display pedestal, studio lighting highlights features" --length 241
```

### Nature & Landscapes
Bring landscapes to life:
```bash
ltx.py i2v ./mountain.png "Time-lapse effect with clouds flowing over peaks, sunlight shifting across valleys, trees swaying" --length 241
```

### Character Animation
Animate game characters or avatars:
```bash
ltx.py i2v ./avatar.png "Character performs idle animation, breathing, looking around, subtle cloth physics" --length 121
```

### Abstract Art
Create mesmerizing abstract animations:
```bash
ltx.py i2v ./abstract.png "Colors flowing and morphing like liquid, patterns rotating and evolving organically" --length 121
```

## Advanced Techniques

### Camera Movements
- **Pan**: "Camera pans slowly from left to right"
- **Zoom**: "Smooth zoom into subject's face"
- **Dolly**: "Camera pulls back while maintaining focus"
- **Orbit**: "Camera orbits 360 degrees around subject"

### Environmental Effects
- **Weather**: "Rain falling gently, puddles rippling"
- **Lighting**: "Sunset colors shifting across scene"
- **Particles**: "Dust motes floating in sunbeams"
- **Fire/Smoke**: "Campfire flames dancing, smoke rising"

### Character Motions
- **Emotions**: "Face transitioning from neutral to joyful"
- **Actions**: "Hands gesturing while explaining"
- **Walk cycles**: "Character walking with natural gait"
- **Combat**: "Sword swing with dynamic motion blur"

## Frame Length Guide

| Duration | Frames | Use Case |
|----------|--------|----------|
| 2s | 49 | Quick gestures |
| 5s | 121 | Standard social media |
| 10s | 241 | Longer narratives |
| 20s | 481 | Extended scenes |

## Tips for Best Results

1. **Input Image Quality**: Higher resolution input = better output
2. **Motion Consistency**: Describe continuous motion, not jumps
3. **Background Stability**: Mention if background should stay static
4. **Subject Isolation**: Clear subjects animate better than cluttered scenes
5. **Test at 360p**: Quick preview before full 720p render

## Common Pitfalls to Avoid

❌ "Person changes into a wolf" (morphing not supported well)
✅ "Person growls and moves aggressively"

❌ "Car drives away then comes back" (direction changes hard)
✅ "Car driving steadily down highway"

❌ "Sudden camera shake" (abrupt motions fail)
✅ "Handheld camera with subtle natural movement"
