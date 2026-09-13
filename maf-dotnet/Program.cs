using Azure.AI.Projects;
using Azure.Identity;
using Microsoft.Agents.AI;
using Microsoft.Agents.AI.Foundry;
using Microsoft.Extensions.AI;
using ModelContextProtocol.Client;
using OpenAI.Responses;

const string defaultPrompt =
    "Find the best open-source repositories for building a production Model Context Protocol gateway. " +
    "Rank at least five candidates and create a score chart.";

static string Required(string name) =>
    Environment.GetEnvironmentVariable(name)
    ?? throw new InvalidOperationException($"{name} is required.");

try
{
    string endpoint = Required("AZURE_AI_PROJECT_ENDPOINT");
    string deployment = Environment.GetEnvironmentVariable("AZURE_AI_MODEL_DEPLOYMENT_NAME")
        ?? "gpt-4.1-mini";
    string mcpUrl = Environment.GetEnvironmentVariable("MCP_SERVER_URL")
        ?? "https://api.githubcopilot.com/mcp/";
    string instructions = await File.ReadAllTextAsync(
        Path.Combine(AppContext.BaseDirectory, "..", "..", "..", "..", "agent-instructions.md"));
    int timeoutSeconds = int.Parse(
        Environment.GetEnvironmentVariable("MCP_TIMEOUT_SECONDS") ?? "30");

    var transport = new HttpClientTransport(new HttpClientTransportOptions
    {
        Name = "gh-apim",
        Endpoint = new Uri(mcpUrl),
        TransportMode = HttpTransportMode.StreamableHttp,
        ConnectionTimeout = TimeSpan.FromSeconds(timeoutSeconds),
        AdditionalHeaders = new Dictionary<string, string>
        {
            ["Authorization"] = $"Bearer {Required("GITHUB_MCP_TOKEN")}",
            ["X-MCP-Readonly"] = "true",
            ["X-MCP-Toolsets"] = "repos",
        },
    });

    Console.WriteLine($"{{\"event\":\"mcp.connect\",\"url\":\"{mcpUrl}\"}}");
    await using var mcpClient = await McpClient.CreateAsync(transport);
    var mcpTools = await mcpClient.ListToolsAsync();
    if (mcpTools.Count == 0 || mcpTools.Any(tool => string.IsNullOrWhiteSpace(tool.Name)))
    {
        throw new InvalidOperationException(
            "MCP tool discovery returned an invalid or empty tool list.");
    }

    Console.WriteLine(
        $"{{\"event\":\"mcp.tools\",\"count\":{mcpTools.Count}}}");

    AITool codeInterpreter = FoundryAITool.CreateCodeInterpreterTool(
        new CodeInterpreterToolContainer(
            CodeInterpreterToolContainerConfiguration.CreateAutomaticContainerConfiguration([])));

    AIAgent agent = new AIProjectClient(new Uri(endpoint), new DefaultAzureCredential())
        .AsAIAgent(
            model: deployment,
            instructions: instructions,
            name: "GitHubRepositoryDiscovery",
            tools: [.. mcpTools.Cast<AITool>(), codeInterpreter]);

    var response = await agent.RunAsync(
        args.Length == 0 ? defaultPrompt : string.Join(' ', args));
    Console.WriteLine(response);
    return 0;
}
catch (Exception ex)
{
    Console.Error.WriteLine(
        $"{{\"event\":\"harness.failure\",\"type\":\"{ex.GetType().Name}\",\"message\":{System.Text.Json.JsonSerializer.Serialize(ex.Message)}}}");
    return 1;
}
