# TAP Software Factory Studio — Floot Edition v0.2.1

[**Open hosted web Studio**](https://tap-software-factory.floot.app) · [Português](README.pt-BR.md) · [Core GitHub release](https://github.com/thalesandradepereira/tap-engineering-standard/releases/tag/software-factory-v4.1.0) · [QA](QA_STATUS.md)

This is an **independent Floot-native web implementation**, built primarily for a MacBook and accessible occasionally on mobile browsers. It does **not** run or automatically import the original TAP Studio Python/FastAPI server.

## Delivered and verified

- Floot production publish confirmed active at `https://tap-software-factory.floot.app` on 2026-10-11.
- Two web entry points responded HTTP 200 in production: `/` and `/login`.
- Floot-managed PostgreSQL and seeded email/password authentication, password-reset flow, session cookies and per-user project ownership.
- Authenticated endpoints for project list, create, save and delete. Four unauthenticated smoke tests returned **401** on the public domain.
- HTML, CSS and JavaScript editor, iframe sandbox preview with restricted CSP, and standalone downloadable HTML export.
- Floot TypeScript typecheck **clean**; both selected Jasmine spec files passed, including ten dedicated Studio template/schema cases.
- Floot checkpoint created before publication; web-only release, **no signed mobile build**.

## Files in this GitHub snapshot

The `snapshot/` folder contains **28 author-created or edited code/design files** captured from the live Floot project. See [manifest](snapshot-manifest.json) for the exact list and Floot project identifier. The Floot platform injects its own React components, session/auth helpers, database client, secrets and project configuration when resources are provisioned; those vendor-managed files **are not mirrored**. This GitHub directory is **a traceability snapshot, not an independently executable or complete Floot export**.

### Data contract

The [SQL schema](schema.sql) documents the `studio_projects` table and per-owner index. Deploying that schema in the GitHub repo does **not** provision a PostgreSQL database. The actual managed database is attached to the user's Floot project. Do not store database URLs, session cookies, passwords or provider API keys in GitHub.

## Access

The app requires its own login. The owner's Floot app account was provisioned with **no password**; the owner can open the published `/login` page, click **Forgot password?**, receive a one-time code via their registered email and choose a password. No password or recovery code was generated or disclosed in this release.

## Integration boundaries

| Capability | Status |
| --- | --- |
| Floot hosted web deploy | **LIVE** |
| Floot PostgreSQL + auth | **PROVISIONED**, authenticated real-user UX still pending |
| Backend per-user access checks | Authenticated owner ID enforced in all four endpoints |
| GitHub code release | Source snapshot and release notes; **not auto-synced to Floot** |
| Original Python/FastAPI runtime | Separate in `../plugins/tap-studio-runtime` |
| Graphify MCP | Plugin remains in core; Graphify OAuth/indexing not verified |
| LLM feature generation | **Live UI/endpoint available; real paid generation NOT run in QA** |
| Browser visual E2E | Pending user-open preview and authenticated session |
| 24/7 uptime/SLA | Floot service hosting, **no independent SLA guarantee** |

For next changes, edit the Floot app using authorized Floot tools, run Floot typecheck/tests, publish, then create a **new reviewed GitHub snapshot**. A GitHub commit alone does not redeploy Floot.

**Made by TAP.**

## AI Builder beta — v0.2.1

The web Studio now includes a **"Crie por descrição"** prompt panel. It uses Floot's integrated **GPT-6 Luna** service; calls debit the owner's Floot credits and therefore require **an explicit checkbox and confirmation on every Generate action**. A maximum of **3 attempts per authorized user per UTC day** is enforced in the server database with an atomic lock. AI generation is restricted by a separate whitelist: anonymous visitors and newly registered accounts cannot spend credits.

Generated HTML, CSS and JavaScript are **validated** and shown in a sandboxed preview. They do **not** replace existing project files until the user chooses **Apply**, and are **not persisted until Save**. The current source files/database are not sent to the model, only the user's description and project title. Invalid/truncated responses may still cost Floot credits and a daily attempt. No live billed model call was performed during engineering QA.

**Security:** Public registration has been disabled server-side (HTTP 403) for this private beta. Existing registered accounts continue to work. A production unauthorized AI request returned HTTP 401; page routes returned 200; TypeScript checked clean and four Jasmine suites passed. No browser-authenticated model E2E, independent penetration test or automated GitHub→Floot deployment has been verified.

[QA record](QA_STATUS.md) · [Reference SQL](schema.sql) · [28-file source snapshot](snapshot-manifest.json)

## Hotfix v0.2.1 — AI JSON response recovery (12 October 2026)

The Floot web application was redeployed with strict JSON schema output requested from GPT-6 Luna, more reliable extraction of complete JSON, explicit incomplete-response handling, and failure credit disclosure. Model output budget increased to 6,000 tokens, which can raise credit usage. Four Jasmine spec suites and TypeScript checks passed, and production HTTP smoke checks succeeded. The original project was preserved. **No new billed model generation was run in the hotfix QA**, so a successful end-to-end AI result still requires one in-app authorized attempt. The previous failed attempt cost **2 Floot credits**. See [incident report](PATCH_JSON_PENDING.md).
