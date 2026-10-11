# TAP Studio Runtime V4 — validation and deployment status

- Version: TAP Make Software 4.0.0; TAP Studio Runtime 0.1.0.
- Implemented: REST API, SQLite persistent projects, owner isolation, PBKDF2 password login, expiring bearer sessions, project file editor, ZIP export, sandbox preview, HTTP JSON-RPC MCP subset.
- Generating via external LLM is disabled by default; explicit opt-in, approved HTTPS endpoint, server secret and provider quotas required. External user consent precedes transmission. No automated deployment.
- QA: 15 new tests passed locally including simulated model service, 36 previous regression tests; CI adds Python venv and tests, total 51 when CI passes.
- Browser QA: Chromium outbound navigation blocked by administrator in test runtime; **not E2E-verified**. JS syntax validated.
- Security limitations: do NOT publicly expose without TLS, reverse proxy, OAuth 2.1 gateway, durable backup, external rate limits, monitoring and review. Existing HTTP bearer prototype is NOT an OAuth-compliant remote ChatGPT plugin. Docker build/host was NOT run locally.
- Graphify integration unchanged, pending account OAuth/indexing. Local Mac remote device currently offline.
- Official Emergent parity NOT established: cloud sandbox orchestration, public previews, App Store publishing, managed DB, enterprise auth, online hosted MCP and automatic deploy remain.
