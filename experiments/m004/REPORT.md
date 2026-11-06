# SECA M004 — refinamento temporal da mecânica celular (2026-11-06)

## Contexto e origem
O código `cell_mechanics.py` foi recuperado do arquivo de experimento anterior `genesis_brain_cycle2.zip` e incluído isoladamente neste diretório para reprodutibilidade, sem sobrescrever módulos existentes. A suíte original foi executada localmente: **15 testes aprovados**. Os três testes adicionais foram executados no mesmo ambiente: **18 testes no total, aprovados**. A execução de CI no GitHub não foi verificada.

## Método
Discos 2D, forças simétricas de repulsão e atração local, integração explícita de Euler, três células em coordenadas (0,0), (0.7,0), (2,0.3), raios 0.5, horizonte de 1 unidade de tempo. Solução com dt=0.001 usada como **referência numérica interna**, não verdade biológica nem solução analítica. Métrica: maior distância euclidiana de posição entre células da simulação e referência.

## Resultados reproduzidos localmente
| dt | erro máximo contra dt=0.001 |
|---:|---:|
| 0.1 | 0.002056919 |
| 0.05 | 0.001094842 |
| 0.025 | 0.000554546 |
| 0.0125 | 0.000269877 |

Erro decresceu monotonamente neste cenário; isso sugere convergência temporal, **não prova estabilidade universal**.

## Reproduzir offline
```sh
cd experiments/m004
python -m unittest -v test_convergence
python convergence.py
```
Para reproduzir os 18 testes, é necessário também executar os testes legados do ZIP de origem, não incluídos neste PR. Os três testes adicionais passam isoladamente.

## Limitações
Unidades arbitrárias, parâmetros não calibrados, sem divisão, sinalização, 3D, conservação de volume, deformação real ou medições embriológicas. A referência numérica usa o mesmo integrador, portanto não é validação independente. Nenhum aprendizado de linguagem nem modelo pré-treinado; execução offline.

## Referência de contexto
[Mechanics of human embryo compaction (Nature, 2024)](https://www.nature.com/articles/s41586-024-07351-x). A página do periódico exigiu autenticação nesta execução; não houve leitura integral nem extração de parâmetros do artigo.
