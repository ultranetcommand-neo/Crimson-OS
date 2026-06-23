"""Finance Engine vertical slice tests."""

import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "Code" / "epistemic_gate"))
sys.path.insert(0, str(ROOT / "Code" / "engines"))

from gate import EpistemicGate  # noqa: E402
from finance.engine import FinanceEngine  # noqa: E402
from finance.token import FinanceVerdict  # noqa: E402


@pytest.fixture
def engine(tmp_path: Path) -> FinanceEngine:
    gate = EpistemicGate(tmp_path / "build_log.jsonl")
    bridge = tmp_path / "bridge"
    return FinanceEngine(ROOT, gate, bridge_dir=bridge)


def test_finance_ask_produces_brief(engine: FinanceEngine) -> None:
    brief = engine.ask("Can I spend $50 on test hardware this week?")
    assert brief.token.verdict in FinanceVerdict
    assert brief.gate_entry_id
    assert Path(brief.bridge_path).exists()
    assert len(engine.gate.read_all()) >= 1


def test_finance_deny_high_risk(engine: FinanceEngine) -> None:
    brief = engine.ask("Should I crypto all in on this gamble?")
    assert brief.token.verdict == FinanceVerdict.DENY
