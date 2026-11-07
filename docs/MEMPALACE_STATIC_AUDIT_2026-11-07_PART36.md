# MemPalace — Auditoria estática, parte 36 (2026-11-07)

## Escopo e evidência
Repositório: MemPalace/mempalace
Commit fixado: `f8e35362189bd0a5abf4c0df1dd5bf90ba059176`
Arquivo: `mempalace/backends/base.py`
Blob Git SHA obtido pela leitura via API: `e4b170e99084d952ce97d22283764aee5f45ef51`.
Leitura realizada por duas faixas contíguas (linhas 1–500 e 501–1100), cobrindo o arquivo de 983 linhas informado no registro anterior. Somente inspeção de texto; nenhum módulo importado, teste executado ou componente instalado.

## Contratos observados
- `PalaceRef.id` é a chave obrigatória de isolamento; namespace só é permitido quando o backend declara suporte e deve ser rejeitado caso contrário.
- `QueryResult` e `GetResult` padronizam formatos de retorno; existe camada transitória de compatibilidade com dicionários.
- `validate_write_batch` verifica comprimentos de colunas e, opcionalmente, duplicidade de IDs.
- `check_embedder_identity` diferencia identidade desconhecida, compatível e incompatível, com opção explícita de troca forçada. Este contrato está associado a embeddings e não é candidato ao núcleo biológico não linguístico do SECA.
- `get_all_metadata` e `get_all_rows` usam paginação com offset. O próprio contrato alerta para custo quadrático em backends que materializam tudo a cada página.
- `get_recent` padrão limita a leitura aos primeiros `limit` registros em ordem de armazenamento e só então ordena por data: não garante os eventos globalmente mais recentes em coleções maiores.
- `update` padrão usa leitura, mesclagem e upsert, sem transação abrangendo o ciclo completo. A afirmação de atomicidade do upsert depende da implementação concreta; não implica isolamento contra escritas concorrentes.
- `run_maintenance` requer serialização de trabalhos do mesmo tipo e sinalização de `already_running`, mas a classe-base apenas rejeita operações não suportadas.
- Métodos padrão `health` retornam saudável e `close` pode ser no-op; são contratos, não provas de saúde ou liberação de recursos.
- `_IncludeSpec.resolve` filtra chaves não reconhecidas, em vez de rejeitá-las; avaliar se projeções inválidas deveriam falhar explicitamente.

## Riscos e questões pendentes
1. Confirmar nos backends concretos se isolamento por ID/namespace é realmente aplicado.
2. Verificar se atualização anunciada como atômica usa transação e bloqueios adequados.
3. Verificar consistência sob mutação concorrente durante paginação por offset.
4. Auditar implementações de recência e suporte a filtros com garantias verificáveis.
5. Avaliar se `health` e `close` são sobrescritos de maneira observável.

## Relevância ao SECA
Adaptação conceitual futura, sem implementação nesta fase: interfaces de memória tipadas, isolamento explícito de experiências, validação antes de gravar, snapshots consistentes, ordenação temporal correta e telemetria de manutenção. Não reutilizar embeddings, modelos pré-treinados, ensino de linguagem, nem mecanismos de rede no núcleo biológico offline.

## Cobertura
Arquivo desta etapa: leitura estática integral por faixas contíguas; hash de blob registrado.
Inventário histórico da árvore: 851 blobs (a reconciliar com evidências de cada arquivo). Cobertura global **não certificada**. Ruflo **não iniciado**.
