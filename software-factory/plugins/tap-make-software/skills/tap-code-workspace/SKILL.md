---
name: tap-code-workspace
description: Use quando for necessário inspecionar arquivos, editar código ou validar sintaxe em workspace autorizado via um servidor MCP local; não use para pedir execução cloud inexistente.
---

# TAP Code Workspace — Local MCP

## Objetivo e limites
Fornecer um **servidor MCP stdio real** (Python stdlib) para listar, ler e escrever arquivos de projeto e validar sintaxe Python/JSON. Não oferece execução arbitrária, sandbox de código, rede, CI, autenticação cloud ou backend hospedado. No ChatGPT web/iOS o processo local não é iniciado automaticamente.

## Acesso e ativação
1. Verifique se o ambiente é host desktop com suporte real a servidores MCP `stdio`, Python 3.11+ disponível e filesystem autorizado.
2. Configure `TAP_WORKSPACE_ROOT` com **caminho absoluto existente**, de escopo mínimo; servidor não aceita raiz `/` nem home do usuário como root.
3. **Leitura:** sem escrita por padrão. Para edição, usuário/administrador ativa expressamente `TAP_ALLOW_WRITES=1` no processo local. Nunca alterar essa flag sem permissão do proprietário.
4. Inspecione `mcp.json`, `server/tap_workspace_mcp.py` e riscos antes de conectar. Execute em workspace sem segredos. Não escale permissões nem bypass.
5. Se não houver host MCP: use arquivos nativos, ambiente Python e GitHub conectado, indicando claramente a capacidade efetiva.

## Ferramentas implementadas
- `tap_workspace_status`: estado, raiz e modo de escrita (não entrega valores de secrets).
- `tap_list_files`: listagem recursiva, bounded, omitindo diretórios ocultos.
- `tap_read_text`: texto em UTF-8 de extensão permitida, limite de bytes e contenção de caminho.
- `tap_write_text`: criação/atualização explícita de texto com modo de escrita ativado, limite de tamanho, sobrescrita deliberada.
- `tap_check_syntax`: compilação AST de Python e parser JSON, sem executar código do projeto.

## QA obrigatório
Testes de travessia de diretório, path absoluto, symlink, arquivos ocultos, dados maiores que limite, escrita desativada, read/write permitido, sintaxe inválida, RPC tools/list e errors. Padrão TAP Engineering Standard, teste negativo primeiro, evidências da execução e relatório de limitações.

## Integração
O `tap-make-software` já inclui esta mesma Skill e pode roteá-la por nome. A versão standalone é opcional. Não confunda integração **de instruções** com conexão efetiva do processo MCP; verifique descoberta de ferramentas em cada sessão.
