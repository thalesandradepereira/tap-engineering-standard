# TAP Software Factory v4.1.0 — Release notes / Notas da versão

**2026-10-11 · Technical preview / Prévia técnica**

[English README](README.md) · [README Português (Brasil)](README.pt-BR.md) · [QA evidence](QA_STATUS.md)

## English — delivered

- TAP Make Software **4.1.0**, with 11 integrated Skills and the official Graphify MCP adapter.
- Ten private plugin packages, including TAP Studio Runtime **0.2.0** (FastAPI, SQLite, login, source editor, ZIP export and isolated preview).
- Protected GitHub CI, documentation quality gate, release notes and bilingual premium documentation.
- Self-hosting blueprint: Docker Compose, Caddy HTTPS, secret-file login bootstrap and SQLite backup utility.
- Floot connection is separate. There is no automatic import/synchronization of the Python project to Floot.

**Evidence:** 174 automated engineering tests were verified on the last protected CI (119 standard, 23 workspace, 8 sandbox profile, 5 scaffolder, 19 Studio). The documentation validator is additional and checked in the release's CI.

**Not operationally verified:** live hosting, TLS on real domain, remote OAuth 2.1 MCP, Graphify indexing, an external AI provider, cloud sandbox jobs, signed mobile builds, browser E2E and production compliance. This is a source-code release, not Emergent feature parity.

## Português (Brasil) — entregas

- TAP Make Software **4.1.0** com 11 Skills integradas e adaptador Graphify MCP oficial.
- Dez pacotes privados, incluindo TAP Studio Runtime **0.2.0** (FastAPI, SQLite, login, editor de código, ZIP e preview isolado).
- CI protegido, validação da documentação em dois idiomas, notas de versão e READMEs premium.
- Configuração para servidor Linux: Docker Compose, Caddy HTTPS, segredo de administrador em arquivo e ferramenta de backup SQLite.
- Floot conectado separadamente; importação do projeto Python e sincronização automática com GitHub não estão implementadas.

**Evidências:** 174 testes automatizados comprovados no último CI protegido (119 padrão, 23 workspace, 8 sandbox, 5 scaffolder, 19 Studio). A validação dos READMEs é adicional e integrada ao CI.

**Não verificado em produção:** hospedagem pública, certificado TLS real, OAuth 2.1 remoto, indexação Graphify, provedor pago de IA, sandbox cloud, compilação mobile assinada, E2E visual e conformidade. Release de código-fonte não significa equivalência operacional com a Emergent.

**Made by TAP** · [Official GitHub repository](https://github.com/thalesandradepereira/tap-engineering-standard).
