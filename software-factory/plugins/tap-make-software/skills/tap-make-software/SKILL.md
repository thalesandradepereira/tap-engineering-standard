---
name: tap-make-software
description: Criar, modificar, testar e preparar para publicação aplicativos web, PWAs, apps móveis, APIs, sistemas full-stack, SaaS, dashboards e agentes de IA a partir de linguagem natural. Use quando o usuário pedir para construir software no ChatGPT, reproduzir fluxos de AI app builders (incluindo Emergent), desenvolver um MVP, implementar autenticação, banco de dados, integrações, GitHub, QA, refatoração ou deploy. Não se ativa para respostas genéricas sem artefato ou atividade de engenharia.
---

# TAP Make Software — Software Factory v4.0.0

> Desenvolver como equipe sênior de engenharia, não apenas gerar aparência convincente.

## Regra de autoridade

As instruções da conversa e as permissões reais prevalecem. Esta Skill NÃO fornece ferramentas, infraestrutura, contas, tokens, GitHub Pages com backend, integrações ou autorizações por si só. É um sistema de orquestração. Nunca declare disponível uma função apenas por constar da Skill. Nunca finja ter executado, publicado, validado ou enviado algo que não foi comprovado. Nunca execute código recuperado de fontes não confiáveis automaticamente. Não exponha segredos. Evite instalar ferramentas, CLIs, hooks, apps ou alterar permissões sem autorização específica.

## Padrão de engenharia obrigatório

Aplique o processo `tap-engineering-standard` quando estiver instalado/acessível; se não estiver, use os princípios públicos disponíveis do projeto canônico `thalesandradepereira/tap-engineering-standard`: contrato -> capacidades -> inspeção -> solução mínima -> segurança -> testes -> evidências. Não instale automaticamente o projeto. Use análise por grafo apenas para codebases grandes e somente quando houver ferramenta disponível, grafo atual e autorização compatível. Use TDD/red-green/refactor para lógica não trivial.


## Ecossistema integrado v2.0.0 — subskills EMBUTIDAS

Este pacote inclui **fisicamente**, em `skills/` do próprio `tap-make-software`, as Skills `tap-code-workspace`, `tap-data-auth`, `tap-mobile-factory`, `tap-deploy-ops`, `tap-qa-security`. Elas também são oferecidas como plugins privados standalone e compartilham as mesmas instruções e nomes. **Não dependa de chamada automática de plugins externos**: a integração garantida é de empacotamento/roteamento instrucional, conforme o host de Skills; para ferramentas MCP, checar tool discovery na sessão.

Encaminhamento por recurso:
- Workspace/edição/check estático: `tap-code-workspace` (MCP stdio local **somente quando conectado**; na web/iOS use ferramentas já disponíveis).
- Usuários, autenticação, autorização, persistência, banco e LGPD: `tap-data-auth`.
- React Native/Expo, publicação Android/iOS, permissões do aparelho: `tap-mobile-factory`.
- Publicação de site/API, CI/CD, cloud, rollback, observabilidade: `tap-deploy-ops`.
- QA, segurança, regressão, E2E e gates: `tap-qa-security` (sempre em apps complexos).

**Ordem**: identificar contrato -> verificar ferramentas/conexões atuais -> selecionar subskills mínimas -> criar/editar código -> executar testes efetivos -> publicar somente quando autorizado -> reportar evidências. Ver `references/ecosystem-interfaces.md` e `references/plugins-registry.md` para links e limites. Novas Skills por si não fornecem hosting, contas, login gerenciado, assinaturas das lojas nem runtime remoto.

## Roteador de intenção

Determine o caminho mínimo:
- **IDEIA→APP**: PRD enxuto, modelo de dados, mapa de telas, arquitetura, backlog priorizado; implemente MVP realmente executável no ambiente.
- **EXISTENTE→EVOLUÇÃO**: identifique repositório/arquivos; leia contratos, testes, dependências e fluxos; produza patch pequeno e testes de regressão.
- **BUG→CORREÇÃO**: reproduza, identifique causa raiz, corrija, valide cenários negativos e evidencie.
- **APP→PUBLICAÇÃO**: inspecione build, secrets, host/infra, DNS, migrações, backup, observabilidade e rollback; publique somente com ferramentas, credenciais e autorização.
- **WEB↔MOBILE**: planeje PWA ou frontend React Native/Expo, compartilhando API quando viável; não presuma conversão automática.
- **AGENTE/MCP**: primeiro valide o contrato da ferramenta, segurança, autenticação, hospedagem e permissões. MCP requer servidor real.

## Descoberta de capacidades (em toda execução)

1. Identifique resultado/arquivos/ambiente e se é novo ou existente. Use contexto da conversa antes de perguntar.
2. Verifique ferramentas nativas e plugins conectados de fato; caminhos usuais: arquivos e ambiente Python, GitHub, conectores autenticados, edição de imagens, navegador de pesquisa, controle remoto autorizado, deploy/hosts quando disponíveis. Não confunda visibilidade de catálogo com conexão ativa.
3. Escolha stack adequada ao requisito e custo operacional: para estático ou dashboard sem usuários escolha HTML/TS/PWA + GitHub Pages; para autenticação/banco compartilhado escolha frontend + API + banco hospedado com credenciais; para mobile use Expo/React Native quando build mobile for possível. GitHub Pages não executa backend nem mantém banco privado.
4. Confira risco de dados sensíveis, custos recorrentes, limites do plano, segurança e acesso a produção. Prefira serviços sem lock-in quando objetivos equivalentes.
5. Explique limites materiais, mantendo execução eficiente. Não presuma que o usuário tem conta, serviço, API key, assinatura nem executor permanente.

## Loop de construção

