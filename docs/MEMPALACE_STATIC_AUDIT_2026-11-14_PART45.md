# MemPalace — auditoria estática, parte 45 (2026-11-14)

## Proveniência e cobertura
- Origem: `MemPalace/mempalace`, commit fixado `f8e35362189bd0a5abf4c0df1dd5bf90ba059176`.
- Arquivo: `mempalace/backends/_inproc_sqlite.py`; blob Git `2f1399aac07d509ccfcabca0d61873c4b00ee02a`.
- Consulta integral ao conector GitHub: 668 linhas retornadas, incluindo linha final; inspeção estática do módulo completo nesta etapa. A contagem corresponde ao texto retornado, podendo incluir linha vazia terminal.
- Evidência de leitura: definições `_HOLD_SCRIPT`, `_key`, `palace_db_lock`, `PalaceSqliteConnection`, `_Anchor`, `_ofd_read_lock`, `_guard`, `_Holder`, `_read_holder_line`, `_stop_holder`, `_start_holder`, `_ensure_holder`, `_ensure_anchor`, `open_reader`, `open_writer`, `release`, `release_all`, `_reset_after_fork_in_child`, e registro `os.register_at_fork` ao fim do arquivo.
- Não houve execução de testes, importação do módulo, instalação, clonagem no Termux ou alteração do SECA. Cobertura global do inventário histórico de 851 caminhos: **não certificada**.

## Arquitetura observada
O módulo serializa operações SQLite locais com `RLock` indexado pelo caminho real normalizado. `open_reader` e `open_writer` adquirem o bloqueio antes de abrir a conexão; o wrapper `PalaceSqliteConnection` fecha e libera o bloqueio. No Linux, mantém âncora e tenta guardas OFD em intervalos SHARED e DMS; em POSIX sem OFD, usa subprocesso auxiliar com conexão WAL ociosa. A leitura funcional usa conexões novas para reduzir risco de estado FTS obsoleto. A implementação trata substituição de inode, substituição de wal-index e estado após fork.

## Achados e limites da inferência estática
1. **Propriedade de fechamento:** `PalaceSqliteConnection.close()` marca `_closed=True` antes de invocar o callback de fechamento. O callback `_close_and_release` garante `lock.release()` em `finally`, mesmo se `conn.close()` lançar. Isso evita reentrância do callback, mas não comprova que o descritor tenha sido fechado caso a operação falhe.
2. **Risco de espera auxiliar:** `_read_holder_line` cria thread daemon para `readline()`, faz `join(2s)` e retorna string vazia se não houver resposta. Não há cancelamento explícito da thread; repetidas falhas podem manter leituras pendentes até EOF ou saída do subprocesso. É hipótese de esgotamento de recursos, não incidente reproduzido.
3. **Guardas best effort:** `_ofd_read_lock` tenta três vezes, capturando todo `OSError`. `_guard` registra falha e permite nova tentativa na próxima leitura. Portanto, a aquisição dos dois guardas não é uma pós-condição obrigatória de `open_reader`; verificar riscos residuais sob contenção.
4. **Encerramento global:** `release_all()` limpa mapas de âncoras/holders sob `_registry_lock`, mas descarta recursos fora do bloqueio individual por banco. A documentação limita uso a testes e shutdown. Chamada concorrente com leitores requer contrato de exclusão externa; não assumir segurança geral.
5. **Dependência de plataforma:** uso de `fcntl`, layout nativo `struct flock`, constante Linux de OFD e subprocesso POSIX implica caminhos distintos por sistema operacional; nenhum teste foi executado aqui.
6. **Segurança de caminho:** `_key` resolve `realpath` para identidade de bloqueio, mas `open_reader` abre o caminho original depois de verificações por `stat`. Substituição concorrente do caminho entre verificação e abertura merece exame específico; não foi demonstrada exploração.
7. **Processo auxiliar:** `subprocess.Popen([sys.executable, "-c", _HOLD_SCRIPT, db_path])` não utiliza shell. Ainda assim, cria processo Python auxiliar e depende da disponibilidade/controle do executável e de pipes; incompatível com uma política que proíba processos auxiliares em eventual arquitetura futura.

## Pertinência ao SECA (somente estudo)
- Adotar como requisitos abstratos: exclusão mútua por identidade de armazenamento, leitura transacional consistente, detecção de substituição de WAL/SHM, tratamento explícito de falhas de guardas e encerramento seguro.
- Não transplantar `ChromaBackend`, guardas OFD, subprocessos, indexação linguística, modelos pré-treinados ou mecanismos de ensino de linguagem para o núcleo biológico offline.
- Priorizar desenho próprio de memória episódica não linguística e experimentos futuros isolados, somente após autorização expressa para implementação.

## Estado do manifesto e próxima etapa
A leitura deste arquivo é registrada como **integral no conteúdo retornado**, ancorada em commit e blob. O manifesto global publicado anteriormente precisa ser reconciliado por caminho, SHA, intervalos e EOF antes de contabilizar cobertura certificada. Próximo passo: confrontar `tests/test_inproc_sqlite_locks.py` com cada ramo e depois verificar outros arquivos ainda sem evidência. Ruflo permanece em espera.
