# SECA — auditoria estática MemPalace, parte 39 (2026-11-14)

## Escopo e evidência
- Repositório de origem: https://github.com/MemPalace/mempalace
- Commit fixado: `f8e35362189bd0a5abf4c0df1dd5bf90ba059176`
- Arquivo: `mempalace/backends/sqlite_exact.py`
- Blob SHA verificado: `427287c1213de009141a5bcaf24188c1f10b807e`
- Tamanho reportado pela árvore Git: 95.869 bytes.
- Leitura: arquivo integral solicitado e inspecionado estaticamente em faixas contíguas 1–2270; sem execução de código de terceiros.
- Inventário: árvore recursiva não truncada com 851 blobs, incluindo um symlink (modo 120000). O manifesto de caminhos/SHA é separado da comprovação de leitura.
- Cobertura global integral: NÃO CERTIFICADA. Relatórios anteriores exigem reconciliação por caminho, SHA e evidência; não calcular porcentagem.
- Testes executados: 0.

## Arquitetura e algoritmos
1. `SQLiteExactBackend` mantém handles de leitura/escrita, esquema, coleções, cache, locks e detecção do banco. `SQLiteExactCollection` expõe add/upsert/update/delete/get/query/get_recent, facetas, busca lexical, manutenção e health.
2. Vetores float32 são persistidos como blobs; distância cosseno exata usa NumPy e fallback float64 para operações intermediárias inseguras. A busca exata varre candidatos; não há índice ANN. Isso é uma técnica de armazenamento/recuperação, NÃO um mecanismo de consciência.
3. Consultas vetoriais validam dimensão, mantêm desempate estável, hidratam documentos depois de selecionar IDs e reutilizam cache por coleção.
4. Filtros simples `$eq`, `$in` e `$and` são parametrizados e enviados ao SQL; filtros complexos seguem avaliação Python. Há índices de locus (wing/room/hall), source_file e filed_at.
5. `get_recent` implementa caminho SQL para casos filtráveis e fallback para o contrato base; ordena timestamps por `recency_key`, com cuidado para formatos UTC diferentes. É necessário examinar `timeutil.py` e testes de datas para certificar a correção.
6. Escritas usam `_cursor(write=True)`, `mine_palace_lock`, RLock, rollback em exceção, commit e incremento de `meta.write_generation` na transação. Isso é mais forte que a implementação padrão read-modify-write de `base.py`, mas ainda não comprova atomicidade sob todos os cenários de falha.
7. Leitura somente leitura diferencia WAL/SHM ativo de abertura immutable; detecta mudança de snapshot via assinatura de arquivo, cabeçalho e geração de escrita. A conexão aplica `PRAGMA query_only=ON`.
8. `maintenance_state` expõe páginas, freelist e token de consistência; `run_maintenance` permite ANALYZE e VACUUM. `health()` da coleção apenas verifica se o handle está aberto, não executa verificação profunda de integridade.

## Riscos, limites e validações pendentes
- `_as_vector_array` verifica forma e tamanho, mas não rejeita explicitamente NaN/Inf; conferir `validate_write_batch` e testes antes de concluir se valores não finitos podem persistir.
- `_json_loads` converte JSON inválido em dicionário vazio: risco de ocultar corrupção de metadados; investigar caminhos de detecção e logs.
- `_equality_where_sql` usa nomes de campos restritos por regex e parâmetros para valores; não atribuir garantia de segurança global sem auditoria dos outros pontos de SQL dinâmico.
- `_cursor` não abre `BEGIN` explicitamente; investigar semântica de transação de cada operação, DDL, falhas e concorrência entre processos.
- O mecanismo de snapshot depende de assinatura, geração e sidecars; validar estaticamente cenários de race condition, WAL e recuperação cruzando `_magic.py` e testes.
- Não foi executado nenhum teste; não há comprovação dinâmica de desempenho, segurança ou integridade.

## Relevância ao SECA (somente conceitual)
- Candidatos a estudo futuro: contratos de memória episódica, transações de eventos, versões de snapshot, integridade, isolamento de experiências, recência temporal e métricas de manutenção.
- Não importar embeddings pré-treinados, modelos linguísticos, dependências de serviços externos, aprendizagem de linguagem nem mecanismos de orquestração para o núcleo biológico offline.
- Nenhuma implementação ou instalação autorizada nesta fase.

## Próximas ações
1. Reconciliar o manifesto dos 851 blobs com as partes 1–39, distinguindo `verificado`, `parcial`, `pendente` e `não textual`, com evidência e SHA.
2. Auditar testes de SQLiteExact e dependências diretas (`_filters.py`, `timeutil.py`, `stored_text.py`, `palace.py`), verificando contratos, concorrência e licença.
3. Iniciar Ruflo somente após cobertura integral certificada do MemPalace.
