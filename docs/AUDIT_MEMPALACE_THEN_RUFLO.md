# SECA — Auditoria sequencial MemPalace → Ruflo
Início: 2026-11-06. **Não concluída.** A auditoria integral exige inventário versionado de todos os arquivos e evidências de leitura.

> **Atualização:** consultar o [estado consolidado](MEMPALACE_STATIC_AUDIT_STATUS.md). O commit está fixado e o inventário completo foi obtido e verificado na parte 14. As informações de bloqueio e cobertura abaixo preservam o registro inicial. Instalação e reprodução mencionadas no plano histórico pertencem a uma fase futura, fora da auditoria estática atual.

## Ordem obrigatória
1. https://github.com/MemPalace/mempalace (branch `develop`; fixar SHA antes de contabilizar cobertura).
2. https://github.com/ruvnet/ruflo (somente após concluir MemPalace).

## Inspeção efetivamente iniciada: MemPalace
- README do projeto e mapa de módulos: https://github.com/MemPalace/mempalace ; https://mempalaceofficial.com/reference/modules
- Arquivo `mempalace/backends/base.py`: localizado na branch `develop`, GitHub informa 982 linhas / 786 linhas de código. Leitura integral ainda pendente.
- Arquivo `mempalace/knowledge_graph.py`: localizado na branch `develop`, GitHub informa 1269 linhas / 1119 linhas de código. Leitura integral ainda pendente.
- Arquivo `benchmarks/BENCHMARKS.md`: localizado na branch `develop`, GitHub informa 770 linhas / 542 linhas de conteúdo. Leitura integral e reprodução pendentes.
- Documentação descreve backends substituíveis, busca lexical e semântica, grafos temporais, agentes e benchmarks R@5. Resultados anunciados não reproduzidos.

## Descoberta relevante para SECA
- O README do MemPalace afirma que a instalação direta no Termux não é suportada devido a dependências compiladas; recomenda Debian PRoot. Assim, não se deve importar o pacote integralmente para o núcleo neural do SECA.
- O MemPalace pode usar embeddings pré-treinados. Para o SECA, usar apenas ideias de persistência e proveniência no laboratório externo, sem pré-treinamento no núcleo.
- Os benchmarks de recuperação documental não são medidas de memória biológica ou consciência.

## Método para concluir 100%
- Fixar commit SHA de cada repositório.
- Gerar manifesto de caminhos e hashes, incluindo documentação, código, testes, scripts, CI e dependências; contar arquivos textuais, binários e gerados separadamente.
- Ler cada arquivo textual até o fim, registrando evidência e decisões por caminho; binários recebem inspeção de metadados/formato.
- Reproduzir instalação isolada, suíte de testes e benchmarks factíveis, anotando bloqueios e limitações.
- Revisar licenças, proveniência, dados externos, riscos de segurança e compatibilidade com Termux.
- Publicar relatório final de cobertura; somente então marcar concluído e iniciar Ruflo.

## Bloqueio desta execução
O ambiente de execução local não conseguiu resolver `github.com` via Git, impedindo clonagem e inventário integral. A inspeção pública por páginas web foi possível, mas não substitui o clone nem leitura completa. Nenhum teste dos repositórios terceiros foi executado nesta etapa.

## Status
MemPalace: **em andamento; cobertura percentual indeterminada**.
Ruflo: **aguardando conclusão de MemPalace**.
