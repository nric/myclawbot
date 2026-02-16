# SOTA Models Reference

Generated: 2026-02-15 17:58

## Recommended Models by Task

### TEXT & REASONING (Global SOTA)
1. **Gemini 3 Pro** (Google) - Elo 1492
   - Availability: API
   - Best for: Complex reasoning, deep research, scientific queries.
2. **Grok-4.1-Thinking** (xAI) - Elo 1482
   - Availability: API
   - Best for: Uncensored reasoning, creative thinking.
3. **Claude Opus 4.5** (Anthropic) - Elo 1466
   - Availability: API
   - Best for: Nuanced writing, coding (see below).

### CODING (Global SOTA)
1. **Claude Opus 4.5 (thinking)** - Elo 1510
   - Availability: API
   - Best for: Complex software architecture, debugging hard bugs.
2. **GPT-5.2-high** (OpenAI) - Elo 1465
   - Availability: API
   - Best for: Rapid prototyping, Python scripting.
3. **Qwen 3 Coder** (Alibaba)
   - Availability: Local (`qwen3-coder-128k`)
   - Best for: Local dev, large context code analysis.

### OPEN WEIGHT / LOCAL
1. **DeepSeek-R1** (DeepSeek)
   - Availability: Local (`ollama pull deepseek-r1`) / OpenRouter
   - Best for: Local reasoning powerhouse, cost-effective heavy lifting.
2. **GLM-4.7** (ZhipuAI)
   - Availability: Local (`glm47-q8-partgpu`)
   - Best for: General purpose, multilingual.
3. **Gemma 3** (Google)
   - Availability: Local (`gemma3-128k`)
   - Best for: Efficiency, speed.

### IMAGE & VIDEO
1. **FLUX.1-dev** (Black Forest Labs) - Local Image
2. **LTX-2 19B** (Lightricks) - Local Video
3. **Wan 2.1** (Alibaba) - Local Video

## Cost-Optimized Strategy
1. **Local First:** Use `qwen3-coder-128k` (coding) and `deepseek-r1` (reasoning) via Ollama.
2. **Efficiency:** Use `gemma3-128k` for simple Q&A.
3. **Premium:** Escalate to `gemini-3-pro` or `claude-opus-4.5` via API only when local models fail or for critical verification.
