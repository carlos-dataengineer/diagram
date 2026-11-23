# Sintaxe de texto → diagrama

O Diagran lê um texto no estilo Mermaid, monta as formas e as conexões e organiza o layout sozinho.
Uma instrução por linha.

## Exemplo

```text
flowchart LR
API[API Atlas] --> B[(Bronze)]
B -->|limpeza e dedup| S[(Silver)]
S --> Q{Dados válidos?}
Q -->|sim| G[(Gold)]
Q -.->|não| L[/Log de rejeitados/]
G --> D[Painel de vendas]
tabela eventos: id_evento bigint PK, email_demo string, dt_criacao timestamp
```

## Direção

| Linha | Efeito |
|---|---|
| `flowchart LR` ou `graph LR` | Horizontal (padrão) |
| `flowchart TB` ou `flowchart TD` | Vertical |

## Formas

| Escreva | Forma |
|---|---|
| `A[Texto]` | Retângulo |
| `A(Texto)` | Retângulo arredondado |
| `A([Início])` | Início/Fim |
| `A{Decisão?}` | Losango |
| `A[(Banco)]` | Cilindro (banco, camada) |
| `A((Texto))` | Elipse |
| `A{{API}}` | Hexágono (serviço, job, API) |
| `A[/Arquivo/]` | Paralelogramo (entrada/saída) |
| `A>Documento]` | Documento |

O identificador (`A`) é usado para ligar as formas; o rótulo é o que aparece. Depois de declarada, a forma pode ser citada só pelo identificador.

Sem forma indicada, o Diagran escolhe pela palavra: termina com `?` → decisão; `início`/`fim` → terminador; `bronze`, `silver`, `gold`, `banco`, `delta`, `lake`, `warehouse`, `dw` → cilindro; `kafka`, `fila`, `queue`, `stream` → fila; `api`, `serviço`, `endpoint` → hexágono; `csv`, `arquivo`, `relatório`, `planilha`, `pdf` → documento; `usuário`, `cliente`, `analista` → ator. Bronze, Silver e Gold ganham as cores das camadas.

## Conexões

| Escreva | Resultado |
|---|---|
| `A --> B`, `A -> B`, `A → B`, `A ==> B` | Seta |
| `A --- B` | Linha sem seta |
| `A -.-> B` | Seta tracejada |
| `A -.- B` | Linha tracejada |
| `A -->\|rótulo\| B` ou `A -- rótulo --> B` | Seta com rótulo |
| `A --> B & C` | Uma origem, vários destinos |
| `A --> B --> C` | Encadeamento |

## Tabelas (modelo ER)

```text
tabela clientes: id_cliente bigint PK, nome_demo string, dt_cadastro date
tabela pedidos: id_pedido bigint PK, id_cliente bigint FK, valor decimal(12,2)
pedidos --> clientes
```

Uma ligação entre duas tabelas vira relação com cardinalidade (muitos → um).

## Ignorado

Linhas começando com `%%` ou `//`, e as instruções Mermaid `classDef`, `class`, `style`, `linkStyle`, `subgraph` e `end`.

## Dicas para um bom diagrama

- Até ~20 formas por diagrama; divida em dois se passar disso.
- Rótulos de 1 a 4 palavras. Detalhes vão no rótulo da conexão.
- Use `-.->` para fluxos opcionais, de erro ou assíncronos.
