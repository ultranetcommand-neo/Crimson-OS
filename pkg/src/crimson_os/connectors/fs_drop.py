"""Write to a markdown bus file. No write if seal FAIL."""
from __future__ import annotations

from pathlib import Path

from .seal_gate import seal_node


def fs_drop(path: str | Path, text: str, iota_on: bool = True) -> dict:
    gated = seal_node({"iota_on": iota_on})
    if gated.get("halt"):
        return {"ok": False, "halt": True, "seal": "FAIL", "wrote": False}
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    with p.open("a", encoding="utf-8") as f:
        f.write(text if text.endswith("\n") else text + "\n")
    return {"ok": True, "seal": "HOLD", "wrote": True, "path": str(p)}
