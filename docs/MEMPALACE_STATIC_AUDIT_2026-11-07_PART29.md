# MemPalace — auditoria estática, parte 29 (2026-11-07)

## Escopo e evidência
- Repositório de origem: MemPalace/mempalace
- Commit fixado: `f8e35362189bd0a5abf4c0df1dd5bf90ba059176`
- Arquivo: `mempalace/config.py`
- Blob Git SHA retornado pela API: `34b364277fe204584bb463e1dfbf4f3f205c12b2`
- Leitura via API GitHub em quatro intervalos contíguos: linhas 1–450, 451–900, 901–1350, 1351–1739. Classificação: leitura integral do arquivo, com análise estática focada em configuração, validação, segurança e persistência.
- `tests/test_config.py`: **não** contabilizado como concluído nesta etapa.
- Execução de código/testes: nenhuma. Instalação: nenhuma. Incorporação ao SECA: nenhuma.

## Achados de código
1. `sanitize_name` restringe comprimento (128), separadores, `..`, NUL e conjunto de caracteres. `canonical_wing` valida antes e depois da normalização. A compatibilidade de nomes históricos em `wing_aliases` aumenta a superfície de casos-limite; requer testes de colisão e Unicode.
2. `sanitize_kg_value` permite pontuação e restringe NUL/comprimento, enquanto `sanitize_kg_lookup` não limita comprimento para consultar registros legados. A distinção entre entrada nova e busca histórica é intencional.
3. `sanitize_iso_temporal` aceita datas e datetimes UTC canônicos, com validação de calendário. Comparações lexicográficas entre datas puras e timestamps ainda exigem avaliação semântica dos consumidores.
4. `connect_sqlite_read` usa URI `mode=ro`, mas, quando o cabeçalho indica WAL e os arquivos auxiliares estão ausentes, abre conexão SQLite normal (com capacidade de escrita) para permitir a criação dos sidecars. Isto é uma exceção deliberada ao isolamento somente-leitura, não prova de exploração.
5. Prioridade de configuração documentada: ambiente > arquivo > padrão. `resolve_write_routing` diferencia escopo de hooks e CLI, incluindo precedência de configurações legadas. Revisar os consumidores antes de afirmar proteção ponta a ponta.
6. `_make_config_dir` restringe permissões a 0700 somente quando cria o diretório; `init` tenta 0700 também para diretório preexistente. `init` tenta 0600 no arquivo recém-criado. Não inferir permissões de arquivos preexistentes.
7. Configuração inclui alternativas de embeddings pré-treinados e endpoint compatível com OpenAI, além de pesos de recuperação vetorial/BM25. São **incompatíveis** com a restrição experimental do núcleo SECA (sem modelos pré-treinados e sem ensino de linguagem), portanto não se propõe transplantá-los.
8. `max_backups` usa retenção padrão 10; zero desativa a poda. `hallway_min_count` e `topic_tunnel_min_count` definem limiares de coocorrência configuráveis; isso pode inspirar critérios abstratos de consolidação de associações, sem adoção de semântica linguística.

## Recomendações de pesquisa para SECA (somente documentação)
- Separar rigorosamente operações de observação e mutação de memória; documentar exceções de SQLite/WAL.
- Distinguir identidade canônica de aliases históricos e estabelecer testes de colisão e migração.
- Definir contratos de timestamps e retenção de checkpoints verificáveis.
- Não incorporar código, dependências, modelos, serviços ou fluxos linguísticos externos nesta fase.

## Cobertura e pendências
Este registro comprova **um** arquivo integralmente recuperado nesta execução, sem duplicar contagem de relatórios anteriores. Não comprova a conclusão de `tests/test_config.py` nem da árvore Git inteira. O manifesto global de caminhos/blobs e o percentual total continuam **não certificados**. Próximo passo: leitura integral de `tests/test_config.py`, seguida de reconciliação da árvore do commit fixado com os registros prévios. Ruflo não iniciado.
