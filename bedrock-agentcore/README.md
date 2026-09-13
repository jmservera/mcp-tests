# Bedrock AgentCore managed harness

This example uses the AgentCore **managed harness**, not a custom Strands loop. AgentCore owns model/tool orchestration and emits failures as streaming events such as `runtimeClientError`.

AgentCore's CLI owns generated project configuration. The repository keeps only the canonical prompt and invocation helper instead of guessing the generated `harness.json` schema.

## Scaffold

Install the current CLI:

```bash
npm install -g @aws/agentcore
```

From this folder, create a project and harness:

```bash
agentcore create --project-name github-mcp-errors --no-agent
cd github-mcp-errors

agentcore add harness \
  --name github-repository-discovery \
  --model-provider bedrock \
  --model-id global.anthropic.claude-sonnet-4-6 \
  --system-prompt "$(cat ../../agent-instructions.md)" \
  --tools remote_mcp \
  --mcp-name gh-apim \
  --mcp-url https://api.githubcopilot.com/mcp/ \
  --mcp-headers '{"Authorization":"Bearer ${arn:aws:bedrock-agentcore:REGION:ACCOUNT_ID:token-vault/default/apikeycredentialprovider/github-mcp-token}","X-MCP-Readonly":"true","X-MCP-Toolsets":"repos"}'

agentcore add tool \
  --harness github-repository-discovery \
  --type agentcore_code_interpreter \
  --name code-interpreter
```

The `${arn:...}` value is AgentCore's documented token-vault reference syntax. Create the credential provider through AgentCore Identity; do not put a token in source control. For managed OAuth rotation, put the MCP server behind AgentCore Gateway and configure outbound OAuth.

Then validate and deploy:

```bash
agentcore validate
agentcore deploy
agentcore invoke --harness github-repository-discovery \
  --allowed-tools "@gh-apim,code-interpreter" \
  "Find the best open-source repositories for building a production MCP gateway."
```

## Invoke with Python

```bash
cd bedrock-agentcore
python3 -m venv .venv
. .venv/bin/activate
pip install -e .
export AGENTCORE_HARNESS_ARN=arn:aws:bedrock-agentcore:...
python invoke.py
```

## Error tests

- **Unauthorized:** configure an invalid credential provider value and invoke.
- **Unreachable:** create a temporary harness tool whose URL is `https://127.0.0.1:1/mcp/`.
- **Runtime:** run `agentcore invoke --verbose` and compare the raw stream with `invoke.py`; runtime failures are printed from `runtimeClientError`.

`invoke.py` does not add retries, so managed-harness retry behavior remains observable. It validates the SDK response and known event payloads, then writes failures as JSON with `event`, `stage`, `type`, and `message` fields. Native `runtimeClientError` messages retain that event name as their stage; SDK call failures, malformed responses, and lazy stream failures use distinct host-side stages.

Official docs: [AgentCore harness](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/harness.html), [tools](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/harness-tools.html), and [streaming errors](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/harness-get-started.html#harness-streaming-format).
