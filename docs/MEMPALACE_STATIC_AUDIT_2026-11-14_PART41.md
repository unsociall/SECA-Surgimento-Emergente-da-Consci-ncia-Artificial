# SECA — MemPalace, auditoria estática Parte 41 (2026-11-14)

## Proveniência e limites
- Repositório: MemPalace/mempalace
- Commit fixado: `f8e35362189bd0a5abf4c0df1dd5bf90ba059176`
- Arquivo: `tests/test_sqlite_exact_backend.py`
- Git blob SHA informado pelo conector: `d7ea8b2718c35261a5183771ec3c00a7e92ccb19`
- Cobertura nesta etapa: linhas **441–1200**, leitura por intervalos via API GitHub. Os blocos 441–800 e 801–1200 foram recuperados; não se declara leitura integral do arquivo.
- Histórico anterior: linhas 1–440 documentadas na Parte 40; sua cobertura não foi revalidada nesta etapa.
- Inventário histórico: 851 caminhos; reconciliação global pendente, sem porcentagem certificada.
- Nenhum teste executado, código instalado, clonado no Termux ou incorporado ao SECA.

## Observações verificáveis nos testes (não resultados de execução)
1. Abertura somente-leitura verifica `PRAGMA query_only`, recusa gravações e preservação dos bytes originais do banco.
2. Leitor separado por subprocesso consulta uma linha ainda presente no WAL e compara bytes de SQLite/WAL/SHM antes/depois.
3. Leitor `immutable` em cache deve ser reaberto quando WAL e SHM surgirem depois de novo escritor; presença de apenas um sidecar não deve forçar reabertura.
4. Escrita direta e manutenção `VACUUM` devem respeitar lease do palace mesmo com disputa entre threads e processo externo; teste coordena eventos e lock reentrante.
5. Detecção de backend rejeita artefatos mistos, arquivo SQLite vazio e arquivo com conteúdo não SQLite.
6. Busca por similaridade utiliza ranking cosseno; união lexical/vetorial e capacidades não suportadas são verificadas.
7. Abertura concorrente inicial deve compartilhar conexão; teste intercepta `sqlite3.connect` e verifica encerramento.
8. Contagem de facetas e filtros, além de ranking vetorial sem carregar documentos completos, possuem testes de contrato.

## Riscos e lacunas
- São expectativas descritas por testes; não provam comportamento da implementação nem correção em produção.
- Os testes que modificam permissões de arquivo podem se comportar diferentemente em ambientes privilegiados.
- A observação de sidecars WAL/SHM não equivale, isoladamente, a garantia de durabilidade ou recuperação pós-falha.
- Testes com barreiras e timeouts podem ser sensíveis ao agendamento de threads.
- Resta continuar o arquivo a partir da linha 1201 e confrontar os contratos com o backend.

## Relevância ao SECA (somente conceitual)
Priorizar especificações de invariantes de memória episódica: leitura sem mutação, snapshot coerente, exclusão de escritores concorrentes, detecção de artefatos incompatíveis e recuperação após interrupções. Não reutilizar mecanismos de embeddings linguísticos, modelos pré-treinados ou ensino de linguagem. O núcleo biológico offline permanece inalterado.

## Próxima etapa
Ler linhas 1201 em diante até EOF, registrar o total real de linhas, comparar SHA com manifesto e reconciliar evidências arquivo a arquivo antes de qualquer percentual. Ruflo continua bloqueado até a conclusão verificável de MemPalace.
