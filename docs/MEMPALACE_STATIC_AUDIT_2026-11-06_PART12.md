# MemPalace — auditoria estática, parte 12 (2026-11-06)

## Evidência
Commit fixado: `f8e35362189bd0a5abf4c0df1dd5bf90ba059176`.
Arquivo: `mempalace/backends/sqlite_exact.py`; blob SHA `427287c1213de009141a5bcaf24188c1f10b807e`.
Linhas 851–1250 consultadas nesta etapa; cumulativo consultado: 1–1250. **Arquivo ainda não confirmado como integralmente lido.** Inventário global e cobertura percentual pendentes.

## Observações estáticas
1. `_rows` valida filtros, seleciona colunas conforme necessidade e aplica LIMIT/OFFSET no SQL apenas quando os filtros não exigem pós-filtragem em Python.
2. `_rows_by_ids` agrupa IDs únicos e consulta em lotes de 900, preservando a possibilidade de remontar a ordem externa.
3. `_index_version` compara assinatura do banco e WAL em modo imutável; `query` repete até três vezes em caso de `_SnapshotChanged`.
4. `_query_once` exige embeddings explícitos, verifica dimensões e faz ranking por distância cosseno com desempate estável via mergesort.
5. `_rank_vectors` mantém matriz de vetores e normas em cache; invalida por `PRAGMA data_version`; filtros simples usam metadados reduzidos.
6. `_load_all_vectors` carrega os embeddings da coleção e ignora vetores vazios ou incompatíveis; `_hydrate` busca o conteúdo dos resultados escolhidos em lotes.

## Riscos e questões abertas
- Consumo de memória proporcional ao número e dimensionalidade dos vetores; não há evidência de limites globais nesta faixa.
- Descarte silencioso de vetores incompatíveis em `_load_all_vectors` merece revisão de observabilidade.
- Não afirmar que os mecanismos funcionam corretamente sob concorrência sem executar testes; nesta fase apenas leitura estática.

## SECA
Avaliar conceitos de consistência de snapshots, desempate determinístico, leitura seletiva e separação entre índices e registros de experiência. Não incorporar embeddings, modelos pré-treinados nem mecanismos de ensino de linguagem. Núcleo biológico offline preservado.

## Estado
Ruflo não iniciado. Nenhuma instalação, execução, teste ou implementação.
