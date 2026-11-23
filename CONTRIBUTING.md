# Como contribuir

Obrigado pelo interesse! Contribuições de código, documentação, exemplos e relatos de erro são bem-vindas.

## Antes de começar

- Procure uma [issue](https://github.com/carlos-dataengineer/diagram/issues) parecida ou abra uma nova descrevendo o problema ou a proposta.
- Para mudanças grandes, combine a ideia na issue antes de escrever o código.

## Fluxo

1. Faça um fork e crie uma branch (`git checkout -b minha-melhoria`).
2. Edite **só** `src/diagran.html` (os arquivos em `app/` e `skills/diagran/assets/` são gerados).
3. Gere os arquivos e rode os testes:
   ```bash
   python scripts/build.py
   python tests/validate_repo.py
   pip install playwright && python -m playwright install chromium
   python tests/test_smoke.py
   ```
4. Se a interface mudou, atualize as imagens com `python scripts/screenshots.py` e o README.
5. Registre a mudança em `CHANGELOG.md`, na seção da próxima versão.
6. Abra o Pull Request preenchendo o modelo.

## Regras do projeto

- O editor continua **um único HTML, sem build obrigatório e sem dependências** em tempo de execução.
- Exemplos, modelos e imagens usam **apenas dados fictícios**. Nada de nomes de empresas, clientes, tabelas, e-mails ou telefones reais.
- Nada de segredos, tokens ou credenciais em código, testes ou issues.
- `install.ps1` e `uninstall.ps1` precisam ser **ASCII puro, sem BOM** (Windows PowerShell 5.1 e `irm | iex`).
- Funciona no tema claro e no escuro, no desktop e no celular.

## Nova versão (mantenedores)

Atualize `VERSION`, `.claude-plugin/plugin.json`, `.claude-plugin/marketplace.json` e `CHANGELOG.md`, faça o merge na `main` e crie a tag `vX.Y.Z`. O workflow de release publica o ZIP da skill e o HTML.
