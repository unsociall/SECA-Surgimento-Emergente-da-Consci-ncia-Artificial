# SECA — Auditoria estática MemPalace — Parte 17 (2026-11-06)

## Escopo e proveniência
Repositório: MemPalace/mempalace. Commit fixado: `f8e35362189bd0a5abf4c0df1dd5bf90ba059176`.
Nesta etapa, conteúdo integral retornado pela API de arquivos para:

| Caminho | Blob Git SHA | Cobertura desta etapa |
|---|---|---|
| `tests/test_lexical.py` | `30380e3ca291830d58d6d18a38aa34bfe9e486e5` | arquivo integral retornado |
| `tests/test_timeutil.py` | `2a685bc11efa715ca4dbfba1b9caf12245617fea` | arquivo integral retornado |
| `tests/test_stored_text.py` | `5f604b91b7665c61464512365214213456c6420b` | arquivo integral retornado |

Os testes **não foram executados**; conclusões abaixo referem-se à intenção e às asserções do código. Não se certifica 100% de cobertura do repositório.

## Descobertas

### Busca lexical
`test_lexical.py` contém corpus de referência e resultados numéricos BM25 (golden tests), cobrindo Unicode, texto vazio, ausência de documentos, stop words e desempate de ranking. O próprio comentário registra a intenção de preservar resultados entre cinco implementações anteriores. Isso é evidência de testes de regressão, não de equivalência comprovada em execução.

### Tempo e ordenação
`test_timeutil.py` cobre horários legados sem timezone, horários UTC com offset, diferentes zonas, filtros de janela, busca BM25, índice temporal, diário, grafo de conhecimento e ordenação por sequência de inserção no logstream. Distinção essencial: ordem cronológica de instantes e ordem causal de anexação são conceitos diferentes; relógio pode retroceder.

### Integridade textual
`test_stored_text.py` testa round-trip de NUL, surrogate Unicode isolado e strings parecidas com escapes; impede que metadados fornecidos pelo chamador falsifiquem a flag interna; verifica leituras e atualizações em SQLite Exact e Chroma, filtros por valores codificados e índice textual próximo a caracteres escapados. Testes mostram contratos esperados; não provam ausência de falhas.

## Hipóteses de adaptação ao SECA (sem implementação)
1. Separar sequência causal monotônica de timestamps de parede para experiências.
2. Especificar invariantes de preservação reversível de dados sensoriais/eventos, inclusive caracteres inválidos em serialização.
3. Criar corpus de regressão determinística para algoritmos internos de recuperação de experiências, sem depender de BM25 ou embeddings como arquitetura cognitiva.
4. Preservar fronteiras entre registro bruto, índice derivado e apresentação externa.

## Pendências e restrições
Confrontar testes com implementação dos módulos, concluir manifesto integral por commit, auditar dependências, licenças, arquitetura e segurança. Ruflo aguarda auditoria integral do MemPalace. Nenhum código instalado, clonado para dispositivo, executado ou incorporado; núcleo experimental biológico offline sem modelos pré-treinados ou ensino de linguagem preservado.
