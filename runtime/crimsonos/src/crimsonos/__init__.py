"""
Crimson OS — Sovereign Multi-Agent Operating Architecture

A 12-node token-ring network coordinating 17 autonomous agents
on consumer hardware with zero cloud dependency.

Architect: Matt Gibson / Crimson Symphony Media
License: Apache 2.0
"""

__version__ = "0.1.0"
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
