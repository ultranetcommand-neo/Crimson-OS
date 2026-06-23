"""
Expand / Contract / Judge valve — §6 sockets (PARTIAL stubs).

Models are swappable bulbs; these functions are the sterile labels.
Output is LIQUID structure — gate closes CRYSTAL with data, not consensus.
"""

from __future__ import annotations

import re

from .token import FinanceToken, FinanceVerdict


def expand(question: str) -> list[str]:
    """Diverge: enumerate considerations (stub — no LLM)."""
    notes = [
        "Survival-first: discretionary spend requires explicit operator intent.",
        "Check whether purchase advances mission vs comfort spending.",
    ]
    if re.search(r"\$\d+", question):
        notes.append("Explicit dollar amount detected — Johnny Cash gate applies.")
    if re.search(r"\b(debt|credit|loan)\b", question, re.I):
        notes.append("Debt exposure — escalate if payoff timeline unclear.")
    return notes


def contract(question: str, expand_notes: list[str]) -> list[str]:
    """Compress: risks and constraints (stub)."""
    risks = [
        "Unvalidated assumptions remain until operator supplies account context.",
        "Valve output is LIQUID — not authorization to spend.",
    ]
    if len(expand_notes) > 3:
        risks.append("High consideration count — narrow scope before execution.")
    return risks


def judge(question: str, expand_notes: list[str], contract_notes: list[str]) -> tuple[FinanceVerdict, float, str]:
    """Synthesize decision (deterministic stub)."""
    q = question.lower()
    if any(w in q for w in ("gamble", "crypto all in", "max out")):
        return FinanceVerdict.DENY, 0.85, "Risk language exceeds survival parameters."
    if any(w in q for w in ("hold", "wait", "defer")):
        return FinanceVerdict.HOLD, 0.7, "Operator requested deferral posture."
    if "?" in question and len(question) < 200:
        return FinanceVerdict.HOLD, 0.55, "Insufficient structured context — operator review required."
    return FinanceVerdict.PROCEED, 0.45, "Tentative proceed — low confidence without NAS finance feed."


def run_valve(question: str, token_id: str, provenance: str = "valve/stub/v1") -> FinanceToken:
    """Full expand → contract → judge pipeline."""
    ex = expand(question)
    co = contract(question, ex)
    verdict, confidence, rationale = judge(question, ex, co)
    return FinanceToken(
        token_id=token_id,
        question=question,
        verdict=verdict,
        confidence=confidence,
        provenance=provenance,
        expand_notes=ex,
        contract_notes=co,
        judge_rationale=rationale,
    )
