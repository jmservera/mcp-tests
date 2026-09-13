<!-- markdownlint-disable-file -->
# Review: MCP error harness examples

## Scope and Evidence

* Task ID: mcp-error-harness-examples
* Review date: 2026-09-13
* Review scope: Full task, P01 through P03.
* Assessed boundary: Shared prompt, four harness implementations/configurations, MCP authentication and errors, Code Interpreter paths, documentation, dependencies, and available validation.
* Plan: .copilot-tracking/plans/2026-09-13/mcp-error-harness-examples-plan.md
* Phase details: .copilot-tracking/details/2026-09-13/mcp-error-harness-examples-phase-details.md
* Plan critique: .copilot-tracking/reviews/plans/2026-09-13/mcp-error-harness-examples-plan-critique.md
* Changes: .copilot-tracking/changes/2026-09-13/mcp-error-harness-examples-changes.md
* Other evidence considered: .copilot-tracking/research/2026-09-13/mcp-error-harness-examples-research.md, production files, package restore/build output, controlled failure-path output.

## Opening Review State

* Interpreted review goal: Determine whether the four examples are credible, comparable, and usable for observing MCP failures.
* Review scope: Full task.
* Evidence readiness: Complete artifact set and local validation evidence available.
* Acceptance basis: Current plan requirements and criteria, resolved PC-001/PC-002, and user-supplied instructions.
* First comparison boundary: Functional use of MCP and Code Interpreter in each example.
* Active read-only boundaries: Review may write only this record.
* Initial blockers: none.

## Execution Status

* Execution status: Complete.
* Review execution evidence: One full comparison completed on 2026-09-13 across all plan markers, source files, configuration guidance, and validation records.

## Plan-to-Change Reconciliation

| Current plan scope | Descriptive changes-record summary | Current-state reconciliation | Gap or rationale |
|---|---|---|---|
| P01 | Shared comparison contract | Reconciled | Canonical prompt, safeguards, matrix, and docs exist |
| P02-T01 | LangChain example | Reconciled | Current API installed and scoring tool executed |
| P02-T02 | MAF example | Reconciled | Current packages restore and build |
| P02-T03 | AgentCore example | Reconciled | CLI-owned config boundary preserved |
| P02-T04 | Copilot Studio example | Partial | MCP setup is complete; prompt-tool input binding is underspecified |
| P03 | Validation and reconciliation | Reconciled | Available checks pass; cloud checks are correctly unavailable |

## Completed Work Assessment

| Related marker | Files | What changed and why | Completion evidence | Validation | Assessment |
|---|---|---|---|---|---|
| P01 | `.gitignore`, `agent-instructions.md`, `README.md` | Established common behavior and scenarios | Files and links exist | Links/secrets/format passed | Reconciled |
| P02-T01 | `langchain-python/` | Native MCP plus bounded analysis tool | Imports and scoring fixture pass | Compile, install, tool, failures pass | Reconciled with RV-001 |
| P02-T02 | `maf-dotnet/` | Native MCP plus hosted Code Interpreter | Build succeeds | .NET build and failure path pass | Reconciled |
| P02-T03 | `bedrock-agentcore/` | Managed harness setup and stream helper | Source/config docs exist | Python/config checks pass; cloud unavailable | Reconciled |
| P02-T04 | `copilot-studio/` | MCP and prompt-tool setup | Setup guide and matrix exist | Local docs pass; tenant unavailable | Gap recorded as RV-002 |
| P03 | All production files | Validation and docs alignment | Changes record is current | Available suite passes | Reconciled |

## Implementation-Time Plan and Detail Update Assessment

| Affected area or marker | What changed and why | Triggering evidence and user decision | Reconciliation performed | Planning and critique state | Assessment |
|---|---|---|---|---|---|
| Functional requirements, P02 | Added native code execution paths and removed guessed AgentCore config | PC-001 and PC-002; no new user decision | Plan, details, tasks, criteria, and handoff updated | Critique findings resolved | Reconciled |
| P02-T01 | Replaced deprecated Python REPL dependency with bounded pandas/matplotlib tool | Install warning and current API validation | Source, manifest, README, plan wording, and details updated | Preserves accepted intent | Reconciled |
| P02-T02 | Updated current MCP/MAF APIs and package versions | Real restore/build failures and package metadata | Source, package versions, README, and details updated | Preserves accepted intent | Reconciled |

## Critique and Material Revision Assessment

