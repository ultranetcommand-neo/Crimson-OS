"""
Weaver Stats daemon stub — aggregates cockpit status + gate log for telemetry.

Phase: PARTIAL. Run once or loop; feeds future Crimson Deck.
"""

from __future__ import annotations

import json
import os
import time
import urllib.request


COCKPIT_STATUS = os.getenv("COCKPIT_STATUS_URL", "http://127.0.0.1:8093/status")
INTERVAL = int(os.getenv("WEAVER_INTERVAL_SEC", "60"))


def fetch_status() -> dict:
    with urllib.request.urlopen(COCKPIT_STATUS, timeout=5) as resp:
        return json.loads(resp.read().decode("utf-8"))


def weave_once() -> dict:
    status = fetch_status()
    payload = {
        "weaver_phase": "PARTIAL",
        "cockpit": status,
        "telemetry_note": "Gatekeeper + daemon mesh not fully wired — status only.",
    }
    return payload


def main() -> None:
    print(f"Weaver stats → {COCKPIT_STATUS} every {INTERVAL}s")
    while True:
        try:
            payload = weave_once()
            print(json.dumps(payload, indent=2))
        except Exception as e:
            print(f"[weaver] error: {e}")
        time.sleep(INTERVAL)


if __name__ == "__main__":
    main()
