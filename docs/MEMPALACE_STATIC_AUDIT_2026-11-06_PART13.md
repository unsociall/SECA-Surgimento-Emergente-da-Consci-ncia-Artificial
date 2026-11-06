# MemPalace — parte 13: inventário integral e continuidade da leitura

Data: 2026-11-06. Commit fixado: `f8e35362189bd0a5abf4c0df1dd5bf90ba059176`.
Árvore raiz: `701bc6b78262f25b2972b23ba106b30040b76aef`.

## Inventário e integridade

O [manifesto completo](audits/mempalace-f8e3536-inventory.json) enumera 851 entradas de arquivo, incluindo um link simbólico, e permite reconstruir a árvore do commit usando caminhos, modos e hashes Git. Foram reconstruídas e conferidas a árvore raiz e as 109 subárvores. A resposta recursiva não estava truncada. Não há submódulos nessa árvore.

Há 850 arquivos regulares. Pela extensão e pelo modo, 846 são candidatos a texto e quatro são candidatos a mídia binária: três caminhos PNG e um MP4. Essas classificações não são inspeção do conteúdo ou do formato. Dezesseis caminhos são candidatos a artefatos gerados por corresponderem a lockfiles, `package-lock.json` ou `benchmarks/results_*`; a origem da geração não foi auditada. O total declarado é 68.835.127 bytes, incluindo conteúdo repetido em caminhos distintos.

O inventário cobre somente os itens rastreados no commit. Dependências instaláveis, modelos e datasets externos não estão incluídos. Enumerar um arquivo não significa tê-lo lido ou auditado.

## Evidências de leitura desta etapa

| Caminho | Escopo efetivamente revisto |
|---|---|
| `mempalace/backends/sqlite_exact.py` | Linhas 1251–2270, até EOF; linhas 1–108 para conferir imports e dependências |
| `LICENSE` | Texto integral |
| `pyproject.toml` | Texto integral |
| `mempalace/backends/__init__.py` | Texto integral |
| `mempalace/backends/registry.py` | Texto integral |
| `mempalace/backends/_magic.py` | Texto integral |
| `mempalace/backends/_filters.py` | Texto integral |

Os hashes dos seis arquivos novos foram recalculados a partir dos textos recebidos e coincidem com o manifesto. Para `sqlite_exact.py`, o texto recebido contém 2270 linhas, 95.869 bytes e blob `427287c1213de009141a5bcaf24188c1f10b807e`. Receber o arquivo completo serviu para verificar seu hash e EOF; não é contabilizado como uma nova leitura das linhas 109–1250 nesta etapa.

As partes 6 e 8 já registravam leitura até EOF de SQLite; as partes 9–12 são releituras parciais e não anulam aquele registro. Os sete registros históricos da parte 8 coincidem com os blobs do inventário. Essa conferência valida a identidade do conteúdo atribuído ao commit, não certifica a qualidade das análises anteriores.

## Observações do backend SQLite

