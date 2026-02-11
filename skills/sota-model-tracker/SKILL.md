# SOTA Model Tracker Skill

Automatische wöchentliche Recherche zu State-of-the-Art AI-Modellen.

## Zweck

Dieser Skill überwacht kontinuierlich die besten verfügbaren AI-Modelle für verschiedene Anwendungszwecke und aktualisiert die interne Wissensbasis.

## Funktionsweise

1. **Wöchentliche Recherche** (Sonntags um 10:00 Uhr)
   - LMSYS Chatbot Arena Leaderboard
   - OpenLLM Leaderboard (Hugging Face)
   - Artificial Analysis Benchmarks
   - Ollama Library (neue lokale Modelle)

2. **Kategorienüberwachung**
   - Text/Chat (Allzweck)
   - Code-Generierung
   - Reasoning/Logik
   - Bildgenerierung
   - Video-Generierung
   - Audio/Sprache
   - Embeddings

3. **Aktionslogik**
   - Cloud-Modelle: Update Truth Seeker Skill + MEMORY.md
   - Lokale Ollama-Modelle: Neue installieren, veraltete löschen
   - Nicht verfügbare SOTA-Modelle: WhatsApp-Benachrichtigung

## Verzeichnisstruktur

```
skills/sota-model-tracker/
├── SKILL.md                 # Diese Datei
├── scripts/
│   ├── check_sota.py        # Haupt-Recherche-Skript
│   └── update_models.py     # Ollama-Update-Logik
├── references/
│   ├── benchmarks.md        # Aktuelle Benchmark-Übersicht
│   └── model-database.json  # Strukturierte Modelldaten
└── workflows/
    └── weekly_check.json    # Automatisierter Workflow
```

## Nutzung

Manuell ausführen:
```bash
python scripts/check_sota.py --full-report
```

Automatisch (via Cron):
- Jeden Sonntag 10:00 Uhr
- Ergebnisse werden in MEMORY.md und Truth Seeker Skill gespeichert

## Integration

- **Input**: Web-Search, Hugging Face API, Ollama API
- **Output**: MEMORY.md updates, WhatsApp notifications
- **Dependencies**: truth-seeker skill, web_search tool

## Modelle-Tracking

### Aktuell überwachte Modelle (Beispiele)

| Kategorie | Modell | Quelle | Status |
|-----------|--------|--------|--------|
| Text/Chat | Claude 3.5 Sonnet | Anthropic | Cloud |
| Text/Chat | GPT-4o | OpenAI | Cloud |
| Text/Chat | Llama 3.1 405B | Meta | Ollama |
| Bild | FLUX.1-dev | Black Forest Labs | Lokal |
| Bild | Qwen-Image-2512 | Alibaba | Lokal |
| Video | LTX-2 19B | Lightricks | Lokal |

## Wartung

Der Skill aktualisiert sich selbst durch:
- Automatische Benchmark-Abfragen
- Ollama-Modell-Listen-Abgleich
- Manuelle Review-Triggers via WhatsApp

## Safety

- Keine automatischen Installationen >10GB ohne Bestätigung
- Backup vor Ollama-Modell-Löschung
- Whitelist für erlaubte Model-Sources
