<!-- markdownlint-disable-file -->
# Research: Post-push MCP harness hardening

## Research Brief

* Topic: Highest-value remaining local reliability gap after pushing the four MCP harness examples.
* Purpose: Select one bounded improvement for a new full RPI lifecycle.
* Audience/use: Implementation planning and post-push hardening.
* Scope: Existing local source, documentation, and credential-free validation.
* Non-goals: Cloud provisioning, changing native harness semantics, or reopening closed RV-001/RV-002.
* Output mode: convergence.
* Research posture: focused, selected because the repository and comparison boundary are known.
* Interaction: skipped because the user explicitly requested another cycle and the repository provides a bounded evidence source.

## Extensions and Participation

* Platform safety and repository instructions: selected.
* RPI research protocol: selected.
* External research: skipped; the current code and already-reviewed platform contract are sufficient.
* Delegation: skipped; this is one tightly coupled, low-volume trace.

## Questions

1. Which remaining local behavior most threatens a trustworthy MCP-error comparison?
2. What smallest correction preserves AgentCore's native error surface?
3. Can the correction be verified without AWS credentials?

## Cycle 1

### Wider Wave

Reviewed the root comparison contract and each remaining harness's caller-facing error boundary. LangChain and MAF emit structured host failures, while AgentCore handles only `runtimeClientError` stream members and assumes a valid top-level `stream`.

### Deeper Wave

* C1 — `bedrock-agentcore/invoke.py:28`: `invoke_harness` exceptions are not converted to a stable nonzero structured failure.
* C2 — `bedrock-agentcore/invoke.py:35`: direct `response["stream"]` access does not validate the required field or datatype.
* C3 — `bedrock-agentcore/invoke.py:40-45`: a `runtimeClientError` is recognized, but malformed error payloads and unknown event shapes are not recorded.
* C4 — `agent-instructions.md:16`: external responses must be validated for expected fields and datatypes.
* C5 — `README.md` comparison worksheet requires logs sufficient to reconstruct the failure sequence.
* C6 — Existing missing-ARN behavior exits nonzero, but produces plain text rather than the same structured failure envelope as streamed runtime failures.

### Contrarian Wave

A broad shared exception abstraction would erase the native behavior this repository is intended to compare. The correction should therefore normalize only the Python helper's caller-facing diagnostics while preserving original AgentCore event types and messages. Automatic retries in the helper would also confound observations of managed-harness retry behavior, so they should not be added.

## Findings

### F1: AgentCore helper response assumptions can hide the actual failure boundary

Evidence: C1-C6.

If the AWS SDK call fails before a stream is returned, or the response omits/mistypes `stream`, the helper raises an unstructured traceback or `KeyError`. That makes AgentCore harder to compare with the other executable harnesses and contradicts the shared output-validation requirement.

### F2: A small stream-consumer boundary is sufficient

Evidence: C1-C3.

Extracting response validation and stream consumption into testable functions can preserve `runtimeClientError` event content, add explicit malformed-response diagnostics, and return a deterministic exit code without credentials.

## Alternatives

* Add retries around `invoke_harness`: rejected because it would obscure whether retries belong to AgentCore or the comparison helper.
* Build a common cross-harness exception model: rejected because native error surfaces are an explicit comparison requirement.
* Document the limitation only: rejected because the helper can be corrected and tested locally with little complexity.

## Decisions and Recommendation

Implement structured AgentCore invocation and stream-response validation, retain native event names/messages, and add credential-free unit tests using fake responses and clients.

## Risks

* Event-stream objects are lazy; tests must cover iteration-time exceptions as well as call-time exceptions.
* Validation must not reject future unknown event members; unknown events should be logged and ignored rather than treated as fatal unless the event itself is malformed.

## Research Disposition

* Disposition: executed.
* Planning Readiness: Ready.
* Gates: Scope is bounded, exact source targets and acceptance behavior are known, and no user decision is required.
* Re-entry decision: Not required; the focused three-wave cycle saturated the material local evidence.

