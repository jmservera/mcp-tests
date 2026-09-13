# Copilot Studio error test matrix

Record observed values rather than expected or inferred values.

| Scenario | Setup | Connection saved? | Tool discovery | Agent-visible error | Retry/fallback observed | Final response continued? | Trace/diagnostic notes |
|---|---|---|---|---|---|---|---|
| Normal | GitHub endpoint + dynamic OAuth | | | | | | |
| Unauthorized | Revoke connection or deny consent | | | | | | |
| Unreachable | Temporary connection to `https://127.0.0.1:1/mcp/` | | | | | | |
| Tool validation | Ask for a repository search with invalid/over-complex arguments | | | | | | |
| Empty results | Use an improbable search query | | | | | | |
| Code execution | Ask for deterministic scoring and a bar chart | N/A | N/A | | | | |

For every scenario, capture the Copilot Studio test transcript and the Activity/diagnostic record if available. Do not paste access tokens or private repository data into this worksheet.

