# Integração do TAP Software Ecosystem v2

## Contrato de handoff (documentos/artefatos, não RPC mágico)
Toda subskill recebe um contrato contendo: objetivo, workspace/repositório, branch, ambiente, dados e nível de sensibilidade, serviços realmente conectados, autorização, riscos, testes solicitados.

Entrega de cada etapa: arquivos alterados, diff, testes realizados com comandos/resultado, dependências, infraestrutura pendente, status (`PLANNED`, `GENERATED`, `LOCAL_TESTED`, `DEPLOYED`, `PRODUCTION_VERIFIED`) e próximos riscos.

## Interfaces de integração
- **ChatGPT Skills:** cinco diretórios embutidos em `skills/`; descoberta depende do host. As cópias standalone são opcionais e não são dependências obrigatórias.
- **GitHub:** use a conexão instalada e permissão do usuário para commits/PRs/CI. Sem conexão, gerar patch/ZIP.
- **Arquivos e QA:** ferramentas nativas ChatGPT quando disponíveis; nunca alegar que o pacote executou comandos sozinho.
- **MCP local `tap-code-workspace`:** código e `mcp.json` estão somente no plugin satélite. A instalação privada em nuvem não executa processos locais no iPhone.
- **DB/Auth:** projetar e implementar conforme stack; provisioning/login multiusuário dependem de DB e IdP autorizados.
- **Mobile:** código Expo/React Native; build/assinatura/publicação demandam ambiente/contas.
- **Deploy:** CI + hosts existentes; GitHub Pages é estático; cloud API/DB exige provedor e credenciais.

## Regra de regressão
Para qualquer etapa que envolva autenticação, persistência ou escrita: executar teste negativo de usuário sem privilégios e diff revisável. Não atribuir a plugins funções que não expõem via servidor ou host.
