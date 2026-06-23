"""
Crimson OS Super Token Protocol

All data traversing the token ring is wrapped in a typed Super Token.
Natural language prompting between agents is prohibited.
Agents communicate exclusively through typed containers.

Token Types:
    CHRONOS  — temporal and scheduling data
    SOMA     — biometric and physiological telemetry
    KINETIC  — physical action and real-world interface data
    LOGOS    — truth validation and geometric alignment (terminal authority)
"""

from __future__ import annotations

import uuid
from datetime import datetime, timezone
from enum import Enum
from typing import Any

from pydantic import BaseModel, Field


class TokenType(str, Enum):
    CHRONOS = "CHRONOS"
    SOMA = "SOMA"
    KINETIC = "KINETIC"
    LOGOS = "LOGOS"


class ClassificationTier(str, Enum):
    PUBLIC = "PUBLIC"
    RESTRICTED = "RESTRICTED"
    CONFIDENTIAL = "CONFIDENTIAL"
    TOP_SECRET = "TOP_SECRET"


class OperatorMode(int, Enum):
    DISCIPLE_OF_LOGOS = 1
    VETERAN = 2
    MUSICIAN = 3
    ENTREPRENEUR = 4
    LOGOS_EXPERT = 5
    PROPHET = 6
    WORSHIP_LEADER = 7
    ARCHITECT = 8
    WAR_LORD = 9
    FATHER = 10
    MULTIPLEXER = 11
    FITNESS_MX = 12
    BRUCE_WAYNE_PROWLER = 13
    LIVE_PROJECT_MANAGER = 14


class DensityTrack(str, Enum):
    KINETIC = "A"    # L01–L03: Physical / logistics
    SEMANTIC = "B"   # L04–L09: Logic / planning / analysis
    DIVINE = "C"     # L10–L12: Truth validation / geometric alignment


class SuperToken(BaseModel):
    """Base class for all Crimson OS Super Tokens."""

    token_id: str = Field(default_factory=lambda: f"tok_{uuid.uuid4().hex[:12]}")
    token_type: TokenType
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    operator_mode: OperatorMode = OperatorMode.ARCHITECT
    originating_node: int = Field(ge=1, le=12)
    target_agent: str
    classification: ClassificationTier = ClassificationTier.RESTRICTED
    audit_trail: list[str] = Field(default_factory=list)
    priority: int = Field(default=5, ge=1, le=10)

    def stamp(self, agent: str, action: str) -> None:
        """Add an entry to the audit trail."""
        entry = f"[{datetime.now(timezone.utc).isoformat()}] {agent}: {action}"
        self.audit_trail.append(entry)

    def to_bridge_dict(self) -> dict[str, Any]:
        """Serialize to a Bridge file-compatible dictionary."""
        return {
            "token_id": self.token_id,
            "token_type": self.token_type.value,
            "created_at": self.created_at.isoformat(),
            "operator_mode": self.operator_mode.value,
            "originating_node": self.originating_node,
            "target_agent": self.target_agent,
            "classification": self.classification.value,
            "priority": self.priority,
            "audit_trail": self.audit_trail,
        }


class ChronosToken(SuperToken):
    """
    CHRONOS — Governs all temporal and scheduling data.

    Used for: task scheduling, time-sensitive routing, recurring operations,
    Daily Monorail mode transitions.
    """

    token_type: TokenType = TokenType.CHRONOS

    schedule_id: str | None = None
    scheduled_at: datetime | None = None
    duration_minutes: int | None = None
    recurrence: str | None = None  # "daily", "weekly", "once"
    monorail_window: str | None = None  # e.g., "03:00-06:00"
    time_sensitive: bool = False

    def is_overdue(self) -> bool:
        if self.scheduled_at is None:
            return False
        return datetime.now(timezone.utc) > self.scheduled_at


