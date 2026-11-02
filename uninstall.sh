#!/usr/bin/env bash
set -euo pipefail
# Remove claude-geo skills, agents and data dir. claude-seo untouched.
rm -rf ~/.zcode/skills/geo ~/.zcode/skills/geo-audit ~/.zcode/skills/geo-page \
       ~/.zcode/skills/geo-llms ~/.zcode/skills/geo-report \
       ~/.claude/skills/geo ~/.claude/skills/geo-audit ~/.claude/skills/geo-page \
       ~/.claude/skills/geo-llms ~/.claude/skills/geo-report
rm -f ~/.zcode/agents/geo-*.md ~/.claude/agents/geo-*.md
rm -rf ~/Library/"Application Support"/claude-geo
echo "✓ claude-geo uninstalled."
