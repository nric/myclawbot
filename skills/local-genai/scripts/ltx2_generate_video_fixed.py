#!/usr/bin/env python3
"""
LTX-2 Two-Stage Video Generation Script - FIXED VERSION
Generates video using the LTX-2 19B model with spatial upscaling.
This version fixes the Gemma text encoder loading issue.

Usage:
    cd ~/ComfyUI && source venv/bin/activate
    python /home/enric/.openclaw/workspace/skills/local-genai/scripts/ltx2_generate_video_fixed.py \
        --prompt "A cat walks across a sunny living room floor" \
        --output ~/ComfyUI/output/ltx2_test_video.mp4
"""

import sys
import os
import argparse
import logging
import torch
from pathlib import Path

# Add the LTX packages to path (installed via pip)
from ltx_core.components.guiders import MultiModalGuiderParams
from ltx_core.loader import LoraPathStrengthAndSDOps, LTXV_LORA_COMFY_RENAMING_MAP
from ltx_core.model.video_vae import TilingConfig, get_video_chunks_number
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
DEFAULT_DISTILLED_LORA = "/mnt/c/models/loras/ltx-2-19b-distilled-lora-384.safetensors"
DEFAULT_SPATIAL_UPSAMPLER = "/mnt/c/models/upscale_models/ltx-2-spatial-upscaler-x2-1.0.safetensors"
DEFAULT_GEMMA_ROOT = "/mnt/c/models/gemma-for-ltxv"
DEFAULT_OUTPUT_DIR = "~/ComfyUI/output"

# Default parameters for quality/speed balance
DEFAULT_HEIGHT = 512  # Stage 1 generates at half this (256)
DEFAULT_WIDTH = 768   # Stage 1 generates at half this (384)
DEFAULT_NUM_FRAMES = 97  # Must be 8*K + 1 (e.g., 33, 65, 97, 121)
DEFAULT_FRAME_RATE = 24.0
DEFAULT_NUM_INFERENCE_STEPS = 30
DEFAULT_SEED = 42

DEFAULT_NEGATIVE_PROMPT = (
    "blurry, out of focus, overexposed, underexposed, low contrast, washed out colors, "
    "excessive noise, grainy texture, poor lighting, flickering, motion blur, distorted proportions, "
    "unnatural skin tones, deformed facial features, asymmetrical face, missing facial features, "
    "extra limbs, disfigured hands, wrong hand count, artifacts, inconsistent perspective, "
    "camera shake, cartoonish rendering, 3D CGI look, unrealistic materials, uncanny valley effect, "
    "jittery movement, awkward pauses, incorrect timing, AI artifacts."
)


def resolve_path(path: str) -> str:
    """Resolve path with expansion and absolutization."""
    return str(Path(path).expanduser().resolve().as_posix())


