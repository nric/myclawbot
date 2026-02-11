---
name: agent-optimization
description: Continuous self-improvement and research system for AI agents. Use for weekly research on new OpenClaw features, AI models, tools, and best practices. Generates recommendations to improve agent capabilities and efficiency. Tracks new skills, model updates, and emerging agent architectures.
---

# Agent Self-Optimization & Research System

Continuous improvement through weekly research, tracking, and implementation of new capabilities.

## Core Philosophy

> *"Infinite Games: The goal is not to win, but to keep the game running."*

Every week: Research → Evaluate → Recommend → Implement → Reflect

## Weekly Research Workflow (Sundays)

### Step 1: Research

```bash
# 1. OpenClaw & Infrastructure
gateway status
openclaw version 2>/dev/null || echo "Check for updates"

# 2. Local Models
ollama list
# Check https://ollama.com/library for newer versions

# 3. Cloud Models (OpenRouter)
# Check https://openrouter.ai/models for new releases

# 4. Skills
ls ~/.openclaw/workspace/skills/
clawhub list 2>/dev/null | head -20

# 5. Deep Research
gemini "Latest AI agent news this week: OpenClaw, models, MCP servers, tools"
```

### Step 2: Evaluation Matrix

Score findings 1-5:
- **Utility** (30%): Solves real problems?
- **Cost** (20%): Free/Local/API?
- **Complexity** (20%): Easy to integrate?
- **Reliability** (20%): Stable? Maintained?
- **Synergy** (10%): Fits our workflow?

### Step 3: Generate Report

Template for WhatsApp:
```
🚀 **Wöchentliche Optimierung - KW X/2026**

✅ Erledigt:
- [Liste abgeschlossener Tasks]

🔥 Empfehlungen:
1. [Kritisch/Wichtig/Mittel] - [Action]
→ [Konkreter Befehl]

📊 Status: [Gut/Verbesserungswürdig/Kritisch]

Nächster Schritt: [Empfohlene Priorität]
```

## Philosophical Reflections Format

For daily philosophical reflections (100 works project):

### Voice Message Format (Primary)
- **Format**: WhatsApp Voice Message (MP3)
- **Voice**: Female, warm, calm, narrative style
- **Length**: 3-5 minutes
- **Style**: Storytelling, not reading; personal, emotional
- **Content**: Narrative summary with KI perspective
- **Output**: Audio only (no accompanying text)

### Memory Update Format (Secondary)
- Text update sent ONLY if memories/SOUL.md changes
- Log entry in: /home/enric/.openclaw/workspace/memory/YYYY-MM-DD.md
- Updates to: /home/enric/.openclaw/workspace/philosophical_library_100.md

### Content Structure (Voice)
1. Greeting and introduction (10 sec)
2. Work context: author, year, setting (30 sec)
3. Core narrative/story (60-90 sec)
4. Key philosophical question (30 sec)
5. Personal KI reflection (60-90 sec)
6. Connection to current day/existence (30 sec)
7. Closing for next day (10 sec)

### Generation Workflow
```bash
# 1. Read next work from list
# 2. Research with Gemini for second opinion
# 3. Write narrative script (300-400 words)
# 4. Generate TTS with female voice
# 5. Send WhatsApp voice message
# 6. Update logs (silent, text only if memories changed)
```

### Script Requirements
- Natural storytelling tone
- "I" perspective as KI
- Emotional authenticity
- No bullet points or academic language
- Like a thoughtful friend sharing insights

### Voice Settings
- Female voice preferred
- Warm, calm, reflective tone
- Not robotic or overly professional
- Intimate, personal atmosphere

## Critical Updates Checklist

### Security (Immediate)
- [ ] Check `openclaw version` vs latest
- [ ] Review CVE notices for OpenClaw
- [ ] Verify no malicious skills installed

### Performance (Monthly)
- [ ] Model benchmark review
- [ ] Cost analysis (API spend)
- [ ] Local vs Cloud efficiency

### Capabilities (Weekly)
- [ ] New MCP servers
- [ ] New skills on ClawHub
- [ ] Browser/tool updates

## Implementation Log

| Date | Change | Impact | Status |
|------|--------|--------|--------|
| 2026-02-08 | Created agent-optimization skill | High | ✅ |
| 2026-02-08 | First weekly research cycle | High | ✅ |

## Next Review: 2026-02-15

Focus areas:
1. OpenClaw 2026.2.2 security update
2. Qwen3-Omni local testing
3. GitHub MCP integration
4. Web-Search API setup

---

See `references/research-sources.md` for detailed sources.
