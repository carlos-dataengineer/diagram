# Arquitetura

## Visão geral

O Diagran é uma aplicação 100% client-side, entregue como um único HTML. A interface usa HTML/CSS e o desenho usa SVG. O estado do documento vive em objetos JavaScript (`nodes` e `edges`).

## Componentes

1. **Shell da aplicação**: barra superior, biblioteca de formas, canvas, inspetor e barra de status.
2. **Modelo do documento**: nós, conexões, metadados e estado de visualização.
3. **Renderizador SVG**: transforma o modelo em elementos gráficos.
4. **Interação**: seleção, arraste, redimensionamento, pan, zoom, edição e atalhos.
5. **Motor de layout**: organização automática em camadas, horizontal ou vertical.
6. **Parser de texto**: sintaxe estilo Mermaid e declarações de tabela viram formas e conexões.
7. **Importação/exportação**: JSON próprio, XML/draw.io, PNG, SVG e Mermaid.
8. **Persistência**: `localStorage` por padrão; no artefato do Claude, também na conta da pessoa.

## Modelo de dados

- `doc.nodes`: `{id, type, x, y, w, h, text, style, fields?}`.
- `doc.edges`: `{id, from, to, text, fromSide?, toSide?, style}`.
- `meta`: `{id, name}`.
- `view`: translação e escala do canvas.

Chaves no `localStorage`: `diagran.current` (diagrama aberto), `diagran.lib` (biblioteca), `diagran.settings` (grade, encaixe) e `diagran.seed` (exemplo inicial já mostrado).

## Capacidades do Claude (opcionais)

Quando publicado como artefato, o editor pede ao Claude, via `window.claude.use(nome)`:

| Capacidade | Uso | Sem ela |
|---|---|---|
| `sample` | Aba **Descrever para a IA** | A aba avisa que a IA está indisponível |
| `downloads` | Salvar PNG/SVG/JSON pelo Claude | Download comum do navegador |
| `db` + `user` | Biblioteca na conta, em `data/users/<id>/diagrams` (privado por pessoa) | Só `localStorage` |

Cada capacidade é independente: a falta de uma não afeta as outras.

## Distribuição

```text
src/diagran.html --build.py--> app/index.html                               (navegador)
                           +-> skills/diagran/assets/diagran.html           (Codex, terminal)
                           +-> skills/diagran/assets/diagran-artifact.html  (artefato do Claude)
```

`install.ps1` e `install.sh` copiam `skills/diagran` para as pastas de skills do Claude Code, do Codex e de agentes, e geram `~/Diagran/diagran.html`. A skill nunca reescreve o editor: entrega sempre os arquivos de `assets/`.

### Diagrama pronto

Antes do primeiro `<script>`, a skill pode injetar:

```html
<script>window.DIAGRAN_NAME = "Nome"; window.DIAGRAN_TEXT = "flowchart LR\nA --> B";</script>
```

Na inicialização, o editor cria um diagrama novo a partir desse texto, com o mesmo parser da janela **Gerar**.
