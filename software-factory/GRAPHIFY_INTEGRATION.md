# Graphify integration and provenance

Official source: https://github.com/Graphify-Labs/graphify (license information upstream: Apache 2.0 and MIT/NOTICE; TAP does not redistribute upstream binaries).
Official hosted MCP setup: https://github.com/Graphify-Labs/graphify-mcp

The TAP Graphify plugin uses `https://api.graphify.com/mcp` (documented, Streamable HTTP) and a custom skill with user authorization gates. `mcp.json` is a connection declaration, not a logged-in session. The hosted implementation is proprietary to Graphify and is **not** included. The local open-source implementation requires separately approved installation of official `graphifyy`, optionally CLI mode.

Do not run `graphify hook install`, `graphify install --strict`, or any download/installer without approval. Treat produced graph as an indexed snapshot, and cross-check relevant edges against current code and tests.
