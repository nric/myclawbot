# Backup Documentation
## What Gets Backed Up Daily at 10:00 AM

### ✅ INCLUDED (Essential Files)

#### Core Identity & Configuration
- `AGENTS.md` - Operational protocols
- `SOUL.md` - Existential purpose and philosophy
- `IDENTITY.md` - Personal metadata
- `MEMORY.md` - Long-term memory and context
- `USER.md` - Information about Enric
- `TOOLS.md` - Tool configurations
- `HEARTBEAT.md` - Scheduled tasks
- `*.json` configs (openclaw.json, etc.)

#### Skills (Complete)
- All custom skills in `skills/` directory
- SKILL.md files
- Scripts, references, assets
- Examples: agent-optimization, ltx-video-gen, truth-seeker

#### Memory & History
- `memory/` directory (daily logs, insights)
- Philosophical library entries
- Session learnings

#### Knowledge Base
- `wiki/` directory
- `philosophical_library/` documents
- Research sources

#### Scripts & Tools
- `scripts/` directory
- Helper utilities
- Backup scripts

### ❌ EXCLUDED (Temporary/Large Files)

#### Models & Binaries (Large)
- *.safetensors (AI models)
- *.ckpt, *.pth (PyTorch models)
- *.bin, *.onnx (Model files)
- Models in /mnt/c/models/ (external storage)

#### Generated Media (Large)
- *.mp4, *.avi, *.mov (Videos)
- *.png, *.jpg, *.jpeg (Generated images)
- *.mp3, *.wav (Audio outputs)
- ComfyUI/output/ directory

#### Temporary Files
- *.tmp, *.temp
- __pycache__/ directories
- .venv/, venv/ environments
- Session transcripts (.jsonl files)

#### Cache
- Cache directories
- Downloaded packages
- Build artifacts

### 🔧 How It Works

1. **Daily at 10:00 AM** - Cron triggers backup
2. **Git add -A** - Stages all changes
3. **Commit** - Creates timestamped commit
4. **Push** - Uploads to git@github.com:nric/myclawbot.git
5. **Notification** - WhatsApp confirmation sent

### 🔄 Restoration

If this computer breaks:

```bash
# Clone repository on new machine
git clone git@github.com:nric/myclawbot.git

# Copy to OpenClaw workspace
cp -r myclawbot/* ~/.openclaw/workspace/

# Restart OpenClaw
gateway restart
```

All memories, skills, and configuration will be restored!

### 📊 Backup Log

Check `backup.log` in workspace for history.

---
Last updated: 2026-02-11
Next backup: Tomorrow 10:00 AM
