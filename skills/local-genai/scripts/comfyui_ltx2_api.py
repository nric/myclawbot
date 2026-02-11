#!/usr/bin/env python3
"""
ComfyUI API Client für LTX-2 Video Generation

Nutzt die ComfyUI REST API für automatisierte Video-Generierung.
Kein Browser-Automation nötig - direkte API-Kommunikation.

Usage:
    cd ~/ComfyUI && source venv/bin/activate
    python /home/enric/.openclaw/workspace/skills/local-genai/scripts/comfyui_ltx2_api.py \
        --prompt "Ein Roboter winkt fröhlich" \
        --output ~/ComfyUI/output/lustiger_roboter.mp4
"""

import json
import requests
import argparse
import os
import sys
import time
from pathlib import Path
from typing import Optional, Dict, Any
import websocket
import uuid
import urllib.request
import urllib.parse

# ComfyUI API Endpoints
COMFYUI_URL = "http://127.0.0.1:8188"
WS_URL = "ws://127.0.0.1:8188/ws"

def queue_prompt(prompt: dict, client_id: str = None) -> dict:
    """Send prompt to ComfyUI queue."""
    client_id = client_id or str(uuid.uuid4())
    payload = {"prompt": prompt, "client_id": client_id}
    
    response = requests.post(
        f"{COMFYUI_URL}/prompt",
        json=payload,
        headers={"Content-Type": "application/json"}
    )
    response.raise_for_status()
    return response.json()

def get_history(prompt_id: str) -> dict:
    """Get execution history for a prompt."""
    response = requests.get(f"{COMFYUI_URL}/history/{prompt_id}")
    response.raise_for_status()
    return response.json()

def get_image(filename: str, subfolder: str = "", folder_type: str = "output") -> bytes:
    """Download a generated file from ComfyUI."""
    params = {"filename": filename, "subfolder": subfolder, "type": folder_type}
    url = f"{COMFYUI_URL}/view?{urllib.parse.urlencode(params)}"
    
    response = requests.get(url)
    response.raise_for_status()
    return response.content

def get_available_models(model_type: str = "checkpoints") -> list:
    """Get list of available models."""
    response = requests.get(f"{COMFYUI_URL}/models/{model_type}")
    response.raise_for_status()
    return response.json()

def load_ltx2_workflow(
    prompt: str,
    width: int = 704,
    height: int = 384,
    num_frames: int = 25,
    frame_rate: float = 25.0,
    seed: int = 42,
    steps: int = 20,
    checkpoint: str = "ltx-2-19b-dev-fp8.safetensors"
) -> dict:
    """
    Load and configure LTX-2 workflow.
    
    Based on ComfyUI's video_ltx2_t2v_distilled.json template,
    but simplified for single-stage generation (no spatial upsampling).
    """
    
    # Base workflow structure for LTX-2
    # This creates a simplified single-stage workflow
    workflow = {
        "1": {
            "inputs": {
                "ckpt_name": checkpoint
            },
            "class_type": "CheckpointLoaderSimple",
            "_meta": {"title": "Load Checkpoint"}
        },
        "2": {
            "inputs": {
                "text": prompt,
                "clip": ["1", 1]
            },
            "class_type": "CLIPTextEncode",
            "_meta": {"title": "Positive Prompt"}
        },
        "3": {
            "inputs": {
                "text": "",
                "clip": ["1", 1]
            },
            "class_type": "CLIPTextEncode",
            "_meta": {"title": "Negative Prompt"}
        },
        "4": {
            "inputs": {
                "width": width,
                "height": height,
                "length": num_frames,
                "batch_size": 1
            },
            "class_type": "EmptyLTXVLatentVideo",
            "_meta": {"title": "Empty LTXV Latent Video"}
        },
        "5": {
            "inputs": {
                "seed": seed,
                "control_after_generate": "fixed",
                "noise": ["4", 0]
            },
            "class_type": "RandomNoise",
            "_meta": {"title": "Random Noise"}
        },
        "6": {
            "inputs": {
                "positive": ["2", 0],
                "negative": ["3", 0],
                "vae": ["1", 2],
                "latent_image": ["4", 0]
            },
            "class_type": "LTXVConditioning",
            "_meta": {"title": "LTXV Conditioning"}
        },
        "7": {
            "inputs": {
                "model": ["1", 0],
                "positive": ["6", 0],
                "negative": ["6", 1],
                "cfg": 1.0
            },
            "class_type": "CFGGuider",
            "_meta": {"title": "CFG Guider"}
        },
        "8": {
            "inputs": {
                "sampler_name": "euler_ancestral"
            },
            "class_type": "KSamplerSelect",
            "_meta": {"title": "KSampler Select"}
        },
        "9": {
            "inputs": {
                "scheduler": "normal",
                "steps": steps,
                "denoise": 1.0
            },
            "class_type": "BasicScheduler",
            "_meta": {"title": "Basic Scheduler"}
        },
        "10": {
            "inputs": {
                "noise": ["5", 0],
                "guider": ["7", 0],
                "sampler": ["8", 0],
                "sigmas": ["9", 0],
                "latent_image": ["4", 0]
            },
            "class_type": "SamplerCustomAdvanced",
            "_meta": {"title": "Sampler Custom Advanced"}
        },
        "11": {
            "inputs": {
                "samples": ["10", 0],
                "vae": ["1", 2]
            },
            "class_type": "VAEDecodeTiled",
            "_meta": {"title": "VAE Decode Tiled"}
        },
        "12": {
            "inputs": {
                "filename_prefix": "LTX-2/API",
                "fps": frame_rate,
                "compress_level": 4,
                "images": ["11", 0]
            },
            "class_type": "SaveAnimatedWEBP",
            "_meta": {"title": "Save Animated WEBP"}
        }
    }
    
    return workflow

