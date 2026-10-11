# Capability map — verificação, não promessas

## Camadas

| Capacidade | Skill isolada | ChatGPT + ferramentas efetivas | Requisito adicional típico |
|---|---|---|---|
| Entender requisitos, PRD, arquitetura, backlog | Sim | Sim | Nenhum |
| Gerar HTML, TS/JS, React, API, SQL, testes | Instruções | Sim via código e arquivos | Runtime para executar |
| Alterar/revisar GitHub | Não | Se GitHub conectado/autorizado | Repositório/permissões |
| Executar builds e testes | Não | Se Python/container/Codex/terminal disponível | Dependências e ambiente |
| Pré-visualização web interativa | Não | Depende da superfície | Servidor/browser/host |
| Banco de dados persistente compartilhado | Não | Não inerente | Supabase/Postgres/Firebase/Cloud SQL/etc. |
| Login real multiusuário | Não | Código apenas | Auth provider + API/banco + segredos |
| Deploy estático no GitHub Pages | Não | Condicional | Repo/Actions/Pages configurados |
| Deploy API e jobs 24x7 | Não | Condicional | Cloud Run/Render/Fly/VPS etc. |
| Build app iOS/Android | Não | Código Expo possível | EAS/build service/credenciais/lojas |
| Pagamento real | Não | Código e sandbox possíveis | Provedor, KYC, chaves, autorização |
| Automação recorrente | Não | Via scheduler disponível e autorizado | Infra, observabilidade, tokens |
| MCP próprio do plugin | Não | Não implementado nesta versão | Endpoint MCP hospedado com auth |

## Estratégias

1. **Static-first** para protótipos, visualizadores, landing pages e PWA local sem dados sensíveis: HTML/CSS/JS ou Vite/React, GitHub Pages. Dados `localStorage` são do navegador, não compartilhados e não são seguros para cadastro multiusuário.
2. **Managed full-stack** para login, dados, arquivos, colaboração: frontend + API, Postgres hospedado e Auth gerenciado (ou FastAPI/Node com RBAC no servidor). Preferir migrations, RLS quando Supabase, backups e ambientes dev/staging/prod.
3. **Native-mobile** para recursos nativos e lojas: Expo/React Native + API compartilhada; preflight App Store/Play Store e EAS. PWA pode ser opção melhor quando distribuição nas lojas não é necessária.
4. **Automation** para notificações, cron, extração e agentes: scheduler + workers/queue + idempotência + tracing. Nunca confundir GitHub Actions cron com garantia de horário exato ou uptime.

## Handoffs

Quando capacidade faltar, concluir o máximo independente: código, testes locais possíveis, configuração de exemplo, plano de deploy reproduzível; declarar o passo não executado. Nunca inventar link publicado.
