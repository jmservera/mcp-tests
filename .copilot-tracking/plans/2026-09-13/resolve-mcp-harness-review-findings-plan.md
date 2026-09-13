<!-- markdownlint-disable-file -->
# RPI Plan: Resolve MCP harness review findings

## Task Metadata

* Task ID: resolve-mcp-harness-review-findings
* Task slug: resolve-mcp-harness-review-findings
* Planning status: implementation-ready
* Plan date: 2026-09-13
* Phase details: .copilot-tracking/details/2026-09-13/resolve-mcp-harness-review-findings-phase-details.md
* Plan critique: .copilot-tracking/reviews/plans/2026-09-13/resolve-mcp-harness-review-findings-plan-critique.md

## Executive Summary

Resolve both defects from the parent lifecycle's review: make the Copilot Studio Code Interpreter tool accept repository metadata explicitly, and separate LangChain MCP connection/discovery timing from the full agent execution timeout. These are surgical corrections that preserve the four-harness comparison.

### User Decisions and Requirements Highlights

* Run another complete RPI lifecycle.
* Address the evidence-backed follow-ups from the prior review.

### What You May Not Know

* The prior review is adequate research evidence: each defect includes exact source evidence, impact, and smallest useful correction.

### Unresolved Decisions or Blockers

* None.

## User Decisions and Requirements

* Run another full RPI cycle from the completed parent task.
* Preserve the original comparison scope and native error semantics.
* Resolve RV-002 and RV-001 without adding unrelated features.

## Goals

* Make the Copilot Studio analysis tool invocation reproducible.
* Prevent LangChain's MCP timeout label from covering healthy long-running agent work.

## Scope and Non-Goals

### In Scope

* `copilot-studio/README.md` input and output configuration.
* `langchain-python/app.py`, `.env.example`, and README timeout behavior.
* Focused validation of both corrections.

### Non-Goals

* Cloud deployment or credentialed service execution.
* Changing retry policy, ranking formula, authentication, or other harnesses.

## Functional Requirements

* Copilot Studio defines a required `repository_metadata_json` text input and embeds it into the Code Interpreter prompt.
  * Observable acceptance criteria: The setup steps name the input, its type, prompt insertion, and expected JSON/file outputs.
* LangChain uses distinct MCP discovery and overall agent-run timeout settings.
  * Observable acceptance criteria: `MCP_TIMEOUT_SECONDS` only covers adapter connection/tool discovery, and `AGENT_TIMEOUT_SECONDS` independently covers agent invocation.
* Timeout failures are classified by stage.
  * Observable acceptance criteria: Structured failure events identify `mcp.discovery` or `agent.run`.

## Non-Functional Requirements

* Changes remain surgical and backward compatible.
  * Objective threshold or evaluation condition: Defaults preserve a 30-second MCP discovery limit and provide a larger finite agent limit.
  * Observable acceptance criteria: Existing endpoint/auth behavior and scoring tool are unchanged.
* Validation remains deterministic.
  * Objective threshold or evaluation condition: Focused tests simulate discovery and agent timeout boundaries without network/model credentials.
  * Observable acceptance criteria: Tests prove one timeout does not encompass the other.

## Acceptance Criteria

* Copilot Studio setup has a complete input/output contract.
* LangChain reports stage-specific timeout failures and retains nonzero exit behavior.
* Python compile, focused timeout tests, link checks, secret scan, and diff checks pass.
* The parent review findings are both closed by exact evidence.

## Implementation Context Record

| Context item | Current artifact or record |
|---|---|
| Plan | .copilot-tracking/plans/2026-09-13/resolve-mcp-harness-review-findings-plan.md |
| Phase details | .copilot-tracking/details/2026-09-13/resolve-mcp-harness-review-findings-phase-details.md |
| Latest critique | .copilot-tracking/reviews/plans/2026-09-13/resolve-mcp-harness-review-findings-plan-critique.md; Complete, Pass |
| Relevant research | Satisfied-and-skipped using .copilot-tracking/reviews/logs/2026-09-13/mcp-error-harness-examples-review.md |
| Changes-record role | .copilot-tracking/changes/2026-09-13/resolve-mcp-harness-review-findings-changes.md |
| Planning execution and readiness | Complete and implementation-ready |
| Continuation context | Active rpi-quick parent continues automatically |

## Sources

* .copilot-tracking/reviews/logs/2026-09-13/mcp-error-harness-examples-review.md: RV-001 and RV-002 evidence and routes.
* Existing LangChain and Copilot Studio source files: Current defect locations.

## Phase Checklist

<!-- rpi:phase id=P01 -->
### [x] P01: Correct reviewed defects

* Intent: Apply both bounded corrections.
* Dependencies: Research satisfied-and-skipped; critique gate.

<!-- rpi:task id=P01-T01 -->
#### [x] P01-T01: Bind Copilot Studio metadata input

* Requirement and evidence: RV-002.
* Expected result: Required text input, prompt binding, and output contract are documented.
* Detail section: P01-T01 in .copilot-tracking/details/2026-09-13/resolve-mcp-harness-review-findings-phase-details.md

<!-- rpi:task id=P01-T02 -->
#### [x] P01-T02: Separate LangChain timeout scopes

* Requirement and evidence: RV-001.
* Expected result: MCP discovery and agent execution have separate limits and error stages.
* Detail section: P01-T02 in .copilot-tracking/details/2026-09-13/resolve-mcp-harness-review-findings-phase-details.md

<!-- rpi:phase id=P02 -->
### [x] P02: Validate and reconcile

* Intent: Prove both review defects are resolved without regression.
* Dependencies: P01.

<!-- rpi:task id=P02-T01 -->
#### [x] P02-T01: Run focused validation

* Requirement and evidence: Parent review exact resolving evidence.
* Expected result: Focused tests and repository checks pass.
* Detail section: P02-T01 in .copilot-tracking/details/2026-09-13/resolve-mcp-harness-review-findings-phase-details.md

## Dependencies

* Existing installed LangChain validation environment or project dependencies.

## Critique Disposition

| Critique run and finding | Disposition | Plan response or residual risk |
|---|---|---|
| Complete, Pass; no findings | accepted | Candidate is credible for implementation; residual cloud execution risk remains explicitly out of scope |

## Follow-Up Items

* None

## Handoff

* Implementation artifact: .copilot-tracking/changes/2026-09-13/resolve-mcp-harness-review-findings-changes.md
* Ready phase or task: Review
* Remaining provisional question or blocker: none
