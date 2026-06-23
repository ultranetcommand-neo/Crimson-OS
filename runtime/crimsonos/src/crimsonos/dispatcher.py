"""
Crimson OS Dynamic Multi-Track Dispatcher

The Dispatcher is the central routing layer. It receives all inputs and sorts
them by density across three tracks before assigning to agents.

Tracks:
    A — Kinetic   (L01-L03): Physical / logistics / real-world action
    B — Semantic  (L04-L09): Logic / planning / analysis / coordination
    C — Divine    (L10-L12): Truth validation / alignment / Logos

The Dispatcher never executes tasks. It classifies, routes, and monitors.
"""

from __future__ import annotations

import re
from datetime import datetime, timezone
from typing import Any

from rich.console import Console
from rich.table import Table

from crimsonos.super_token import (
    ChronosToken,
    ClassificationTier,
    DensityTrack,
    KineticToken,
    LogosToken,
    OperatorMode,
    SomaToken,
    SuperToken,
    TokenType,
)

console = Console()


LOGOS_TRIGGER_PATTERNS = [
    r"\blaw of one\b",
    r"\breflect(ion|ions)?\b",
    r"\blogos\b",
    r"\byhwh\b",
    r"\bjesus\b",
    r"\btruth\b",
    r"\bgeometric\s+invariant\b",
    r"\b137\b",
    r"\bfine.structure\b",
    r"\bgolden\s+ratio\b",
    r"\bphi\b",
    r"\bscripture\b",
    r"\bbible\b",
    r"\btheolog\w+\b",
    r"\bgolden\s+ratio\b",
    r"\bnegentr\w+\b",
]

KINETIC_TRIGGER_PATTERNS = [
    r"\bclean\b",
    r"\bbuild\b",
    r"\bfix\b",
    r"\brepair\b",
    r"\bship\b",
    r"\bsource\b",
    r"\bbuy\b",
    r"\bpurchase\b",
    r"\bphysical\b",
    r"\blogistic\w*\b",
    r"\bhardware\b",
    r"\bexercise\b",
    r"\bcardio\b",
    r"\bworkout\b",
    r"\bsomatic\b",
    r"\bgrounding\b",
]

FINANCIAL_TRIGGER_PATTERNS = [
    r"\bspend\b",
    r"\bbuy\b",
    r"\bpurchase\b",
    r"\bcost\b",
    r"\b\$\d+\b",
    r"\bmoney\b",
    r"\bbudget\b",
    r"\bdebt\b",
    r"\bcrypto\b",
    r"\busaa\b",
    r"\bboa\b",
]


# Map of operator modes to their primary tracks and lead agents
MODE_CONFIG: dict[OperatorMode, dict[str, Any]] = {
    OperatorMode.DISCIPLE_OF_LOGOS: {
        "tracks": [DensityTrack.DIVINE],
        "lead_agents": ["matthias", "ig_inspector"],
        "prepend_ig": True,
        "time_window": "03:00–06:00",
    },
    OperatorMode.VETERAN: {
        "tracks": [DensityTrack.KINETIC],
        "lead_agents": ["general_crusher", "quartermaster"],
        "prepend_ig": False,
        "time_window": "any",
    },
    OperatorMode.MUSICIAN: {
        "tracks": [DensityTrack.SEMANTIC],
        "lead_agents": ["creation_engine", "billy_cmo"],
        "prepend_ig": False,
        "time_window": "evening",
    },
    OperatorMode.ENTREPRENEUR: {
        "tracks": [DensityTrack.SEMANTIC],
        "lead_agents": ["q_orchestrator", "neo_cto", "johnny_cash", "billy_cmo"],
        "prepend_ig": False,
        "time_window": "06:00–12:00",
    },
    OperatorMode.LOGOS_EXPERT: {
        "tracks": [DensityTrack.DIVINE],
        "lead_agents": ["ig_inspector", "librarian"],
        "prepend_ig": True,
        "time_window": "any",
    },
    OperatorMode.PROPHET: {
        "tracks": [DensityTrack.DIVINE],
        "lead_agents": ["matthias", "ig_inspector"],
        "prepend_ig": True,
        "time_window": "morning",
    },
    OperatorMode.WORSHIP_LEADER: {
        "tracks": [DensityTrack.DIVINE],
        "lead_agents": ["matthias"],
        "prepend_ig": True,
        "time_window": "03:00–06:00",
    },
    OperatorMode.ARCHITECT: {
        "tracks": [DensityTrack.SEMANTIC, DensityTrack.DIVINE],
        "lead_agents": ["neo_cto", "q_orchestrator", "librarian"],
        "prepend_ig": False,
        "time_window": "12:00–18:00",
    },
    OperatorMode.WAR_LORD: {
        "tracks": [DensityTrack.KINETIC],
        "lead_agents": ["general_crusher", "taskmaster"],
        "prepend_ig": False,
        "time_window": "any",
    },
    OperatorMode.FATHER: {
        "tracks": [DensityTrack.SEMANTIC],
        "lead_agents": ["q_orchestrator", "doctor"],
        "prepend_ig": False,
        "time_window": "any",
    },
    OperatorMode.MULTIPLEXER: {
        "tracks": [DensityTrack.KINETIC, DensityTrack.SEMANTIC, DensityTrack.DIVINE],
        "lead_agents": ["q_orchestrator", "neo_cto", "general_crusher", "librarian",
                        "billy_cmo", "johnny_cash"],
        "prepend_ig": True,
        "time_window": "peak-ops",
    },
    OperatorMode.FITNESS_MX: {
        "tracks": [DensityTrack.KINETIC],
        "lead_agents": ["biometric_monitor", "doctor"],
        "prepend_ig": False,
        "time_window": "06:00",
    },
    OperatorMode.BRUCE_WAYNE_PROWLER: {
        "tracks": [DensityTrack.SEMANTIC],
        "lead_agents": ["q_orchestrator", "shield_ids", "gilfoyle"],
        "prepend_ig": False,
        "time_window": "any (declared only)",
    },
    OperatorMode.LIVE_PROJECT_MANAGER: {
        "tracks": [DensityTrack.KINETIC, DensityTrack.SEMANTIC],
        "lead_agents": ["taskmaster", "q_orchestrator", "neo_cto"],
        "prepend_ig": False,
        "time_window": "Phase II+",
    },
}


