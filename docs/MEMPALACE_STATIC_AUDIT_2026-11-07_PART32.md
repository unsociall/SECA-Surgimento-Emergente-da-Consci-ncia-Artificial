# SECA — MemPalace, auditoria estática, parte 32

Data: 2026-11-07. Origem: MemPalace/mempalace, commit fixado `f8e35362189bd0a5abf4c0df1dd5bf90ba059176`.

## Inventário e evidências
Consulta da árvore Git recursiva do commit fixado: `truncated=false`, **851 blobs**. Este número é o denominador de arquivos versionados, não um percentual de análise. O manifesto individual completo e a reconciliação das partes anteriores ainda estão pendentes.

| Caminho | Blob SHA | Estado | Evidência |
|---|---|---|---|
| `tests/test_env.py` | `289966ba233d6b15c508360127b4fbad3583748d` | leitura integral estática nesta etapa | GitHub fetch_file, ref fixado, conteúdo completo retornado |
| `tests/test_once.py` | inexistente na árvore fixada | não contabilizar | busca de caminhos na árvore recursiva |
| `mempalace/_env.py` | `24c1add031de4a18b0bedc1cdd23e19574570791` | previamente relatado; não contado novamente | árvore Git |
| `mempalace/_once.py` | `c604d91eb7a9f1504dcf6459304ed0cf92170b11` | previamente relatado; não contado novamente | árvore Git |

## Análise integral de `tests/test_env.py`

O módulo de testes usa `pytest`, `monkeypatch`, `caplog` e fixture `autouse` que limpa a variável `MEMPALACE_TEST_ENV_VAR`. Verifica: vocabulários booleanos verdadeiros/falsos com espaços e capitalização; uso de defaults em ausência e string vazia; `env_flag` retornando `None`; valor booleano desconhecido com aviso único e fallback por chamada; conversão inteira/float; rejeição de `inf`, `-inf`, `nan` e valores inválidos; aviso único para números inválidos; limpeza de strings; separação de listas por vírgula ignorando entradas vazias; e auxiliares `parse_bool`/`parse_number`, inclusive rejeição de booleanos como números e não finitos.

**Limites da evidência:** o arquivo declara expectativas de comportamento; nenhum teste foi executado. O teste de aviso único não demonstra persistência entre processos nem limite de memória do mecanismo de deduplicação. O fallback de `env_bool(VAR, True)` e `env_bool(VAR, False)` com o mesmo valor inválido evidencia que a política padrão é determinada pelo chamador, podendo divergir entre pontos de uso. O conjunto de casos não prova segurança de todas as variáveis de ambiente nem cobertura exaustiva de entrada malformada.

## Relevância ao SECA (somente hipóteses arquiteturais)

1. Classificar parâmetros de integridade de memória, checkpoint e recuperação como **críticos**, exigindo erro explícito em vez de fallback silencioso.
2. Para parâmetros não críticos, permitir defaults documentados, com observabilidade e deduplicação de avisos de capacidade limitada.
3. Separar validação sintática, limites semânticos e política de falha; testar números não finitos e configurações contraditórias.
4. Evitar qualquer dependência de embeddings pré-treinados, ensino de linguagem, rede ou serviços externos no núcleo biológico offline.

## Pendências e restrições

Reconstruir manifesto completo dos 851 blobs com caminho, SHA, tipo, status de leitura e evidência; reconciliar relatórios anteriores sem duplicação; prosseguir nos arquivos ainda não auditados. Ruflo só após certificação integral do MemPalace. Nenhum código foi instalado, executado ou integrado ao SECA; apenas consultas estáticas ao GitHub e publicação deste relatório.
