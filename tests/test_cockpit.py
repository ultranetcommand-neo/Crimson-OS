"""Cockpit HTTP endpoint tests."""

import json
import sys
import threading
import urllib.request
from http.server import ThreadingHTTPServer
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "Code" / "Node_1_Q_Frontend_Orchestrator"))

import cockpit_server  # noqa: E402


@pytest.fixture
def cockpit_url(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setattr(cockpit_server, "BUILD_LOG", tmp_path / "build_log.jsonl")
    monkeypatch.setattr(cockpit_server, "REPO_ROOT", ROOT)
    server = ThreadingHTTPServer(("127.0.0.1", 0), cockpit_server.CockpitHandler)
    port = server.server_address[1]
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    yield f"http://127.0.0.1:{port}"
    server.shutdown()


def _get(url: str) -> dict:
    with urllib.request.urlopen(url, timeout=5) as resp:
        return json.loads(resp.read().decode("utf-8"))


def _post(url: str, body: dict) -> tuple[int, dict]:
    data = json.dumps(body).encode("utf-8")
    req = urllib.request.Request(
        url,
        data=data,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            return resp.status, json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        return e.code, json.loads(e.read().decode("utf-8"))


def test_status(cockpit_url: str) -> None:
    payload = _get(f"{cockpit_url}/status")
    assert payload["node"] == 1
    assert payload["role"] == "Q"
    assert "substrate" in payload


def test_build_intake(cockpit_url: str) -> None:
    code, payload = _post(
        f"{cockpit_url}/build",
        {
            "action": "INTAKE",
            "artifact_path": "Geometric_Unity_Validation/proof.md",
            "ring": 10,
            "register": "theorem",
        },
    )
    assert code == 201
    assert payload["ok"] is True


def test_finance_ask(cockpit_url: str) -> None:
    code, payload = _post(
        f"{cockpit_url}/finance/ask",
        {"question": "Can I spend $20 on cables?"},
    )
    assert code == 201
    assert payload["ok"] is True
    assert "summary" in payload
