<!-- markdownlint-disable-file -->
# Implementation Changes: Post-push MCP harness hardening

## Metadata

* Task ID: post-push-harness-hardening
* Plan: .copilot-tracking/plans/2026-09-13/post-push-harness-hardening-plan.md
* Implementation status: Complete
* Review readiness: Ready

## Structured AgentCore response handling (P01-T01)

Refactored `bedrock-agentcore/invoke.py` into testable invocation and stream-consumption boundaries. The helper now:

* emits JSON failures with `event`, `stage`, `type`, and `message`;
* validates the top-level response, stream iterability, and known event payload datatypes;
* preserves `runtimeClientError` as the native stage and retains its message/type;
* reports SDK call, client creation, malformed response, malformed event, and lazy stream failures distinctly;
* ignores unknown mapping events for forward compatibility;
* adds no retry behavior.

## Tests and documentation (P01-T02)

Added seven standard-library unit tests covering successful content, future unknown events, absent and mistyped streams, malformed events, native runtime errors, SDK invocation errors, and lazy stream exceptions. Updated the README with the diagnostic contract and explicit no-retry behavior.

## Validation (P02-T01)

| Check | Result |
|---|---|
| Fresh editable package install | Passed |
| Unit tests | 7 passed |
| Python compilation | Passed |
| Missing ARN subprocess | Passed; structured configuration failure and exit 1 |
| Relative Markdown links | Passed |
| Secret-pattern scan | Passed |
| Changed-file whitespace | Passed |
| `git diff --check` | Passed |

## Implementation Decisions

* Unknown mapping events are ignored rather than rejected, preserving compatibility with future AgentCore event variants.
* Known event types are validated strictly because malformed known payloads cannot be interpreted reliably.
* Retries remain the managed harness's responsibility so comparison observations are not distorted.

## Blockers

* None.

## Remaining Work

* None in the active plan.

## Follow-Up Items

* None.

