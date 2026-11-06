# SECA — Taxonomia e quantificação operacional de estados afetivos

Data: 2026-11-06

## Evidência científica
- Cowen & Keltner (2017), PNAS, identificaram 27 dimensões distinguíveis de experiências emocionais autorrelatadas em respostas a 2.185 vídeos. **Não se trata de uma lista universal ou definitiva**. https://doi.org/10.1073/pnas.1702247114
- Russell (1980), modelo circumplexo: valência e ativação são dimensões úteis para descrever afeto. https://pdodds.w3.uvm.edu/research/papers/others/1980/russell1980a.pdf
- Watson, Clark & Tellegen (1988), PANAS: instrumento psicométrico para afetos positivos e negativos. https://pubmed.ncbi.nlm.nih.gov/3397865/

## Convenção computacional
`AffectState` define valência [-1,1], ativação [0,1], dominância [0,1] e 27 intensidades [0,1] independentes. A taxonomia de 27 rótulos é uma aproximação operacional baseada no estudo PNAS; o estudo inicial avaliou 34 rótulos e reduziu-os a 27 dimensões, portanto os nomes do código não equivalem a uma lista canônica validada. Intensidades **não são valores biológicos calibrados** nem evidência de sentimentos experimentados.

## Testes
Comando local: `cd experiments/emotions && python -m unittest -v`.
Em 2026-11-06, nove testes locais foram executados e aprovados: contagem de categorias, estado padrão, atualização, decaimento, valores inválidos, categorias inválidas, valência inválida, decaimento inválido e coexistência. Execução em CI não verificada.

## Limitações
O módulo é uma estrutura de mensuração operacional e não um gerador de emoções emergentes. `set_intensity` atribui valores externamente; portanto não constitui mecanismo de desenvolvimento neural espontâneo. A integração futura deve derivar variáveis observáveis de circuitos, homeostase, recompensa e aprendizagem local, com controles e comparação empírica. Não inferir consciência.

## Próximo experimento EM002
Propor circuito simples com entradas homeostáticas e valência/ativação calculadas a partir de eventos internos (sem rótulos linguísticos durante a simulação); medir estabilidade, dependência do histórico e controles sem plasticidade.
