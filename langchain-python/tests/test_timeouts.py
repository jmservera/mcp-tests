import asyncio
import json
import os
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch
from uuid import uuid4

from app import (
    HarnessStageTimeout,
    create_model,
    discover_mcp_tools,
    invoke_agent,
    load_environment,
)
from telemetry import AgentTelemetry, enabled


class FakeAdapter:
    def __init__(self, enter_delay=0, list_delay=0):
        self.enter_delay = enter_delay
        self.list_delay = list_delay
        self.exited = False

    async def __aenter__(self):
        await asyncio.sleep(self.enter_delay)
        return self

    async def list_tools(self):
        await asyncio.sleep(self.list_delay)
        return [object()]

    async def __aexit__(self, _type, _value, _traceback):
        self.exited = True


class FakeAgent:
    def __init__(self, delay):
        self.delay = delay

    async def ainvoke(self, _input, config=None):
        await asyncio.sleep(self.delay)
        return {"messages": []}


class TimeoutBoundaryTests(unittest.IsolatedAsyncioTestCase):
    def test_telemetry_is_enabled_by_default_and_accepts_truthy_values(self):
        with patch.dict(os.environ, {}, clear=True):
            self.assertTrue(enabled("TELEMETRY_ENABLED", True))
        with patch.dict(
            os.environ, {"TELEMETRY_INCLUDE_CONTENT": "true"}, clear=True
        ):
            self.assertTrue(enabled("TELEMETRY_INCLUDE_CONTENT", False))

    def test_azure_openai_model_uses_configured_deployment(self):
        environment = {
            "AZURE_OPENAI_ENDPOINT": "https://example.openai.azure.com/",
            "AZURE_OPENAI_DEPLOYMENT_NAME": "test-deployment",
            "AZURE_OPENAI_API_VERSION": "2024-10-21",
        }
        with patch.dict(os.environ, environment, clear=True):
            model = create_model()
        self.assertEqual("test-deployment", model.deployment_name)
        self.assertEqual("2024-10-21", model.openai_api_version)
        self.assertTrue(callable(model.azure_ad_token_provider))

    def test_dotenv_loads_without_overriding_host_environment(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / ".env"
            path.write_text(
                "AZURE_OPENAI_ENDPOINT=https://dotenv.openai.azure.com/\n"
                "AZURE_OPENAI_DEPLOYMENT_NAME=dotenv-deployment\n",
                encoding="utf-8",
            )
            with patch.dict(
                os.environ,
                {"AZURE_OPENAI_ENDPOINT": "https://host.openai.azure.com/"},
                clear=True,
            ):
                load_environment(path)
                self.assertEqual(
                    "https://host.openai.azure.com/",
                    os.environ["AZURE_OPENAI_ENDPOINT"],
                )
                self.assertEqual(
                    "dotenv-deployment",
                    os.environ["AZURE_OPENAI_DEPLOYMENT_NAME"],
                )

    def test_telemetry_records_structured_tool_error_when_enabled(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "telemetry.jsonl"
            with patch.dict(
                os.environ,
                {
                    "TELEMETRY_FILE": str(path),
                    "TELEMETRY_INCLUDE_CONTENT": "true",
                },
                clear=True,
            ):
                telemetry = AgentTelemetry({"search_repositories"})
                with telemetry.tracer.start_as_current_span("invoke.agent"):
                    failed_run_id = uuid4()
                    telemetry.handler.on_tool_start(
                        {"name": "search_repositories"},
                        '{"query":"test"}',
                        run_id=failed_run_id,
                    )
                    telemetry.handler.on_tool_end(
                        SimpleNamespace(
                            status="error",
                            content={"code": "RATE_LIMITED", "retryable": True},
                        ),
                        run_id=failed_run_id,
                    )
                    recovery_run_id = uuid4()
                    telemetry.handler.on_tool_start(
                        {"name": "search_repositories"},
                        '{"query":"test fallback"}',
                        run_id=recovery_run_id,
                    )
                    telemetry.handler.on_tool_end(
                        SimpleNamespace(status="success", content={"items": []}),
                        run_id=recovery_run_id,
                    )
                telemetry.shutdown()

            records = [
                json.loads(line)
                for line in path.read_text(encoding="utf-8").splitlines()
            ]
            failed, recovered = records[:2]
            self.assertEqual("execute_tool.search_repositories", failed["name"])
            self.assertEqual("ERROR", failed["status"])
            self.assertEqual(
                "error", failed["attributes"]["gen_ai.tool.result.status"]
            )
            self.assertIn(
                "RATE_LIMITED",
                failed["attributes"]["gen_ai.tool.call.result"],
            )
            self.assertEqual("UNSET", recovered["status"])
            self.assertEqual(failed["trace_id"], recovered["trace_id"])
            self.assertEqual(failed["parent_span_id"], recovered["parent_span_id"])

    async def test_discovery_timeout_has_mcp_stage(self):
        with self.assertRaises(HarnessStageTimeout) as raised:
            await discover_mcp_tools(FakeAdapter(enter_delay=0.05), 0.01)
        self.assertEqual("mcp.discovery", raised.exception.stage)

    async def test_agent_work_is_not_limited_by_discovery_timeout(self):
        adapter = FakeAdapter()
        await discover_mcp_tools(adapter, 0.01)
        result = await invoke_agent(FakeAgent(delay=0.03), "prompt", 0.1)
        self.assertEqual({"messages": []}, result)

    async def test_agent_timeout_has_agent_stage(self):
        with self.assertRaises(HarnessStageTimeout) as raised:
            await invoke_agent(FakeAgent(delay=0.05), "prompt", 0.01)
        self.assertEqual("agent.run", raised.exception.stage)


if __name__ == "__main__":
    unittest.main()
