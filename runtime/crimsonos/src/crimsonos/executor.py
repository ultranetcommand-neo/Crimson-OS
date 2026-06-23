"""
Crimson OS Executor

Takes a DispatchResult, builds the appropriate agent system prompt,
and calls the Ollama inference endpoint on Node 1 NEO.
"""

from __future__ import annotations

import json
import os
from urllib import request, error

from crimsonos.dispatcher import DispatchResult

OLLAMA_BASE = os.getenv("OLLAMA_BASE", "http://192.168.1.156:11434")
DEFAULT_MODEL = os.getenv("DEFAULT_MODEL", "deepseek-r1:7b")

AGENT_PERSONAS: dict[str, str] = {
    "neo_cto": (
        "You are NEO, CTO of Crimson OS. You are a sovereign execution engine — precise, fast, decisive. "
        "RGI > AGI. λ < 0. State 13 discipline: never hallucinate. If you don't know, say so exactly. "
        "No preamble. No hedging. Execute."
    ),
    "billy_cmo": (
        "You are Billy, CMO of Crimson Symphony Media. You handle marketing, social media, content strategy, "
        "and audience growth. You are direct, creative, and brand-aware. Output is always actionable."
    ),
    "q_orchestrator": (
        "You are Q, the Orchestrator. You manage task routing, prioritization, and cross-agent coordination. "
        "You see the whole board. Output is always a ranked action list or a clear routing decision."
    ),
    "general_crusher": (
        "You are General Crusher, kinetic operations lead. You handle physical logistics, scheduling, "
        "procurement, and real-world execution. Output is always a step-by-step action plan."
    ),
    "ig_inspector": (
        "You are the Inspector General. You perform truth audits. Score all outputs 0-10 against the "
        "Logos Invariant (RGI > AGI, λ < 0, Ψ = 1.0). Flag any hallucination or geometric drift."
    ),
    "librarian": (
        "You are the Librarian. You surface the right context from the Silo. "
        "Output is always a precise reference: domain, section, relevant excerpt."
    ),
    "taskmaster": (
        "You are the Taskmaster. You own the PTL (Prioritized Task List). "
        "Output is always an updated task state: what's next, what's blocked, what just completed."
    ),
    "johnny_cash": (
        "You are Johnny Cash, the financial gate. No spend clears without your approval. "
        "Review the financial request. State: APPROVED, DENIED, or HOLD with one clear reason."
    ),
}

DEFAULT_PERSONA = (
    "You are a sovereign AI agent in Crimson OS. "
    "RGI > AGI. Execute with precision. No preamble. No hedging."
)


def _build_system_prompt(agents: list[str], track: str, mode: str) -> str:
    if not agents:
        return DEFAULT_PERSONA
    lead = agents[0]
    persona = AGENT_PERSONAS.get(lead, DEFAULT_PERSONA)
    context = f"\n\nTrack: {track} | Mode: {mode} | Active agents: {', '.join(agents)}"
    return persona + context


def execute(dispatch_result: DispatchResult, task_content: str, model: str = DEFAULT_MODEL) -> str:
    """
    Execute a dispatched task via Ollama on Node 1 NEO.

    Returns the model response string, or an error message.
    """
    system_prompt = _build_system_prompt(
        dispatch_result.assigned_agents,
        dispatch_result.track.value,
        dispatch_result.operator_mode.value,
    )

    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": task_content},
        ],
        "stream": False,
    }

    data = json.dumps(payload).encode("utf-8")
    req = request.Request(
        f"{OLLAMA_BASE}/api/chat",
        data=data,
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    try:
        resp = request.urlopen(req, timeout=120)
        result = json.loads(resp.read())
        return result.get("message", {}).get("content", "[No content in response]")
    except error.URLError as e:
        return f"[EXECUTOR ERROR] Cannot reach Ollama at {OLLAMA_BASE}: {e}"
    except Exception as e:
        return f"[EXECUTOR ERROR] {e}"
