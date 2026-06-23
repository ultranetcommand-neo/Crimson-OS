"""
Crimson OS Bridge Protocol (SCAFFOLDING)

YAML bridge file read/write for the target Agent_Bridge ledger (DESIGNED/PARTIAL
in the full OS). This module does not connect to NAS or live daemons.
"""

from __future__ import annotations

import uuid
import yaml
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from pydantic import BaseModel, Field

from crimsonos.super_token import ClassificationTier


BRIDGE_DIR_DEFAULT = Path("/mnt/vault/bridge")


class BridgeStatus(str):
    PENDING = "PENDING"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETE = "COMPLETE"
    BLOCKED = "BLOCKED"
    ESCALATED = "ESCALATED"
    FAILED = "FAILED"


class BridgeFile(BaseModel):
    """
    A Bridge file is the atomic unit of inter-agent communication in Crimson OS.

    Bridge files are written to Node 06 Vault and read by the target agent.
    The Scribe (Node 09) aggregates all Bridge files into the immutable audit log.
    """

    bridge_id: str = Field(
        default_factory=lambda: f"brg_{uuid.uuid4().hex[:12]}"
    )
    originating_node: int = Field(ge=1, le=12)
    originating_agent: str
    target_agent: str
    token_type: str = "LOGOS"
    status: str = BridgeStatus.PENDING
    task_summary: str
    task_detail: str | None = None
    ig_score_self: float | None = Field(default=None, ge=0, le=10)
    ig_score_verified: float | None = Field(default=None, ge=0, le=10)
    ig_adjustment_reason: str | None = None
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    completed_at: datetime | None = None
    classification: ClassificationTier = ClassificationTier.RESTRICTED
    metadata: dict[str, Any] = Field(default_factory=dict)

    def complete(self, ig_score_self: float | None = None) -> None:
        """Mark this Bridge file as complete."""
        self.status = BridgeStatus.COMPLETE
        self.completed_at = datetime.now(timezone.utc)
        if ig_score_self is not None:
            self.ig_score_self = ig_score_self

    def block(self, reason: str) -> None:
        """Mark this Bridge file as blocked."""
        self.status = BridgeStatus.BLOCKED
        self.metadata["block_reason"] = reason

    def escalate(self, to_agent: str = "q_orchestrator") -> None:
        """Escalate this Bridge file to a higher authority."""
        self.status = BridgeStatus.ESCALATED
        self.metadata["escalated_to"] = to_agent
        self.metadata["escalated_at"] = datetime.now(timezone.utc).isoformat()

    def apply_ig_audit(self, verified_score: float, reason: str) -> None:
        """
        IG applies an audit adjustment.

        If the self-reported score exceeds verified by more than 0.5,
        the IG adjusts and documents reasoning.
        """
        self.ig_score_verified = verified_score
        if (
            self.ig_score_self is not None
            and self.ig_score_self - verified_score > 0.5
        ):
            self.ig_adjustment_reason = (
                f"Score adjusted from {self.ig_score_self} to {verified_score}. "
                f"Reason: {reason}"
            )
        else:
            self.ig_adjustment_reason = reason

    def to_yaml(self) -> str:
        """Serialize to YAML for file writing."""
        data = {
            "bridge_id": self.bridge_id,
            "originating_node": self.originating_node,
            "originating_agent": self.originating_agent,
            "target_agent": self.target_agent,
            "token_type": self.token_type,
            "status": self.status,
            "task_summary": self.task_summary,
            "classification": self.classification.value,
            "timestamp": self.timestamp.isoformat(),
        }
        if self.task_detail:
            data["task_detail"] = self.task_detail
        if self.ig_score_self is not None:
            data["ig_score_self"] = self.ig_score_self
        if self.ig_score_verified is not None:
            data["ig_score_verified"] = self.ig_score_verified
        if self.ig_adjustment_reason:
            data["ig_adjustment_reason"] = self.ig_adjustment_reason
        if self.completed_at:
            data["completed_at"] = self.completed_at.isoformat()
        if self.metadata:
            data["metadata"] = self.metadata
        return yaml.dump(data, default_flow_style=False, allow_unicode=True)

    def write(self, bridge_dir: Path | None = None) -> Path:
        """
        Write this Bridge file to the vault directory.

        Falls back to a local ./bridge/ directory if /mnt/vault is not mounted.
        """
        if bridge_dir is None:
            if BRIDGE_DIR_DEFAULT.exists():
                bridge_dir = BRIDGE_DIR_DEFAULT
            else:
                bridge_dir = Path("./bridge")

        bridge_dir.mkdir(parents=True, exist_ok=True)
        filename = f"{self.bridge_id}_{self.timestamp.strftime('%Y%m%dT%H%M%S')}.yaml"
        filepath = bridge_dir / filename
        filepath.write_text(self.to_yaml(), encoding="utf-8")
        return filepath

    @classmethod
    def read(cls, filepath: Path) -> "BridgeFile":
        """Read a Bridge file from disk."""
        data = yaml.safe_load(filepath.read_text(encoding="utf-8"))
        return cls(
            bridge_id=data["bridge_id"],
            originating_node=data["originating_node"],
            originating_agent=data["originating_agent"],
            target_agent=data["target_agent"],
            token_type=data.get("token_type", "LOGOS"),
            status=data.get("status", BridgeStatus.PENDING),
            task_summary=data["task_summary"],
            task_detail=data.get("task_detail"),
            ig_score_self=data.get("ig_score_self"),
            ig_score_verified=data.get("ig_score_verified"),
            ig_adjustment_reason=data.get("ig_adjustment_reason"),
            classification=ClassificationTier(data.get("classification", "RESTRICTED")),
            metadata=data.get("metadata", {}),
        )

    @classmethod
    def list_bridge_dir(cls, bridge_dir: Path | None = None) -> list[Path]:
        """List all Bridge files in a directory, sorted by modification time."""
        if bridge_dir is None:
            bridge_dir = BRIDGE_DIR_DEFAULT if BRIDGE_DIR_DEFAULT.exists() else Path("./bridge")
        if not bridge_dir.exists():
            return []
        return sorted(bridge_dir.glob("brg_*.yaml"), key=lambda p: p.stat().st_mtime)
