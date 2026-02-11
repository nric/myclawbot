# Current Task: LTX-2 Video-Generierung (T2V & I2V)

**Gestartet:** 2026-02-04 10:15
**Ziel:** LTX-2 für Text-to-Video und Image-to-Video einrichten, Skill erstellen.

## Setup-Schritte:
- [x] Modelle downloaden:
    - [x] `ltx-2-19b-dev-fp8.safetensors` (Main)
    - [x] `gemma_3_12B_it_fp4_mixed.safetensors` (Text Encoder)
    - [x] `ltx-2-spatial-upscaler-x2-1.0.safetensors` (Upscaler)
    - [x] `ltx-2-19b-distilled-lora-384.safetensors` (LoRA)
    - [x] `ltx-2-19b-lora-camera-control-dolly-left.safetensors` (Camera LoRA)
- [x] ComfyUI Custom Nodes prüfen/aktualisieren für LTX-2.
- [x] Text-to-Video Testlauf (Pikachu).
- [ ] Image-to-Video Testlauf (Roboter-Bild animieren).
- [x] Skill `ltx-2` erstellen (Initialpaket).

## Notizen:
- Nutze `/mnt/c/models/` für alle großen Dateien.
- RTX 5090 (32GB VRAM) sollte die FP8 Versionen problemlos handhaben.
- Wenn das lokale LLM (Ollama) aktiv ist, ist kein VRAM für Video-Generation frei (Modell muss vorher entladen werden).
