# MemPalace — auditoria estática, parte 44 (2026-11-14)

## Escopo e proveniência
- Origem: `MemPalace/mempalace`, commit fixado `f8e35362189bd0a5abf4c0df1dd5bf90ba059176`.
- `tests/test_inproc_sqlite_locks.py`: blob Git `b1ec03f79f22082728235780ff4a8a7e8bd9ea01`; 549 linhas retornadas na consulta integral do conector. Estado: leitura estática integral do conteúdo retornado, sujeito à reconciliação do manifesto.
- `mempalace/backends/_inproc_sqlite.py`: blob Git `2f1399aac07d509ccfcabca0d61873c4b00ee02a`; 668 linhas retornadas. Estado: inspeção estática parcial, **não** certificar leitura integral neste relatório.
- Nenhum teste ou componente foi executado, instalado ou incorporado. Nenhuma alteração no dispositivo do usuário.

## Evidências do teste
O arquivo define provas para serialização das escritas Chroma com `palace_db_lock`, manutenção do bloqueio durante a vida de leitores, liberação em erro de abertura e fechamento idempotente, leituras aninhadas sem vazamento de estado, confirmação de transação do escritor, substituição de arquivo SQLite e leitura atualizada, inspeção `quick_check` concorrente com escrita em journal rollback e WAL, retenção dos bloqueios SHARED/DMS e dos inodes WAL/SHM, reabertura Chroma, âncora ocupada, subprocesso guardião de bloqueios, transição DELETE→WAL e fallback de OFD locks no Linux.

## Confronto inicial com implementação
O módulo de implementação declara `_locks` por caminho normalizado, `threading.RLock`, wrappers `PalaceSqliteConnection`, `open_reader` e `open_writer`, guardas OFD em Linux, e processo auxiliar de retenção de conexão em POSIX sem OFD. `release` e `release_all` descartam âncoras e guardiões. A existência de testes e de ramos de proteção não comprova correção em runtime.

## Riscos e pontos a verificar
1. `PalaceSqliteConnection.close()` marca `_closed` e libera lock por callback; o callback fecha conexão e libera bloqueio. Examinar comportamento em exceções, reutilização indevida e operações fora do contexto.
2. `_read_holder_line` cria thread daemon e espera com prazo; uma leitura bloqueada pode sobreviver ao timeout. Avaliar acúmulo de threads e encerramento em cenários de falha.
3. `_ofd_read_lock` captura `OSError` genericamente e faz tentativas curtas; investigar distinção entre contenção transitória, plataforma incompatível e erro permanente.
4. `release_all` limpa registros sob `_registry_lock` e depois descarta recursos; confrontar com operações concorrentes e locks individuais.
5. Testes POSIX/Linux são condicionais; evidência de portabilidade para outros sistemas permanece incompleta.

## Relevância ao SECA
Requisitos potenciais para memória episódica offline: serialização explícita de leitura/escrita, persistência resistente a checkpoint WAL, verificação de integridade que não perturbe gravações, recuperação de snapshots e descarte determinístico de recursos. São **hipóteses de projeto**, sem adoção de Chroma, MemPalace, modelos pré-treinados ou ensino de linguagem.

## Cobertura e continuidade
O inventário histórico de 851 caminhos e o manifesto publicado anteriormente exigem reconciliação por caminho+blob+intervalos e evidência do EOF. Não declarar porcentagem global nem 100%. Próxima etapa: leitura integral e comparação linha a linha de `mempalace/backends/_inproc_sqlite.py`, e marcação verificável no manifesto; Ruflo permanece em espera.
