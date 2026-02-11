#!/usr/bin/env python3
"""
Vereinfachtes LTX-2 Video Generation Script (nur Stage 1)
Verwendet niedrigere Auflösung für stabilen Betrieb auf RTX 5090.

Usage:
    cd ~/ComfyUI && source venv/bin/activate
    python /home/enric/.openclaw/workspace/skills/local-genai/scripts/ltx2_simple_generate.py \
        --prompt "Ein Roboter winkt" \
        --output ~/ComfyUI/output/ltx2_test.mp4
"""

import sys
import os
import argparse
import logging
from pathlib import Path
import torch

# Add the LTX packages to path
from ltx_core.components.guiders import MultiModalGuiderParams
from ltx_core.loader import LoraPathStrengthAndSDOps, LTXV_LORA_COMFY_RENAMING_MAP
from ltx_core.model.video_vae import TilingConfig
from ltx_pipelines.ti2vid_two_stages import TI2VidTwoStagesPipeline
from ltx_pipelines.utils.media_io import encode_video
from ltx_pipelines.utils.constants import AUDIO_SAMPLE_RATE

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Default paths for models
DEFAULT_CHECKPOINT = "/mnt/c/models/diffusion_models/ltx-2-19b-dev-fp8.safetensors"
DEFAULT_SPATIAL_UPSAMPLER = "/mnt/c/models/upscale_models/ltx-2-spatial-upscaler-x2-1.0.safetensors"
DEFAULT_TEXT_ENCODER = "/mnt/c/models/text_encoders/qwen_2.5_vl_7b_fp8_scaled.safetensors"
DEFAULT_OUTPUT_DIR = "~/ComfyUI/output"

# Konservative Parameter für stabile Ausführung
DEFAULT_HEIGHT = 320  # Niedrige Auflösung für weniger VRAM
DEFAULT_WIDTH = 512   # Muss durch 32 teilbar sein
DEFAULT_NUM_FRAMES = 17  # 8*2 + 1 = 17 Frames
DEFAULT_FRAME_RATE = 25.0
DEFAULT_NUM_INFERENCE_STEPS = 20
DEFAULT_SEED = 42

def resolve_path(path: str) -> str:
    """Resolve path with expansion and absolutization."""
    return str(Path(path).expanduser().resolve().as_posix())

