# Microsoft Agent Framework .NET

Uses Microsoft Agent Framework with Azure OpenAI's Responses API and the official MCP C# SDK. MCP discovery and connection failures remain .NET exceptions; tool-level MCP errors remain tool results available to the agent. The Azure OpenAI agent also receives a hosted Code Interpreter tool.

`ResponsesClient` is configured directly with Azure's `BearerTokenPolicy`. `FoundryAITool.CreateCodeInterpreterTool` is retained only as the MAF adapter for the OpenAI Responses hosted tool.

The project uses the current MAF, MCP, and `Microsoft.Extensions.AI` package family together. It avoids the `Azure.AI.OpenAI` wrapper because its current preview pins an older `OpenAI` runtime that is binary-incompatible with current MAF and MCP packages.

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

`AZURE_OPENAI_ENDPOINT` can be the resource root or Responses endpoint. The app normalizes these forms to the required `/openai/v1` base:

* `https://jmfoundry.openai.azure.com/`
* `https://jmfoundry.openai.azure.com/openai/v1`
* `https://jmfoundry.services.ai.azure.com/openai/v1/responses`

`AZURE_OPENAI_DEPLOYMENT_NAME` must be the deployment name shown in the Azure portal, which is not necessarily the underlying model name.

## Force a transport error

```bash
MCP_SERVER_URL=https://127.0.0.1:1/mcp/ dotnet run
```

The console writes `mcp.connect`, `mcp.tools`, or `harness.failure` records without logging the token.

Official docs: [MAF Azure OpenAI provider](https://learn.microsoft.com/en-us/agent-framework/integrations/by-component/model-providers/azure-openai), [MAF MCP tools](https://learn.microsoft.com/en-us/agent-framework/agents/tools/local-mcp-tools), and [Code Interpreter](https://learn.microsoft.com/en-us/agent-framework/agents/tools/code-interpreter).
