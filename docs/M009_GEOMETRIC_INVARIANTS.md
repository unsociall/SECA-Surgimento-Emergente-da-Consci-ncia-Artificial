# M009 — Invariantes geométricos e robustez básica

Data: 2026-11-06. Branch: `experiment/m009-symmetry-invariants-20261106`.

## Objetivo
Verificar invariância por translação e rotação, conservação do centroide sob forças internas, tratamento de posições coincidentes e entradas inválidas, sem alterar os experimentos M003–M008.

## Modelo
Partículas em 2D com força central aos pares, repulsão para distância menor que 2r e atração para distâncias entre 2r e alcance definido. Passo explícito de Euler sob mobilidade unitária. Forças de pares são iguais e opostas. Células coincidentes são contadas, mas não separadas: evita orientação artificial e mantém a limitação física explícita.

## Execução local
`cd experiments/m009 && python -m unittest -v`
Resultado observado: **11 testes aprovados em 0,011 s** no ambiente local Python, incluindo 40 células por 30 passos. Arquivos correspondentes foram publicados via GitHub, mas CI e execução da cópia remota ainda não confirmados.

## Limitações
Este modelo não simula fecundação, clivagem, desenvolvimento embrionário real, plasticidade neural ou consciência. Parâmetros sem calibração; não há dados biológicos de referência. Conservação de centroide não implica conservação de energia. Euler explícito pode ficar instável para passos grandes. Coincidência exata permanece sem separação.

## Fundamentação
- Mechanics of human embryo compaction (Nature, 2024): https://www.nature.com/articles/s41586-024-07351-x
- Graner & Glazier, Simulation of biological cell sorting using a two-dimensional extended Potts model (Phys Rev Lett, 1992): https://doi.org/10.1103/PhysRevLett.69.2013

Fontes fornecem contexto, não validação quantitativa deste modelo.

## Próximo passo
Avaliar sensibilidade ao passo temporal e comparação com referência de solução mais refinada; posteriormente, construir módulo de divisão celular e testar conservação de linhagens.
