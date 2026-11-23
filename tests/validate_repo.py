#!/usr/bin/env python3
"""Validações estáticas do repositório (sem navegador).

Confere: manifesto da skill, manifestos do plugin, versão consistente,
arquivos gerados presentes, instaladores em ASCII sem BOM, links e imagens do README
e, opcionalmente, termos proibidos (dados reais que não podem ir a público).

Termos proibidos ficam fora do repositório: passe-os em DIAGRAN_PROIBIDOS,
separados por vírgula. Ex.: DIAGRAN_PROIBIDOS="empresa x,tabela_real" python tests/validate_repo.py
"""
from __future__ import annotations

import json
import os
import re
import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parent.parent
SKILL_DIR = ROOT / "skills" / "diagran"
errors: list[str] = []


def check(cond: bool, msg: str) -> None:
    if not cond:
        errors.append(msg)


# Skill
skill = (SKILL_DIR / "SKILL.md").read_text(encoding="utf-8")
m = re.match(r"^---\n(.*?)\n---\n", skill, re.S)
check(bool(m), "SKILL.md sem frontmatter YAML")
if m:
    front = dict(re.findall(r"^(\w+):\s*(.+)$", m.group(1), re.M))
    check(front.get("name") == "diagran", "SKILL.md: name deve ser 'diagran'")
    desc = front.get("description", "")
    check(20 <= len(desc) <= 1024, "SKILL.md: description deve ter entre 20 e 1024 caracteres")
for ref in re.findall(r"`((?:assets|references)/[^`]+)`", skill):
    check((SKILL_DIR / ref).exists(), f"SKILL.md cita {ref}, que não existe")
check((SKILL_DIR / "agents" / "openai.yaml").exists(), "falta skills/diagran/agents/openai.yaml (Codex)")

# Plugin e versão
version = (ROOT / "VERSION").read_text(encoding="utf-8").strip()
plugin = json.loads((ROOT / ".claude-plugin/plugin.json").read_text(encoding="utf-8"))
market = json.loads((ROOT / ".claude-plugin/marketplace.json").read_text(encoding="utf-8"))
check(plugin.get("name") == "diagran", "plugin.json: name deve ser 'diagran'")
check(plugin.get("version") == version, f"plugin.json: versão {plugin.get('version')} difere de VERSION {version}")
entries = [p for p in market.get("plugins", []) if p.get("name") == "diagran"]
check(len(entries) == 1, "marketplace.json: precisa de uma entrada 'diagran'")
if entries:
    check(entries[0].get("version") == version, "marketplace.json: versão difere de VERSION")
check(f"[{version}]" in (ROOT / "CHANGELOG.md").read_text(encoding="utf-8"), f"CHANGELOG.md sem a versão {version}")

# Arquivos gerados
for rel in ["app/index.html", "skills/diagran/assets/diagran.html", "skills/diagran/assets/diagran-artifact.html"]:
    p = ROOT / rel
    check(p.exists(), f"{rel} não existe (rode python scripts/build.py)")
    if p.exists():
        check("<title>Diagran</title>" in p.read_text(encoding="utf-8"), f"{rel} sem o título Diagran")
artifact = (SKILL_DIR / "assets" / "diagran-artifact.html").read_text(encoding="utf-8")
check(not re.search(r"<!doctype|<html|<body", artifact, re.I), "diagran-artifact.html não pode ter doctype/html/body")

# Instaladores
for rel in ["install.ps1", "uninstall.ps1"]:
    raw = (ROOT / rel).read_bytes()
    check(not raw.startswith(b"\xef\xbb\xbf"), f"{rel} não pode ter BOM (quebra o irm | iex)")
    check(all(b < 128 for b in raw), f"{rel} precisa ser ASCII puro (Windows PowerShell 5.1)")
for rel in ["install.sh", "uninstall.sh"]:
    raw = (ROOT / rel).read_bytes()
    check(raw.startswith(b"#!/usr/bin/env bash"), f"{rel} sem shebang")
    check(b"\r\n" not in raw, f"{rel} precisa de quebras de linha LF")

# README: imagens e links locais
readme = (ROOT / "README.md").read_text(encoding="utf-8")
for img in re.findall(r'src="(docs/images/[^"]+)"', readme) + re.findall(r"!\[[^\]]*\]\((docs/images/[^)]+)\)", readme):
    check((ROOT / img).exists(), f"README cita {img}, que não existe")
for link in re.findall(r"\]\(((?!https?://|#|mailto:)[^)\s]+)\)", readme):
    check((ROOT / link.split("#")[0]).exists(), f"README aponta para {link}, que não existe")

# Termos proibidos (passados por variável de ambiente, nunca gravados aqui)
terms = [t.strip().lower() for t in os.environ.get("DIAGRAN_PROIBIDOS", "").split(",") if t.strip()]
if terms:
    for p in ROOT.rglob("*"):
        if ".git" in p.parts or not p.is_file() or p.suffix.lower() in {".png", ".jpg", ".zip"}:
            continue
        text = p.read_text(encoding="utf-8", errors="ignore").lower()
        for t in terms:
            if t in text:
                errors.append(f"termo proibido em {p.relative_to(ROOT).as_posix()}: {t!r}")

if errors:
    print("Falhas:")
    for e in errors:
        print(f"  - {e}")
    sys.exit(1)
print("Repositório válido." + (f" ({len(terms)} termos proibidos conferidos)" if terms else ""))
