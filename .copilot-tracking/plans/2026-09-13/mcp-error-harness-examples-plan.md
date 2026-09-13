<!-- markdownlint-disable-file -->
# RPI Plan: MCP error harness examples

## Task Metadata

* Task ID: mcp-error-harness-examples
* Task slug: mcp-error-harness-examples
* Planning status: ready candidate
* Plan date: 2026-09-13
* Phase details: .copilot-tracking/details/2026-09-13/mcp-error-harness-examples-phase-details.md
* Plan critique: .copilot-tracking/reviews/plans/2026-09-13/mcp-error-harness-examples-plan-critique.md

## Executive Summary

Create four isolated examples that connect the same GitHub Copilot MCP endpoint to LangChain, Microsoft Agent Framework, the managed Bedrock AgentCore harness, and Copilot Studio. A shared prompt keeps agent behavior constant while each platform's native MCP initialization, tool-result, transport, and runtime errors remain visible. Each example includes a normal configuration and an invalid-endpoint test path.

### User Decisions and Requirements Highlights

* Use `https://api.githubcopilot.com/mcp/` and the supplied repository-discovery instructions in every example.
* Keep every example as simple as the platform permits and place it in its own folder.
* Review current platform documentation before implementation.

### What You May Not Know

* AgentCore now has a managed configuration-based harness. Using it directly is a more accurate harness comparison than deploying a Strands code loop to AgentCore Runtime.
* Copilot Studio is configured through its onboarding wizard, so its deliverable is a reproducible configuration guide and test matrix rather than a conventional executable project.
* Live OAuth and cloud deployment require user-owned tenants, subscriptions, roles, and credentials; repository validation can cover syntax, package restoration where available, and configuration shape.

### Unresolved Decisions or Blockers

* None. The code-first examples will accept an existing bearer token; Copilot Studio will use OAuth dynamic discovery; AgentCore documents a token-vault/Gateway path for production OAuth.

## User Decisions and Requirements

* Build the four numbered examples: LangChain Python, Microsoft Agent Framework .NET, Bedrock AgentCore, and Copilot Studio.
* Put each example in its own folder.
* Use the GitHub Copilot MCP server at `https://api.githubcopilot.com/mcp/`.
* Apply the supplied GitHub Repository Discovery Agent instructions consistently.
* Make each implementation minimal while retaining visible MCP error behavior.
* When an MCP operation fails, the agent should retry/fallback within the prompt's bounds, explain terminal failures, and continue with usable results.
* Review official platform documentation before coding.

## Goals

* Enable side-by-side comparison of native MCP error behavior across four harnesses.
* Keep prompt, endpoint, error scenarios, and expected observations comparable.
* Provide enough setup guidance to run each example without committing credentials.

## Scope and Non-Goals

### In Scope

* Shared agent instructions.
* LangChain Python console app with MCP adapter and deterministic error logging.
* MAF .NET console app with official MCP C# transport and Azure OpenAI agent.
* AgentCore managed harness configuration with remote MCP and Code Interpreter tools.
* Copilot Studio onboarding configuration and failure test matrix.
* Root comparison documentation and environment examples.

### Non-Goals

* Provisioning Azure, AWS, GitHub, or Power Platform resources.
* Implementing a custom OAuth broker or storing reusable credentials.
* Creating a custom MCP server.
* Normalizing or hiding platform-specific error objects.
* Live private-repository testing.

## Functional Requirements

* Every example uses the same complete system instructions.
  * Observable acceptance criteria: Shared prompt content is referenced or copied without semantic omissions.
* Every example defaults to the GitHub MCP endpoint and supports a reproducible connection-failure scenario.
  * Observable acceptance criteria: Documentation gives a command/configuration using an invalid endpoint and states the expected native error surface.
* Code-first examples log high-level MCP connection/run failure context and return a nonzero exit code on terminal host failure.
  * Observable acceptance criteria: No broad catch converts failure into success; exception type/message is emitted without credentials.
* Authentication is externalized.
  * Observable acceptance criteria: Tokens and cloud identifiers are read from environment/config placeholders and `.env` files are ignored.
