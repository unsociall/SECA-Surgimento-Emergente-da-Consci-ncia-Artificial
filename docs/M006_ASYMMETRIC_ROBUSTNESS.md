# M006 — Robustez com populações assimétricas (2026-11-06)

## Objetivo
Verificar invariantes de um modelo **isolado** de mecânica celular 2D com interações pareadas, sem modificar o núcleo existente ou os PRs M003–M005.

## Modelo
Partículas/células pontuais em 2D, interação simétrica por pares: repulsão linear para distância < 2r, atração fraca para 2r ≤ distância < alcance, interação zero além do alcance. Atualização explícita de Euler. Coincidência exata de posições usa direção fixa +x: convenção artificial que quebra invariância rotacional e exige revisão.

## Testes locais
12 testes de implementação equivalente executados em Python unittest: **12 passaram**, duração 0,081 s. Cobertura: população vazia e unitária; centroide em cinco células assimétricas após 100 passos; 100 células após 50 passos com posições finitas; invariância de translação; invariância de permutação em células não coincidentes; repulsão; ausência de interação distante; separação de coincidentes; rejeição de passo, coordenada e contagem inválidos. Comando para repetir no repositório: `cd experiments/m006 && python -m unittest -v`. **Os arquivos publicados são uma transcrição equivalente e não foram reexecutados após publicação; CI não confirmado.**

## Fundamentação científica
- Maître et al. (2015), *Adhesion functions in cell sorting by mechanically coupling the cortices of adhering cells*, Science: https://doi.org/10.1126/science.aaa9323
- *Mechanics of human embryo compaction* (2024), Nature: https://www.nature.com/articles/s41586-024-07351-x

Estes estudos fundamentam a relevância de mecânica e adesão, mas **não** validam a lei de força escolhida.

## Limitações
Sem unidades físicas calibradas, membranas, forças cortical/adesiva medidas, dinâmica 3D, divisão celular, sinalização ou diferenciação. Não é uma simulação exata do embrião ou cérebro. A conservação do centroide decorre da simetria de forças internas e não garante precisão física. Testes unitários ≠ validação biológica. Próxima etapa: comparação de passo temporal em arranjos assimétricos e análise da degenerescência por coincidência.
