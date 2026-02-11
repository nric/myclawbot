#!/usr/bin/env python3
"""
Generate image using ComfyUI API
Usage: python generate_image.py "your prompt here" --model flux --output result.png
"""

import argparse
import json
import requests
import sys
import time
from pathlib import Path

COMFYUI_URL = "http://127.0.0.1:8188"
OUTPUT_DIR = Path.home() / "ComfyUI" / "output"

def create_flux_workflow(prompt, negative_prompt="", width=1024, height=1024, seed=42, steps=20):
    """Create Flux workflow JSON"""
    return {
        "1": {
            "inputs": {"ckpt_name": "flux1-dev-fp8.safetensors"},
            "class_type": "CheckpointLoaderSimple"
        },
        "2": {
            "inputs": {"text": prompt, "clip": ["1", 1]},
            "class_type": "CLIPTextEncode"
        },
        "3": {
            "inputs": {"text": negative_prompt, "clip": ["1", 1]},
            "class_type": "CLIPTextEncode"
        },
        "4": {
            "inputs": {"width": width, "height": height, "batch_size": 1},
            "class_type": "EmptyLatentImage"
        },
        "5": {
            "inputs": {
                "seed": seed,
                "steps": steps,
                "cfg": 1.0,
                "sampler_name": "euler",
                "scheduler": "normal",
                "denoise": 1,
                "model": ["1", 0],
                "positive": ["2", 0],
                "negative": ["3", 0],
                "latent_image": ["4", 0]
            },
            "class_type": "KSampler"
        },
        "6": {
            "inputs": {"samples": ["5", 0], "vae": ["1", 2]},
            "class_type": "VAEDecode"
        },
        "7": {
            "inputs": {"filename_prefix": "api_output", "images": ["6", 0]},
            "class_type": "SaveImage"
        }
    }

def submit_workflow(workflow):
    """Submit workflow to ComfyUI"""
    try:
        response = requests.post(
            f"{COMFYUI_URL}/prompt",
            json={"prompt": workflow},
            timeout=10
        )
        response.raise_for_status()
        return response.json()["prompt_id"]
    except requests.exceptions.ConnectionError:
        print(f"Error: Cannot connect to ComfyUI at {COMFYUI_URL}")
        print("Make sure ComfyUI is running: cd ~/ComfyUI && python main.py")
        sys.exit(1)
    except Exception as e:
        print(f"Error submitting workflow: {e}")
        sys.exit(1)

def wait_for_completion(prompt_id, timeout=300):
    """Wait for generation to complete"""
    start = time.time()
    print(f"Waiting for generation... (timeout: {timeout}s)")
    
    while time.time() - start < timeout:
        try:
            response = requests.get(f"{COMFYUI_URL}/history/{prompt_id}", timeout=10)
            data = response.json()
            
            if prompt_id in data:
                status = data[prompt_id].get("status", {})
                status_str = status.get("status_str", "unknown")
                
                if status_str == "success":
                    print("✓ Generation complete!")
                    return True
                elif status_str == "error":
                    print("✗ Generation failed!")
                    # Get error details
                    msgs = status.get("messages", [])
                    errors = [m for m in msgs if isinstance(m, list) and len(m) > 1 and "error" in str(m[0]).lower()]
                    if errors:
                        print(f"Error: {errors[0][1].get('exception_message', 'Unknown error')}")
                    return False
                
                print(f"  Status: {status_str}...", end="\r")
        except Exception as e:
            print(f"  Warning: {e}", end="\r")
        
        time.sleep(2)
    
    print("\n✗ Timeout waiting for generation")
    return False

def find_latest_output(prefix="api_output"):
    """Find the most recent output file"""
    files = sorted(OUTPUT_DIR.glob(f"{prefix}_*.png"), key=lambda x: x.stat().st_mtime, reverse=True)
    return files[0] if files else None

def main():
    parser = argparse.ArgumentParser(description="Generate images using ComfyUI")
    parser.add_argument("prompt", help="Text prompt for generation")
    parser.add_argument("--negative", "-n", default="", help="Negative prompt")
    parser.add_argument("--model", "-m", default="flux", choices=["flux"], help="Model to use")
    parser.add_argument("--width", "-W", type=int, default=1024, help="Image width")
    parser.add_argument("--height", "-H", type=int, default=1024, help="Image height")
    parser.add_argument("--steps", "-s", type=int, default=20, help="Sampling steps")
    parser.add_argument("--seed", type=int, default=None, help="Random seed")
    parser.add_argument("--output", "-o", help="Output filename")
    
    args = parser.parse_args()
    
    # Use random seed if not specified
    if args.seed is None:
        args.seed = int(time.time()) % 100000
    
    print(f"Prompt: {args.prompt}")
    print(f"Model: {args.model}")
    print(f"Size: {args.width}x{args.height}")
    print(f"Seed: {args.seed}")
    print("-" * 50)
    
    # Create workflow
    if args.model == "flux":
        workflow = create_flux_workflow(
            args.prompt,
            args.negative,
            args.width,
            args.height,
            args.seed,
            args.steps
        )
    
    # Submit and wait
    prompt_id = submit_workflow(workflow)
    print(f"Submitted: {prompt_id}")
    
    success = wait_for_completion(prompt_id)
    
    if success:
        output_file = find_latest_output()
        if output_file:
            print(f"\nOutput: {output_file}")
            if args.output:
                import shutil
                shutil.copy(output_file, args.output)
                print(f"Copied to: {args.output}")
        else:
            print(f"\nOutput saved to: {OUTPUT_DIR}")
    else:
        sys.exit(1)

if __name__ == "__main__":
    main()
