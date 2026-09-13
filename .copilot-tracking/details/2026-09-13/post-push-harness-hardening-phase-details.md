<!-- markdownlint-disable-file -->
# RPI Phase Details: Post-push MCP harness hardening

## Metadata

* Task ID: post-push-harness-hardening
* Related plan: .copilot-tracking/plans/2026-09-13/post-push-harness-hardening-plan.md
* Research: .copilot-tracking/research/2026-09-13/post-push-harness-hardening-research.md

## Phase Index

| Phase ID | Name | Status |
|---|---|---|
| P01 | Harden AgentCore response handling | complete |
| P02 | Validate and reconcile | complete |

<!-- rpi:phase id=P01 -->
## P01: Harden AgentCore response handling

### Context and Intent

The helper currently validates only one known stream event and assumes the SDK call and response shape succeed. Add a narrow caller boundary without changing managed-harness orchestration.

### Boundaries

* Include response shape, event shape, call/iteration errors, and stable diagnostics.
* Exclude retries and normalization across harnesses.

<!-- rpi:task id=P01-T01 -->
### P01-T01: Add structured invocation and stream validation

* Extract a JSON failure emitter and response consumer.
* Require a mapping response with a non-string iterable `stream`.
* Preserve `runtimeClientError` as the reported native event.
* Treat malformed known events as failures.
* Ignore unknown mapping events for forward compatibility.
* Catch ordinary SDK and event-stream exceptions at the host boundary.

<!-- rpi:task id=P01-T02 -->
### P01-T02: Add credential-free behavioral tests and documentation

* Use standard-library unittest and fake iterable responses.
* Cover successful text, malformed stream, runtime error, and iteration failure.
* Document the structured failure envelope and lack of helper retries.

<!-- rpi:phase id=P02 -->
## P02: Validate and reconcile

<!-- rpi:task id=P02-T01 -->
### P02-T01: Run focused validation

* Run unit tests and Python compilation.
* Install the package in a fresh temporary environment.
* Verify missing ARN remains nonzero and structured.
* Run link, secret, whitespace, and git diff checks.

## Candidate Validation Lock

* Test ownership: Implementation.
* Exact removals: Direct unchecked `response[\"stream\"]` loop.
* Maximum additions: One test module and small helper functions; no dependencies.
* Canonical targets: `bedrock-agentcore/invoke.py`, README, tests.
* Generated targets: none.
* Semantic coverage: Native runtime errors and malformed host responses.
* Regression coverage: Successful streamed text and missing configuration.
