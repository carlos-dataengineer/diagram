#!/usr/bin/env python3
"""Gera os arquivos distribuídos do Diagran a partir de src/diagran.html.

Saídas:
  app/index.html                                 documento completo, abre direto no navegador
  skills/diagran/assets/diagran.html             cópia do documento completo (usada pela skill)
  skills/diagran/assets/diagran-artifact.html    fragmento para publicar como artefato no Claude

Uso:
  python scripts/build.py          gera os arquivos
  python scripts/build.py --check  falha se os arquivos gerados estiverem desatualizados
"""
from __future__ import annotations

import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "src" / "diagran.html"

OUT_APP = ROOT / "app" / "index.html"
OUT_SKILL = ROOT / "skills" / "diagran" / "assets" / "diagran.html"
OUT_ARTIFACT = ROOT / "skills" / "diagran" / "assets" / "diagran-artifact.html"

# Mesmo esqueleto que o Claude usa ao publicar um artefato: o arquivo abre igual
# no navegador e, se for republicado, o Claude reconhece e não aninha o esqueleto.
SKELETON_HEAD = (
    '<!doctype html><html lang="pt-BR"><head><meta charset=utf8>'
    '<meta name=viewport content="width=device-width,initial-scale=1,viewport-fit=cover">'
    "<style>:root{color-scheme:light;box-sizing:border-box;padding-top:env(safe-area-inset-top,0px);"
    "padding-bottom:env(safe-area-inset-bottom,0px)}html{scroll-padding-top:env(safe-area-inset-top,0px)}"
    "body{margin:0;padding:0;font:14px -apple-system,BlinkMacSystemFont,sans-serif;background:#fff;color:#000}"
    "img{max-width:100%}[hidden]:not([hidden=until-found i]){display:none!important}</style></head><body>\n"
)
SKELETON_TAIL = "\n</body></html>\n"


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8").replace("\r\n", "\n")


def build() -> dict[Path, str]:
    fragment = read(SRC).strip("\n")
    if not fragment.startswith("<title>Diagran</title>"):
        raise SystemExit(f"{SRC} deve começar com <title>Diagran</title> (é um fragmento, sem <html>/<body>).")
    full = SKELETON_HEAD + fragment + SKELETON_TAIL
    return {OUT_APP: full, OUT_SKILL: full, OUT_ARTIFACT: fragment + "\n"}


def main() -> int:
    check = "--check" in sys.argv
    stale = []
    for path, content in build().items():
        current = path.read_text(encoding="utf-8") if path.exists() else None
        if current == content:
            continue
        if check:
            stale.append(path.relative_to(ROOT).as_posix())
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding="utf-8", newline="\n")
            print(f"gerado: {path.relative_to(ROOT).as_posix()}")
    if stale:
        print("Arquivos desatualizados. Rode: python scripts/build.py")
        for s in stale:
            print(f"  - {s}")
        return 1
    if check:
        print("Arquivos gerados em dia.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
