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

## Atualização M012

E001 usa agora `seca.neuron.LIFNeuron`; o pacote deve estar instalado ou acessível por `PYTHONPATH`. Na raiz, executar `PYTHONPATH=src python experiments/E001_lif_current_response.py` grava `experiments/E001_results.csv`. `--output caminho.csv` permite uma saída alternativa. O caminho padrão independe do diretório atual e o CSV usa LF.

O [incremento M012](../docs/M012_NUMERICS_CI_EVIDENCE.md) executou os oito testes atuais de E001, incluindo reprodução byte a byte do CSV por uma chamada da CLI a partir de outro diretório. A curva de 1 ms foi preservada. A suíte completa pode ser executada com `python tools/run_tests.py` na raiz, sem instalar dependências de terceiros.

## Referências
- https://brian2.readthedocs.io/en/stable/
- https://docs.neuroml.org/Userdocs/TestingNeuroMLModels.html
