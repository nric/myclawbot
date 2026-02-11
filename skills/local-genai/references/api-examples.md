# ComfyUI API Examples

## API Endpoints

### System Status
```bash
curl -s http://127.0.0.1:8188/system_stats
```

### Queue Status
```bash
curl -s http://127.0.0.1:8188/queue
```

### Available Nodes
```bash
curl -s http://127.0.0.1:8188/object_info
```

### Submit Prompt
```bash
curl -s -X POST http://127.0.0.1:8188/prompt \
  -H "Content-Type: application/json" \
  -d @workflow.json
```

### Check History
```bash
curl -s http://127.0.0.1:8188/history/{prompt_id}
```

## Python Helper Script

```python
import requests
import json
import time

COMFYUI_URL = "http://127.0.0.1:8188"

def submit_workflow(workflow_json):
    """Submit workflow and return prompt_id"""
    response = requests.post(
        f"{COMFYUI_URL}/prompt",
        json={"prompt": workflow_json}
    )
    return response.json()["prompt_id"]

def wait_for_completion(prompt_id, timeout=300):
    """Wait for job completion"""
    start = time.time()
    while time.time() - start < timeout:
        response = requests.get(f"{COMFYUI_URL}/history/{prompt_id}")
        data = response.json()
        
        if prompt_id in data:
            status = data[prompt_id].get("status", {})
            if status.get("status_str") == "success":
                return True
            elif status.get("status_str") == "error":
                return False
        
        time.sleep(5)
    return None

def get_available_models(model_type="CheckpointLoaderSimple"):
    """Get list of available models"""
    response = requests.get(f"{COMFYUI_URL}/object_info")
    data = response.json()
    
    if model_type in data:
        inputs = data[model_type].get("input", {})
        required = inputs.get("required", {})
        
        if "ckpt_name" in required:
            return required["ckpt_name"][0]
    return []

# Example usage
if __name__ == "__main__":
    # Load workflow
    with open("workflow.json") as f:
        workflow = json.load(f)
    
    # Submit
    prompt_id = submit_workflow(workflow)
    print(f"Submitted: {prompt_id}")
    
    # Wait
    success = wait_for_completion(prompt_id)
    print(f"Success: {success}")
```

## Common Node Types

### Loaders
- `CheckpointLoaderSimple` - Load model checkpoint
- `UNETLoader` - Load UNet/diffusion model
- `CLIPLoader` - Load text encoder
- `VAELoader` - Load VAE

### Conditioning
- `CLIPTextEncode` - Encode text prompt
- `LTXVConditioning` - LTX video conditioning

### Sampling
- `KSampler` - Standard sampling
- `EmptyLatentImage` - Create empty image latent
- `EmptyLTXVLatentVideo` - Create empty video latent

### Decoding
- `VAEDecode` - Decode latent to image

### Output
- `SaveImage` - Save generated image
- `SaveVideo` - Save generated video

## Error Handling

Common errors and solutions:

### CUDA Out of Memory
```python
# Reduce batch size or resolution
# Use CPU offloading
```

### Model Not Found
```bash
# Check available models
curl -s http://127.0.0.1:8188/object_info/CheckpointLoaderSimple
```

### Shape Mismatch
- Verify correct CLIP type for model
- Check latent dimensions match model requirements