Fonte primária: [sqlite_exact.py no commit fixado](https://github.com/MemPalace/mempalace/blob/f8e35362189bd0a5abf4c0df1dd5bf90ba059176/mempalace/backends/sqlite_exact.py).

1. `get_recent` (linha 1289) separa grupos de timestamps UTC e demais formas, ordena candidatos com `recency_key` e hidrata os IDs selecionados. A correção temporal depende também de `timeutil.py`, ainda pendente nesta sequência.
2. `iter_metadata` (1405) percorre o cursor sem materializar todos os documentos; aplica projeções, filtros e lotes de até 900 valores em um campo de associação. Isso é um padrão útil para inspeção de grandes históricos de laboratório.
3. `facet_counts` (1531) aceita chaves validadas e filtros traduzíveis em SQL; recusa filtros que exigiriam avaliação local. A declaração explícita dessa limitação evita apresentar agregações incompletas como completas.
4. A busca lexical (1562 e 1583) usa FTS quando disponível e BM25 Python como alternativa. No caminho FTS com `where`, não há `LIMIT` SQL: os candidatos são materializados e hidratados antes do filtro Python. No fallback, os documentos filtrados também são carregados para pontuação. O custo pode crescer com o corpus; não foi medido.
5. `maintenance_state` (1658) pode substituir falha de contagem por zero e omitir dados adicionais em exceções. Para o SECA, ausência de observação deve ser distinguida de uma população vazia ou de uma verificação bem-sucedida.
6. `run_maintenance` (1689) diferencia `ANALYZE` de `VACUUM`, e este último altera temporariamente o modo de transação. Os cenários de interrupção e concorrência ainda dependem da revisão dos testes e chamadores.
7. A abertura somente leitura (1790–1922) escolhe a forma de conexão conforme WAL/SHM, mantém handles separados e não chama `_init_schema` nesse modo. O texto define proteções; seu funcionamento sob concorrência não foi testado nesta etapa.
8. A inicialização de esquema e as migrações FTS (1923–2100) sincronizam rowids e criam índices derivados dos metadados em abertura gravável. Falhas de operação na preparação FTS são tratadas como indisponibilidade do recurso; distinguir causas merece revisão de observabilidade.
9. `delete_collection` (2242) usa o lock do handle e faz várias operações antes do commit; seu corpo não obtém `mine_palace_lock` nem explicita rollback. A revisão dos chamadores é necessária antes de classificar esse caminho como um defeito de concorrência ou atomicidade. Não foi reproduzida uma falha.

## Registro, filtros e dependências

- `registry.py` define precedência de configuração e descoberta por entry points. `ep.load()` e construção de instâncias ocorrem sob um `Lock`; verificar reentrância de plugins é uma questão aberta, não um deadlock observado. O carregamento de plugins envolve código executável e deve ser considerado na revisão posterior de isolamento.
- `_magic.py` implementa sondagem de cabeçalhos por SQLite, cache por dispositivo/inode e retenção de conexões de sondagem em POSIX. O módulo explica a motivação relacionada a locks de descritores; sua compatibilidade com diferentes ambientes e o ciclo de vida dessas conexões não foram validados aqui.
- `_filters.py` rejeita nomes de operadores desconhecidos e compartilha a avaliação em Python entre backends. `validate_where` não equivale a uma validação integral do formato e do tipo dos operandos; revisar coerência com o caminho SQL e casos negativos.
- A licença raiz declara MIT. Isso não estabelece a licença de cada dependência, mídia ou dataset. `pyproject.toml` declara Python >=3.10 e inclui ChromaDB, NumPy, Hugging Face Hub e tokenizers como dependências principais. Escolher SQLite não transforma a instalação padrão em um pacote sem essas dependências.

## Aplicação ao SECA e estado

Avaliar conceitos de projeção seletiva, declaração de capacidades, identidade do backend, proveniência e migração verificável no laboratório externo. Tratar erros de leitura e ausência de dados como estados distintos. Nenhum componente foi incorporado ao núcleo neural.

Há seis novas leituras integrais e sete registros históricos de leitura até EOF, em 13 caminhos distintos. **Isso não é auditoria semântica completa de 13 arquivos, nem auditoria integral do MemPalace.** Os 838 caminhos sem esse registro seguem pendentes; mídia e link simbólico exigem critérios próprios de inspeção.

Nenhuma instalação, importação do pacote, execução de testes, benchmark ou alteração no Termux. Foram executadas somente verificações de metadados, hashes e estrutura documental. Ruflo permanece aguardando a conclusão da leitura e auditoria estática do MemPalace.

Próximos arquivos: `mempalace/lexical.py`, `mempalace/timeutil.py`, `mempalace/stored_text.py` e `mempalace/config.py`, seguidos dos testes relacionados. Ver [estado consolidado](MEMPALACE_STATIC_AUDIT_STATUS.md).

Elaboração com assistência do ChatGPT (OpenAI).
