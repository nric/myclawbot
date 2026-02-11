#!/usr/bin/env python3
"""
SOTA Model Tracker - Weekly Research Script
Checks for latest state-of-the-art AI models across benchmarks.
"""

import json
import os
import sys
from datetime import datetime
from pathlib import Path

# Configuration
MODEL_DB_PATH = Path(__file__).parent.parent / "references" / "model-database.json"
MEMORY_PATH = Path.home() / ".openclaw" / "workspace" / "MEMORY.md"
TRUTH_SEEKER_PATH = Path.home() / ".openclaw" / "workspace" / "skills" / "truth-seeker" / "references" / "sota-models.md"

# Model categories to track
CATEGORIES = {
    "text_chat": ["claude", "gpt", "llama", "gemini", "kimi"],
    "code": ["codestral", "deepseek-coder", "qwen-coder", "codellama"],
    "reasoning": ["o1", "deepseek-r1", "gemini-thinking", "claude-reasoning"],
    "image": ["flux", "sdxl", "midjourney", "qwen-image", "dall-e"],
    "video": ["ltx", "sora", "gen3", "wan", "mochi"],
    "audio": ["whisper", "elevenlabs", "gpt-4o-audio", "kokoro"],
    "embeddings": ["text-embedding", "nomic", "mxbai", "bge"]
}

# Benchmark sources
BENCHMARKS = {
    "lmsys": "https://chat.lmsys.org/?leaderboard",
    "openllm": "https://huggingface.co/spaces/open-llm-leaderboard/open_llm_leaderboard",
    "artificial_analysis": "https://artificialanalysis.ai/",
    "ollama_library": "https://ollama.com/library"
}

def load_model_database():
    """Load current model database."""
    if MODEL_DB_PATH.exists():
        with open(MODEL_DB_PATH) as f:
            return json.load(f)
    return {"last_updated": None, "models": {}}

def save_model_database(db):
    """Save model database."""
    MODEL_DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(MODEL_DB_PATH, 'w') as f:
        json.dump(db, f, indent=2)

def check_ollama_models():
    """Check available Ollama models."""
    try:
        import subprocess
        result = subprocess.run(['ollama', 'list'], capture_output=True, text=True)
        lines = result.stdout.strip().split('\n')[1:]  # Skip header
        models = []
        for line in lines:
            parts = line.split()
            if parts:
                models.append({
                    "name": parts[0],
                    "size": parts[-2] + " " + parts[-1] if len(parts) > 2 else "unknown"
                })
        return models
    except Exception as e:
        print(f"Error checking Ollama: {e}")
        return []

def generate_research_prompt():
    """Generate prompt for web research."""
    return """Research the current state-of-the-art AI models as of {date}.

For each category, identify the TOP 3 models:
1. Text/Chat (Conversational AI)
2. Code Generation
3. Reasoning/Logic
4. Image Generation
5. Video Generation
6. Audio/Speech
7. Embeddings

For each model, provide:
- Name and version
- Provider/Organization
- Best benchmark scores
- Availability (API, Open Source, Ollama)
- Whether it's better than previous SOTA

Focus on models available through:
- OpenRouter
- Ollama (local)
- Direct API

Format as structured JSON-like output for parsing.""".format(date=datetime.now().strftime("%Y-%m-%d"))

def update_memory_file(findings):
    """Update MEMORY.md with new findings."""
    if not MEMORY_PATH.exists():
        print(f"MEMORY.md not found at {MEMORY_PATH}")
        return
    
    with open(MEMORY_PATH) as f:
        content = f.read()
    
    # Add SOTA section if not exists
    sota_section = "## SOTA MODEL TRACKER\n\n"
    sota_section += f"Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n"
    
    for category, models in findings.items():
        sota_section += f"### {category.upper().replace('_', ' ')}\n"
        for model in models[:3]:  # Top 3
            sota_section += f"- **{model['name']}** ({model['provider']}): {model.get('benchmark', 'N/A')}\n"
        sota_section += "\n"
    
    # Replace or append section
    if "## SOTA MODEL TRACKER" in content:
        # Find and replace existing section
        import re
        pattern = r"## SOTA MODEL TRACKER.*?\n(?=##|$)"
        content = re.sub(pattern, sota_section, content, flags=re.DOTALL)
    else:
        content += "\n" + sota_section
    
    with open(MEMORY_PATH, 'w') as f:
        f.write(content)
    
    print(f"✓ Updated {MEMORY_PATH}")

