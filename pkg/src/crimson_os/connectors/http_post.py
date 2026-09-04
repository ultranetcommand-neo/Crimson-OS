"""Webhook connector. No send if seal FAIL."""
from __future__ import annotations

import json
import os
import urllib.error
import urllib.request

from .seal_gate import seal_node


def http_post(url: str | None, body: dict, iota_on: bool = True) -> dict:
    gated = seal_node({"iota_on": iota_on, "body": body})
    if gated.get("halt"):
        return {"ok": False, "halt": True, "seal": "FAIL", "sent": False}
    target = url or os.environ.get("CRIMSON_WEBHOOK_URL")
    if not target:
        return {"ok": True, "halt": False, "seal": "HOLD", "sent": False, "reason": "no CRIMSON_WEBHOOK_URL"}
    data = json.dumps(body).encode("utf-8")
    req = urllib.request.Request(target, data=data, headers={"Content-Type": "application/json"}, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=8) as resp:
            return {"ok": True, "seal": "HOLD", "sent": True, "status": resp.status}
    except urllib.error.URLError as e:
        return {"ok": False, "seal": "HOLD", "sent": False, "error": str(e)}
