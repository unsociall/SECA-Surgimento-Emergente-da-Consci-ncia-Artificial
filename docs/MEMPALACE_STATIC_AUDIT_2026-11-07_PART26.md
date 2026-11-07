# MemPalace — Auditoria estática, parte 26 (2026-11-07)

**Escopo:** somente leitura de código remoto via API GitHub. Nenhuma instalação, importação Python, execução de testes, clone no Termux ou integração ao SECA. **Referência:** `MemPalace/mempalace` ref `f8e3536` (abreviada; SHA integral do commit ainda não confirmado). Não confundir SHA de blob com SHA de commit.

## Evidência de leitura integral nesta parte

| Arquivo | Blob SHA Git | Resultado |
|---|---|---|
| `tests/test_fsio.py` | `97bb5c9f32a8da26e621ed5a8bbe3e3db098f41d` | conteúdo integral retornado e inspecionado |
| `tests/test_paths.py` | `5f6c516297bbdf5a498b2e13595e06da6214e789` | conteúdo integral retornado e inspecionado |

`mempalace/fsio.py` foi consultado para cruzamento com os testes (blob `a8e8cf3bd40bec775d00c92c70bb0bbbc69ee033`); **não contabilizar novamente** arquivo anteriormente estudado.

## Resultados: test_fsio.py

- Exercita criação exclusiva de temporários (`O_EXCL`), limite de tentativas somente em colisão, e propagação imediata de erros de permissão; documenta regressão associada ao comportamento de `mkstemp` no Windows.
- Injeta falhas durante serialização, `fsync` e `os.replace`, exigindo preservação dos bytes anteriores nas rotas atômicas.
- Simula compartilhamento de arquivos no Windows: substituição com retentativas limitadas e **sem** escrita direta quando o arquivo está bloqueado por leitor.
- Confirma por expectativa de teste que, quando não é possível criar temporário, existe fallback **in-place** para alguns erros, com aviso; isso **não é atomicidade** e pode truncar dados em interrupções.
- Cobre permissões privadas (0600 fora de Windows), gravação exata de bytes, tratamento de links simbólicos com `follow_symlinks=False`, nome temporário aleatório e leitura concorrente em Windows.
- **Limitação:** testes são evidências de comportamentos pretendidos, não de execução bem-sucedida nesta auditoria; simulações não substituem testes de falha de energia reais, concorrência interprocessos ou inspeção de ACLs.

## Resultados: test_paths.py

- Matriz de nove cenários para diretório de configuração: padrão, XDG absoluto/relativo, expansão de `~`, override e detecção de dados legados.
- Compara derivação de chaves de instância/lock por hash de caminhos normalizados com expressões anteriores.
- Verifica caminhos de estado, locks, identidade e diretório de armazenamento, preservando compatibilidade.
- Inclui teste que varre a AST dos arquivos Python e reprova literais de caminhos `.mempalace` fora do módulo central. **Limitação:** análise AST de literais não identifica todos os caminhos montados dinamicamente, nem código não Python.

## Avaliação de segurança e aplicação ao SECA

1. **Checkpoints e memória episódica:** propor política *fail-closed* para gravações críticas: se não houver publicação atômica, manter versão anterior e registrar falha; não reproduzir automaticamente o fallback truncável.
2. **Arquivos não confiáveis:** considerar política explícita de links simbólicos, criação exclusiva e diretórios sob controle do processo. A existência dos testes não demonstra ausência de TOCTOU.
3. **Localização de dados:** centralizar caminhos offline e testar migração de formatos sem leitura/ensino de linguagem.
4. **Validação:** futuros ensaios próprios do SECA devem incluir interrupções, corrupção, concorrência e reinicialização; **não executar nesta fase**.

## Manifesto e cobertura

Estes dois caminhos são **evidências individuais** com blobs identificados, mas não há aqui árvore Git completa, contagem total de arquivos nem reconciliação deduplicada de todas as partes. **Cobertura global: não certificada; nenhum percentual declarado.** Confirmar SHA integral de origem e construir inventário integral da árvore antes de qualquer afirmação de 100%. Não iniciar Ruflo até concluir MemPalace.

**Preservação:** nenhuma alteração ao núcleo biológico offline do SECA, nenhum modelo pré-treinado, nenhum ensino de linguagem e nenhuma implementação de MemPalace/Ruflo.
