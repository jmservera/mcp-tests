<!-- markdownlint-disable-file -->
# RPI Plan: Post-push MCP harness hardening

## Task Metadata

* Task ID: post-push-harness-hardening
* Task slug: post-push-harness-hardening
* Planning status: implementation-ready
* Plan date: 2026-09-13

## Executive Summary

Harden the Bedrock AgentCore invocation helper so SDK failures, malformed harness responses, and runtime stream errors produce deterministic structured diagnostics without obscuring AgentCore's native event semantics or introducing comparison-altering retries.

## User Decisions and Requirements

* Push the completed repository changes.
* Run another full RPI cycle.
* Preserve the original goal of comparing native MCP error behavior.

## Goals

* Validate AgentCore response and stream shapes before use.
* Produce consistent nonzero structured failures for call-time, stream-time, and runtime error events.
* Add credential-free regression tests.

## Scope and Non-Goals

### In Scope

* `bedrock-agentcore/invoke.py`
* AgentCore helper tests and README behavior notes.

### Non-Goals

* Automatic retries.
* Shared cross-harness exception abstractions.
* AWS deployment or credentialed invocation.

## Functional Requirements

* Missing configuration, SDK invocation exceptions, malformed responses/events, and `runtimeClientError` events produce structured stderr diagnostics and exit 1.
* Valid content deltas stream to stdout and exit 0.
* Unknown well-formed event types do not fail the invocation.

## Non-Functional Requirements

* Preserve native AgentCore event names and messages.
* Add no production dependency.
* Keep functions independently testable without AWS credentials.

## Acceptance Criteria

* Unit tests cover success, missing/mistyped stream, runtime client error, and iteration exception.
* Existing missing-ARN nonzero behavior remains.
* Python compilation, package install, links, secrets, and diff hygiene pass.

## Implementation Context Record

| Context item | Current artifact or record |
|---|---|
| Research | .copilot-tracking/research/2026-09-13/post-push-harness-hardening-research.md; executed, Ready |
| Plan | .copilot-tracking/plans/2026-09-13/post-push-harness-hardening-plan.md |
| Details | .copilot-tracking/details/2026-09-13/post-push-harness-hardening-phase-details.md |
| Critique | .copilot-tracking/reviews/plans/2026-09-13/post-push-harness-hardening-plan-critique.md |
| Changes record | .copilot-tracking/changes/2026-09-13/post-push-harness-hardening-changes.md |

## Sources

* .copilot-tracking/research/2026-09-13/post-push-harness-hardening-research.md

## Phase Checklist

<!-- rpi:phase id=P01 -->
### [x] P01: Harden AgentCore response handling

<!-- rpi:task id=P01-T01 -->
#### [x] P01-T01: Add structured invocation and stream validation

* Expected result: All locally observable failure boundaries return stable JSON diagnostics and correct exit status.
* Detail section: P01-T01 in the phase-details artifact.

<!-- rpi:task id=P01-T02 -->
#### [x] P01-T02: Add credential-free behavioral tests and documentation

* Expected result: Tests cover the accepted event contract and README explains diagnostics.
* Detail section: P01-T02 in the phase-details artifact.

<!-- rpi:phase id=P02 -->
### [x] P02: Validate and reconcile

<!-- rpi:task id=P02-T01 -->
#### [x] P02-T01: Run focused validation

* Expected result: Tests and repository checks pass with evidence recorded.
* Detail section: P02-T01 in the phase-details artifact.

## Dependencies

* Existing boto3 dependency only.

## Critique Disposition

| Critique run and finding | Disposition | Plan response or residual risk |
|---|---|---|
| Complete, Pass; no findings | accepted | Native-event preservation and credential-free test boundary are credible |

## Follow-Up Items

* None.

## Handoff

* Implementation artifact: .copilot-tracking/changes/2026-09-13/post-push-harness-hardening-changes.md
* Ready phase or task: Review.
* Blockers: none.