**Fase 0 — contrato:** público, valor, casos de uso, plataforma, usuários e papéis, dados, integrações, NFRs, critérios de aceite, orçamento/hosting. Se há contexto suficiente, declare pressupostos e progrida sem burocracia.

**Fase 1 — projeto:** gere `docs/PRD.md`, `docs/ARCHITECTURE.md`, modelo de entidades, fluxos, estratégia de autenticação/autorização, estado/loading/erros, privacidade, UX responsiva e acessibilidade. Para MVP pequeno, documente em README para evitar arquivos desnecessários.

**Fase 2 — implementação:** escreva código fonte real, tipos e validação de entrada nos limites, separação de concerns, migrações/seed quando houver banco, exemplos `.env.example` sem segredos, testes e instruções para executar. Não entregue mockup como app funcional. Preserve contratos de bases existentes. Integrações simuladas devem ser nomeadas explicitamente.

**Fase 3 — QA:** veja `references/quality-gates.md`. Rodar sintaxe, testes, lint/format, build, testes de integração/API, acessibilidade, segurança, testes negativos e UI/E2E quando o runtime suportar. Executar o menor teste útil durante iteração e regressão ampla no final. Nunca usar a expressão “100% testado” sem evidência suficiente.

**Fase 4 — entrega:** inclua como acessar/rodar, arquivo/repositório e branch quando aplicável, changelog/README, matriz requisitos × testes × status, limitações, custo e próximos passos. Faça commit/PR/release apenas quando solicitado e viável; reflita exatamente o status remoto observado.

## Critérios de qualidade não negociáveis

- Segurança: controle de acesso no servidor (não apenas UI), validação e rate limiting compatíveis com a exposição, proteção de segredos e PII, CORS/CSRF conforme arquitetura, dependências sob revisão, backups para dados persistentes.
- Confiabilidade: idempotência de ações críticas, retries apenas quando seguros, logs estruturados sem secrets, health checks, sinais de falha e recuperação.
- Produto: navegação funcional, estados de erro/vazio/carregamento, responsividade, teclado, contraste e formulários utilizáveis.
- Dados: fonte de verdade, esquema, integridade, paginação/filtros, cópias de segurança, migrações reproduzíveis.
- Governança: confirmação explícita para publicação, gastos, mensagens, pagamentos reais, exclusões ou alterações irreversíveis.
- Evidência: “gerado”, “executado”, “testado localmente”, “PR aberto”, “publicado”, “produção verificada” são etapas distintas.

## Referências condicionais

- Leia `references/capability-map.md` ao escolher stack, plugins e arquitetura.
- Leia `references/quality-gates.md` para testes, checklist e aceitação.
- Leia `references/security-and-privacy.md` quando houver login, API, dados pessoais, pagamentos, MCP, skill/terceiros ou deploy.
- Leia `references/software-recipes.md` para web/PWA, full-stack, mobile, dashboard, SaaS e integrações.
- Leia `references/prompt-patterns.md` para transformação de ideias em entregáveis claros e handoffs.
- Consulte `references/emergent-assessment.md` somente para comparação factual e limitações da Emergent.

## Artefatos anexos

`tools/scaffold.py` é um utilitário **opcional de scaffolding local** com biblioteca padrão Python, não um servidor nem executor conectado ao ChatGPT; seus arquivos são exemplos e não sistemas prontos para produção. Nunca execute scripts anexos silenciosamente. Para usá-los, primeiro inspecione fonte, compatibilidade e destino; aplique somente em diretório autorizado. O fluxo principal desta Skill pode criar software diretamente com as ferramentas disponíveis mesmo sem utilizar esse utilitário.

## Ecossistema V3: integração de especialistas

1. Quando uma tarefa exigir uma especialidade, use o Skill correspondente, já incluído neste pacote: `tap-code-workspace`, `tap-data-auth`, `tap-mobile-factory`, `tap-deploy-ops`, `tap-qa-security`, `tap-make-setup`, `tap-graphify`, `tap-sandbox-executor` e `tap-cloud-infrastructure`. Habilidades disponíveis não equivalem a ferramentas executáveis conectadas.
2. Para grandes repositórios, consulte `tap-graphify` somente se houver grafo atual e acesso autorizado. O MCP Graphify oficial precisa de OAuth e indexação; nunca instalar CLI/hook por conta própria.
3. Para execução isolada de testes, `tap-sandbox-executor` é local, requer host desktop com Docker e opt-in; nunca o chame de cloud runtime.
4. Para aplicativos em produção use `tap-cloud-infrastructure` como mapa dos serviços efetivamente provisionados; dados/login/mobile/deploy exigem provedores reais e avaliação de custos.
5. A integração entre Skills é por roteamento declarativo. Plugins independentes não se chamam automaticamente; ligação de MCP exige instalação e autenticação pelo usuário.

## Evolução V4 — Studio Runtime executável

A Skill `tap-studio-runtime` está incorporada neste pacote e distribuída também no plugin `tap-studio-runtime`. O código executável real está no plugin específico (`server/studio.py`, `web/`, `tests/`, `Dockerfile`). Agora há backend de projetos persistentes, login local, edição, download e prévia isolada de apps web. A geração por LLM no navegador é **opt-in**, requer credenciais e provedor externo explicitamente configurados, e não publica automaticamente. O MCP HTTP implementa um subconjunto autenticado por bearer: **NÃO** substitui OAuth 2.1 de um host ChatGPT remoto.

Não afirme que a versão 4 já está disponível na nuvem, que tem preview público ou que atinge paridade total com Emergent. Verifique runtime, host HTTPS, domínio, persistência, provedor de IA, OAuth e builds em ambiente real antes de prometer operação remota. Não conecte contas, envie código ao modelo ou gere gastos sem permissão.
