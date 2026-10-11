# TAP Make Software — Software Ecosystem integrado v2.0.0

**Autor:** TAP Creative Lab. **Distribuição:** plugin privado de orquestração e skill portátil (`skills/tap-make-software/SKILL.md`). **Status:** não é um serviço de hospedagem nem possui servidor MCP próprio.

## Finalidade

Criar, alterar, testar e preparar software via ChatGPT com segurança e qualidade: websites/PWAs, full-stack, APIs, bancos, SaaS, dashboards, apps Expo/React Native, ferramentas e agentes. O resultado concreto depende das ferramentas e autorizações disponíveis em cada conversa, e da infraestrutura do projeto.

## Como usar

No ChatGPT, após conectar/ativar o plugin em uma conversa compatível:

- `@tap-make-software Crie um app de gestão de clientes com login, banco de dados e dashboard.`
- `@tap-make-software Analise o meu repositório GitHub, corrija os bugs, rode testes, atualize README e prepare um release.`
- `@tap-make-software Crie um PWA que possa ser hospedado no GitHub Pages; explique a persistência dos dados.`

A invocação exata e disponibilidade automática dependem da superfície de ChatGPT e da instalação. Alternativamente, leia o `SKILL.md` e use seus procedimentos com um assistente compatível com Agent Skills.

## Limitações reais

- O plugin **não cria, por si, um servidor, VM, banco cloud ou conta**.
- A Skill **não instala** dependências, não altera permissões e não executa comandos ocultos.
- GitHub Pages hospeda apenas arquivos estáticos e não suporta login/banco privado multiusuário sem serviços externos.
- Publicar iOS/Android requer SDK/build service, credenciais, testes e contas de loja.
- Escrever código para uma API/integração não prova que a API real esteja conectada.
- Não há conexão autenticada com uma conta Emergent neste plugin; não importa projetos diretamente da conta Emergent. Utilize código exportado legitimamente.
- Scripts demonstrativos servem para protótipos, não para produção sem revisão e hardening.

## Estrutura

```text
plugin.json
skills/tap-make-software/SKILL.md
skills/tap-make-software/agents/openai.yaml
skills/tap-make-software/references/{capability-map,quality-gates,security-and-privacy,software-recipes,prompt-patterns,emergent-assessment}.md
tools/scaffold.py
tests/test_scaffold.py
```

## Scaffold local opcional

Inspecione `tools/scaffold.py` antes de executá-lo:

```bash
python3 tools/scaffold.py new demo-pwa --template static-pwa --output ./out
python3 -m unittest discover -s tests -v
```

Isso gera um miniapp de tarefas estático com cadastro/edição/exclusão no próprio navegador, filtros e exportação JSON, permitindo prototipagem rápida. Não implementa login verdadeiro, banco multiusuário nem publicação automática. O código pode ser implantado num host de arquivos estáticos. Não requer downloads nem rede para gerar.

## QA e segurança

As referências contêm matrizes de aceitação, fluxos de autorização, estratégias de integração e limitações verificáveis. O fluxo incorpora princípios do projeto canônico [`tap-engineering-standard`](https://github.com/thalesandradepereira/tap-engineering-standard) sem instalar suas ferramentas automaticamente. Para integração, veja as capacidades realmente conectadas no host.

## Changelog

### v1.0.0 — 2026-10-11
- Skill de orquestração com roteamento de modos e referência à engenharia TAP.
- Regras e recipes para web, mobile, full-stack, IA/MCP, dashboards, academia.
- Checklist de segurança/QA e pesquisa de capacidades da Emergent.
- Scaffold demonstrativo sem dependências e testes unitários.

## Integração v2.0.0 (2026-10-11)

Inclui Skills independentes dentro do mesmo plugin: `tap-code-workspace`, `tap-data-auth`, `tap-mobile-factory`, `tap-deploy-ops`, `tap-qa-security` e `tap-make-setup`. Consulte `skills/tap-make-software/references/ecosystem-interfaces.md`. Cada uma existe também como plugin privado separado, mas **não há plugin-to-plugin RPC** implicado. A instalação na conta registra instruções; só um servidor MCP real disponibiliza ferramentas adicionais.

`tap-code-workspace` contém MCP stdio na sua distribuição autônoma. Executá-lo em desktop é opcional e depende de instalação/aprovação do usuário; ele não sobe automaticamente em ChatGPT web/iOS. Outros módulos criam código/configuração para serviços, mas não provisionam contas.

## Plugins satélites criados

- [tap-code-workspace](https://chatgpt.com/plugins/plugins_6acb8adc2eac81918b75b252463b424c)
- [tap-data-auth](https://chatgpt.com/plugins/plugins_6acb8ae6770c81918a94eb161c22a0fc)
- [tap-mobile-factory](https://chatgpt.com/plugins/plugins_6acb8af028c08191b400e3c81e4a1520)
- [tap-deploy-ops](https://chatgpt.com/plugins/plugins_6acb8af9429c81918d5553378de38c1c)
- [tap-qa-security](https://chatgpt.com/plugins/plugins_6acb8b035318819186274cc54abb2f49)

Esses links não ativam uma dependência inter-plugin; cada skill já está instalada dentro do pacote principal ao ativá-lo no host.


## V3 — complementos
- Graphify remoto: MCP oficial incluído em `mcp.json`, sujeito a OAuth e indexação. O Graphify local não foi instalado.
- Sandbox executor: pacote especializado local, separado da Skill principal. Necessita Docker autorizado.
- Cloud infrastructure: diretrizes de provisionamento, sem recursos provisionados.
- Todos os módulos distribuídos separadamente também têm suas Skills incluídas neste orquestrador.

## V4 — TAP Studio Runtime

Nova Skill `tap-studio-runtime` incluída. O serviço executável e testes residem no plugin standalone `tap-studio-runtime` e na pasta `software-factory/plugins/tap-studio-runtime/` no GitHub. Não há endereço de produção nem autenticação OAuth remota configurada automaticamente.
