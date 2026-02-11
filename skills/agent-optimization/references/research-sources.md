# Research Sources for Agent Optimization

Curated list of high-quality information sources for continuous improvement.

## OpenClaw Ecosystem

### Official Channels
- **GitHub**: https://github.com/openclaw/openclaw
  - Watch releases, issues, discussions
  - Check for new features and bug fixes
  
- **Discord**: https://discord.com/invite/clawd
  - #announcements for major updates
  - #general for community tips
  - #skills for new skill announcements

- **Documentation**: https://docs.openclaw.ai
  - Check periodically for new guides
  
- **ClawHub**: https://clawhub.com
  - Browse new skills weekly
  - Check trending and featured

## Model Landscape

### OpenRouter (Cloud Models)
- **Dashboard**: https://openrouter.ai/models
  - Track new model releases
  - Compare pricing and performance
  - Check for special offers

### Ollama (Local Models)
- **Library**: https://ollama.com/library
  - Weekly: `ollama list` then check for updates
  - Key models to track:
    - qwen3-coder (coding tasks)
    - kimi-k2.5 (multimodal agent)
    - deepseek-v3.2 (reasoning)
    - gemma3 (general purpose)
    - mistral-small (efficient)

### Model Evaluation Sources
- **LMSYS Chatbot Arena**: https://chat.lmsys.org/
  - Leaderboard updates
- **Artificial Analysis**: https://artificialanalysis.ai/
  - Model comparison and benchmarks

## AI/Agent Research

### Academic
- **arXiv AI**: https://arxiv.org/list/cs.AI/recent
  - Filter: agents, LLM, multimodal
- **HuggingFace Papers**: https://huggingface.co/papers
  - Trending AI research
- **Papers with Code**: https://paperswithcode.com/
  - Implementations available

### Industry
- **Anthropic Research**: https://www.anthropic.com/research
  - Constitutional AI, agent safety
- **Google AI Blog**: https://ai.googleblog.com/
  - Gemini updates, new capabilities
- **OpenAI Blog**: https://openai.com/blog/
  - Model announcements

### News & Communities
- **Hacker News**: https://news.ycombinator.com/
  - Search: "AI agents", "LLM", "local models"
- **Reddit**:
  - r/LocalLLaMA (local model discussions)
  - r/ClaudeAI (Anthropic ecosystem)
  - r/MachineLearning (research)
  - r/OpenClaw (if exists)

### Newsletters
- **Import AI**: https://importai.substack.com/
- **The Batch**: https://www.deeplearning.ai/the-batch/
- **TLDR AI**: https://tldr.tech/ai

## Tools & Integrations

### MCP (Model Context Protocol)
- **Official**: https://github.com/modelcontextprotocol
  - New servers and capabilities
- **Community**: https://github.com/modelcontextprotocol/servers

### Browser Automation
- **Playwright**: https://playwright.dev/
  - New browser features
- **Browser-Use**: https://github.com/browser-use/browser-use
  - Agentic browser control

### Coding Agents
- **Codex CLI**: OpenAI updates
- **Claude Code**: Anthropic releases
- **OpenCode**: https://github.com/opencode-ai/opencode
- **Pi Coding Agent**: DeepSeek updates

## Infrastructure

### Hardware/Performance
- **NVIDIA Drivers**: https://www.nvidia.com/drivers
  - CUDA updates, new features
- **ROCm**: AMD GPU support tracking

### Container/Orchestration
- **Docker Hub**: New official images
- **Kubernetes**: AI/ML tooling updates

## Productivity & Workflow

### Development Tools
- **GitHub CLI**: `gh --version` and release notes
- **New CLI tools**: Check Product Hunt, HN

### Automation
- **n8n**: https://n8n.io/workflows
  - New integrations
- **Zapier**: AI feature updates

## Monitoring Strategy

### Daily (Automated)
- HEARTBEAT.md tasks
- OpenClaw gateway status
- System health

### Weekly (Manual Research)
- Review all sources above
- Run `ollama list` for updates
- Check ClawHub for new skills
- Gemini CLI for latest info

### Monthly (Deep Dive)
- Academic paper review
- Major model evaluations
- Architecture improvements
- Skill audit (remove unused)

## Quick Commands

```bash
# Check all at once
gemini "What's new in AI agents this week? OpenClaw, OpenRouter, Ollama updates?"

# Model updates
ollama list && echo "Check https://ollama.com/library for newer versions"

# GitHub releases
gh release list --repo openclaw/openclaw --limit 5

# Skill updates
clawhub list | grep -i update
```

## Evaluation Criteria

Before adding to research rotation:
1. **Signal/Noise**: High-quality, low-hype
2. **Relevance**: Directly applicable to our workflow
3. **Freshness**: Regular updates
4. **Community**: Active discussion
5. **Credibility**: Established source

## Archive

Previously valuable, now monitor less frequently:
- (None yet - update as needed)

---

*Last Updated: 2026-02-08*
*Next Review: 2026-02-15*
