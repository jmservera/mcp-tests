<!-- markdownlint-disable-file -->
# RPI Plan Critique: MCP error harness examples

## Metadata

* Task ID: mcp-error-harness-examples
* Critique date: 2026-09-13
* Plan: .copilot-tracking/plans/2026-09-13/mcp-error-harness-examples-plan.md
* Phase details: .copilot-tracking/details/2026-09-13/mcp-error-harness-examples-phase-details.md
* Critique execution status: Complete

## Inputs and Criterion Boundary

* Task context and caller requirements: Four minimal examples using one supplied instruction set, GitHub Copilot MCP, and observable MCP error behavior.
* Research and evidence considered: .copilot-tracking/research/2026-09-13/mcp-error-harness-examples-research.md, mcp-policy.xml, user request.
* Decisions, dependencies, and acceptance criteria considered: Four harnesses, managed AgentCore harness, externalized auth, invalid-endpoint tests, local versus cloud validation ownership.
* Assessment boundary: Credibility of the implementation plan from supplied evidence; no additional API research or cloud execution.

## Coverage Assessment

| Requirement, research, phase, or task ID | Coverage | Evidence or concern |
|---|---|---|
| Shared instruction set | Partial | Prompt declares Code Interpreter as available, but only AgentCore explicitly plans that tool |
| P02-T01 LangChain | Partial | MCP integration is covered; Python analysis/chart capability is not |
| P02-T02 MAF | Partial | MCP integration is covered; hosted Code Interpreter capability is not |
| P02-T03 AgentCore | Partial | Tool types are covered, but a hand-authored generated `harness.json` schema is not supported by the research evidence |
| P02-T04 Copilot Studio | Partial | MCP onboarding is covered; Code Interpreter/tool availability setup is not |
| P03 validation | Covered | Local versus credentialed cloud validation is separated honestly |

## Verdict

* Verdict: Revise
* Rationale: The plan is close to implementation-ready, but it does not make the supplied “Code Interpreter” capability truthful across all four examples and overstates the ability to validate a hand-authored AgentCore generated configuration.

## Findings

<!-- rpi:critique id=PC-001 -->
### PC-001 [High]: Code Interpreter availability is inconsistent with the canonical prompt

* Related IDs: User requirement to use supplied instructions, P02-T01, P02-T02, P02-T03, P02-T04.
* Evidence: User request and .copilot-tracking/plans/2026-09-13/mcp-error-harness-examples-plan.md.
* Concern: The prompt tells the agent that Code Interpreter is available, but the plan only provisions it for AgentCore.
* Impact: Three examples could fail for reasons unrelated to MCP behavior, invalidating the comparison and preventing required ranking/chart output.
* Smallest useful change: Add the simplest native code-analysis/interpreter tool to LangChain, MAF, and Copilot Studio, or explicitly create harness-specific prompt variants that truthfully describe available tools while preserving all other instructions.
* Action owner: planning parent.
* Exact resolving evidence: Plan and phase details state the selected Code Interpreter implementation or truthful prompt variation for every harness, with matching acceptance criteria.
* Decision route: direct planner correction; the user explicitly required the supplied instructions and no divergent product choice is needed.

<!-- rpi:critique id=PC-002 -->
### PC-002 [Medium]: AgentCore generated configuration is treated as a canonical hand-authored target without schema evidence

* Related IDs: P02-T03, AgentCore acceptance criterion, Candidate Validation Lock.
* Evidence: Research W6-W7 and .copilot-tracking/details/2026-09-13/mcp-error-harness-examples-phase-details.md.
* Concern: Official evidence documents CLI generation and tool object examples, but not the complete project-local `harness.json` schema the plan proposes to author and validate.
* Impact: A syntactically valid JSON file could still be rejected by AgentCore, undermining the “working example” claim.
* Smallest useful change: Make documented AgentCore CLI commands and system prompt the canonical setup, and either omit generated files or label any JSON as a non-canonical illustrative fragment. Validate with `agentcore validate` only when the CLI is available.
* Action owner: planning parent.
* Exact resolving evidence: Plan no longer claims schema-valid hand-authored generated files; AgentCore targets and acceptance criteria use CLI scaffolding plus documented command inputs.
* Decision route: direct planner correction.

## Strengths and Residual Risk

* The plan correctly preserves native MCP failure surfaces, externalizes credentials, and separates local checks from cloud acceptance.
* Residual risk remains that live OAuth behavior cannot be observed without user-owned credentials and tenants; this is already explicit and acceptable.

## Questions or Blocking Evidence Gaps

* None. Both findings are planner-owned corrections.

## Limitations

* Exact Code Interpreter API names for MAF and Copilot Studio require implementation-time verification from the already identified official documentation family.

## Recommended Next Action

* Highest-impact finding: PC-001.
* Action owner: planning parent.
* Smallest next action: Revise all four task details and acceptance criteria for truthful Code Interpreter availability, then remove the unsupported AgentCore generated-config claim.
* User response required: no.
