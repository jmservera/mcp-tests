# Microsoft Agent Framework .NET

Uses Microsoft Agent Framework with the official MCP C# SDK. MCP discovery and connection failures remain .NET exceptions; tool-level MCP errors remain tool results available to the agent. The Foundry agent also receives a hosted Code Interpreter tool created with `FoundryAITool`.

## Run

```bash
cd maf-dotnet
export AZURE_AI_PROJECT_ENDPOINT=https://your-project.services.ai.azure.com/api/projects/your-project
export AZURE_AI_MODEL_DEPLOYMENT_NAME=gpt-4.1-mini
export GITHUB_MCP_TOKEN=...
dotnet run
```

`DefaultAzureCredential` is used for the Foundry project. Authenticate with `az login` for local development.

## Force a transport error

```bash
MCP_SERVER_URL=https://127.0.0.1:1/mcp/ dotnet run
```

The console writes `mcp.connect`, `mcp.tools`, or `harness.failure` records without logging the token.

Official docs: [MAF MCP tools](https://learn.microsoft.com/en-us/agent-framework/agents/tools/local-mcp-tools) and [Code Interpreter](https://learn.microsoft.com/en-us/agent-framework/agents/tools/code-interpreter).
