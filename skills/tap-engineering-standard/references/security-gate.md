# Security and Supply-Chain Gate

Use this reference when a task introduces or evaluates an external repository, package, Agent Skill, plugin, connector, MCP server, installer, hook, account integration, credential, or networked service. Read only the sections needed for the current decision.

## 1. Establish provenance

1. Identify the canonical repository owner, project name, website, package name, and publisher.
2. Distinguish the original project from forks, mirrors, typo-squats, copied instructions, generated listings, and unofficial installers.
3. Compare repository, package-registry, release, and documentation identities when those sources are available.
4. Verify license terms for the exact component being adopted; different components can use different licenses.
5. Treat stars, download counts, social-media recommendations, and benchmark screenshots as signals rather than proof of safety.

## 2. Inspect the execution boundary

Read the actual installation and execution paths before recommending them:

- package manifests, lockfiles, lifecycle scripts, and transitive dependencies;
- shell installers, PowerShell installers, Dockerfiles, Compose files, and CI workflows;
- agent instructions, hooks, MCP tools, browser permissions, and connector scopes;
- binaries, generated files, native extensions, subprocess calls, and dynamic evaluation;
- startup behavior, persistence, auto-update paths, uninstall behavior, and filesystem access.

Prefer a reviewed versioned release, a pinned dependency, scoped execution, and a reversible installation. Avoid piping remote scripts directly into a shell or running installers that conceal their changes.

## 3. Build a data-flow map

Identify each relevant source, transformation, destination, and retention point:

| Data class | Questions to answer |
| --- | --- |
| Source code | Is proprietary code read, indexed, copied, uploaded, or retained? |
| Credentials | Are tokens, cookies, API keys, SSH keys, or password managers accessed? |
| Conversation history | Are agent transcripts, shell histories, local logs, or prior prompts collected? |
| Personal information | Are names, emails, identifiers, health, legal, financial, or location data exposed? |
| Telemetry | What is collected, when is consent requested, and how is collection disabled? |
| Network access | Which hosts are contacted, under what conditions, using which credentials? |
| Generated artifacts | Where are graphs, caches, reports, temporary files, and embeddings written? |

Never transmit sensitive source, user information, secrets, or private files without authorization that covers the destination and purpose.

## 4. Test permission and injection boundaries

Check whether the capability:

- auto-approves commands or weakens a host product's confirmation flow;
- rewrites commands through a hook before permission checks;
- executes untrusted text through a shell, template, evaluator, or subprocess;
- follows instructions embedded in code, issues, webpages, PDFs, logs, or generated output;
- grants write access when read-only access would satisfy the task;
- exposes tools that can send messages, publish content, transfer funds, alter accounts, or delete data;
- accepts unvalidated paths, URLs, redirects, archive entries, or file uploads;
- permits SSRF, path traversal, XSS, command injection, privilege escalation, or secret leakage.

Treat negative security tests as evidence only when they were actually executed in an authorized environment.

## 5. Assess maintenance and operational maturity

Inspect available release history, recent meaningful commits, issue response, test coverage, CI status, security policy, disclosed advisories, dependency updates, breaking changes, rollback guidance, and platform-specific integration defects.

Differentiate:

- a reported issue from a confirmed current vulnerability;
- a patched historical defect from an unresolved exposure;
- an issue affecting an optional integration from a defect in the core package;
- a benchmark of one narrow operation from a claim about total model cost or end-to-end latency.

Do not invent dates, stars, versions, findings, test results, or security classifications when evidence is missing.

## 6. Return a decision

Use one of these decisions:

- **Adopt**: the capability is useful, compatible, reviewable, maintained, and its material risks are controlled.
- **Pilot**: the capability may help, but evidence, platform maturity, permissions, operational cost, or integration stability requires a limited trial.
- **Reject for now**: unresolved high-impact risk, unsafe installation, unclear provenance, permission bypass, excessive exposure, or incompatibility outweighs the benefit.

State the decisive evidence, residual risk, minimum safe configuration, and a native or lower-risk alternative when one exists.
