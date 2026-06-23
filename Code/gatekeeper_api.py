"""
Sovereign Gate API facade — routes to cockpit POST /build (§8 / SYSTEM_SEMANTIC).

Phase: PARTIAL. Thin client; production IG bus remains DESIGNED.
"""

from __future__ import annotations

import json
import os
import urllib.request


COCKPIT_BUILD = os.getenv("COCKPIT_BUILD_URL", "http://127.0.0.1:8093/build")


def post_build(payload: dict) -> dict:
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        COCKPIT_BUILD,
        data=data,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=10) as resp:
        return json.loads(resp.read().decode("utf-8"))


def intake(artifact_path: str, ring: int, register: str, notes: str | None = None) -> dict:
    return post_build({
        "action": "INTAKE",
        "artifact_path": artifact_path,
        "ring": ring,
        "register": register,
        "notes": notes,
    })
