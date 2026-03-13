# TTS STANDARDS - GERMAN ONLY (v1.0)
## ABSOLUTE SINGLE SOURCE OF TRUTH

### MANDATORY METHOD
For ALL German TTS tasks:
```
bash /home/enric/.openclaw/workspace/scripts/safe_tts_de.sh "<DEUTSCHER TEXT>" <name>
```

### FORBIDDEN (NEVER USE)
- `tts` tool with German text
- `openclaw tts` command
- Any external TTS API
- Old scripts or methods

### STANDARD WORKFLOW
1. Write German text
2. Call safe_tts_de.sh
3. Send .ogg file via WhatsApp

### VOICE GUARANTEE
- Engine: Sherpa-ONNX
- Model: vits-piper-de_DE-kerstin-low
- Language: GERMAN ONLY

This is the ONLY valid TTS method.
