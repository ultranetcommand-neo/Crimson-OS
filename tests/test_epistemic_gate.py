"""Tests for epistemic gate register partition."""

import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "Code" / "epistemic_gate"))

from gate import EpistemicGate, GateViolation  # noqa: E402


@pytest.fixture
def gate(tmp_path: Path) -> EpistemicGate:
    return EpistemicGate(tmp_path / "test_build_log.jsonl")


def test_theorem_promote_crystal(gate: EpistemicGate) -> None:
    entry = gate.promote_crystal(
        "Geometric_Unity_Validation/proof.md",
        ring=10,
        register="theorem",
    )
    assert entry.phase == "CRYSTAL"
    assert len(gate.read_all()) == 1


def test_lemma_requires_falsification_entry(gate: EpistemicGate) -> None:
    with pytest.raises(GateViolation):
        gate.promote_crystal(
            "Geometric_Unity_Validation/jhtdb_ablation_results.json",
            ring=9,
            register="lemma",
        )


def test_lemma_with_falsification_entry(gate: EpistemicGate) -> None:
    gate.promote_crystal(
        "Geometric_Unity_Validation/jhtdb_ablation_results.json",
        ring=9,
        register="lemma",
        falsification_entry="Geometric_Unity_Validation/REPRODUCE.md",
    )
    assert gate.read_all()[0]["falsification_entry"]


def test_symbolic_overlay_cannot_crystallize(gate: EpistemicGate) -> None:
    with pytest.raises(GateViolation):
        gate.promote_crystal(
            "Silo/12_Logos_YHWH/logos.md",
            ring=12,
            register="symbolic_overlay",
        )


def test_symbolic_overlay_root_write_forbidden(gate: EpistemicGate) -> None:
    from gate import BuildLogEntry

    with pytest.raises(GateViolation):
        gate.append(
            BuildLogEntry(
                entry_id="abc12345",
                timestamp_utc="2026-06-18T00:00:00+00:00",
                artifact_path="overlay.md",
                ring=12,
                register="symbolic_overlay",
                phase="GAS",
                gate_action="INTAKE",
                root_write=True,
            )
        )