# SECA M005 — Diagnóstico de refinamento temporal
Data: 2026-11-06. Base: mecânica bidimensional de discos moles do experimento Genesis Brain M002, copiada para pasta isolada para evitar alterações destrutivas.

## Execução
`cd experiments/m005 && python -m unittest -v`
Ambiente local Python 3, biblioteca padrão. **7 testes aprovados** na execução local. CI ainda não verificado.

## Cenário
Quatro discos: (0,0), (0.4,0.1), (1.25,0.2), (0.1,1.1); raio 0.5. Tempo total 0.5 unidades arbitrárias. Passos 0.1, 0.05, 0.025, 0.0125.

## Diferença máxima entre resoluções sucessivas
- 0.1 versus 0.05: 0.009155044468258104
- 0.05 versus 0.025: 0.004441762050273312
- 0.025 versus 0.0125: 0.0021808782779430464

As diferenças decrescem neste cenário. Centroide preservado numericamente até 12 casas decimais no teste. Isso é **verificação numérica**, não validação experimental da embriogênese. Não há garantia de convergência para qualquer configuração ou parâmetro.

## Referências
- https://www.nature.com/articles/s41586-024-07351-x — mecânica da compactação embrionária humana.
- https://www.nature.com/articles/s41586-025-09151-3 — morfodinâmica do desenvolvimento inicial de organoides cerebrais.

## Limitações e próximos passos
O modelo não incorpora adesão molecular, sinalização, proliferação, diferenciação ou geometria 3D; unidades e coeficientes não calibrados. Futuro: testes de múltiplas sementes e condições iniciais, limites de estabilidade e comparação com medidas publicadas. Offline, sem modelos pré-treinados nem ensino de linguagem.
