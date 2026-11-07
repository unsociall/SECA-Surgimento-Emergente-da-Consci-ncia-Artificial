# SECA — MemPalace, auditoria estática parte 18 (2026-11-06)

## Referência verificável
- Repositório de origem: MemPalace/mempalace
- Commit fixado: `f8e35362189bd0a5abf4c0df1dd5bf90ba059176`
- Arquivo: `mempalace/backends/sqlite_exact.py`
- Blob SHA: `427287c1213de009141a5bcaf24188c1f10b807e`
- Trecho consultado nesta etapa: linhas 2101–fim do arquivo (pedido até 2450; retorno terminou em `__all__`). A cobertura acumulada das partes anteriores só pode ser certificada após confrontar os registros de leitura efetivos, sobretudo o intervalo 1701–2100.

## Evidências do trecho final
1. `get_collection` valida diretório, coleção e caminho local; usa bloqueio ao criar coleção e incrementa geração de escrita.
2. `_normalize_args` aceita três formas de invocação e rejeita argumentos inesperados.
3. `close_palace` invalida a geração de vida do caminho, remove handles dos registros e fecha conexões sob locks.
4. `close` sinaliza encerramento sob lock global, limpa registros e fecha handles individualmente.
5. `health` detecta backend fechado ou arquivo SQLite ausente, mas não constitui auditoria profunda da integridade do banco.
6. `detect` verifica assinatura SQLite, evitando a abertura de descritor simples que poderia afetar locks POSIX de conexões WAL existentes.
7. `delete_collection` tenta remover linhas FTS e ignora `sqlite3.OperationalError` nesse passo; em seguida exclui documentos e coleção e realiza commit. **Questão de auditoria:** avaliar a amplitude da exceção ignorada e a atomicidade sob falha, confrontando testes e código completo.

## Possibilidades para SECA
Estudar o controle de ciclo de vida de conexões, a proteção de locks de armazenamento e a distinção entre health-check superficial e verificação de integridade. Nenhuma proposta implica adotar embeddings, modelos pré-treinados ou ensino de linguagem. Núcleo biológico offline preservado.

## Status
Leitura exclusivamente estática. Nenhum teste executado, instalação ou alteração no núcleo. Manifesto global do MemPalace ainda não reconciliado; não declarar cobertura 100%. Ruflo não iniciado.
