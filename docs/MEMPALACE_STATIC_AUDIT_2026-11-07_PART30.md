# SECA — Auditoria estática MemPalace — Parte 30 (2026-11-07)

## Escopo e evidência
- Repositório de origem: MemPalace/mempalace.
- Commit fixado: `f8e35362189bd0a5abf4c0df1dd5bf90ba059176`.
- Árvore Git recursiva consultada: `truncated=false`, **851 blobs** (incluindo documentação, testes e demais arquivos versionados), **300 blobs sob `tests/`** e **18 sob `docs/`**. Estes totais não são porcentagens de leitura e não excluem arquivos binários ou gerados.
- Arquivo integralmente recuperado: `tests/test_config.py`; blob Git `f4ff77fa36a414ea2aae290ed1393f8c9834a8de`; 1.580 linhas pela separação de quebras de linha do conteúdo recuperado; 171 funções declaradas `test_*` identificadas por inspeção textual (parametrizações podem gerar mais casos).
- Evidência: a entrada da árvore Git para esse caminho contém o mesmo SHA do conteúdo recuperado. O arquivo estava pendente na Parte 29. Nenhum teste foi executado.

## Análise estática dos testes
1. **Configuração e precedência:** arquivo JSON, variáveis de ambiente e argumentos explícitos; cenários para Chroma, SQLite exato, Qdrant, Milvus e pgvector. Alguns campos de serviços externos, como URLs, tokens e DSNs, são cobertos apenas por testes de configuração, não por testes de conectividade.
2. **SQLite e WAL:** os testes demonstram uma distinção intencional entre conexões de leitura com sidecars presentes e abertura normal quando o índice WAL não existe. Um teste executa um INSERT seguido de rollback na conexão obtida por `connect_sqlite_read`, evidenciando que o fallback não impõe isolamento estritamente read-only. Isto é evidência estática da expectativa do teste, não prova de execução bem-sucedida.
3. **Normalização e validação:** casos para caminhos, nomes Unicode, travessia de diretórios, bytes NUL, comprimentos máximos, datas e horários UTC; verificar separadamente o tratamento de links simbólicos no código de produção.
4. **Chunking e terminação:** parâmetros inválidos são reparados; `chunk_size > 0` e `0 <= chunk_overlap <= chunk_size // 2` são invariantes explicitamente testadas para evitar laços infinitos; `min_chunk_size <= chunk_size` evita ingestão vazia. Para o SECA, a ideia transferível é validar invariantes de segmentação de experiências sensoriais, **não** importar segmentação textual.
5. **Operação e recuperação:** limites de threads, backups, configuração de hooks, resolução XDG/legado e preservação de configuração existente; testes de valores inválidos e de compatibilidade retroativa.
6. **Incompatibilidades com o núcleo SECA:** os testes incluem embeddings, idioma, mineração de conversas, backends remotos e ranking textual. Esses componentes não devem ser importados para o núcleo biológico offline, sem modelos pré-treinados e sem ensino de linguagem.

## Riscos e limites
- A exceção de WAL abre uma superfície de escrita para uma operação denominada de leitura; estudar separação de privilégios, abertura controlada e isolamento de dados críticos.
- Os testes não comprovam segurança operacional, aprovação em CI nem ausência de vulnerabilidades.
- A árvore recursiva **não truncada** estabelece um denominador inicial de 851 blobs, mas o manifesto de cobertura integral precisa ser reconciliado com todas as partes anteriores, um blob por caminho e SHA. **Não há porcentagem global certificada.**
- Nenhuma instalação, execução de código do repositório, teste dinâmico, implementação ou integração ao SECA.

## Próximos passos
Consolidar manifesto `path, blob_sha, tipo, tamanho, estado, evidência, relatório` para os 851 blobs, reconciliar os relatórios anteriores e priorizar arquivos não lidos. Ruflo só começa após certificação integral do MemPalace.
