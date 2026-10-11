---
name: tap-data-auth
description: Use quando um aplicativo precisa de login, usuários, equipes, banco de dados persistente, permissões, migrações, dados sensíveis ou sincronização entre dispositivos.
---

# TAP Data & Auth

## Contrato
1. Defina usuários e organizações, papéis, registros, limites de dados e superfícies expostas.
2. Verifique provedor real disponível (Supabase/PostgreSQL, Firebase, SQL gerenciado, banco existente, backend próprio). **Não presuma conta/credenciais/API keys.** Para MVP local, SQLite pode armazenar dados, mas não torna o app multiusuário remoto automaticamente.
3. Projete entidades, chaves estrangeiras, índices, restrições, timestamps UTC, migrações reversíveis, backups e retenção/LGPD (inclusive tratamento de dados de saúde).
4. Priorize autenticação gerenciada com sessões, cookies `HttpOnly`, `Secure`, `SameSite`, CSRF conforme o fluxo; nunca implementar login só na interface. OAuth PKCE quando apropriado.
5. Autorize cada acesso no servidor/BD por ownership ou tenant. Use RLS quando o banco oferecer e teste que A não lê/escreve registros de B.
6. Crie migrations, testes de isolamento, fixtures com dados falsos, `.env.example` e roteiro de restauração; exija aprovação antes de operações de migração irreversível.

## Decisão por infraestrutura
- **GitHub Pages:** apenas frontend estático; precisa API e armazenamento hospedados externos para login real e persistência entre usuários.
- **PostgreSQL hospedado:** isolamento por `tenant_id`, RLS, migrações, pool de conexões, backup e PITR conforme serviço.
- **Firebase:** regras de segurança negam por padrão, indices e IAM, testes com emulator (não presume serviço conectado).
- **SQLite local:** protótipos/offline; não expor diretamente ao browser para acesso remoto e não prometer concorrência cloud.

## Segurança e QA
Testes de usuário não autenticado, cross-tenant, privilege escalation, IDOR, brute force/rate limits, session invalidation, recovery de senha, consentimento/retenção de dados pessoais. Nenhum dado de saúde em serviços não autorizados.

## Evidência
Entregar esquema/migrações, matriz de papéis, testes de isolamento, disponibilidade real do provedor, status da implantação e rollback. Se não houver credenciais, fornecer projeto e testes locais sem afirmar banco cloud funcional.

## Integração
Ative esta competência dentro de `tap-make-software` para etapas com auth/DB. O plugin standalone é alternativa especializada, não contém credenciais nem instala provedores.
