import asyncio
import unittest

from app import HarnessStageTimeout, discover_mcp_tools, invoke_agent


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

    async def ainvoke(self, _input):
        await asyncio.sleep(self.delay)
        return {"messages": []}


class TimeoutBoundaryTests(unittest.IsolatedAsyncioTestCase):
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
