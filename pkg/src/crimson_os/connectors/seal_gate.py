"""Fail-closed gate. Dead jot does not send."""
from __future__ import annotations

from typing import Any

from crimson_os.seal import Seal


def seal_node(state: dict[str, Any]) -> dict[str, Any]:
    iota = state.get("iota_on", True)
    if isinstance(iota, str):
        iota = iota.lower() != "false"
    result = Seal.verify(bool(iota))
    out = dict(state)
    out["seal"] = result
    out["n"] = Seal.T112 if result == "HOLD" else None
    out["halt"] = result != "HOLD"
    if out["halt"]:
        out["stop"] = "NO_EDGE"
    return out
