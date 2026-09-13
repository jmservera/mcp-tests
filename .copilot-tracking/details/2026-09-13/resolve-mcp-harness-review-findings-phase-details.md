<!-- markdownlint-disable-file -->
# RPI Phase Details: Resolve MCP harness review findings

## Metadata

* Task ID: resolve-mcp-harness-review-findings
* Task slug: resolve-mcp-harness-review-findings
* Related plan: .copilot-tracking/plans/2026-09-13/resolve-mcp-harness-review-findings-plan.md
* Evidence sources: .copilot-tracking/reviews/logs/2026-09-13/mcp-error-harness-examples-review.md

## Phase Index

| Phase ID | Name | Status | Detail sections |
|---|---|---|---|
| P01 | Correct reviewed defects | complete | P01, P01-T01, P01-T02 |
| P02 | Validate and reconcile | complete | P02, P02-T01 |

<!-- rpi:phase id=P01 -->
## P01: Correct reviewed defects

### Context

The parent review found two independent medium defects with exact local corrections.

### Intent

Close both defects without altering the original architecture.

### Boundaries

* Included: Copilot Studio prompt input/output contract and LangChain timeout scope/error stage.
* Excluded: Cloud execution, retry-policy changes, and unrelated cleanup.

### Likely Targets

* `copilot-studio/README.md`
* `langchain-python/app.py`
* `langchain-python/.env.example`
* `langchain-python/README.md`

### Dependencies

* None.

### Validation Expectations

* Documentation explicitly binds the prompt input.
* Focused async tests prove discovery and run timeout independence.

### Completion Evidence

* RV-001 and RV-002 exact resolving evidence exists.

### Unresolved Items

* None.

<!-- rpi:task id=P01-T01 -->
### P01-T01: Bind Copilot Studio metadata input

#### Context

The current prompt references JSON but defines no parameter.

#### Intent

Add a required text parameter and explicit outputs.

#### Boundaries

* Included: Input name/type/description, prompt insertion, scored JSON and chart output.
* Excluded: Tenant-specific screenshots or export packages.

#### Likely Targets

* `copilot-studio/README.md`

#### Dependencies

* None.

#### Validation Expectations

* Key input/output terms appear in the setup steps.

#### Completion Evidence

* Guide is executable without inventing a parameter.

#### Unresolved Items

* None.

<!-- rpi:task id=P01-T02 -->
### P01-T02: Separate LangChain timeout scopes

#### Context

One outer timeout currently covers MCP discovery and the complete agent.

#### Intent

Use one discovery timeout and one larger agent-run timeout with stage-aware failures.

#### Boundaries

* Included: Timeout parsing, scoped contexts, stage tagging, environment docs.
* Excluded: Per-tool retry or model-provider timeout changes.

#### Likely Targets

* `langchain-python/app.py`
* `langchain-python/.env.example`
* `langchain-python/README.md`

#### Dependencies

* None.

#### Validation Expectations

* Discovery timeout can trigger before agent construction.
* Agent timeout can trigger after discovery without being labeled MCP discovery.

#### Completion Evidence

* Focused credential-free async tests pass.

#### Unresolved Items

* None.

<!-- rpi:phase id=P02 -->
## P02: Validate and reconcile

### Context

The fixes are small but affect diagnostic interpretation.

### Intent

Run targeted behavioral and repository integrity checks.

### Boundaries

* Included: Python compile/tests, documentation assertions, links, secrets, diff.
* Excluded: Live OAuth/cloud invocation.

### Likely Targets

* Changed production files and child tracking artifacts.

### Dependencies

* P01.

### Validation Expectations

* All focused checks pass.

### Completion Evidence

* Changes record contains commands and outcomes.

### Unresolved Items

* None.

<!-- rpi:task id=P02-T01 -->
### P02-T01: Run focused validation

#### Context

Exact resolving evidence is known from the parent review.

#### Intent

Demonstrate defect closure and no local regression.

#### Boundaries

* Included: Direct unit-style async probes and static checks.
* Excluded: Re-running unrelated MAF or AgentCore builds.

#### Likely Targets

* `langchain-python/app.py`
* `copilot-studio/README.md`

#### Dependencies

* P01 complete.

#### Validation Expectations

* Timeout stage assertions and documentation contract checks pass.

#### Completion Evidence

* Recorded passing commands.

#### Unresolved Items

* None.

## Candidate Validation Lock

* Test ownership: Implementation owns all focused local checks.
* Exact removals: One outer timeout scope.
* Maximum additions: One small test file if needed; no new production dependencies.
* Canonical targets: Existing LangChain and Copilot Studio files.
* Generated targets: none.
* Semantic coverage: Stage-specific timeout behavior and complete prompt binding.
* Regression coverage: Existing scoring, auth, endpoint, and native error behavior remain unchanged.
* Validation evidence: Compile, focused behavioral tests, doc assertions, links, secrets, diff.
