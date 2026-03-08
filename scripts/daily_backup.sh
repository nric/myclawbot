#!/bin/bash
# Tägliches Agenten-Backup Skript
# Sichert alle wichtigen Agenten-Dateien im Git-Repository
# Ausführung um: 10:00 Uhr täglich

set -e

# Konfiguration
WORKSPACE="/home/enric/.openclaw/workspace"
GIT_REPO="git@github.com:nric/myclawbot.git"
BACKUP_TIME=$(date +"%Y-%m-%d %H:%M:%S")
DATE=$(date +"%Y-%m-%d")

# Farben für Ausgabe
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # Keine Farbe

echo "🛡️  Agenten-Backup - $BACKUP_TIME"
echo "================================"

cd "$WORKSPACE"

# Prüfen ob Git initialisiert ist
if [ ! -d ".git" ]; then
    echo -e "${RED}✗ Git nicht initialisiert${NC}"
    exit 1
fi

# Prüfen ob Remote korrekt ist
current_remote=$(git remote get-url origin 2>/dev/null || echo "")
if [ "$current_remote" != "$GIT_REPO" ]; then
    echo -e "${YELLOW}⚠ Setze Remote auf $GIT_REPO${NC}"
    git remote remove origin 2>/dev/null || true
    git remote add origin "$GIT_REPO"
fi

# Änderungen prüfen
echo "📋 Prüfe auf Änderungen..."
git add -A

# Prüfen ob Änderungen zum Committen vorliegen
if git diff --cached --quiet; then
    echo -e "${GREEN}✓ Keine Änderungen zum Sichern${NC}"
    exit 0
fi

# Zeigen was gesichert wird
echo "📦 Dateien zum Sichern:"
git diff --cached --name-only | head -20
if [ $(git diff --cached --name-only | wc -l) -gt 20 ]; then
    echo "... und $(($(git diff --cached --name-only | wc -l) - 20)) weitere Dateien"
fi

# Backup Commit erstellen
echo "💾 Erstelle Backup-Commit..."
git commit -m "Tägliches Backup - $DATE

- Skills: $(git diff --cached --name-only | grep -c 'skills/' || echo 0) Dateien
- Memory: $(git diff --cached --name-only | grep -c 'memory/' || echo 0) Dateien  
- Config: $(git diff --cached --name-only | grep -c '\.(json|md)$' || echo 0) Dateien

Auto-Backup um 10:00 Uhr"

# Zu Remote pushen
echo "🚀 Pushe zum Remote-Repository..."
if git push origin main 2>/dev/null || git push origin master 2>/dev/null; then
    echo -e "${GREEN}✓ Backup erfolgreich!${NC}"
    echo "📍 Repository: $GIT_REPO"
    echo "🕐 Nächstes Backup: Morgen 10:00 Uhr"
else
    echo -e "${RED}✗ Push fehlgeschlagen - SSH-Schlüssel und Repository-Zugriff prüfen${NC}"
    exit 1
fi

# Backup Log erstellen
echo "$DATE: Backup abgeschlossen ($(git diff --cached --name-only | wc -l) Dateien)" >> "$WORKSPACE/backup.log"

echo ""
echo "================================"
echo "🛡️  Backup abgeschlossen!"
