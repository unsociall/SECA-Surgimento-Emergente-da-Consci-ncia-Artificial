# SECA M010 — Divisão abstrata e rastreamento de linhagem
Data: 2026-11-06

## Objetivo
Introduzir um primeiro registro determinístico de divisão celular, sem substituir os módulos mecânicos anteriores. Um identificador de célula-mãe é mantido como referência histórica nas células-filhas; a mãe deixa o conjunto de células ativas.

## Método
Duas filhas são colocadas simetricamente em torno do centro da mãe, separadas por uma distância positiva configurável e ângulo finito. IDs são monotônicos, gerações são incrementadas e a posição média das filhas coincide com a da mãe. Biblioteca padrão Python, execução offline.

## Testes locais
Comando: `cd experiments/m010 && python -m unittest -v`
9 testes passaram em execução local (0,001 s), verificando inicialização, parentesco, ponto médio, distância, erros de parâmetros, determinismo, segunda geração e unicidade de identificadores. Os testes foram executados sobre arquivos locais com o mesmo conteúdo publicado; CI ainda não verificado.

## Contexto científico
Referência: *Mechanics of human embryo compaction*, Nature (2024): https://www.nature.com/articles/s41586-024-07351-x
A divisão simétrica é uma simplificação geométrica de engenharia, não um resultado calibrado pelo artigo. Desenvolvimento embrionário real envolve ciclo celular, polarização, forças, adesão, sinalização e assimetria.

## Limitações
Não há conservação de massa/volume, célula 3D, cronômetro de ciclo celular, apoptose, diferenciação ou ligação com motor mecânico M009. `centroid()` é média não ponderada; não representa centro de massa em geral. A linhagem das mães removidas não é mantida como tabela histórica independente; apenas as filhas vivas guardam seus pais. Testes unitários não constituem validação biológica.

## Próximo incremento
Persistir árvore genealógica completa de células, volumes e conservação em divisão, com testes de integração aos motores mecânicos existentes após revisão dos PRs abertos.