class DispatchResult:
    """Result of a Dispatcher routing decision."""

    def __init__(
        self,
        token: SuperToken,
        track: DensityTrack,
        assigned_agents: list[str],
        requires_ig_first: bool,
        requires_johnny_cash: bool,
        operator_mode: OperatorMode,
        routing_reason: str,
    ):
        self.token = token
        self.track = track
        self.assigned_agents = assigned_agents
        self.requires_ig_first = requires_ig_first
        self.requires_johnny_cash = requires_johnny_cash
        self.operator_mode = operator_mode
        self.routing_reason = routing_reason
        self.dispatched_at = datetime.now(timezone.utc)

    def __str__(self) -> str:
        ig_flag = " [IG FIRST — Wait command active]" if self.requires_ig_first else ""
        cash_flag = " [Johnny Cash gate required]" if self.requires_johnny_cash else ""
        return (
            f"DISPATCH RESULT\n"
            f"  Track:    {self.track.value} ({self.track.name})\n"
            f"  Mode:     {self.operator_mode.value} — {self.operator_mode.name}\n"
            f"  Agents:   {', '.join(self.assigned_agents)}{ig_flag}{cash_flag}\n"
            f"  Reason:   {self.routing_reason}\n"
            f"  Time:     {self.dispatched_at.isoformat()}"
        )


