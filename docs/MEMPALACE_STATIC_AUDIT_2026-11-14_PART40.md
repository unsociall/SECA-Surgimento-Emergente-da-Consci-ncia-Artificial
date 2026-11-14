# MemPalace — auditoria estática, parte 40 (14/11/2026)

## Escopo e rastreabilidade
- Repositório de origem: `MemPalace/mempalace`.
- Commit fixado: `f8e35362189bd0a5abf4c0df1dd5bf90ba059176`.
- Arquivo: `tests/test_sqlite_exact_backend.py`.
- Blob Git SHA conferido via leitura no commit: `d7ea8b2718c35261a5183771ec3c00a7e92ccb19`.
- Trechos efetivamente lidos nesta etapa: linhas **1–440**, inclusive; **leitura parcial**. O restante não foi examinado nesta etapa.
- Referência: https://github.com/MemPalace/mempalace/blob/f8e35362189bd0a5abf4c0df1dd5bf90ba059176/tests/test_sqlite_exact_backend.py#L1-L440
- Nenhum teste ou código do projeto foi executado. Nenhuma instalação ou alteração no dispositivo do usuário.

## Evidências do trecho
1. Os testes de inclusão, consulta, filtragem, atualização, reabertura e persistência verificam a API SQLiteExact (linhas 37–96).
2. O teste de IDs duplicados em um mesmo lote espera falha e contagem zero, caracterizando uma expectativa de rollback do lote (linhas 98–110).
3. Operações de escrita e consulta com dimensões vetoriais incompatíveis devem lançar `DimensionMismatchError`, mantendo o registro existente (linhas 112–129).
4. A consulta por IDs deve preservar a ordem requisitada e IDs repetidos; filtros devem intersectar a lista de IDs (linhas 131–178).
5. Testes de paginação examinam SQL rastreado, verificando `LIMIT/OFFSET`, limites negativos tratados por fatiamento Python, `limit=0` e consultas por chave primária (linhas 180–333).
6. Há teste de isolamento entre coleções com o mesmo ID de documento, incluindo upsert e exclusão filtrada (linhas 335–358).
7. Busca lexical inclui caminho FTS e fallback Python; outro teste busca evitar perda de resultados quando filtros são aplicados após a janela lexical (linhas 360–408).
8. Testes de filtros lógicos e fechamento de coleções aparecem nas linhas 410–433. O teste de abertura read-only inicia nas linhas 435–440, mas não foi lido por completo.

## Limites de inferência
Os testes expressam expectativas, não comprovam sua aprovação ou a correção da implementação. A análise da suíte inteira permanece **pendente**. Não há porcentagem global certificada. O manifesto histórico de 851 blobs requer reconciliação arquivo a arquivo; a leitura parcial deste arquivo **não** deve ser contada como integral.

## Relevância potencial ao SECA
- Candidato conceitual: invariantes de atomicidade de gravações episódicas, isolamento entre espaços de memória e ordenação determinística da recuperação.
- Testes de limites de paginação e de leitura somente ajudam a definir contratos próprios de persistência e recuperação.
- Os vetores e a busca lexical deste projeto não devem ser transplantados como requisitos do núcleo experimental do SECA: o núcleo deve permanecer offline, sem modelos pré-treinados e sem ensino de linguagem.
- **Decisão nesta fase:** somente documentação e auditoria; nenhuma integração.

## Próxima ação
Continuar a leitura do mesmo arquivo a partir da linha 441, até o fim, e então atualizar a reconciliação do manifesto com evidências completas. Ruflo permanece bloqueado até a conclusão verificável do MemPalace.
