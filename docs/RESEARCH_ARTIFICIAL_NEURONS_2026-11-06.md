# SECA — Levantamento de neurônios artificiais e dados públicos (2026-11-06)

## Categorias
1. Neurônios biológicos derivados de células-tronco e organoides: células reais cultivadas em laboratório.
2. Modelos computacionais de neurônios: LIF, Hodgkin–Huxley e modelos multicompartmentais.
3. Neurônios físicos neuromórficos: dispositivos eletrônicos ou spintrônicos que imitam algumas propriedades.

## Fontes prioritárias
| Fonte | Evidência / dados | Aplicação no SECA | Limite |
|---|---|---|---|
| *Preconfigured neuronal firing sequences in human brain organoids* (Nature Neuroscience, 2025) | Eletrofisiologia DANDI 001603; scRNA-seq GSE290330; código braingeneers/Protosequences | Atividade espontânea e sequências populacionais | Organoides não equivalem a cérebro completo |
| *Spontaneous activity spike data and RNA-seq gene expression data from human forebrain organoids* (Zenodo, 2026) | Spikes espontâneos e RNA-seq; 8 eletrodos, 30 kHz, organoides 75–367 dias | Dinâmica espontânea sem estimulação externa deliberada | Spike detection e amostragem condicionam análise |
| *An in vitro whole-cell electrophysiology dataset of human cortical neurons* (GigaScience, 2022) | DANDI 000293; 118 neurônios humanos | Parâmetros elétricos e comparação de curvas f-I | Neurônios de tecido cirúrgico, não cultivados artificialmente |
| Allen Cell Types Database | Registros NWB, morfologias SWC, modelos | Calibração e comparação independente | Mistura de espécies e tipos celulares |
| BlueBrain/OpenData | Modelos, morfologia, sinapses, canais iônicos | Comparar modelos multiescala | Heterogeneidade de origem e licenças |
| DishBrain (Neuron, 2022) | Experimento com culturas neuronais e Pong | Aprendizagem em malha fechada e controles | Não prova experiência subjetiva |
| Brainoware (Nature Electronics, 2023) | Reservatório de organoide para processamento | Dinâmica de reservatório e estímulos | Não é cérebro autônomo |

## Links
- https://www.nature.com/articles/s41593-025-02111-0
- https://dandiarchive.org/dandiset/001603
- https://zenodo.org/records/20286251
- https://pmc.ncbi.nlm.nih.gov/articles/PMC9664072/
- https://dandiarchive.org/dandiset/000293
- https://brain-map.org/support/documentation/documentation-cell-types-database
- https://github.com/BlueBrain/OpenData
- https://pmc.ncbi.nlm.nih.gov/articles/PMC9747182/
- https://www.nature.com/articles/s41928-023-01069-w
- https://pubmed.ncbi.nlm.nih.gov/40462992/

## Próximos experimentos
E002: analisar intervalos entre disparos, rajadas, autocorrelação e sequências espontâneas dos registros DANDI 001603, usando pipeline reproduzível e controles por embaralhamento temporal.
E003: ajustar parâmetros de neurônios computacionais com registros patch-clamp humanos (DANDI 000293), separando treino de parâmetros e avaliação fora da amostra.
E004: comparar atividade espontânea com modelos sem plasticidade e com conectividade randomizada.

## Cautelas
Este documento é levantamento bibliográfico. Não houve download nem validação independente dos conjuntos de dados nesta etapa. Nenhum estudo listado demonstra, por si, consciência artificial.
