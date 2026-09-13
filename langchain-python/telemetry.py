import json
import os
import threading
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from uuid import UUID

from langchain_core.callbacks import BaseCallbackHandler
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import ReadableSpan, TracerProvider
from opentelemetry.sdk.trace.export import (
    BatchSpanProcessor,
    SimpleSpanProcessor,
    SpanExportResult,
    SpanExporter,
)
from opentelemetry.trace import Status, StatusCode


def enabled(name: str, default: bool) -> bool:
    value = os.getenv(name)
    if value is None:
        return default
    return value.lower() in {"1", "true", "yes", "on"}


def json_value(value: Any) -> Any:
    if value is None or isinstance(value, (bool, int, float, str)):
        return value
    if isinstance(value, (list, tuple)):
        return [json_value(item) for item in value]
    if isinstance(value, dict):
        return {str(key): json_value(item) for key, item in value.items()}
    return str(value)


class JsonLinesSpanExporter(SpanExporter):
    def __init__(self, path: Path):
        self.path = path
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.lock = threading.Lock()

    def export(self, spans: list[ReadableSpan]) -> SpanExportResult:
        with self.lock, self.path.open("a", encoding="utf-8") as stream:
            for span in spans:
                context = span.get_span_context()
                parent = span.parent
                record = {
                    "timestamp": datetime.now(timezone.utc).isoformat(),
                    "trace_id": f"{context.trace_id:032x}",
                    "span_id": f"{context.span_id:016x}",
                    "parent_span_id": (
                        f"{parent.span_id:016x}" if parent is not None else None
                    ),
                    "name": span.name,
                    "status": span.status.status_code.name,
                    "attributes": json_value(dict(span.attributes or {})),
                    "events": [
                        {
                            "name": event.name,
                            "attributes": json_value(dict(event.attributes or {})),
                        }
                        for event in span.events
                    ],
                }
                stream.write(json.dumps(record) + "\n")
        return SpanExportResult.SUCCESS


class AgentTelemetry:
    def __init__(self, mcp_tool_names: set[str]):
        self.include_content = enabled("TELEMETRY_INCLUDE_CONTENT", False)
        self.provider = TracerProvider(
            resource=Resource.create(
                {
                    "service.name": "mcp-error-comparison-langchain",
                    "service.version": "0.1.0",
                    "deployment.environment": os.getenv(
                        "DEPLOYMENT_ENVIRONMENT", "local"
                    ),
                }
            )
        )
        telemetry_path = Path(
            os.getenv(
                "TELEMETRY_FILE",
                str(Path(__file__).with_name("artifacts") / "telemetry.jsonl"),
            )
        )
        self.provider.add_span_processor(
            SimpleSpanProcessor(JsonLinesSpanExporter(telemetry_path))
        )
        if os.getenv("OTEL_EXPORTER_OTLP_ENDPOINT"):
            self.provider.add_span_processor(BatchSpanProcessor(OTLPSpanExporter()))
        self.tracer = self.provider.get_tracer("mcp-error-comparison.langchain")
        self.handler = AgentTelemetryHandler(
            self.tracer, mcp_tool_names, self.include_content
        )

    def shutdown(self) -> None:
        self.provider.shutdown()


class AgentTelemetryHandler(BaseCallbackHandler):
    def __init__(self, tracer, mcp_tool_names: set[str], include_content: bool):
        self.tracer = tracer
        self.mcp_tool_names = mcp_tool_names
        self.include_content = include_content
        self.spans: dict[UUID, Any] = {}
        self.lock = threading.Lock()

    def _start(self, run_id: UUID, name: str, attributes: dict[str, Any]) -> None:
        span = self.tracer.start_span(name)
        for key, value in attributes.items():
            span.set_attribute(key, value)
        with self.lock:
            self.spans[run_id] = span

    def _finish(
        self,
        run_id: UUID,
        attributes: dict[str, Any] | None = None,
        error: BaseException | None = None,
    ) -> None:
        with self.lock:
            span = self.spans.pop(run_id, None)
        if span is None:
            return
        for key, value in (attributes or {}).items():
            span.set_attribute(key, value)
        if error is not None:
            span.set_attribute("error.type", type(error).__name__)
            if self.include_content:
                span.record_exception(error)
                span.set_status(Status(StatusCode.ERROR, str(error)))
            else:
                span.set_status(Status(StatusCode.ERROR))
        span.end()

    def on_chat_model_start(
        self, serialized, messages, *, run_id, parent_run_id=None, **kwargs
    ) -> None:
        attributes = {
            "gen_ai.operation.name": "chat",
            "gen_ai.request.message_count": sum(len(batch) for batch in messages),
        }
        if self.include_content:
            attributes["gen_ai.input.messages"] = json.dumps(
                json_value(messages), default=str
            )
        self._start(run_id, "chat", attributes)

    def on_llm_end(self, response, *, run_id, parent_run_id=None, **kwargs) -> None:
        self._finish(run_id, {"gen_ai.response.type": type(response).__name__})

    def on_llm_error(
        self, error, *, run_id, parent_run_id=None, **kwargs
    ) -> None:
        self._finish(run_id, error=error)

    def on_tool_start(
        self, serialized, input_str, *, run_id, parent_run_id=None, **kwargs
    ) -> None:
        tool_name = (serialized or {}).get("name") or kwargs.get("name") or "unknown"
        attributes = {
            "gen_ai.operation.name": "execute_tool",
            "gen_ai.tool.name": tool_name,
            "gen_ai.tool.type": (
                "mcp" if tool_name in self.mcp_tool_names else "local"
            ),
        }
        if self.include_content:
            attributes["gen_ai.tool.call.arguments"] = input_str
        self._start(run_id, f"execute_tool.{tool_name}", attributes)

    def on_tool_end(self, output, *, run_id, parent_run_id=None, **kwargs) -> None:
        status = str(getattr(output, "status", "success"))
        attributes = {"gen_ai.tool.result.status": status}
        if self.include_content:
            attributes["gen_ai.tool.call.result"] = json.dumps(
                json_value(getattr(output, "content", output)), default=str
            )
        error = RuntimeError("Tool returned an error result.") if status == "error" else None
        self._finish(run_id, attributes, error)

    def on_tool_error(
        self, error, *, run_id, parent_run_id=None, **kwargs
    ) -> None:
        self._finish(run_id, error=error)


def add_conversation_events(span, messages: list[Any], include_content: bool) -> None:
    for index, message in enumerate(messages):
        attributes = {
            "gen_ai.message.index": index,
            "gen_ai.message.role": getattr(message, "type", type(message).__name__),
            "gen_ai.message.tool_call_count": len(
                getattr(message, "tool_calls", None) or []
            ),
        }
        status = getattr(message, "status", None)
        if status is not None:
            attributes["gen_ai.tool.result.status"] = str(status)
        if self_content := (
            json.dumps(json_value(getattr(message, "content", "")), default=str)
            if include_content
            else None
        ):
            attributes["gen_ai.message.content"] = self_content
        span.add_event("gen_ai.conversation.message", attributes)
