# LangChain Python

Uses LangChain's current `MCPAdapter` with FastMCP authentication. MCP server results marked `isError` are delivered to the model as error `ToolMessage` values; connection and session failures raise to `app.py`, which logs the exception type/message and exits nonzero.

## Run

```bash
cd langchain-python
python3 -m venv .venv
. .venv/bin/activate
pip install -e .
cp .env.example .env
# Edit .env with AZURE_OPENAI_ENDPOINT and AZURE_OPENAI_DEPLOYMENT_NAME.
az login
export GITHUB_MCP_TOKEN=...
python app.py
```

The app loads `langchain-python/.env` before reading configuration, without overriding variables already exported by the host. It constructs `AzureChatOpenAI` with `DefaultAzureCredential`: deployed Azure environments use managed identity, while local development can use the signed-in Azure CLI identity from `az login`. Set `AZURE_CLIENT_ID` for a user-assigned managed identity. `AZURE_OPENAI_API_VERSION` defaults to `2024-10-21`.

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

Official docs: [LangChain AzureChatOpenAI](https://docs.langchain.com/oss/python/integrations/chat/azure_chat_openai), [LangChain MCP](https://docs.langchain.com/oss/python/langchain/mcp), [authentication](https://docs.langchain.com/oss/python/langchain/mcp/auth), and [tool errors](https://docs.langchain.com/oss/python/langchain/mcp/tools#errors).
