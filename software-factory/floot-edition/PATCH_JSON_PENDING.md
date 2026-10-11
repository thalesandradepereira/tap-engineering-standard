# TAP Floot AI Builder — Correção JSON preparada (não publicada)

**Data:** 11/10/2026 · **Status:** proposta em PR draft, ainda NÃO aplicada ao Floot. Código fonte publicado no GitHub NÃO atualiza o Floot automaticamente.

## Diagnóstico e impacto
Uma geração autorizada para o projeto TAP Teste 001 falhou com a mensagem de JSON inválido. O banco registrou uma tentativa com **status failed e 2.0000 créditos Floot consumidos**, em 2026-10-11 19:40:36 UTC. O código do usuário não foi substituído. A resposta bruta do provedor não está disponível; por isso, **a causa exata não foi comprovada** (pode incluir saída truncada, código cercado por Markdown ou texto adicional).

A conta Floot esgotou as 100 ações de desenvolvimento diárias. Segundo a plataforma, as ações de edição/QA/publicação serão liberadas novamente em **12/10/2026 14:00 UTC (11:00 Brasília)**. Não usar outro projeto/conta para contornar essa restrição.

## Alterações propostas
- Solicitar formato JSON Schema estrito ao GPT-6 Luna pela API de respostas do Floot, exigindo as chaves html/css/javascript.
- Aumentar o teto de saída de 3200 para 6000 tokens. **Isso pode aumentar créditos cobrados em uma nova geração autorizada.**
- Diferenciar resposta com status incompleto, inclusive esgotamento de tokens, de JSON inválido.
- Extrair somente objeto JSON completo, com tratamento de chaves dentro de strings. Não inventar fechamento de JSON truncado nem fazer retry automático.
- Exibir créditos contabilizados na mensagem de erro quando informados, mantendo consentimento explícito, limite diário e validações de segurança.
- Acrescentar testes Jasmine cobrindo prefácio, strings com chaves, truncamento e formatos da resposta.

## Critérios de publicação
Após o reset Floot: aplicar as cinco alterações na versão real do projeto Floot, executar typecheck e Jasmine completos, verificar endpoint sem login (401) e cadastro bloqueado (403), criar checkpoint e publicar somente web. **Não chamar o modelo pago no QA automatizado.** Confirmar com o usuário uma única geração real controlada (aceite por chamada); registrar o custo e o resultado. Só depois fechar a PR e criar a tag Floot v0.2.1.

**Made by TAP**
