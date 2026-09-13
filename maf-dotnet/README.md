# Microsoft Agent Framework .NET

Uses Microsoft Agent Framework with Azure OpenAI's Responses API and the official MCP C# SDK. MCP discovery and connection failures remain .NET exceptions; tool-level MCP errors remain tool results available to the agent. The Azure OpenAI agent also receives a hosted Code Interpreter tool.

`FoundryAITool.CreateCodeInterpreterTool` is retained only as the MAF adapter for the OpenAI Responses hosted tool; model requests are created by `AzureOpenAIClient`, not `AIProjectClient`.

## Run

```bash
cd maf-dotnet
cp .env.example .env
# Edit .env with AZURE_OPENAI_ENDPOINT and AZURE_OPENAI_DEPLOYMENT_NAME.
az login
export GITHUB_MCP_TOKEN=...
dotnet run
```

The app loads `maf-dotnet/.env` before reading configuration, without replacing variables already present in the process environment. `DefaultAzureCredential` excludes secret-based environment credentials: deployed Azure environments use managed identity, while local development uses the signed-in developer identity from `az login`. Set `AZURE_CLIENT_ID` for a user-assigned managed identity and assign that identity access to the Azure OpenAI resource.

## Force a transport error

```bash
MCP_SERVER_URL=https://127.0.0.1:1/mcp/ dotnet run
```

The console writes `mcp.connect`, `mcp.tools`, or `harness.failure` records without logging the token.

Official docs: [MAF Azure OpenAI provider](https://learn.microsoft.com/en-us/agent-framework/integrations/by-component/model-providers/azure-openai), [MAF MCP tools](https://learn.microsoft.com/en-us/agent-framework/agents/tools/local-mcp-tools), and [Code Interpreter](https://learn.microsoft.com/en-us/agent-framework/agents/tools/code-interpreter).
