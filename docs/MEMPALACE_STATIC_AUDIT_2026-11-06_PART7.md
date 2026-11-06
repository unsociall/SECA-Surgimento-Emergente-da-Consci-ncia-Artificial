# SECA — Auditoria MemPalace, parte 7: testes SQLite (2026-11-06)

Fonte: https://github.com/MemPalace/mempalace/blob/f8e35362189bd0a5abf4c0df1dd5bf90ba059176/tests/test_sqlite_exact_backend.py

## Evidência
`tests/test_sqlite_exact_backend.py`, SHA blob `d7ea8b2718c35261a5183771ec3c00a7e92ccb19`, linhas 1–700 consultadas. **Arquivo parcial**, EOF não verificado. Consulta de busca identificou commit `f8e35362189bd0a5abf4c0df1dd5bf90ba059176` no índice; leituras por fetch não foram fixadas explicitamente nesse ref, portanto não assumir identidade de commit.

## Testes encontrados
- Falha de escrita deve reverter lote inteiro; dimensão de vetores incompatível deve ser recusada.
- Recuperação por IDs deve preservar ordem e duplicações, com filtros aplicados corretamente.
- `LIMIT/OFFSET` SQL devem evitar leituras desnecessárias e manter paginação.
- FTS lexical deve ter fallback Python; filtros devem ser aplicados corretamente.
- Coleções distintas devem permanecer isoladas.
- Leitura `read_only` deve rejeitar escrita, evitar inicialização de esquema e não alterar arquivos.
- Leitor read-only deve observar WAL ativo e reabrir quando WAL aparece após conexão immutable.
- Cache de leitor immutable não deve ser descartado por sidecar WAL incompleto.
- Escrita deve disputar a lease de outro processo e thread em espera deve readquirir lease válida.

## Avaliação
A suíte contém casos relevantes para persistência, concorrência, integridade de leitura e recuperação. **Os testes foram inspecionados, não executados.** A existência de um teste não prova sua aprovação. Antes de alegar conformidade: executar em ambiente de teste isolado, capturar versões, saída pytest e SHA do checkout.

## Próximas ações
Ler o restante da suíte, examinar código dos métodos sob teste e comparar com casos de falha; construir inventário do repositório e medir cobertura. Nenhuma instalação no Termux ou integração ao SECA.
