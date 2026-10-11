# Full-stack hosting — TAP Studio v0.2

The self-hosted deployment template was added under `plugins/tap-studio-runtime/deploy`.
It implements:
- Linux single-host Docker Compose with Caddy HTTPS, automatic TLS when authorized DNS and open ports are configured
- private FastAPI container (no public backend listener) and SQLite persistent volume
- administrator bootstrap password loaded from a Docker secret file readable by UID 10001
- read-only container root and dropped Linux capabilities for the application
- on-demand consistent SQLite/WAL snapshots saved in a dedicated backup volume
- configuration guidance for domain, secrets, host monitoring, offsite backup, rollback and no-auto-publish safety gates

## Current status

**Configuration saved, code tested locally; no hosted instance deployed.**
Required before launch: an authorized Linux server/VPS, hostname, DNS, actual Docker Engine and Compose, admin secret, firewall, cost acceptance, smoke test of the domain, an offsite backup schedule. Floot is NOT installed in this account as of this configuration and its connection requires explicit user action. OAuth 2.1 for ChatGPT remote MCP and cloud code execution are not part of this template.

To deploy on a host, follow [the production README](plugins/tap-studio-runtime/deploy/README.production.md). Never expose the backend port or paste secrets into ChatGPT or GitHub.
