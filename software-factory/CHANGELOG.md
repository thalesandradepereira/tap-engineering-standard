# TAP Software Factory — Changelog

Software Factory versions track the main orchestrator; individual plugins keep independent versions in [plugin-inventory.json](plugin-inventory.json). A GitHub commit, an official GitHub Release and deployment are separate events.

## 4.1.0 — 2026-10-11
- TAP Make Software v4.1.0 and TAP Studio Runtime v0.2.0.
- Self-hosted Docker Compose/Caddy HTTPS configuration, persistent SQLite, secret-file bootstrap, consistent backup utility.
- English and Portuguese premium READMEs, release notes and documentation QA gate.
- Prior protected CI verified 174 tests; no production host or domain was deployed.

## 4.0.0 — 2026-10-11
- Added TAP Studio Runtime FastAPI app, SQLite, authenticated projects, web editor, ZIP export and optional AI endpoint with explicit consent.
- Embedded Studio Skill in the core (11 Skills).

## 3.0.0 — 2026-10-11
- Added Graphify official hosted MCP adapter, Docker sandbox test profile and cloud infrastructure guidance.
- Consolidated plugins into the GitHub software-factory tree.

## 2.0.0 — 2026-10-11
- Added workspace, data/auth, mobile, deploy and security specialist workflows.

## 1.0.0 — 2026-10-11
- Initial orchestrator and static PWA scaffold.

[Release notes v4.1.0](RELEASE_NOTES_v4.1.0.md) · [QA](QA_STATUS.md).
