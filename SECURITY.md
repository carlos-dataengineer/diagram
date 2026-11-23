# Política de segurança

## Versões suportadas

Só a versão mais recente (branch `main` e a última tag) recebe correções.

## Como relatar uma vulnerabilidade

**Não abra uma issue pública.** Use o [relato privado de vulnerabilidades](https://github.com/carlos-dataengineer/diagram/security/advisories/new) do GitHub, com:

- o que acontece e o impacto;
- passos para reproduzir (de preferência com um diagrama ou arquivo de exemplo fictício);
- versão e ambiente (navegador, Claude, Codex, sistema).

A resposta inicial vem em até 7 dias.

## Escopo

- O editor (`src/diagran.html`): injeção de HTML ou script via importação de JSON, draw.io, Mermaid ou rótulos.
- Os instaladores (`install.*`, `uninstall.*`): apagar ou sobrescrever arquivos fora das pastas do Diagran.
- A skill (`skills/diagran`): instruções que levem o agente a expor dados ou executar algo não pedido.

## Boas práticas para quem usa

- Não coloque senhas, tokens ou dados pessoais em diagramas que serão compartilhados.
- Antes de rodar o instalador, você pode ler o script: ele só copia arquivos para `~/.claude/skills`, `~/.codex/skills`, `~/.agents/skills` e `~/Diagran`.
