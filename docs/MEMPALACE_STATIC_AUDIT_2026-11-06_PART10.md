# MemPalace — auditoria estática complementar, parte 10 (2026-11-06)

## Referência e cobertura
Commit de origem fixado: `f8e35362189bd0a5abf4c0df1dd5bf90ba059176`.
Arquivo: `mempalace/backends/sqlite_exact.py`, blob SHA `427287c1213de009141a5bcaf24188c1f10b807e`.
Nesta etapa: linhas 181–420 consultadas. Com as linhas 1–180 da etapa anterior, há cobertura de leitura das linhas 1–420, **não do arquivo inteiro**. Inventário global pendente; percentual não calculado.

## Análise do código
- `_equality_where_sql` traduz conjunções e predicados de igualdade/`$in` para SQL parametrizado; operadores não suportados retornam `None` para avaliação posterior. O limite de `$in` é 500.
- `_cosine_distances` calcula distância cosseno exata por NumPy em float32, recomputando casos numericamente inseguros em float64; vetores nulos recebem distância 1.
- `sqlite_wing_room_counts` consulta SQLite em modo somente leitura e exclui registros administrativos (`registry` e `is_sentinel`) da contagem.
- `sqlite_wing_source_counts` restringe a consulta à coleção solicitada e seleciona origens de sessões de Claude/Codex por padrões de caminho.
- `sqlite_room_wing_hall_counts` agrega por sala/ala/corredor e extrai data máxima; a semântica cronológica depende da formatação dos metadados.
- As consultas usam parâmetros para nomes de coleção e valores. Expressões SQL interpoladas derivam de constantes internas ou nomes previamente validados nos trechos vistos; a revisão de segurança integral permanece aberta.

## SECA: interpretação, não implementação
Transações, agregações de eventos, controle de geração e proteção contra instabilidade numérica são candidatos a estudo conceitual. A busca por embeddings e os diretórios de transcrições de agentes não devem ser confundidos com mecanismos biológicos de memória. Preservar núcleo offline, sem modelos pré-treinados e sem ensino de linguagem.

## Restrições
Leitura exclusivamente estática; nenhum teste executado, instalação ou incorporação. Não iniciar Ruflo antes de concluir o inventário e a auditoria do MemPalace.
