# TAP Floot AI Builder — Incidente JSON e hotfix v0.2.1

**Estado: hotfix PUBLICADO no Floot em 12/10/2026; teste de geração paga ainda pendente.**

## Ocorrência original

Em 11/10/2026 às 19:40:36 UTC, a primeira geração real de IA retornou mensagem de JSON inválido e consumiu **2,0000 créditos Floot**. O registro no banco ficou em estado \`failed\`. A resposta bruta do modelo não estava disponível; os logs confirmam uma requisição com aproximadamente 23 segundos de duração, mas não revelam a forma exata da resposta. Não afirmar uma causa raiz específica.

## Correção publicada

O backend passou a solicitar **JSON Schema estrito**, com \`html\`, \`css\` e \`javascript\`. O parser reconhece JSON completo mesmo com texto de apresentação ou blocos Markdown; detecta respostas \`incomplete\` e **nunca conserta artificialmente JSON truncado**. O limite máximo de saída subiu de **3.200 para 6.000 tokens**, podendo aumentar o consumo de créditos de uma geração longa. Falhas agora informam créditos contabilizados quando conhecidos.

O código preserva login obrigatório, lista de contas habilitadas, três solicitações/dia UTC, confirmação de cobrança a cada geração e as etapas separadas **Prévia → Aplicar → Salvar**. Nenhuma chamada paga é repetida automaticamente.

## Evidência de QA

- Quatro suítes Jasmine aprovadas, inclusive testes adicionais de conteúdo com prefixo, chaves em strings, resposta incompleta e diferentes formatos de saída.
- TypeScript limpo e checkpoint Floot \`bb2c19e7-b696-4a0e-82bc-8537e944c12b\`.
- Floot confirmou o deploy no domínio \`https://tap-software-factory.floot.app\`.
- Pós-deploy: \`/\` e \`/login\` responderam 200, solicitação de IA anônima 401 e cadastro público 403.
- Consulta posterior: o projeto \`TAP Teste 001\` continua intacto, **zero solicitações ao modelo no dia 12/10 durante o QA**, permanecendo os 2 créditos históricos do incidente.
- **A qualidade de uma geração real concluída e a cobrança correspondente ainda não foram verificadas.** Para esse teste, cada chamada deverá ser aprovada explicitamente no painel do usuário.

## Limitações

O código do Floot e o snapshot no GitHub não possuem sincronização automática; o snapshot não exporta os serviços internos do Floot. QA verde não equivale a certificação de segurança completa nem comprova que todo prompt produzirá JSON utilizável.

**Made by TAP**
