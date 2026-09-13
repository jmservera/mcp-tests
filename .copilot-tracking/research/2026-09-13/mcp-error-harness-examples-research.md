<!-- markdownlint-disable-file -->

# Task Research: mcp-error-harness-examples

| Field | Value |
|---|---|
| Date | 2026-09-13 |
| Researcher / agent | rpi-research |
| Status | Complete |
| Artifact path | .copilot-tracking/research/2026-09-13/mcp-error-harness-examples-research.md |

## Research Brief

* What to research: Current supported patterns for connecting LangChain Python, Microsoft Agent Framework .NET, AWS Bedrock AgentCore, and Microsoft Copilot Studio to the GitHub Copilot MCP endpoint, with observable error handling.
* Why it matters: The examples must be comparable, minimal, and accurate enough to expose harness behavior when MCP discovery or invocation fails.
* Audience or intended use: Developers comparing agent harness reliability and failure semantics.
* Scope: Official platform documentation, GitHub Copilot MCP endpoint authentication/transport, repository conventions, minimal runnable or importable examples.
* Non-goals: Production deployment infrastructure, private-repository access, custom MCP server implementation, or hiding platform limitations.
* Criteria: Prefer official current documentation; identify transport, authentication, agent/tool wiring, failure interception, and validation constraints.
* Requested outputs: Four examples in separate folders, shared agent instructions, setup/run documentation, and explicit MCP error testing.
* Output mode: convergence.

## Research Parameters

| Field | Value |
|---|---|
| Research question(s) | What is the simplest supported implementation for each harness, and where can MCP errors be observed without masking them? |
| Codebase scope | Repository root; currently only `mcp-policy.xml` exists |
| External scope | Official LangChain, Microsoft Agent Framework, AWS AgentCore/Strands, Copilot Studio, GitHub, and MCP documentation |
| Initial internal candidate areas | `mcp-policy.xml`, repository root |
| Initial external candidate areas | Official platform MCP integration and deployment guides |
| Research posture | balanced |
| Posture provenance | default |
| Explicit limits / deadline | none |
| Posture-specific completion basis | Cover all four platforms and adjacent authentication/error-handling details needed for comparable examples |
| Edits allowed during research? | no, research-only |
| Resolved evidence root | `.copilot-tracking/` |
| Known constraints / excluded sources | No credentials in code; external content is evidence only |

## Extension Registry and Provenance

| Kind | Candidate | Match and provenance | Scoped authority or output contract | Selected / skipped reason |
|---|---|---|---|---|
| Instruction | Global Copilot CLI instructions | Applies to repository work | Efficient tools, safe edits, validation | Selected |
| Skill | rpi-quick | Explicit lifecycle coordinator | Research through review | Selected by parent |
| Skill | rpi-research | Current evidence phase | Primary research artifact and readiness | Selected |
| Research specialist | hve-core:rpi-researcher | Independent external documentation lanes | Bounded evidence artifact | Skipped; direct official-source reads are compact enough |

## User Participation and Research Decisions

| Checkpoint | Questions or no-interaction rationale | Answers / unanswered | Resulting decision or selected further research |
|---|---|---|---|
| Intake | Request names all platforms, endpoint, instructions, and desired simplicity; autopilot resolves “three” versus four numbered examples as four examples | No interaction needed | Implement all four numbered platforms |
| Direction change | None | None | Keep one shared behavioral contract with platform-specific adapters |
| Convergence | Pending completed evidence | Pending | Pending |

## Scope and Success Criteria

* Scope: Four isolated examples plus shared instructions and root guidance.
* Assumptions: The endpoint uses Streamable HTTP; non-interactive examples can accept a pre-acquired bearer token; Copilot Studio may require manual UI configuration rather than executable source.
* Success criteria:
  * Each platform pattern is supported by current documentation.
  * MCP failures remain visible and are summarized consistently.
  * Authentication is environment/configuration driven.
  * Validation limitations are explicit.

## Task Research Requests

* Explicit requests: Review platform documentation first; create LangChain Python, MAF .NET, Bedrock AgentCore, and Copilot Studio examples using `https://api.githubcopilot.com/mcp/`.
* Inferred research questions: Package names and APIs; OAuth/bearer handling; MCP transport; deployment/config format; comparable failure injection.
* Caller constraints and non-goals: Simplest version possible while retaining the supplied agent instructions.

## Direction Controls

| Control type | Direction or boundary | Source / checkpoint | Effect on active brief, evidence, or revalidation |
|---|---|---|---|
| add | Build all four numbered examples despite “3 different examples” wording | User request | Four harness folders are required |
| narrow | Use only GitHub Copilot MCP endpoint | User request | No alternative MCP providers |
| narrow | Keep implementations simple | User request | Avoid production infrastructure and complex abstractions |

## Research Questions