def parse_args():
    parser = argparse.ArgumentParser(
        description="Generate video using LTX-2 two-stage pipeline (FIXED)",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    
    parser.add_argument(
        "--checkpoint-path",
        type=str,
        default=DEFAULT_CHECKPOINT,
        help="Path to LTX-2 model checkpoint (.safetensors file)"
    )
    parser.add_argument(
        "--distilled-lora",
        type=str,
        default=DEFAULT_DISTILLED_LORA,
        help="Path to distilled LoRA for stage 2"
    )
    parser.add_argument(
        "--spatial-upsampler-path",
        type=str,
        default=DEFAULT_SPATIAL_UPSAMPLER,
        help="Path to spatial upsampler model"
    )
    parser.add_argument(
        "--gemma-root",
        type=str,
        default=DEFAULT_GEMMA_ROOT,
        help="Path to Gemma text encoder model files"
    )
    parser.add_argument(
        "--prompt",
        type=str,
        required=True,
        help="Text prompt describing the desired video content"
    )
    parser.add_argument(
        "--negative-prompt",
        type=str,
        default=DEFAULT_NEGATIVE_PROMPT,
        help="Negative prompt for things to avoid"
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
        help="Height of output video (must be divisible by 64, stage 1 uses half)"
    )
    parser.add_argument(
        "--width",
        type=int,
        default=DEFAULT_WIDTH,
        help="Width of output video (must be divisible by 64, stage 1 uses half)"
    )
    parser.add_argument(
        "--num-frames",
        type=int,
        default=DEFAULT_NUM_FRAMES,
        help="Number of frames (must be 8*K + 1, e.g., 33, 65, 97, 121)"
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
        help="Number of denoising steps (higher = better quality, slower)"
    )
    parser.add_argument(
        "--video-cfg-scale",
        type=float,
        default=3.0,
        help="Classifier-free guidance scale for video"
    )
    parser.add_argument(
        "--video-stg-scale",
        type=float,
        default=1.0,
        help="Spatio-temporal guidance scale for video"
    )
    parser.add_argument(
        "--video-rescale-scale",
        type=float,
        default=0.7,
        help="Rescale scale for video"
    )
    parser.add_argument(
        "--enable-fp8",
        action="store_true",
        help="Enable FP8 mode to reduce memory usage (RTX 5090 compatible)"
    )
    parser.add_argument(
        "--enhance-prompt",
        action="store_true",
        help="Use LLM to enhance the prompt automatically"
    )
    
    return parser.parse_args()


def validate_model_files(args) -> bool:
    """Check that all required model files exist."""
    files_to_check = [
        ("Checkpoint", args.checkpoint_path),
        ("Distilled LoRA", args.distilled_lora),
        ("Spatial Upsampler", args.spatial_upsampler_path),
        ("Gemma root", args.gemma_root),
    ]
    
    all_exist = True
    for name, path in files_to_check:
        resolved = resolve_path(path)
        if name == "Gemma root":
            exists = os.path.isdir(resolved)
        else:
            exists = os.path.isfile(resolved)
        
        if exists:
            logger.info(f"✓ {name}: {resolved}")
        else:
            logger.error(f"✗ {name} NOT FOUND: {resolved}")
            all_exist = False
    
    return all_exist


def main():
    args = parse_args()
    
    # Resolve all paths
    args.checkpoint_path = resolve_path(args.checkpoint_path)
    args.distilled_lora = resolve_path(args.distilled_lora)
    args.spatial_upsampler_path = resolve_path(args.spatial_upsampler_path)
    args.gemma_root = resolve_path(args.gemma_root)
    args.output_path = resolve_path(args.output_path)
    
    # Validate model files
    logger.info("Validating model files...")
    if not validate_model_files(args):
        logger.error("Some required model files are missing. Please check the paths.")
        sys.exit(1)
    
    # Ensure output directory exists
    output_dir = os.path.dirname(args.output_path)
    os.makedirs(output_dir, exist_ok=True)
    
    # Setup LoRA configuration
    distilled_lora_config = [
        LoraPathStrengthAndSDOps(
            args.distilled_lora,
            1.0,  # strength
            LTXV_LORA_COMFY_RENAMING_MAP
        )
    ]
    
    logger.info("Initializing LTX-2 Two-Stage Pipeline...")
    logger.info(f"  Checkpoint: {os.path.basename(args.checkpoint_path)}")
    logger.info(f"  FP8 Mode: {'Enabled' if args.enable_fp8 else 'Disabled'}")
    logger.info(f"  Output: {args.output_path}")
    logger.info(f"  Resolution: {args.width}x{args.height} @ {args.frame_rate}fps")
    logger.info(f"  Frames: {args.num_frames} (duration: {args.num_frames/args.frame_rate:.1f}s)")
    logger.info(f"  Inference Steps: {args.num_inference_steps}")
    
    # Monkey-patch the model ledger to fix meta tensor issue
    # This is the key fix - we need to ensure the text encoder is loaded with actual weights
    try:
        from ltx_pipelines.utils import model_ledger
        from transformers import AutoModelForCausalLM, AutoTokenizer
        
        original_text_encoder_build = model_ledger.TextEncoderBuilder.build
        
        def patched_text_encoder_build(self, device, dtype):
            """Build text encoder with proper weight loading."""
            logger.info(f"Loading Gemma text encoder from {self.gemma_root}...")
            
            # Load with proper device placement
            model = AutoModelForCausalLM.from_pretrained(
                self.gemma_root,
                torch_dtype=dtype,
                device_map=device if device != "meta" else None,
                low_cpu_mem_usage=False,  # Ensure weights are fully loaded
            )
            
            # Move to target device if not already there
            if device != "meta" and hasattr(model, 'device') and str(model.device) != str(device):
                model = model.to(device)
            
            return model
        
        # Apply the patch
        model_ledger.TextEncoderBuilder.build = patched_text_encoder_build
        logger.info("Applied text encoder loading fix")
        
    except Exception as e:
        logger.warning(f"Could not apply text encoder patch: {e}")
        logger.warning("Will try default loading method...")
    
    # Initialize pipeline
    pipeline = TI2VidTwoStagesPipeline(
        checkpoint_path=args.checkpoint_path,
        distilled_lora=distilled_lora_config,
        spatial_upsampler_path=args.spatial_upsampler_path,
        gemma_root=args.gemma_root,
        loras=[],  # No additional LoRAs for base generation
        fp8transformer=args.enable_fp8,
    )
    
    # Setup tiling config for memory efficiency
    tiling_config = TilingConfig.default()
    video_chunks_number = get_video_chunks_number(args.num_frames, tiling_config)
    
    logger.info(f"Starting video generation...")
    logger.info(f"  Prompt: {args.prompt[:80]}{'...' if len(args.prompt) > 80 else ''}")
    
    try:
        # Generate video
        video, audio = pipeline(
            prompt=args.prompt,
            negative_prompt=args.negative_prompt,
            seed=args.seed,
            height=args.height,
            width=args.width,
            num_frames=args.num_frames,
            frame_rate=args.frame_rate,
            num_inference_steps=args.num_inference_steps,
            video_guider_params=MultiModalGuiderParams(
                cfg_scale=args.video_cfg_scale,
                stg_scale=args.video_stg_scale,
                rescale_scale=args.video_rescale_scale,
                modality_scale=3.0,
                skip_step=0,
                stg_blocks=[29],
            ),
            audio_guider_params=MultiModalGuiderParams(
                cfg_scale=7.0,
                stg_scale=1.0,
                rescale_scale=0.7,
                modality_scale=3.0,
                skip_step=0,
                stg_blocks=[29],
            ),
            images=[],  # No image conditioning for text-to-video
            tiling_config=tiling_config,
            enhance_prompt=args.enhance_prompt,
        )
        
        logger.info("Encoding video to MP4...")
        encode_video(
            video=video,
            fps=args.frame_rate,
            audio=audio,
            audio_sample_rate=AUDIO_SAMPLE_RATE,
            output_path=args.output_path,
            video_chunks_number=video_chunks_number,
        )
        
        # Verify output
        if os.path.exists(args.output_path):
            file_size = os.path.getsize(args.output_path)
            logger.info(f"✓ Video saved successfully!")
            logger.info(f"  Path: {args.output_path}")
            logger.info(f"  Size: {file_size / (1024*1024):.2f} MB")
            
            if file_size < 1024 * 1024:  # Less than 1MB
                logger.warning("  Warning: File size is small, may indicate issues")
        else:
            logger.error("✗ Video file was not created!")
            sys.exit(1)
            
    except Exception as e:
        logger.error(f"Error during generation: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
