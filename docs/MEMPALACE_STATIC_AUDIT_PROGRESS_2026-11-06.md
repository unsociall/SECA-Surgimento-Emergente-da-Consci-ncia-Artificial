# SECA — Progresso de leitura estática MemPalace (2026-11-06)

> **Registro histórico inicial.** O [estado consolidado](MEMPALACE_STATIC_AUDIT_STATUS.md) contém o commit fixado, o inventário completo e as leituras acumuladas. As pendências deste registro descrevem seu momento de elaboração.

## Escopo e integridade
Fonte: https://github.com/MemPalace/mempalace, leitura pela integração GitHub, sem instalação, execução ou download para Termux. **SHA abaixo é SHA de blob de arquivo, não commit fixado de repositório.** Inventário completo pendente.

| Caminho | Intervalos consultados | Blob SHA | Estado |
|---|---|---|---|
| `mempalace/backends/base.py` | 1–1100 (última consulta alcançou EOF antes do limite) | `e4b170e99084d952ce97d22283764aee5f45ef51` | cobertura de leitura por intervalos completa; revisão aprofundada pendente |
| `mempalace/embedding.py` | 1–1200 | `56a54ababc75d6d60370be7f6208db2d94099558` | parcial; verificar EOF e continuar |

**Observação:** as consultas retornaram todo o texto de cada intervalo, mas parte foi resumida na análise; isso não equivale a auditoria linha a linha concluída.

## Descobertas verificadas no código
- `PalaceRef` estabelece isolamento por ID e opcionalmente namespace; backends sem suporte devem rejeitar namespace.
- `check_embedder_identity` compara nome de modelo e dimensão e falha em conflito, exceto quando troca é explicitamente autorizada.
- `QueryResult` e `GetResult` fornecem resultados tipados e compatibilidade transitória com dicionários.
- `BaseCollection` define `add`, `upsert`, `query`, `get`, `delete`, `count`; recursos opcionais devem sinalizar falta de suporte.
- `embedding.py` controla cache e concorrência de sessões, seleção de providers ONNX, fallback CPU, identificação de vetores degenerados e ordenação de documentos por tamanho para reduzir padding.
- Regras de versão ONNX evitam leitura de pesos externos a partir de caminhos incorretos em versões antigas.

## Relevância para SECA
Aproveitar como **conceitos de engenharia**: isolamento de experimentos, contratos de armazenamento, validação de representação, resultados tipados, detecção de falhas numéricas e serialização de tarefas concorrentes. Não transportar embeddings pré-treinados para o cérebro experimental.

## Progresso honesto
- Dois arquivos centrais consultados em intervalos extensos.
- Cobertura total do repositório: **não mensurável ainda** (manifesto ausente).
- Ruflo: **não iniciado nesta sequência**, conforme ordem solicitada.
- Nenhum teste executado, nenhuma instalação ou integração feita.

## Próximos passos
1. Finalizar `embedding.py`, confirmar EOF e revisar fluxos relevantes.
2. Inventariar o repositório inteiro em um commit fixo.
3. Seguir arquivos de backend, grafo temporal, busca, testes e benchmarks com checklist verificável.
