#!/usr/bin/env python3
"""
Qwen-Image-2512 Direct Pipeline
Generate images using Qwen-Image model directly via diffusers
"""

import torch
from diffusers import QwenImagePipeline, QwenImageTransformer2DModel
from transformers import Qwen2_5_VLForConditionalGeneration
import os
from pathlib import Path
import argparse

MODEL_PATH = "/mnt/c/models/Qwen/Qwen-Image-2512"
OUTPUT_DIR = Path.home() / "ComfyUI" / "output"

def generate_image(prompt, negative_prompt="", width=1024, height=1024, steps=20, guidance_scale=4.5, seed=None):
    """Generate image using Qwen-Image-2512"""
    
    print("🚀 Loading Qwen-Image-2512...")
    print(f"   Model: {MODEL_PATH}")
    
    # Set random seed
    if seed is None:
        seed = torch.randint(0, 2**32, (1,)).item()
    generator = torch.Generator(device="cuda").manual_seed(seed)
    
    print(f"   Seed: {seed}")
    
    # Load model components with bfloat16 for efficiency
    print("📥 Loading transformer...")
    transformer = QwenImageTransformer2DModel.from_pretrained(
        os.path.join(MODEL_PATH, "transformer"),
        torch_dtype=torch.bfloat16
    ).to("cuda")
    
    print("📥 Loading text encoder...")
    text_encoder = Qwen2_5_VLForConditionalGeneration.from_pretrained(
        os.path.join(MODEL_PATH, "text_encoder"),
        torch_dtype=torch.bfloat16
    ).to("cuda")
    
    print("🔧 Creating pipeline...")
    pipe = QwenImagePipeline.from_pretrained(
        MODEL_PATH,
        transformer=transformer,
        text_encoder=text_encoder,
        torch_dtype=torch.bfloat16,
    )
    
    # Enable CPU offloading for memory efficiency
    print("🔄 Enabling CPU offloading...")
    pipe.enable_model_cpu_offload()
    if hasattr(pipe, "enable_vae_slicing"):
        pipe.enable_vae_slicing()
    
    print(f"🎨 Generating image...")
    print(f"   Prompt: {prompt[:60]}...")
    print(f"   Size: {width}x{height}")
    print(f"   Steps: {steps}")
    
    # Generate
    image = pipe(
        prompt=prompt,
        negative_prompt=negative_prompt,
        width=width,
        height=height,
        num_inference_steps=steps,
        guidance_scale=guidance_scale,
        generator=generator,
    ).images[0]
    
    # Save
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    output_file = OUTPUT_DIR / f"qwen_image_{seed}.png"
    image.save(output_file)
    
    print(f"✅ Saved: {output_file}")
    return output_file

def main():
    parser = argparse.ArgumentParser(description="Generate images with Qwen-Image-2512")
    parser.add_argument("prompt", help="Text prompt")
    parser.add_argument("--negative", "-n", default="", help="Negative prompt")
    parser.add_argument("--width", "-W", type=int, default=1024, help="Image width")
    parser.add_argument("--height", "-H", type=int, default=1024, help="Image height")
    parser.add_argument("--steps", "-s", type=int, default=20, help="Inference steps")
    parser.add_argument("--cfg", "-c", type=float, default=4.5, help="Guidance scale")
    parser.add_argument("--seed", type=int, default=None, help="Random seed")
    
    args = parser.parse_args()
    
    try:
        output = generate_image(
            prompt=args.prompt,
            negative_prompt=args.negative,
            width=args.width,
            height=args.height,
            steps=args.steps,
            guidance_scale=args.cfg,
            seed=args.seed
        )
        print(f"\n🎉 Success! Image saved to: {output}")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())
