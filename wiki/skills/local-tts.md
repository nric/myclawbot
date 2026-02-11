---
name: local-tts
description: Local Text-to-Speech using sherpa-onnx (offline, fast, high quality).
metadata:
  {
    "openclaw":
      {
        "emoji": "🗣️",
        "requires": { "bins": ["sherpa-onnx-offline-tts"] }
      }
  }
---

# Local TTS (Sherpa-ONNX)

This skill provides a simple wrapper for generating speech from text using the locally installed `sherpa-onnx` runtime and models.

## Usage

Run the following command to generate audio:

```bash
/home/enric/.openclaw/tools/sherpa-onnx-tts/runtime/bin/sherpa-onnx-offline-tts \
  --vits-model=/home/enric/.openclaw/tools/sherpa-onnx-tts/models/vits-piper-en_US-lessac-high/en_US-lessac-high.onnx \
  --vits-tokens=/home/enric/.openclaw/tools/sherpa-onnx-tts/models/vits-piper-en_US-lessac-high/tokens.txt \
  --vits-data-dir=/home/enric/.openclaw/tools/sherpa-onnx-tts/models/vits-piper-en_US-lessac-high/espeak-ng-data \
  --output-filename=output.wav \
  "Your text here"
```

## Quick Script

A convenience script is available at `/home/enric/.openclaw/workspace/scripts/speak.sh`.

```bash
./scripts/speak.sh "Hello world" output.wav
```

## Installation Details

- **Runtime:** `/home/enric/.openclaw/tools/sherpa-onnx-tts/runtime`
- **Model:** `vits-piper-en_US-lessac-high` (Female, Neutral, High Quality)
- **Model Path:** `/home/enric/.openclaw/tools/sherpa-onnx-tts/models/vits-piper-en_US-lessac-high`

## Adding German

To add German support, download a German model from the [sherpa-onnx release page](https://github.com/k2-fsa/sherpa-onnx/releases/tag/tts-models) (e.g., `vits-piper-de_DE-thorsten-low`) and extract it to the models directory. Then update the paths in the command.
