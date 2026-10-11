# Graphify — origem, licenças e limites

- Repositório canônico: https://github.com/Graphify-Labs/graphify
- Documentação de MCP hospedado: https://github.com/Graphify-Labs/graphify-mcp
- MCP Streamable HTTP oficial: `https://api.graphify.com/mcp`, requer OAuth compatível e seleção/indexação de repositório.
- Pacote CLI upstream: `graphifyy` (não confundir com pacotes homônimos); CLI `graphify`.
- Licenças upstream consultadas: Apache-2.0 e MIT com avisos/NOTICE próprios. O TAP não redistribui o motor nem afirma patrocínio oficial.
- Original: arquivos gerados podem incluir `graphify-out/graph.html`, `graphify-out/GRAPH_REPORT.md`, `graphify-out/graph.json`.
- Para usar CLI local já aprovado: confirmar disponibilidade, executar `graphify .` em workspace autorizado; em modo consulta `graphify query "qual o fluxo de autenticação?"`. Somente após consentimento instalar: `uv tool install graphifyy` (exemplo, NÃO executado pela Skill).
- Não ativar `graphify hook install`, `graphify install --strict`, scripts de instalação em shell, reindexação contínua ou serviços públicos por padrão.
- Segurança: parsing AST é local; modo semântico e MCP hospedado podem expor código e conteúdo ao fornecedor. Requer autorização explícita e minimização de dados.
- Resultados do MCP dependem da autenticação, permissões e indexação. Saída do grafo pode estar desatualizada.