* Latest critique dispositions: PC-001 and PC-002 are both resolved in the current plan and implementation.
* Material revisions: No divergent user decision was introduced; changes preserve the requested four-harness comparison.
* Dependent-work pause assessment: No affected work resumed before planner-owned corrections were recorded.
* Justification assessment: Supported.

## Plan Follow-Up Assessment

| Follow-up item | Why outside immediate scope | Owner or next action | Assessment and route |
|---|---|---|---|
| None | Not applicable | Not applicable | No pre-existing follow-up |

## Findings

<!-- rpi:review id=RV-001 -->
### RV-001 [Medium]: LangChain MCP timeout also limits the complete agent run

* Related scope: P02-T01.
* Evidence: `langchain-python/app.py` places MCP connection, discovery, all model turns, GitHub tool calls, scoring, and chart generation inside one `asyncio.timeout` configured as `MCP_TIMEOUT_SECONDS=30`.
* Impact: The normal multi-tool comparison prompt can fail after 30 seconds even when MCP is healthy, and the resulting `TimeoutError` is reported as a harness failure that can be mistaken for an MCP transport error.
* Destination: rpi-implement.
* Smallest useful next action: Restrict the MCP timeout to connection/discovery or rename/separate it from a larger agent-run timeout; add a controlled test proving normal agent work is not classified as MCP timeout.

<!-- rpi:review id=RV-002 -->
### RV-002 [Medium]: Copilot Studio Code Interpreter prompt lacks an input binding

* Related scope: P02-T04.
* Evidence: `copilot-studio/README.md` asks the prompt tool to process repository metadata JSON but does not define a text input variable or insert that input into the prompt.
* Impact: The orchestrator has no documented parameter through which to pass MCP repository metadata, so the prompt tool may execute without candidate data and cannot reliably produce the required ranking/chart.
* Destination: rpi-implement.
* Smallest useful next action: Add a required text input such as `repository_metadata_json`, insert it into the prompt instructions, and record the expected output fields/file.

## Defects

* RV-001 -> rpi-implement.
* RV-002 -> rpi-implement.

## Routed Findings

| Finding | Destination | Owner or next action | Reason for route |
|---|---|---|---|
| RV-001 | rpi-implement | Separate connection and run timeout semantics | Local implementation defect |
| RV-002 | rpi-implement | Define and bind the Copilot Studio prompt input | Documentation/configuration defect |

Later implementation of a routed finding does not require another Review.

## Residual Work

* Credentialed AgentCore and Copilot Studio execution remains user-owned acceptance work because cloud accounts and tenants are unavailable; this is not a defect.

## Blockers and Remaining Work

* Blockers: none for the completed review.
* Remaining active work: none in the completed plan; RV-001 and RV-002 are routed later implementation work.

## Validation Evidence

| Command | Scope | Status | Summary |
|---|---|---|---|
| `python3 -m py_compile` | Python sources | Passed | LangChain and AgentCore compile |
| Fresh venv install/import | LangChain | Passed | Current MCP/LangChain APIs import |
| Scoring fixture | LangChain | Passed | Ranking JSON and chart produced |
| Missing-token/unreachable runs | LangChain | Passed | Both exit nonzero with structured failures |
| `dotnet build` | MAF | Passed | Zero warnings and errors on .NET 10 |
| Unreachable run | MAF | Passed | Nonzero structured `HttpRequestException` |
| Missing ARN run | AgentCore helper | Passed | Nonzero configuration failure |
| TOML/XML/link/secret/diff checks | Repository | Passed | All local integrity checks passed |
| AgentCore deploy/invoke | Managed cloud harness | Unavailable | Requires user AWS account and credentials |
| Copilot Studio setup/test | Managed cloud harness | Unavailable | Requires user Power Platform tenant and GitHub authorization |

## Outcome

* Outcome: Defects found.
* Outcome rationale: Execution completed and most requirements are credibly implemented, but two medium defects can distort the LangChain comparison and prevent the Copilot Studio analysis tool from receiving data.

## Closeout Routing Record

| Finding class | Destination | Owner or next action |
|---|---|---|
| Implementation defect | rpi-implement | Address RV-001 and RV-002 |
| Decision gap or invalid assumption | none | none |
| Material evidence gap | none | none |
| Non-blocking residual work | User cloud acceptance | Run AgentCore and Copilot Studio with owned credentials |

* Execution status: Complete.
* Outcome: Defects found.
* Validation coverage: All local checks passed; credentialed cloud checks unavailable.
* Blockers: none.
