# MemPalace — Auditoria estática, parte 25 (2026-11-07)

## Escopo e proveniência
Repositório de origem: MemPalace/mempalace. Ref de leitura: commit abreviado `f8e3536` (ainda é necessário resolver e registrar SHA completo do commit e a árvore integral para certificar cobertura). Acesso exclusivamente por leitura de arquivos via GitHub; nenhum código de terceiros foi executado, instalado ou importado ao SECA.

### Evidências desta etapa
| Caminho | Git blob SHA | Extensão do conteúdo recebido | Situação |
|---|---|---:|---|
| `mempalace/fsio.py` | `a8e8cf3bd40bec775d00c92c70bb0bbbc69ee033` | 20.476 caracteres | conteúdo integral recebido e analisado |
| `mempalace/paths.py` | `93a9028473ad3b6b4d80ae870e8de51bec32b14a` | 6.807 caracteres | conteúdo integral recebido e analisado |

**Atenção:** estes são dois arquivos examinados nesta etapa; não afirmar que são inéditos no manifesto consolidado antes de deduplicar por caminho e blob. Não existe denominador de árvore completa validado nesta etapa; cobertura percentual indeterminada.

## fsio.py — análise de algoritmos e segurança
- `atomic_publish`: arquivo temporário criado com `O_EXCL`, escrita, flush e fsync, `os.replace` e tentativa de fsync no diretório. Usa `O_NOFOLLOW` quando disponível na criação temporária.
- Exceção importante à atomicidade: quando `follow_symlinks=True` e há EACCES/EPERM/EROFS em criação/rename, pode recorrer a `write_in_place`, que trunca o destino antes de completar a gravação. Portanto, a garantia de não truncamento **não é universal**. A função emite aviso no stderr.
- `follow_symlinks=False` evita fallback in-place e impede seguir link simbólico no caminho final durante publicação, propriedade relevante para registros sensíveis.
- `read_json_for_update` recusa sobrescrever estado ilegível ou JSON inválido, preservando bytes via `move_aside` quando possível.
- `open_source_file` rejeita symlinks e arquivos não regulares; usa `O_NONBLOCK` para não bloquear em FIFO. Reabre sem nonblock sob EAGAIN em arquivo regular, com ressalvas de corrida de filesystem.
- `decode_source` preserva bytes com UTF-8, surrogateescape e fallback Windows-1252; heurística de detecção não garante identificação da codificação original. `universal_newlines=True` normaliza quebras de linha e portanto não mantém os bytes exatos nesse modo.
- A implementação de `fsync_directory` ignora falhas; a durabilidade real varia conforme SO e filesystem. Não foi verificada empiricamente.

## paths.py — análise de persistência e migração
- Separa configuração (preferência por variável de ambiente, instalação legada e XDG) de estado (`~/.mempalace`).
- `palace_key` usa SHA-256 do caminho canônico normalizado e 24 caracteres hexadecimais; chave de identificação, **não** autenticação.
- `knowledge_graph_path` prioriza grafo local com fatos; se vazio, pode apontar para grafo histórico com fatos. Não mescla grafos. Risco funcional a verificar: ambiguidade de localização durante migrações e coexistência de arquivos.
- `knowledge_graph_has_rows` trata erro de leitura ou consulta como potencial presença de dados, estratégia conservadora para evitar perda por troca indevida de arquivo.
- `canonical_palace_path` resolve links simbólicos; equivalência entre caminhos e migrações depende de sistema operacional e mudanças de montagem.

## Relação com server_registry.py
O registro de servidor usa `atomic_write_text` com comportamento padrão `follow_symlinks=True` para token e serverinfo; para `mesh_state` usa explicitamente `follow_symlinks=False`. Assim, a proteção contra substituição por symlink e o fallback de escrita **diferem** entre arquivos. O token remove symlink antes de gravar quando cria um novo token, mas a leitura e a reutilização do token existente precisam ser avaliadas em conjunto com permissões da pasta. Isso é uma hipótese de superfície de ataque local, não exploração demonstrada.

## Relevância ao SECA — somente proposta
1. Para checkpoints e memória episódica offline: gravação transacional sem fallback in-place em dados críticos; registro de versão, checksum e recuperação após falha.
2. Para estados ilegíveis: quarentena não destrutiva, sem substituição automática.
3. Para fontes de experiências: limitar tamanho, exigir arquivos regulares e preservar metadados de codificação quando necessário.
4. Para isolamento de experiências: caminhos canônicos, identificadores estáveis e distinção entre configuração e dados.
Nenhuma adaptação implementada.

## Pendências verificáveis
- Resolver SHA completo de `f8e3536`, obter árvore recursiva completa, registrar cada caminho/tipo/blob, marcar arquivos binários e submódulos separadamente.
- Reconciliar partes anteriores e deduplicar evidências antes de calcular porcentagem.
- Ler testes específicos de `fsio` e `paths`, dependências, licenças e demais arquivos da árvore; testes não executados.
- Não iniciar Ruflo até fechar integralmente o inventário e a análise MemPalace.
