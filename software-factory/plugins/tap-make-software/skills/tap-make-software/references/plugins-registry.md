# Registry de plugins satélites — 2026-10-11

**Propósito:** links administrativos; não configura dependência automática, não concede credenciais nem conexão MCP. As cinco Skills já estão no plugin principal, com conteúdo byte-idêntico às versões standalone criadas.

- `tap-code-workspace`: https://chatgpt.com/plugins/plugins_6acb8adc2eac81918b75b252463b424c
- `tap-data-auth`: https://chatgpt.com/plugins/plugins_6acb8ae6770c81918a94eb161c22a0fc
- `tap-mobile-factory`: https://chatgpt.com/plugins/plugins_6acb8af028c08191b400e3c81e4a1520
- `tap-deploy-ops`: https://chatgpt.com/plugins/plugins_6acb8af9429c81918d5553378de38c1c
- `tap-qa-security`: https://chatgpt.com/plugins/plugins_6acb8b035318819186274cc54abb2f49

**Estratégia recomendada:** ative apenas `tap-make-software` como rota principal. Plugins satélites podem ser usados independentemente quando disponíveis. O runtime de arquivos funciona apenas num host compatível com MCP local stdio que esteja explicitamente configurado.

## V3 — módulos adicionais
- `tap-graphify`: endpoint oficial `https://api.graphify.com/mcp` (OAuth e indexação exigidos; não conectado automaticamente).
- `tap-sandbox-executor`: MCP stdio local com Docker opt-in (não cloud).
- `tap-cloud-infrastructure`: orquestração de provisão, custos e gates; sem cloud provisionada.

- `tap-studio-runtime` — projeto executável de workspace privado com REST, SQLite e MCP HTTP bearer; **código pronto para autohospedagem, NÃO serviço hospedado ou OAuth conectado**.
