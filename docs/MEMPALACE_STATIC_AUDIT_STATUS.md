# MemPalace → Ruflo — estado consolidado da auditoria

Atualização: 2026-11-06. **Auditoria estática em andamento.**

Este é o ponto de retomada. Os relatórios numerados preservam etapas anteriores; suas pendências locais não devem substituir automaticamente os registros acumulados de leitura.

## Referência fixa e inventário

- Repositório: https://github.com/MemPalace/mempalace
- Commit: `f8e35362189bd0a5abf4c0df1dd5bf90ba059176`.
- Árvore raiz: `701bc6b78262f25b2972b23ba106b30040b76aef`.
- [Manifesto de caminhos e hashes](audits/mempalace-f8e3536-inventory.json).
- [Evidências e observações da parte 14](MEMPALACE_STATIC_AUDIT_2026-11-06_PART14.md).

| Medida | Estado verificável |
|---|---|
| Entradas de arquivo inventariadas | 851, incluindo um link simbólico |
| Arquivos regulares / subdiretórios | 850 / 109 |
| Classificação provisória por caminho e modo | 846 candidatos a texto, quatro candidatos a mídia binária, um link |
| Novas leituras integrais nesta etapa | Seis arquivos |
| Registros anteriores de leitura até EOF | Sete arquivos, com identidade de blob conferida |
| Caminhos distintos com registro de leitura até EOF | 13 |
| Caminhos sem registro de leitura até EOF | 838 |
| Auditoria semântica integral / validação em execução | Não concluídas / não realizadas nesta etapa |

O inventário dos caminhos está completo. A leitura e a auditoria dos conteúdos continuam incompletas. A classificação de texto, mídia e geração é provisória; não houve inspeção de formato de toda a árvore. A contagem de leituras inclui documentação e configuração e não corresponde a um percentual de código auditado.

## Registro de leitura por caminho

| Caminho | Evidência | Pendência |
|---|---|---|
| `mempalace/backends/base.py` | EOF informado na parte 8; blob coincide com o commit | Revisão semântica aprofundada |
| `mempalace/embedding.py` | EOF informado na parte 8; blob coincide | Revisão semântica e dependências |
| `mempalace/knowledge_graph.py` | EOF informado na parte 8; blob coincide | Revisão semântica e temporalidade |
| `mempalace/backends/sqlite_exact.py` | EOF histórico; releitura atual de 1251–2270 e imports 1–108 | Cruzar dependências, chamadores e testes; evitar reiniciar pelas partes 9–12 |
| `tests/test_knowledge_graph.py` | EOF informado na parte 8; blob coincide | Cruzamento de casos e implementação |
| `tests/test_backend_conformance.py` | EOF informado na parte 8; blob coincide | Cruzamento de contratos e casos negativos |
| `tests/test_sqlite_exact_backend.py` | EOF informado na parte 8; blob coincide | Cruzamento dos testes de concorrência e manutenção |
| `LICENSE` | Leitura integral na parte 14; hash recalculado | Licenças de dependências e dados separadas |
| `pyproject.toml` | Leitura integral na parte 14; hash recalculado | Lockfiles e dependências transitivas |
| `mempalace/backends/__init__.py` | Leitura integral na parte 14; hash recalculado | Cadeia de importações dos backends |
| `mempalace/backends/registry.py` | Leitura integral na parte 14; hash recalculado | Reentrância e descoberta de plugins |
| `mempalace/backends/_magic.py` | Leitura integral na parte 14; hash recalculado | Ciclo de vida de conexões e portabilidade |
| `mempalace/backends/_filters.py` | Leitura integral na parte 14; hash recalculado | Tipos de operandos e equivalência com filtros SQL |

Conferir hashes do histórico não reproduz uma leitura anterior nem certifica suas conclusões. A releitura parcial de um arquivo já registrado até EOF deve ser anotada como aprofundamento, sem aumentar a contagem de arquivos ou apagar o registro anterior.

## Próxima sequência

1. Ler `mempalace/lexical.py`, `mempalace/timeutil.py`, `mempalace/stored_text.py` e `mempalace/config.py`, no mesmo commit; registrar os hashes e as dependências encontradas.
2. Cruzar buscas, temporalidade, codecs, migrações e exclusões com os respectivos testes. Não executar esses testes nesta fase.
3. Seguir pelo manifesto para os demais módulos, testes, documentação, CI, scripts, segurança, licenças e benchmarks. Atualizar o registro por caminho; um novo relatório deve acrescentar evidência ou aprofundamento explícito.
4. Inspecionar metadados e formatos de mídia e resolver o link simbólico sem tratá-lo como fonte Python. Datasets e modelos externos precisam de inventário separado.
5. Somente após concluir a leitura e a auditoria estática do inventário do MemPalace, iniciar o Ruflo em um commit fixado.

## Regras desta fase

Leitura estática, sem instalação, importação dos pacotes, execução de seus testes ou benchmarks, nem implementação a partir desses projetos. Verificações locais de JSON, hashes Git, contagem de arquivos e sintaxe dos fontes SECA são operações sobre metadados e texto; não são testes de comportamento.

Reprodução em execução é uma fase futura distinta. Os planos antigos que mencionam instalação ou benchmarks não autorizam sua execução durante a auditoria estática atual.

Manter o núcleo neural SECA offline, sem modelos pré-treinados ou linguagem embutida. Memória documental e orquestração de agentes são temas da infraestrutura externa de pesquisa, sem equivalência presumida com memória biológica ou consciência.
