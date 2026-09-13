# LangChain Python

Uses LangChain's current `MCPAdapter` with FastMCP authentication. MCP server results marked `isError` are delivered to the model as error `ToolMessage` values; connection and session failures raise to `app.py`, which logs the exception type/message and exits nonzero.

## Run

```bash
cd langchain-python
python3 -m venv .venv
. .venv/bin/activate
pip install -e .
export OPENAI_API_KEY=...
export GITHUB_MCP_TOKEN=...
python app.py
```

For interactive OAuth discovery instead of a supplied token:

```bash
export MCP_AUTH_MODE=oauth
unset GITHUB_MCP_TOKEN
python app.py
```

## Force a transport error

```bash
MCP_SERVER_URL=https://127.0.0.1:1/mcp/ python app.py
```

The local `code_interpreter` tool validates JSON metadata, performs the deterministic scoring formula with pandas, and writes `artifacts/repository-ranking.png`. It is intentionally narrower and safer than an unrestricted Python REPL.

`MCP_TIMEOUT_SECONDS` (default `30`) limits only MCP connection and tool discovery. `AGENT_RUN_TIMEOUT_SECONDS` (default `180`) independently limits model reasoning, MCP tool calls, scoring, and chart generation. Timeout failures include a `stage` of either `mcp.discovery` or `agent.run`, so slow healthy agent work is not mislabeled as MCP discovery failure.

Official docs: [LangChain MCP](https://docs.langchain.com/oss/python/langchain/mcp), [authentication](https://docs.langchain.com/oss/python/langchain/mcp/auth), and [tool errors](https://docs.langchain.com/oss/python/langchain/mcp/tools#errors).
