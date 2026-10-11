# TAP Studio full-stack deployment (self-hosted, single host)

This is an **operational blueprint**, not a currently running cloud service or an OAuth-enabled ChatGPT integration. Uses one FastAPI process, persistent SQLite volume, and Caddy TLS reverse proxy. It does not run arbitrary code or provide sandbox agents. Default AI generation remains OFF. Docker must be installed on an authorized, patched Linux server. **Never run third-party installation scripts or grant Docker privileges from an untrusted user.**

## Prerequisites
- Linux server accessible on TCP 80/443, Docker Engine with `docker compose`, and public A/AAAA DNS record pointing the chosen domain to the server. DNS and reverse-proxy TLS must be tested; do not use `localhost` or `example.com` in real deployments.
- Server-level firewall, SSH key authentication, encrypted/offsite backups, reliable persistent disk and monitoring. Set reasonable compute, storage and network cost caps at the host provider.
- Work within `software-factory/plugins/tap-studio-runtime` after reviewing all files. Clone or upload only from the official repository.

## Configuration (the operator executes these on their own server)
1. Create a **private server environment file** from `deploy/.env.production.example` and replace `TAP_STUDIO_DOMAIN`, `TAP_STUDIO_ADMIN_USER`, `TAP_STUDIO_SECRET_FILE`. Do not commit that file or passwords. Store it OUTSIDE the public Git repository.
2. Generate a strong password with a trusted password manager. Place it in the secret file at the `TAP_STUDIO_SECRET_FILE` absolute path, readable by numeric UID **10001** inside the app container (file-backed Docker secrets cannot automatically remap file ownership). Restrict its permissions and directory to authorized accounts; consider a host secret manager.
3. Validate configuration safely: `docker compose --env-file /secure/location/tap-studio.env -f deploy/compose.production.yml config --quiet`. Avoid printing `docker compose config` containing environment details in shared logs.
4. Build and start: `docker compose --env-file /secure/location/tap-studio.env -f deploy/compose.production.yml up -d --build studio caddy`.
5. Verify `https://<your-domain>/health` returns status `ok`, and that login, project persistence after a service restart, no unauthenticated API read, and TLS certificate issuance work. The `/mcp` path uses private bearer sessions only, **not OAuth 2.1**; do not connect it to ChatGPT as a public MCP server.
6. Create a consistent SQLite backup (on-demand): `docker compose --env-file /secure/location/tap-studio.env -f deploy/compose.production.yml --profile backup run --rm --no-deps backup`. The backup stays in `tap-studio-backups` named volume; arrange separate encrypted offsite extraction, restore rehearsal, pruning and schedule. No automatic backups or retention are configured by this file.

## Security / incident plan
- **Never** change Compose or Caddy configuration to publish the backend port 8080 directly.
- Password bootstrap only creates the first user. Rotating the secret file does **not** automatically change an existing user's password or revoke sessions; implement explicit account lifecycle management before offering a multiuser SaaS.
- Use HTTPS only, and restrict admin access to your trusted user network where possible. Password session tokens are not OAuth. Password protection does not imply SOC2/LGPD readiness.
- Use a single Studio instance. SQLite/WAL on a single persistent local filesystem is not suitable as an automatic multi-region or stateless serverless database; cloud HA requires a database migration and independent tests.
- Test restore in staging: stop the app, preserve the original volume, restore the validated backup into a separate volume, start the staging stack and verify data. Never overwrite live data as a quick rollback. Apply a reviewed code rollback without changing the SQLite schema unless compatible.
- Caddy TLS works only when DNS and ports 80/443 are correct. Use a production-valid domain; do not claim TLS live from static syntax checks.
- Current external AI model configuration is **off in this production Compose**. Enable only after provider authorization, quota enforcement, secret management and privacy review.

## Unimplemented
No cloud provider account, DNS update, OAuth gateway, managed Postgres, email verification, signup/invitations, mobile compilation, CI-to-production deploy, remote sandbox or production uptime monitoring is provisioned here. Hosting cost varies by provider.
