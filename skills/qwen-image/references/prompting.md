# Qwen-Image Prompting Guide

## Prompt Structure

Qwen-Image excels with detailed, descriptive prompts:

```
[Subject], [Action/Pose], [Environment/Background], 
[Lighting], [Style/Medium], [Quality modifiers]
```

## Effective Keywords

### Subject Modifiers

**People:**
- Portrait: "close-up portrait", "upper body", "full body"
- Expression: "serene expression", "confident gaze", "joyful smile"
- Clothing: "elegant dress", "casual attire", "professional suit"

**Objects:**
- Material: "polished metal", "weathered wood", "translucent glass"
- Condition: "pristine", "weathered", "glowing", "dusty"

### Environment

**Settings:**
- Nature: "misty forest", "urban alleyway", "serene lake"
- Architecture: "Gothic cathedral", "modern skyscraper", "cozy cottage"
- Time: "golden hour", "blue hour", "midday sun", "starry night"

### Lighting

**Types:**
- Natural: "soft diffused light", "dramatic sunlight", "overcast"
- Artificial: "neon lighting", "warm tungsten", "cool LED"
- Mood: "dramatic shadows", "rim lighting", "volumetric fog"

### Style & Medium

**Art Styles:**
- Traditional: "oil painting", "watercolor", "charcoal sketch"
- Digital: "digital art", "concept art", "3D render"
- Photographic: "photorealistic", "cinematic", "editorial photography"

**Modifiers:**
- "highly detailed", "intricate details", "fine textures"
- "8k resolution", "sharp focus", "professional quality"
- "trending on ArtStation", "award-winning"

## Advanced Techniques

### Negative Prompts

Minimal negative prompts needed, but can include:
- "blurry, low quality, distorted"
- "text, watermark, signature"
- "deformed, ugly, duplicate"

### Composition Control

**Camera Angles:**
- "wide angle shot", "telephoto compression"
- "low angle", "high angle", "aerial view"
- "Dutch angle", "over-the-shoulder"

**Framing:**
- "rule of thirds", "centered composition"
- "leading lines", "symmetrical"

### Style Mixing

Combine multiple styles:
```
"Photorealistic portrait in the style of Renaissance painting, 
dramatic chiaroscuro lighting, oil paint texture"
```

## Example Prompts

### Portrait

```
Professional portrait of a young woman with flowing red hair, 
soft natural lighting, shallow depth of field, 
85mm lens, photorealistic, 8k, highly detailed skin texture
```

### Landscape

```
Majestic mountain range at sunrise, snow-capped peaks, 
alpine lake reflection, golden hour lighting, 
panoramic view, cinematic composition, 8k landscape photography
```

### Architecture

```
Futuristic sustainable cityscape, towering organic buildings, 
vertical gardens, clean lines, glass and steel, 
blue hour lighting, architectural photography, photorealistic
```

### Product

```
Premium watch product photography, rose gold case, 
black leather strap, studio lighting, soft shadows, 
white background, macro lens, highly detailed, commercial photography
```

### Fantasy

```
Epic fantasy dragon perched on castle tower, 
iridescent scales, stormy sky with lightning, 
dramatic atmosphere, concept art style, highly detailed, 8k
```

## Tips for Best Results

1. **Be Specific**: Include details about materials, lighting, and mood
2. **Use Quality Tags**: "photorealistic", "8k", "highly detailed"
3. **Camera Settings**: Mention lens type, aperture for photographic looks
4. **Reference Artists**: "in the style of [artist name]" for specific aesthetics
5. **Test Variations**: Generate multiple images with seed variations

## Common Pitfalls

- **Too Vague**: "a nice picture" → "a detailed landscape photograph"
- **Conflicting Terms**: Mixing incompatible styles
- **Overloading**: Too many concepts in one prompt (keep focused)
- **Neglecting Lighting**: Lighting has huge impact on final result
