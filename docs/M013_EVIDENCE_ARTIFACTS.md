# M013 — exportação e backup verificáveis de evidências

Data: 2026-11-06. Base: `260e28bce71121dd3390211104af87ed22a9f5fb`.

## Objetivo e implementação

Completar a exportação e os backups previstos no protótipo de rastreabilidade M011, preservando os checksums e os escopos de integridade introduzidos em M012. O código é infraestrutura externa de laboratório; não representa memória neural simulada.

`EvidenceStore` oferece dois métodos novos:

| Método | Resultado | Verificações antes da publicação |
|---|---|---|
| `export_jsonl(destino, experiment=None)` | JSONL canônico, em ordem lexical de IDs, com filtro opcional | Cada registro é verificado em um único snapshot de leitura |
| `backup_sqlite(destino, timeout_s=10)` | Um arquivo SQLite reabrível, incluindo dados confirmados presentes no WAL da origem | API de backup SQLite, `quick_check` e verificação de cada registro da cópia |

A exportação percorre o cursor e serializa um registro por vez. Sua memória de serialização depende do tamanho do maior registro; o conteúdo completo do banco não é transformado em uma lista Python. A ordem dos IDs é determinística, e a interpretação causal dos eventos continua dependendo do protocolo experimental.

Os métodos retornam formato, caminho, quantidade de registros, quantidade de registros legados, tamanho em bytes, SHA-256 e os resultados de sincronização do arquivo e do diretório. O hash identifica os bytes do artefato publicado. Os registros legados continuam com versão 1 e `payload_only`; não recebem uma garantia de contexto que o registro original não possuía.

## Publicação e estados de falha

`evidence_io.py` cria um arquivo exclusivo no diretório de destino, prepara todo o conteúdo, sincroniza o arquivo, calcula o hash e só então substitui o destino com `os.replace`. Não existe fallback para truncar e regravar o arquivo anterior. Uma colisão de nome temporário falha sem reutilizar ou remover o arquivo encontrado.

Falhas anteriores à substituição preservam os bytes do destino anterior. A sincronização do diretório é tentada após a substituição; seu resultado aparece em `directory_fsynced`, separado de `file_fsynced`. Um resultado `False` não permite afirmar durabilidade da renomeação diante de perda de energia. Não houve teste físico de queda de energia.

Destinos que apontam para um banco aberto na conexão, seus arquivos auxiliares, um hardlink para eles ou um link simbólico são recusados. O diretório pai deve existir. O destino é um artefato inativo; ele não deve ser um banco aberto por outra aplicação. A guarda não descobre todas as conexões de outros processos.

Uma transação já aberta pelo chamador faz a operação falhar antes da criação do artefato; ela não é confirmada nem desfeita pelo método. A exportação cria e encerra sua própria transação de leitura. O backup usa outra conexão somente para a cópia, encerrada antes da publicação.

`timeout_s` é um prazo cooperativo verificado entre passos da cópia SQLite. Uma chamada bloqueante de SQLite ou do sistema de arquivos pode ultrapassá-lo; validação, hash e sincronização também consomem tempo. O prazo não é uma interrupção assíncrona de toda a operação.

## Validação executada

**138 testes locais aprovados em 11 suítes**, em Python 3.12.14 com SQLite 3.53.1. São 23 testes novos de artefatos, além dos 115 existentes. Comando: `python tools/run_tests.py` na raiz.

- [Resumo, ambiente e hashes dos fontes testados](validation/M013_test_summary.json).
- [Log completo da execução aprovada](validation/M013_unittest_python312.log).

Os casos novos verificam exportação determinística e filtrada, exportação vazia, validação de conteúdo e versão, preservação de transação do chamador, proteção de bancos e arquivos auxiliares, links, falha na criação do temporário, colisão de nome, falha de `fsync`, falha de substituição e comunicação da limitação de sincronização do diretório.

Também foram executados casos com uma escrita por outra conexão durante a exportação em WAL, backup de dados confirmados no WAL, reabertura da cópia sem arquivos auxiliares, banco em memória, preservação de registros legados e expiração simulada do prazo de cópia. Os testes de permissões POSIX passaram no ambiente local. Windows, Android físico e falhas físicas de armazenamento não foram validados nesta etapa.

Os bancos e arquivos usados nos testes eram temporários e sintéticos. Nenhum banco pessoal foi copiado ou alterado. Não foi criada uma rotina de restauração automática nem um agendamento de backups.

## Referências e limites

A implementação usa a API `Connection.backup` documentada pelo [Python](https://docs.python.org/3.12/library/sqlite3.html#sqlite3.Connection.backup) e o mecanismo descrito na [documentação SQLite](https://www.sqlite.org/backup.html) e em seu [contrato de API](https://www.sqlite.org/c3ref/backup_finish.html). A verificação dos registros e o protocolo de publicação são código próprio do SECA.

O estudo estático do MemPalace continuou em [15 arquivos de persistência e roteamento](MEMPALACE_AUDIT_PERSISTENCE_ROUTING_2026-11-06.md). Nenhum código desses arquivos foi copiado, instalado, importado ou executado. A auditoria de terceiros segue estática, e o Ruflo permanece na sequência após sua conclusão.

Este incremento melhora reprodução e conservação de evidências de software. Não acrescenta plasticidade, redes sinápticas ou validação biológica. A padronização automática de metadados de execução, datasets e parâmetros continua como trabalho posterior.

Elaboração, implementação e revisão com assistência do ChatGPT (OpenAI).
