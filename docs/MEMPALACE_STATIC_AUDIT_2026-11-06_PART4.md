# SECA — Auditoria MemPalace, parte 4 (2026-11-06)

Análise estática por GitHub; nenhuma instalação, execução ou incorporação de código.

## Evidências de leitura
- `tests/test_knowledge_graph.py`: intervalos 1–760 consultados; último retorno encerra no EOF; blob `ace7ccf217987c3f16f0fc47140c867612bf8260`.
- `tests/test_backend_conformance.py`: intervalo 1–160; consulta a partir da linha 161 retornou vazio, indicando EOF; blob `fa134d22ea5cc5d7e0cf7c4228b2e4c10f1deb49`.
- `mempalace/backends/sqlite_exact.py`: intervalos 1–500; leitura parcial; blob `427287c1213de009141a5bcaf24188c1f10b807e`.

## Achados
1. SQLiteExact armazena vetores float32 e calcula distância de cosseno exata; a função `_cosine_distances` recompõe em float64 apenas linhas afetadas por overflow/underflow, mantendo zeros a distância um.
2. `_equality_where_sql` faz pushdown de filtros escalares parametrizados, enquanto operadores complexos seguem para avaliação Python.
3. `_write_lock` obtém mutex do handle antes da posse de escrita entre processos, explicitamente para evitar que outra thread ultrapasse o prazo da lease.
4. Testes do grafo incluem regressão de limite temporal exato entre fatos sucessores, prevenção de confusão de entidades com nomes semelhantes, escape literal de metacaracteres SQL LIKE e limpeza de conexões.
5. Testes de conformidade exercitam isolamento entre palácios, validação de lotes, filtros e ausência de upsert em atualização de ID inexistente.

## Avaliação SECA
A comparação com backend exato pode servir como referência determinística para experimentos de recuperação; registro de tempo, isolamento e tolerância numérica são boas propriedades de infraestrutura. Não confundir índice vetorial com memória neural biológica.

## Cobertura
Cinco arquivos tiveram seus intervalos até EOF consultados (`base.py`, `embedding.py`, `knowledge_graph.py`, `test_knowledge_graph.py`, `test_backend_conformance.py`). Isso NÃO constitui revisão integral semântica, execução de testes ou porcentagem global de MemPalace. `sqlite_exact.py` parcial. Inventário completo e commit fixo ainda pendentes. Ruflo não iniciado.
