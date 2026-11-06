# SECA — Auditoria MemPalace, parte 5: backend SQLite e testes numéricos

Data: 2026-11-06. Fonte: https://github.com/MemPalace/mempalace

## Leitura
`mempalace/backends/sqlite_exact.py` linhas 1–1200, SHA de blob `427287c1213de009141a5bcaf24188c1f10b807e`. **Parcial**: EOF não confirmado.

## Análise
- `_cursor(write=True)`: rollback em exceção; incremento da geração apenas se transação iniciada; limpeza de caches após escrita.
- `_ensure_collection_dimension`: valida dimensões dos vetores para impedir misturas incompatíveis.
- `_rows`: filtros simples executados no SQL parametrizado; filtros Python exigem paginação após filtragem.
- `_write_lock`: serialização por handle antes de lease entre processos.
- `_cosine_distances`: distância de cosseno exata com recálculo float64 quando produtos ou denominadores float32 apresentam condições numéricas perigosas.

## Testes numéricos independentes — executados em ambiente isolado Python/NumPy
Foi reproduzida a lógica da função `_cosine_distances` a partir do código consultado, **sem importar nem executar o pacote MemPalace**. Comparação com tolerância absoluta 1e-5.

| Caso | Esperado | Obtido | Resultado |
|---|---:|---:|---|
| idêntico | 0 | 0 | passou |
| ortogonal | 1 | 1 | passou |
| oposto | 2 | 2 | passou |
| vetor zero | 1 | 1 | passou |
| magnitude 1e30 | 0 | 0 | passou |
| magnitude 1e-30 | 0 | 0 | passou |

**Limites:** teste reproduzido não substitui teste direto no código-fonte nem a suíte oficial. Não cobre integração SQLite, concorrência, migração, falhas de disco ou todos os casos de ponto flutuante.

## Aplicação SECA
Propor testes numéricos de referência para rotinas de comparação de estados; não pressupor que embeddings representem atividade neural biológica.

## Próximos passos
Confirmar EOF de `sqlite_exact.py`, mapear as funções restantes, auditar casos de teste de SQLite e registrar um manifesto versionado de arquivos. Ruflo permanece pendente.
