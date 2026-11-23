# Funcionalidades do Diagran

## Editor
- Área de desenho SVG com grade opcional e encaixe.
- Zoom, ajuste à tela, pan (Espaço, botão do meio, toque) e pinça no celular.
- Seleção individual, múltipla e por área; arraste, redimensionamento e edição inline.
- Desfazer/refazer, copiar/colar, duplicação e ordem (frente/trás).
- Alinhar, distribuir, mesmo tamanho e agrupar em contêiner.

## Elementos
- Retângulo, arredondado, elipse, decisão, entrada/saída, hexágono, banco de dados, fila/stream, documento, nuvem, nota, início/fim, texto, ator, tabela ER e contêiner.
- 12 estilos de cor (inclusive Bronze, Silver e Gold), preenchimento, contorno, fonte, negrito, espessura, tracejado e opacidade.

## Conexões
- Pontos de ancoragem; rotas ortogonais, retas e curvas.
- Setas, cardinalidade (ER), tracejado e rótulos.
- Soltar no vazio cria a próxima etapa já conectada.

## Geração
- Texto estilo Mermaid e declarações de tabelas viram diagrama, com layout automático.
- Colar texto ou JSON no canvas gera ou importa direto.
- IA (descrição em português) no artefato do Claude.
- Diagrama pronto entregue pela skill (`window.DIAGRAN_TEXT`).

## Arquivos
- Salvamento automático e biblioteca de diagramas.
- Importa JSON do Diagran, XML/draw.io e texto Mermaid.
- Exporta PNG (2x), SVG, JSON e Mermaid.

## Distribuição
- Skill para Claude Code, Codex e agentes; plugin do Claude Code.
- Instalação e desinstalação em um comando (Windows, macOS, Linux).
