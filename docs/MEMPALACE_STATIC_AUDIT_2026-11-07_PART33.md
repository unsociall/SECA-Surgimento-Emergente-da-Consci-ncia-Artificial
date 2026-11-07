# MemPalace — auditoria estática, parte 33 (2026-11-07)

## Escopo e proveniência
Origem: MemPalace/mempalace; commit imutável `f8e35362189bd0a5abf4c0df1dd5bf90ba059176`.
Árvore Git recursiva consultada: `truncated=false`, 851 entradas do tipo blob. Este número é o denominador do inventário, **não** uma medição de cobertura auditada.

Arquivos lidos integralmente nesta etapa:
- `tests/test_backend_conformance.py`, blob `fa134d22ea5cc5d7e0cf7c4228b2e4c10f1deb49` (5.582 bytes na árvore).
- `tests/_backend_conformance.py`, blob `03d9602cf6b422a1d78f74583c100651bc59bfd1` (tamanho não aferido nesta etapa).

Conferência cruzada sem contagem adicional: `tests/test_env.py` (blob `289966ba233d6b15c508360127b4fbad3583748d`) e `mempalace/_once.py` (blob `c604d91eb7a9f1504dcf6459304ed0cf92170b11`). `tests/test_once.py` retornou 404, não é evidência de leitura.

## Contratos observados no código de testes
A suíte parametriza Chroma, SQLiteExact e RustExact. Os testes verificam isolamento por `PalaceRef.id` em `query/get/count/delete`; atualização sem criação implícita de IDs ausentes; equivalência de filtros de metadados; rejeição de lotes com colunas de tamanhos diferentes; comportamento do `BaseCollection.update`; rejeição explícita de namespace não suportado; e não divulgação falsa da capability `supports_namespace_isolation`.

O módulo auxiliar inclui uma matriz de filtros ($eq, $in, comparações, $and, $or, $ne, $nin), com semântica explícita para campos ausentes. Para mecanismos que não reproduzem essa semântica, há parâmetro de exclusão dos casos de campo ausente. A verificação de isolamento usa uma sonda com ID fixo e confere que uma exclusão na partição B não remove a entrada na A.

## Limites de evidência
**Nenhum teste foi executado.** A existência das asserções não prova que os backends as satisfazem, nem que o isolamento é resistente a adversários. A matriz de testes não cobre, por si só, concorrência, falhas de energia, bypass por caminho alternativo ou ACL de sistema operacional. O uso de `MagicMock` no teste de upsert prova somente a forma esperada da chamada, não a atomicidade real de armazenamento.

## Relevância ao SECA (propostas, sem implementação)
1. Definir contrato de isolamento por instância e por domínio de memória, com negativa explícita quando a capacidade não existir.
2. Proibir atualização que crie silenciosamente uma experiência inexistente.
3. Validar integralmente lotes antes de persistir alterações de memória episódica.
4. Especificar semântica de campos ausentes e filtros antes de escolher mecanismo de armazenamento.
5. Exigir testes adicionais de concorrência, corrupção e recuperação em fase posterior, fora da auditoria exclusivamente estática.

Não importar embeddings, modelos pré-treinados, dependências de linguagem ou backends do MemPalace para o núcleo biológico offline.

## Estado
Manifesto global e cobertura integral: **não certificados**. Não inferir percentual a partir da contagem de relatórios. Ruflo permanece bloqueado até reconciliação e auditoria integral do MemPalace.
