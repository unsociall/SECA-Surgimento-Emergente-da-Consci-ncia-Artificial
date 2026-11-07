# MemPalace — auditoria estática, parte 23

Data: 2026-11-07. Fonte: MemPalace/mempalace, ref fixada `f8e3536` (ref abreviada herdada das etapas anteriores; SHA completo do commit ainda não reconciliado). **Somente leitura; testes não executados.**

## Evidência de leitura integral nesta etapa
- `tests/test_hub_client.py` — blob Git SHA-1 `9ccfc5370ed658aacfe82da7012ccd7169b5e8fd`; conteúdo integral recuperado via GitHub `fetch_file` com ref `f8e3536`. **Novo arquivo lido nesta etapa**.
- `mempalace/server_registry.py` — blob `660b01ddc6ab9b94b0c7c22da34c8e3be2f5f2ba`; conteúdo integral relido para cruzamento. **Não contabilizar novamente**.
- `tests/test_server_registry.py` — consulta retornou 404; **não lido**. Não inferir ausência definitiva sem inventário da árvore.

## Cobertura semântica de tests/test_hub_client.py
O teste usa `pytest`, `monkeypatch` e `io.BytesIO` para simular transporte HTTP sem abrir rede. Os cenários verificados no código dos testes abrangem:
- descoberta negativa quando não há palace, registro, processo vivo ou encaminhamento habilitado;
- proteção contra encaminhar para o próprio PID;
- transformação de bind wildcard `0.0.0.0` em loopback `127.0.0.1`;
- transporte sem Authorization quando não existe token, e bearer token quando existe;
- resposta HTTP 401: nova tentativa **uma vez** com token alternativo, ou propagação do erro;
- formato exato de JSON-RPC `tools/call`, tratamento de corpo vazio;
- endpoint `/healthz` e indisponibilidade simulada;
- rejeição de fingerprint divergente e extração do primeiro bloco textual.

## Avaliação crítica
1. Os testes **especificam comportamento**, mas não demonstram aprovação em execução real.
2. A validação de processo por PID (vista em `server_registry.py`) não autentica identidade nem garante que o serviço na porta seja o mesmo processo; risco de confiança em registro local precisa de avaliação de modelo de ameaças.
3. A transformação de wildcard em loopback limita o destino esperado, mas `client_base_url` também aceita host/scheme fornecidos pelo registro. A origem e as permissões do arquivo de registro devem ser consideradas na análise de confiança; **não afirmar exploração demonstrada**.
4. Retry após 401 é restrito e evita repetição genérica de escritas em falhas de transporte; falta verificar cenários de timeout e idempotência nos testes complementares.
5. Não há neste arquivo testes explícitos de IPv6, symlink hostil, substituição de PID, validade de porta, corrupção do token, concorrência ou restrições de permissão em múltiplas plataformas. Ausência neste arquivo **não prova ausência na suíte completa**.

## Relevância ao SECA
- Considerar contratos de falha fechada e identidade de instância na futura memória persistente offline.
- Separar estado histórico de estado vivo e evitar replay não idempotente.
- O SECA-Bio permanece intacto: **não copiar, integrar, instalar ou executar** MemPalace.
- Sem modelos pré-treinados e sem ensino de linguagem.

## Controle de cobertura
**1 novo arquivo integralmente lido nesta parte; 1 releitura sem contagem adicional; 1 caminho não localizado.**
Percentual global **indeterminado**: a árvore integral do commit fixado e a reconciliação de todos os manifestos ainda não foram verificados. Não declarar 100%. Ruflo continua pendente.
