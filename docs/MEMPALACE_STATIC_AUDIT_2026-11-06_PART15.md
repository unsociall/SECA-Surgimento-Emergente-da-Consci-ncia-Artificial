# MemPalace — complemento de auditoria estática, parte 15

Referência imutável: commit `f8e35362189bd0a5abf4c0df1dd5bf90ba059176`; arquivo `mempalace/backends/sqlite_exact.py`, blob `427287c1213de009141a5bcaf24188c1f10b807e`.

## Evidência da execução
Foram consultadas diretamente as linhas 1701–2100 do arquivo por leitura de fonte no GitHub. Esta leitura confirma os mecanismos abaixo e é uma **revisão de aprofundamento**, não uma contagem de arquivo adicional: o relatório parte 14 já registra o arquivo integral e inventário completo do commit. Evitar dupla contagem de cobertura.

## Constatações
- `compact` executa `VACUUM` em autocommit sob lock e restaura `isolation_level` em `finally`.
- `_database_signature` usa atributos do arquivo e cabeçalho SQLite acrescidos da geração de escrita para identificar alterações que o mtime não distingue.
- `_connect_read_only` verifica a dupla `-wal`/`-shm`; usa `mode=ro` quando há WAL e `immutable=1` no banco limpo, evitando escrita incidental em leitura.
- `_connect` serializa abertura e migração de esquema; `PRAGMA query_only=ON` reforça o acesso somente leitura.
- `_init_schema` cria tabelas e tenta habilitar FTS5; `_ensure_fts_rowid_sync` reconcilia índices textuais com linhas dos documentos.
- `_ensure_locus_columns` cria colunas geradas virtuais e índices de localização, origem e data.

## Questões de auditoria ainda abertas
Verificar, por leitura cruzada de testes, as garantias de concorrência, falhas de migração, recuperação de FTS e interação com o ciclo de vida de conexões. Não afirmar testes aprovados sem execução.

## SECA
Possível transferência conceitual: transações, isolamento de leitura, geração monotônica, indexação temporal e consistência entre registros e índices. Não transferir embeddings, modelos pré-treinados ou instrução de linguagem. Nenhum código instalado, executado ou incorporado. Ruflo permanece posterior à conclusão comprovada da análise MemPalace.