* Every harness exposes a code execution/analysis tool consistent with the supplied instructions.
  * Observable acceptance criteria: LangChain includes a bounded Python scoring/chart tool, MAF includes a hosted Foundry Code Interpreter tool, AgentCore includes its managed Code Interpreter, and Copilot Studio setup adds a prompt tool with Code Interpreter enabled.
* Copilot Studio instructions use Streamable HTTP and OAuth dynamic discovery.
  * Observable acceptance criteria: The guide includes exact wizard values and normal, invalid URL, unauthorized, and tool-level error tests.

## Non-Functional Requirements

* Minimality.
  * Objective threshold or evaluation condition: No shared runtime abstraction and no unnecessary framework beyond each platform's official SDK.
  * Observable acceptance criteria: Each executable example has one primary source file and one dependency manifest.
* Traceability.
  * Objective threshold or evaluation condition: Root and per-example READMEs cite official documentation and describe observed error channels.
  * Observable acceptance criteria: Each platform section names its discovery/transport/tool/runtime failure behavior.
* Safety.
  * Objective threshold or evaluation condition: No secrets, destructive GitHub tools, or private/org searches by default.
  * Observable acceptance criteria: GitHub remote MCP is configured read-only with repository/search tools where the harness supports headers.
* Validation.
  * Objective threshold or evaluation condition: Run the smallest available syntax/build/config checks; document unavailable cloud validation.
  * Observable acceptance criteria: Python compiles, .NET restores/builds if SDK is available, and JSON/YAML parse successfully.

## Acceptance Criteria

* Four top-level example folders exist and are independently understandable.
* The LangChain and MAF examples can be configured with environment variables and preserve terminal MCP errors.
* The AgentCore example uses documented CLI commands to generate canonical project configuration and does not claim a guessed generated schema is valid.
* The Copilot Studio folder contains exact setup steps, prompt content, and an error-comparison checklist.
* A root README explains how to run the same prompt and failure cases across all four harnesses.
* No credential-like value is committed.

## Implementation Context Record

| Context item | Current artifact or record |
|---|---|
| Plan | .copilot-tracking/plans/2026-09-13/mcp-error-harness-examples-plan.md |
| Phase details | .copilot-tracking/details/2026-09-13/mcp-error-harness-examples-phase-details.md |
| Latest critique | .copilot-tracking/reviews/plans/2026-09-13/mcp-error-harness-examples-plan-critique.md with Revise verdict; all findings resolved directly |
| Relevant research | .copilot-tracking/research/2026-09-13/mcp-error-harness-examples-research.md |
| Changes-record role | .copilot-tracking/changes/2026-09-13/mcp-error-harness-examples-changes.md is created by implementation |
| Planning execution and readiness | Complete and implementation-ready after critique corrections |
| Continuation context | Active rpi-quick parent continues automatically after critique |

## Sources

* .copilot-tracking/research/2026-09-13/mcp-error-harness-examples-research.md: Current official API, authentication, and error-surface evidence.
* mcp-policy.xml: Existing repository context confirms OAuth discovery and the importance of preserving MCP transport/error semantics.
* User request: Defines platforms, endpoint, prompt, and simplicity requirement.

## Phase Checklist

<!-- rpi:phase id=P01 -->
### [x] P01: Establish shared comparison contract

* Intent: Create one prompt, common environment/error conventions, and root comparison guidance.
* Dependencies: Research complete.

<!-- rpi:task id=P01-T01 -->
#### [x] P01-T01: Add shared instructions and repository safeguards

* Requirement and evidence: User-supplied prompt; no committed credentials.
* Expected result: Shared instruction file, `.gitignore`, and common error-scenario definitions.
* Detail section: P01-T01 in .copilot-tracking/details/2026-09-13/mcp-error-harness-examples-phase-details.md

<!-- rpi:task id=P01-T02 -->
#### [x] P01-T02: Add root comparison documentation

