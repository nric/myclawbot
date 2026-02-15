# SOTA Models Reference (Truth Seeker)

Last Verification: 2026-02-15 17:50
Source: LMSYS / Feb 2026 Leaderboard

## Tier 1: Supreme Reasoning (Global SOTA)
Use for critical logic, architectural decisions, and truth arbitration.

1.  **Gemini 3 Pro** (Google) - Elo 1492
    - *Best for:* Multimodal reasoning, complex instruction following.
2.  **Grok-4.1-Thinking** (xAI) - Elo 1482
    - *Best for:* Deep reasoning, chain-of-thought verification.
3.  **Claude Opus 4.5 (thinking)** (Anthropic) - Elo 1466 / 1510 (Coding)
    - *Best for:* Coding, nuanced writing, safety-critical tasks.

## Tier 2: High Efficiency / Daily Driver
Use for standard tasks, summaries, and initial drafts.

1.  **Gemini 3 Flash** (Google) - Elo 1470
    - *Best for:* Speed, large context windows.
2.  **GPT-5.2-high** (OpenAI) - Elo 1465
    - *Best for:* General purpose, tool use.

## Tier 3: Local / Open Weights (Privacy & Cost)
Use when offline, for sensitive data, or for bulk processing.

1.  **GLM-4.7** (ChatGLM) - Elo 1445
    - *Status:* Installed (`glm47-q8-partgpu`).
    - *Role:* Primary local reasoner.
2.  **DeepSeek-R1** (DeepSeek)
    - *Status:* Recommended (Not installed).
    - *Role:* Open-weight reasoning champion.
3.  **Qwen 3 Coder** (Alibaba)
    - *Status:* Installed (`qwen3-coder-128k`).
    - *Role:* Local coding specialist.

## Image & Video
- **Image:** FLUX.1-dev (Local), DALL-E 3 (API).
- **Video:** LTX-2 19B (Local), Runway Gen-3 (API).
