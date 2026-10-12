# TAP Software Factory Studio — Edição Floot v0.2.1

[**Abrir TAP Studio hospedado**](https://tap-software-factory.floot.app) · [English](README.md) · [Release do núcleo no GitHub](https://github.com/thalesandradepereira/tap-engineering-standard/releases/tag/software-factory-v4.1.0) · [Relatório QA](QA_STATUS.md)

Implementação **web independente, nativa do Floot**, para desenvolvimento principalmente pelo MacBook e uso ocasional no celular. Ela **não executa nem importa automaticamente** o backend original TAP Studio Python/FastAPI.

## O que foi entregue e verificado

- Publicação web ativa pelo Floot no endereço `https://tap-software-factory.floot.app`, em 11/10/2026.
- `/` e `/login` responderam **HTTP 200** no domínio publicado.
- PostgreSQL gerenciado, autenticação, recuperação por e-mail, sessão e propriedade dos projetos por conta.
- Endpoints protegidos para listar, criar, salvar e excluir projetos. **Quatro verificações sem login retornaram HTTP 401** no domínio público.
- Editor HTML/CSS/JS, preview em iframe isolado com CSP restritiva e exportação de HTML independente.
- TypeScript sem erros; as quatro suítes Jasmine selecionadas passaram, com dez casos específicos do Studio.
- Checkpoint restaurável criado antes da publicação. Release **somente web**, sem consumir build nativo iOS/Android.

## Arquivos versionados neste snapshot

A pasta `snapshot/` contém **28 arquivos autorais/de integração** obtidos do projeto Floot. O [manifesto](snapshot-manifest.json) identifica os arquivos e o projeto de origem. O Floot fornece componentes React, helpers de autenticação, configuração do banco e credenciais gerenciadas, que **não foram replicados neste repositório**. Esta pasta serve para **rastreabilidade e auditoria**, não é um export completo do Floot para executar isoladamente.

### Dados e segurança

O [esquema SQL](schema.sql) documenta a tabela `studio_projects` com vínculo a cada usuário. O banco em execução permanece no Floot. Nenhum segredo, URL de banco, cookie de sessão ou senha deve ir para o GitHub.

## Primeiro acesso

O Floot criou a conta administrativa do proprietário **sem senha inicial**. Abra `/login` no endereço publicado, use **Forgot password?** e o e-mail cadastrado para definir uma senha com o código recebido. Nenhuma senha ou código de recuperação foi gerado por mim.

## Limites reais da integração

| Recurso | Situação |
| --- | --- |
| Aplicação web no Floot | **PUBLICADA** |
| PostgreSQL e login | **PROVISIONADOS**, UX autenticada real a confirmar |
| Isolamento por usuário | Condição de proprietário presente em todos os endpoints |
| Integração com GitHub | Snapshot de código e release; **sem sincronização automática** |
| Backend Python original | Separado em `../plugins/tap-studio-runtime` |
| Graphify | Skills preservadas; OAuth/indexação externa pendentes |
| Geração por IA paga | **Disponível com confirmação de créditos, sem chamadas pagas no QA** |
| QA visual autenticado | Pendente após abrir e fazer login no app |
| SLA/uptime | Infraestrutura Floot; sem garantia independente |

Para futuras atualizações: modificar o Floot, testar, republicar e atualizar este snapshot por PR no GitHub. Um commit GitHub **não publica automaticamente** o Floot.

**Made by TAP.**

## TAP AI Builder — versão beta v0.2.1

A edição Floot oferece o painel **"Crie por descrição"**. A geração utiliza **GPT-6 Luna integrado ao Floot** e **consome créditos Floot quando executada**. Cada solicitação exige marcar o aceite e confirmar novamente antes de chamar a IA. O servidor limita o uso a **3 tentativas por usuário autorizado por dia UTC**, verificando o limite de modo atômico. Apenas contas habilitadas na lista de permissões podem gerar conteúdo.

O HTML/CSS/JavaScript retornado passa por validações e aparece em **pré-visualização isolada**. O projeto existente não muda até clicar em **Aplicar no editor** e os arquivos só ficam salvos depois de **Salvar**. Não enviamos o código atual nem registros do banco à IA: somente a descrição e o nome do projeto. Respostas inválidas/truncadas ainda podem consumir créditos e uma tentativa diária. Nenhuma chamada paga foi executada durante os testes de engenharia.

**Segurança:** cadastro público bloqueado no servidor (HTTP 403), logins anteriores preservados; endpoint de IA sem sessão respondeu HTTP 401. TypeScript aprovado, **4 suítes Jasmine** passaram. Teste E2E autenticado usando o modelo real, pentest independente e sincronização automática GitHub→Floot continuam pendentes.

[Relatório QA](QA_STATUS.md) · [SQL de referência](schema.sql) · [Snapshot de 28 arquivos](snapshot-manifest.json)

## Hotfix v0.2.1 — correção de JSON (12/10/2026)

A aplicação Floot foi republicada solicitando JSON Schema estrito ao GPT-6 Luna, extraindo apenas objetos JSON completos, detectando respostas interrompidas e informando créditos cobrados em caso de erro. O teto de saída foi aumentado para **6.000 tokens**, podendo elevar o custo de uma geração longa. As quatro suítes Jasmine e o TypeScript passaram; testes HTTP em produção confirmaram login, bloqueio de chamadas anônimas e cadastro fechado. O projeto original foi preservado. **Nenhuma chamada paga foi realizada no QA do hotfix**; a primeira geração real bem-sucedida ainda precisa ser testada com autorização individual. A tentativa anterior falhou e consumiu **2 créditos Floot**. Veja [relatório do incidente](PATCH_JSON_PENDING.md).
