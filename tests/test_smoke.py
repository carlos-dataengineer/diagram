#!/usr/bin/env python3
"""Teste de fumaça: abre o Diagran num navegador real e exercita o básico.

Requer: pip install playwright && python -m playwright install chromium
Uso:    python tests/test_smoke.py
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

from playwright.sync_api import sync_playwright

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parent.parent
APP = (ROOT / "app" / "index.html").as_uri()


def current(page) -> dict:
    page.wait_for_timeout(1700)  # o salvamento local é adiado em 1,2 s
    return page.evaluate("JSON.parse(localStorage.getItem('diagran.current')||'null')") or {}


def main() -> int:
    failures: list[str] = []
    with sync_playwright() as p:
        try:
            browser = p.chromium.launch()
        except Exception:
            browser = p.chromium.launch(channel="msedge")

        # 1. Abre sem erros, com o exemplo fictício
        page = browser.new_page(viewport={"width": 1440, "height": 900})
        errors: list[str] = []
        page.on("pageerror", lambda e: errors.append(str(e)))
        page.goto(APP)
        page.wait_for_timeout(800)
        if page.title() != "Diagran":
            failures.append(f"título inesperado: {page.title()!r}")
        count = page.locator("#stCount").inner_text()
        if not count or int(count.split()[0]) < 5:
            failures.append("o diagrama de exemplo não foi desenhado")
        if page.locator("#libList .item").count() < 20:
            failures.append("a biblioteca de formas veio incompleta")

        # 2. Texto → diagrama
        page.locator("#bGen").click()
        page.locator('[data-tab="text"]').click()
        page.locator("#gIn").fill("flowchart LR\nA[Origem demo] --> B[(Bronze)]\nB --> C[(Silver)]\nC --> D[(Gold)]")
        page.locator("#gGo").click()
        doc = current(page).get("doc", {})
        labels = {n.get("text") for n in doc.get("nodes", [])}
        if not {"Origem demo", "Bronze", "Silver", "Gold"} <= labels:
            failures.append(f"texto → diagrama não gerou as formas esperadas: {sorted(map(str, labels))}")
        if len(doc.get("edges", [])) != 3:
            failures.append(f"texto → diagrama gerou {len(doc.get('edges', []))} conexões, esperava 3")

        # 3. Desfazer
        before = len(doc.get("nodes", []))
        page.locator("#svg").click(position={"x": 5, "y": 5})
        page.keyboard.press("Control+z")
        if len(current(page).get("doc", {}).get("nodes", [])) == before:
            failures.append("Ctrl+Z não desfez a geração")

        # 4. Menu de exportação
        page.locator("#bExport").click()
        page.wait_for_timeout(200)
        menu = page.locator("body").inner_text()
        for item in ["PNG", "SVG", "Mermaid"]:
            if item not in menu:
                failures.append(f"menu Exportar sem a opção {item}")
        page.keyboard.press("Escape")

        if errors:
            failures.append("erros na página: " + " | ".join(errors[:3]))
        page.close()

        # 5. Diagrama pronto entregue pela skill (window.DIAGRAN_TEXT)
        page = browser.new_page(viewport={"width": 1280, "height": 800})
        text = "flowchart TB\nI([Início]) --> P{Pedido válido?}\nP -->|sim| F([Fim])"
        page.add_init_script(f"window.DIAGRAN_NAME = 'Teste skill'; window.DIAGRAN_TEXT = {json.dumps(text)};")
        page.goto(APP)
        cur = current(page)
        labels = {n.get("text") for n in cur.get("doc", {}).get("nodes", [])}
        if labels != {"Início", "Pedido válido?", "Fim"}:
            failures.append(f"DIAGRAN_TEXT não foi carregado: {sorted(map(str, labels))}")
        if page.locator("#docName").input_value() != "Teste skill":
            failures.append("DIAGRAN_NAME não virou o nome do diagrama")
        browser.close()

    if failures:
        print("Falhas no teste de fumaça:")
        for f in failures:
            print(f"  - {f}")
        return 1
    print("Teste de fumaça ok.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
