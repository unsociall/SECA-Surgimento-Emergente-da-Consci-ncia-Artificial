# SECA — MemPalace: auditoria estática, parte 28 (2026-11-07)

## Proveniência e escopo
Repositório: MemPalace/mempalace. Commit fixado: `f8e35362189bd0a5abf4c0df1dd5bf90ba059176`.
Arquivos recuperados diretamente pelo conector GitHub, sem instalação ou execução:
- `mempalace/config.py` — blob `34b364277fe204584bb463e1dfbf4f3f205c12b2`, 1.739 linhas; **análise parcial**, não contabilizar como leitura integral.
- `tests/test_config.py` — blob `f4ff77fa36a414ea2aae290ed1393f8c9834a8de`, 1.580 linhas; **análise parcial**, não contabilizar como leitura integral.

## Evidências observadas
1. `sanitize_name` rejeita separadores de caminhos, `..`, NUL, valores vazios e comprimentos acima de 128. `sanitize_kg_lookup` admite identificadores históricos mais longos para permitir consulta sem criação.
2. `sanitize_iso_temporal` exige data completa ou data/hora UTC em formato canônico e valida calendário, visando preservar ordenação lexicográfica de valores temporais SQLite TEXT.
3. `connect_sqlite_read` usa URI com `mode=ro` normalmente; no caso WAL sem arquivos auxiliares `-wal`/`-shm`, abre conexão SQLite normal, que possui capacidade de escrita. Os testes `test_connect_sqlite_read_takes_a_normal_open_when_the_wal_index_is_missing`, `...stays_read_only_for_a_rollback_journal_database` e `...stays_read_only_while_the_sidecars_are_there` explicitam essa distinção. Testes apenas lidos, não executados.
4. A configuração prevê múltiplos backends e modelos de embeddings, inclusive opções externas. Essas dependências **não são compatíveis por padrão** com o requisito SECA de núcleo biológico offline, sem pesos pré-treinados e sem ensino de linguagem.
5. Os testes incluem precedência de variáveis de ambiente e aliases de caminhos, validação de nomes Unicode e rejeição de travessia de diretórios.

## Avaliação para SECA (somente estudo)
- Candidato conceitual: validação de nomes, timestamps canônicos e separação explícita de modo de leitura de memória.
- Risco a investigar: fallback de conexão com capacidade de escrita em rotinas nominalmente de leitura; não inferir exploração ou falha sem análise dos chamadores e contexto de permissões.
- Não copiar componentes de embeddings, pipelines de linguagem ou conectores remotos.
- Não foram executados testes, instaladas dependências ou feitas alterações no dispositivo.

## Controle de cobertura
Os dois arquivos acima continuam **PARCIAIS**. A obtenção do conteúdo completo e de seus hashes não equivale à leitura/análise integral. Inventário global do commit e reconciliação de relatórios anteriores pendentes; percentual de cobertura **não certificado**. Ruflo não iniciado.

## Próxima etapa
Analisar sistematicamente as seções restantes de ambos os arquivos, registrar intervalos verificados e cruzar cada função crítica com seus testes; em paralelo obter a árvore Git recursiva do commit e montar manifesto deduplicado com caminho, tipo, blob SHA, estado e evidência.
