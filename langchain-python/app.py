import argparse
import asyncio
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

import matplotlib
import pandas as pd
from azure.identity import DefaultAzureCredential, get_bearer_token_provider
from dotenv import load_dotenv
from fastmcp.client import Client
from fastmcp.client.transports import StreamableHttpTransport
from langchain.agents import create_agent
from langchain.mcp import MCPAdapter
from langchain.tools import tool
from langchain_openai import AzureChatOpenAI

from telemetry import AgentTelemetry, add_conversation_events


DEFAULT_PROMPT = (
    "After identifying my username, make the first search_repositories call with this query verbatim. Do not split or simplify it:"
    "user:jmservera (books OR library OR catalog OR doc OR docx OR pdf OR html OR epub OR markdown OR jpeg OR tiff)"
    "When the recoverable validation error is returned, follow its instructions and retry using smaller searches. Then rank the repositories and open the requested Windows desktop client PR."
)


class HarnessStageTimeout(TimeoutError):
    def __init__(self, stage: str, seconds: float):
        self.stage = stage
        super().__init__(f"{stage} timed out after {seconds:g} seconds.")


def required(name: str) -> str:
    value = os.getenv(name)
    if not value:
        raise ValueError(f"{name} is required.")
    return value


def load_instructions() -> str:
    return (Path(__file__).parent.parent / "agent-instructions.md").read_text(
        encoding="utf-8"
    )


def load_environment(path: Path | None = None) -> None:
    load_dotenv(path or Path(__file__).with_name(".env"), override=False)


def create_mcp_client() -> Client:
    url = os.getenv("MCP_SERVER_URL", "https://api.githubcopilot.com/mcp/")
    auth_mode = os.getenv("MCP_AUTH_MODE", "bearer").lower()
    if auth_mode == "oauth":
        auth = "oauth"
    elif auth_mode == "bearer":
        auth = required("GITHUB_MCP_TOKEN")
    else:
        raise ValueError("MCP_AUTH_MODE must be 'bearer' or 'oauth'.")
    transport = StreamableHttpTransport(
        url,
        auth=auth,
        headers={"X-MCP-Readonly": "true", "X-MCP-Toolsets": "repos"},
    )
    return Client(transport)


def create_model() -> AzureChatOpenAI:
    credential = DefaultAzureCredential(
        exclude_environment_credential=True,
        managed_identity_client_id=os.getenv("AZURE_CLIENT_ID") or None,
    )
    return AzureChatOpenAI(
        azure_deployment=required("AZURE_OPENAI_DEPLOYMENT_NAME"),
        azure_endpoint=required("AZURE_OPENAI_ENDPOINT"),
        azure_ad_token_provider=get_bearer_token_provider(
            credential,
            "https://cognitiveservices.azure.com/.default",
        ),
        api_version=os.getenv("AZURE_OPENAI_API_VERSION", "2024-10-21"),
    )


def timeout_seconds(name: str, default: str) -> float:
    value = float(os.getenv(name, default))
    if value <= 0:
        raise ValueError(f"{name} must be greater than zero.")
    return value


async def discover_mcp_tools(adapter: MCPAdapter, timeout: float) -> list:
    entered = False
    try:
        async with asyncio.timeout(timeout):
            await adapter.__aenter__()
            entered = True
            return await adapter.list_tools()
    except TimeoutError as exc:
        if entered:
            await adapter.__aexit__(type(exc), exc, exc.__traceback__)
        raise HarnessStageTimeout("mcp.discovery", timeout) from exc
    except BaseException as exc:
        if entered:
            await adapter.__aexit__(type(exc), exc, exc.__traceback__)
        raise


async def invoke_agent(agent, prompt: str, timeout: float, callbacks=None):
    try:
        async with asyncio.timeout(timeout):
            return await agent.ainvoke(
                {"messages": [{"role": "user", "content": prompt}]},
                config={"callbacks": callbacks or []},
            )
    except TimeoutError as exc:
        raise HarnessStageTimeout("agent.run", timeout) from exc


