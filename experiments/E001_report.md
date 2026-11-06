# SECA — E001: curva corrente-frequência de neurônio LIF

Data: 2026-11-06.

## Hipótese
No modelo LIF determinístico simplificado, correntes abaixo do limiar estacionário não provocam disparos; correntes maiores produzem frequências crescentes.

## Método
Python padrão, Euler explícito com passo de 1 ms, constante de tempo de 20 ms, repouso -70, limiar -55, refratariedade de 2 passos e reset para -70. Corrente em unidades arbitrárias. Cada condição simula 1000 ms, reinicializando o neurônio. Sem treinamento.

## Execução local
Comando: `cd experiments && python E001_lif_current_response.py && python -m unittest test_E001 -v`.

Resultados em `E001_results.csv`. Frequências (Hz) para correntes 0, 5, 10, 14, 15, 16, 20, 30, 40: 0, 0, 0, 0, 0, 17, 33, 62, 83. Seis testes executados localmente e aprovados em 2026-11-06. A execução no GitHub Actions deve ser verificada separadamente.

## Limitações
Verificação computacional, **não validação biológica**. Sem canais iônicos explícitos, sinapses, ruído, metabolismo ou dendritos. Nenhuma conclusão sobre consciência.

## Próximo experimento
Comparar passo temporal e curva f-I com implementação independente Brian2; buscar dados experimentais de referência.

## Referências
- https://brian2.readthedocs.io/en/stable/
- https://docs.neuroml.org/Userdocs/TestingNeuroMLModels.html
