# TAP Studio Floot Edition v0.2.0 — QA / Garantia de qualidade

**Release:** 2026-10-11 · **Website:** https://tap-software-factory.floot.app

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
| AI calls billed during QA | **0** (no real model request) |
| Native builds | **0** |
| True GPT-6 Luna model/credit E2E | **NOT RUN** (requires explicit consent and billing) |
| Authenticated browser interaction E2E | **NOT RUN** |
| Third-party pentest and output adversarial review | **NOT RUN** |
| Graphify OAuth and GitHub → Floot auto-sync | **NOT CONFIGURED** |

**Limitations:** This source is an audit-only snapshot of 28 authored files. Floot's proprietary generated auth helpers, production environment and live PostgreSQL data are not exported. A GitHub tag does not publish Floot automatically. A green TypeScript/Jasmine suite does not verify generated pages from real model traffic.

**Made by TAP.**

## Incidente real de IA — 11/10/2026

Uma tentativa de geração retornou erro de JSON inválido e consumiu **2.0000 créditos Floot** (status `failed` na tabela `studio_ai_requests`). A resposta original do modelo não foi retida: causa exata ainda não comprovada. A correção está em um PR draft, **não publicada**, pois o Floot atingiu o limite diário de build (reinício 12/10/2026 14:00 UTC). Consulte [plano de correção](PATCH_JSON_PENDING.md).
