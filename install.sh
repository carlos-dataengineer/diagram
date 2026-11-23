#!/usr/bin/env bash
# Instala o Diagran: a skill para Claude Code e Codex, e a ferramenta pronta no computador.
#
#   curl -fsSL https://raw.githubusercontent.com/carlos-dataengineer/diagram/main/install.sh | bash
#
# Opções (também como variáveis de ambiente):
#   --no-open       não abre o navegador          DIAGRAN_NO_OPEN=1
#   --skip-claude   não instala no Claude Code    DIAGRAN_SKIP_CLAUDE=1
#   --skip-codex    não instala no Codex          DIAGRAN_SKIP_CODEX=1
#   --ref <ref>     branch ou tag (padrão: main)  DIAGRAN_REF=v1.0.0
set -euo pipefail

REPO="carlos-dataengineer/diagram"
NO_OPEN="${DIAGRAN_NO_OPEN:-0}"
SKIP_CLAUDE="${DIAGRAN_SKIP_CLAUDE:-0}"
SKIP_CODEX="${DIAGRAN_SKIP_CODEX:-0}"
REF="${DIAGRAN_REF:-main}"

while [ $# -gt 0 ]; do
  case "$1" in
    --no-open) NO_OPEN=1 ;;
    --skip-claude) SKIP_CLAUDE=1 ;;
    --skip-codex) SKIP_CODEX=1 ;;
    --ref) shift; REF="${1:?informe a branch ou tag}" ;;
    -h|--help) sed -n '2,11p' "$0"; exit 0 ;;
    *) echo "Opção desconhecida: $1" >&2; exit 1 ;;
  esac
  shift
done

step() { printf '  \033[36m>\033[0m %s\n' "$1"; }
ok()   { printf '  \033[32m✓\033[0m %s\n' "$1"; }
warn() { printf '  \033[33m!\033[0m %s\n' "$1" >&2; }

printf '\n  Diagran · editor de fluxogramas, pipelines e modelos ER\n\n'

# 1. Origem dos arquivos
TMP=""
cleanup() { if [ -n "$TMP" ]; then rm -rf "$TMP"; fi; }
trap cleanup EXIT

SCRIPT_DIR=""
if [ -n "${BASH_SOURCE[0]:-}" ] && [ -f "${BASH_SOURCE[0]}" ]; then
  SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
fi

if [ -n "$SCRIPT_DIR" ] && [ -f "$SCRIPT_DIR/skills/diagran/SKILL.md" ]; then
  ROOT="$SCRIPT_DIR"
  step "Usando os arquivos locais em $ROOT"
else
  command -v curl >/dev/null || { echo "Instale o curl e tente de novo." >&2; exit 1; }
  command -v tar >/dev/null || { echo "Instale o tar e tente de novo." >&2; exit 1; }
  TMP="$(mktemp -d)"
  case "$REF" in v[0-9]*) KIND="tags" ;; *) KIND="heads" ;; esac
  step "Baixando $REPO ($REF)"
  curl -fsSL "https://codeload.github.com/$REPO/tar.gz/refs/$KIND/$REF" | tar -xz -C "$TMP"
  ROOT="$(find "$TMP" -mindepth 1 -maxdepth 1 -type d | head -n 1)"
  [ -f "$ROOT/skills/diagran/SKILL.md" ] || { echo "O pacote baixado não tem skills/diagran/SKILL.md." >&2; exit 1; }
fi
SKILL_SRC="$ROOT/skills/diagran"

# 2. Skill
install_skill() {
  local target="$1" label="$2"
  if [ -e "$target" ]; then
    if [ -f "$target/SKILL.md" ] && grep -Eq '^name:[[:space:]]*diagran[[:space:]]*$' "$target/SKILL.md"; then
      rm -rf "$target"
    else
      warn "$target já existe e não parece ser o Diagran. Pulei $label para não apagar nada."
      return 0
    fi
  fi
  mkdir -p "$(dirname "$target")"
  cp -R "$SKILL_SRC" "$target"
  ok "Skill instalada para $label em $target"
}

INSTALLED=""
if [ "$SKIP_CLAUDE" != "1" ]; then
  install_skill "$HOME/.claude/skills/diagran" "Claude Code"
  INSTALLED="$INSTALLED claude"
fi
if [ "$SKIP_CODEX" != "1" ]; then
  install_skill "${CODEX_HOME:-$HOME/.codex}/skills/diagran" "Codex"
  install_skill "$HOME/.agents/skills/diagran" "agentes (pasta compartilhada)"
  INSTALLED="$INSTALLED codex"
fi

# 3. Ferramenta pronta
APP_DIR="$HOME/Diagran"
APP_FILE="$APP_DIR/diagran.html"
mkdir -p "$APP_DIR"
cp "$SKILL_SRC/assets/diagran.html" "$APP_FILE"
ok "Ferramenta gerada em $APP_FILE"

if [ "$NO_OPEN" != "1" ]; then
  if command -v open >/dev/null 2>&1; then open "$APP_FILE" && ok "Aberta no navegador"
  elif command -v xdg-open >/dev/null 2>&1; then (xdg-open "$APP_FILE" >/dev/null 2>&1 &) && ok "Aberta no navegador"
  else warn "Não encontrei como abrir o navegador. Abra manualmente: $APP_FILE"
  fi
fi

# 4. Próximos passos
printf '\n  Pronto. Como usar:\n'
case "$INSTALLED" in *claude*) printf '    Claude Code  peça "abrir o Diagran" ou digite /diagran (gera o artefato)\n' ;; esac
case "$INSTALLED" in *codex*) printf '    Codex        peça "abra o Diagran" ou digite $diagran\n' ;; esac
printf '    Navegador    %s\n\n' "$APP_FILE"
printf '  Abra uma nova conversa para o agente reconhecer a skill.\n\n'
