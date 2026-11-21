# Arquitetura

## Visão geral

O Diagran é uma aplicação client-side autocontida, entregue como um único HTML. A interface usa HTML/CSS e o motor de desenho usa SVG. O estado do documento é mantido em objetos JavaScript (`nodes` e `edges`).

## Componentes lógicos

1. **Shell da aplicação** — barra superior, biblioteca de formas, canvas, inspetor e barra de status.
2. **Modelo de documento** — nós, conexões, metadados e estado de visualização.
3. **Renderizador SVG** — transforma o modelo em elementos gráficos.
4. **Interação** — seleção, arraste, resize, pan, zoom, edição e atalhos.
5. **Motor de layout** — organização automática horizontal/vertical.
6. **Importação/exportação** — JSON próprio, XML/draw.io, PNG, SVG e Mermaid.
7. **Persistência** — localStorage como padrão; integração opcional com capacidades fornecidas pelo host Claude.

## Modelo conceitual

- `doc.nodes`: elementos gráficos com id, tipo, posição, dimensões, texto e estilo.
- `doc.edges`: conexões com origem, destino, rótulo e estilo.
- `meta`: identificador e nome do diagrama.
- `view`: translação e escala do canvas.

## Decisões de distribuição

A aplicação permanece em um HTML autocontido para facilitar execução e portabilidade. A Skill atua como camada de instalação e geração do artefato, sem acoplar o runtime do editor a um agente específico.
