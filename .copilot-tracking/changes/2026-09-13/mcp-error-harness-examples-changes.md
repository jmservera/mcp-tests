<!-- markdownlint-disable-file -->
# RPI Changes: MCP error harness examples

## Metadata

* Task ID: mcp-error-harness-examples
* Related plan: .copilot-tracking/plans/2026-09-13/mcp-error-harness-examples-plan.md
* Phase details: .copilot-tracking/details/2026-09-13/mcp-error-harness-examples-phase-details.md
* Implementation date: 2026-09-13

## Execution Status

* Status: Complete
* Declared invocation scope: full plan
* Completed scope markers: P01, P01-T01, P01-T02, P02, P02-T01, P02-T02, P02-T03, P02-T04, P03, P03-T01, P03-T02
* All remaining active-plan markers: none
* Status basis: Full approved plan is implemented and all available local validation passes.

## Execution Summary

The shared comparison contract and all four platform examples are implemented. Validation corrected current LangChain and MAF API mismatches, verified controlled failure paths, and reconciled documentation with the final source.

## Completed Work

### Established the shared comparison contract

* Related phase or task: P01, P01-T01, P01-T02.
* Files: `.gitignore`, `agent-instructions.md`, `README.md`.
* What changed and why: Added the canonical agent instructions, credential/generated-file safeguards, common prompt, error scenarios, and comparison worksheet.
* Completion evidence: All four harness folders and native error surfaces are linked from the root README.
* Validation: Markdown/path reconciliation pending final pass.

### Implemented LangChain Python example

* Related phase or task: P02-T01.
* Files: `langchain-python/app.py`, `langchain-python/pyproject.toml`, `langchain-python/.env.example`, `langchain-python/README.md`.
* What changed and why: Added current `MCPAdapter`/FastMCP integration, bearer or OAuth auth, bounded deterministic pandas/matplotlib scoring, tool validation, and terminal failure logging.
* Completion evidence: Dependencies install; current constructor APIs import; scoring tool creates a chart.
* Validation: Python compile and direct scoring-tool test passed.

### Implemented Microsoft Agent Framework .NET example

* Related phase or task: P02-T02.
* Files: `maf-dotnet/Program.cs`, `maf-dotnet/MafMcpErrors.csproj`, `maf-dotnet/.env.example`, `maf-dotnet/README.md`.
* What changed and why: Added current MCP 2.2 Streamable HTTP client, Foundry agent, hosted Code Interpreter, externalized auth, and native exception logging.
* Completion evidence: Current NuGet packages restore and the project builds with .NET 10.
* Validation: `dotnet build` passed with zero warnings/errors.

### Implemented AgentCore managed harness example

* Related phase or task: P02-T03.
* Files: `bedrock-agentcore/invoke.py`, `bedrock-agentcore/pyproject.toml`, `bedrock-agentcore/README.md`.
* What changed and why: Added CLI-owned harness scaffolding guidance, remote MCP and Code Interpreter configuration, token-vault auth, and a stream consumer that reports `runtimeClientError`.
* Completion evidence: Python source compiles and documented configuration fragments parse.
* Validation: Cloud validation pending user AWS account and generated project.

### Implemented Copilot Studio example

* Related phase or task: P02-T04.
* Files: `copilot-studio/README.md`, `copilot-studio/agent-instructions.md`, `copilot-studio/error-test-matrix.md`.
* What changed and why: Added exact MCP onboarding, dynamic OAuth, Code Interpreter prompt-tool setup, and an observation worksheet.
* Completion evidence: Setup values match current official documentation.
* Validation: Live tenant validation remains user-owned.

## Implementation-Time Plan and Detail Updates

### Applied critique corrections before implementation

* Affected plan area or markers: Functional Requirements, Acceptance Criteria, P02-T01 through P02-T04.
* What changed: Added a truthful native Code Interpreter path for every harness and made AgentCore CLI scaffolding canonical.
* Why: Resolve PC-001 and PC-002 without changing user intent.
* Triggering evidence: .copilot-tracking/reviews/plans/2026-09-13/mcp-error-harness-examples-plan-critique.md.
* User answer or decision: none; direct planner correction.
* Reconciliation performed: Executive summary, requirements, tasks, details, validation ownership, critique disposition, and handoff are current.
* Planning and critique state: Implementation-ready; one critique completed and resolved.

## Validation Record

| Check | Scope | Status | Evidence or reason |
|---|---|---|---|
| Python compile | LangChain and AgentCore | Passed | `python3 -m py_compile` completed |
| LangChain dependency/API import | LangChain | Passed | Fresh virtual environment installed the project and imported current FastMCP/LangChain APIs |
| LangChain scoring/chart test | LangChain | Passed | Two-candidate fixture produced deterministic ranking JSON and a chart |
| LangChain missing-token failure | LangChain | Passed | Exited 1 with structured `ValueError` event |
| LangChain unreachable MCP failure | LangChain | Passed | Exited 1 with structured connection failure event |
| NuGet package restore/build | MAF | Passed | .NET 10 build completed with zero warnings and errors |
| MAF unreachable MCP failure | MAF | Passed | Exited 1 with structured `HttpRequestException` event |
| AgentCore missing-configuration failure | AgentCore | Passed | Invocation helper exited nonzero when harness ARN was absent |
| TOML/XML parsing | All manifests | Passed | Python standard-library parsers completed |
| Local Markdown links | Production docs | Passed | Every relative Markdown target exists |
| Secret pattern scan | Repository | Passed | No token/key patterns found |
| Diff/trailing whitespace | Repository | Passed | `git diff --check` and source checks completed |
| AgentCore live validation | AgentCore | Unavailable | Requires generated CLI project, AWS account, execution role, and credential provider |
| Copilot Studio live validation | Copilot Studio | Unavailable | Requires user tenant, connection, and GitHub authorization |

## Pre-Review Reconciliation

* Plan markers and phase details: All active markers complete and current.
* Completed-work evidence and handoff prose: Current.
* Validation, blockers, remaining work, and follow-up items: Available checks pass; no blockers, remaining work, or follow-ups.
* Review readiness: Ready.

## Blockers

* None.

## Remaining Work

* None.

## Follow-Up Items

* Canonical plan list: .copilot-tracking/plans/2026-09-13/mcp-error-harness-examples-plan.md, `## Follow-Up Items`
* None.

## Return-to-Caller State

* Implementation execution status: Complete.
* Declared scope and markers: Full plan; P01 through P03 and all tasks complete.
* Validation coverage: Python, LangChain APIs/scoring/failures, MAF build/failure, AgentCore helper failure, config parsing, links, secrets, and whitespace passed; credentialed cloud validation unavailable.
* Blockers: none.
* Current plan and detail updates: Critique corrections applied.
* Planning and critique state: Current and implementation-ready.
* Follow-up items: none.
* Review readiness or no-handoff reason: Ready for one post-implementation review.
* Continuation owner: rpi-quick parent.
