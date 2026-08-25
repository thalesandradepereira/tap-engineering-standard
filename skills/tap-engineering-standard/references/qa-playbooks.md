# Engineering QA Playbooks

Load only the playbook section that matches the current task. Every conclusion must distinguish verified behavior, inferred behavior, and behavior that could not be tested.

## Acceptance and verification matrix

Before substantive implementation, convert the request into observable checks:

| Requirement | Verification method | Evidence | Status |
| --- | --- | --- | --- |
| Stated user outcome | Direct inspection, executable check, or observed product behavior | Actual result | Pass / Fail / Not verified |
| Existing behavior | Focused regression test | Test name and output | Pass / Fail / Not verified |
| Security boundary | Configuration review or negative test | Observed denial or controlled behavior | Pass / Fail / Not verified |
| External side effect | Authoritative downstream status | Delivery, persistence, publication, or system response | Pass / Fail / Not verified |

Build success, accepted requests, queued jobs, mocked responses, and stale screenshots do not prove completed downstream behavior.

## Dashboards and analytics

Verify the complete path from source records to visible results:

1. Confirm schema, column types, encodings, dates, currency, null handling, duplicates, aggregation grain, and source row count.
2. Reconcile unfiltered KPI totals against independent source calculations.
3. Test each filter independently and in combination with every other filter.
4. Verify bidirectional cross-filter propagation between charts, cards, tables, drill-downs, search, and exports.
5. Confirm clear/reset behavior, empty states, no-result combinations, and persistence or intentional reset of drill-down state.
6. Validate hierarchical drill-down, breadcrumbs, labels, tooltips, units, sorting, and decimal precision.
7. Export a filtered selection and compare row count, totals, column order, formats, and file contents against the visible state.
8. Inspect keyboard access, focus visibility, contrast, screen-reader labels, narrow viewports, and meaningful error states.
9. Test representative large inputs without inventing performance metrics or claiming stress tests that were not run.

## Scheduled workflows and email automations

Trace the complete chain rather than stopping at a green workflow icon:

1. Identify trigger, default branch, cron expression, timezone, event permissions, concurrency, and skipped-run conditions.
2. Inspect required secrets by presence or configuration status only; never print their values.
3. Check token expiry, application-password scope, provider authentication, and API quota behavior.
4. Verify data collection, freshness thresholds, deduplication, language-specific content generation, formatting, and fallback behavior.
5. Test every declared locale independently. A delivered Portuguese email does not prove the English version was generated or sent.
6. Confirm recipient selection, SMTP/API response, provider acceptance, delivery evidence, retries, and duplicate-send prevention.
7. Distinguish workflow success, provider acceptance, inbox delivery, and spam-folder routing.
8. Verify structured logs expose decisive failures while redacting secrets, private data, and sensitive content.
9. Re-run only when authorized and report observable downstream results for every expected message.

## API and data integrations

Check authentication, authorization, request and response schemas, pagination, timestamps, retries, idempotency, rate limits, timeouts, circuit breaking, partial failure, stale caches, provider limits, and backward compatibility.

For writes, distinguish receipt, persistence, asynchronous completion, and downstream visibility. Verify rollback or compensating behavior when a multi-step change can leave inconsistent state.

## Agent Skills, plugins, and MCP

Verify:

- required `SKILL.md` frontmatter and descriptive activation boundaries;
- references that exist, are relevant, and are loaded only when necessary;
- exact skill name, host-specific metadata, icon integrity, and installation state;
- host compatibility and the difference between a public repository and an installed capability;
- available tools, requested permissions, read/write boundaries, and confirmation requirements;
- prompt-injection resistance, sensitive-data handling, failure modes, and cross-surface behavior;
- explicit invocation and, when observable, relevant implicit activation.

Do not claim that a Skill works on a platform unless the required support was verified or its compatibility is explicitly qualified.

## GitHub repositories and releases

Verify repository ownership, actual public/private visibility, default branch, license recognition, README rendering, bilingual links, canonical source files, relative links, workflow triggers, job permissions, action pinning, status checks, and the latest run conclusion.

Inspect a real workflow run rather than treating the presence of a YAML file as evidence that CI passed. Distinguish a queued run, an in-progress job, a skipped workflow, and a successful execution.

## Browser-visible interfaces

Observe rendered UI behavior after the change. Verify the requested interaction, loading states, navigation, validation errors, responsive layout, accessibility basics, and relevant console failures when those tools are available.

Screenshots illustrate state but do not replace functional interaction. A local build does not prove a hosted deployment updated successfully.

## Release decision

Summarize what was tested, what passed, what failed, what could not be verified, and whether the remaining uncertainty blocks delivery. Do not inflate confidence when access, fixtures, credentials, environment parity, or downstream confirmation is missing.
