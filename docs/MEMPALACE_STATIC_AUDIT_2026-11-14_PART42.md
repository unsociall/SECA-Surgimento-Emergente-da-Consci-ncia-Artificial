# SECA — MemPalace, auditoria estática Parte 42 (2026-11-14)

## Proveniência
- Origem: https://github.com/MemPalace/mempalace
- Commit fixado: `f8e35362189bd0a5abf4c0df1dd5bf90ba059176`
- Arquivo: `tests/test_sqlite_exact_backend.py`
- Git blob SHA retornado pela API: `d7ea8b2718c35261a5183771ec3c00a7e92ccb19`
- Leitura nesta etapa: intervalos solicitados 1201–1550, 1551–1950, 1951–2400 e 2401–3000; o último retornou conteúdo vazio. Os três primeiros retornaram conteúdo; o arquivo termina no intervalo 1951–2400.
- Partes 40 e 41 documentaram intervalos 1–440 e 441–1200, respectivamente. A combinação constitui cobertura declarada por intervalos do arquivo, mas a integridade dos intervalos anteriores não foi revalidada nesta etapa.
- Testes executados: zero. Nenhuma instalação, execução, clone para Termux ou modificação do núcleo SECA.

## Contratos observados nos testes (não validação da implementação)
1. Cache de matrizes vetoriais: filtros de igualdade reutilizam matriz; adições locais e gravações por outro handle devem invalidar resultados antigos.
2. Organização de metadados: contagens por wing/room/hall e índices de locus e `source_file`; migração de esquemas anteriores deve preencher colunas e índices.
3. Desempate estável em top-k e consultas somente-leitura durante lease de escritor, incluindo SQLiteExact e RustExact.
4. Leitores imutáveis devem reabrir após ciclo de escrita/checkpoint; leitura de esquema legado não deve criar WAL nem migrar banco sob lock de escritor.
5. Assinatura de banco deve detectar alterações mesmo quando estatísticas de arquivo permanecem constantes.
6. Wrappers aposentados podem reconectar; fechamento explícito deve continuar impedindo uso.
7. Uma consulta em lote precisa refazer o lote inteiro se o banco mudar entre ranking e hidratação, evitando resultados de snapshots misturados.
8. Atualização exclusiva de metadados deve preservar documento, embedding e índice FTS; contagens devem respeitar collection_id.
9. Iteração de metadados evita paginação por OFFSET para pré-buscas; índices FTS devem manter rowid sincronizado e migrar bancos antigos.
10. Filtros de igualdade e inclusão possuem caminhos otimizados, mas entradas com NUL, surrogate e valores nulos exigem semântica consistente.
11. Recuperação temporal compara ordenação exata com oráculo de varredura completa, considerando fusos, timestamps com formatos mistos, aliases e ausência de datas; índices de recência são adicionados em abertura gravável, não em somente-leitura.

## Riscos e limites
- O uso de testes com `subprocess`, `monkeypatch` e `EXPLAIN QUERY PLAN` foi apenas lido, nunca executado.
- Testes expressam intenção, não prova de segurança, atomicidade ou desempenho em produção.
- O intervalo final vazio sustenta EOF antes da linha 2401, mas o número exato da última linha não foi apurado aqui.
- Manifesto histórico de 851 caminhos ainda precisa de reconciliação individual de evidências e hashes. Cobertura global: **não certificada**.

## Possibilidades para SECA — somente estudo
- Especificar snapshots coerentes para recuperação de episódios, com invalidação de caches após mutações.
- Separar metadados fisiológicos/temporais do conteúdo de experiência e exigir atualização atômica.
- Criar oráculos determinísticos para ordenação temporal com relógios e fusos divergentes.
- Projetar recuperação após interrupção e isolamento de experiências sem acoplar buscas linguísticas ou embeddings pré-treinados.

Nenhum componente MemPalace foi incorporado; o núcleo biológico offline sem modelos pré-treinados e sem ensino de linguagem permanece inalterado. Ruflo só será iniciado após conclusão verificável do inventário e análise MemPalace.