def track_progress(ws_url: str, prompt_id: str):
    """Track generation progress via WebSocket."""
    print(f"Connecting to WebSocket for progress tracking...")
    
    ws = websocket.create_connection(ws_url)
    
    try:
        while True:
            msg = ws.recv()
            if isinstance(msg, str):
                data = json.loads(msg)
                msg_type = data.get("type")
                
                if msg_type == "progress":
                    value = data.get("data", {}).get("value", 0)
                    max_val = data.get("data", {}).get("max", 100)
                    print(f"\rProgress: {value}/{max_val} ({100*value/max_val:.1f}%)", end="", flush=True)
                
                elif msg_type == "executing":
                    node = data.get("data", {}).get("node")
                    if node is None:
                        print("\n✓ Execution complete!")
                        break
                
                elif msg_type == "execution_error":
                    print(f"\n✗ Execution error: {data}")
                    return False
                    
    except websocket.WebSocketException as e:
        print(f"\nWebSocket error: {e}")
        return False
    finally:
        ws.close()
    
    return True

def wait_for_completion(prompt_id: str, timeout: int = 600) -> Optional[dict]:
    """Wait for prompt execution to complete."""
    start_time = time.time()
    
    while time.time() - start_time < timeout:
        history = get_history(prompt_id)
        
        if prompt_id in history:
            return history[prompt_id]
        
        time.sleep(1)
    
    return None

def main():
    parser = argparse.ArgumentParser(
        description="Generate video using ComfyUI API with LTX-2"
    )
    parser.add_argument("--prompt", required=True, help="Text prompt for video")
    parser.add_argument("--output", required=True, help="Output file path")
    parser.add_argument("--width", type=int, default=704, help="Video width")
    parser.add_argument("--height", type=int, default=384, help="Video height")
    parser.add_argument("--frames", type=int, default=25, help="Number of frames")
    parser.add_argument("--fps", type=float, default=25.0, help="Frame rate")
    parser.add_argument("--steps", type=int, default=20, help="Inference steps")
    parser.add_argument("--seed", type=int, default=42, help="Random seed")
    parser.add_argument("--checkpoint", default="ltx-2-19b-dev-fp8.safetensors",
                       help="Checkpoint filename")
    
    args = parser.parse_args()
    
    # Check ComfyUI is running
    try:
        requests.get(f"{COMFYUI_URL}/system_stats", timeout=5)
    except requests.ConnectionError:
        print(f"✗ ComfyUI nicht erreichbar unter {COMFYUI_URL}")
        print("Bitte starte ComfyUI zuerst:")
        print("  cd ~/ComfyUI && source venv/bin/activate && python main.py --listen 127.0.0.1 --port 8188")
        sys.exit(1)
    
    print("=" * 60)
    print("🎬 ComfyUI LTX-2 API Client")
    print("=" * 60)
    print(f"Prompt: {args.prompt}")
    print(f"Resolution: {args.width}x{args.height}")
    print(f"Frames: {args.frames} @ {args.fps}fps")
    print(f"Steps: {args.steps}, Seed: {args.seed}")
    print("=" * 60)
    
    # Load and configure workflow
    print("\n📋 Lade Workflow...")
    workflow = load_ltx2_workflow(
        prompt=args.prompt,
        width=args.width,
        height=args.height,
        num_frames=args.frames,
        frame_rate=args.fps,
        seed=args.seed,
        steps=args.steps,
        checkpoint=args.checkpoint
    )
    
    # Queue the prompt
    print("🚀 Starte Generation...")
    try:
        result = queue_prompt(workflow)
        prompt_id = result["prompt_id"]
        print(f"Prompt ID: {prompt_id}")
    except Exception as e:
        print(f"✗ Fehler beim Queue: {e}")
        sys.exit(1)
    
    # Track progress
    print("\n⏳ Warte auf Fertigstellung...")
    try:
        success = track_progress(WS_URL, prompt_id)
        if not success:
            print("Fehler während der Ausführung!")
            sys.exit(1)
    except Exception as e:
        print(f"WebSocket-Fehler (versuche Polling): {e}")
        # Fallback to polling
        history = wait_for_completion(prompt_id)
        if not history:
            print("Timeout!")
            sys.exit(1)
    
    # Get results
    print("\n📥 Lade Ergebnisse...")
    history = get_history(prompt_id)
    
    if prompt_id not in history:
        print("✗ Prompt nicht in History gefunden")
        sys.exit(1)
    
    outputs = history[prompt_id].get("outputs", {})
    
    # Find saved files
    saved_files = []
    for node_id, node_output in outputs.items():
        if "images" in node_output:
            for image in node_output["images"]:
                saved_files.append(image["filename"])
    
    if not saved_files:
        print("✗ Keine Dateien generiert")
        sys.exit(1)
    
    print(f"\n✓ Generiert: {saved_files}")
    
    # Download the file
    latest_file = saved_files[-1]
    print(f"\n⬇️  Lade {latest_file} herunter...")
    
    try:
        file_data = get_image(latest_file)
        output_path = Path(args.output)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_path, "wb") as f:
            f.write(file_data)
        
        print(f"✓ Gespeichert: {output_path}")
        print(f"  Größe: {len(file_data) / 1024 / 1024:.1f} MB")
        
    except Exception as e:
        print(f"✗ Download-Fehler: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
