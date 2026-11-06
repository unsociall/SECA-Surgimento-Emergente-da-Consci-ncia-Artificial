# MemPalace — auditoria estática, parte 11 (2026-11-06)

Commit fixado: `f8e35362189bd0a5abf4c0df1dd5bf90ba059176`.
Arquivo `mempalace/backends/sqlite_exact.py` (blob `427287c1213de009141a5bcaf24188c1f10b807e`): linhas 421–850 consultadas nesta etapa; cumulativo 1–850, **parcial**.

## Evidências de código
- `_SQLiteExactHandle` guarda estado de conexão, locks, modos somente leitura/imutável, geração e caches vetoriais/nativos.
- `_write_lock` ordena mutex local antes do bloqueio de escrita interprocessos, prevenindo a liberação antecipada da posse de escrita por outra thread.
- `_cursor` aplica rollback em exceções; incrementa `write_generation` apenas quando há transação de escrita; commit e invalidação dos caches após escrita.
- `_ensure_collection_dimension` rejeita dimensões heterogêneas na mesma coleção.
- `_replace_fts` mantém índice FTS sincronizado com inserção e alteração de documentos.
- `add` e `upsert` exigem embeddings explícitos; `update` de apenas metadados preserva documento, embedding e FTS.
- `get_stored_embedder_identity` registra nome de modelo de embedding; não é compatível como dependência cognitiva do SECA sem reformulação.

## Análise para SECA
Estudar padrões de atomicidade, integridade, sincronização de índices e cache para armazenamento de experiências sem adotar embeddings externos, modelos pré-treinados ou ensino de linguagem. A validade dos bloqueios sob todos os cenários depende de auditoria adicional e testes, proibidos nesta fase.

## Estado
Nenhum arquivo novo declarado integralmente lido. Inventário total não estabelecido, porcentagem global desconhecida; Ruflo não iniciado. Nenhuma instalação, execução ou implementação.
