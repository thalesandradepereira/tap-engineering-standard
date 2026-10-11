---
name: tap-graphify
description: Use quando precisar mapear uma base de código grande, rastrear chamadas, dependências, arquitetura, impacto de mudanças, testes relacionados ou consultar grafos Graphify existentes via MCP; não é necessário em mudanças pequenas e localizadas.
---
# TAP Graphify — adaptador seguro

**Proveniência:** integração independente do TAP Make Software com Graphify-Labs/graphify. NÃO é o motor oficial Graphify nem concede acesso automático a nenhum repositório. Consulte `references/origin-and-usage.md`.

1. Verifique se o MCP Graphify realmente aparece como conectado e autorizado. Se não estiver, considere apenas a análise estática nativa do repositório e reporte o limite; não afirme execução.
2. Se o usuário possuir código local autorizado, identifique se `graphify` (pacote oficial `graphifyy`) já está instalado e o grafo existente é recente. Não instale binários/CLI/hooks nem ative modo `--strict` automaticamente.
3. Grafo apenas quando útil: grandes projetos, impacto multi-arquivo, dependências; em correção localizada use busca direcionada primeiro.
4. Antes de consultar grafo, confira revisão/commit, `graph.json`, escopo e timestamp de atualização. Um grafo desatualizado não comprova chamadas atuais. Valide arestas de impacto contra código e testes reais; não trate conexões inferidas como extraídas.
5. O MCP oficial hospedado pode requerer OAuth e indexação dos repositórios escolhidos. Peça autorização apropriada ao conectar repositórios privados ou disponibilizar arquivos ao provedor. Nunca envie código ou segredos sem autorização para aquele destino.
6. Cite caminho/linha quando possível e informe o que foi efetivamente verificado. Análise estática não substitui QA runtime.
7. Para alterações na execução, siga `tap-engineering-standard` e `tap-qa-security` quando disponíveis.

Este plugin contém `mcp.json` apontando a um endpoint documentado do provedor; isso não equivale a login, autorização, indexação ou conexão em funcionamento.
