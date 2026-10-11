---
name: tap-cloud-infrastructure
description: Use quando um software gerado pelo TAP Make Software precisa funcionar na nuvem com backend, credenciais, banco, login, CI/CD, observabilidade, domínios ou hospedagem de produção.
---
# TAP Cloud Infrastructure

Especialidade: preparar implantação em ambiente próprio, separando configuração de executores e serviços reais. **Esta Skill não provisiona servidores, credenciais, DNS ou banco** e não substitui conectores conectados.

1. Identifique requisitos e contas efetivamente disponíveis (GitHub, Google Cloud, PostgreSQL/Supabase, Expo EAS, Apple/Google Stores). Não presuma conexões.
2. Separe três domínios: frontend estático/PWA (GitHub Pages); API/serviços (Cloud Run ou backend host aprovado); DB multiusuário/auth (PostgreSQL gerenciado + provedor Auth com políticas).
3. Para execução de código não confiável use sandbox/worker isolado, nunca execute na instância MCP principal, com limites, fila, TTL, isolamento de rede, storage efêmero e auditoria. Requer infraestrutura e revisão antes da operação.
4. Antes de publicar peça autorização apropriada para conta, recursos/custos e ações externas; jamais grave secrets em GitHub, logs ou markdown.
5. Produza IaC/manifesto, separação staging/prod, migrações, backup/restauração, logs redigidos, limites de custo, alertas e rollback.
6. Rode testes locais e integração quando possível, depois valide status real da plataforma. PR aprovado não é deploy; deploy não é serviço verificado em produção.
7. Gerencie diferentes perfis (web, mobile, data/auth, QA) com `tap-make-software`, `tap-data-auth`, `tap-mobile-factory`, `tap-deploy-ops`, `tap-qa-security` quando disponíveis.

Consulte `references/production-gates.md` para critérios de aceite e dependências ainda pendentes.
