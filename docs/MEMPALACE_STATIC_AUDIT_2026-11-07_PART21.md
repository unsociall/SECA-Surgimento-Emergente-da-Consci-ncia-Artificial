# SECA — Auditoria estática MemPalace — Parte 21 (2026-11-07)

## Evidência e escopo
Fonte: `MemPalace/mempalace`, commit fixado `f8e35362189bd0a5abf4c0df1dd5bf90ba059176`, branch de origem `develop`.
Arquivo integralmente lido via GitHub: `mempalace/server_registry.py`, blob SHA `660b01ddc6ab9b94b0c7c22da34c8e3be2f5f2ba`. Leitura textual completa até EOF; análise somente estática, sem importação, execução ou testes dinâmicos.

## Arquitetura observada
- `server_state_dir` deriva diretório por caminho canônico do palace; token e `serverinfo.json` são arquivos locais.
- `load_or_create_server_token` utiliza `secrets.token_urlsafe(32)`, trava interprocessos, tenta diretório 0700, remove symlink do token e publica por escrita atômica. Reutiliza token existente entre reinicializações.
- `write_serverinfo` publica PID, host, porta, esquema, read_only, capacidades, fingerprint de busca e caminho canônico.
- `read_live_serverinfo` rejeita registro inválido ou PID não vivo; `clear_serverinfo` só apaga quando PID registrado corresponde ao atual.
- `write_mesh_state` publica pares/perfis e timestamp por escrita atômica; `read_mesh_state` preserva estado anterior, distinguindo `writer_alive`.
- `client_base_url` troca bind wildcard por loopback para clientes locais; `load_server_tokens` tenta primeiro credencial do palace e depois variável de ambiente, sem duplicatas.

## Limitações e hipóteses de risco (não confirmadas por execução)
1. **PID não é identidade autenticada:** reutilização de PID ou registro adulterado pode produzir falso positivo de processo vivo. A verificação não demonstra que o PID pertence ao hub correto. Investigar `_proc.py` e consumidores.
2. **Validação de endpoint:** `read_live_serverinfo` exige apenas porta inteira e host não vazio, sem faixa 1–65535, esquema permitido, correspondência de `palace_path` ou garantia de loopback. `client_base_url` interpola valores do registro; examinar se algum agente pode adulterar o arquivo e redirecionar credenciais.
3. **Permissões de arquivo:** a documentação declara modo 0600, mas a função não define explicitamente chmod no token/registro; depende do contrato real de `atomic_write_text`. Verificar `fsio.py` e testes para confirmar.
4. **Estado de malha:** `read_mesh_state` fornece `written_at` e `writer_alive`, mas não impõe TTL; consumidor deve distinguir dado antigo de dado atual. `peers` e `profiles` são aceitos como dict sem validação profunda.
5. **Rotação de token:** token persistente não tem expiração/rotação explícita neste módulo. Avaliar ciclo de vida e controles do servidor.
6. **Tratamento de erros:** `json.dumps` de dados não serializáveis pode falhar; erros de permissões no `chmod` são ignorados. Determinar expectativas e cobertura dos testes.

Estas observações são **superfícies de revisão**, não vulnerabilidades demonstradas.

## Possíveis adaptações ao SECA (somente estudo)
- Registro local de processos e tarefas com identificador de instância, PID, timestamp e verificação de integridade.
- Checkpoints atômicos e marcação explícita de estado obsoleto; separar estado persistido de estado efetivamente vivo.
- Política de escritor único para impedir corrupção de memória; avaliar recuperação após falha sem depender de hub remoto.
- Credenciais locais apenas se houver comunicação interprocessos; não transferir mecanismos HTTP desnecessários ao núcleo biológico offline.

## Cobertura
Uma nova entrada com caminho, commit e blob SHA, sem afirmar percentual global. O inventário histórico de 851 entradas citado em relatórios anteriores **ainda precisa ser reconciliado e validado no commit fixado**; arquivos repetidos devem ser deduplicados por caminho. O Ruflo permanece pendente até cobertura integral verificável do MemPalace.

## Próximas leituras
`mempalace/_proc.py`, `mempalace/fsio.py` (contrato de permissões), testes de registro e autenticação, depois consumidores de `read_live_serverinfo`.

Nenhum componente de terceiros foi instalado, executado, treinado ou integrado ao SECA.
