# TAP Software Factory Studio — Edição Floot v0.1.0

[**Abrir TAP Studio hospedado**](https://tap-software-factory.floot.app) · [English](README.md) · [Release do núcleo no GitHub](https://github.com/thalesandradepereira/tap-engineering-standard/releases/tag/software-factory-v4.1.0) · [Relatório QA](QA_STATUS.md)

Implementação **web independente, nativa do Floot**, para desenvolvimento principalmente pelo MacBook e uso ocasional no celular. Ela **não executa nem importa automaticamente** o backend original TAP Studio Python/FastAPI.

## O que foi entregue e verificado

- Publicação web ativa pelo Floot no endereço `https://tap-software-factory.floot.app`, em 11/10/2026.
- `/` e `/login` responderam **HTTP 200** no domínio publicado.
- PostgreSQL gerenciado, autenticação, recuperação por e-mail, sessão e propriedade dos projetos por conta.
- Endpoints protegidos para listar, criar, salvar e excluir projetos. **Quatro verificações sem login retornaram HTTP 401** no domínio público.
- Editor HTML/CSS/JS, preview em iframe isolado com CSP restritiva e exportação de HTML independente.
- TypeScript sem erros; as duas suítes Jasmine selecionadas passaram, com dez casos específicos do Studio.
- Checkpoint restaurável criado antes da publicação. Release **somente web**, sem consumir build nativo iOS/Android.

## Arquivos versionados neste snapshot

A pasta `snapshot/` contém **19 arquivos autorais/de integração** obtidos do projeto Floot. O [manifesto](snapshot-manifest.json) identifica os arquivos e o projeto de origem. O Floot fornece componentes React, helpers de autenticação, configuração do banco e credenciais gerenciadas, que **não foram replicados neste repositório**. Esta pasta serve para **rastreabilidade e auditoria**, não é um export completo do Floot para executar isoladamente.

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
| Geração por IA paga | **Não ativada** |
| QA visual autenticado | Pendente após abrir e fazer login no app |
| SLA/uptime | Infraestrutura Floot; sem garantia independente |

Para futuras atualizações: modificar o Floot, testar, republicar e atualizar este snapshot por PR no GitHub. Um commit GitHub **não publica automaticamente** o Floot.

**Made by TAP.**
