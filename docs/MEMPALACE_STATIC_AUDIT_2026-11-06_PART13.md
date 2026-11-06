# MemPalace — auditoria estática, parte 13 (2026-11-06)

Commit de referência: `f8e35362189bd0a5abf4c0df1dd5bf90ba059176`.
Arquivo `mempalace/backends/sqlite_exact.py`, blob `427287c1213de009141a5bcaf24188c1f10b807e`: linhas **1251–1700** lidas nesta etapa; cumulativo 1–1700, ainda **parcial**.

## Evidências
- `get` diferencia paginação em SQL de filtragem em Python, preservando a semântica de limites negativos.
- `get_recent` busca recência por `filed_at` e distingue timestamps UTC e outras representações, com ordenação por `recency_key`; a correção depende das funções auxiliares ainda não auditadas.
- `delete` remove documentos e entradas FTS em lotes de até 900 identificadores.
- `iter_metadata` faz streaming e admite filtros SQL, listas de valores e projeção de chaves; `get_all_metadata` usa esse iterador como caminho preferencial.
- `facet_counts` usa agrupamento SQL e limita nomes de campos por expressão regular.
- `lexical_search` usa FTS5/BM25 quando disponível e faz fallback para BM25 em Python. Trata-se de busca textual, não de cognição emergente.
- `maintenance_state` expõe contagem de páginas, freelist e token de consistência; `run_maintenance` inicia manutenção ANALYZE nesta faixa.

## Pontos de atenção
- Leitura temporal depende de normalização de formatos de timestamps e deve ser comparada com `timeutil.py` e testes.
- A busca lexical alternativa pode escanear muitos registros; requer análise de custo e de limites.
- Exceções genéricas em `maintenance_state` podem reduzir observabilidade.

## Aplicação ao SECA
Estudar somente conceitos de recuperação determinística, manutenção e integridade de registros. Não adotar FTS/BM25 como substituto de mecanismos cognitivos biológicos; não incorporar modelos pré-treinados ou ensino de linguagem.

## Estado
Nenhuma execução, instalação, teste ou implementação. Inventário total e cobertura percentual ainda desconhecidos. Ruflo permanece bloqueado até auditoria integral verificável do MemPalace.
