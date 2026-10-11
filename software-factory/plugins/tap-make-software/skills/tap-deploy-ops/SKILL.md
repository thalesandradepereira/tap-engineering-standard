---
name: tap-deploy-ops
description: Use quando for necessário publicar site, API, SaaS ou app, configurar GitHub Actions, CI/CD, domínio, monitoramento, ambiente de staging ou rollback de deploy.
---

# TAP Deploy & Ops

## Pipeline de lançamento
1. Identifique stack, DNS, domínio, conta de hospedagem e permissões reais. Nenhuma Skill cria uma VM/serviço automaticamente.
2. **Site estático/PWA:** GitHub Pages, Cloudflare Pages ou similar. Nunca atribuir banco privado, login no servidor ou segredos a GitHub Pages.
3. **Backend:** Cloud Run, Render, Fly, AWS, Azure, hospedagem gerenciada; exigem billing, credenciais, quotas e configuração próprias. Armazene secrets no secret manager, não no repositório.
4. Gere pipeline de build, testes, SAST/dep scanning, artefatos e deploy em staging; configure deploy produção com gates e rollback testável.
5. Verifique migrações antes/depois do deploy, observabilidade, health check, roteamento, TLS, CORS, cache e políticas de backup/restauração.
6. Para publicações externas ou alteração de gastos/ACL, solicite autorização compatível; não alterar configurações de segurança ocultamente.

## Evidência exigida
Identifique commit/branch, CI run/conclusão real, URL servida, probe HTTP quando disponível, teste de funcionalidade pós-deploy, versão e plano de rollback. Distinguir ações enviadas e resultados finais; deploy verde não prova app saudável.

## Integração
Use dentro do `tap-make-software` quando a entrega exige publicação; o plugin standalone não dispõe de servidor hospedado, domínio ou provedores pré-autorizados.
