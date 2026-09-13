<!-- markdownlint-disable-file -->
# RPI Phase Details: MCP error harness examples

## Metadata

* Task ID: mcp-error-harness-examples
* Task slug: mcp-error-harness-examples
* Related plan: .copilot-tracking/plans/2026-09-13/mcp-error-harness-examples-plan.md
* Evidence sources: .copilot-tracking/research/2026-09-13/mcp-error-harness-examples-research.md, mcp-policy.xml, user request

## Phase Index

| Phase ID | Name | Status | Detail sections |
|---|---|---|---|
| P01 | Establish shared comparison contract | complete | P01, P01-T01, P01-T02 |
| P02 | Implement four harness examples | complete | P02, P02-T01 through P02-T04 |
| P03 | Validate and reconcile | complete | P03, P03-T01, P03-T02 |

<!-- rpi:phase id=P01 -->
## P01: Establish shared comparison contract

### Context

The harness comparison is meaningful only if the endpoint, system instructions, user query, and failure scenarios remain constant. Existing repository code does not provide shared conventions.

### Intent

Create canonical shared assets before platform-specific wiring.

### Boundaries

* Included: Prompt, environment variable names, invalid endpoint convention, expected error categories, root overview.
* Excluded: Shared runtime wrapper or normalized exception class.

### Likely Targets

* `agent-instructions.md`: Canonical supplied prompt.
* `.gitignore`: Credential and generated artifact protection.
* `README.md`: Cross-harness setup and comparison matrix.

### Dependencies

* Completed research artifact.

### Validation Expectations

* Prompt is present and referenced by all examples.
* README commands match actual paths and environment variables.

### Completion Evidence

* Shared files exist and all four folders are listed.

### Unresolved Items

* None.

<!-- rpi:task id=P01-T01 -->
### P01-T01: Add shared instructions and repository safeguards

#### Context

The user supplied a long prompt whose reliability clauses are central to the error comparison.

#### Intent

Preserve it as the canonical instruction source and prevent accidental credential commits.

#### Boundaries

* Included: Exact semantic content, path references, `.env`/chart/cache ignores.
* Excluded: Rewriting prompt behavior.

#### Likely Targets

* `agent-instructions.md`
* `.gitignore`

#### Dependencies

* None.

#### Validation Expectations

* Every numbered instruction and output heading remains present.

#### Completion Evidence

* File review and search for key clauses.

#### Unresolved Items

* None.

<!-- rpi:task id=P01-T02 -->
### P01-T02: Add root comparison documentation

#### Context

Native failure semantics differ and must be compared without implying equivalent behavior.

#### Intent

Document one repeatable normal request and four failure classes.

#### Boundaries

* Included: Discovery/auth/transport/tool failure matrix and commands.
* Excluded: Fabricated runtime outcomes.

#### Likely Targets

* `README.md`

#### Dependencies

* P01-T01.

#### Validation Expectations

* Links and commands resolve to created files.

#### Completion Evidence

* Manual path/config reconciliation.

#### Unresolved Items

* None.

<!-- rpi:phase id=P02 -->
## P02: Implement four harness examples

### Context

Official sources define four distinct extension points. Native implementations must remain separate.

### Intent

Create minimal examples that expose each harness's own failure surface.

### Boundaries

* Included: One primary source/config path per example, a native code execution/analysis tool, environment templates, concise READMEs.
* Excluded: Infrastructure-as-code, shared retry library, custom OAuth application.

### Likely Targets

* `langchain-python/`
* `maf-dotnet/`
* `bedrock-agentcore/`
* `copilot-studio/`

### Dependencies

* P01.

### Validation Expectations

* Dependency manifests parse/restore where tools are available.
* Source/config files contain no tokens.

### Completion Evidence

* Four complete folder trees and targeted checks.

### Unresolved Items

* None.

<!-- rpi:task id=P02-T01 -->
### P02-T01: Implement LangChain Python example

#### Context

Current LangChain uses beta `langchain.mcp.MCPAdapter` backed by FastMCP. Server-reported errors become error `ToolMessage` values; connection failures raise.

#### Intent

Create an async console app that loads the shared instructions, connects with OAuth or bearer auth, adds a bounded Python scoring/chart tool, lists tools, runs the agent, and reports terminal failures.

#### Boundaries

* Included: OpenAI-compatible LangChain model selection, endpoint override, timeout, optional OAuth mode, bounded pandas/matplotlib analysis tool, concise operational log.
* Excluded: Catching and synthesizing server `ToolMessage` errors outside the agent.

#### Likely Targets

* `langchain-python/app.py`
* `langchain-python/pyproject.toml`
* `langchain-python/.env.example`
* `langchain-python/README.md`

#### Dependencies

* Python 3.10+, model credential, GitHub authorization.

#### Validation Expectations

* `python3 -m py_compile` and dependency metadata parsing.

#### Completion Evidence

* Compile passes; invalid endpoint path is documented.

#### Unresolved Items

* Live OAuth/browser and model invocation require credentials.

<!-- rpi:task id=P02-T02 -->
### P02-T02: Implement MAF .NET example

#### Context

MAF consumes official MCP C# SDK tools as `AITool`; the SDK has explicit Streamable HTTP, headers, OAuth, and connection timeout options.

#### Intent

Create one console program using a Foundry/Azure AI agent with MCP C# transport and a hosted `FoundryAITool` Code Interpreter, with environment validation and native exception reporting.

#### Boundaries

* Included: Bearer header, read-only tool headers, endpoint override, timeout, one agent invocation.
* Additional included behavior: hosted Code Interpreter.
* Excluded: Interactive OAuth callback server and custom retry middleware.

#### Likely Targets

