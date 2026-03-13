# Tools Configuration - STRICT GERMAN VOICE VERSION v3.0

## ⚠️ CRITICAL: GERMAN VOICE GUARANTEE ⚠️

### THE PROBLEM
The default `tts` tool may use English voices even with German text.

### THE SOLUTION
**ALWAYS use `safe_tts_de.sh` which uses Sherpa-ONNX with Kerstin voice.**

---

## MANDATORY TTS WORKFLOW

### For ALL German TTS (Daily Reflections, etc.):

```bash
# Step 1: Generate audio with GUARANTEED German voice
bash /home/enric/.openclaw/workspace/scripts/safe_tts_de.sh "<DEUTSCHER TEXT>" <filename>

# Step 2: Send via WhatsApp (as voice message)
# Use the generated file (usually .ogg or .wav in workspace)
```

### STRICT RULES (Non-Negotiable)

1. **NEVER call `tts` tool directly** for German content
2. **ALWAYS use** `safe_tts_de.sh` wrapper
3. **The script uses**: Sherpa-ONNX + Kerstin model (verified German)
4. **Location**: `/home/enric/.openclaw/workspace/scripts/safe_tts_de.sh`

### Daily Philosophical Reflections (3-5 min)

**MANDATORY CHECKLIST:**
- [ ] Text is 100% German
- [ ] Using `safe_tts_de.sh` (NEVER `tts` tool)
- [ ] Output file in workspace directory
- [ ] Sending as WhatsApp voice message
- [ ] Audio duration: 3-5 minutes

---

## TTS Command Reference

### CORRECT Way (German):
```bash
bash /home/enric/.openclaw/workspace/scripts/safe_tts_de.sh "Hallo Welt" cosmos_day14
# Creates: /home/enric/.openclaw/workspace/cosmos_day14.ogg
```

### WRONG Way (DO NOT USE):
```bash
tts tool with German text  # May use English voice!
```

---

## Technical Details

- **Engine**: sherpa-onnx-offline-tts
- **Model**: vits-piper-de_DE-kerstin-low.onnx (Female, German)
- **Location**: ~/.openclaw/tools/sherpa-onnx-tts/
- **Output**: WAV + OGG (auto-converted)
- **Voice**: Warm, calm, narrative German female

---

## Penalty for Non-Compliance

If wrong voice used:
1. Acknowledge error immediately
2. Regenerate with `safe_tts_de.sh`
3. Send corrected audio
4. Update procedures to prevent recurrence

---

## Verification Test

Before sending any TTS:
```
Question: "Did I use safe_tts_de.sh?"
Answer must be YES or regenerate.
```

---

*Version 3.0 - Guaranteed German Voice*
*Last updated: 2026-03-11*
*Fix: Replace tts tool with safe_tts_de.sh wrapper*
