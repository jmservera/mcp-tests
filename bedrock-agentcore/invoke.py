import argparse
import json
import os
import sys
import uuid
from collections.abc import Mapping

import boto3


DEFAULT_PROMPT = (
    "Find the best open-source repositories for building a production Model "
    "Context Protocol gateway. Rank at least five candidates and create a score chart."
)


def emit_failure(stage: str, message: str, error_type: str) -> None:
    print(
        json.dumps(
            {
                "event": "harness.failure",
                "stage": stage,
                "type": error_type,
                "message": message,
            }
        ),
        file=sys.stderr,
    )


def consume_response(response: object) -> int:
    if not isinstance(response, Mapping):
        emit_failure(
            "harness.response",
            "invoke_harness returned a non-object response.",
            "InvalidResponse",
        )
        return 1

    stream = response.get("stream")
    if isinstance(stream, (str, bytes, Mapping)):
        stream = None
    try:
        events = iter(stream)
    except TypeError:
        emit_failure(
            "harness.response",
            "invoke_harness response is missing an iterable stream.",
            "InvalidResponse",
        )
        return 1

    failed = False
    try:
        for event in events:
            if not isinstance(event, Mapping):
                emit_failure(
                    "harness.stream",
                    "AgentCore returned a non-object stream event.",
                    "InvalidEvent",
                )
                failed = True
                continue

            if "contentBlockDelta" in event:
                content_delta = event["contentBlockDelta"]
                if not isinstance(content_delta, Mapping):
                    emit_failure(
                        "harness.stream",
                        "contentBlockDelta must be an object.",
                        "InvalidEvent",
                    )
                    failed = True
                    continue
                delta = content_delta.get("delta", {})
                if not isinstance(delta, Mapping):
                    emit_failure(
                        "harness.stream",
                        "contentBlockDelta.delta must be an object.",
                        "InvalidEvent",
                    )
                    failed = True
                    continue
                text = delta.get("text")
                if text is not None and not isinstance(text, str):
                    emit_failure(
                        "harness.stream",
                        "contentBlockDelta.delta.text must be a string.",
                        "InvalidEvent",
                    )
                    failed = True
                    continue
                if text:
                    print(text, end="", flush=True)
            elif "runtimeClientError" in event:
                failed = True
                error = event["runtimeClientError"]
                if not isinstance(error, Mapping) or not isinstance(
                    error.get("message"), str
                ):
                    emit_failure(
                        "runtimeClientError",
                        "AgentCore returned a malformed runtimeClientError event.",
                        "InvalidEvent",
                    )
                    continue
                emit_failure(
                    "runtimeClientError",
                    error["message"],
                    str(error.get("type", "RuntimeClientError")),
                )
    except Exception as exc:
        emit_failure("harness.stream", str(exc), type(exc).__name__)
        failed = True

    print()
    return 1 if failed else 0


def invoke(client, harness_arn: str, session_id: str, prompt: str) -> int:
    try:
        response = client.invoke_harness(
            harnessArn=harness_arn,
            runtimeSessionId=session_id,
            messages=[{"role": "user", "content": [{"text": prompt}]}],
        )
    except Exception as exc:
        emit_failure("harness.invoke", str(exc), type(exc).__name__)
        return 1
    return consume_response(response)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("prompt", nargs="?", default=DEFAULT_PROMPT)
    parser.add_argument("--session-id", default=str(uuid.uuid4()))
    args = parser.parse_args()

    harness_arn = os.getenv("AGENTCORE_HARNESS_ARN")
    if not harness_arn:
        emit_failure(
            "configuration",
            "AGENTCORE_HARNESS_ARN is required.",
            "ConfigurationError",
        )
        return 1

    try:
        client = boto3.client(
            "bedrock-agentcore", region_name=os.getenv("AWS_REGION", "us-west-2")
        )
    except Exception as exc:
        emit_failure("client.create", str(exc), type(exc).__name__)
        return 1
    return invoke(client, harness_arn, args.session_id, args.prompt)


if __name__ == "__main__":
    raise SystemExit(main())
