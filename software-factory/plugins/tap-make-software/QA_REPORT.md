# QA report — v1.0.0 / 2026-10-11

## Verificações executadas

| Caso | Evidência | Resultado |
|---|---|---|
| Schema JSON do plugin e limite 30 caracteres | `python3` / `json.load`, `len(shortDescription)=27` | PASS |
| Skill metadata e arquivos referenciados | Verificação estrutural | PASS |
| Scaffolder seguro | `python3 -m unittest discover -s tests -v`: 5/5 | PASS |
| Sintaxe Python | `python3 -m py_compile tools/scaffold.py` | PASS |
| Artefatos gerados | Pastas, HTML, JS, CSS, manifest, SW | PASS |
| Sintaxe JavaScript | `node --check app.js sw.js` | PASS |
| JSON do webmanifest | `python3 -m json.tool` | PASS |
| Teste visual controlado com DOM | Chromium/Playwright `set_content`, scripts/style embutidos: criar tarefa, concluir, filtrar, armazenamento mock | PASS |
| Responsividade em viewport 390px | Verificação de scroll horizontal em Chromium/Playwright | PASS |
| Browser servido por URL local | Chromium bloqueou localhost e `file://` por política de administrador | NOT VERIFIED |
| Serviço Worker offline em URL real | Não possível nas condições de navegação | NOT VERIFIED |
| Build de app mobile ou deploy real | Fora do escopo desta versão | NOT IMPLEMENTED |
| Scanner oficial skillguard | CLI `skillguard` não está instalado neste runtime | NOT RUN |
| Auditoria estática manual | Revisão de instruções, scripts, caminhos de escrita, importações e secrets | PASS com limites |
| Plugin conectado e gatilho em nova conversa | Depende de criação/ativação posterior | NOT VERIFIED |

## Escopo de segurança

- Scaffolder não envia requisições de rede, instala dependências ou invoca shell.
- Nomes validados por allowlist estrita; evita path traversal e não sobrescreve diretórios existentes.
- O arquivo de exemplo usa `localStorage` e não coleta dados remotos; nunca usá-lo com PII sensível.
- A Skill instrui a não instalar hooks, desativar permissões, acessar secrets ou publicar sem autorização.
- **Nenhum scanner ou teste é uma certificação de segurança.**

## Limites de teste

A validação DOM controlada não equivale ao teste E2E do site hospedado. Autenticação, banco compartilhado, deploy cloud e app mobile não foram implementados nesta v1.0.0 e não foram validados.

## Expansão v2.0.0 — verificações de 2026-10-11
- 5 Skills especializadas incluídas **fisicamente** no plugin principal.
- 5 pacotes satélites skills-first registrados como privados em conta, com instruções byte-identical às Skills da suíte principal.
- Servidor MCP stdio somente no satélite `tap-code-workspace`, com leitura por padrão e escrita apenas por variável do host `TAP_ALLOW_WRITES=1`.
- Não existe servidor MCP remoto ou banco/cloud gerenciado implantado pelo pacote; integração de habilidades **não** concede acesso a contas externas.
- 23 testes unitários e protocolo stdio do servidor local **PASS**; 5 testes de scaffold original **PASS**.
- QA estrutural, preservação de defaultPrompts, frontmatter/manifestos, symlinks e regressões **PASS** (validação local).
- CLI `skillguard` indisponível; avaliação estática manual realizada sem certificar segurança. Riscos residuais de runtime local: host com permissões concedidas, corrida de filesystem em ambiente multiusuário e execução de código fora de sandbox não suportada.
- Testes E2E em ChatGPT iOS/web, implantação cloud, banco autenticado, Play Store e App Store: **NOT VERIFIED / NOT IMPLEMENTED**, dependem do ambiente.