* `maf-dotnet/MafMcpErrors.csproj`
* `maf-dotnet/Program.cs`
* `maf-dotnet/.env.example`
* `maf-dotnet/README.md`

#### Dependencies

* .NET SDK, Azure OpenAI endpoint/deployment, Azure credential, GitHub token.

#### Validation Expectations

* `dotnet build` when SDK exists; otherwise XML/source inspection and documented limitation.

#### Completion Evidence

* Build result or environment-blocked evidence.

#### Unresolved Items

* Exact NuGet prerelease versions resolve at implementation time.

<!-- rpi:task id=P02-T03 -->
### P02-T03: Implement AgentCore managed harness example

#### Context

Managed harness tools are declarative and runtime failures appear as streamed `runtimeClientError` events. Direct remote MCP supports headers; managed OAuth should use Gateway/Identity.

#### Intent

Provide documented CLI scaffolding for a harness with remote GitHub MCP and Code Interpreter, plus the system prompt and a simple invoke helper that prints runtime errors.

#### Boundaries

* Included: Canonical CLI commands, system prompt, boto3 invocation helper, deployment/test instructions.
* Excluded: AWS role/CDK provisioning and raw token committed into JSON.

#### Likely Targets

* `bedrock-agentcore/app/github-repository-discovery/system-prompt.md`
* `bedrock-agentcore/invoke.py`
* `bedrock-agentcore/pyproject.toml`
* `bedrock-agentcore/README.md`

#### Dependencies

* AWS credentials, current AgentCore CLI, execution role, credential provider/Gateway for production auth.

#### Validation Expectations

* Python syntax parses; documented JSON fragments parse; `agentcore validate` runs only after CLI scaffolding if installed.

#### Completion Evidence

* Local parsing passes and cloud-only steps are explicit.

#### Unresolved Items

* Generated AgentCore project files are CLI-managed and intentionally absent from the repository example.

<!-- rpi:task id=P02-T04 -->
### P02-T04: Implement Copilot Studio example

#### Context

Copilot Studio uses a managed onboarding wizard and supports Streamable HTTP plus OAuth dynamic discovery.

#### Intent

Provide a reproducible MCP setup record, a Code Interpreter-enabled prompt tool, and an error test matrix using the shared prompt.

#### Boundaries

* Included: Wizard values, dynamic discovery OAuth, Code Interpreter prompt tool, agent prompt, normal/error scenarios, observed-result worksheet.
* Excluded: Unexportable tenant-specific agent package and credentials.

#### Likely Targets

* `copilot-studio/README.md`
* `copilot-studio/agent-instructions.md`
* `copilot-studio/error-test-matrix.md`

#### Dependencies

* Copilot Studio tenant and environment.

#### Validation Expectations

* Markdown consistency and exact endpoint/auth settings.

#### Completion Evidence

* Setup can be followed without inferred values.

#### Unresolved Items

* Live connector creation cannot be verified locally.

<!-- rpi:phase id=P03 -->
## P03: Validate and reconcile

### Context

Two examples depend on local SDKs and two require cloud control planes. Validation must distinguish observed checks from unexecuted cloud behavior.

### Intent

Verify all locally measurable requirements and ensure documentation states limitations precisely.

### Boundaries

* Included: Syntax/build/config validation, secret scan, path/reference review, Git diff review.
* Excluded: Deploying billable/shared cloud resources.

### Likely Targets

* All created source, config, and README files.

### Dependencies

* P02.

### Validation Expectations

* Python and JSON checks pass.
* .NET build attempted only if SDK is present.
* No secret patterns or placeholder tokens that resemble real credentials.

### Completion Evidence

* Commands and outcomes recorded in changes artifact.

### Unresolved Items

* Live OAuth and tool calls remain user-run acceptance tests.

<!-- rpi:task id=P03-T01 -->
### P03-T01: Run targeted validation

#### Context

Validation should cover the exact artifacts without adding tooling.

#### Intent

Run the smallest available checks.

#### Boundaries

* Included: `python3 -m py_compile`, JSON parsing, XML project parse, `dotnet build` if present, `agentcore validate` if present, `git diff --check`.
* Excluded: Package installation solely to compensate for missing platform SDKs.

#### Likely Targets

* All executable/configuration files.

#### Dependencies

* P02 complete.

#### Validation Expectations

* All available checks pass.

#### Completion Evidence

* Changes artifact records commands and results.

#### Unresolved Items

* None beyond unavailable tools/cloud credentials.

<!-- rpi:task id=P03-T02 -->
### P03-T02: Reconcile documentation and implementation

#### Context

Fast-moving APIs make stale names and unsupported claims a material risk.

#### Intent

Review final paths, package names, environment variables, and error descriptions against the implementation.

#### Boundaries

* Included: Directly related corrections.
* Excluded: New features discovered during review.

#### Likely Targets

* Root and per-example READMEs.

#### Dependencies

* P03-T01.

#### Validation Expectations

* No broken local links or mismatched commands.

#### Completion Evidence

* Final diff review.

#### Unresolved Items

* None.

## Candidate Validation Lock

* Test ownership: Implementation owns syntax/build/config checks; users own credentialed cloud integration tests.
* Exact removals: none.
* Maximum additions: one root README, one shared prompt, one `.gitignore`, and up to five focused files per example folder.
* Canonical targets: `agent-instructions.md`, four example folders, root README.
* Generated targets: All AgentCore project configuration is generated by the CLI and is intentionally not hand-authored.
* Semantic coverage: Same prompt and normal/failure scenarios across harnesses.
* Regression coverage: Existing `mcp-policy.xml` remains unchanged.
* Validation evidence: Python compile, JSON/XML parse, optional .NET build/AgentCore validation, diff and secret checks.
