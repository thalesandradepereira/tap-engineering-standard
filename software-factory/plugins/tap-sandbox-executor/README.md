# TAP Sandbox Executor

MCP **local e opt-in**. Não é um serviço cloud, não conecta automaticamente ao ChatGPT iOS/web. Requer Python 3.11+, Docker instalado e configurado pelo dono do dispositivo, imagem local já presente.

Configuração de host, fornecida manualmente pelo usuário (não incluída com valores privados):

- `TAP_SANDBOX_PROJECT_ROOT=/absolute/path/to/an/approved/python/project`
- `TAP_SANDBOX_IMAGE=python@sha256:<digest-revisado>` (imagem com Python e unittest, no daemon local)
- `TAP_SANDBOX_ALLOW_RUN=1`

Execute apenas `tap_run_python_unittests`. Docker não é uma garantia contra ataques ao host: não usar para código comprovadamente hostil, multiusuário nem em máquinas com segredos sensíveis sem revisão da postura de segurança.
