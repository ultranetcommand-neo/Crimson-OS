"""Finance Engine orchestrator — question → valve → gate → brief."""

from __future__ import annotations

import uuid
from datetime import datetime, timezone
from pathlib import Path

from .token import FinanceBrief, FinanceToken
from .valve import run_valve


class FinanceEngine:
    """§12 vertical slice: one survival question through the stack."""

    def __init__(self, repo_root: Path, gate, bridge_dir: Path | None = None):
        self.repo_root = Path(repo_root)
        self.gate = gate
        self.bridge_dir = bridge_dir or self.repo_root / "Agent_Bridge"

    def ask(self, question: str) -> FinanceBrief:
        token_id = f"fin_{uuid.uuid4().hex[:12]}"
        token: FinanceToken = run_valve(question.strip(), token_id)

        intake = self.gate.intake(
            artifact_path="Silo/6_Money_Manager_Caesar/decision_template.md",
            ring=6,
            register="lemma",
            notes=f"Finance ask: {question[:120]}",
        )

        if token.confidence >= 0.5:
            liquid = self.gate.promote_liquid(
                artifact_path=f"finance_token/{token_id}",
                ring=6,
                register="lemma",
                notes=f"verdict={token.verdict.value} confidence={token.confidence}",
            )
            gate_entry_id = liquid.entry_id
        else:
            gate_entry_id = intake.entry_id

        bridge_path = self._write_bridge(token, gate_entry_id)
        summary = (
            f"Finance verdict: {token.verdict.value} "
            f"(confidence {token.confidence:.2f}). {token.judge_rationale}"
        )
        return FinanceBrief(
            token=token,
            gate_entry_id=gate_entry_id,
            bridge_path=str(bridge_path),
            summary=summary,
        )

    def _write_bridge(self, token: FinanceToken, gate_entry_id: str) -> Path:
        self.bridge_dir.mkdir(parents=True, exist_ok=True)
        ts = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S")
        path = self.bridge_dir / f"finance_{token.token_id}_{ts}.md"
        body = f"""# Finance Engine Brief

**Gate entry:** `{gate_entry_id}`  
**Phase:** LIQUID  
**Verdict:** {token.verdict.value}  
**Confidence:** {token.confidence:.2f}  
**Provenance:** {token.provenance}  
**Time:** {token.freshness_utc.isoformat()}

## Question
{token.question}

## Expand
{chr(10).join('- ' + n for n in token.expand_notes)}

## Contract
{chr(10).join('- ' + n for n in token.contract_notes)}

## Judge
{token.judge_rationale}

---
*Finance Engine v1 — operator numbers stay off GitHub; structure only.*
"""
        path.write_text(body, encoding="utf-8")
        return path
