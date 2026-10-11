---
name: tap-make-setup
description: Use quando o usuário ativar o TAP Make Software pela primeira vez ou pedir verificação de integração, ferramentas, ambiente, GitHub, banco, hosting e mobile.
---

# TAP Make Software — onboarding

1. Detecte quais ferramentas estão efetivamente disponíveis e autorizadas. Cheque GitHub, editor de arquivos, runtime de testes, hosting, provedor de banco/IdP e ambiente de build mobile.
2. Confira os cinco módulos internos: `tap-code-workspace`, `tap-data-auth`, `tap-mobile-factory`, `tap-deploy-ops`, `tap-qa-security`. Não os declare instalados como plugins individuais sem verificação.
3. Monte matriz `capacidade / verificada / exige conexão / ausente`.
4. Se houver conexão MCP local, cheque descoberta das ferramentas `tap_*`; se não, informe que o pacote só contém a Skill e que o servidor local satélite precisa de instalação específica em host compatível.
5. Defina projeto piloto pequeno com plano de QA, nenhum deploy oculto, nenhuma instalação silenciosa.

- Verifique MCP Graphify OAuth/indexação, Docker/imagem imutável para sandbox e identidade de infra cloud; relate cada estado separadamente.
