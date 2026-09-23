#!/usr/bin/env python3
"""Request best-effort preservation of the NiceTryGPT Git origin in Software Heritage."""

from __future__ import annotations

import argparse
import json
from urllib.parse import urlencode
from urllib.request import Request, urlopen

DEFAULT_ORIGIN = "https://github.com/aleff-github/NiceTryGPT"
API_ENDPOINT = "https://archive.softwareheritage.org/api/1/origin/save/"
ACCEPTED_REQUEST_STATUSES = {"accepted", "pending"}


class ArchiveRequestError(RuntimeError):
    pass


def build_request_url(origin_url: str) -> str:
    params = urlencode({"visit_type": "git", "origin_url": origin_url})
    return f"{API_ENDPOINT}?{params}"


def validate_response(payload: dict) -> tuple[str, str | None]:
    request_status = payload.get("save_request_status")
    task_status = payload.get("save_task_status")
    if request_status not in ACCEPTED_REQUEST_STATUSES:
        raise ArchiveRequestError(
            f"unexpected Software Heritage request status: {request_status!r}"
        )
    return request_status, task_status


def request_archive(origin_url: str, timeout: float = 30.0) -> dict:
    request = Request(build_request_url(origin_url), method="POST")
    with urlopen(request, timeout=timeout) as response:
        payload = json.loads(response.read().decode("utf-8"))
    validate_response(payload)
    return payload


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--origin", default=DEFAULT_ORIGIN)
    parser.add_argument(
        "--print-url",
        action="store_true",
        help="print the request URL without performing a network request",
    )
    args = parser.parse_args()

    if args.print_url:
        print(build_request_url(args.origin))
        return 0

    payload = request_archive(args.origin)
    request_status, task_status = validate_response(payload)
    print(json.dumps(payload, sort_keys=True))
    print(
        f"Software Heritage request: {request_status}; "
        f"task: {task_status}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
