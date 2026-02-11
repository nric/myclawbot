# SOTA Models Reference

Generated: 2026-02-08 16:10

## Recommended Models by Task

### TEXT CHAT

1. **Claude 3.5 Sonnet** (Anthropic)
   - Availability: API
   - Best for: General use

2. **GPT-4o** (OpenAI)
   - Availability: API
   - Best for: General use

3. **Llama 3.1 405B** (Meta)
   - Availability: Ollama
   - Best for: General use

### CODE

1. **Claude 3.5 Sonnet** (Anthropic)
   - Availability: API
   - Best for: General use

2. **DeepSeek-Coder-V2** (DeepSeek)
   - Availability: API/Ollama
   - Best for: General use

3. **Codestral** (Mistral)
   - Availability: API/Ollama
   - Best for: General use

### IMAGE

1. **FLUX.1-dev** (Black Forest Labs)
   - Availability: Local
   - Best for: General use

2. **Qwen-Image-2512** (Alibaba)
   - Availability: Local
   - Best for: General use

3. **DALL-E 3** (OpenAI)
   - Availability: API
   - Best for: General use

### VIDEO

1. **LTX-2 19B** (Lightricks)
   - Availability: Local
   - Best for: General use

2. **Wan 2.1** (Alibaba)
   - Availability: Local
   - Best for: General use

3. **Runway Gen-3** (Runway)
   - Availability: API
   - Best for: General use

## Usage Guidelines

### High-Reasoning Tasks
- Use: Models labeled for reasoning
- Cloud: Claude 3.5 Sonnet, GPT-4o, DeepSeek-R1
- Local: DeepSeek-R1-Distill via Ollama

### Fast/Efficient Tasks
- Use: Gemini Flash, Llama 3.1 8B
- Local: gemma3:4b, qwen2.5:7b

### Code Generation
- Use: Claude 3.5 Sonnet, GPT-4o, DeepSeek-Coder
- Local: codestral, codellama

### Image Generation
- Local: FLUX.1-dev, Qwen-Image-2512
- API: DALL-E 3, Midjourney

### Video Generation
- Local: LTX-2 (Lightricks)
- API: Runway Gen-3, Pika

## Cost-Optimized Strategy

1. Always try local Ollama models first
2. Use Gemini Flash for quick tasks
3. Reserve premium models (Claude, GPT-4o) for complex reasoning
4. Batch-process with local models when possible

## Last Check

Models verified working on this system:
