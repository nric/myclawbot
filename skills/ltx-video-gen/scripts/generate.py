#!/usr/bin/env python3
"""
LTX-2 Video Generation Helper Script with monitoring and cleanup
"""

import subprocess
import argparse
import sys
import os
import time
from pathlib import Path
import signal

def cleanup_comfyui():
    """Stop ComfyUI server to free VRAM/RAM."""
    print("🧹 Cleaning up ComfyUI server...")
    subprocess.run(["pkill", "-f", "python main.py"], capture_output=True)
    time.sleep(2)
    
    # Verify
    result = subprocess.run(["pgrep", "-f", "python main.py"], capture_output=True)
    if result.returncode != 0:
        print("✓ ComfyUI stopped successfully")
    else:
        print("⚠ Some processes may still be running")

def monitor_progress(log_file, timeout=1200):
    """Monitor generation progress with timeout."""
    start_time = time.time()
    last_progress = ""
    
    print("⏳ Monitoring generation progress...")
    while time.time() - start_time < timeout:
        if Path(log_file).exists():
            with open(log_file, 'r') as f:
                lines = f.readlines()
                for line in lines[-10:]:
                    if "Progress:" in line and line != last_progress:
                        print(line.strip())
                        last_progress = line
                    if "Execution finished" in line or "Generation Complete" in line:
                        return True
        
        # Check if process still running
        result = subprocess.run(["pgrep", "-f", "ltx.py"], capture_output=True)
        if result.returncode != 0 and time.time() - start_time > 30:
            print("⚠ ltx.py process not found")
            return False
            
        time.sleep(10)
    
    print("⚠ Timeout reached")
    return False

def generate_video(
    prompt: str,
    output_name: str = None,
    resolution: str = "720p",
    length: int = 241,
    steps: int = 25,
    cfg: float = 4.0,
    seed: int = None,
    cleanup: bool = True,
    monitor: bool = True
):
    """Generate a video using LTX-2 via ComfyUI with monitoring."""
    
    comfy_dir = Path("/home/enric/ComfyUI")
    ltx_script = comfy_dir / "ltx.py"
    output_dir = comfy_dir / "output"
    log_file = f"/tmp/ltx_{output_name or 'output'}.log"
    
    if not ltx_script.exists():
        print(f"Error: ltx.py not found at {ltx_script}")
        sys.exit(1)
    
    # Cleanup before start
    cleanup_comfyui()
    
    # Build command
    cmd = [
        str(ltx_script),
        "t2v",
        prompt
    ]
    
    if output_name:
        cmd.extend(["--output", output_name])
    
    cmd.extend([
        "--resolution", resolution,
        "--length", str(length),
        "--steps", str(steps),
        "--cfg", str(cfg)
    ])
    
    if seed:
        cmd.extend(["--seed", str(seed)])
    
    print(f"🎬 Starting video generation...")
    print(f"Prompt: {prompt[:60]}...")
    print(f"Resolution: {resolution}, Frames: {length}")
    
    # Run generation with logging
    with open(log_file, 'w') as log:
        process = subprocess.Popen(cmd, stdout=log, stderr=subprocess.STDOUT)
    
    # Monitor progress
    if monitor:
        success = monitor_progress(log_file)
        if not success:
            print("⚠ Generation may have failed or timed out")
            cleanup_comfyui()
            return None
    else:
        process.wait()
    
    # Find output file
    time.sleep(2)  # Wait for file write
    output_files = sorted(output_dir.glob(f"{output_name or 'ltx_t2v'}*.mp4"), 
                          key=lambda p: p.stat().st_mtime, reverse=True)
    
    if output_files:
        latest = output_files[0]
        print(f"\n✓ Video generated: {latest}")
        
        # Cleanup after successful generation
        if cleanup:
            cleanup_comfyui()
        
        return str(latest)
    else:
        print("\n⚠ Could not find output file")
        cleanup_comfyui()
        return None

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate videos with LTX-2")
    parser.add_argument("prompt", help="Video description")
    parser.add_argument("--output", "-o", help="Output filename prefix")
    parser.add_argument("--resolution", "-r", default="720p", choices=["720p", "540p", "360p"])
    parser.add_argument("--length", "-l", type=int, default=241, help="Number of frames (24fps)")
    parser.add_argument("--steps", "-s", type=int, default=25, help="Sampling steps")
    parser.add_argument("--cfg", "-c", type=float, default=4.0, help="CFG scale")
    parser.add_argument("--seed", type=int, help="Random seed")
    parser.add_argument("--cleanup", action="store_true", default=True, help="Cleanup after generation")
    parser.add_argument("--no-cleanup", action="store_true", dest="no_cleanup", help="Skip cleanup")
    parser.add_argument("--monitor", action="store_true", default=True, help="Monitor progress")
    
    args = parser.parse_args()
    cleanup = not args.no_cleanup
    
    result = generate_video(
        prompt=args.prompt,
        output_name=args.output,
        resolution=args.resolution,
        length=args.length,
        steps=args.steps,
        cfg=args.cfg,
        seed=args.seed,
        cleanup=cleanup,
        monitor=args.monitor
    )
    
    sys.exit(0 if result else 1)
