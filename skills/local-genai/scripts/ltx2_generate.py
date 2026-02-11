#!/usr/bin/env python3
"""
LTX-2 Two-Stage Video Generation Script
Uses the official LTX-2 Python package with existing models.
"""

import torch
import logging
from pathlib import Path

from ltx_pipelines.ti2vid_two_stages import TI2VidTwoStagesPipeline
from ltx_core.loader import LoraPathStrengthAndSDOps, LTXV_LORA_COMFY_RENAMING_MAP
from ltx_core.components.guiders import MultiModalGuiderParams
from ltx_core.model.video_vae import TilingConfig, get_video_chunks_number
from ltx_pipelines.utils.media_io import encode_video
from ltx_pipelines.utils.constants import AUDIO_SAMPLE_RATE

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Model paths - using existing models
MODELS_DIR = Path("/mnt/c/models")
CHECKPOINT_PATH = MODELS_DIR / "diffusion_models" / "ltx-2-19b-dev-fp8.safetensors"
SPATIAL_UPSCALER_PATH = MODELS_DIR / "upscale_models" / "ltx-2-spatial-upscaler-x2-1.0.safetensors"
GEMMA_ROOT = MODELS_DIR / "gemma-for-ltxv"
DISTILLED_LORA_PATH = MODELS_DIR / "loras" / "ltx-2-19b-distilled-lora-384.safetensors"

OUTPUT_DIR = Path.home() / "ComfyUI" / "output"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def generate_video(
    prompt: str,
    negative_prompt: str = "low quality, blurry, distorted",
    output_filename: str = "ltx2_output.mp4",
    height: int = 512,
    width: int = 768,
    num_frames: int = 73,  # ~3 seconds at 24fps
    frame_rate: float = 24.0,
    num_inference_steps: int = 40,
    seed: int = 42,
    enable_fp8: bool = True,
):
    """
    Generate a video using LTX-2 two-stage pipeline.
    
    Args:
        prompt: Text description of the video
        negative_prompt: What to avoid in the video
        output_filename: Name of output file
        height: Video height (must be divisible by 32)
        width: Video width (must be divisible by 32)
        num_frames: Number of frames (must be divisible by 8)
        frame_rate: FPS
        num_inference_steps: Denoising steps (20-40 recommended)
        seed: Random seed
        enable_fp8: Use FP8 quantization for lower VRAM
    """
    
    device = "cuda" if torch.cuda.is_available() else "cpu"
    logger.info(f"Using device: {device}")
    
    # Configure distilled LoRA
    distilled_lora = [
        LoraPathStrengthAndSDOps(
            path=str(DISTILLED_LORA_PATH),
            strength=1.0,
            sd_ops=LTXV_LORA_COMFY_RENAMING_MAP,
        )
    ]
    
    # Initialize pipeline
    logger.info("Initializing LTX-2 Two-Stage Pipeline...")
    pipeline = TI2VidTwoStagesPipeline(
        checkpoint_path=str(CHECKPOINT_PATH),
        distilled_lora=distilled_lora,
        spatial_upsampler_path=str(SPATIAL_UPSCALER_PATH),
        gemma_root=str(GEMMA_ROOT),
        loras=[],  # Additional LoRAs can be added here
        device=device,
        fp8transformer=enable_fp8,
    )
    
    # Configure guider parameters
    video_guider_params = MultiModalGuiderParams(
        cfg_scale=3.0,  # Guidance scale
        stg_scale=0.0,  # Spatiotemporal guidance
        rescale_scale=0.0,
        modality_scale=0.0,
        skip_step=0,
        stg_blocks=None,
    )
    
    audio_guider_params = MultiModalGuiderParams(
        cfg_scale=3.0,
        stg_scale=0.0,
        rescale_scale=0.0,
        modality_scale=0.0,
        skip_step=0,
        stg_blocks=None,
    )
    
    # Tiling configuration for memory efficiency
    tiling_config = TilingConfig.default()
    
    logger.info(f"Generating video: {height}x{width}, {num_frames} frames @ {frame_rate}fps")
    logger.info(f"Prompt: {prompt}")
    
    # Generate video
    video, audio = pipeline(
        prompt=prompt,
        negative_prompt=negative_prompt,
        seed=seed,
        height=height,
        width=width,
        num_frames=num_frames,
        frame_rate=frame_rate,
        num_inference_steps=num_inference_steps,
        video_guider_params=video_guider_params,
        audio_guider_params=audio_guider_params,
        images=[],  # Empty for text-to-video, add (image_path, frame_index, scale) tuples for image-to-video
        tiling_config=tiling_config,
        enhance_prompt=False,
    )
    
    # Get video chunks number for encoding
    video_chunks_number = get_video_chunks_number(num_frames, tiling_config)
    
    # Save video
    output_path = OUTPUT_DIR / output_filename
    logger.info(f"Saving video to: {output_path}")
    
    encode_video(
        video=video,
        fps=frame_rate,
        audio=audio,
        audio_sample_rate=AUDIO_SAMPLE_RATE,
        output_path=str(output_path),
        video_chunks_number=video_chunks_number,
    )
    
    logger.info(f"Video saved successfully: {output_path}")
    
    # Return path for verification
    return output_path


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Generate video using LTX-2")
    parser.add_argument("--prompt", type=str, required=True, help="Text prompt for video generation")
    parser.add_argument("--negative-prompt", type=str, default="low quality, blurry, distorted", help="Negative prompt")
    parser.add_argument("--output", type=str, default="ltx2_output.mp4", help="Output filename")
    parser.add_argument("--height", type=int, default=512, help="Video height (divisible by 32)")
    parser.add_argument("--width", type=int, default=768, help="Video width (divisible by 32)")
    parser.add_argument("--frames", type=int, default=73, help="Number of frames (divisible by 8)")
    parser.add_argument("--fps", type=float, default=24.0, help="Frame rate")
    parser.add_argument("--steps", type=int, default=40, help="Inference steps")
    parser.add_argument("--seed", type=int, default=42, help="Random seed")
    parser.add_argument("--no-fp8", action="store_true", help="Disable FP8 quantization")
    
    args = parser.parse_args()
    
    output = generate_video(
        prompt=args.prompt,
        negative_prompt=args.negative_prompt,
        output_filename=args.output,
        height=args.height,
        width=args.width,
        num_frames=args.frames,
        frame_rate=args.fps,
        num_inference_steps=args.steps,
        seed=args.seed,
        enable_fp8=not args.no_fp8,
    )
    
    print(f"\n✅ Video generated: {output}")
