"""Calibrated finance token — §7 contract (LIQUID output, not truth)."""

from __future__ import annotations

from datetime import datetime, timezone
from enum import Enum

from pydantic import BaseModel, Field


class FinanceVerdict(str, Enum):
    PROCEED = "PROCEED"
    HOLD = "HOLD"
    DENY = "DENY"


class FinanceToken(BaseModel):
    """Structured output from Expand/Contract/Judge valve."""

    token_id: str
    question: str
    verdict: FinanceVerdict
    confidence: float = Field(ge=0.0, le=1.0)
    provenance: str
    freshness_utc: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    phase: str = "LIQUID"
    expand_notes: list[str] = Field(default_factory=list)
    contract_notes: list[str] = Field(default_factory=list)
    judge_rationale: str = ""


class FinanceBrief(BaseModel):
    """Operator-facing brief after gate promotion."""

    token: FinanceToken
    gate_entry_id: str
    bridge_path: str
    summary: str
