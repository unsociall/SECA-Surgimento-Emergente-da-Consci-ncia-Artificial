# SECA — M011: análise de MemPalace e Ruflo e protótipo de rastreabilidade
Data: 2026-11-06.

> Atualização do protótipo de evidências: [M012](M012_NUMERICS_CI_EVIDENCE.md) adiciona checksum versionado do contexto e migração preservando registros antigos. Os testes e limites abaixo descrevem a versão inicial.

## Escopo e proveniência
Análise de README, mapa de módulos e documentação pública. **Não houve leitura integral de todos os arquivos de ambos os repositórios, instalação ou reprodução de seus benchmarks.** Não alegar integração dos projetos completos.

## MemPalace
- Código: https://github.com/MemPalace/mempalace
- Mapa de módulos: https://mempalaceofficial.com/reference/modules
- Contrato de backends (`mempalace/backends/base.py`) separa armazenamento de busca; implementações incluem ChromaDB e SQLite.
- `knowledge_graph.py` mantém relações com validade temporal em SQLite; `layers.py` organiza níveis de memória; `searcher/` combina recuperação lexical e vetorial.
- README anuncia 96,6% R@5 no LongMemEval, resultado **não reproduzido**. R@5 não mede cognição biológica.
- Modelos de embedding pré-treinados são incompatíveis com o núcleo neural experimental; memória documental externa é admissível.

## Ruflo
- Código: https://github.com/ruvnet/ruflo
- README descreve workflows, agentes especializados, memória, hooks, auditoria e automação. A instalação CLI pode criar arquivos e hooks no workspace; não instalar sem auditoria.
- Componentes de interesse: `ruflo-workflows`, `ruflo-swarm`, `ruflo-docs`, `ruflo-testgen`, `ruflo-security-audit`.
- Métricas anunciadas pelo projeto não foram reproduzidas. Não incluir agentes LLM no cérebro experimental.

## Decisão de arquitetura
Separar dois domínios:
1. **Laboratório externo**: indexação de experimentos, proveniência, agentes de pesquisa, revisão e publicação.
2. **Núcleo SECA**: modelos de células e circuitos neurais offline, sem modelos pré-treinados nem linguagem ensinada.

## Protótipo M011
`experiments/evidence/evidence_store.py`: SQLite com registros imutáveis por ID, serialização JSON canônica, hash SHA-256 e consulta por experimento. Hash identifica alterações acidentais; **não oferece autenticação nem proteção contra um atacante que modifique simultaneamente o registro e o hash**.

Comando: `cd experiments/evidence && python -m unittest -v`.

Nove testes executados localmente e aprovados em 2026-11-06, para versão equivalente do módulo: roundtrip, hash determinístico, duplicatas, identificador inválido, NaN, filtragem, ausência, persistência e adulteração simples. Os arquivos publicados devem ser reexecutados em CI para confirmação independente.

## Próximos incrementos
- M012: registrar versões de dataset, commit, parâmetros e ambiente de execução, com exportação JSONL e backups.
- Auditar os módulos relevantes dos dois repositórios arquivo a arquivo, com licença, dependências e testes.
- Criar pipeline de revisão com gates obrigatórios: teste → relatório → auditoria → publicação.
- Não misturar histórico documental com engramas ou memória biológica simulada.
