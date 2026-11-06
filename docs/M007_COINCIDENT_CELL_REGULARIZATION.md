# SECA M007 — Regularização determinística de células coincidentes
Data: 2026-11-06

## Objetivo
Corrigir a singularidade geométrica de duas células pontuais com posições idênticas na aproximação mecânica 2D. Este módulo é **experimental e isolado**; não substitui o motor existente.

## Método
Força de repulsão por pares: F = k(2r-d), para d<2r, com direção normalizada do vetor entre centros. Quando d=0, usa direção fixa no eixo x, com sinais opostos para cada membro do par. Integração explícita de Euler. Interações par-a-par conservam a soma das forças.

## Execução local
Comando: `cd experiments/m007 && python -m unittest -v`
Resultado observado em 2026-11-06: **7 testes passaram (0,007 s)**, incluindo separação de centros coincidentes, soma das forças nula, conservação do centroide, ausência de contato distante, determinismo, entradas inválidas e finitude em 100 passos com 20 células coincidentes. A execução no CI e dos arquivos recuperados diretamente do GitHub não foi verificada.

## Limitações
A direção fixa resolve a singularidade, mas **quebra invariância rotacional e, em geral, de permutação** quando há centros coincidentes. A interação de força central e o raio são parâmetros de brinquedo, não calibrados. Não há divisão, adesão, diferenciação ou sinalização bioquímica. Estabilidade numérica depende de dt, k e densidade. Testes unitários não validam embriogênese.

## Fundamentação e confronto futuro
- Mechanics of human embryo compaction, Nature (2024): https://www.nature.com/articles/s41586-024-07351-x
- Future work: comparar estratégias isotrópicas de desempate, regularização suave e métodos de dinâmica de partículas, além de propriedades de convergência e parâmetros experimentais.

Sem modelos pré-treinados; simulação offline; nenhuma linguagem ensinada.
