import argparse
import os
import sys
import uuid

import boto3


DEFAULT_PROMPT = (
    "Find the best open-source repositories for building a production Model "
    "Context Protocol gateway. Rank at least five candidates and create a score chart."
)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("prompt", nargs="?", default=DEFAULT_PROMPT)
    parser.add_argument("--session-id", default=str(uuid.uuid4()))
    args = parser.parse_args()

    harness_arn = os.getenv("AGENTCORE_HARNESS_ARN")
    if not harness_arn:
        raise SystemExit("AGENTCORE_HARNESS_ARN is required.")

    client = boto3.client(
        "bedrock-agentcore", region_name=os.getenv("AWS_REGION", "us-west-2")
    )
    response = client.invoke_harness(
        harnessArn=harness_arn,
        runtimeSessionId=args.session_id,
        messages=[{"role": "user", "content": [{"text": args.prompt}]}],
    )

    failed = False
    for event in response["stream"]:
        if "contentBlockDelta" in event:
            text = event["contentBlockDelta"].get("delta", {}).get("text")
            if text:
                print(text, end="", flush=True)
        elif "runtimeClientError" in event:
            failed = True
            error = event["runtimeClientError"]
            print(
                f"\n[harness.failure] {error.get('message', 'Unknown runtime error')}",
                file=sys.stderr,
            )
    print()
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())

