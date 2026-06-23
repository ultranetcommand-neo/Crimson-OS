"""
Crimson OS — Protocol Scaffold (Python)

Phase: SCAFFOLDING. Typed stubs for routing, tokens, bridge files, and IG audit
shapes. Not the live multi-agent runtime — see MASTER_ARCHITECTURE in the monorepo.

Architect: Matt Gibson / Crimson Symphony Media
License: Apache 2.0
"""

__version__ = "0.1.1"
__author__ = "Matt Gibson"
__email__ = "crimson@crimsonsymphonymedia.com"

from crimsonos.dispatcher import Dispatcher
from crimsonos.super_token import (
    ChronosToken,
    SomaToken,
    KineticToken,
    LogosToken,
    SuperToken,
)
from crimsonos.bridge import BridgeFile
from crimsonos.ig import IGProtocol

__all__ = [
    "Dispatcher",
    "ChronosToken",
    "SomaToken",
    "KineticToken",
    "LogosToken",
    "SuperToken",
    "BridgeFile",
    "IGProtocol",
]
