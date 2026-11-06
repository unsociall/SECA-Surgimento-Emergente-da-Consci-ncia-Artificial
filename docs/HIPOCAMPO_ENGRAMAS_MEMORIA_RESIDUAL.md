# SECA — Hipocampo, engramas silenciosos e memória residual
Data: 2026-11-06

## Terminologia
"Memória residual" não é um mecanismo único e padronizado. Distinguir traço mnêmico persistente, engrama silencioso, recuperação natural, recuperação induzida e consolidação de sistemas. A ausência de recordação comportamental não implica necessariamente apagamento do traço, mas tampouco prova que todo esquecimento preserve memórias.

## Evidências publicadas
1. *Silent memory engrams as the basis for retrograde amnesia* (PNAS, 2017): em camundongos com amnésia experimental, optogenética permitiu recuperação de informações não acessíveis por pistas naturais. https://pmc.ncbi.nlm.nih.gov/articles/PMC5699085/
2. *A short-term memory trace persists for days in the mouse hippocampus* (Communications Biology, 2022): traço hipocampal recuperável optogeneticamente e facilitação de consolidação por reexposição. https://www.nature.com/articles/s42003-022-04167-1
3. *Neural Traces of Forgotten Memories Persist in Humans and are Behaviorally Relevant* (eLife, versão publicada em 2026): padrões de fMRI 7T compatíveis com persistência de traços episódicos não acessíveis conscientemente, com relação a respostas de escolha. https://doi.org/10.7554/eLife.109530.1
4. *Role of the hippocampus in systems consolidation of remote fear memory* (Experimental & Molecular Medicine, 2026): revisão das interações hipocampo-neocórtex e papel persistente do hipocampo. https://www.nature.com/articles/s12276-026-01680-9
5. *Neurogenesis-dependent transformation of hippocampal engrams* (2021): hipótese de transformação e silenciamento de engramas por reorganização da circuitaria. https://pubmed.ncbi.nlm.nih.gov/34400284/

## Implicações para SECA (hipóteses de engenharia, não resultados biológicos)
- Modelar DG/CA3/CA1 inicialmente como populações simplificadas com conectividade explícita, sem afirmar equivalência anatômica.
- Separar **armazenamento do traço** (pesos/conectividade) de **acessibilidade da recuperação** (limiar, pistas e estado de rede).
- Adicionar plasticidade local, decaimento, interferência e reativação offline, sem modelos pré-treinados ou ensino de linguagem.
- Definir métricas de similaridade de padrões, recuperação por pistas incompletas, retenção após silêncio e interferência entre memórias.
- Implementar controles negativos: rede sem plasticidade, pesos embaralhados, pistas não relacionadas, remoção de conexões e sementes independentes.

## Proposta experimental H001
Codificar padrões binários arbitrários em rede associativa pequena usando regra local; reduzir a acessibilidade da pista sem apagar os pesos; medir recuperação antes/depois da redução e após restauração da pista. Comparar com controles de pesos embaralhados. **Importante:** um resultado positivo seria apenas demonstração computacional de dissociação entre armazenamento e recuperação; não valida engramas biológicos, memória humana nem consciência.

## Próximas etapas
Implementar H001 com testes determinísticos e documentar resultados brutos; depois comparar métricas com dados experimentais abertos e modelos publicados.

## Restrições
Simulação offline, sem LLM pré-treinado, sem instrução linguística. Não interpretar recuperação optogenética animal como prova de lembrança consciente.
