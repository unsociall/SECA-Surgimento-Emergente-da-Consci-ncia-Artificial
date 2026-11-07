# SECA — Protocolo de duas arquiteturas sem pré-treinamento

Data: 2026-11-07. Estado: **proposta experimental registrada; nenhuma execução, treinamento ou resultado empírico nesta etapa**.

## Hipótese e objetivo
Comparar duas arquiteturas pequenas, inicializadas sem pesos pré-treinados, sob **o mesmo ambiente e orçamento computacional**, para investigar aquisição incremental de regularidades, memória e adaptação. Nenhuma evidência obtida nesse protocolo será apresentada como prova de consciência.

## Trilhas independentes
**Trilha A — SECA-Bio (principal):** unidades recorrentes biologicamente inspiradas, estado interno persistente durante episódios, sinapses ajustáveis, modulação por recompensa/novidade e mecanismo de homeostase. Regras de plasticidade devem ser especificadas matematicamente e submetidas a ablação. Não presumir equivalência com neurônios biológicos reais.

**Trilha B — SECA-Zero (comparativa):** rede recorrente compacta (RNN/GRU de arquitetura pública, **pesos novos aleatórios**, sem importar checkpoints) para aprender predição de estímulos e decisões em um ambiente não linguístico. GRU é uma escolha de controle técnico, não um modelo de linguagem. Um Transformer sem pesos treinados pode ser estudado depois, mas não é necessário para o primeiro experimento.

## Ambiente controlado, sem linguagem
Mundo discreto com sinais sensoriais vetoriais, localização, ações e consequências. Exemplo: labirinto pequeno com obstáculos, recursos e estados de energia; recompensa por exploração segura e obtenção de recurso. Não fornecer textos, vocabulários, rótulos semânticos ou modelos pré-treinados.

## Protocolo mínimo reproduzível
1. Fixar especificação do ambiente, versão de código, seeds e limites de memória/tempo.
2. Inicializar ambas as redes com pesos novos; registrar hashes das configurações e checkpoints.
3. Aplicar o mesmo conjunto de episódios e limites de observações/ações.
4. Medir erro de predição, retorno por episódio, generalização em mapas não vistos, adaptação a mudanças, retenção após interrupção e estabilidade.
5. Comparar com controles: agente aleatório, política fixa e cada arquitetura com plasticidade/memória desativada.
6. Repetir com múltiplas seeds; publicar dispersão, não somente melhor execução. Evitar alegações de consciência a partir de recompensa ou desempenho.
7. Documentar resultados negativos, falhas e custos computacionais.

## Critérios de decisão
Aprovar progressão somente se houver reprodução, vantagem robusta sobre controles e ausência de vazamento entre treino e avaliação. Sem evidência, registrar inconclusivo.

## Separação e segurança
- Preservar o núcleo SECA-Bio original. Trilha B é experimento isolado, sem substituir ou reescrever o núcleo.
- Não importar pesos, embeddings linguísticos, checkpoints ou dados de treinamento externos.
- MemPalace e Ruflo continuam **somente sob auditoria estática**, em ordem; este protocolo não integra nem executa componentes deles.
- Armazenamento local de experimentos pode usar arquivos/SQLite, sem Supabase. GitHub armazena código, especificações e relatórios, não segredos.
- Não executar código de terceiros nem configurar o Termux do usuário.

## Próximos entregáveis
A. Especificação formal do ambiente e vetores sensoriais.
B. Duas implementações independentes e pequenas, com testes unitários próprios.
C. Runner de experimentos com checkpoints e comparações controladas.
D. Relatório de resultados com métricas e limitações.

**Status atual:** apenas este plano foi registrado. Não há modelos treinados, benchmark executado ou validação de aprendizagem.
