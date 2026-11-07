# SECA — Auditoria estática MemPalace — Parte 31 (2026-11-07)

## Escopo e rastreabilidade
Repositório-fonte: https://github.com/MemPalace/mempalace
Commit fixado: `f8e35362189bd0a5abf4c0df1dd5bf90ba059176`.
Método: leitura remota do texto completo via API GitHub; nenhum código executado, nenhuma instalação ou clonagem no dispositivo.

| Caminho | Blob Git SHA-1 | Estado nesta etapa |
|---|---|---|
| `mempalace/_env.py` | `24c1add031de4a18b0bedc1cdd23e19574570791` | leitura integral e análise estática |
| `mempalace/_once.py` | `c604d91eb7a9f1504dcf6459304ed0cf92170b11` | leitura integral e análise estática |

A leitura integral acima se refere aos dois arquivos obtidos nesta etapa, não à cobertura global do repositório. Não se afirma que sejam inéditos no histórico de auditorias sem reconciliação.

## Análise técnica de `_env.py`
- Centraliza a interpretação de variáveis de ambiente em funções `env_str`, `env_flag`, `env_bool`, `env_int`, `env_float` e `env_list`.
- `parse_bool` aceita um conjunto fechado de valores verdadeiros/falsos, ignorando diferenças de caixa e espaços nas bordas.
- `parse_number` rejeita booleanos e floats não finitos; valores inválidos geram fallback ao padrão, com aviso deduplicado por nome e valor.
- `env_list` separa por vírgulas e remove itens vazios; não oferece escape de vírgulas ou validação semântica de itens.
- Risco de desenho: fallback silencioso para default após warning pode ser inadequado em configurações de segurança críticas; é preferível falhar explicitamente para controles obrigatórios. Não constitui vulnerabilidade comprovada.
- Limitação: `env_int` aceita inteiros arbitrariamente grandes, sem validação de faixa; consumidores precisam impor limites.

## Análise técnica de `_once.py`
- Implementa deduplicação de avisos por processo com `set` global e `threading.Lock`.
- A região crítica torna `first_time` atômica entre threads do mesmo processo.
- `reset` limpa o conjunto sob lock, destinado a testes; não há persistência entre reinicializações.
- O conjunto cresce conforme a cardinalidade de chaves distintas. Entradas externas variáveis podem ampliar o consumo de memória, dependendo do padrão de uso.
- Não há sincronização entre processos; garantias são estritamente locais ao processo.

## Relevância para o SECA
1. Separar configuração experimental de parâmetros essenciais de integridade; valores inválidos em limites críticos devem impedir a inicialização do subsistema afetado, não retornar defaults perigosos.
2. Registrar avisos diagnósticos de maneira limitada em memória, com critérios de expiração/capacidade e sem confundir deduplicação de logs com memória episódica.
3. Não transportar código, modelos pré-treinados, embeddings, treinamento de linguagem nem dependências para o núcleo biológico offline. Todas as ideias permanecem conceituais.

## Controle de cobertura
O inventário de 851 blobs foi informado em relatório anterior, mas **não foi novamente reconciliado nesta etapa**. Não atribuir percentual. A confirmação de cobertura exige manifesto por caminho e blob SHA, vínculo com evidência de leitura e deduplicação de registros anteriores.

## Próximo passo
Verificar os testes específicos de parsing de ambiente e deduplicação; depois confrontar o manifesto completo do commit com todos os relatórios. Ruflo permanece bloqueado até o encerramento certificado de MemPalace.
