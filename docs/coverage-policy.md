# Coverage Policy / Política de Cobertura

## English

The repository prioritizes adversarial regression tests and dependency-free validation over a headline coverage percentage. The current CI deliberately does not install `coverage.py` or another third-party coverage package because doing so would add a networked supply-chain dependency to a repository whose validator and tests otherwise use only the Python standard library.

A future branch-coverage or mutation-testing tool may be adopted when its benefit justifies that new trust boundary. Any such change should be introduced in a dedicated pull request with a pinned version, provenance review, dependency inspection, and an explicit update to the security model.

Coverage metrics are evidence of exercised code, not proof of correctness. Security-sensitive parser behavior should continue to be backed by focused positive and negative regression cases even if a coverage tool is added later.

## Português do Brasil

O repositório prioriza testes adversariais de regressão e validação sem dependências externas em vez de um percentual de cobertura isolado. O CI atual não instala deliberadamente `coverage.py` nem outro pacote de cobertura de terceiros, pois isso adicionaria uma dependência de supply chain com acesso à rede a um repositório cujo validador e testes usam somente a biblioteca padrão do Python.

Uma futura ferramenta de cobertura de branches ou mutation testing poderá ser adotada quando o benefício justificar esse novo limite de confiança. Qualquer mudança desse tipo deve ser feita em um pull request dedicado, com versão fixada, revisão de proveniência, inspeção de dependências e atualização explícita do modelo de segurança.

Métricas de cobertura demonstram código exercitado, não comprovam correção. Comportamentos sensíveis de parsing devem continuar protegidos por casos positivos e negativos de regressão mesmo que uma ferramenta de cobertura seja adicionada no futuro.
