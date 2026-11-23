#!/usr/bin/env bash
# Remove a skill do Diagran do Claude Code e do Codex.
# Apaga apenas pastas cujo SKILL.md se chama "diagran". Use --all para remover também ~/Diagran/diagran.html.
#   curl -fsSL https://raw.githubusercontent.com/carlos-dataengineer/diagram/main/uninstall.sh | bash
set -euo pipefail
ALL="${DIAGRAN_UNINSTALL_ALL:-0}"
[ "${1:-}" = "--all" ] && ALL=1
for t in "$HOME/.claude/skills/diagran" "${CODEX_HOME:-$HOME/.codex}/skills/diagran" "$HOME/.agents/skills/diagran"; do
  if [ -f "$t/SKILL.md" ] && grep -Eq '^name:[[:space:]]*diagran[[:space:]]*$' "$t/SKILL.md"; then
    rm -rf "$t"; echo "  removido: $t"
  fi
done
APP="$HOME/Diagran/diagran.html"
if [ "$ALL" = "1" ] && [ -f "$APP" ]; then
  rm -f "$APP"; rmdir "$HOME/Diagran" 2>/dev/null || true; echo "  removido: $APP"
elif [ -f "$APP" ]; then
  echo "  mantido: $APP (use --all para remover)"
fi
echo "  Diagran desinstalado."
