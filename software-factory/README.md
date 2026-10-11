# TAP Software Factory — code and plugin ecosystem

Monorepo export synchronized from the user's private ChatGPT plugins on 2026-10-11.
This directory keeps source for **all nine plugins**, with their Agent Skills and executable local MCP server sources where included. Their private ChatGPT installation state is separate from this source tree.

## Contents

- **tap-make-software** v3.0.0: 30 files, 10 Skill(s), MCP config.
- **tap-code-workspace** v1.0.0: 8 files, 1 Skill(s), MCP config.
- **tap-data-auth** v1.0.0: 4 files, 1 Skill(s).
- **tap-mobile-factory** v1.0.0: 4 files, 1 Skill(s).
- **tap-deploy-ops** v1.0.0: 4 files, 1 Skill(s).
- **tap-qa-security** v1.0.0: 4 files, 1 Skill(s).
- **tap-graphify** v1.0.0: 7 files, 1 Skill(s), MCP config.
- **tap-sandbox-executor** v1.0.0: 8 files, 1 Skill(s), MCP config.
- **tap-cloud-infrastructure** v1.0.0: 5 files, 1 Skill(s).

The main plugin (`plugins/tap-make-software`) contains **10 Skills**, including Graphify, sandbox testing, cloud infrastructure, authentication/data, mobile, deploy, QA and setup. Specialist plugins are separately packageable.

## Graphify — upstream vs TAP integration

- Original software (not vendored or installed here): https://github.com/Graphify-Labs/graphify
- Original hosted MCP public instructions: https://github.com/Graphify-Labs/graphify-mcp
- TAP integration: `plugins/tap-graphify/skills/tap-graphify/SKILL.md` and `plugins/tap-graphify/mcp.json`
- Main plugin also declares the official hosted Graphify MCP endpoint; connection and OAuth are **not** automatic. Indexing a private repo requires separate authorization. The code-mapping CLI is named `graphify`, official package `graphifyy`. No Graphify CLI, hooks or third-party scripts have been installed.
- A license notice/link is in `GRAPHIFY_INTEGRATION.md`.

## Security and operational reality

Repository presence != plugin connected != tools executable != infrastructure provisioned.
`tap-sandbox-executor` is an opt-in **local** Docker test server, not a cloud sandbox.
`tap-code-workspace` is local, disabled for writes unless opted in.
Database/Auth cloud, mobile signed builds, CI credentials, hosted execution, production deployment, and OAuth Graphify require separately provided infrastructure and relevant permission.
Never add secrets to Git. Do not turn on automatic hooks or unreviewed installers.

See `QA_STATUS.md` for what was locally tested. GitHub source sync alone does not test ChatGPT plugin connections.

## V4 — Self-hosted TAP Studio Runtime

`plugins/tap-studio-runtime` contains runnable code for a browser-based project editor, authenticated API and persistent SQLite storage; its model API is opt-in. Hosting, OAuth, credentials, actual model calls and production security gates require separate services and approval. The main plugin now includes 11 Skills, preserving Graphify.

## Full-stack TLS self-hosting

The [TAP Studio deployment playbook](DEPLOY_FULLSTACK.md) describes a production-shaped Docker Compose/Caddy configuration, persistent SQLite and backups. Not yet deployed. Core TAP Make Software v4.1.0 and TAP Studio Runtime v0.2.0.
