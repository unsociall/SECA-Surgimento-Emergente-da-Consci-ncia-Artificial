# MemPalace — Auditoria estática, parte 24 (2026-11-07)

## Escopo e rastreabilidade
Repositório de origem: MemPalace/mempalace. Ref fixada para leitura: `f8e3536` (ref abreviada já adotada nos relatórios anteriores; reconciliar com SHA completo do commit antes de certificar o inventário).
Arquivo novo lido integralmente nesta etapa: `mempalace/_proc.py`, blob SHA Git `2dc4331005a3e7400b4813ceab91d7df3e176d00`.
Releitura cruzada (não contar novamente): `mempalace/server_registry.py`, blob `660b01ddc6ab9b94b0c7c22da34c8e3be2f5f2ba`; `tests/test_hub_client.py`, blob `9ccfc5370ed658aacfe82da7012ccd7169b5e8fd`.
Tentativas de leitura de `tests/test_proc.py` e `tests/test_server_registry.py`: HTTP 404 no ref indicado; **não** contam como lidos nem comprovam ausência na árvore.

## Leitura técnica integral: mempalace/_proc.py
- `pid_alive` rejeita `bool`, valores não inteiros e PIDs não positivos.
- POSIX: usa `os.kill(pid, 0)`; `ProcessLookupError` e `OSError` genérico retornam falso, `PermissionError` retorna verdadeiro.
- Windows: usa `OpenProcess(SYNCHRONIZE)`, `WaitForSingleObject(handle, 0)` e `CloseHandle` em `finally`; acesso negado conta como vivo. Um `WaitForSingleObject` diferente de `WAIT_OBJECT_0` conta como vivo, inclusive falha da sondagem.
- `kernel32` define `restype` e `argtypes` de `OpenProcess`, mas `CloseHandle` tem somente `argtypes`; revisar semântica e tratamento de erro em auditoria de integração.
- Não há verificação de identidade do processo além do PID; reutilização de PID pode produzir falso positivo de identidade mesmo quando a sondagem de existência é correta.

## Análise cruzada e risco
`read_live_serverinfo` verifica PID vivo, porta inteira e host não vazio, mas não comprova identidade do processo ou vinculação criptográfica ao servidor esperado. `client_base_url` usa `scheme` e `host` do registro, normalizando apenas wildcards para loopback. Se o arquivo de registro for adulterado por um agente com acesso de escrita, há risco potencial de redirecionamento de credenciais em clientes que aceitem destinos arbitrários; **não demonstrado por execução**. A classificação de risco depende das permissões efetivas e dos chamadores.

## Relevância para SECA (apenas proposta)
Em futuras especificações de persistência offline, distinguir **processo existente** de **instância autorizada**; usar identificador de instância, registro de inicialização, validade temporal e autenticação de canal local, além de PID. Documentar falhas de sondagem como estado indeterminado em vez de assumir identidade válida. Não incorporar código de MemPalace nesta fase.

## Cobertura e pendências
Uma nova entrada com leitura integral verificável nesta etapa. **Sem porcentagem global**: falta obter árvore completa, manifesto reconciliado e commit completo. Nenhum teste foi executado, nenhum componente instalado ou integrado. Ruflo permanece aguardando MemPalace. Núcleo biológico SECA offline, sem pesos pré-treinados e sem ensino de linguagem, preservado.
