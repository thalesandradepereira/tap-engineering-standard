# TAP Studio Floot Edition v0.2.1 — QA / Garantia de qualidade

**Release:** 2026-10-12 · **Website:** https://tap-software-factory.floot.app

| Gate / Teste | Result / Resultado |
|---|---|
| Production website and login | **PASS** HTTP 200 |
| AI endpoint without user session | **PASS** HTTP 401 |
| Public registration endpoint | **PASS** HTTP 403 (disabled) |
| Floot TypeScript validation | **PASS** (clean) |
| Floot Jasmine specs | **PASS** — 4 spec files |
| Generation payload/validation rules | **PASS** unit tests, model mocked |
| AI access entitlements | **PASS** — one account enabled |
| Existing TAP Teste 001 persisted | **PASS**, current source preserved |
| New model calls billed during hotfix QA | **0** (no paid generation) |
| Native builds | **0** |
| True GPT-6 Luna model/credit E2E | **NOT RUN** (requires explicit consent and billing) |
| Authenticated browser interaction E2E | **NOT RUN** |
| Third-party pentest and output adversarial review | **NOT RUN** |
| Graphify OAuth and GitHub → Floot auto-sync | **NOT CONFIGURED** |

**Limitations:** This source is an audit-only snapshot of 28 authored files. Floot's proprietary generated auth helpers, production environment and live PostgreSQL data are not exported. A GitHub tag does not publish Floot automatically. A green TypeScript/Jasmine suite does not verify generated pages from real model traffic.

**Made by TAP.**

## Hotfix 12/10/2026 — v0.2.1

**Floot production deploy completed**, 4 Jasmine suites passed and TypeScript clean. Production HTTP smoke confirmed 200 (site/login), 401 (anonymous AI), 403 (public signup). The original project remains intact; **0 new billed generations during QA**. The initial failed request had already consumed 2 Floot credits on 11/10. The exact model response causing the earlier failure was not logged, and a successful real paid generation is **not yet certified**. See [incident and hotfix record](PATCH_JSON_PENDING.md).
