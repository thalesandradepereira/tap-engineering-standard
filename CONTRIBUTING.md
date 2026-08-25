# Contributing / Como contribuir

## English

Thank you for improving TAP Engineering Standard. Keep contributions focused, reviewable, and compatible with the project's security model.

1. Read the complete skill, both READMEs, and the security policy.
2. Open an issue before proposing a broad behavioral or compatibility change.
3. Preserve the canonical skill name and keep required instructions in `SKILL.md`.
4. Do not add installers, hooks, telemetry, external dependencies, automatic approvals, or permission bypasses.
5. Update English and Brazilian Portuguese documentation together when user-facing behavior changes.
6. Run `python3 scripts/validate_skill.py` and `python3 -m unittest discover -s tests -v`.
7. Submit a pull request describing the change, rationale, verification, and security impact.

Use responsible disclosure for security issues. Do not include credentials, private source code, or personal data in public contributions.

## Português do Brasil

Obrigado por contribuir com o TAP Engineering Standard. Mantenha as alterações objetivas, auditáveis e compatíveis com o modelo de segurança.

1. Leia a Skill completa, os dois READMEs e a política de segurança.
2. Abra uma issue antes de propor alterações amplas de comportamento ou compatibilidade.
3. Preserve o nome canônico da Skill e mantenha as instruções necessárias em `SKILL.md`.
4. Não adicione instaladores, hooks, telemetria, dependências externas, aprovações automáticas ou mecanismos para contornar permissões.
5. Atualize simultaneamente a documentação em inglês e português quando houver mudança perceptível para o usuário.
6. Execute `python3 scripts/validate_skill.py` e `python3 -m unittest discover -s tests -v`.
7. Envie um pull request descrevendo a alteração, a justificativa, os testes executados e os impactos de segurança.

Utilize divulgação responsável para problemas de segurança. Não inclua credenciais, código privado ou dados pessoais em contribuições públicas.
