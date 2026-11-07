# SECA — Auditoria estática MemPalace — Parte 19 (2026-11-07)

## Referência e método
Origem: MemPalace/mempalace; commit fixado `f8e35362189bd0a5abf4c0df1dd5bf90ba059176`. Consulta textual integral via conector GitHub; **nenhum módulo foi importado, instalado ou executado**. Esta etapa documenta leitura de fonte, não validação de comportamento.

| Caminho | Blob SHA observado | Evidência |
|---|---|---|
| `mempalace/metadata_types.py` | `b11a56b5c0853170ad56c3f7dbc3244364a243de` | Texto integral recebido e inspecionado |
| `mempalace/fsio.py` | `a8e8cf3bd40bec775d00c92c70bb0bbbc69ee033` | Texto integral recebido e inspecionado |
| `mempalace/paths.py` | `93a9028473ad3b6b4d80ae870e8de51bec32b14a` | Texto integral recebido e inspecionado |
| `mempalace/_env.py` | `24c1add031de4a18b0bedc1cdd23e19574570791` | Texto integral recebido e inspecionado |
| `mempalace/_once.py` | `c604d91eb7a9f1504dcf6459304ed0cf92170b11` | Texto integral recebido e inspecionado |

## Achados de código
1. **Metadados**: `coerce_metadata_types` converte apenas campos declarados e preserva valores que não se convertem de forma segura; limites de inteiros assinados de 64 bits; `is_sentinel` trata strings legadas como `"false"` e `"0"` sem interpretá-las como verdadeiras. `is_bookkeeping` também classifica IDs com prefixos reservados. Revisar colisões com IDs de usuário e invariantes dos consumidores.
2. **Publicação de estado**: `fsio.atomic_publish` usa arquivo temporário exclusivo, sincronização, substituição e sincronização de diretório; **existe fallback de escrita in-place** sob EACCES/EPERM/EROFS quando segue links, explicitamente sujeito a truncamento após interrupção. Não assumir atomicidade universal. `read_json_for_update` recusa sobrescrever JSON corrompido e tenta preservar bytes anteriores.
3. **Leitura de origem**: `open_source_file` rejeita symlink e arquivos não regulares, usa O_NOFOLLOW quando disponível e O_NONBLOCK para evitar FIFO bloqueante. `decode_source` distingue UTF-8, surrogateescape e Windows-1252, com objetivo de round-trip; a opção de normalização de quebras de linha é transformadora, não reversível em bytes.
4. **Caminhos e migração**: `paths.py` separa diretório de configuração XDG e estado legado; seleciona grafo histórico se o grafo local não tem fatos, sem fusão automática. Uma falha de leitura do grafo é conservadoramente tratada como possível existência de fatos.
5. **Configuração e avisos**: `_env.py` rejeita números não finitos e flags inválidas, usando default e aviso único; `_once.py` guarda chaves num conjunto protegido por mutex. A coleção de chaves não tem limite explícito e dura até o fim do processo ou `reset`.

## Questões de segurança e consistência para revisão posterior
- Verificar testes de interrupção no fallback in-place, permissões, links simbólicos e condições de corrida entre `lstat` e abertura.
- Conferir se consumidores preservam a distinção entre dados inválidos, ausentes e valores normalizados.
- Conferir migração de grafos, escolhas de caminho em configurações legadas e comportamento de exceções.
- Examinar risco de crescimento do conjunto `_seen` em processos de longa duração e uso de entradas não confiáveis.
- Revisar dependências e licenças de terceiros separadamente. Nenhum problema acima foi reproduzido.

## Relevância para SECA
Aproveitáveis **como conceitos a estudar**, não como implementação nesta fase: persistência resistente a falhas, tratamento explícito de dados corrompidos, separação entre estado e configuração, normalização tipada e preservação de proveniência. Uma infraestrutura de auditoria pode usar esses princípios sem integrar MemPalace ao núcleo cognitivo. Preservar núcleo biológico offline sem modelos pré-treinados e sem ensino de linguagem.

## Cobertura e continuidade
O manifesto anterior documentava **20 caminhos distintos** com registro até EOF entre **851 entradas** (inclui um symlink). Os cinco caminhos acima são novas evidências nesta etapa, **sujeitas a reconciliação contra o manifesto e relatórios concorrentes**. Não atualizar o percentual certificado sem esse confronto; nenhuma auditoria semântica completa foi certificada. Próximos caminhos: `mempalace/write_routing.py`, `mempalace/hub_client.py`, testes de configuração e persistência. Ruflo ainda não iniciado.
