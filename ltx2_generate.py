#!/usr/bin/env python3
"""
LTX-2 Two-Stage Video Generation Script
Generates video using TI2VidTwoStagesPipeline
"""

import os
import sys
import logging
from pathlib import Path

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Model paths
LTX_MODEL_PATH = "/mnt/c/models/diffusion_models/ltx-2-19b-dev-fp8.safetensors"
SPATIAL_UPSAMPLER_PATH = "/mnt/c/models/upscale_models/ltx-2-spatial-upscaler-x2-1.0.safetensors"
DISTILLED_LORA_PATH = "/mnt/c/models/loras/ltx-2-19b-distilled-lora-384.safetensors"
GEMMA_ROOT = "/mnt/c/models/gemma-for-ltxv"
OUTPUT_DIR = Path.home() / "ComfyUI/output"

# Ensure output directory exists
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

def generate_video(
    prompt: str,
    output_path: str,
    width: int = 512,
    height: int = 320,
    num_frames: int = 97,  # ~4 seconds at 24fps
    frame_rate: float = 24.0,
    num_inference_steps: int = 40,
    seed: int = 42,
    negative_prompt: str = "",
    image_conditioning: list = None,
):
    """
    Generate video using LTX-2 TI2VidTwoStagesPipeline.
    
    Args:
        prompt: Text description of the video
        output_path: Where to save the output MP4
        width: Video width (must be divisible by 64 for two-stage)
        height: Video height (must be divisible by 64 for two-stage)
        num_frames: Number of frames to generate
        frame_rate: Frames per second
        num_inference_steps: Number of denoising steps (higher = better quality, slower)
        seed: Random seed for reproducibility
        negative_prompt: What to avoid in the video
        image_conditioning: Optional list of (image_path, frame_idx, strength) tuples
    """
    import torch
    from ltx_core.loader import LTXV_LORA_COMFY_RENAMING_MAP, LoraPathStrengthAndSDOps
    from ltx_core.components.guiders import MultiModalGuiderParams
    from ltx_pipelines.ti2vid_two_stages import TI2VidTwoStagesPipeline
    from ltx_pipelines.utils.media_io import encode_video
    from ltx_pipelines.utils.constants import AUDIO_SAMPLE_RATE
    from ltx_core.model.video_vae import TilingConfig, get_video_chunks_number

    # Verify model files exist
    for path, name in [
        (LTX_MODEL_PATH, "Main LTX-2 model"),
        (SPATIAL_UPSAMPLER_PATH, "Spatial upsampler"),
        (DISTILLED_LORA_PATH, "Distilled LoRA"),
    ]:
        if not os.path.exists(path):
            raise FileNotFoundError(f"{name} not found at: {path}")

    logger.info(f"Generating video: {width}x{height} @ {frame_rate}fps, {num_frames} frames")
    logger.info(f"Prompt: {prompt}")

    # Setup distilled LoRA
    distilled_lora = [
        LoraPathStrengthAndSDOps(
            DISTILLED_LORA_PATH,
            0.7,  # LoRA strength
            LTXV_LORA_COMFY_RENAMING_MAP
        ),
    ]

    # Create pipeline
    logger.info("Loading LTX-2 Two-Stage Pipeline...")
    pipeline = TI2VidTwoStagesPipeline(
        checkpoint_path=LTX_MODEL_PATH,
        distilled_lora=distilled_lora,
        spatial_upsampler_path=SPATIAL_UPSAMPLER_PATH,
        gemma_root=GEMMA_ROOT,
        loras=[],  # Additional LoRAs can be added here
        fp8transformer=True,  # Enable FP8 for lower memory usage
    )

    # Setup guider parameters
    video_guider_params = MultiModalGuiderParams(
        cfg_scale=3.0,        # Classifier-free guidance scale
        stg_scale=1.0,        # Spatio-temporal guidance
        rescale_scale=0.7,    # Rescale to prevent over-saturation
        modality_scale=3.0,   # Audio-visual sync (video-only: set to 1.0)
        skip_step=0,          # Skip guidance every N steps (0 = never skip)
        stg_blocks=[29],      # Which transformer blocks to perturb
    )

    audio_guider_params = MultiModalGuiderParams(
        cfg_scale=7.0,
        stg_scale=1.0,
        rescale_scale=0.7,
        modality_scale=3.0,
        skip_step=0,
        stg_blocks=[29],
    )

    # Default negative prompt
    if not negative_prompt:
        negative_prompt = "low quality, blurry, distorted, artifacts, noise"

    # Image conditioning (optional)
    if image_conditioning is None:
        images = []
    else:
        images = image_conditioning

    # Setup tiling config
    tiling_config = TilingConfig.default()
    video_chunks_number = get_video_chunks_number(num_frames, tiling_config)

    # Generate video
    logger.info("Starting generation (Stage 1: Low-res + Stage 2: Upsampling)...")
    
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
        images=images,
        tiling_config=tiling_config,
        enhance_prompt=False,  # Set to True to auto-enhance prompt
    )

    # Save video
    logger.info(f"Saving video to: {output_path}")
    encode_video(
        video=video,
        fps=frame_rate,
        audio=audio,
        audio_sample_rate=AUDIO_SAMPLE_RATE,
        output_path=output_path,
        video_chunks_number=video_chunks_number,
    )

    logger.info(f"Video saved successfully!")
    return output_path


def main():
    """Main entry point - generates test video."""
    
    # Test video parameters
    prompt = "A cat walks across a sunny living room floor, moving from left to right"
    output_path = OUTPUT_DIR / "ltx2_test_video.mp4"
    
    # Generation settings
    # Resolution must be divisible by 64 for two-stage pipeline
    width = 512
    height = 320
    
    # Duration: 4 seconds at 24fps = 96 frames (rounding to 97 for the model)
    # Note: LTX-2 typically expects certain frame counts
    frame_rate = 24.0
    num_frames = 97  # ~4 seconds
    
    num_inference_steps = 40  # Quality vs speed tradeoff
    seed = 42
    
    logger.info("=" * 60)
    logger.info("LTX-2 Video Generation Test")
    logger.info("=" * 60)
    logger.info(f"Output: {output_path}")
    logger.info(f"Resolution: {width}x{height}")
    logger.info(f"Duration: {num_frames / frame_rate:.1f} seconds ({num_frames} frames)")
    logger.info(f"Seed: {seed}")
    logger.info("=" * 60)

    try:
        result_path = generate_video(
            prompt=prompt,
            output_path=str(output_path),
            width=width,
            height=height,
            num_frames=num_frames,
            frame_rate=frame_rate,
            num_inference_steps=num_inference_steps,
            seed=seed,
        )
        logger.info(f"\nSuccess! Video saved to: {result_path}")
        return 0
    except Exception as e:
        logger.error(f"Generation failed: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
