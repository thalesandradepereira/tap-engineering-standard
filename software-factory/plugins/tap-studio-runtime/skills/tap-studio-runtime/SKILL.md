---
name: tap-studio-runtime
description: Use quando o usuário solicitar um editor de apps acessível por navegador, controle de projetos persistentes, preview HTML/CSS/JS, integração com serviço de geração por IA ou execução de servidor TAP Studio Runtime.
---
# TAP Studio Runtime

Use a aplicação self-hosted em `server/studio.py` para projetos web privados. Antes de operar, confirme host, autenticação, persistência e custos. **O código existir no GitHub não prova que o serviço esteja hospedado nem que o plugin MCP remoto esteja conectado.**

1. Crie projeto com POST `/api/projects` ou MCP `tap_create_project`, depois edite arquivos com operações autenticadas. Gerador padrão é determinístico, **não um LLM**.
2. A geração por LLM usa `/api/projects/ai-generate` apenas quando endpoint externo, token, nome de modelo e host explicitamente permitido estão configurados e quando o usuário consente com envio da descrição e eventuais custos. Nunca transmitir dados privados automaticamente.
3. Visualização apenas em iframe isolado e sem deploy; validar todo código gerado antes de expor externamente.
4. Login é local; o endpoint HTTP `/mcp` NÃO implementa autorização OAuth 2.1 exigida para integrações protegidas remotas do ChatGPT. Não inventar URL de produção.
5. Banco SQLite precisa de volume persistente/backup. Execução arbitrária não está presente; para comandos/testes usar sandbox autorizado separado. Atualize README e testes, preserve Graphify e status honesto.

Seguir `tap-engineering-standard`, `tap-qa-security`, `tap-data-auth`, `tap-deploy-ops` e `tap-graphify` quando disponíveis e relevantes; nunca conceder permissões extras implicitamente.
