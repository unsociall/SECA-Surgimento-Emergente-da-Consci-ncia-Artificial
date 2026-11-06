# SECA — Registro de experimentos anteriores (Genesis Brain)

Data de consolidação: 2026-11-06.

## Proveniência e verificação
Os dois incrementos abaixo foram relatados em execuções anteriores sob o nome **Genesis Brain**. Este documento preserva as alegações e limitações para não perder o histórico. **Os arquivos ZIP originais e os logs brutos de execução não foram recuperados nem auditados nesta consolidação**; portanto, os números são resultados *relatados*, não testes reexecutados nesta publicação. A migração integral de código exige recuperar e comparar os arquivos com o repositório atual.

## G001 — Compactação celular geométrica
- Método relatado: simulador 2D determinístico com deslocamento de células em direção ao centroide.
- Invariante relatado: conservação da quantidade de células.
- Resultado relatado: quatro células, dispersão média 1,4142 → 0,4931 após dez iterações.
- Testes relatados: seis aprovados localmente; sem logs auditáveis neste registro.
- Limitação: não representa forças celulares, adesão, diferenciação ou embriogênese real.

## G002 — Interações mecânicas locais
- Método relatado: repulsão entre células sobrepostas, atração de curto alcance e integração temporal.
- Resultados relatados:
  - Distância sobreposta: 0,20 → 0,36.
  - Sobreposição: 0,80 → 0,64.
  - Distância entre células próximas: 1,10 → 1,0988.
  - Distância entre células afastadas: 10,00 → 10,00.
- Testes relatados: quinze aprovados, incluindo os seis anteriores; não reexecutados nesta consolidação.
- Limitação: parâmetros não calibrados com dados biológicos; conservação do centro de massa requer verificação sob diferentes condições de contorno.

## Fontes científicas para confronto
- [Mechanics of human embryo compaction (Nature, 2024)](https://www.nature.com/articles/s41586-024-07351-x)
- [Morphodynamics of human early brain organoid development (Nature, 2025)](https://www.nature.com/articles/s41586-025-09151-3)

As referências oferecem hipóteses e observações experimentais; não demonstram que G001/G002 reproduzem o desenvolvimento humano.

## Plano de integração auditável
1. Recuperar arquivos-fonte dos incrementos G001 e G002.
2. Executar os testes em ambiente isolado e registrar versões, comandos e logs.
3. Comparar com os módulos existentes em `src/seca`; evitar substituição destrutiva.
4. Migrar somente código verificado, com testes de regressão e relatório.
5. Ajustar parâmetros a partir de dados experimentais com avaliação fora da amostra.

## Restrições do projeto
Sem modelos pré-treinados, sem ensino explícito de linguagem e com simulações neurais offline. Testes computacionais não constituem validação biológica e não demonstram consciência.
