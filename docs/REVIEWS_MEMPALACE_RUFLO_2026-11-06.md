# SECA — Análise preliminar: MemPalace e Ruflo
Data: 2026-11-06
Status: **triagem técnica, não leitura integral do código**.

## Fontes verificadas
- https://github.com/MemPalace/mempalace
- https://mempalaceofficial.com/reference/modules
- https://github.com/MemPalace/mempalace/blob/develop/docs/HISTORY.md
- https://github.com/ruvnet/ruflo
- https://github.com/ruvnet/ruflo/blob/main/v3/README.md

## MemPalace
Sistema local-first de armazenamento literal de histórico e busca por similaridade, com backends configuráveis. Documentação identifica `mempalace/backends/base.py` como contrato dos backends; ChromaDB é padrão, com SQLite, Rust, Milvus, Qdrant e pgvector opt-in. Possui grafo temporal de entidades em SQLite, organização wings/rooms/drawers, MCP, mineração de conversas e diários por agente.

### Evidência e cautelas
README anuncia 96,6% R@5 bruto no LongMemEval (500 questões), 98,4% R@5 híbrido em 450 questões de teste; **não reproduzido por SECA**. R@5 mede recuperação documental, não memória episódica humana nem consciência. Algumas configurações usam modelos pré-treinados de embeddings (embeddinggemma/minilm); **não introduzir esses modelos no núcleo neural experimental SECA**. O histórico do projeto documenta correções públicas de alegações e segurança; auditar versão e dependências antes de executar.

### Aproveitamento proposto
Memória *externa de laboratório* para protocolos, commits, logs, dados, falhas e proveniência. Preferir primeiro SQLite e arquivos texto sem embeddings, com busca lexical determinística; só considerar embeddings em ferramentas de pesquisa externas, claramente isoladas do cérebro simulado.

## Ruflo
Framework de orquestração de agentes para CLI/MCP, com roteamento de tarefas, swarms, memória compartilhada, hooks, segurança e suporte a múltiplos provedores LLM. Documentação v3 descreve módulos memory/swarm/security, padrões microkernel, event sourcing e armazenamento híbrido SQLite/AgentDB.

### Evidência e cautelas
README anuncia centenas de ferramentas/agentes e ganhos de desempenho; **não reproduzidos por SECA**. A arquitetura depende de modelos LLM externos para tarefas cognitivas. Não integrar Ruflo ao cérebro experimental; usar apenas como inspiração para automação de engenharia, com revisão humana e rastreabilidade.

### Aproveitamento proposto
Orquestração de pipeline: pesquisador → implementador → executor de testes → auditor → publicador. Cada tarefa com artefatos, evidências, revisão e bloqueio de publicação em caso de falha. Manter agente e simulação separados.

## Decisões
1. **Não copiar nem instalar diretamente** nenhum dos projetos no núcleo experimental.
2. Criar armazenamento externo de experimentos em SQLite com identificador, hipótese, commit, dataset, parâmetros, comando, resultado, limitações e timestamp.
3. Criar pipeline determinístico de execução de testes e verificação de publicação, inspirado no Ruflo.
4. Só marcar análise integral como concluída após leitura de arquivos relevantes, revisão de licença, dependências, testes e benchmark independente.
5. Preservar simulações offline, sem LLMs pré-treinados ou ensino de linguagem.

## Próxima inspeção de código
MemPalace: `mempalace/backends/base.py`, `mempalace/knowledge_graph.py`, `mempalace/searcher/`, `benchmarks/BENCHMARKS.md`, testes.
Ruflo: módulos de `v3/@claude-flow/memory`, `swarm`, `security`, event sourcing, testes e relatórios de benchmark.

Este levantamento é arquitetura e documentação; nenhum benchmark nem teste de integração foi executado nesta etapa.
