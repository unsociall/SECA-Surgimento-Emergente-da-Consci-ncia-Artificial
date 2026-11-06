# SECA — Fila de leitura científica e auditoria de repositórios
Iniciado em 2026-11-06. **Status: triagem, não leitura integral.** Cada item só passa a CONCLUÍDO após leitura do artigo/documentação completa, inspeção dos módulos relevantes, identificação de licenças, reprodução de um exemplo e relatório com evidências. Não copiar código sem verificar licença.

## Repositórios prioritários
| Ordem | Repositório | Área | Aplicação SECA | Estado |
|---|---|---|---|---|
| 1 | https://github.com/brian-team/brian2 | neurônios pulsantes | comparar dinâmica LIF e plasticidade | README e estrutura inicial examinados |
| 2 | https://github.com/NeuroML/NeuroML2 | modelos padronizados | interoperabilidade de células, sinapses e canais | artigo-base examinado parcialmente |
| 3 | https://github.com/neuronsimulator/nrn | eletrofisiologia | canais iônicos e morfologia | pendente |
| 4 | https://github.com/nest/nest-simulator | redes neurais pulsantes | dinâmica de populações | pendente |
| 5 | https://github.com/arbor-sim/arbor | multicompartmental | dendritos e árvores neurais | pendente |
| 6 | https://github.com/Neurosim-lab/netpyne | redes biológicas | conectividade de circuitos | pendente |
| 7 | https://github.com/CompuCell3D/CompuCell3D | morfogênese celular | adesão, crescimento e mecânica | pendente |
| 8 | https://github.com/MathCancer/PhysiCell | células e microambiente | proliferação e diferenciação | pendente |
| 9 | https://github.com/BioDynaMo/biodynamo | simulação baseada em agentes | crescimento e organização celular | pendente |
| 10 | https://github.com/openworm/c302 | circuito de C. elegans | circuitos e comportamento sem linguagem | pendente |
| 11 | https://github.com/AllenInstitute/AllenSDK | dados experimentais | comparação eletrofisiológica | pendente |
| 12 | https://github.com/NeurodataWithoutBorders/pynwb | padrão NWB | ingestão de dados neurais | pendente |
| 13 | https://github.com/dandi/dandi-cli | arquivos DANDI | aquisição reprodutível de gravações | pendente |
| 14 | https://github.com/OpenSourceBrain/osb-model-validation | validação | testes contra dados empíricos | pendente |
| 15 | https://github.com/scidash/sciunit | testes científicos | separar software de modelo biológico | pendente |

**Nota:** nomes e URLs na fila são candidatos a verificar; inclusão não significa inspeção de conteúdo, compatibilidade ou licença.

## Artigos e fontes científicas
1. Stimberg et al. (2019), *Brian 2, an intuitive and efficient neural simulator*, eLife. https://doi.org/10.7554/eLife.47314 — identificado, leitura integral pendente.
2. Sinha et al. (2025), *The NeuroML ecosystem for standardized multi-scale modeling in neuroscience*, eLife. https://pmc.ncbi.nlm.nih.gov/articles/PMC11723582/ — introdução e arquitetura de padronização examinadas; restante pendente.
3. *Mechanics of human embryo compaction* (2024), Nature. https://www.nature.com/articles/s41586-024-07351-x — identificado; leitura integral pendente.
4. *Morphodynamics of human early brain organoid development* (2025), Nature. https://www.nature.com/articles/s41586-025-09151-3 — identificado; leitura integral pendente.
5. *Silent memory engrams as the basis for retrograde amnesia* (2017), PNAS. https://pmc.ncbi.nlm.nih.gov/articles/PMC5699085/ — identificado; leitura integral pendente.
6. Cowen & Keltner (2017), *Self-report captures 27 distinct categories of emotion*, PNAS. https://doi.org/10.1073/pnas.1702247114 — identificado; leitura integral pendente.

## Arquivos experimentais
- https://dandiarchive.org/dandiset/001603
- https://dandiarchive.org/dandiset/000293
- https://alleninstitute.org/open-science/
- https://biccn.org/data

## Primeiro achado técnico
Brian2 é um simulador baseado em relógio para redes pulsantes, em Python, com equações diferenciais e documentação de exemplos. Sua licença indicada é CeCILL 2.1. A documentação atual indica dependências como NumPy, SymPy e Cython. O SECA deve primeiro comparar curvas corrente-frequência e integradores, mantendo o núcleo próprio independente.

O artigo NeuroML descreve LEMS para representar estrutura e dinâmica de modelos de forma legível por máquina; diferencia padrões de dados (NWB) de padrões de modelos (NeuroML). Isso é relevante para exportar e confrontar resultados sem impor um único motor de simulação.

## Protocolo de leitura integral
Para cada fonte: (1) versão/DOI/commit e licença; (2) leitura completa do texto disponível; (3) estrutura e módulos; (4) hipóteses/equações; (5) dados, métodos e controles; (6) teste reproduzível; (7) relatório de aplicabilidade e limites; (8) decisão de integrar, adaptar ou rejeitar. Quando o texto integral não estiver acessível, registrar explicitamente o bloqueio. Não atribuir porcentagens fictícias.

## Restrições
Simulações neurais offline, sem modelos pré-treinados ou ensino de linguagem. Testes de software não são validação biológica. Não inferir consciência de atividade neural.