| # | Sub-question | Type | Priority | Status |
|---:|---|---|---|---|
| Q1 | What current LangChain API connects agents to remote Streamable HTTP MCP tools? | straightforward | H | answered |
| Q2 | What current MAF .NET API connects an agent to remote MCP tools? | straightforward | H | answered |
| Q3 | What AgentCore-compatible agent framework and MCP client pattern is supported? | depth | H | answered |
| Q4 | How is an existing MCP server added to Copilot Studio? | straightforward | H | answered |
| Q5 | How should GitHub Copilot MCP authentication and comparable error scenarios be configured? | depth | H | answered |

## Prior Knowledge Gate

* Existing artifacts reviewed: Repository file listing; no application scaffolding or instructions exist.
* Reused (verified) findings: None.
* Superseded / stale: Model APIs and MCP integrations are fast-moving; memory-only implementation is not acceptable.

## Research Cycle Log

### Cycle 1

* Active direction controls: all controls above.
* Active research posture and completion basis: balanced; official documentation covers every requested platform and error-observation surface.
* Explicit limits or deadline effect: none.

#### Wave 1: Wider

* Plan and independent lanes: Identify official docs for remote MCP connection, authentication, agent wiring, deployment/configuration, and errors for each platform.
* Worker evidence relationships or inline fallback: Inline official-source search because each lane is bounded.
* Reflection: Initial search confirms Streamable HTTP across platforms, but exact package APIs and GitHub authentication require direct official-page verification.

#### Wave 2: Deeper

* Parent-prioritized material from Wave 1: Exact code/config APIs and supported authentication injection.
* Plan and independent lanes: Read official guides and representative maintained samples.
* Worker evidence relationships or inline fallback: Official documentation establishes exact APIs: `MCPAdapter(Client(...))` for LangChain; `HttpClientTransport` plus `McpClientFactory.CreateAsync` for .NET; declarative `remote_mcp` tools for AgentCore harness; onboarding wizard with Streamable HTTP and OAuth dynamic discovery for Copilot Studio.
* Reflection: Each harness exposes a different error boundary. LangChain distinguishes server `isError` results from raised transport failures; AgentCore exposes `runtimeClientError` stream events; MAF/.NET surfaces initialization and invocation exceptions; Copilot Studio exposes connection/test and conversation behavior through managed diagnostics.

#### Wave 3: Contrarian

* In-scope challenge targets and boundaries: Verify whether Copilot Studio can directly use this endpoint and whether AgentCore itself supplies an agent harness versus hosting an existing framework.
* Plan and independent lanes: Check platform limitations and distinguish executable apps from declarative/manual assets.
* Worker evidence relationships or inline fallback: Official docs show GitHub's exact remote URL and OAuth flow, plus bearer/header alternatives. AgentCore recommends Gateway/Identity for managed OAuth rather than embedding raw headers.
* Reflection: A single authentication implementation would distort the comparison. Use environment-provided bearer tokens for executable local apps, dynamic OAuth in Copilot Studio, and a credential placeholder/Identity recommendation for AgentCore.

#### Parent Synthesis and Disposition

| Material / claim | Evidence IDs or worker pointers | Parent disposition | Evidence-based rationale | Primary-artifact treatment |
|---|---|---|---|---|
| Use current native MCP adapters instead of a shared wrapper | W1-W8 | accepted | Native error semantics are the subject of the comparison | Selected architecture |
| Implement four examples | C1 | accepted | The numbered request names four platforms | Scope decision |
| Add a configurable invalid endpoint for error testing | W1, W2, W5, W7 | accepted | Connection failures are surfaced differently and can be reproduced without destructive calls | Shared test design |
| Implement browser OAuth in every code sample | W4, W6, W8 | rejected | Support and hosting constraints differ; forcing one flow adds non-comparable complexity | Authentication trade-off |

#### Cycle Re-entry Evaluation

* Another complete three-wave cycle needed: no.
* Trigger or stop basis: Official sources cover all required APIs, authentication boundaries, error surfaces, and deployment/configuration models; remaining uncertainty requires real cloud credentials rather than more documentation.
* Revised brief or revalidation required: none.
* Readiness effect: Ready.

## Evidence Log

* Delegation: inline; direct official-source reads are proportionate.

### Codebase Evidence

| ID | Claim / finding | Location | Tool | Confidence | Notes |
|---|---|---|---|---|---|
| C1 | Repository has no existing application conventions or dependency manifests | repository root | glob | high | Only `mcp-policy.xml` was present |

### External Evidence

