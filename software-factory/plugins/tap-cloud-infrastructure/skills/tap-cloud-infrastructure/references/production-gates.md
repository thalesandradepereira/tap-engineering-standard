# Production acceptance gates

| Resultado | Precondições e prova | Sem isso |
|---|---|---|
| Backend cloud executa | Conta/projeto, deploy, URL HTTPS, auth, teste runtime | somente fonte/manifesto |
| Banco multiusuário | instância, migrações, políticas RLS, backup/restauração, teste negativo de isolamento | somente esquema |
| Login | provedor autorizado, tokens, sessão, refresh/revogação, teste de autorização por API | somente telas/fluxo |
| Mobile nas lojas | contas Apple/Google, certificados, builds assinadas e aprovação nas stores | código e plano de build |
| Preview de aplicativo | host aprovado e URL real, checagem de conteúdo/status | preview local opcional |
| Deploy automático | CI com credenciais protegidas, autorização, rollback, observabilidade, rollout de staging | workflow ou YAML isolado |
| Agente Graphify remoto | OAuth, repositório explicitamente selecionado e indexado | integração configurada, não ativa |

**Alertas de custo**: quotas, política de retenção, limite de jobs, rede, storage, backups, tabela de preços atual do provedor.
