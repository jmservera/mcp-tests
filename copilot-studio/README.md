# Microsoft Copilot Studio

Copilot Studio is a managed, low-code harness. This folder records the reproducible agent configuration rather than pretending that tenant-specific exported code can be run locally.

## Create the agent

1. Create an agent that uses the **standard harness**.
2. Copy the contents of [`../agent-instructions.md`](../agent-instructions.md) into the agent's **Instructions**.
3. Do not add private knowledge sources for the baseline comparison.

## Add the GitHub MCP server

On the agent's **Tools** page:

1. Select **Add a tool** > **New tool** > **Model Context Protocol**.
2. Set **Server name** to `gh-apim`.
3. Set **Server description** to `Search GitHub repositories and retrieve repository metadata for evidence-based repository discovery.`
4. Set **Server URL** to `https://api.githubcopilot.com/mcp/`.
5. Select **OAuth 2.0**.
6. Select **Dynamic discovery**.
7. Create the connection, complete GitHub authorization, and add the tool to the agent.

The GitHub server's OAuth connection represents the signed-in user. Keep the baseline public-only; obtain explicit user clarification before private or organization-scoped searches.

## Add Code Interpreter

1. Select **Add a tool** > **New tool** > **Prompt**.
2. Name it `Analyze repository candidates`.
3. Add a required **Text** input named `repository_metadata_json`. Describe it as `A JSON array of repository metadata gathered from GitHub MCP, including repository, stars, forks, last_updated, relevance, and maintenance_quality.`
4. Insert `repository_metadata_json` into the prompt and use:

   > Given the repository metadata JSON below, validate the fields and calculate the deterministic weighted score specified by the agent instructions. Return the scored repository array as JSON, including normalized metrics and total score, and create a horizontal ranking bar chart as a file.
   >
   > Repository metadata:
   > `/repository_metadata_json`

   Use the prompt editor's variable insertion control for `/repository_metadata_json`; do not type a look-alike literal if the editor renders inserted variables differently.
5. Configure the prompt output to return both the scored JSON text and the generated chart file.
6. Enable **Code interpreter** in the prompt editor.
7. Save the prompt and add it to the agent.

Copilot Studio exposes Code Interpreter through a prompt tool, so the orchestrator must choose that tool after GitHub metadata has been gathered and pass the gathered JSON into the required `repository_metadata_json` input.

## Test

Use the common prompt from the root README, then complete [`error-test-matrix.md`](error-test-matrix.md). For the unreachable case, create a temporary second MCP tool with `https://127.0.0.1:1/mcp/`; delete it after testing.

The managed service can reject an invalid connection during setup rather than during conversation. Record that distinction because it is part of the harness behavior.

Official docs: [connect an existing MCP server](https://learn.microsoft.com/en-us/microsoft-copilot-studio/mcp-add-existing-server-to-agent) and [Code Interpreter for prompts](https://learn.microsoft.com/en-us/microsoft-copilot-studio/code-interpreter-for-prompts).
