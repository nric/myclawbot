#!/bin/bash
# Wöchentliches Agent-Optimierungs-Forschungsskript
# Läuft jeden Sonntag oder bei Bedarf

echo "🔍 Starte wöchentliche Agenten-Forschung..."
echo "=================================="

# OpenClaw prüfen
echo "📦 OpenClaw Status:"
openclaw version 2>/dev/null || echo "  (manuell prüfen: openclaw --version)"

echo ""
echo "🤖 Lokale Modelle (Ollama):"
ollama list 2>/dev/null | head -20 || echo "  Ollama nicht verfügbar"

echo ""
echo "📝 Installierte Skills:"
ls -1 /home/enric/.openclaw/workspace/skills/ 2>/dev/null || echo "  Keine benutzerdefinierten Skills"

echo ""
echo "💡 Empfohlene Forschungsaktionen:"
echo "  1. Prüfe https://github.com/openclaw/openclaw/releases"
echo "  2. Prüfe https://ollama.com/library auf Modell-Updates"
echo "  3. Prüfe https://clawhub.com auf neue Skills"
echo "  4. Führe aus: gemini 'KI-Agenten News diese Woche'"
echo "  5. Discord: https://discord.com/invite/clawd"

echo ""
echo "✅ Forschungszyklus abgeschlossen!"
echo "Nächster Schritt: Ergebnisse auswerten und Empfehlungen erstellen."
