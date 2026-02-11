#!/usr/bin/env python3
"""
LTX-2 Video Generation Script
Handles T2V and I2V using the fixed directory structure.
"""

import json
import urllib.request
import os
import sys
import argparse

COMFY_URL = "http://127.0.0.1:8188"
WORKFLOW_PATH = "/home/enric/ComfyUI/user_workflows/ltxv_i2v_final.json"

def generate_video(prompt_text, image_name=None, frames=97, steps=30):
    with open(WORKFLOW_PATH, 'r') as f:
        workflow = json.load(f)
    
    # Update prompt
    workflow["3"]["inputs"]["text"] = prompt_text
    
    # Update image if provided
    if image_name:
        workflow["2"]["inputs"]["image"] = image_name
    
    # Update specs
    workflow["6"]["inputs"]["length"] = frames
    workflow["7"]["inputs"]["steps"] = steps
    
    # Submit
    payload = {"prompt": workflow}
    data = json.dumps(payload).encode('utf-8')
    
    req = urllib.request.Request(
        f"{COMFY_URL}/prompt",
        data=data,
        headers={'Content-Type': 'application/json'},
        method='POST'
    )
    
    try:
        with urllib.request.urlopen(req) as response:
            result = json.loads(response.read().decode('utf-8'))
            return result.get('prompt_id')
    except Exception as e:
        print(f"Error submitting prompt: {e}")
        return None

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--prompt", required=True)
    parser.add_argument("--image", help="Filename in ComfyUI input folder")
    parser.add_argument("--frames", type=int, default=97)
    parser.add_argument("--steps", type=int, default=30)
    
    args = parser.parse_args()
    prompt_id = generate_video(args.prompt, args.image, args.frames, args.steps)
    if prompt_id:
        print(f"SUCCESS: Prompt submitted. ID: {prompt_id}")
    else:
        sys.exit(1)
