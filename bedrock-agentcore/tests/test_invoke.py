import contextlib
import io
import json
import unittest

from invoke import consume_response, invoke


class FakeClient:
    def __init__(self, response=None, error=None):
        self.response = response
        self.error = error

    def invoke_harness(self, **_kwargs):
        if self.error:
            raise self.error
        return self.response


class FailingStream:
    def __iter__(self):
        yield {"contentBlockDelta": {"delta": {"text": "partial"}}}
        raise RuntimeError("stream disconnected")


class InvokeTests(unittest.TestCase):
    def capture(self, function, *args):
        stdout = io.StringIO()
        stderr = io.StringIO()
        with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
            status = function(*args)
        failures = [
            json.loads(line)
            for line in stderr.getvalue().splitlines()
            if line.strip()
        ]
        return status, stdout.getvalue(), failures

    def test_successful_content_stream(self):
        response = {
            "stream": [
                {"contentBlockDelta": {"delta": {"text": "hello"}}},
                {"futureEvent": {"value": 1}},
            ]
        }
        status, stdout, failures = self.capture(consume_response, response)
        self.assertEqual(0, status)
        self.assertEqual("hello\n", stdout)
        self.assertEqual([], failures)

    def test_missing_stream_is_structured_failure(self):
        status, _, failures = self.capture(consume_response, {})
        self.assertEqual(1, status)
        self.assertEqual("harness.response", failures[0]["stage"])
        self.assertEqual("InvalidResponse", failures[0]["type"])

    def test_mistyped_stream_is_structured_failure(self):
        status, _, failures = self.capture(
            consume_response, {"stream": {"not": "an event stream"}}
        )
        self.assertEqual(1, status)
        self.assertEqual("harness.response", failures[0]["stage"])

    def test_malformed_event_is_structured_failure(self):
        status, _, failures = self.capture(consume_response, {"stream": ["bad"]})
        self.assertEqual(1, status)
        self.assertEqual("harness.stream", failures[0]["stage"])
        self.assertEqual("InvalidEvent", failures[0]["type"])

    def test_runtime_client_error_preserves_native_stage(self):
        response = {
            "stream": [
                {
                    "runtimeClientError": {
                        "type": "DependencyFailure",
                        "message": "MCP connection failed",
                    }
                }
            ]
        }
        status, _, failures = self.capture(consume_response, response)
        self.assertEqual(1, status)
        self.assertEqual("runtimeClientError", failures[0]["stage"])
        self.assertEqual("DependencyFailure", failures[0]["type"])
        self.assertEqual("MCP connection failed", failures[0]["message"])

    def test_lazy_stream_exception_is_structured_failure(self):
        status, stdout, failures = self.capture(
            consume_response, {"stream": FailingStream()}
        )
        self.assertEqual(1, status)
        self.assertEqual("partial\n", stdout)
        self.assertEqual("harness.stream", failures[0]["stage"])

    def test_invocation_exception_is_structured_failure(self):
        status, _, failures = self.capture(
            invoke,
            FakeClient(error=ConnectionError("unreachable")),
            "arn",
            "session",
            "prompt",
        )
        self.assertEqual(1, status)
        self.assertEqual("harness.invoke", failures[0]["stage"])
        self.assertEqual("ConnectionError", failures[0]["type"])


if __name__ == "__main__":
    unittest.main()
