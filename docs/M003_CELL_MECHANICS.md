# SECA — M003: interações mecânicas locais (2026-11-06)

## Objetivo
Avançar do modelo de divisão celular idealizada para uma representação espacial 2D com forças simétricas por pares. Modelo ilustrativo, sem calibração biológica.

## Método
Células circulares rígidas com raios arbitrários. Quando há sobreposição, força repulsiva linear; quando a separação está dentro de uma faixa além do contato, atração finita; fora dela, interação nula. Atualização de Euler explícito em regime superamortecido. Sem gradientes químicos, polaridade, adesão molecular, mitose espacial ou ruído.

## Testes e evidência
Em ambiente Python local (2026-11-06), executei **10 testes** para implementação equivalente, com comando `python -m unittest -v test_mechanics`; resultado: 10 testes OK. O arquivo publicado usa importação pelo pacote `seca` e deve ser confirmado separadamente pelo CI. Testes cobrem: lista vazia, célula isolada, repulsão, atração, separação distante, centroide, centros coincidentes, parâmetros inválidos, imutabilidade da entrada e centroide para duas células.

Para reproduzir após instalar o pacote: `python -m unittest discover -s tests -p 'test_mechanics.py' -v`.

## Referência científica
*Mechanics of human embryo compaction*, Nature (2024): https://www.nature.com/articles/s41586-024-07351-x

A referência motiva o estudo de forças mecânicas; **os coeficientes desta implementação não foram extraídos nem ajustados aos dados do artigo**.

## Limitações
Não há unidades físicas calibradas; simetria de forças garante centroide sob aritmética ideal, mas não conserva energia e não assegura estabilidade para passos grandes. Coincidência exata de centros usa eixo fixo e introduz anisotropia. Testes unitários não validam embriogênese.

## Próximo passo
Estudo de convergência temporal (dt, dt/2, dt/4), análise de energia efetiva, e calibração com medições de geometria celular; preservar diferenças entre modelos 2D e 3D.
