"""GitHub ping. No request if seal FAIL. Token from env."""
from __future__ import annotations

import json
import os
import urllib.error
import urllib.request

from .seal_gate import seal_node


def github_ping(iota_on: bool = True) -> dict:
    gated = seal_node({"iota_on": iota_on})
    if gated.get("halt"):
        return {"ok": False, "halt": True, "seal": "FAIL", "sent": False}
    token = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
    if not token:
        return {"ok": False, "seal": "HOLD", "sent": False, "reason": "no GITHUB_TOKEN"}
    req = urllib.request.Request(
        "https://api.github.com/user",
        headers={
            "Authorization": f"Bearer {token}",
            "Accept": "application/vnd.github+json",
            "User-Agent": "crimson-os",
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=8) as resp:
            body = json.loads(resp.read().decode())
            return {"ok": True, "seal": "HOLD", "sent": True, "login": body.get("login")}
    except urllib.error.URLError as e:
        return {"ok": False, "seal": "HOLD", "sent": False, "error": str(e)}
