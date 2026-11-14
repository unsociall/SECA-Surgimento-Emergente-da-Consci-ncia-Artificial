# SECA — MemPalace, auditoria estática Parte 43 (2026-11-14)

## Proveniência e escopo
- Repositório: https://github.com/MemPalace/mempalace
- Commit fixado: `f8e35362189bd0a5abf4c0df1dd5bf90ba059176`
- Arquivo lido integralmente: `tests/test_wal_status_cache_regressions.py`
- Blob SHA Git verificado: `7820d1aef3bdbdd04fa6c848bf17ab31637e7d5e`
- Manifesto de origem: `docs/MEMPALACE_TREE_MANIFEST_f8e3536.tsv`; entrada correspondente confere em caminho e SHA. O manifesto ainda marca entradas como `PENDENTE_DE_RECONCILIACAO`, inclusive esta; a evidência desta parte deve ser reconciliada antes de atualizar contagens globais.
- Método: leitura de texto via API GitHub, sem execução dos testes, importação de módulos, instalação ou alterações no Termux.

## Leitura integral e lógica do teste
O arquivo possui um único teste parametrizado em dois valores (`taxonomy` e `graph`), portanto duas variantes lógicas. Importa `contextlib`, `os`, `sqlite3`, `chromadb`, `pytest`, o helper de testes `_patch_mcp_server` e `_inproc_sqlite`. Dentro do teste importa `mcp_server` e `chroma_sqlite`.

1. Habilita `PRAGMA journal_mode=WAL` para `chroma.sqlite3` e abre `chromadb.PersistentClient`.
2. Cria coleção sem função de embedding automática e insere vetores explícitos de dimensão 2 com metadados `wing/room/hall`.
3. Substitui a seleção do backend por `chroma`, intercepta uma de duas funções de contagem e conta invocações reais.
4. Lê duas vezes o resumo inicial e exige contagem 1 com apenas uma consulta real (cache hit).
5. Captura `inode`, `mtime_ns` e tamanho do arquivo SQLite principal; grava novo documento via cliente Chroma; exige que esses três atributos do arquivo principal não mudem, caracterizando a condição de fixture WAL-only.
6. Exige que a próxima leitura observe contagem 2 e execute uma nova consulta; a leitura seguinte deve reutilizar o cache sem consulta adicional.
7. Em `finally`, fecha o cliente e libera o recurso `_inproc_sqlite.release(db)`.

## Conclusões e limites
- Contrato testado: invalidação dos caches de taxonomia e grafo após commit externo restrito ao WAL, mesmo com metadados do arquivo principal inalterados.
- A contagem de chamadas distingue invalidação de cache de simples retorno de dados atualizados; também verifica reutilização subsequente.
- O teste não comprova, sem execução, que a implementação passa; não demonstra robustez a múltiplos processos, perda de energia, corrida de checkpoints, arquivos WAL corrompidos ou falhas durante fechamento.
- A condição WAL-only depende do comportamento do SQLite/Chroma no ambiente do teste; a asserção de invariância do arquivo principal é uma pré-condição explícita e pode tornar o teste sensível ao ambiente.
- Dependências diretas de teste observadas: pytest, chromadb, sqlite3 e helpers internos. Não se inferiu versão ou compatibilidade sem consultar manifests de dependências.

## Relevância ao SECA
Uma futura memória episódica local poderá exigir um marcador de versão transacional ou outra evidência de commit efetivo para invalidar índices derivados, em vez de depender exclusivamente de `mtime`/tamanho do banco principal. Recomenda-se separar estado persistido de visões derivadas, definir contratos de coerência após gravações externas e projetar testes próprios de recuperação temporal e concorrência. São apenas requisitos para pesquisa futura: não importar Chroma, MCP, embeddings externos, modelos pré-treinados ou ensino de linguagem para o núcleo biológico offline.

## Situação global e próximos passos
Inventário histórico: 851 blobs, árvore informada como não truncada; cobertura integral global **não certificada**. A leitura integral deste arquivo tem evidência de caminho e blob, mas o manifesto global precisa de reconciliação dos relatórios anteriores. Priorizar `tests/test_inproc_sqlite_locks.py` e o código correspondente de `mempalace/backends/_inproc_sqlite.py`, verificando políticas de lock e invalidação. Ruflo só depois de MemPalace integralmente certificado.
