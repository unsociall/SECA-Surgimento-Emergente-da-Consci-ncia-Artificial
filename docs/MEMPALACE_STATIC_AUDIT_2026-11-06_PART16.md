# MemPalace — auditoria estática, parte 16 (2026-11-06)

## Fonte e escopo
Commit fixado: `f8e35362189bd0a5abf4c0df1dd5bf90ba059176`.

Leitura integral do conteúdo retornado pelo GitHub para três arquivos (linhas calculadas incluindo possível linha final vazia):
- `mempalace/lexical.py` — blob `bc0ab7a4e09dab8811062b7d2bd39dce233ae344`; 73 linhas na separação por newline.
- `mempalace/timeutil.py` — blob `e8b512b8da0969f79ccffa8284433a2425fbfa94`; 118 linhas.
- `mempalace/stored_text.py` — blob `27362a9a1b4c2ed040c91e01cb7c5a9057ccd179`; 264 linhas.

## Constatações
1. `lexical.py`: tokenizer Unicode com tokens de comprimento >=2, lowercase, stopwords opcionais; BM25 com IDF suavizado, k1=1.5, b=0.75, frequência por termo e normalização por comprimento. Pontua sobre a coleção de candidatos recebida, não sobre corpus global necessariamente.
2. `timeutil.py`: novas escritas em UTC ISO-8601 com offset; valores históricos ingênuos interpretados como hora local; `recency_key` ordena por instante com prioridade inferior para strings inválidas e ausências. `recency_floor` calcula limite textual conservador de um dia.
3. `stored_text.py`: política de escape reversível para NUL, surrogate isolado e prefixo reservado, com flag em metadados. IDs e chaves com caracteres inválidos são rejeitados. `dumps_internal` preserva surrogates em escape JSON; `dumps_client` substitui por U+FFFD, deliberadamente com perda apenas na apresentação.

## Questões abertas
- Verificar testes de transição de fuso horário/DST e datas ingênuas em ambientes distintos.
- Verificar os testes de round-trip, filtros SQL e flag de escape em atualizações parciais.
- Verificar limites e coerência do BM25 entre backends e corpus de candidatos.
- A leitura estática não demonstra correção em execução nem segurança integral.

## Aplicação conceitual ao SECA
Separar registro de experiência, codificação reversível, indexação, recuperação temporal e avaliação de relevância. Preservar núcleo biológico offline; não importar modelos pré-treinados, embeddings de linguagem nem mecanismos de instrução linguística.

## Cobertura
O manifesto do relatório Parte 14 declara 851 entradas rastreadas, 850 arquivos regulares e um link simbólico. A Parte 14 declara 13 caminhos distintos com registros integrais até EOF; estes três caminhos são adicionais **se ausentes do manifesto de cobertura anterior**, a confirmar na consolidação. Não converter isso automaticamente em porcentagem de auditoria semântica. Ruflo ainda não iniciado. Nenhuma instalação, clonagem, importação, execução de testes ou implementação.
