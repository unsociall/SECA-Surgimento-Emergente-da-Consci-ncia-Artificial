# SECA — Auditoria MemPalace, parte 8: testes SQLite completos e commit fixado

Data: 2026-11-06.

## Commit de referência
MemPalace: `f8e35362189bd0a5abf4c0df1dd5bf90ba059176`.

As sete leituras anteriores foram revalidadas por SHA de blob com `fetch_file(ref=commit)`; os hashes coincidem com as leituras anteriores. Isso permite atribuir as leituras já realizadas ao commit fixado, sem presumir cobertura de arquivos não listados.

## Manifesto parcial, verificável

| Arquivo | SHA de blob | Leitura |
|---|---|---|
| `mempalace/backends/base.py` | `e4b170e99084d952ce97d22283764aee5f45ef51` | até EOF |
| `mempalace/embedding.py` | `56a54ababc75d6d60370be7f6208db2d94099558` | até EOF |
| `mempalace/knowledge_graph.py` | `49f0ba3377e31ef43b132f2feb3487bad94b58b7` | até EOF |
| `mempalace/backends/sqlite_exact.py` | `427287c1213de009141a5bcaf24188c1f10b807e` | até EOF |
| `tests/test_knowledge_graph.py` | `ace7ccf217987c3f16f0fc47140c867612bf8260` | até EOF |
| `tests/test_backend_conformance.py` | `fa134d22ea5cc5d7e0cf7c4228b2e4c10f1deb49` | até EOF |
| `tests/test_sqlite_exact_backend.py` | `d7ea8b2718c35261a5183771ec3c00a7e92ccb19` | linhas 1–2350; linha 2351 em diante vazia (EOF) |

**Nota:** leitura integral de arquivo não equivale a análise semântica completa, revisão de cada ramo ou aprovação dos testes. Não existe inventário total do repositório ainda, portanto não existe percentual global verificável.

## Testes adicionais identificados nas linhas 701–2350
- Consistência de ranking por cosseno e desempate estável em top-k.
- Estratégia de busca híbrida: união de candidatos vetoriais e BM25; busca lexical em closets.
- Leitor com lease de escrita em outro processo; refresh de cache após ciclo do escritor.
- Leitura de esquema legado sem migração durante abertura read-only.
- Alteração em commit pequeno detectada mesmo quando metadados de arquivo não mudam.
- Reabertura de wrappers antigos após substituição de handle, preservando semântica de close explícito.
- Teste parametrizado de retry do lote inteiro durante update/delete nas fases load, before_hydrate e after_hydrate, para SQLite, Rust e fallback.
- Atualização só de metadados sem alterar documento, embedding e FTS.
- Sincronização de rowid entre tabela de documentos e FTS; migração de índices FTS legados.
- Pushdown SQL de filtros `$eq`/`$in`; índices de recência e comportamento read-only.

## Riscos e recomendações para SECA
1. Snapshot de leitura consistente é obrigatório para não misturar resultados de versões diferentes do mesmo experimento.
2. Atualizações de índices textuais devem ser atômicas com dados-base e ter testes de migração.
3. Fallback de busca lexical precisa de métricas separadas: correção, recall e latência.
4. Leitura read-only não deve causar migração, alteração de metadados ou side effects.
5. Em experimentos do SECA, distinguir armazenamento e busca de memória cognitiva/plasticidade; não incorporar embeddings pré-treinados ao núcleo biológico offline.

## Limitações
Nenhuma suíte MemPalace foi executada; os testes foram inspecionados estaticamente. Não houve instalação, clonagem ou integração. Próximo: obter inventário recursivo do commit e auditar outros módulos e testes; Ruflo somente após concluir MemPalace.