* Requirement and evidence: Four harnesses need comparable execution and observation.
* Expected result: Root README maps normal, unauthorized, unreachable, and tool-level failure cases.
* Detail section: P01-T02 in .copilot-tracking/details/2026-09-13/mcp-error-harness-examples-phase-details.md

<!-- rpi:phase id=P02 -->
### [x] P02: Implement four harness examples

* Intent: Add the smallest native implementation/configuration for each platform.
* Dependencies: P01.

<!-- rpi:task id=P02-T01 -->
#### [x] P02-T01: Implement LangChain Python example

* Requirement and evidence: LangChain `MCPAdapter`/FastMCP auth and native error semantics.
* Expected result: One async app with MCP and bounded Python scoring/chart tools, dependency manifest, environment template, and README.
* Detail section: P02-T01 in .copilot-tracking/details/2026-09-13/mcp-error-harness-examples-phase-details.md

<!-- rpi:task id=P02-T02 -->
#### [x] P02-T02: Implement MAF .NET example

* Requirement and evidence: MAF with official MCP C# SDK and Azure OpenAI client.
* Expected result: Console app with MCP and hosted Code Interpreter tools, project file, environment template, and README.
* Detail section: P02-T02 in .copilot-tracking/details/2026-09-13/mcp-error-harness-examples-phase-details.md

<!-- rpi:task id=P02-T03 -->
#### [x] P02-T03: Implement AgentCore managed harness example

* Requirement and evidence: AgentCore declarative remote MCP and Code Interpreter tools.
* Expected result: Documented CLI scaffolding commands, system prompt, invocation helper, and README; generated project config remains CLI-owned.
* Detail section: P02-T03 in .copilot-tracking/details/2026-09-13/mcp-error-harness-examples-phase-details.md

<!-- rpi:task id=P02-T04 -->
#### [x] P02-T04: Implement Copilot Studio example

* Requirement and evidence: Standard harness MCP onboarding wizard with Streamable HTTP and OAuth dynamic discovery.
* Expected result: MCP configuration record, Code Interpreter prompt-tool setup, agent prompt, and error test matrix.
* Detail section: P02-T04 in .copilot-tracking/details/2026-09-13/mcp-error-harness-examples-phase-details.md

<!-- rpi:phase id=P03 -->
### [x] P03: Validate and reconcile

* Intent: Verify source/configuration integrity and align documentation with observed limits.
* Dependencies: P02.

<!-- rpi:task id=P03-T01 -->
#### [x] P03-T01: Run targeted validation

* Requirement and evidence: Python syntax, .NET build where available, JSON/YAML parsing, secret scan.
* Expected result: Passing local checks or explicit environment-blocked evidence.
* Detail section: P03-T01 in .copilot-tracking/details/2026-09-13/mcp-error-harness-examples-phase-details.md

<!-- rpi:task id=P03-T02 -->
#### [x] P03-T02: Reconcile documentation and implementation

* Requirement and evidence: Final files must describe actual commands, limitations, and error surfaces.
* Expected result: No stale paths, package names, or unsupported validation claims.
* Detail section: P03-T02 in .copilot-tracking/details/2026-09-13/mcp-error-harness-examples-phase-details.md

## Dependencies

* Python 3.10+ and model-provider credentials for LangChain runtime testing.
* .NET SDK and Azure OpenAI resource/credentials for MAF runtime testing.
* AWS account, AgentCore CLI, execution role, and GitHub credential provider for AgentCore deployment.
* Copilot Studio environment and GitHub authorization for managed connector testing.

## Critique Disposition

| Critique run and finding | Disposition | Plan response or residual risk |
|---|---|---|
| PC-001 Code Interpreter availability inconsistent | resolved | Added a native code execution/analysis tool requirement and task detail for all four harnesses |
| PC-002 Unsupported AgentCore generated-config claim | resolved | CLI commands are canonical; no hand-authored generated project configuration is required |

## Follow-Up Items

* None

## Handoff

* Implementation artifact: .copilot-tracking/changes/2026-09-13/mcp-error-harness-examples-changes.md
* Ready phase or task: P01
* Remaining provisional question or blocker: none
