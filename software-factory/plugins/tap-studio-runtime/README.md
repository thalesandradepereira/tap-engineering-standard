# TAP Studio Runtime 0.1.0 — hosted-ready private beta

This is **new runnable software**, not a Skill-only promise. It implements a FastAPI web UI + REST API + SQLite durable persistence + HTTP JSON-RPC MCP subset. Local integration tests use FastAPI TestClient. No cloud service, OAuth identity provider, isolated arbitrary-code runner, production hosting or AI model is configured automatically.

## Features actually implemented

- Administrator bootstrap, PBKDF2-hashed passwords, token sessions with expiry and logout, brute-force throttling.
- Authenticated per-owner projects persisted in SQLite, safe file names/types, up to 30 text files/project, 100 KB each.
- Prompt → deterministic accessible HTML/CSS/JS starter; file editor, download ZIP, sandboxed preview.
- Optional AI provider with a preconfigured HTTPS OpenAI-compatible `/chat/completions` endpoint, allowlisted hostname, server-side secret, consent checkbox, max 2 requests/minute/user, strict output validation, fail-closed storage and no automatic deployment. The first external call can incur model charges.
- HTTP MCP JSON-RPC tools: `tap_list_projects`, `tap_create_project`, `tap_read_project_files`, `tap_write_project_file`. HTTP Bearer tokens are issued by local login; **not OAuth-compliant ChatGPT remote plugin integration**. Production ChatGPT connection requires external OAuth 2.1 issuer/gateway and endpoint setup.
- No subprocess/shell exposure; self-host locally with Docker Compose. The container port is localhost-bound by default, not public.

## Run on developer machine

```bash
cd tap-studio-runtime
python3 -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
export TAP_STUDIO_DB_PATH="$PWD/studio.db"
export TAP_STUDIO_ADMIN_USER=admin
export TAP_STUDIO_ADMIN_PASSWORD='REPLACE_WITH_LONG_RANDOM_PASSWORD'
python server/studio.py
```

Open `http://127.0.0.1:8080/` in a browser. The API has no public registration. To self-host with Docker, copy `.env.example` to a private `.env`, replace the secret value, then `docker compose -f deploy/compose.yml up --build`. Docker Compose is localhost-only; add trusted reverse proxy with TLS, backup, auth gateway and compliance measures before public exposure. Do **not** use ephemeral SQLite storage on Cloud Run without a separately designed database migration.

## Optional external model

Set `TAP_STUDIO_MODEL_ENDPOINT` to an HTTPS **exact** chat completions URL, `TAP_STUDIO_MODEL_NAME`, `TAP_STUDIO_MODEL_KEY`, and a comma-separated `TAP_STUDIO_ALLOWED_MODEL_HOSTS` containing the endpoint host. Credentials go to the process environment/secret manager only. The user explicitly checks consent before external transmission. External output is untrusted and not production-safe just because it renders. No billing cap is guaranteed by the code; set provider-side hard quotas first.

## QA

`python -m unittest discover -s tests -v`

Cross-user access, input limits, path traversal, failed logins, token revocation, MCP authorization, ZIP integrity and consent gates are tested. Provider integration is mocked/off unless configured. Deploy, multi-instance performance, OAuth and real model cost are not tested. Run behind HTTPS in a controlled environment before sending personal or sensitive data.

## Known differences versus Emergent

No managed always-on hosting, public preview domains, agents orchestrating code/run/debug, React/Expo native pipelines, automatic git pushes, mobile builds, multi-user invitations, paid quotas, OAuth identity, or source-level Graphify indexing. TAP Studio is a self-hostable private-beta control plane; the ChatGPT Skills and other MCP plugins support the broader *workflow*, not automatic in-process tool composition.

## Full-stack single-host deployment (v0.2.0)

A production-shaped deployment template is available in [`deploy/README.production.md`](deploy/README.production.md), using Caddy automatic HTTPS, a non-public FastAPI backend, persistent SQLite volume, Docker secrets for bootstrap credentials and on-demand consistent database backups. It has **not** been deployed to a real host; DNS, container runtime and credentials remain outside this package. Graphify and existing Skills remain separate and intact.
