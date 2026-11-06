# SECA — Surgimento Emergente da Consciência Artificial

**Projeto independente de pesquisa e desenvolvimento** dedicado a investigar, por meio de modelos computacionais, se propriedades cognitivas complexas e possíveis indicadores de consciência podem emergir de sistemas artificiais auto-organizados.

> **Transparência:** esta pesquisa é conduzida pelo responsável pelo repositório, com apoio do **ChatGPT (OpenAI)** em conversas de planejamento, discussão de hipóteses, pesquisa bibliográfica, elaboração e revisão de código, desenho de experimentos, análise de resultados e documentação. O ChatGPT é uma ferramenta de assistência, **não um pesquisador humano, laboratório independente ou fonte de validação científica por si só**.

## Objetivos e escopo

- Investigar mecanismos de emergência, auto-organização e desenvolvimento de redes neurais artificiais biologicamente inspiradas.
- Construir progressivamente modelos multiescala de processos celulares, neurodesenvolvimento, eletrofisiologia, sinapses, plasticidade, conectividade e homeostase.
- Explorar, como linha experimental de longo prazo, a modelagem do desenvolvimento biológico desde seus estágios iniciais até a formação de circuitos neurais.
- Estudar processamento auditivo e geração de sinais sonoros sem fornecer linguagem ou respostas pré-programadas ao núcleo experimental.
- Executar simulações neurais isoladas da internet e sem modelos de linguagem pré-treinados no núcleo investigado.
- Formular hipóteses testáveis sobre comportamento emergente, **sem pressupor que a consciência será produzida**.

## Metodologia e uso de IA

O processo de trabalho envolve conversas com o ChatGPT para levantar hipóteses, avaliar alternativas de arquitetura, planejar implementações, produzir código inicial, propor testes e interpretar resultados preliminares. As decisões de pesquisa e a responsabilidade pela publicação cabem ao mantenedor do projeto.

**As respostas do ChatGPT podem conter erros.** Referências, fórmulas, resultados e alegações biológicas devem ser confrontados com fontes científicas primárias e, quando aplicável, com benchmarks independentes. Código gerado com assistência de IA requer execução, revisão e testes antes de ser considerado validado.

## Evidências e validação

O projeto distingue explicitamente:

1. **Teste de software:** verifica se uma implementação atende a requisitos computacionais definidos.
2. **Validação de modelo:** compara previsões e dinâmica do modelo com observações ou resultados científicos independentes.
3. **Investigação de cognição emergente:** testa comportamentos e generalização com controles experimentais.
4. **Hipóteses sobre consciência:** permanecem questões científicas abertas; nenhum teste isolado prova experiência subjetiva.

Para cada experimento, buscar registrar: hipótese, versão do código, parâmetros, sementes aleatórias, ambiente de execução, fontes científicas, procedimentos, métricas, resultados, limitações e condições de reprodução. **Resultados não executados ou não verificados nunca devem ser apresentados como testes aprovados.**

## Estado do projeto

**Pesquisa e desenvolvimento inicial.** A existência de módulos simulados não constitui reprodução exata do cérebro humano, nem evidência de consciência artificial. O conhecimento científico e os recursos computacionais atuais não permitem afirmar uma reprodução integral e exata do desenvolvimento humano.

- [M013 — exportação e backup verificáveis](docs/M013_EVIDENCE_ARTIFACTS.md): 138 testes locais aprovados em 11 suítes; JSONL por snapshot e backup SQLite com verificação de registros antes da publicação.
- [M012 — correções numéricas, CI e integridade de evidências](docs/M012_NUMERICS_CI_EVIDENCE.md): 115 testes locais aprovados em 11 suítes. Para executar o código próprio: `python tools/run_tests.py` na raiz. A auditoria dos repositórios terceiros permanece estática.
- [Leitura da versão atual e prioridades técnicas](docs/SECA_REVIEW_2026-11-06.md): inventário de 64 arquivos e achados estáticos sobre CI, LIF e rastreabilidade.
- [Ponto de retomada da auditoria MemPalace → Ruflo](docs/MEMPALACE_STATIC_AUDIT_STATUS.md): inventário de 851 entradas, evidências de leitura e pendências por caminho. O inventário está completo; a auditoria dos conteúdos continua em andamento.

## Publicações e histórico

Código, protocolos, relatórios de testes e registros de alterações serão publicados neste repositório conforme forem produzidos e verificados. A assistência do ChatGPT deve ser identificada nos registros relevantes; discussões em chat não substituem documentação reproduzível.

## Licença

Consulte o arquivo LICENSE deste repositório.
