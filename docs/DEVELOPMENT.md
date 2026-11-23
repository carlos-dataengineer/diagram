# Desenvolvimento

## Requisitos

- Navegador moderno (Chrome, Edge, Firefox ou Safari).
- Python 3.9+ para os scripts de build e testes.
- Playwright para o teste de fumaça e as capturas: `pip install playwright && python -m playwright install chromium`.

## Ciclo de trabalho

1. Edite `src/diagran.html`. Ele é um fragmento: começa em `<title>` e não tem `<html>`/`<body>`.
2. `python scripts/build.py` gera `app/index.html` e os assets da skill.
3. Abra `app/index.html` no navegador para testar.
4. `python tests/validate_repo.py` e `python tests/test_smoke.py`.
5. Se a interface mudou: `python scripts/screenshots.py`.

`python scripts/build.py --check` falha se os arquivos gerados estiverem desatualizados (a CI usa isso).

## Testar a instalação sem mexer no seu ambiente

```bash
HOME="$(mktemp -d)" bash install.sh --no-open
```

## Termos proibidos

Para garantir que nenhum dado real vá a público, rode a validação com os termos que não podem aparecer (eles não ficam gravados no repositório):

```bash
DIAGRAN_PROIBIDOS="termo um,termo dois" python tests/validate_repo.py
```

## Diretrizes

- Sem build obrigatório e sem dependências em tempo de execução.
- Exemplos sempre fictícios.
- Importações inválidas falham sem corromper o diagrama atual.
- Conteúdo vindo de arquivos, IA ou da conta é escapado antes de virar HTML ou SVG.
