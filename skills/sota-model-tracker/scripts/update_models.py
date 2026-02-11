#!/usr/bin/env python3
"""
Ollama Model Manager
Handles installation and cleanup of Ollama models.
"""

import subprocess
import sys
from pathlib import Path

# Models that should always be kept (core capabilities)
CORE_MODELS = {
    "llama3.1": "General purpose, best overall local model",
    "gemma3": "Efficient, good for quick tasks",
    "qwen2.5": "Multilingual, coding",
    "codestral": "Code generation",
    "nomic-embed-text": "Embeddings",
    "mxbai-embed-large": "Better embeddings",
    "deepseek-r1": "Reasoning tasks"
}

def get_installed_models():
    """Get list of installed Ollama models."""
    try:
        result = subprocess.run(
            ['ollama', 'list'],
            capture_output=True,
            text=True,
            check=True
        )
        models = []
        for line in result.stdout.strip().split('\n')[1:]:  # Skip header
            parts = line.split()
            if parts:
                name = parts[0]
                size = ' '.join(parts[-2:]) if len(parts) > 2 else 'unknown'
                models.append({'name': name, 'size': size})
        return models
    except Exception as e:
        print(f"Error: {e}")
        return []

def install_model(model_name):
    """Install a new Ollama model."""
    print(f"📥 Installing {model_name}...")
    try:
        subprocess.run(
            ['ollama', 'pull', model_name],
            check=True,
            capture_output=True
        )
        print(f"✓ {model_name} installed")
        return True
    except Exception as e:
        print(f"✗ Failed to install {model_name}: {e}")
        return False

def remove_model(model_name):
    """Remove an Ollama model."""
    print(f"🗑️  Removing {model_name}...")
    try:
        subprocess.run(
            ['ollama', 'rm', model_name],
            check=True,
            capture_output=True
        )
        print(f"✓ {model_name} removed")
        return True
    except Exception as e:
        print(f"✗ Failed to remove {model_name}: {e}")
        return False

def check_model_size(model_name):
    """Check size of model before installation."""
    # This would ideally query Ollama API for size info
    # For now, use rough estimates
    SIZE_ESTIMATES = {
        "llama3.1": "4.7GB",
        "llama3.1:70b": "40GB",
        "gemma3": "3.2GB",
        "gemma3:12b": "8GB",
        "qwen2.5": "4.7GB",
        "qwen2.5:14b": "9GB",
        "codestral": "6.7GB",
        "deepseek-r1": "4.7GB",
        "deepseek-r1:14b": "9GB"
    }
    return SIZE_ESTIMATES.get(model_name, "Unknown")

def main():
    """Main execution."""
    print("🦙 Ollama Model Manager")
    print("=" * 50)
    
    # Get current models
    installed = get_installed_models()
    print(f"\n📦 Installed models: {len(installed)}")
    for m in installed:
        marker = " ⭐" if m['name'].split(':')[0] in CORE_MODELS else ""
        print(f"  • {m['name']} ({m['size']}){marker}")
    
    # Check for updates (simplified logic)
    print("\n🔍 Checking for recommended models...")
    
    # Compare with core models
    installed_names = {m['name'].split(':')[0] for m in installed}
    missing = set(CORE_MODELS.keys()) - installed_names
    
    if missing:
        print(f"\n⚠️  Missing core models: {', '.join(missing)}")
        for model in missing:
            size = check_model_size(model)
            print(f"  • {model}: {CORE_MODELS[model]} (~{size})")
    else:
        print("\n✓ All core models installed")
    
    # Find outdated models (not in core list)
    removable = []
    for m in installed:
        base_name = m['name'].split(':')[0]
        if base_name not in CORE_MODELS and not base_name.startswith('all-minilm'):
            removable.append(m)
    
    if removable:
        print(f"\n🧹 Potentially outdated models:")
        for m in removable:
            print(f"  • {m['name']} ({m['size']})")
        print("\nRun with --cleanup to remove these (keeps core models)")

if __name__ == "__main__":
    main()
