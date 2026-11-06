# MemPalace — auditoria estática complementar (2026-11-06)

## Escopo e evidência
- Repositório: MemPalace/mempalace
- Commit fixado: `f8e35362189bd0a5abf4c0df1dd5bf90ba059176`
- Arquivo `tests/test_sqlite_exact_backend.py`: linhas 1–170 consultadas nesta etapa; blob SHA `d7ea8b2718c35261a5183771ec3c00a7e92ccb19`. O histórico anterior relata leitura completa; esta etapa não revalida essa cobertura integral.
- Arquivo `mempalace/backends/sqlite_exact.py`: linhas 1–180 consultadas nesta etapa; blob SHA `427287c1213de009141a5bcaf24188c1f10b807e`. **Leitura parcial; não contar como arquivo integralmente auditado.**
- Inventário total do commit: ainda não estabelecido; cobertura global: indeterminada.

## Observações confirmadas no código
1. Backend local SQLite armazena vetores como blobs float32; descreve busca exata por distância cosseno, com numpy e cache de matriz.
2. A geração de escrita (`write_generation`) é incrementada por SQL na transação, para detectar atualizações em leitores imutáveis.
3. Há índices por localização lógica (`wing`, `room`, `hall`), por arquivo de origem e por data de arquivamento.
4. O filtro de igualdade pode ser traduzido em SQL; operadores mais complexos seguem caminho Python, conforme docstring. O restante da implementação ainda requer inspeção.
5. Testes cobrem rollback de lote duplicado, dimensão de vetor, persistência após reabertura, filtros e ordenação de IDs.

## Relevância e limites para SECA
- Candidato conceitual: log de experiências com transações atômicas, geração monotônica para invalidação de cache, índices estruturais e testes de consistência.
- Não adotar embeddings, linguagem, modelos pré-treinados nem MemPalace como núcleo cognitivo. Os exemplos textuais são dados de teste do projeto externo.
- Nenhum teste foi executado. Não há conclusão sobre comportamento real, segurança global ou licenças.

## Próximos passos
Completar leitura de `sqlite_exact.py`, validar invariantes contra os testes, levantar árvore integral no commit, revisar dependências/licenças/segurança, só depois avançar para Ruflo.
