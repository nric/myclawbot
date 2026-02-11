#!/usr/bin/env python3
"""
Qwen-Image-2512 Generator
Generate images using ComfyUI API with Qwen-Image model
"""

import argparse
import json
import requests
import sys
import time
from pathlib import Path

COMFYUI_URL = "http://127.0.0.1:8188"
OUTPUT_DIR = Path.home() / "ComfyUI" / "output"
WORKFLOW_PATH = Path(__file__).parent.parent / "assets" / "qwen_image_2512.json"

def create_api_workflow(prompt, width=1328, height=1328, steps=20, seed=None, use_lightning=False):
    """Create API-compatible workflow from template"""
    
    if seed is None:
        seed = int(time.time()) % 1000000000
    
    # Base workflow structure (from analyzed JSON)
    workflow = {
        "1": {
            "inputs": {"vae_name": "qwen_image_vae.safetensors"},
            "class_type": "VAELoader"
        },
        "2": {
            "inputs": {
                "clip_name": "qwen_2.5_vl_7b_fp8_scaled.safetensors",
                "type": "qwen_image"
            },
            "class_type": "CLIPLoader"
        },
        "3": {
            "inputs": {
                "unet_name": "qwen_image_2512_fp8_e4m3fn.safetensors",
                "weight_dtype": "fp8_e4m3fn"
            },
            "class_type": "UNETLoader"
        },
        "4": {
            "inputs": {
                "text": prompt,
                "clip": ["2", 0]
            },
            "class_type": "CLIPTextEncode"
        },
        "5": {
            "inputs": {
                "text": "",
                "clip": ["2", 0]
            },
            "class_type": "CLIPTextEncode"
        },
        "6": {
            "inputs": {
                "width": width,
                "height": height,
                "batch_size": 1
            },
            "class_type": "EmptySD3LatentImage"
        },
        "7": {
            "inputs": {
                "seed": seed,
                "steps": steps,
                "cfg": 4.5,
                "sampler_name": "euler",
                "scheduler": "normal",
                "denoise": 1.0,
                "model": ["8", 0],
                "positive": ["4", 0],
                "negative": ["5", 0],
                "latent_image": ["6", 0]
            },
            "class_type": "KSampler"
        },
        "8": {
            "inputs": {
                "shift": 1.73,
                "model": ["3", 0]
            },
            "class_type": "ModelSamplingAuraFlow"
        },
        "9": {
            "inputs": {
                "samples": ["7", 0],
                "vae": ["1", 0]
            },
            "class_type": "VAEDecode"
        },
        "10": {
            "inputs": {
                "filename_prefix": "qwen_image",
                "images": ["9", 0]
            },
            "class_type": "SaveImage"
        }
    }
    
    # Add Lightning LoRA if requested
    if use_lightning:
        workflow["11"] = {
            "inputs": {
                "lora_name": "Qwen-Image-Lightning-4steps-V1.0.safetensors",
                "strength_model": 1.0,
                "strength_clip": 1.0,
                "model": ["3", 0],
                "clip": ["2", 0]
            },
            "class_type": "LoraLoader"
        }
        # Update references
        workflow["7"]["inputs"]["model"] = ["11", 0]
        workflow["4"]["inputs"]["clip"] = ["11", 1]
        workflow["5"]["inputs"]["clip"] = ["11", 1]
        workflow["8"]["inputs"]["model"] = ["11", 0]
    
    return workflow, seed

def submit_workflow(workflow):
    """Submit workflow to ComfyUI API"""
    try:
        response = requests.post(
            f"{COMFYUI_URL}/prompt",
            json={"prompt": workflow},
            timeout=10
        )
        response.raise_for_status()
        return response.json()["prompt_id"]
    except requests.exceptions.ConnectionError:
        print(f"❌ Error: Cannot connect to ComfyUI at {COMFYUI_URL}")
        print("   Start ComfyUI first: cd ~/ComfyUI && python main.py")
        sys.exit(1)
    except Exception as e:
        if hasattr(e, 'response') and e.response is not None:
            print(f"❌ Error submitting workflow: {e.response.text}")
        else:
            print(f"❌ Error submitting workflow: {e}")
        sys.exit(1)