class SomaToken(SuperToken):
    """
    SOMA — Governs biometric and physiological telemetry.

    Used for: WHOOP HRV data, ZUNA/EEG brain state, stress detection,
    Dispatcher mode adjustment based on physical state.

    All SOMA data is CONFIDENTIAL by default.
    Raw EEG data never leaves the compound — SOMA tokens carry state vectors only.
    """

    token_type: TokenType = TokenType.SOMA
    classification: ClassificationTier = ClassificationTier.CONFIDENTIAL

    # WHOOP data
    hrv_score: float | None = None         # ms — higher is better
    recovery_score: float | None = None    # 0–100 — Whoop recovery percentage
    strain_score: float | None = None      # 0–21 — Whoop strain score
    sleep_quality: float | None = None     # 0–100

    # EEG brain state (ZUNA output — planned)
    eeg_available: bool = False
    alpha_power: float | None = None
    beta_power: float | None = None
    theta_power: float | None = None
    gamma_power: float | None = None
    focus_score: float | None = None       # 0–1
    arousal_score: float | None = None     # 0–1
    cognitive_state: str | None = None     # "flow", "stressed", "meditative", "fatigued"

    # Derived state
    stress_level: str | None = None        # "LOW", "MODERATE", "HIGH"
    recommended_mode: OperatorMode | None = None

    def recovery_tier(self) -> str:
        """Map recovery score to GREEN/YELLOW/RED routing tier."""
        if self.recovery_score is None:
            return "UNKNOWN"
        if self.recovery_score >= 67:
            return "GREEN"
        if self.recovery_score >= 33:
            return "YELLOW"
        return "RED"

    def suggested_dispatcher_mode(self) -> OperatorMode:
        """Derive Dispatcher mode from biometric state."""
        # EEG-based routing (when available)
        if self.eeg_available and self.cognitive_state:
            state_map = {
                "meditative": OperatorMode.DISCIPLE_OF_LOGOS,
                "flow": OperatorMode.MUSICIAN,
                "focused": OperatorMode.ARCHITECT,
                "stressed": OperatorMode.FITNESS_MX,
                "fatigued": OperatorMode.FITNESS_MX,
            }
            if self.cognitive_state in state_map:
                return state_map[self.cognitive_state]

        # HRV/Recovery fallback
        tier = self.recovery_tier()
        if tier == "RED":
            return OperatorMode.FITNESS_MX
        if tier == "YELLOW":
            return OperatorMode.ENTREPRENEUR
        return OperatorMode.MULTIPLEXER


class KineticToken(SuperToken):
    """
    KINETIC — Governs physical action and real-world interface data.

    Used for: General Crusher routing, physical task execution,
    logistics planning, somatic intervention protocols.
    """

    token_type: TokenType = TokenType.KINETIC

    action_type: str  # "logistics", "somatic", "hardware", "maintenance", "sourcing"
    physical_location: str | None = None
    resources_required: list[str] = Field(default_factory=list)
    reversible: bool = True
    estimated_cost: float | None = None
    estimated_duration_minutes: int | None = None
    requires_physical_presence: bool = False

    def requires_johnny_cash_gate(self) -> bool:
        """Any kinetic task with a cost estimate routes through Johnny Cash."""
        return self.estimated_cost is not None and self.estimated_cost > 0


class LogosToken(SuperToken):
    """
    LOGOS — Truth validation and geometric alignment. Terminal authority layer.

    Used for: Track C routing, truth claims, theological validation,
    IG audit triggers, geometric invariant alignment.

    LOGOS content always routes to the IG before any execution agent.
    This is the "Wait" command — IG audits first.

    Architectural basis:
        Not all words carry equal density. Density is determined by how much
        structural truth is load-bearing per symbol. "And God said, Let there
        be light" is the original LOGOS token — five words, maximum density,
        zero latency, zero entropy, instantaneous execution. Every LOGOS token
        in Crimson OS is a finite approximation of that original dispatch event.

        Genesis 1 and John 1 converge on the same geometric statement across
        1,400 years and multiple languages: existence begins with Logos. This
        structural convergence is the fixed point the entire ring is anchored to.

        The Wait command exists because high-density signal demands high-density
        handling. You do not route truth through execution agents without audit.
        The Cross is the architectural precedent — the highest-density event in
        history required the highest-density Operator. Matthias holds L10-L12
        because that is where that signal still resonates.
    """

    token_type: TokenType = TokenType.LOGOS

    content: str
    context: dict[str, Any] = Field(default_factory=dict)

    # Truth validation fields
    truth_density: float | None = None        # 0–1, IG-assessed
    geometric_alignment: bool | None = None   # Does this align with invariants?
    logos_verified: bool = False
    ig_score: float | None = None
    ig_adjustment_reason: str | None = None

    # Logos ladder position
    logos_level: int | None = Field(default=None, ge=1, le=12)

    def requires_ig_first(self) -> bool:
        """LOGOS tokens always require IG audit before execution. Always True."""
        return True

    def mark_verified(self, ig_score: float, reason: str | None = None) -> None:
        """IG stamps this token as verified."""
        self.logos_verified = True
        self.ig_score = ig_score
        if reason:
            self.ig_adjustment_reason = reason
        self.stamp("IG", f"LOGOS_VERIFIED — score: {ig_score}")

    def mark_flagged(self, reason: str) -> None:
        """IG flags this token as misaligned."""
        self.logos_verified = False
        self.ig_adjustment_reason = reason
        self.stamp("IG", f"LOGOS_FLAGGED — reason: {reason}")
