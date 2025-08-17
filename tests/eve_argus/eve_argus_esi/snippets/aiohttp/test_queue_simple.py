"""Tests for SimpleAiohttpActionRunner snippet.

These tests cover:
1. Successful execution of multiple GET requests.
2. Skipping actions when a shutdown signal is preset.
3. Enforcing the max_concurrent_requests limit.
4. Skipping remaining queued actions after a failure triggers shutdown.
"""

import threading
import time
from http.server import BaseHTTPRequestHandler, HTTPServer

import pytest

from eve_argus.eve_argus_esi.snippets.aiohttp.queue_simple import (
    AiohttpAction,
    AiohttpRequest,
    AiohttpRequestStatus,
    AiohttpResponse,
    RequestState,
    Signals,
    SimpleAiohttpActionRunner,
)


class _TestHandler(BaseHTTPRequestHandler):
    def do_GET(self):  # noqa: N802 (HTTP verb name style)
        body = b"ok"
        self.send_response(200)
        self.send_header("Content-Type", "text/plain")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, format, *args):  # noqa: A003 (shadow built-in)
        # Silence default stderr logging to keep test output clean.
        pass


@pytest.fixture()
def http_server():
    """Provide a running ephemeral HTTP server for tests."""
    server = HTTPServer(("127.0.0.1", 0), _TestHandler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    # wait briefly to ensure server loop started
    time.sleep(0.05)
    yield server
    server.shutdown()
    thread.join(timeout=2)


def _make_actions(urls: list[str]) -> list[AiohttpAction]:
    actions: list[AiohttpAction] = []
    for u in urls:
        req = AiohttpRequest(method="GET", url=u)
        status = AiohttpRequestStatus()
        actions.append(AiohttpAction(request=req, request_status=status))
    return actions


def test_simple_aiohttp_action_runner_success_requests(http_server):
    """All actions should complete with 200 responses and proper counters."""
    port = http_server.server_port
    urls = [f"http://127.0.0.1:{port}/test/{i}" for i in range(5)]
    actions = _make_actions(urls)

    runner = SimpleAiohttpActionRunner(max_concurrent_requests=10)
    runner.do_actions(workers=3, actions=actions)

    for action in actions:
        assert action.response is not None, "Expected a response object"
        assert action.response.status_code == 200
        assert action.response.text == "ok"
        # Implementation sets FINISHED state in finally block on success
        assert action.request_status.current_state == RequestState.FINISHED
        assert action.request_status.request_count == 1
        assert action.request_status.success_count == 1
        assert action.request_status.failure_count == 0


def test_simple_aiohttp_action_runner_skipped_when_shutdown():
    """All actions should be skipped when shutdown signal is set before start."""
    # If the runner is already in shutdown mode, all actions should be skipped without responses.
    actions = _make_actions(
        ["http://127.0.0.1:12345/should_not_request" for _ in range(3)]
    )
    runner = SimpleAiohttpActionRunner()
    runner.runner_status = Signals.WORKER_SHUTDOWN
    runner.do_actions(workers=2, actions=actions)

    for action in actions:
        assert action.response is None
        assert action.request_status.current_state == RequestState.SKIPPED
        assert action.request_status.request_count == 0
        assert action.request_status.success_count == 0
        assert action.request_status.failure_count == 0


def test_simple_aiohttp_action_runner_limits_workers(monkeypatch):
    """Requested workers above limit should not exceed max_concurrent_requests."""
    # Verify that requesting more workers than max_concurrent_requests does not exceed the limit.
    limit = 2
    runner = SimpleAiohttpActionRunner(max_concurrent_requests=limit)

    actions = _make_actions([f"http://127.0.0.1:9/{i}" for i in range(10)])

    # Track concurrent executions of the patched _make_request
    state = {"current": 0, "max": 0}

    async def fake_make_request(name, aiohttp_action, session):  # noqa: D401
        # Simulate I/O with a small sleep while tracking concurrency.
        state["current"] += 1
        if state["current"] > state["max"]:
            state["max"] = state["current"]
        # Populate success result similar to real implementation (minimal fields)
        aiohttp_action.request_status.request_count += 1
        aiohttp_action.request_status.success_count += 1
        aiohttp_action.response = AiohttpResponse(
            uuid=aiohttp_action.request.request_id,
            status_code=200,
            status_reason="OK",
            headers=[],
            text="ok",
            request_id=aiohttp_action.request.request_id,
        )
        # allow overlap
        import asyncio

        await asyncio.sleep(0.05)
        state["current"] -= 1

    monkeypatch.setattr(runner, "_make_request", fake_make_request)

    runner.do_actions(workers=5, actions=actions)

    assert state["max"] <= limit, f"Concurrency {state['max']} exceeded limit {limit}"
    # Ensure every action was processed
    for action in actions:
        assert action.response is not None
        assert action.request_status.success_count == 1


def test_simple_aiohttp_action_runner_skips_after_failure(monkeypatch):
    """When a request errors, subsequent queued actions should be skipped."""
    runner = SimpleAiohttpActionRunner(max_concurrent_requests=5)

    # Create one action that will fail followed by several that would succeed if run.
    urls = ["http://localhost:9/fail"] + [
        f"http://localhost:9/success/{i}" for i in range(4)
    ]
    actions = _make_actions(urls)

    # Patch _make_request so first action simulates failure, sets shutdown, others would be skipped.
    async def fake_make_request(name, aiohttp_action, session):
        if "fail" in aiohttp_action.request.url:
            aiohttp_action.request_status.request_count += 1
            aiohttp_action.request_status.failure_count += 1
            aiohttp_action.request_status.current_state = RequestState.FINISHED
            runner.runner_status = Signals.WORKER_SHUTDOWN
            # Simulate no response body available
            aiohttp_action.response = AiohttpResponse(
                uuid=aiohttp_action.request.request_id,
                status_code=400,
                status_reason="Bad Request",
                headers=[],
                text="bad",
                request_id=aiohttp_action.request.request_id,
            )
        else:
            # Would succeed, but we expect skip logic in worker to prevent calling this branch
            aiohttp_action.request_status.request_count += 1
            aiohttp_action.request_status.success_count += 1
            aiohttp_action.response = AiohttpResponse(
                uuid=aiohttp_action.request.request_id,
                status_code=200,
                status_reason="OK",
                headers=[],
                text="ok",
                request_id=aiohttp_action.request.request_id,
            )

    monkeypatch.setattr(runner, "_make_request", fake_make_request)

    runner.do_actions(workers=3, actions=actions)

    first = actions[0]
    assert first.request_status.failure_count == 1
    assert first.request_status.current_state == RequestState.FINISHED
    assert first.response is not None and first.response.status_code == 400

    # Remaining should be skipped: no response set, state SKIPPED, counters zero
    for skipped in actions[1:]:
        assert skipped.request_status.current_state == RequestState.SKIPPED
        assert skipped.response is None
        assert skipped.request_status.request_count == 0
        assert skipped.request_status.success_count == 0
        assert skipped.request_status.failure_count == 0
