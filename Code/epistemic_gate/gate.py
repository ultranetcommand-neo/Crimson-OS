"""
Crimson OS — Epistemic Gate (public stub)

Append-only build log with register partition enforcement.
Status: PARTIAL — stdlib file I/O; production target is single-writer cockpit + NAS ledger.

Fail closed: invalid transitions raise GateViolation.
"""

from __future__ import annotations

import json
import uuid
from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Optional

VALID_REGISTERS = frozenset(
    {"physical_state", "closed_math", "theorem", "lemma", "symbolic_overlay"}
)
VALID_PHASES = frozenset({"GAS", "LIQUID", "CRYSTAL", "RETRACTED"})
VALID_ACTIONS = frozenset(
    {"INTAKE", "PROMOTE_LIQUID", "PROMOTE_CRYSTAL", "DEMOTE", "FALSIFY", "RETRACT"}
)

# symbolic_overlay must never claim root_write on physical rings
PHYSICAL_RINGS = frozenset({2, 3, 4})


class GateViolation(Exception):
    """Policy or transition violation — fail closed."""


@dataclass
class BuildLogEntry:
    entry_id: str
    timestamp_utc: str
    artifact_path: str
    ring: int
    register: str
    phase: str
    gate_action: str
    falsification_entry: Optional[str] = None
    root_write: bool = False
    taxonomy_class: Optional[str] = None
    operator_ratified: bool = False
    notes: Optional[str] = None

    def to_dict(self) -> dict[str, Any]:
        d = asdict(self)
        return {k: v for k, v in d.items() if v is not None}


def _now_utc() -> str:
    return datetime.now(timezone.utc).isoformat()


def _validate_entry(entry: BuildLogEntry) -> None:
    if entry.register not in VALID_REGISTERS:
        raise GateViolation(f"Unknown register: {entry.register}")
    if entry.phase not in VALID_PHASES:
        raise GateViolation(f"Unknown phase: {entry.phase}")
    if entry.gate_action not in VALID_ACTIONS:
        raise GateViolation(f"Unknown gate_action: {entry.gate_action}")
    if not (1 <= entry.ring <= 12):
        raise GateViolation(f"Ring out of range: {entry.ring}")

    if entry.register == "symbolic_overlay":
        if entry.root_write:
            raise GateViolation(
                "symbolic_overlay cannot root_write — partition to L12 only"
            )
        if entry.ring in PHYSICAL_RINGS and entry.phase == "CRYSTAL":
            raise GateViolation(
                "symbolic_overlay cannot crystallize on physical rings (L2–L4)"
            )

    if entry.gate_action == "PROMOTE_CRYSTAL":
        if entry.register == "lemma" and not entry.falsification_entry:
            raise GateViolation(
                "lemma → CRYSTAL requires falsification_entry path"
            )
        if entry.register == "symbolic_overlay":
            raise GateViolation("symbolic_overlay cannot PROMOTE_CRYSTAL")


class EpistemicGate:
    def __init__(self, log_path: Path):
        self.log_path = Path(log_path)
        self.log_path.parent.mkdir(parents=True, exist_ok=True)

    def append(self, entry: BuildLogEntry) -> BuildLogEntry:
        _validate_entry(entry)
        line = json.dumps(entry.to_dict(), ensure_ascii=False) + "\n"
        with open(self.log_path, "a", encoding="utf-8") as f:
            f.write(line)
        return entry

    def intake(
        self,
        artifact_path: str,
        ring: int,
        register: str,
        notes: Optional[str] = None,
    ) -> BuildLogEntry:
        entry = BuildLogEntry(
            entry_id=uuid.uuid4().hex[:12],
            timestamp_utc=_now_utc(),
            artifact_path=artifact_path,
            ring=ring,
            register=register,
            phase="GAS",
            gate_action="INTAKE",
            notes=notes,
        )
        return self.append(entry)

    def promote_liquid(
        self,
        artifact_path: str,
        ring: int,
        register: str,
        notes: Optional[str] = None,
    ) -> BuildLogEntry:
        entry = BuildLogEntry(
            entry_id=uuid.uuid4().hex[:12],
            timestamp_utc=_now_utc(),
            artifact_path=artifact_path,
            ring=ring,
            register=register,
            phase="LIQUID",
            gate_action="PROMOTE_LIQUID",
            notes=notes,
        )
        return self.append(entry)

    def promote_crystal(
        self,
        artifact_path: str,
        ring: int,
        register: str,
        falsification_entry: Optional[str] = None,
        operator_ratified: bool = False,
        notes: Optional[str] = None,
    ) -> BuildLogEntry:
        entry = BuildLogEntry(
            entry_id=uuid.uuid4().hex[:12],
            timestamp_utc=_now_utc(),
            artifact_path=artifact_path,
            ring=ring,
            register=register,
            phase="CRYSTAL",
            gate_action="PROMOTE_CRYSTAL",
            falsification_entry=falsification_entry,
            operator_ratified=operator_ratified,
            notes=notes,
        )
        return self.append(entry)

    def read_all(self) -> list[dict[str, Any]]:
        if not self.log_path.exists():
            return []
        rows: list[dict[str, Any]] = []
        with open(self.log_path, encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line:
                    rows.append(json.loads(line))
        return rows


if __name__ == "__main__":
    gate = EpistemicGate(Path("build_log.jsonl"))
    gate.promote_crystal(
        "Geometric_Unity_Validation/proof.md",
        ring=10,
        register="theorem",
        operator_ratified=False,
        notes="Theorem register — empirical bridges remain LIQUID",
    )
    gate.promote_liquid(
        "Geometric_Unity_Validation/jhtdb_ablation_results.json",
        ring=9,
        register="lemma",
        notes="Published negative: candidate_beats_random false",
    )
    print(f"Wrote {len(gate.read_all())} entries to {gate.log_path}")