# SECA — Auditoria estática MemPalace, parte 6 (2026-11-06)

## Escopo
`mempalace/backends/sqlite_exact.py`, blob SHA `427287c1213de009141a5bcaf24188c1f10b807e`, consultado da linha 1 ao EOF (último bloco 2251–2700 encerra em `__all__`). A leitura não equivale a revisão linha a linha certificada. Fonte: https://github.com/MemPalace/mempalace

## Descobertas
1. `_cursor` usa rollback em erro, commit no sucesso e geração de escrita somente em transações abertas; invalida caches vetorial e nativo após escrita.
2. `_rows` separa filtros SQL parametrizados de filtros Python, preservando semântica de paginação.
3. `get(ids=...)` usa consulta por identificadores; `_hydrate` recupera documentos após ranking, em lotes de até 900 IDs.
4. `lexical_search` prefere FTS e usa pontuação BM25 Python quando FTS não está disponível.
5. Conexões de leitura recebem `PRAGMA query_only=ON`; controle de snapshots observa WAL/SHM e assinaturas do banco.
6. `_init_schema` define tabelas SQLite e WAL; `delete_collection` remove registros e atualiza a geração.

## Pontos para auditoria adicional
- Avaliar cobertura dos testes de concorrência, atualizações de cache e sincronização WAL.
- Examinar limites e robustez do fallback FTS/BM25 e sanitização de tokens.
- Fixar commit e obter manifesto recursivo antes de alegar percentual global.

## Validação
**Nenhum novo teste executado nesta etapa**. A revisão foi exclusivamente estática, sem instalação, importação do MemPalace ou alteração no Termux.

## Estado
Seis arquivos já consultados até EOF: `base.py`, `embedding.py`, `knowledge_graph.py`, `sqlite_exact.py`, `test_knowledge_graph.py`, `test_backend_conformance.py`. Isso não comprova cobertura integral do repositório. Ruflo aguardando.
