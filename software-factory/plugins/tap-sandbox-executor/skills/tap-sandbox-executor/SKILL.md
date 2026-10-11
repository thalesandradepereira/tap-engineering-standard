---
name: tap-sandbox-executor
description: Use quando testes Python em repositório autorizado precisarem rodar isolados de processos locais e houver runtime Docker já disponível, imagem local revisada e permissão explícita de execução.
---
# TAP Sandbox Executor

Executor de testes Python em Docker local restrito, **não** hospedagem cloud e **não** sandbox comprovadamente inviolável. Leia README e `server/sandbox_mcp.py` antes de ativar. Utilize somente sob autorização do dono do workspace.

- O MCP inicia desabilitado para execuções. Requer `TAP_SANDBOX_PROJECT_ROOT` absoluto, `TAP_SANDBOX_IMAGE` como referência imutável `@sha256:` revisada e `TAP_SANDBOX_ALLOW_RUN=1`.
- Não instala Docker, puxa imagens, ativa daemon, monta segredos, executa shell nem altera permissões. Usa `docker --pull=never` com rede desativada, imagem restrita, montagens read-only, recursos limitados e nenhum privilégio novo.
- Tem apenas `tap_sandbox_status` e `tap_run_python_unittests`. Testes são código do projeto e devem ser considerados não confiáveis, embora isolados. Docker daemon local também precisa ser confiável.
- Se não houver runtime ou autorização, gere instruções e testes estáticos; informe que não executou.
- Logs de testes podem vazar dados: redija segredos, evite arquivos privados e não exponha saídas sem inspeção.
- Execute outros testes/linguagens com executor homologado apropriado, nunca contorne a allowlist.
