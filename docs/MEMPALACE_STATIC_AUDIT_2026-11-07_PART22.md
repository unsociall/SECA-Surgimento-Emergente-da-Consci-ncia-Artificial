# MemPalace — auditoria estática, parte 22

Data: 2026-11-07. **Origem fixada:** MemPalace/mempalace, ref `f8e3536`. Não houve instalação, importação nem execução de código de terceiros.

## Evidência de leitura integral neste lote
| Arquivo | Git blob SHA | Situação |
|---|---|---|
| `tests/test_write_routing.py` | `7de864d9aa49f7f5a57e736403ecf084fe78e90e` | Conteúdo integral obtido via API GitHub e examinado estaticamente |
| `mempalace/server_registry.py` | `660b01ddc6ab9b94b0c7c22da34c8e3be2f5f2ba` | Releitura integral para análise cruzada |

Tentativa de leitura de `tests/test_server_registry.py` na mesma ref retornou HTTP 404: **não registrar como lido nem inferir que não existem outros testes de registry**. É necessário inventário recursivo fixado para descobrir nomes reais.

## Testes de roteamento: observações
O arquivo de testes cobre parse de `direct/prefer/require`, normalização de caixa e espaços, rejeição de valores inválidos, compatibilidade de flags legadas, matriz de oito combinações de disponibilidade/inicialização do daemon, prioridades de variáveis de ambiente versus configuração, escopos CLI/hooks e rejeição de escopo desconhecido.

A matriz testa que `require` sem daemon disponível e sem possibilidade de inicialização resulta em `BLOCKED`, enquanto `prefer` permite fallback para escrita direta. **Isso é evidência do comportamento esperado pelos testes, não de sua aprovação em runtime**.

## Análise cruzada de registro do servidor
O registro é escrito com `atomic_write_text`, inclui PID, host, porta, esquema e capacidades; o token é criado com `secrets.token_urlsafe(32)` sob lock. A leitura de `serverinfo` exige PID vivo e porta inteira, mas **não autentica identidade do processo nem verifica a identidade da instância HTTP**. `client_base_url` constrói URL a partir de campos do registro sem validação explícita de esquema/host nessa função. Consequências concretas dependem do controle de acesso ao arquivo e dos chamadores; não declarar vulnerabilidade confirmada.

O `read_mesh_state` preserva estado publicado mesmo quando o escritor morreu e retorna `writer_alive`; essa distinção entre informação histórica e disponibilidade atual é relevante para memória e coordenação de agentes.

## Possibilidades para SECA (apenas estudo)
- Especificar política de gravação local `fail-closed` para checkpoints críticos; sem depender de daemon remoto.
- Projetar registros com identidade de instância, validade temporal e geração monotônica, além do PID.
- Diferenciar memória histórica de estado vivo em metadados de persistência.
- Elaborar testes próprios de matriz de política e recuperação, sem copiar ou executar código MemPalace.

## Cobertura e pendências
Este lote certifica **1 novo arquivo integral** e **1 arquivo relido** com hashes; não soma releituras como novos arquivos. O inventário global ainda não foi reconciliado com a árvore completa do commit fixado. **Percentual global: não determinado.** Ruflo não iniciado. Próximo passo: obter árvore recursiva do commit, localizar testes de registro/autenticação e ler seus conteúdos integrais.
