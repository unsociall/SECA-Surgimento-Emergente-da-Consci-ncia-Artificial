# M012 — validação numérica, testes completos e evidências versionadas

Data: 2026-11-06. Base: `a2978df399a6670672e7405544edfba05cd55c65`.

## Problema e comportamento resultante

Este incremento resolve os cinco pontos S001–S005 identificados na [leitura anterior do SECA](SECA_REVIEW_2026-11-06.md). O trabalho é manutenção do código próprio e da infraestrutura externa de pesquisa. A auditoria dos repositórios terceiros permanece estática: nenhum pacote MemPalace ou Ruflo foi instalado, importado ou executado.

| Ponto | Antes | Agora |
|---|---|---|
| S001: seleção no CI | Somente `tests/`; 81 métodos experimentais fora da seleção | `tools/run_tests.py` seleciona as suítes experimentais e executa cada diretório em um processo separado |
| S002: domínio numérico LIF | NaN, infinito e overflow podiam contaminar o estado | Validação do estado, corrente, passo e resultado; erro não avança o estado |
| S003: refratariedade | Dois passos, cuja duração variava com `dt_ms` | Duração explícita em milissegundos; um passo que cruza o fim do intervalo integra somente o tempo ativo |
| S004: integridade de evidências | Hash somente do payload | Novos registros verificam um envelope canônico com ID, experimento, tipo, conteúdo, data UTC e versão do checksum |
| S005: resultado E001 | Script gravava um CSV com nome diferente do relatório | Padrão `experiments/E001_results.csv`, independente do diretório atual, com opção `--output` e finais de linha LF |

E001 passa a usar o mesmo neurônio do pacote `seca`, evitando duas implementações divergentes. O teste da CLI gera o resultado em diretório temporário e o compara byte a byte com o CSV versionado. A curva registrada com passo de 1 ms permanece igual: 0, 0, 0, 0, 0, 17, 33, 62 e 83 Hz para as nove correntes do experimento.

## Execução e evidência

Comando na raiz: `python tools/run_tests.py`.

**Resultado local: 115 testes aprovados em 11 suítes, Python 3.12.14.**

- [Resumo estruturado e hashes dos fontes testados](validation/M012_test_summary.json).
- [Saída completa da execução aprovada](validation/M012_unittest_python312.log).

| Suíte | Testes |
|---|---:|
| E001 | 8 |
| Estados afetivos | 9 |
| Evidências e migração | 15 |
| M004 | 3 |
| M005 | 7 |
| M006 | 12 |
| M007 | 7 |
| M008 | 8 |
| M009 | 11 |
| M010 | 9 |
| Núcleo, numérica e executor de testes | 26 |

Os novos testes cobrem falha deliberada em experimento e isolamento de nomes de módulos; rejeição de valores não finitos sem mutação; overflow; duração refratária entre passos de 0,25 a 2 ms; cruzamento do intervalo refratário; aproximação da solução analítica sub-limiar ao refinar o passo; contexto da evidência; migração e reabertura de banco legado; versão desconhecida de checksum; e reprodução do CSV por uma CLI iniciada em outro diretório.

Uma primeira execução encontrou um erro na fixture de isolamento do executor: o diretório de testes da fixture estava vazio. A fixture recebeu um teste de referência e a execução completa foi repetida com sucesso. Nenhum resultado de falha foi contado como aprovação. O CI continua configurado para Python 3.11; o resultado local acima deve ser distinguido da execução remota.

## Compatibilidade e migração

O estado experimental `refractory_steps` foi substituído por `refractory_ms` e `refractory_remaining_ms`. O alias `LIF` de E001 usa os nomes do núcleo, `potential` e `resting`; os nomes antigos `voltage`, `rest` e `refractory` não são preservados. Usos externos desses campos precisam de atualização. Os usos internos foram revisados e testados.

O banco recebe a coluna `checksum_version` quando necessário. Registros antigos mantêm payload, data e hash originais, com versão 1 e `integrity_scope="payload_only"`. Não são reclassificados como protegidos integralmente. Novos registros usam versão 2 e `integrity_scope="envelope"`. Uma versão desconhecida é recusada.

O hash da versão 2 representa JSON canônico, não a disposição original de espaços e chaves do payload. IDs, experimento, tipo e data UTC também participam do envelope. Um hash continua sem autenticar um registro contra quem consegue alterar dados e checksum juntos. A migração foi testada sobre um banco sintético com o esquema anterior; nenhum banco pessoal ou de produção foi modificado nesta etapa.

## Limites científicos

São testes de software e verificação numérica de um modelo idealizado. A aproximação analítica testa a equação LIF adotada, não a fidelidade a neurônios humanos. Não foram adicionadas sinapses, plasticidade, diferenciação celular ou uma rede cognitiva integrada. Nenhum resultado demonstra consciência.

O estudo externo avançou em sete arquivos do MemPalace, descritos no [relatório de busca, tempo e codificação](MEMPALACE_AUDIT_LEXICAL_TIME_CODEC_CONFIG_2026-11-06.md). Nenhum código desses arquivos foi copiado para o núcleo SECA. Ruflo continua na sequência após a conclusão da auditoria estática do MemPalace.

Elaboração, implementação e revisão com assistência do ChatGPT (OpenAI).