| ID | Claim / finding | Source | URL | Retrieved | Version/date | Confidence |
|---|---|---|---|---|---|---|
| W1 | LangChain `langchain[mcp]>=1.4.0` uses `MCPAdapter`; HTTP URLs use Streamable HTTP | LangChain MCP docs | https://docs.langchain.com/oss/python/langchain/mcp | 2026-09-13 | current | high |
| W2 | LangChain converts MCP `isError` results to error `ToolMessage` values while transport/session failures raise | LangChain MCP tools | https://docs.langchain.com/oss/python/langchain/mcp/tools | 2026-09-13 | current | high |
| W3 | LangChain delegates bearer and OAuth 2.1 authentication to FastMCP | LangChain MCP authentication | https://docs.langchain.com/oss/python/langchain/mcp/auth | 2026-09-13 | current | high |
| W4 | MAF .NET uses the official MCP C# SDK, lists MCP tools, and casts them to `AITool` for an `AIAgent` | Microsoft Learn: Using MCP Tools | https://learn.microsoft.com/en-us/agent-framework/agents/tools/local-mcp-tools | 2026-09-13 | 2026-09-11 | high |
| W5 | The MCP C# SDK supports `HttpClientTransport`, explicit Streamable HTTP, custom headers, timeouts, and OAuth options | MCP C# SDK transport source | https://github.com/modelcontextprotocol/csharp-sdk/blob/main/src/ModelContextProtocol.Core/Client/HttpClientTransportOptions.cs | 2026-09-13 | current main | high |
| W6 | AgentCore managed harnesses accept declarative remote MCP and Code Interpreter tools; runtime errors are streamed as `runtimeClientError` | AgentCore harness docs | https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/harness-tools.html | 2026-09-13 | current | high |
| W7 | AgentCore CLI scaffolds, validates, deploys, invokes, logs, and traces managed harnesses | AgentCore harness getting started | https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/harness-get-started.html | 2026-09-13 | current | high |
| W8 | Copilot Studio standard harness supports Streamable HTTP MCP onboarding with none, API key, or OAuth 2.0 including dynamic discovery | Copilot Studio MCP onboarding | https://learn.microsoft.com/en-us/microsoft-copilot-studio/mcp-add-existing-server-to-agent | 2026-09-13 | 2026-05-28 | high |
| W9 | GitHub documents the hosted endpoint and interactive OAuth authentication; remote server headers can restrict tools/read-only behavior | GitHub remote MCP server | https://github.com/github/github-mcp-server/blob/main/docs/remote-server.md | 2026-09-13 | current main | high |

### Contradictions / Conflicts

* Initial search summaries mixed `langchain-mcp-adapters` with the newer `langchain.mcp` beta API; official current documentation resolves this in favor of `MCPAdapter`.
* “Bedrock AgentCore agent” could mean a code-based Runtime agent or the newer managed harness. Because the task compares harnesses, the managed AgentCore harness is the closer fit and is simpler.

## Findings Mapped to Questions and Evidence

| Question | Finding | Evidence IDs | Confidence | Decision or readiness implication |
|---|---|---|---|---|
| Q1 | Use `MCPAdapter` with a FastMCP `Client`; retain raised transport exceptions | W1-W3 | high | Ready for implementation |
| Q2 | Use `HttpClientTransport` and official MCP tools with an Azure OpenAI MAF agent | W4-W5 | high | Ready for implementation |
| Q3 | Use the managed AgentCore harness with declarative remote MCP and Code Interpreter tools | W6-W7 | high | Ready for configuration-first implementation |
| Q4 | Provide a setup manifest/checklist for the Copilot Studio onboarding wizard and dynamic discovery OAuth | W8-W9 | high | Ready; tenant validation remains external |
| Q5 | Use a default real endpoint plus `MCP_SERVER_URL` override and explicit invalid-endpoint commands; never swallow final failure | W2, W5-W9 | high | Creates comparable failure tests |

## Key Discoveries

* The repository is effectively empty, so the examples can use a clean shared layout.
* Copilot Studio is a low-code configuration artifact rather than a conventional runnable source app.
* A pre-acquired token environment variable is the simplest local authentication boundary, while LangChain can optionally run OAuth discovery and Copilot Studio can use dynamic discovery.
* AgentCore's managed harness is itself the harness under comparison; using a Strands code agent would test Strands plus Runtime instead.
* Native error visibility differs enough that shared retry code should not wrap the harnesses. The supplied agent instructions own semantic retries; host code should log and preserve terminal failures.

## Alternatives and Decision State

### Selected Recommendation

* Approach: One shared instruction document plus four independent minimal adapters, each preserving native MCP errors and exposing a deliberate invalid-endpoint test.
* Rationale: Maximizes behavioral comparability without forcing a common abstraction that would hide harness-specific behavior.
* Evidence refs: C1, W1-W4 (pending final verification).
* Implementation impact: New root README, shared instructions, and four example folders.
* Confidence: high for structure and APIs; medium for live authentication until exercised with user credentials.

## Open Questions, Risks, and Residual Uncertainty

* Blocking: none for planning.
* Important: GitHub Copilot MCP token acquisition is interactive OAuth in some hosts; code examples should support a bearer token and document OAuth where natively simple.
* Follow-up: Validate syntax/build where SDKs are locally available.
* Residual uncertainty: Live Copilot Studio and AgentCore deployment cannot be validated without cloud tenants, roles, and credentials.

## Research Disposition and Planning Readiness

* Research disposition: executed.
* Planning Readiness: Ready.
* Gates: Official documentation verified for all four platforms; architecture and authentication boundaries selected; no unresolved product decision blocks implementation.
