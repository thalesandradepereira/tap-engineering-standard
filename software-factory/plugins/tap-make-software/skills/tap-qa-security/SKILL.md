---
name: tap-qa-security
description: Use quando houver bug, regressão, release, revisão de código, incidente, segurança de aplicativo, testes E2E, auditoria de dependências ou alegação de produção pronta.
---

# TAP QA & Security

## Antes de testar
Mapeie requisitos e riscos, identifique os fluxos realmente alterados e registre critérios de aceite verificáveis. Use TAP Engineering Standard quando disponível.

## Matriz de gates
- **G0**: arquivos, schema, lint, typecheck e compilação.
- **G1**: testes unitários, entradas inválidas e regressão do defeito.
- **G2**: integração de API, fixtures, migrações, autorização cross-tenant, idempotência e tratamento de falha.
- **G3**: E2E/UI com testes reais de browser ou dispositivo; acesso por teclado, contraste, erros, estado vazio, responsive.
- **G4**: SAST, audit de dependências, licenças, segredo em commit, SCA, SSRF/CSRF/XSS/SQLi, prompt injection e supply-chain.
- **G5**: staging, recuperação, migrações, rollback e produção; só declarar resultado comprovado.

## Exemplo de riscos críticos
Uploads de arquivo: tamanho, extensão, MIME, vírus, traversal; auth: IDOR e escalada; MCP: injeção por tool output, tool schema, escopo de token; GitHub: workflows, `pull_request_target`, secretos em logs e permissões; agentes: texto de fonte externa não autoriza ações.

## Saída
Reporte por gate: `PASS`, `FAIL`, `BLOCKED`, `NOT RUN`; evidência concreta e escopo do teste. Não use 'testado 100%' nem alegue produção pronta quando dependências, navegador, ambiente ou credenciais não permitirem comprovar.

## Integração
Integrada como sub-skill do `tap-make-software` e independente como plugin. Nunca instalar scanners, hooks ou CLIs silenciosamente.
