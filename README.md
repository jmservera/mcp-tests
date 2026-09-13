# GitHub MCP error harness comparison

Four minimal examples run the same repository-discovery instructions against the hosted GitHub Copilot MCP server:

| Harness | Example | Native error surface |
|---|---|---|
| LangChain Python | [`langchain-python/`](langchain-python/) | MCP `isError` becomes an error `ToolMessage`; transport/session failures raise |
| Microsoft Agent Framework .NET | [`maf-dotnet/`](maf-dotnet/) | MCP discovery and invocation failures surface as .NET exceptions or tool results |
| Bedrock AgentCore managed harness | [`bedrock-agentcore/`](bedrock-agentcore/) | Runtime failures arrive as `runtimeClientError` stream events |
| Microsoft Copilot Studio | [`copilot-studio/`](copilot-studio/) | Connection creation/test diagnostics and managed conversation/tool errors |

The shared system prompt is [`agent-instructions.md`](agent-instructions.md). The examples intentionally do not wrap all failures in a common exception type because the native behavior is what this repository compares.

## Structured-error test

The executable harnesses use a deliberately over-complex `search_repositories` query as their default prompt. The GitHub MCP server returns a structured, recoverable validation error, after which the agent is expected to follow the returned guidance, retry with smaller searches, and continue the task.

Do not use private or organization-scoped repositories for the comparison.

## Observed results

Results recorded on September 13, 2026:

| Harness | Test status | Observed structured-error behavior |
|---|---|---|
| LangChain Python | Verified | The MCP error is returned as an error tool message that remains visible to the agent; the agent can revise the query and continue. |
| Microsoft Agent Framework .NET | Verified | The structured MCP tool error remains in the agent interaction, allowing a subsequent corrected tool call. |
| Bedrock AgentCore | Verified | The harness preserves the structured MCP tool error for the agent, which can recover by changing its next tool call. |
| Microsoft Copilot Studio | Not yet tested | No behavior is claimed until the same scenario is run in Copilot Studio. |

These results verify the MCP structured tool-error path exercised by this repository; they are not a general conformance certification for every MCP feature or failure mode.

## Common failure scenarios

Run the same scenarios in each harness and record whether the model sees the failure, whether the harness retries, and what reaches the caller.

| Scenario | Configuration | Expected category |
|---|---|---|
| Normal | `https://api.githubcopilot.com/mcp/` with valid authorization | Tool discovery and calls succeed |
| Unauthorized | Real endpoint with a missing or invalid token/connection | OAuth challenge or authentication failure |
| Unreachable | `https://127.0.0.1:1/mcp/` | Connection/transport failure |
| Tool-level validation | Ask for an over-complex GitHub search or invalid arguments | MCP tool result reports an error while the connection remains usable |
| Empty results | Ask for an intentionally improbable repository query | Agent should explain the empty set and request/refine criteria |

For executable examples, override `MCP_SERVER_URL=https://127.0.0.1:1/mcp/` to reproduce the unreachable case. In Copilot Studio, create a temporary second MCP connection with that URL.

## Comparison worksheet

Capture these fields for each run:

1. Did MCP tool discovery complete?
2. Was the error delivered to the model, raised to host code, or converted to a runtime event?
3. Did the harness or agent retry? How many times?
4. Were alternate queries/tools attempted?
5. Did the final response acknowledge missing data without fabrication?
6. Did the process exit/fail, or continue with partial results?
7. Were logs/traces sufficient to reconstruct the sequence?

## Authentication

The hosted endpoint supports OAuth discovery. The local code examples also accept an already-issued token through `GITHUB_MCP_TOKEN`, which keeps authentication setup outside the comparison code. Never commit tokens or generated `.env` files.

The LangChain and Microsoft Agent Framework examples load their local `.env` file before configuration and use `DefaultAzureCredential` for Azure OpenAI. Managed identity is used when deployed to Azure; local developers can authenticate with `az login`. Both use `AZURE_OPENAI_ENDPOINT` and `AZURE_OPENAI_DEPLOYMENT_NAME`, with optional `AZURE_CLIENT_ID` for a user-assigned managed identity.

Both executable examples emit OpenTelemetry-compatible traces for model and tool activity. Content is excluded by default; set `TELEMETRY_INCLUDE_CONTENT=true` only in a secured local environment to capture the internal message sequence, tool arguments, and structured MCP error results.

## Documentation reviewed

- [LangChain AzureChatOpenAI](https://docs.langchain.com/oss/python/integrations/chat/azure_chat_openai)
- [LangChain MCP](https://docs.langchain.com/oss/python/langchain/mcp)
- [LangChain MCP authentication](https://docs.langchain.com/oss/python/langchain/mcp/auth)
- [Microsoft Agent Framework MCP tools](https://learn.microsoft.com/en-us/agent-framework/agents/tools/local-mcp-tools)
- [Microsoft Agent Framework Azure OpenAI provider](https://learn.microsoft.com/en-us/agent-framework/integrations/by-component/model-providers/azure-openai)
- [Microsoft Agent Framework Code Interpreter](https://learn.microsoft.com/en-us/agent-framework/agents/tools/code-interpreter)
- [AgentCore harness tools](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/harness-tools.html)
- [Copilot Studio MCP onboarding](https://learn.microsoft.com/en-us/microsoft-copilot-studio/mcp-add-existing-server-to-agent)
- [GitHub remote MCP server](https://github.com/github/github-mcp-server/blob/main/docs/remote-server.md)
