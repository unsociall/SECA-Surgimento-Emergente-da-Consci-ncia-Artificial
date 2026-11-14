# SECA — MemPalace auditoria estática, parte 38 (2026-11-14)

## Escopo e proveniência
Repositório de origem: https://github.com/MemPalace/mempalace
Commit fixado: `f8e35362189bd0a5abf4c0df1dd5bf90ba059176`.
Arquivo integralmente lido nesta etapa: `mempalace/backends/_magic.py` — blob Git `155347fd9b10e7d80d1b535683ef0726bd23b581`.
`mempalace/backends/sqlite_exact.py` foi consultado apenas parcialmente nesta etapa; **não** é contabilizado como leitura integral.
Método: inspeção de texto via API do GitHub, sem importar módulos, instalar dependências ou executar testes.

## Análise do código de _magic.py
- `_stat_regular_file` rejeita caminhos inexistentes e tipos que não sejam arquivos regulares, mas segue links simbólicos via `os.stat`.
- `read_header_fields` coleta cinco PRAGMAs SQLite usando URI `mode=ro&immutable=1` e permite consulta adicional parametrizada. O retorno `None` não distingue erro de formato, ausência de conteúdo e outras falhas SQLite; exceções de `os.stat` são propagadas.
- `has_sqlite_magic` usa cache positivo por par `(st_dev, st_ino)`, não armazena negativos e conserva conexões de sondagem em POSIX. Em Windows fecha conexões após a sondagem. No fallback, lê diretamente 16 bytes quando SQLite recusa a abertura; logo, um prefixo válido não comprova integridade do banco.
- `forget` limpa apenas `_positive`; não fecha conexões em `_retained_conns`. `close_retained` fecha conexões retidas, mas não limpa `_positive`. Esses contratos distintos exigem documentação cuidadosa.
- Risco a investigar: cache positivo por inode pode continuar verdadeiro após alteração **in-place** do conteúdo, porque a chave não incorpora tamanho, mtime nem geração. É uma inferência estática; impacto real depende dos chamadores e da mutabilidade dos arquivos.
- Risco a investigar: `read_header_fields` sempre fecha a conexão temporária; a justificativa do módulo sobre retenção de conexões POSIX se aplica explicitamente a `has_sqlite_magic`. Verificar os chamadores e a interação com SQLite de bibliotecas nativas antes de concluir segurança de locks.
- Risco a investigar: em `has_sqlite_magic`, a consulta `os.stat` e o uso subsequente do caminho não são atômicos; mudanças concorrentes do arquivo podem invalidar a identidade usada no cache.
- A documentação do módulo explica risco de liberação de locks POSIX ao fechar descritores de mesmo inode e a distinção entre SQLite da biblioteca Python e SQLite embutido no Chroma. Essa explicação é hipótese técnica do código, não validação experimental desta auditoria.

## Relevância ao SECA
Separar identidade de arquivo, reconhecimento de formato, verificação de integridade e persistência de memória episódica. Para futura arquitetura própria, prever detecção de substituição/alteração, invariantes de concorrência, limites de recursos de conexões retidas e tratamento explícito de falhas. Não importar código, embeddings ou modelos de linguagem do MemPalace.

## Evidência e cobertura
Manifesto incremental:
| Caminho | Blob SHA | Estado | Evidência |
|---|---|---|---|
| `mempalace/backends/_magic.py` | `155347fd9b10e7d80d1b535683ef0726bd23b581` | lido integralmente nesta etapa | este relatório |
| `mempalace/backends/sqlite_exact.py` | não certificado nesta etapa | parcial, sem contagem | leitura exploratória |

O total histórico de 851 blobs ainda precisa ser reconciliado contra a árvore completa do commit e relatórios anteriores; **nenhuma porcentagem global certificada**. Ruflo aguarda conclusão integral do MemPalace. Testes executados: zero. Nenhuma alteração ao núcleo SECA.
