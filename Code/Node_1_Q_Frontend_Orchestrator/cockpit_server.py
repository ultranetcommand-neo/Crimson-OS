#!/usr/bin/env python3
"""
Q Cockpit HTTP server — Node 1 (PARTIAL-LIVE substrate).

Endpoints:
    GET  /status         — machine-readable system state (First Ping target)
    POST /build          — epistemic gate intake / promotion (single writer)
    GET  /build          — tail of build log (read-only)
    POST /finance/ask    — Finance Engine vertical slice
    GET  /health         — liveness probe
"""

from __future__ import annotations

import json
import os
import sys
import urllib.error
import urllib.request
from datetime import datetime, timezone
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT / "Code" / "epistemic_gate"))
sys.path.insert(0, str(REPO_ROOT / "Code" / "engines"))

from gate import EpistemicGate, GateViolation  # noqa: E402
from finance.engine import FinanceEngine  # noqa: E402

HOST = os.getenv("COCKPIT_HOST", "0.0.0.0")
PORT = int(os.getenv("COCKPIT_PORT", "8093"))
INTRANET_URL = os.getenv("INTRANET_URL", "http://127.0.0.1:8092/Node_0.md")
BUILD_LOG = Path(os.getenv("BUILD_LOG_PATH", str(REPO_ROOT / "data" / "build_log.jsonl")))


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _intranet_reachable() -> bool:
    try:
        req = urllib.request.Request(INTRANET_URL, method="GET")
        with urllib.request.urlopen(req, timeout=3) as resp:
            return resp.status == 200
    except (urllib.error.URLError, TimeoutError, OSError):
        return False


def _gate() -> EpistemicGate:
    return EpistemicGate(BUILD_LOG)


def _status_payload() -> dict[str, Any]:
    gate = _gate()
    entries = gate.read_all()
    return {
        "node": 1,
        "role": "Q",
        "phase": "PARTIAL-LIVE",
        "cockpit_version": "0.1.0",
        "timestamp_utc": _utc_now(),
        "intranet_url": INTRANET_URL,
        "substrate": {
            "intranet_reachable": _intranet_reachable(),
            "build_log_path": str(BUILD_LOG),
            "gate_log_entries": len(entries),
        },
        "engines": {
            "finance": {"phase": "PARTIAL", "endpoint": "POST /finance/ask"},
            "epistemic_gate": {"phase": "PARTIAL", "endpoint": "POST /build"},
        },
        "control_plane": ["OPERATOR", "Q", "N.E.O.", "CMO_Edge", "RINGMASTER"],
    }


def _handle_build(body: dict[str, Any]) -> dict[str, Any]:
    action = body.get("action", "").upper()
    artifact_path = body.get("artifact_path", "")
    ring = int(body.get("ring", 0))
    register = body.get("register", "")
    notes = body.get("notes")
    falsification_entry = body.get("falsification_entry")
    operator_ratified = bool(body.get("operator_ratified", False))

    if not artifact_path or not register or ring < 1:
        raise ValueError("artifact_path, ring, register required")

    gate = _gate()
    if action == "INTAKE":
        entry = gate.intake(artifact_path, ring, register, notes=notes)
    elif action == "PROMOTE_LIQUID":
        entry = gate.promote_liquid(artifact_path, ring, register, notes=notes)
    elif action == "PROMOTE_CRYSTAL":
        entry = gate.promote_crystal(
            artifact_path,
            ring,
            register,
            falsification_entry=falsification_entry,
            operator_ratified=operator_ratified,
            notes=notes,
        )
    else:
        raise ValueError(f"Unknown action: {action}")

    return {"ok": True, "entry": entry.to_dict()}


class CockpitHandler(BaseHTTPRequestHandler):
    server_version = "CrimsonCockpit/0.1"

    def log_message(self, fmt: str, *args: Any) -> None:
        sys.stderr.write(f"[cockpit] {self.address_string()} - {fmt % args}\n")

    def _send_json(self, code: int, payload: dict[str, Any]) -> None:
        data = json.dumps(payload, indent=2).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(data)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(data)

    def _read_json_body(self) -> dict[str, Any]:
        length = int(self.headers.get("Content-Length", 0))
        raw = self.rfile.read(length) if length else b"{}"
        return json.loads(raw.decode("utf-8") or "{}")

    def do_OPTIONS(self) -> None:
        self.send_response(204)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def do_GET(self) -> None:
        if self.path in ("/health", "/health/"):
            self._send_json(200, {"ok": True, "time": _utc_now()})
        elif self.path in ("/status", "/status/"):
            self._send_json(200, _status_payload())
        elif self.path.startswith("/build"):
            tail = 20
            if "?" in self.path:
                for part in self.path.split("?", 1)[1].split("&"):
                    if part.startswith("tail="):
                        tail = int(part.split("=", 1)[1])
            rows = _gate().read_all()[-tail:]
            self._send_json(200, {"entries": rows, "count": len(rows)})
        else:
            self._send_json(404, {"error": "not_found", "path": self.path})

    def do_POST(self) -> None:
        try:
            body = self._read_json_body()
            if self.path in ("/build", "/build/"):
                result = _handle_build(body)
                self._send_json(201, result)
            elif self.path in ("/finance/ask", "/finance/ask/"):
                question = body.get("question", "").strip()
                if not question:
                    self._send_json(400, {"error": "question required"})
                    return
                engine = FinanceEngine(REPO_ROOT, _gate())
                brief = engine.ask(question)
                self._send_json(201, {
                    "ok": True,
                    "summary": brief.summary,
                    "gate_entry_id": brief.gate_entry_id,
                    "bridge_path": brief.bridge_path,
                    "token": brief.token.model_dump(mode="json"),
                })
            else:
                self._send_json(404, {"error": "not_found", "path": self.path})
        except GateViolation as e:
            self._send_json(409, {"error": "gate_violation", "message": str(e)})
        except (ValueError, json.JSONDecodeError, KeyError) as e:
            self._send_json(400, {"error": "bad_request", "message": str(e)})
        except Exception as e:
            self._send_json(500, {"error": "internal", "message": str(e)})


def main() -> None:
    BUILD_LOG.parent.mkdir(parents=True, exist_ok=True)
    server = ThreadingHTTPServer((HOST, PORT), CockpitHandler)
    print(f"Crimson OS Cockpit listening on http://{HOST}:{PORT}")
    print(f"  GET  /status")
    print(f"  POST /build")
    print(f"  POST /finance/ask")
    print(f"  build log: {BUILD_LOG}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nCockpit shutdown.")
        server.server_close()


if __name__ == "__main__":
    main()