def parse_args():
    parser = argparse.ArgumentParser(
        description="Generate video using LTX-2 (vereinfachte Stage 1 only)",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    
    parser.add_argument(
        "--checkpoint-path",
        type=str,
        default=DEFAULT_CHECKPOINT,
        help="Path to LTX-2 model checkpoint"
    )
    parser.add_argument(
        "--spatial-upsampler-path",
        type=str,
        default=DEFAULT_SPATIAL_UPSAMPLER,
        help="Path to spatial upsampler model (optional, für Stage 2)"
    )
    parser.add_argument(
        "--text-encoder-path",
        type=str,
        default=DEFAULT_TEXT_ENCODER,
        help="Path to text encoder (Qwen FP8)"
    )
    parser.add_argument(
        "--prompt",
        type=str,
        required=True,
        help="Text prompt describing the desired video content"
    )
    parser.add_argument(
        "--output-path",
        type=str,
        required=True,
        help="Path to save the output video (MP4 format)"
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=DEFAULT_SEED,
        help="Random seed for reproducible generation"
    )
    parser.add_argument(
        "--height",
        type=int,
        default=DEFAULT_HEIGHT,
        help="Height of output video (must be divisible by 32)"
    )
    parser.add_argument(
        "--width",
        type=int,
        default=DEFAULT_WIDTH,
        help="Width of output video (must be divisible by 32)"
    )
    parser.add_argument(
        "--num-frames",
        type=int,
        default=DEFAULT_NUM_FRAMES,
        help="Number of frames (8*K + 1, z.B. 9, 17, 25, 33)"
    )
    parser.add_argument(
        "--frame-rate",
        type=float,
        default=DEFAULT_FRAME_RATE,
        help="Frame rate of output video in FPS"
    )
    parser.add_argument(
        "--num-inference-steps",
        type=int,
        default=DEFAULT_NUM_INFERENCE_STEPS,
        help="Number of denoising steps"
    )
    parser.add_argument(
        "--enable-fp8",
        action="store_true",
        default=True,
        help="Enable FP8 mode (immer aktiv für dieses Modell)"
    )
    parser.add_argument(
        "--skip-stage-2",
        action="store_true",
        default=True,
        help="Nur Stage 1 ausführen (schneller, weniger VRAM)"
    )
    
    return parser.parse_args()

def validate_model_files(args) -> bool:
    """Check that all required model files exist."""
    files_to_check = [
        ("Checkpoint", args.checkpoint_path),
        ("Text Encoder", args.text_encoder_path),
    ]
    
    if not args.skip_stage_2:
        files_to_check.append(("Spatial Upsampler", args.spatial_upsampler_path))
    
    all_exist = True
    for name, path in files_to_check:
        resolved = resolve_path(path)
        exists = os.path.isfile(resolved)
        
        if exists:
            size_gb = os.path.getsize(resolved) / (1024**3)
            logger.info(f"✓ {name}: {resolved} ({size_gb:.1f} GB)")
        else:
            logger.error(f"✗ {name} NOT FOUND: {resolved}")
            all_exist = False
    
    return all_exist

def main():
    args = parse_args()
    
    # Resolve all paths
    args.checkpoint_path = resolve_path(args.checkpoint_path)
    args.spatial_upsampler_path = resolve_path(args.spatial_upsampler_path)
    args.text_encoder_path = resolve_path(args.text_encoder_path)
    args.output_path = resolve_path(args.output_path)
    
    # Validate model files
    logger.info("Validating model files...")
    if not validate_model_files(args):
        logger.error("Some required model files are missing.")
        sys.exit(1)
    
    # Ensure output directory exists
    output_dir = os.path.dirname(args.output_path)
    os.makedirs(output_dir, exist_ok=True)
    
    # Log configuration
    logger.info("=" * 60)
    logger.info("LTX-2 Video Generation (Vereinfacht - Stage 1 Only)")
    logger.info("=" * 60)
    logger.info(f"Checkpoint: {os.path.basename(args.checkpoint_path)}")
    logger.info(f"Text Encoder: {os.path.basename(args.text_encoder_path)}")
    logger.info(f"Output: {args.output_path}")
    logger.info(f"Resolution: {args.width}x{args.height} @ {args.frame_rate}fps")
    logger.info(f"Frames: {args.num_frames} (duration: {args.num_frames/args.frame_rate:.1f}s)")
    logger.info(f"Inference Steps: {args.num_inference_steps}")
    logger.info(f"Stage 2 Upsampling: {'Disabled' if args.skip_stage_2 else 'Enabled'}")
    logger.info("=" * 60)
    
    logger.info(f"Prompt: {args.prompt}")
    logger.info("Starting generation...")
    
    # TODO: Implementiere die vereinfachte Generation
    # Für jetzt zeigen wir eine Fehlermeldung mit den korrekten Parametern
    logger.error(""
    logger.error("Dieses Skript ist noch nicht vollständig implementiert.")
    logger.error("Die korrekten ComfyUI-Parameter sind:")
    logger.error(f"  - Auflösung: {args.width}x{args.height} (durch 32 teilbar)")
    logger.error(f"  - Frames: {args.num_frames} (8*K + 1)")
    logger.error(f"  - FPS: {args.frame_rate}")
    logger.error(f"  - Schritte: {args.num_inference_steps}")
    logger.error("")
    logger.error("Bitte verwende stattdessen ComfyUI direkt mit dem Workflow:")
    logger.error("video_ltx2_t2v_distilled.json")
    logger.error(""
    
    sys.exit(1)

if __name__ == "__main__":
    main()
