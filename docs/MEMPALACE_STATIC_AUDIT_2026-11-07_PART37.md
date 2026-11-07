# SECA — Auditoria estática MemPalace — Parte 37 (2026-11-07)

## Proveniência e escopo
- Origem: MemPalace/mempalace
- Commit fixado: `f8e35362189bd0a5abf4c0df1dd5bf90ba059176`
- Arquivo integralmente lido nesta etapa: `tests/test_backend_header_probe_locks.py`
- Git blob SHA: `f18205220d7d06a3f60d9ef562f351bfec43a52e`
- Árvore Git recursiva consultada neste ciclo: `truncated=false`, 851 entradas do tipo blob.
- Leitura exclusivamente estática. **Zero testes executados**; não houve instalação, clonagem no Termux nem implementação.
- A cobertura global dos 851 arquivos continua **não certificada**; este documento não atribui percentual.

## Análise integral do arquivo
O módulo contém regressões para probes de cabeçalho de bancos SQLite em modo WAL e preservação de locks POSIX. A motivação documentada é que um `open()`/close convencional do arquivo SQLite no mesmo processo pode liberar locks fcntl associados ao par processo/inode, inclusive locks mantidos por outro descritor; fechamento de conexão externa pode então fazer checkpoint e remover arquivos `-wal` e `-shm` ainda em uso. Trata-se de hipótese de falha de integridade explicitada pelos autores, não de reprodução independente nesta auditoria.

Funções auxiliares: `_run` (subprocesso Python), `_shared_lock_held` (tentativa de lock exclusivo de outro processo), `_lock_released_within` (polling e GC), `_writer`, `_chroma_writer`, `_add`, `_sidecar_inodes`; fixture `_cold_probe_cache` limpa estado da camada `_magic`.

Casos de teste lidos:
1. `test_probes_open_no_plain_descriptor_on_live_databases`: intercepta `builtins.open`, `io.open`, `os.open` e exige que detectores e assinatura de banco não abram diretamente arquivos `.sqlite3`.
2. `test_probes_keep_writer_shared_lock`: após detecção e leitura de assinatura repetidas, verifica manutenção de lock compartilhado e sua liberação ao fechar o backend.
3. `test_probes_keep_chroma_writer_shared_lock`: exercita caminho Chroma com bindings SQLite nativos separados do `sqlite3` do Python; exige retenção do lock após probes com cache limpo.
4. `test_external_close_cannot_orphan_wal_after_probes`: compara inodes dos sidecars WAL/SHM e visibilidade de uma escrita subsequente a um fechamento externo. O comentário distingue diferenças entre versões SQLite 3.50.4 e 3.53.3, sem que isso seja verificado aqui.
5. `test_detect_rejects_empty_then_accepts_written_header`: arquivos vazios não identificam backend; arquivo substituído com inode novo invalida detecção positiva; arquivo contendo somente magic SQLite é aceito, o que **não comprova integridade de um banco completo**.
6. `test_database_signature_tracks_changes`: assinatura muda após escrita/checkpoint; arquivo ausente causa `OSError`; conteúdo inválido retorna assinatura com cabeçalho não reconhecido.
7. `test_read_header_fields_reads_through_sqlite_only`: valida leitura de `user_version` e rejeição de diretórios e arquivos vazios.

## Achados e limites
- **Integridade WAL — alta prioridade de investigação**: detecção aparentemente somente de leitura pode afetar locks e persistência quando bibliotecas SQLite diferentes coexistem. Os testes especificam mitigação, mas sem executar testes não há comprovação da implementação.
- **Identificação não equivale a validação**: aceitar cabeçalho com apenas magic SQLite é suficiente para identificação heurística, não para declarar o banco íntegro.
- **Portabilidade**: testes de lock são marcados POSIX; extrapolação para Windows/Android ou outras versões SQLite requer avaliação própria.
- **Limites do teste**: `monkeypatch` de `open` Python não intercepta toda abertura de descritores por código nativo; a prova de lock em subprocesso complementa a cobertura.
- **Concorrência**: `_magic.forget()` e `_magic.close_retained()` são relevantes para gestão de recursos; a segurança de seus caminhos concretos depende de auditoria posterior do módulo `mempalace/backends/_magic.py`.

## Relevância para o SECA
Inspirar requisitos de uma futura memória episódica própria: (a) leitura de metadados sem interferir nos locks do escritor; (b) checkpoints recuperáveis e verificáveis; (c) detecção de corrupção independente da identificação do formato; (d) testes de concorrência e consistência de logs WAL; (e) separação de capacidades de leitura/escrita. **Nenhuma integração proposta nesta fase**. Preservar o núcleo biológico offline, sem modelos pré-treinados e sem ensino de linguagem.

## Manifesto incremental verificável
| Caminho | Blob SHA | Evidência | Estado |
|---|---|---|---|
| `tests/test_backend_header_probe_locks.py` | `f18205220d7d06a3f60d9ef562f351bfec43a52e` | Parte 37 | Leitura integral estática |

O manifesto **global** ainda requer reconciliação individual dos 851 blobs com relatórios anteriores. Próximo alvo: `mempalace/backends/_magic.py` e verificações dos caminhos `detect()` em `sqlite_exact.py` e `chroma.py`. Ruflo não iniciado.
