# QA Gate — evidências por camada

**Gate A — contrato:** requisitos, riscos, critérios de aceite, estados esperados, migração de dados e permissões aprovadas.

**Gate B — código:** lint/typecheck e testes unitários; interfaces e payloads com contrato claro; erros tratados; sem secrets, credenciais ou tokens nos arquivos.

**Gate C — integração:** APIs reais ou mocks explicitados; HTTP status apropriado; auth/roles negative tests; DB constraints; paginação; serialização; timeouts/retries; logging; CORS/CSRF; arquivos/uploads se existirem.

**Gate D — produto:** responsividade mobile, teclado, acessibilidade básica (labels, contraste, foco), navegação/CRUD/estados vazio e de erro; cross-filter e reconciliação para dashboards.

**Gate E — segurança:** ver `security-and-privacy.md`; dependências, vulnerabilidades conhecidas, injeções, autorização BOLA/IDOR, secrets em logs, proteção de PII, rotas públicas e headers apropriados.

**Gate F — release:** testes verdes em ambiente adequado, deploy confirmado, health check e smoke de produção quando possível, migração e rollback, README/changelog, URL e release link reais. Não classificar `queued` ou `published` como testado em produção.

## QA matriz final

| Requisito | Evidência verificável | Estado |
|---|---|---|
| App inicia | Comando real, exit code e porta | Pass / Fail / Not tested |
| Fluxo principal funciona | Teste/E2E observado | Pass / Fail / Not tested |
| Login e autorização | Testes positivos e negativos | Pass / Fail / Not tested / N/A |
| Persistência | Teste de leitura após reinício | Pass / Fail / Not tested / N/A |
| Build | Build com comando e saída | Pass / Fail / Not tested |
| Segurança | Inspeção/testes por fronteira | Pass / Fail / Not tested |
| Publicação | URL + response/health confirmados | Pass / Fail / Not tested |

Priorizar testes automatizados não elimina revisão humana das funções de negócio e regras regulatórias. Testes do scaffold não demonstram segurança de apps gerados posteriormente.