class Dispatcher:
    """
    The Dynamic Multi-Track Dispatcher.

    Receives SuperTokens and routes them to the appropriate agent(s)
    based on content density, operator mode, and biometric state.
    """

    def __init__(self, default_mode: OperatorMode = OperatorMode.ARCHITECT):
        self.current_mode = default_mode
        self.soma_state: SomaToken | None = None
        self._route_history: list[DispatchResult] = []

    def update_mode(self, mode: OperatorMode) -> None:
        """Explicitly set the operator mode."""
        self.current_mode = mode
        console.print(f"[yellow]Dispatcher mode → {mode.value}: {mode.name}[/yellow]")

    def ingest_soma(self, soma: SomaToken) -> None:
        """Update biometric state and adjust mode if SOMA suggests a different mode."""
        self.soma_state = soma
        suggested = soma.suggested_dispatcher_mode()
        if suggested != self.current_mode:
            console.print(
                f"[cyan]SOMA update: biometric state suggests mode "
                f"{suggested.value} ({suggested.name}). "
                f"Current mode: {self.current_mode.name}. "
                f"Override requires Architect declaration.[/cyan]"
            )

    def classify(self, content: str) -> tuple[DensityTrack, bool, bool]:
        """
        Classify content into a density track.

        Returns:
            (track, requires_ig_first, requires_johnny_cash)
        """
        content_lower = content.lower()

        # Check for Logos content — always Wait (IG first)
        logos_match = any(
            re.search(p, content_lower) for p in LOGOS_TRIGGER_PATTERNS
        )

        # Check for Kinetic content — Go command
        kinetic_match = any(
            re.search(p, content_lower) for p in KINETIC_TRIGGER_PATTERNS
        )

        # Check for financial content — Johnny Cash gate
        financial_match = any(
            re.search(p, content_lower) for p in FINANCIAL_TRIGGER_PATTERNS
        )

        if logos_match:
            return DensityTrack.DIVINE, True, financial_match

        if kinetic_match and not logos_match:
            return DensityTrack.KINETIC, False, financial_match

        # Default: Semantic
        return DensityTrack.SEMANTIC, False, financial_match

    def route(self, token: SuperToken) -> DispatchResult:
        """
        Route a SuperToken to the appropriate agent(s).

        LOGOS tokens always go to IG first (Wait command).
        KINETIC tokens go directly to General Crusher + Librarian (Go command).
        SOMA tokens update biometric state — no agent routing.
        CHRONOS tokens go to Taskmaster.
        """
        mode_config = MODE_CONFIG[self.current_mode]

        # SOMA: internal update only
        if isinstance(token, SomaToken):
            self.ingest_soma(token)
            result = DispatchResult(
                token=token,
                track=DensityTrack.KINETIC,
                assigned_agents=["biometric_monitor"],
                requires_ig_first=False,
                requires_johnny_cash=False,
                operator_mode=self.current_mode,
                routing_reason="SOMA token — biometric state updated internally. No agent routing.",
            )
            self._route_history.append(result)
            return result

        # CHRONOS: Taskmaster
        if isinstance(token, ChronosToken):
            result = DispatchResult(
                token=token,
                track=DensityTrack.SEMANTIC,
                assigned_agents=["taskmaster"],
                requires_ig_first=False,
                requires_johnny_cash=False,
                operator_mode=self.current_mode,
                routing_reason="CHRONOS token — scheduled to Taskmaster.",
            )
            self._route_history.append(result)
            return result

        # LOGOS: always IG first
        if isinstance(token, LogosToken):
            result = DispatchResult(
                token=token,
                track=DensityTrack.DIVINE,
                assigned_agents=["ig_inspector", "matthias"],
                requires_ig_first=True,
                requires_johnny_cash=False,
                operator_mode=self.current_mode,
                routing_reason="LOGOS token — Wait command. IG audit required before any execution.",
            )
            self._route_history.append(result)
            return result

        # KINETIC: General Crusher + Librarian
        if isinstance(token, KineticToken):
            requires_cash = token.requires_johnny_cash_gate()
            agents = ["general_crusher", "librarian"]
            if requires_cash:
                agents.insert(0, "johnny_cash")
            result = DispatchResult(
                token=token,
                track=DensityTrack.KINETIC,
                assigned_agents=agents,
                requires_ig_first=False,
                requires_johnny_cash=requires_cash,
                operator_mode=self.current_mode,
                routing_reason="KINETIC token — Go command. Physical feasibility check.",
            )
            self._route_history.append(result)
            return result

        # Generic SuperToken: classify by content if available
        content = getattr(token, "content", "") or ""
        track, requires_ig, requires_cash = self.classify(content)

        # Apply mode override
        if mode_config.get("prepend_ig") and not requires_ig:
            requires_ig = True

        # Determine agents
        if track == DensityTrack.DIVINE or requires_ig:
            agents = ["ig_inspector"] + mode_config["lead_agents"]
        elif track == DensityTrack.KINETIC:
            agents = ["general_crusher", "librarian"]
            if requires_cash:
                agents.insert(0, "johnny_cash")
        else:
            agents = mode_config["lead_agents"]

        # Deduplicate while preserving order
        seen: set[str] = set()
        unique_agents = [a for a in agents if not (a in seen or seen.add(a))]  # type: ignore[func-returns-value]

        result = DispatchResult(
            token=token,
            track=track,
            assigned_agents=unique_agents,
            requires_ig_first=requires_ig,
            requires_johnny_cash=requires_cash,
            operator_mode=self.current_mode,
            routing_reason=f"Content classified as Track {track.value}. Mode: {self.current_mode.name}.",
        )
        self._route_history.append(result)
        return result

    def status_table(self) -> Table:
        """Generate a Rich table showing current Dispatcher state."""
        table = Table(title="Crimson OS Dispatcher Status", show_header=True)
        table.add_column("Parameter", style="cyan")
        table.add_column("Value", style="white")

        table.add_row("Current Mode", f"{self.current_mode.value} — {self.current_mode.name}")
        mode_cfg = MODE_CONFIG[self.current_mode]
        table.add_row("Active Tracks", ", ".join(t.value for t in mode_cfg["tracks"]))
        table.add_row("Lead Agents", ", ".join(mode_cfg["lead_agents"]))
        table.add_row("IG Prepend", str(mode_cfg.get("prepend_ig", False)))
        table.add_row("Time Window", mode_cfg.get("time_window", "any"))

        if self.soma_state:
            table.add_row("HRV Score", str(self.soma_state.hrv_score or "N/A"))
            table.add_row("Recovery", f"{self.soma_state.recovery_score or 'N/A'}% — {self.soma_state.recovery_tier()}")
            table.add_row("EEG State", self.soma_state.cognitive_state or "N/A")

        table.add_row("Routes This Session", str(len(self._route_history)))
        return table
