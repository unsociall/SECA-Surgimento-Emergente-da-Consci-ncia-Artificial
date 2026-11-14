# MemPalace — auditoria estática Parte 46 (2026-11-14)

## Escopo e evidência
Repositório: `MemPalace/mempalace`; commit fixado `f8e35362189bd0a5abf4c0df1dd5bf90ba059176`.
Arquivos lidos integralmente nesta etapa via API GitHub, sem execução:
- `tests/test_inproc_sqlite_locks.py` — blob `b1ec03f79f22082728235780ff4a8a7e8bd9ea01`.
- `mempalace/backends/_inproc_sqlite.py` — blob `2f1399aac07d509ccfcabca0d61873c4b00ee02a`.

## Confronto entre contratos e implementação
1. **Serialização intraprocesso:** `palace_db_lock` usa `RLock` por caminho real normalizado; `open_reader` e `open_writer` adquirem o lock antes de abrir conexão. Os testes `test_reader_holds_the_lock_until_close`, `test_failed_open_releases_the_lock`, `test_writer_commits_and_releases_on_exit` e `test_chroma_writes_hold_the_palace_lock` exercitam os contratos. A proteção de escrita do Chroma depende da integração externa a este módulo, ainda não certificada.
2. **Ciclo de vida da conexão:** `PalaceSqliteConnection.close` marca `_closed` e chama `_release`, que fecha a conexão real em `finally` libera o lock. Há um risco estático: se `conn.close()` lançar exceção, `_closed` já será True, impedindo nova tentativa de fechar, embora o lock seja liberado. Testes verificam idempotência nominal, não essa exceção.
3. **Âncoras e OFD:** `_ensure_anchor` conserva conexão em falha de prime; `_guard` tenta OFD read locks nos intervalos SHARED/DMS. `test_a_busy_anchor_stays_open` cobre falha de prime. A função `_guard` pode retornar com `db_guarded` ou `shm_guarded` falsos e `open_reader` prossegue: garantia é best effort, não bloqueio obrigatório.
4. **Fallback sem OFD:** `_HOLD_SCRIPT` mantém processo auxiliar e conexão ociosa em WAL; rollback-journal libera a conexão para permitir commits externos. Testes `test_open_reader_keeps_a_holder_until_release`, `test_idle_rollback_holder_allows_external_commits_and_fresh_reads` e `test_idle_holder_detects_delete_to_wal_and_retains_sidecar_guard` cobrem a transição. `_read_holder_line` cria thread daemon que pode permanecer bloqueada em `readline()` após timeout; não há cancelamento explícito.
5. **WAL e sidecars:** testes `test_fast_path_reads_keep_the_palace_locked`, `test_chroma_reopen_keeps_python_reads_current` e `test_lock_holder_allows_checkpoints_without_replacing_sidecars` comparam inodes e locks de SHARED/DMS, além de dados recuperados. Não provam ausência de todas as condições de corrida.
6. **Portabilidade:** `_F_OFD_SETLK` usa fallback numérico 37 em Linux, verificado por teste. Pressuposto ABI específico precisa de revisão por arquitetura/plataforma; POSIX sem OFD usa helper, não o mesmo mecanismo.
7. **Encerramento:** `release` usa lock por caminho, mas `release_all` esvazia registries sob `_registry_lock` e descarta recursos fora dos locks por caminho. Existe possibilidade teórica de concorrência com leitores ativos; requer exame de chamadas e testes específicos antes de classificar como falha.

## Relevância ao SECA
Requisitos conceituais para memória episódica offline: serialização por unidade de armazenamento, controle explícito de versão/snapshot, persistência de eventos, recuperação após interrupção, sinalização de falhas de guardas e testes de concorrência. Não transferir diretamente o helper subprocess, Chroma ou a camada de embeddings; não incorporar modelo pré-treinado nem ensino linguístico.

## Limitações e cobertura
Auditoria exclusivamente estática: **zero testes executados**. O inventário histórico informado é de 851 caminhos, mas esta etapa não reconciliou todas as entradas com evidências por blob e intervalos. **Cobertura global não certificada; nenhuma porcentagem atribuída.** Os dois blobs acima têm leitura integral nesta etapa; o restante do manifesto permanece sujeito a reconciliação. Ruflo não iniciado.

## Próxima etapa
Inspecionar os pontos de integração de `palace_db_lock` em `mempalace/backends/chroma.py`, os testes de shutdown/fork e reconciliar as entradas correspondentes no manifesto antes de expandir a cobertura.
