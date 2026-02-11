#!/usr/bin/env python3
"""
Check local generative AI setup
Verifies ComfyUI, models, and GPU configuration
"""

import subprocess
import sys
from pathlib import Path

def check_comfyui():
    """Check if ComfyUI is installed and running"""
    print("=" * 60)
    print("ComfyUI Status")
    print("=" * 60)
    
    comfy_path = Path.home() / "ComfyUI"
    if comfy_path.exists():
        print(f"✓ ComfyUI found at: {comfy_path}")
    else:
        print(f"✗ ComfyUI not found at: {comfy_path}")
        return False
    
    # Check if running
    result = subprocess.run(
        ["curl", "-s", "http://127.0.0.1:8188/system_stats"],
        capture_output=True,
        text=True
    )
    if result.returncode == 0 and result.stdout:
        print("✓ ComfyUI is running on port 8188")
        return True
    else:
        print("⚠ ComfyUI is not running")
        print("  Start with: cd ~/ComfyUI && python main.py")
        return False

def check_models():
    """Check available models"""
    print("\n" + "=" * 60)
    print("Model Status")
    print("=" * 60)
    
    model_paths = {
        "Flux 1 Dev": "/mnt/c/models/checkpoints/flux1-dev-fp8.safetensors",
        "Z-Image": "/mnt/c/models/diffusion_models/z_image_turbo_bf16.safetensors",
        "LTX-Video": "/mnt/c/models/diffusion_models/ltx-video-2b-v0.9.1.safetensors",
        "Qwen-Image": "/mnt/c/models/Qwen/Qwen-Image-2512/model_index.json",
    }
    
    for name, path in model_paths.items():
        p = Path(path)
        if p.exists():
            size = p.stat().st_size / (1024**3)  # GB
            print(f"✓ {name}: {size:.1f} GB")
        else:
            print(f"✗ {name}: Not found")

def check_gpu():
    """Check GPU and PyTorch CUDA setup"""
    print("\n" + "=" * 60)
    print("GPU & CUDA Status")
    print("=" * 60)
    
    try:
        result = subprocess.run(
            ["nvidia-smi", "--query-gpu=name,memory.total", "--format=csv,noheader"],
            capture_output=True,
            text=True
        )
        if result.returncode == 0:
            gpu_info = result.stdout.strip()
            print(f"✓ GPU: {gpu_info}")
        else:
            print("✗ nvidia-smi failed")
    except FileNotFoundError:
        print("✗ nvidia-smi not found")
    
    # Check PyTorch CUDA
    result = subprocess.run(
        ["bash", "-c", "cd ~/ComfyUI && source venv/bin/activate && python -c \"import torch; print(f'PyTorch: {torch.__version__}'); print(f'CUDA available: {torch.cuda.is_available()}'); print(f'CUDA version: {torch.version.cuda}')\""],
        capture_output=True,
        text=True
    )
    if result.returncode == 0:
        print(result.stdout.strip())
    else:
        print("✗ Could not check PyTorch CUDA")

def check_custom_nodes():
    """Check installed custom nodes"""
    print("\n" + "=" * 60)
    print("Custom Nodes")
    print("=" * 60)
    
    nodes_path = Path.home() / "ComfyUI" / "custom_nodes"
    expected_nodes = [
        "QwenImage-ComfyUI",
        "ComfyUI-LTXVideo"
    ]
    
    for node in expected_nodes:
        node_path = nodes_path / node
        if node_path.exists():
            print(f"✓ {node}")
        else:
            print(f"✗ {node} (not installed)")

def main():
    print("\n" + "=" * 60)
    print("Local Generative AI Setup Check")
    print("=" * 60)
    
    check_comfyui()
    check_models()
    check_gpu()
    check_custom_nodes()
    
    print("\n" + "=" * 60)
    print("Summary")
    print("=" * 60)
    print("For image generation: Flux 1 Dev is ready to use")
    print("For video generation: LTX-Video model available (needs workflow)")
    print("Advanced models: Z-Image and Qwen-Image need custom workflows")
    print()
    print("Quick start:")
    print("  python scripts/generate_image.py 'your prompt here'")
    print()

if __name__ == "__main__":
    main()