def update_truth_seeker(findings):
    """Update Truth Seeker skill with model recommendations."""
    TRUTH_SEEKER_PATH.parent.mkdir(parents=True, exist_ok=True)
    
    content = f"""# SOTA Models Reference

Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}

## Recommended Models by Task

"""
    
    for category, models in findings.items():
        content += f"### {category.upper().replace('_', ' ')}\n\n"
        for i, model in enumerate(models[:3], 1):
            content += f"{i}. **{model['name']}** ({model['provider']})\n"
            content += f"   - Availability: {model.get('availability', 'Unknown')}\n"
            content += f"   - Best for: {model.get('strengths', 'General use')}\n\n"
    
    content += """## Usage Guidelines

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
"""
    
    with open(TRUTH_SEEKER_PATH, 'w') as f:
        f.write(content)
    
    print(f"✓ Updated {TRUTH_SEEKER_PATH}")

def notify_new_models(new_models):
    """Send WhatsApp notification for interesting new models."""
    if not new_models:
        return
    
    message = "🤖 *Neue SOTA Modelle verfügbar!*\n\n"
    for model in new_models[:5]:  # Limit to 5
        message += f"• *{model['name']}* ({model['provider']})\n"
        message += f"  Kategorie: {model['category']}\n"
        message += f"  Verfügbarkeit: {model.get('availability', 'Unbekannt')}\n\n"
    
    message += "\nSoll ich diese installieren/recherchieren?"
    
    # This would be called via the message tool
    print(f"Would send WhatsApp:\n{message}")
    return message

def main():
    """Main execution."""
    print(f"🚀 SOTA Model Tracker - {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print("=" * 60)
    
    # Load current database
    db = load_model_database()
    print(f"📊 Loaded database (last updated: {db.get('last_updated', 'Never')})")
    
    # Check Ollama models
    ollama_models = check_ollama_models()
    print(f"🦙 Found {len(ollama_models)} Ollama models")
    
    # For now, create a template structure
    # In production, this would call web_search and analyze results
    findings = {
        "text_chat": [
            {"name": "Claude 3.5 Sonnet", "provider": "Anthropic", "availability": "API"},
            {"name": "GPT-4o", "provider": "OpenAI", "availability": "API"},
            {"name": "Llama 3.1 405B", "provider": "Meta", "availability": "Ollama"}
        ],
        "code": [
            {"name": "Claude 3.5 Sonnet", "provider": "Anthropic", "availability": "API"},
            {"name": "DeepSeek-Coder-V2", "provider": "DeepSeek", "availability": "API/Ollama"},
            {"name": "Codestral", "provider": "Mistral", "availability": "API/Ollama"}
        ],
        "image": [
            {"name": "FLUX.1-dev", "provider": "Black Forest Labs", "availability": "Local"},
            {"name": "Qwen-Image-2512", "provider": "Alibaba", "availability": "Local"},
            {"name": "DALL-E 3", "provider": "OpenAI", "availability": "API"}
        ],
        "video": [
            {"name": "LTX-2 19B", "provider": "Lightricks", "availability": "Local"},
            {"name": "Wan 2.1", "provider": "Alibaba", "availability": "Local"},
            {"name": "Runway Gen-3", "provider": "Runway", "availability": "API"}
        ]
    }
    
    # Update files
    update_memory_file(findings)
    update_truth_seeker(findings)
    
    # Check for new models (simplified)
    new_models = []  # Would compare with previous db
    
    if new_models:
        notify_new_models(new_models)
    
    # Save database
    db["last_updated"] = datetime.now().isoformat()
    db["models"] = findings
    save_model_database(db)
    
    print("\n✅ SOTA Model Tracker complete!")
    print(f"📁 Database saved: {MODEL_DB_PATH}")

if __name__ == "__main__":
    main()
