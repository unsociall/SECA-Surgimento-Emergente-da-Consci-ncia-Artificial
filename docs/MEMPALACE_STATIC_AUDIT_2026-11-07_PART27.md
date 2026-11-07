# Auditoria estática MemPalace — Parte 27 (parcial, escopo delimitado)

Data: 2026-11-07. Origem: MemPalace/mempalace, commit **f8e35362189bd0a5abf4c0df1dd5bf90ba059176**, resolvido pelo endpoint de commit do GitHub. Não executar arquivos, testes ou dependências.

## Evidência e cobertura desta sessão
- `mempalace/config.py`: blob Git **34b364277fe204584bb463e1dfbf4f3f205c12b2**, 73.305 caracteres retornados pelo conector. **Leitura parcial**: foi inspecionado o início do arquivo, não o conteúdo integral.
- `tests/test_config.py`: arquivo consultado e trechos inspecionados, incluindo testes de precedência de configuração e conexões SQLite. **Leitura parcial**; hash do blob não registrado nesta sessão.
- Commit de origem confirmado integralmente, mas **não há manifesto integral da árvore** nem porcentagem verificável. Estes dois arquivos NÃO são contados como concluídos.
- Nenhum teste ou código-fonte de terceiro foi executado. Nenhum componente foi instalado, copiado para o dispositivo ou incorporado ao SECA.

## Observações sustentadas pelos trechos inspecionados
1. `sanitize_name` valida tipo, não-vazio, limite de 128 caracteres, bloqueio de `..`, barras e NUL, além de expressão regular para caracteres permitidos. `normalize_wing_name` produz identificadores normalizados; a relação entre nomes históricos e novos é tratada por `wing_aliases`.
2. `sanitize_iso_temporal` aceita datas ISO e instantes UTC canônicos, valida datas reais e normaliza `+00:00` para `Z`, evitando comparações lexicográficas inconsistentes.
3. `connect_sqlite_read` tenta modo somente leitura e usa conexão normal para o caso específico de banco WAL sem arquivos auxiliares `-wal`/`-shm`. **Implicação de segurança:** esse fallback abre uma conexão com capacidade de escrita, ainda que a finalidade seja leitura. É uma decisão de compatibilidade a avaliar, não uma vulnerabilidade comprovada.
4. Trechos de `tests/test_config.py` especificam precedência de variáveis de ambiente sobre arquivo, leitura de WAL sem sidecars, manutenção de read-only em outros cenários e codificação de caminhos com espaços.

## Pertinência ao SECA — somente estudo
- Considerar validação estrita de identificadores de memória e normalização temporal para eventos sensoriais.
- Para o núcleo biológico offline, **não importar** mecanismos de embeddings linguísticos, ChromaDB ou modelos pré-treinados presentes nas configurações de MemPalace.
- Investigar o custo de manter leitura estritamente somente leitura em checkpoints SQLite e alternativas para consistência WAL.
- Não inferir consciência, aprendizagem ou desempenho a partir de recursos de armazenamento.

## Pendências verificáveis
1. Recuperar árvore completa do commit, produzir manifesto por caminho + tipo + blob SHA, inclusive testes, documentação, dependências e licenças.
2. Ler integralmente `config.py` e `tests/test_config.py`, registrar linhas/intervalos e hashes; só então alterar status para concluído.
3. Reconciliar as partes 1–26 e remover duplicações na contagem.
4. Manter Ruflo em espera até cobertura integral certificada do MemPalace.

**Status:** avanço parcial documentado; sem certificação de cobertura global.
