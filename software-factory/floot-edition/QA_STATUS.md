# Floot Edition v0.1.0 — QA evidence / Evidências de QA

**As of / Verificado em:** 2026-10-11

| Test | Result |
| --- | --- |
| Floot plugin connection and project creation | PASS |
| Floot-managed PostgreSQL and Auth provisioning | PASS |
| Database table and index migration | PASS |
| Floot TypeScript typecheck | PASS (clean) |
| Jasmine default suite: themeMode + studioTemplates | PASS (2 spec files, 0 failures) |
| Ten Studio template/schema assertions | PASS |
| Public production GET / and /login | PASS (both HTTP 200) |
| Unauthenticated production GET /_api/studio/projects | PASS (HTTP 401) |
| Unauthenticated production POST /_api/studio/create | PASS (HTTP 401) |
| Unauthenticated production POST /_api/studio/save | PASS (HTTP 401) |
| Unauthenticated production POST /_api/studio/delete | PASS (HTTP 401) |
| Floot get_publish_status | PASS (published:true, public web URL) |
| Checkpoint and source snapshot | PASS |
| Owner-sign-in happy path / real authenticated CRUD | **NOT VERIFIED** |
| Browser screenshot / E2E after login | **NOT VERIFIED** (preview not open) |
| Automatic GitHub-to-Floot deploy | **NOT IMPLEMENTED** |
| Graphify private repo OAuth/indexing | **NOT VERIFIED** |
| Production penetration test, SLA, rate-limit abuse under load | **NOT VERIFIED** |

This is **not** evidence that production logins, account recovery emails, or authenticated projects have been end-to-end tested. Real user sign-in must be verified separately.

Keep the previously released Python/FastAPI and Graphify source untouched. No credentials or preview access tokens were committed.

**Made by TAP.**
