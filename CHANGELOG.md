# Changelog

Todas as mudanças relevantes deste projeto. O formato segue o [Keep a Changelog](https://keepachangelog.com/pt-BR/1.1.0/) e o versionamento segue o [SemVer](https://semver.org/lang/pt-BR/).

## [1.1.0] - 2026-11-23

### Adicionado
- Instalação em um comando para Claude Code e Codex (`install.ps1` e `install.sh`), com desinstaladores.
- A instalação gera a ferramenta em `~/Diagran/diagran.html` e abre no navegador.
- Skill `skills/diagran` com instruções para publicar o artefato no Claude (IA, downloads e diagramas salvos na conta) e para abrir no Codex; `agents/openai.yaml` para o Codex.
- Diagrama pronto entregue pelo agente: `window.DIAGRAN_TEXT` e `window.DIAGRAN_NAME` abrem o editor já com o desenho.
- Referência da sintaxe texto → diagrama em `skills/diagran/references/SINTAXE.md`.
- Plugin e marketplace do Claude Code em `.claude-plugin/`.
- `src/diagran.html` como fonte única e `scripts/build.py` para gerar `app/` e os assets da skill.
- Testes: `tests/validate_repo.py` (estrutura, versões, instaladores, README, termos proibidos) e `tests/test_smoke.py` (navegador real).
- CI com validação, teste de fumaça e instalação em Ubuntu, macOS e Windows; release automática por tag.
- README reescrito com instalação, casos de uso, capturas novas, atalhos e perguntas frequentes.

### Alterado
- Modelo de exemplo "Fluxo de pedidos fictícios" com domínios e relatórios de um e-commerce fictício.
- `SKILL.md` da raiz movido para `skills/diagran/SKILL.md`.

## [1.0.0] - 2026-11-23

### Adicionado
- Organização inicial do projeto Diagran para distribuição como Skill.
- Aplicação preservada como artefato HTML autocontido.
- Exemplos e modelos demonstrativos com dados fictícios.
- Documentação inicial, diretrizes de contribuição, privacidade e segurança.