@tool
def code_interpreter(repository_metadata_json: str) -> str:
    """Score repository metadata deterministically and save a ranking chart.

    Input is a JSON array. Each item must contain repository, stars, forks,
    last_updated, relevance, and maintenance_quality. The final two fields are
    numeric values from 0 through 1 based on the agent's cited evidence.
    """
    records = json.loads(repository_metadata_json)
    required_fields = {
        "repository",
        "stars",
        "forks",
        "last_updated",
        "relevance",
        "maintenance_quality",
    }
    if not isinstance(records, list) or not records:
        raise ValueError("Expected a non-empty JSON array.")
    if any(
        not isinstance(item, dict) or not required_fields <= item.keys()
        for item in records
    ):
        raise ValueError(f"Each item must contain: {sorted(required_fields)}")

    frame = pd.DataFrame(records)
    for column in ("stars", "forks", "relevance", "maintenance_quality"):
        frame[column] = pd.to_numeric(frame[column], errors="raise")
    if not frame["relevance"].between(0, 1).all():
        raise ValueError("relevance values must be between 0 and 1.")
    if not frame["maintenance_quality"].between(0, 1).all():
        raise ValueError("maintenance_quality values must be between 0 and 1.")
    frame["last_updated"] = pd.to_datetime(
        frame["last_updated"], utc=True, errors="raise"
    )

    def normalize(series: pd.Series) -> pd.Series:
        minimum, maximum = float(series.min()), float(series.max())
        if minimum == maximum:
            return pd.Series(1.0, index=series.index)
        return (series - minimum) / (maximum - minimum)

    frame["stars_normalized"] = normalize(frame["stars"])
    frame["forks_normalized"] = normalize(frame["forks"])
    frame["activity_normalized"] = normalize(
        frame["last_updated"].map(lambda value: value.timestamp())
    )
    frame["score"] = (
        0.40 * frame["relevance"]
        + 0.25 * frame["stars_normalized"]
        + 0.15 * frame["forks_normalized"]
        + 0.15 * frame["activity_normalized"]
        + 0.05 * frame["maintenance_quality"]
    )
    frame = frame.sort_values(["score", "repository"], ascending=[False, True])

    matplotlib.use("Agg")
    axis = frame.plot.barh(
        x="repository", y="score", legend=False, title="Repository ranking"
    )
    axis.invert_yaxis()
    axis.figure.tight_layout()
    chart_path = Path("artifacts") / "repository-ranking.png"
    chart_path.parent.mkdir(exist_ok=True)
    axis.figure.savefig(chart_path)

    output = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "formula": (
            "0.40 relevance + 0.25 stars + 0.15 forks + "
            "0.15 activity + 0.05 maintenance"
        ),
        "normalization_ranges": {
            "stars": [int(frame["stars"].min()), int(frame["stars"].max())],
            "forks": [int(frame["forks"].min()), int(frame["forks"].max())],
            "last_updated": [
                frame["last_updated"].min().isoformat(),
                frame["last_updated"].max().isoformat(),
            ],
        },
        "library_versions": {
            "python": sys.version.split()[0],
            "pandas": pd.__version__,
            "matplotlib": matplotlib.__version__,
        },
        "chart": str(chart_path),
        "ranked": json.loads(
            frame.to_json(orient="records", date_format="iso")
        ),
    }
    return json.dumps(output)


async def run(prompt: str) -> None:
    mcp_timeout = timeout_seconds("MCP_TIMEOUT_SECONDS", "30")
    agent_timeout = timeout_seconds("AGENT_RUN_TIMEOUT_SECONDS", "180")
    model = create_model()
    print(json.dumps({"event": "mcp.connect", "url": os.getenv("MCP_SERVER_URL", "default")}))

    adapter = MCPAdapter(create_mcp_client())
    entered = False
    telemetry = None
    try:
        mcp_tools = await discover_mcp_tools(adapter, mcp_timeout)
        entered = True
        if not mcp_tools or any(not getattr(tool, "name", None) for tool in mcp_tools):
            raise RuntimeError("MCP tool discovery returned an invalid or empty tool list.")

        print(
            json.dumps(
                {
                    "event": "mcp.tools",
                    "count": len(mcp_tools),
                    "names": [tool.name for tool in mcp_tools],
                }
            )
        )
        agent = create_agent(
            model=model,
            tools=[*mcp_tools, code_interpreter],
            system_prompt=load_instructions(),
        )
        if os.getenv("TELEMETRY_ENABLED", "false").lower() == "true":
            print(json.dumps({"event": "telemetry.enabled"}))
            telemetry = AgentTelemetry({tool.name for tool in mcp_tools})
            with telemetry.tracer.start_as_current_span("invoke.agent") as span:
                span.set_attribute("gen_ai.operation.name", "invoke_agent")
                span.set_attribute(
                    "gen_ai.agent.name", "GitHubRepositoryDiscovery"
                )
                result = await invoke_agent(
                    agent, prompt, agent_timeout, [telemetry.handler]
                )
                add_conversation_events(
                    span, result["messages"], telemetry.include_content
                )
        else:
            result = await invoke_agent(agent, prompt, agent_timeout)
        print(result["messages"][-1].content)
    finally:
        if telemetry is not None:
            telemetry.shutdown()
        if entered:
            await adapter.__aexit__(None, None, None)


def main() -> int:
    load_environment()
    parser = argparse.ArgumentParser()
    parser.add_argument("prompt", nargs="?", default=DEFAULT_PROMPT)
    args = parser.parse_args()
    try:
        asyncio.run(run(args.prompt))
    except Exception as exc:
        print(
            json.dumps(
                {
                    "event": "harness.failure",
                    "stage": getattr(exc, "stage", "harness"),
                    "type": type(exc).__name__,
                    "message": str(exc),
                }
            ),
            file=sys.stderr,
        )
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
