#!/bin/bash
# Download script for LTX-2 models
# Run: bash download_ltx2_models.sh

set -e

echo "=========================================="
echo "LTX-2 Model Download Script"
echo "=========================================="
echo ""

# Create directories
mkdir -p /mnt/c/models/checkpoints
mkdir -p /mnt/c/models/text_encoders
mkdir -p /mnt/c/models/loras
mkdir -p /mnt/c/models/upscale_models

echo "Checking available space..."
df -h /mnt/c/models/

echo ""
echo "Installing huggingface-hub if needed..."
pip install -q huggingface-hub || true

echo ""
echo "=========================================="
echo "Downloading ltx-2-19b-distilled.safetensors"
echo "Size: ~38 GB"
echo "Destination: /mnt/c/models/checkpoints/"
echo "=========================================="
huggingface-cli download Lightricks/LTX-2 ltx-2-19b-distilled.safetensors \
    --local-dir /mnt/c/models/checkpoints \
    --local-dir-use-symlinks False

echo ""
echo "=========================================="
echo "Downloading gemma_3_12B_it_fp4_mixed.safetensors"
echo "Size: ~6 GB (FP4 quantized)"
echo "Destination: /mnt/c/models/text_encoders/"
echo "=========================================="
huggingface-cli download Comfy-Org/ltx-2 split_files/text_encoders/gemma_3_12B_it_fp4_mixed.safetensors \
    --local-dir /mnt/c/models/text_encoders \
    --local-dir-use-symlinks False

echo ""
echo "=========================================="
echo "Optional: Downloading LoRA for 384px (lightweight)"
echo "Size: ~400 MB"
echo "=========================================="
huggingface-cli download Lightricks/LTX-2 ltx-2-19b-distilled-lora-384.safetensors \
    --local-dir /mnt/c/models/loras \
    --local-dir-use-symlinks False || echo "LoRA download optional, continuing..."

echo ""
echo "=========================================="
echo "Optional: Downloading spatial upscaler"
echo "Size: ~2 GB"
echo "=========================================="
huggingface-cli download Lightricks/LTX-2 ltx-2-spatial-upscaler-x2-1.0.safetensors \
    --local-dir /mnt/c/models/upscale_models \
    --local-dir-use-symlinks False || echo "Upscaler download optional, continuing..."

echo ""
echo "=========================================="
echo "Download complete!"
echo "=========================================="
echo ""
echo "Downloaded models:"
ls -lh /mnt/c/models/checkpoints/ltx-2-19b-distilled.safetensors 2>/dev/null || echo "  - distilled model not found"
ls -lh /mnt/c/models/text_encoders/gemma_3_12B_it_fp4_mixed.safetensors 2>/dev/null || echo "  - gemma encoder not found"
echo ""
echo "You can now use ComfyUI with LTX-2!"
