# SECA — Auditoria estática MemPalace — Parte 20 (2026-11-07)

## Referência verificável
Repositório de origem: MemPalace/mempalace; commit fixado `f8e35362189bd0a5abf4c0df1dd5bf90ba059176`. Os dois arquivos abaixo foram obtidos por leitura textual integral pelo conector GitHub no commit indicado; não houve importação, instalação, execução, teste dinâmico ou configuração no dispositivo do usuário.

| Caminho | Blob SHA | Cobertura desta etapa |
|---|---|---|
| `mempalace/write_routing.py` | `ab57034fd0d1d1caffe39f1552110f6409925683` | EOF recebido; análise estática |
| `mempalace/hub_client.py` | `98c4e1cfb60621329fd9f708dc558ed1af11feda` | EOF recebido; análise estática |

## 1. Política de roteamento de escrita
`write_routing.py` define políticas `direct`, `prefer` e `require`, com decisão explícita `direct`, `daemon` ou `blocked`. `require` bloqueia escrita direta se o daemon estiver indisponível e não puder iniciar. `prefer` pode fazer fallback para escrita direta; esse fallback **não é equivalente a exclusividade de escritor**. A precedência usa o primeiro candidato não nulo; uma configuração inválida interrompe a resolução, com origem identificada. Configurações booleanas legadas só são aceitas com `legacy_boolean=True`. O próprio módulo afirma que não altera defaults dos consumidores por si só; integração de hooks/CLI requer verificação separada.

**SECA:** estudar máquina de estados explícita para permissões de gravação e modo fail-closed. Não integrar código nesta fase.

## 2. Cliente do hub e idempotência
`hub_client.py` define descoberta por registro local, verificação `/healthz`, encaminhamento JSON-RPC para `/mcp`, seleção de credenciais locais e identificação de configurações de busca divergentes. Busca com override local pode permanecer local para evitar resultados de configuração incompatível. O cliente só tenta outra credencial quando recebe HTTP 401, presumindo rejeição antes do despacho; outras falhas não são automaticamente repetidas.

O retorno `proxy_error_response` adverte que uma operação mutável pode ter sido processada sem resposta. **Não há garantia de exactly-once**: falta de resposta não comprova ausência de efeito. A estratégia de não repetir automaticamente é conservadora. O `call_tool` usa identificador JSON-RPC constante `1` por chamada, o que merece análise contextual de concorrência e correlação no servidor, sem afirmar vulnerabilidade. `tool_result` assume o primeiro bloco textual de uma resposta com formato esperado; respostas alternativas levantam questão de robustez do parser. `discover` captura exceções genericamente e retorna indisponibilidade, o que pode mascarar a causa operacional nos consumidores, embora registre debug.

**SECA:** estudar identificadores únicos de operação, log durável de intenção/resultado e reconciliação após timeout, mantendo persistência local offline e sem serviços externos obrigatórios.

## 3. Riscos e testes a localizar
- Testes da matriz `direct/prefer/require`, especialmente indisponibilidade do daemon e ausência de fallback em `require`.
- Testes de falha depois do despacho remoto, duplicação, retry de credenciais 401 e respostas JSON-RPC incompletas.
- Revisão de `server_registry.py` para autorização, tokens, permissões, validação de URL e registro de processos.
- Confirmar consumidores efetivos de `write_routing.py` antes de atribuir garantia sistêmica.

## 4. Cobertura e limites
O relatório Parte 19 indicou 20 entradas previamente documentadas, mais cinco evidências a reconciliar, sobre inventário histórico de 851 entradas (incluindo symlink). Esta parte adiciona **dois caminhos com blob SHA**, mas **não certifica total consolidado nem percentual** sem deduplicação e manifesto integral amarrado ao commit. Não afirmar auditoria de 100%. Ruflo permanece aguardando a conclusão verificável do MemPalace.

## 5. Restrições preservadas
Auditoria somente estática. Nenhum componente de MemPalace/Ruflo foi incorporado ou executado. O núcleo biológico offline do SECA permanece separado, sem modelos pré-treinados nem ensino de linguagem.
