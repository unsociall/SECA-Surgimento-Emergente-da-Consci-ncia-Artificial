# SECA — leitura do repositório e prioridades técnicas

Data: 2026-11-06. Referência: commit `bee16c958e85c43ff6a3e6bb91cf51062de9f1bf`.

## Escopo verificado

Foram lidos os **64 arquivos rastreados** dessa versão: fontes, testes, experimentos, resultados registrados, documentação, configuração de CI e licença. Os arquivos adicionados por esta revisão não fazem parte desse denominador. O [manifesto da revisão](audits/seca-bee16c9-review.json) registra caminhos, modos, tamanhos e hashes de blob.

Os 28 arquivos Python foram analisados sintaticamente com `ast.parse`, sem importar ou executar os módulos. Foram contados 96 métodos de teste declarados: 15 em `tests/` e 81 em `experiments/`. Contagem de métodos não é execução, aprovação ou cobertura de código. Nenhum teste ou experimento foi executado nesta revisão.

## Estado da implementação

| Área | Implementação encontrada | Limite atual |
|---|---|---|
| Divisão celular | `src/seca/cells.py`: divisão binária e gerações | Sem ciclo celular, volume, diferenciação ou sinalização |
| Mecânica | `src/seca/mechanics.py` e variantes M004–M009 | Modelos 2D idealizados, ainda separados e sem calibração empírica |
| Eletrofisiologia | `src/seca/neuron.py` e E001 | LIF isolado; sem rede sináptica ou plasticidade |
| Linhagem espacial | `experiments/m010/lineage.py` | Mantém células vivas e referências aos pais; não preserva toda a árvore histórica |
| Estados afetivos | `experiments/emotions/emotion_state.py` | Valores atribuídos externamente; não são estados emergentes demonstrados |
| Rastreabilidade | `experiments/evidence/evidence_store.py` | SQLite e hash do payload; contexto do registro não participa do hash |

O repositório contém componentes experimentais iniciais. Não existe nesta versão uma integração que realize o desenvolvimento completo de um circuito neural, memória associativa ou cognição emergente. Os resultados históricos continuam sujeitos às limitações registradas nos respectivos relatórios.

## Achados estáticos e correções propostas

As correções abaixo são uma fila de trabalho, **não implementações ou testes concluídos**. O incremento atual permanece dedicado à leitura estática.

### S001 — CI não seleciona os testes dos experimentos

Evidência: `.github/workflows/tests.yml:14` executa somente `python -m unittest discover -s tests -v`. Os 81 métodos em `experiments/` ficam fora dessa seleção. Assim, um resultado positivo desse job não confirma os experimentos M004–M010, E001, emoções ou evidências.

Correção proposta para fase posterior: selecionar cada suíte experimental em processo separado e em seu diretório correspondente. M004 e M005 importam módulos com o mesmo nome (`cell_mechanics`); reunir todos os diretórios no mesmo processo pode criar colisões de importação.

Critério de aceitação futuro: uma falha deliberada em qualquer suíte selecionada deve reprovar o job; registrar comandos e contagens reais, sem tomar a contagem estática como resultado executado.

### S002 — LIF precisa de validação explícita de valores finitos

Evidência: `src/seca/neuron.py:13` verifica desigualdades para `dt_ms` e `tau_ms`, mas não verifica finitude de parâmetros, corrente ou estado. Comparações com NaN não oferecem uma validação de domínio suficiente. O E001 usa uma condição diferente para o passo, mas também não valida todos os valores do estado e da corrente.

Correção proposta: definir e validar o domínio numérico completo antes de alterar o estado. Especificar o comportamento para NaN, infinito, constante de tempo inválida e estado inicial incompatível.

Critério futuro: entradas inválidas devem falhar sem contaminar o estado; comparar trajetórias válidas com uma referência independente. Os casos de falha foram identificados por leitura, não executados.

### S003 — Refratariedade depende do passo de integração

Evidência: `src/seca/neuron.py:21` fixa `refractory_steps = 2`; E001 também fixa dois passos. Alterar `dt_ms` altera o intervalo refratário representado em milissegundos. Isso deve ser controlado antes de comparar frequências entre diferentes resoluções temporais.

Correção proposta: declarar a unidade da refratariedade e separar sua duração do número de passos, ou explicitar essa dependência no protocolo. O comportamento atual com passo de 1 ms não foi reexecutado nesta etapa.

### S004 — Hash de evidência não vincula o payload ao contexto

Evidência: `experiments/evidence/evidence_store.py:20` serializa e calcula o hash somente de `payload`; `get`, na linha 32, verifica somente esse conteúdo. Os campos `id`, `experiment`, `kind` e `created_at` não integram o checksum. Atribuir o mesmo payload a outro contexto não altera esse hash.

Correção proposta: definir um envelope versionado de evidência que inclua os campos de contexto necessários, com uma estratégia explícita para registros legados. Um checksum desse envelope continuaria sem oferecer autenticação contra quem consegue alterar dados e checksum juntos.

Critério futuro: alterações acidentais em campos vinculados devem ser detectadas, além de alterações no payload. Não houve alteração de banco ou reprodução de adulteração nesta revisão.

### S005 — Nome do CSV de E001 diverge do relatório

Evidência: `experiments/E001_lif_current_response.py` grava `results_lif.csv`, enquanto `experiments/E001_report.md` aponta `E001_results.csv`. O arquivo já versionado não é automaticamente substituído pelo comando documentado.

Correção proposta: tornar caminho e política de geração explícitos e registrar a comparação entre o resultado gerado e o resultado versionado. Nenhum resultado experimental foi regenerado aqui.

## Continuidade da pesquisa

A frente ativa é a auditoria sequencial MemPalace → Ruflo. O [estado consolidado](MEMPALACE_STATIC_AUDIT_STATUS.md) passa a informar inventário e evidências de leitura, evitando reiniciar a leitura do mesmo trecho a partir de relatórios antigos.

O núcleo experimental segue offline, sem pesos pré-treinados ou linguagem incorporada. As ideias extraídas de armazenamento e orquestração pertencem à infraestrutura externa de pesquisa; sua adoção exige revisão própria. Leitura, teste de software e validação biológica permanecem etapas distintas.

Elaboração e revisão com assistência do ChatGPT (OpenAI). Este documento não é validação científica independente.