def wait_for_completion(prompt_id, timeout=600):
    """Wait for generation to complete"""
    start = time.time()
    print(f"⏳ Waiting for generation... (timeout: {timeout}s)")
    
    while time.time() - start < timeout:
        try:
            response = requests.get(f"{COMFYUI_URL}/history/{prompt_id}", timeout=10)
            data = response.json()
            
            if prompt_id in data:
                status = data[prompt_id].get("status", {})
                status_str = status.get("status_str", "unknown")
                
                if status_str == "success":
                    print("\n✅ Generation complete!")
                    return True, data[prompt_id]
                elif status_str == "error":
                    print("\n❌ Generation failed!")
                    msgs = status.get("messages", [])
                    errors = [m for m in msgs if isinstance(m, list) and "error" in str(m[0]).lower()]
                    if errors:
                        print(f"   Error: {errors[0][1].get('exception_message', 'Unknown')}")
                    return False, None
                
                # Progress indicator
                elapsed = int(time.time() - start)
                print(f"   Status: {status_str}... ({elapsed}s)", end="\r")
                
        except Exception as e:
            pass
        
        time.sleep(2)
    
    print("\n⚠️  Timeout waiting for generation")
    return False, None

def find_output_file(prompt_id):
    """Find the generated image file"""
    # Check for recent files
    files = sorted(OUTPUT_DIR.glob("qwen_image_*.png"), key=lambda x: x.stat().st_mtime, reverse=True)
    if files:
        return files[0]
    return None

def generate_image(prompt, width=1328, height=1328, steps=20, seed=None, use_lightning=False, output=None):
    """Main generation function"""
    
    print("🎨 Qwen-Image-2512 Generator")
    print(f"   Prompt: {prompt[:60]}...")
    print(f"   Size: {width}x{height}")
    print(f"   Steps: {steps}")
    if use_lightning:
        print(f"   Mode: Lightning (4 steps)")
    print()
    
    # Create workflow
    workflow, seed = create_api_workflow(prompt, width, height, steps, seed, use_lightning)
    print(f"🎲 Seed: {seed}")
    
    # Submit
    print("📤 Submitting to ComfyUI...")
    prompt_id = submit_workflow(workflow)
    print(f"   Prompt ID: {prompt_id}")
    
    # Wait
    success, result = wait_for_completion(prompt_id)
    
    if success:
        # Find output
        output_file = find_output_file(prompt_id)
        if output_file:
            print(f"\n💾 Saved: {output_file}")
            if output:
                import shutil
                shutil.copy(output_file, output)
                print(f"   Copied to: {output}")
            return output_file
        else:
            print(f"\n⚠️  Output saved to: {OUTPUT_DIR}")
            return None
    else:
        return None

def main():
    parser = argparse.ArgumentParser(description="Generate images with Qwen-Image-2512")
    parser.add_argument("prompt", help="Text prompt for generation")
    parser.add_argument("--width", "-W", type=int, default=1328, help="Image width")
    parser.add_argument("--height", "-H", type=int, default=1328, help="Image height")
    parser.add_argument("--steps", "-s", type=int, default=20, help="Inference steps")
    parser.add_argument("--seed", type=int, default=None, help="Random seed")
    parser.add_argument("--lightning", "-l", action="store_true", help="Use Lightning 4-step mode")
    parser.add_argument("--output", "-o", help="Output filename")
    
    args = parser.parse_args()
    
    result = generate_image(
        prompt=args.prompt,
        width=args.width,
        height=args.height,
        steps=args.steps,
        seed=args.seed,
        use_lightning=args.lightning,
        output=args.output
    )
    
    return 0 if result else 1

if __name__ == "__main__":
    sys.exit(main())
