# MemPalace — persistência, metadados, caminhos e roteamento

Data: 2026-11-06. Commit fixado: `f8e35362189bd0a5abf4c0df1dd5bf90ba059176`.

## Leitura efetiva e proveniência

Foram lidos integralmente 15 arquivos, totalizando **3213 linhas**. Tamanho e hash de blob foram conferidos contra o [manifesto versionado](audits/mempalace-f8e3536-inventory.json). A [árvore de origem](https://github.com/MemPalace/mempalace/tree/f8e35362189bd0a5abf4c0df1dd5bf90ba059176) permanece imutável para esta auditoria.

| Arquivo | Linhas |
|---|---:|
| `mempalace/metadata_types.py` | 132 |
| `mempalace/fsio.py` | 551 |
| `mempalace/paths.py` | 194 |
| `mempalace/_env.py` | 106 |
| `mempalace/_once.py` | 26 |
| `mempalace/write_routing.py` | 210 |
| `mempalace/hub_client.py` | 283 |
| `tests/test_metadata_types.py` | 102 |
| `tests/test_env.py` | 103 |
| `tests/test_paths.py` | 144 |
| `tests/test_fsio.py` | 462 |
| `tests/test_fsio_writers.py` | 187 |
| `tests/test_write_routing.py` | 422 |
| `tests/test_hub_client.py` | 176 |
| `tests/test_config_non_object.py` | 115 |

O relatório paralelo parte 15 aprofunda SQLite já registrado até EOF. Ele foi preservado e não acrescenta uma nova unidade à cobertura por caminho.

## Persistência e leitura de fontes

`fsio.py` prepara um temporário exclusivo, sincroniza e substitui o destino. Contudo, nos modos padrão, algumas falhas de permissão admitem uma gravação direta com aviso. Nesse caminho, o próprio código informa que uma interrupção pode truncar o destino. Os testes distinguem falhas de serialização, sincronização, substituição, compartilhamento Windows e políticas de links. Foram lidos, não executados.

A sincronização de diretório ignora erros; a chamada, isoladamente, não confirma durabilidade em todos os ambientes. O comportamento real depende do sistema de arquivos e das condições de falha.

A leitura de fontes recusa links e arquivos não regulares, e o descritor fornece o `mtime` usado na proveniência. Há preservação de bytes mediante codificação registrada, com tratamento específico para UTF-8, bytes avulsos e Windows-1252. Normalizar finais de linha é uma transformação separada da preservação dos bytes originais.

Questão aberta: `read_source_text` compara o tamanho obtido antes da leitura com `max_bytes` e depois chama uma leitura sem limite explícito. O caso de um arquivo que cresce durante essa janela requer revisão adicional. Nenhuma falha foi reproduzida nesta auditoria.

## Metadados e configuração

`metadata_types.py` converte campos declarados quando a entrada é reconhecida. Valores não convertidos são preservados; isso não equivale a um esquema estrito de tipos. A marca de registro administrativo tem tratamento próprio para valores legados. Casos extremos de conversão e seus chamadores continuam pendentes de aprofundamento.

`_env.py` diferencia vazio, valor válido e valor não interpretável, exclui booleanos da conversão numérica e recusa floats não finitos nessa conversão. `_once.py` usa um conjunto protegido por lock para suprimir mensagens repetidas por processo; não há limite explícito para a quantidade de chaves distintas retidas nesse conjunto.

Os testes de configuração não objeto descrevem como `null`, listas, strings, números e booleanos na raiz do JSON devem produzir defaults, aviso e preservação do arquivo até uma gravação explícita. As fixtures e os demais testes extensos de configuração permanecem pendentes.

## Caminhos, políticas e comunicação

`paths.py` separa configuração e estado, mantém compatibilidade com instalações legadas e deriva chaves a partir de caminhos canônicos. Essa identidade depende da localização no sistema de arquivos. O código também escolhe entre grafos local e legado, tratando erros de leitura SQLite de forma conservadora quando o arquivo foi identificado. A migração e os chamadores precisam de revisão completa.

`write_routing.py` distingue `direct`, `prefer` e `require`, registra a origem da configuração e produz uma decisão explícita. A função de decisão não converte `require` em escrita direta quando o daemon está indisponível. A adoção dessa política pelos consumidores de hooks e CLI ainda precisa ser auditada antes de afirmar a garantia no fluxo inteiro.

`hub_client.py` relaciona configurações que afetam busca, aplica escopo por backend/modelo e envia JSON-RPC ao hub descoberto. Há uma tentativa com outra credencial somente no caso HTTP 401; outros erros não repetem automaticamente a operação mutante. A premissa de rejeição antes da execução e a seleção de endpoint/token dependem de `server_registry.py` e do servidor, ainda pendentes. Não foi feita chamada de rede a um hub.

## Aplicabilidade ao SECA

Os conceitos úteis ao laboratório são separar configuração efetiva de arquivo bruto, reconhecer migrações legadas, manter projeções distintas da evidência original e explicitar o efeito de cada política de falha. A infraestrutura de RPC ou de agentes não foi adicionada ao núcleo neural.

O [M013](M013_EVIDENCE_ARTIFACTS.md) implementa exportação e backup próprios com validação antes da publicação. Seus testes não executam nem validam MemPalace ou Ruflo. O mecanismo SQLite usado pelo SECA foi confrontado com a documentação primária da biblioteca.

## Estado e próxima sequência

O inventário permanece com 851 entradas. Há **35 caminhos com leitura até EOF documentada**: 28 com leitura direta e conferência registradas nestes incrementos e sete com evidência histórica. Restam 816 caminhos sem esse registro. Nenhuma dessas contagens significa auditoria semântica integral ou aprovação da suíte de terceiros.

Próximos alvos: `mempalace/server_registry.py`, `mempalace/daemon.py`, consumidores e testes de roteamento CLI/hooks, testes extensos de configuração e suas fixtures. A auditoria do Ruflo permanece posterior à conclusão do inventário de leitura e da análise estática do MemPalace.

Nenhuma instalação, importação ou execução dos pacotes MemPalace/Ruflo. Elaboração com assistência do ChatGPT (OpenAI).
