#!/usr/bin/env python3
"""Gera as capturas de tela do README em docs/images/.

Todas usam os modelos prontos do Diagran, com dados fictícios.

Requer: pip install playwright && python -m playwright install chromium
Uso:    python scripts/screenshots.py
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

from playwright.sync_api import Page, sync_playwright

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parent.parent
APP = (ROOT / "app" / "index.html").as_uri()
OUT = ROOT / "docs" / "images"

TEMPLATE = {"pedidos": 1, "medallion": 2, "decisao": 3, "er": 4, "ingestao": 5}

CRM_TEXT = """flowchart TB
I([Início]) --> F[/Formulário do site demo/]
F --> V{Contato válido?}
V -->|não| D[Descartar e registrar motivo]
V -->|sim| S{Cliente já existe?}
S -->|sim| A[Atualizar cadastro]
S -->|não| N[Criar cliente demo]
A --> E{{API de e-mail fictícia}}
N --> E
E --> FIM([Fim])
D --> FIM"""


def open_app(page: Page) -> None:
    page.goto(APP)
    page.wait_for_timeout(900)


def template(page: Page, key: str) -> None:
    page.evaluate(f"newDiagram(TEMPLATES[{TEMPLATE[key]}])")
    page.wait_for_timeout(500)
    page.evaluate("sel.clear();renderProps();requestRender()")
    page.wait_for_timeout(300)


def shot(page: Page, name: str, **kw) -> None:
    page.screenshot(path=str(OUT / f"{name}.png"), **kw)
    print(f"gerado: docs/images/{name}.png")


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    with sync_playwright() as p:
        try:
            browser = p.chromium.launch()
        except Exception:
            browser = p.chromium.launch(channel="msedge")

        def new_page(dark: bool = False, w: int = 1440, h: int = 860, **kw) -> Page:
            ctx = browser.new_context(viewport={"width": w, "height": h}, device_scale_factor=1,
                                      color_scheme="dark" if dark else "light", locale="pt-BR", **kw)
            pg = ctx.new_page()
            open_app(pg)
            return pg

        # Modelos prontos
        page = new_page()
        shot(page, "pedidos")
        for key in ["medallion", "decisao", "er"]:
            template(page, key)
            shot(page, key)

        # Propriedades de uma forma selecionada
        template(page, "medallion")
        page.evaluate("sel=new Set([doc.nodes.find(n=>/Silver/.test(n.text)).id]);renderProps();requestRender()")
        page.wait_for_timeout(300)
        shot(page, "propriedades")

        # Janela Novo diagrama
        page.locator("#bFiles").click()
        page.wait_for_timeout(300)
        shot(page, "meus-diagramas")
        page.locator("#fNew").click()
        page.wait_for_timeout(300)
        shot(page, "novo")
        page.keyboard.press("Escape")

        # Gerar a partir de texto
        page.locator("#bGen").click()
        page.locator('[data-tab="text"]').click()
        page.locator("#gIn").fill(CRM_TEXT)
        page.wait_for_timeout(200)
        shot(page, "gerar")
        page.locator("#gGo").click()
        page.evaluate("meta.name='Cadastro de clientes (demo)';document.querySelector('#docName').value=meta.name")
        page.wait_for_timeout(3500)  # espera o aviso sumir
        page.evaluate("sel.clear();renderProps();requestRender()")
        page.wait_for_timeout(300)
        shot(page, "gerado")

        # Menu Exportar
        page.locator("#bExport").click()
        page.wait_for_timeout(300)
        shot(page, "exportar")
        page.keyboard.press("Escape")

        # Menu Organizar
        page.locator("#bLayout").click()
        page.wait_for_timeout(300)
        shot(page, "organizar")
        page.keyboard.press("Escape")
        page.context.close()

        # Tema escuro
        page = new_page(dark=True)
        template(page, "ingestao")
        shot(page, "ingestao")
        page.context.close()

        # Celular
        page = new_page(w=390, h=844, is_mobile=True, has_touch=True)
        template(page, "decisao")
        shot(page, "celular")
        page.context.close()

        # Diagrama pronto entregue pela skill
        ctx = browser.new_context(viewport={"width": 1440, "height": 860}, device_scale_factor=1, locale="pt-BR")
        page = ctx.new_page()
        txt = "flowchart LR\nAPP[App de pedidos demo] --> K[Fila de eventos]\nK --> J{{Job de ingestão}}\nJ --> B[(Bronze)]\nB --> S[(Silver)]\nS --> Q{Qualidade ok?}\nQ -->|sim| G[(Gold)]\nQ -.->|não| R[/Relatório de rejeitados/]\nG --> P[Painel de vendas demo]"
        page.add_init_script(f"window.DIAGRAN_NAME='Pipeline pedido pelo agente';window.DIAGRAN_TEXT={json.dumps(txt)};")
        open_app(page)
        page.wait_for_timeout(400)
        page.evaluate("sel.clear();renderProps();requestRender()")
        page.wait_for_timeout(300)
        page.evaluate("zoomAt(1.55)")
        page.wait_for_timeout(3000)
        shot(page, "skill-diagrama-pronto")
        ctx.close()
        browser.close()
    return 0


if __name__ == "__main__":
    sys.exit(main())
