using Azure.Identity;
using DotNetEnv;
using Microsoft.Agents.AI;
using Microsoft.Agents.AI.Foundry;
using Microsoft.Extensions.AI;
using ModelContextProtocol.Client;
using OpenAI.Responses;
using System.ClientModel.Primitives;

const string defaultPrompt =
    "After identifying my username, make the first search_repositories call with this query verbatim. Do not split or simplify it:"+
    "user:jmservera (books OR library OR catalog OR doc OR docx OR pdf OR html OR epub OR markdown OR jpeg OR tiff)"+
    "When the recoverable validation error is returned, follow its instructions and retry using smaller searches. Then rank the repositories and open the requested Windows desktop client PR.";
    
static string Required(string name) =>
    Environment.GetEnvironmentVariable(name)
    ?? throw new InvalidOperationException($"{name} is required.");

static Uri RequiredResponsesEndpoint()
{
    string value = Required("AZURE_OPENAI_ENDPOINT");
    if (!Uri.TryCreate(value, UriKind.Absolute, out Uri? endpoint)
        || endpoint.Scheme != Uri.UriSchemeHttps)
    {
        throw new InvalidOperationException(
            "AZURE_OPENAI_ENDPOINT must be an absolute HTTPS endpoint.");
    }

    string path = endpoint.AbsolutePath.TrimEnd('/');
    if (path.EndsWith("/responses", StringComparison.OrdinalIgnoreCase))
    {
        path = path[..^"/responses".Length];
    }
    if (string.IsNullOrEmpty(path))
    {
        path = "/openai/v1";
    }
    if (!path.EndsWith("/openai/v1", StringComparison.OrdinalIgnoreCase))
    {
        throw new InvalidOperationException(
            "AZURE_OPENAI_ENDPOINT must be an Azure OpenAI Responses base endpoint, " +
            "for example 'https://<resource-name>.openai.azure.com/openai/v1'.");
    }

    var builder = new UriBuilder(endpoint)
    {
        Path = path,
        Query = string.Empty,
        Fragment = string.Empty,
    };
    return builder.Uri;
}

static void LoadEnvironment()
{
    string workingDirectoryPath = Path.Combine(Environment.CurrentDirectory, ".env");
    string projectPath = Path.GetFullPath(
        Path.Combine(AppContext.BaseDirectory, "..", "..", "..", ".env"));
    string? path = File.Exists(workingDirectoryPath)
        ? workingDirectoryPath
        : File.Exists(projectPath) ? projectPath : null;
    if (path is not null)
    {
        Env.NoClobber().Load(path);
    }
}

try
{
    LoadEnvironment();
    Uri endpoint = RequiredResponsesEndpoint();
    string deployment = Environment.GetEnvironmentVariable("AZURE_OPENAI_DEPLOYMENT_NAME")
        ?? "gpt-4.1-mini";
    string mcpUrl = Environment.GetEnvironmentVariable("MCP_SERVER_URL")
        ?? "https://api.githubcopilot.com/mcp/";
    string instructions = await File.ReadAllTextAsync(
        Path.Combine(AppContext.BaseDirectory, "..", "..", "..", "..", "agent-instructions.md"));
    int timeoutSeconds = int.Parse(
        Environment.GetEnvironmentVariable("MCP_TIMEOUT_SECONDS") ?? "30");
    string? managedIdentityClientId = Environment.GetEnvironmentVariable("AZURE_CLIENT_ID");
    var credential = new DefaultAzureCredential(
        new DefaultAzureCredentialOptions
        {
            ExcludeEnvironmentCredential = true,
            ManagedIdentityClientId = string.IsNullOrWhiteSpace(managedIdentityClientId)
                ? null
                : managedIdentityClientId,
        });
    var responsesClient = new ResponsesClient(
        authenticationPolicy: new BearerTokenPolicy(
            credential,
            "https://ai.azure.com/.default"),
        options: new ResponsesClientOptions { Endpoint = endpoint });
    AITool codeInterpreter = FoundryAITool.CreateCodeInterpreterTool(
        new CodeInterpreterToolContainer(
            CodeInterpreterToolContainerConfiguration.CreateAutomaticContainerConfiguration([])));

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

    AIAgent agent = responsesClient.AsAIAgent(
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
