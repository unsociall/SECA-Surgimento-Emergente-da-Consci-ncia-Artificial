# SECA — Auditoria estática MemPalace: continuação 2026-11-06

Fonte: https://github.com/MemPalace/mempalace (integração GitHub). Nenhuma instalação, execução ou teste do MemPalace.

## Cobertura observada nesta etapa
| Arquivo | Intervalos consultados acumulados | Blob SHA | Situação |
|---|---|---|---|
| `mempalace/backends/base.py` | 1–1100; retorno termina no final do arquivo | `e4b170e99084d952ce97d22283764aee5f45ef51` | consultado integralmente; auditoria semântica não concluída |
| `mempalace/embedding.py` | 1–1900; retorno 1501–1900 termina em `get_embedder_identity` | `56a54ababc75d6d60370be7f6208db2d94099558` | consultado integralmente; auditoria semântica não concluída |
| `mempalace/knowledge_graph.py` | 1–500 | `49f0ba3377e31ef43b132f2feb3487bad94b58b7` | parcial |

**Importante:** blob SHA identifica conteúdo de arquivo, não fixa commit de repositório. Manifesto de todos os arquivos e percentual global ainda pendentes. Ler trechos não equivale a verificar todas as funções.

## Descobertas novas
1. `embedding.py`: detecção de nomes de modelos digitados incorretamente, evitando troca silenciosa de espaço vetorial; compatibilidade com nomes históricos e `probe_dimension` que só memoriza sondagens bem-sucedidas. Falhas retornam dimensão desconhecida, com nova tentativa posterior.
2. `knowledge_graph.py`: entidades e relações temporais em SQLite; referências à origem documental de cada fato; migração de grafos legados exige revisão explícita e prevê conflitos de fatos e IDs.
3. `knowledge_graph.py`: normalização Unicode NFC e regras de escape para evitar colisões entre identificadores; datas de validade usam intervalos semiabertos `[valid_from,valid_to)`, com tratamento de datas legadas sem hora.
4. `knowledge_graph.py`: valida intervalos invertidos antes de inserir relações.

## Avaliação para SECA
- Adotar **conceitualmente** proveniência de fatos, temporalidade de observações, migração explícita e detecção de conflito entre evidências.
- O grafo documental de entidades **não** equivale à memória neural simulada.
- Não incorporar embeddings pré-treinados no núcleo experimental.
- Verificar custo, licença e testes antes de qualquer proposta de reutilização de código.

## Próxima leitura
`mempalace/knowledge_graph.py` a partir da linha 501, seguida de testes e contratos de backends.

## Estado
MemPalace: leitura estática em andamento; cobertura percentual total indeterminada.
Ruflo: aguardando.
