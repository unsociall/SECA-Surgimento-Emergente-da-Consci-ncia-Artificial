# MemPalace — busca lexical, tempo, codificação e configuração

Data: 2026-11-06. Commit: `f8e35362189bd0a5abf4c0df1dd5bf90ba059176`.

## Leitura efetiva

Sete arquivos foram lidos integralmente, totalizando 2881 linhas. Os textos foram conferidos por tamanho e hash de blob contra o [inventário fixado](audits/mempalace-f8e3536-inventory.json).

| Caminho | Linhas até EOF | Blob SHA |
|---|---:|---|
| `mempalace/lexical.py` | 72 | `bc0ab7a4e09dab8811062b7d2bd39dce233ae344` |
| `mempalace/timeutil.py` | 117 | `e8b512b8da0969f79ccffa8284433a2425fbfa94` |
| `mempalace/stored_text.py` | 263 | `27362a9a1b4c2ed040c91e01cb7c5a9057ccd179` |
| `mempalace/config.py` | 1738 | `34b364277fe204584bb463e1dfbf4f3f205c12b2` |
| `tests/test_lexical.py` | 73 | `30380e3ca291830d58d6d18a38aa34bfe9e486e5` |
| `tests/test_stored_text.py` | 289 | `5f604b91b7665c61464512365214213456c6420b` |
| `tests/test_timeutil.py` | 329 | `2a685bc11efa715ca4dbfba1b9caf12245617fea` |

Fonte primária: [árvore do MemPalace no commit analisado](https://github.com/MemPalace/mempalace/tree/f8e35362189bd0a5abf4c0df1dd5bf90ba059176). Os testes acima foram lidos, não executados.

## Busca lexical

`lexical.py` extrai palavras Unicode com pelo menos dois caracteres, converte para minúsculas e aceita uma lista de palavras a descartar. O BM25 calcula frequências e IDF sobre o conjunto de documentos recebido; mudanças nesse conjunto podem mudar as pontuações. A consulta é tratada como conjunto de termos, não como uma sequência neural ou uma memória aprendida.

O teste correspondente registra tokens e valores de referência para textos em inglês, caracteres acentuados, japonês, strings vazias e caracteres substitutos isolados. Também descreve ordenação e remoção de palavras. Os valores são declarados como derivados de implementações anteriores do próprio projeto, não de um benchmark independente reproduzido pelo SECA.

Pendência: conferir normalização Unicode e equivalência com a tokenização FTS ao longo dos chamadores. O módulo não explicita normalização NFC. Não foi reproduzida uma divergência de ranking.

## Tempo e recência

`timeutil.py` produz novas datas em UTC com offset explícito. Datas legadas sem fuso são interpretadas no fuso local da execução. `recency_key` distingue valores interpretáveis, strings inválidas e valores ausentes; `recency_floor` fornece um limite textual conservador ou retorna uma string vazia quando não consegue estabelecê-lo.

Os testes incluem fusos UTC−3 e UTC+9, mistura de formatos legados e UTC, janelas inclusivas/exclusivas, recência em SQLite/Chroma, consultas do grafo e ordem de anexação do log mesmo quando o relógio retrocede. Fixtures, integrações e todos os chamadores ainda não foram integralmente auditados.

Para o SECA, registrar separadamente tempo simulado, ordem de eventos e data de execução. Um timestamp legado sem offset não transporta sozinho o fuso de origem; a reprodução entre máquinas precisa registrar essa informação. UTC no registro externo não substitui a ordem causal nem o relógio do simulador.

## Texto persistido e apresentação

`stored_text.py` distingue texto armazenado, texto de índice e texto apresentado ao cliente. Usa um prefixo e uma marca reservada para tornar reversíveis NUL, substitutos Unicode isolados e strings que já parecem conter escapes. IDs e chaves incompatíveis são recusados em vez de reescritos. A apresentação externa pode substituir caracteres por U+FFFD, enquanto a comunicação interna mantém escapes exatos.

Os testes cobrem ida e volta, marca falsificada, filtros, atualização parcial, resultados sem metadados solicitados, leitores SQLite diretos e busca lexical. A semântica depende também de `metadata_types.py` e dos contratos de validação dos lotes; essas dependências permanecem pendentes. Não foi certificada a reversibilidade de todos os formatos aceitos por toda a aplicação.

Aplicação conceitual: diferenciar evidência original de uma projeção para busca ou apresentação. Nenhum codec desse projeto foi incorporado ao simulador.

## Configuração e efeitos de leitura

`config.py` foi lido em seis intervalos consecutivos, de 1 a 1738, até EOF.

- A precedência não é universal: a propriedade `backend` consulta o arquivo antes da variável de ambiente; várias outras propriedades fazem o inverso. Um protocolo reproduzível deve registrar valores efetivos, não apenas o arquivo de configuração.
- Arquivos ausentes, não interpretáveis e inacessíveis têm estados diferentes. A gravação recusa sobrescrever um arquivo que não conseguiu ler; arquivos malformados são separados antes da tentativa de substituição. A atomicidade depende de `fsio.py`, ainda pendente.
- `search_config_fingerprint` monta um resumo dos valores relevantes para o backend selecionado; seu escopo depende de `hub_client.SEARCH_SETTINGS`, ainda não auditado aqui.
- `connect_sqlite_read` pode usar uma conexão normal quando identifica WAL sem arquivos auxiliares. Portanto, seu nome não garante ausência de efeitos no sistema de arquivos. A rotina é distinta da abertura estritamente somente leitura do backend já examinado. A compatibilidade e o impacto sobre locks precisam de revisão entre módulos, sem falha reproduzida nesta etapa.
- Há palavras-chave previamente definidas para categorias como emoções, consciência e identidade. São regras de classificação de texto; não representam indicadores emergentes de estados internos.
- Configurações de modelos, endpoints, chaves, hooks e roteamento de escrita pertencem à aplicação externa. `resolve_write_routing` declara que alguns consumidores serão introduzidos em incrementos posteriores; a presença de uma opção não demonstra que todo fluxo já a aplica.

## Cobertura e próximos arquivos

O inventário continua com 851 entradas. Existem agora **20 caminhos com registro de leitura até EOF**: 13 com leitura direta e conferência documentadas nestes incrementos e sete provenientes do histórico. Restam 831 caminhos sem esse registro, incluindo itens com critérios próprios de inspeção. Não se trata de 20 auditorias semânticas concluídas.

Próxima leitura: `metadata_types.py`, `fsio.py`, `paths.py`, `_env.py`, `_once.py`, `write_routing.py`, `hub_client.py` e os testes de configuração. Preservar o commit e acrescentar evidências ao manifesto sem recontar arquivos já lidos. Ruflo permanece aguardando a conclusão da auditoria estática do MemPalace.

Nenhuma instalação, importação ou execução de MemPalace ou Ruflo. Os testes do código próprio SECA, descritos em [M012](M012_NUMERICS_CI_EVIDENCE.md), são uma atividade separada e não validam esses projetos terceiros.

Elaboração com assistência do ChatGPT (OpenAI).
