# TAP Software Factory — QA / Garantia de Qualidade

**As-of / Referência:** 2026-10-11; TAP Make Software v4.1.0; TAP Studio Runtime v0.2.0.

| Scope / Escopo | Tests / Testes | Evidence / Evidência |
| --- | ---: | --- |
| TAP Engineering Standard | 119 | Protected GitHub Actions, PR #10 |
| Workspace MCP | 23 | Protected GitHub Actions |
| Docker sandbox profile | 8 | Mocked runtime; tests passed |
| PWA scaffold | 5 | Protected GitHub Actions |
| TAP Studio Runtime | 19 | FastAPI TestClient, protected CI |
| **Total** | **174** | Last verified completed CI |

The additional bilingual documentation gate (README links, locale switch, ten plugin versions, security caveats and Mermaid diagrams) runs via `python3 software-factory/scripts/validate_readmes.py` on pull requests and main updates.

O novo QA documental verifica referências internas, correspondência EN/PT-BR, inventário com dez plugins, avisos obrigatórios e diagramas. Seus resultados devem ser confirmados no workflow da versão.

## Excluded / Não verificado

Real Docker container start; Linux production service; DNS and TLS on public domain; OAuth 2.1; Graphify repository indexing; real paid AI provider requests; remote sandbox execution; browser E2E on public host; signed app store builds; formal LGPD audit; offsite disaster restore.

## Governance / Governança

A green CI workflow is not equivalent to a real deployment. No secret should be committed, no release should be published against failed checks, and no GitHub branch protection should be bypassed.

Um CI verde não comprova serviço hospedado. Nenhum segredo deve ser adicionado ao repositório, nem release publicado com QA reprovado.

[Readme English](README.md) · [Leia-me em português](README.pt-BR.md) · [Release notes](RELEASE_NOTES_v4.1.0.md).
