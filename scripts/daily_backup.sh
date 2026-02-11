#!/bin/bash
# Daily Agent Backup Script
# Backs up all essential agent files to git repository
# Run at: 10:00 AM daily

set -e

# Configuration
WORKSPACE="/home/enric/.openclaw/workspace"
GIT_REPO="git@github.com:nric/myclawbot.git"
BACKUP_TIME=$(date +"%Y-%m-%d %H:%M:%S")
DATE=$(date +"%Y-%m-%d")

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo "🛡️  Agent Backup - $BACKUP_TIME"
echo "================================"

cd "$WORKSPACE"

# Check if git is initialized
if [ ! -d ".git" ]; then
    echo -e "${RED}✗ Git not initialized${NC}"
    exit 1
fi

# Ensure correct remote
current_remote=$(git remote get-url origin 2>/dev/null || echo "")
if [ "$current_remote" != "$GIT_REPO" ]; then
    echo -e "${YELLOW}⚠ Setting remote to $GIT_REPO${NC}"
    git remote remove origin 2>/dev/null || true
    git remote add origin "$GIT_REPO"
fi

# Check for changes
echo "📋 Checking for changes..."
git add -A

# Check if there are changes to commit
if git diff --cached --quiet; then
    echo -e "${GREEN}✓ No changes to backup${NC}"
    exit 0
fi

# Show what's being backed up
echo "📦 Files to backup:"
git diff --cached --name-only | head -20
if [ $(git diff --cached --name-only | wc -l) -gt 20 ]; then
    echo "... and $(($(git diff --cached --name-only | wc -l) - 20)) more files"
fi

# Create backup commit
echo "💾 Creating backup commit..."
git commit -m "Daily backup - $DATE

- Skills: $(git diff --cached --name-only | grep -c 'skills/' || echo 0) files
- Memory: $(git diff --cached --name-only | grep -c 'memory/' || echo 0) files  
- Config: $(git diff --cached --name-only | grep -c '\.(json|md)$' || echo 0) files

Auto-backup at 10:00 AM"

# Push to remote
echo "🚀 Pushing to remote..."
if git push origin main 2>/dev/null || git push origin master 2>/dev/null; then
    echo -e "${GREEN}✓ Backup successful!${NC}"
    echo "📍 Repository: $GIT_REPO"
    echo "🕐 Next backup: Tomorrow 10:00 AM"
else
    echo -e "${RED}✗ Push failed - check SSH key and repository access${NC}"
    exit 1
fi

# Create backup log
echo "$DATE: Backup completed ($(git diff --cached --name-only | wc -l) files)" >> "$WORKSPACE/backup.log"

echo ""
echo "================================"
echo "🛡️  Backup complete!"
