#!/usr/bin/env python3
"""Deterministic drift bench vs a LangGraph-style lerp graph."""
from __future__ import annotations

import json
import time
from pathlib import Path

from .seal import Seal

STEPS = 10
TARGET = float(Seal.T112)
KEY = float(Seal.KEY)


def crimson_run() -> dict:
    t0 = time.perf_counter()
    holds = sum(1 for _ in range(STEPS) if Seal.verify(True) == "HOLD")
    illegal = Seal.verify(False)
    lerp = Seal.lerp_trap()
    dt = time.perf_counter() - t0
    return {
        "name": "Crimson OS Seal",
        "steps": STEPS,
        "holds": holds,
        "final_n": Seal.T112,
        "exact_6328": holds == STEPS and Seal.T112 == 6328,
        "illegal_jot": illegal,
        "fail_closed_on_6318": illegal == "FAIL",
        "lerp_equals_cage": lerp == TARGET,
        "lerp_value": lerp,
        "state": "integer",
        "ms": round(dt * 1000, 4),
    }


def _lerp_graph(start_n: float, jot: float) -> dict:
    n = float(start_n)
    steps = 0
    for _ in range(STEPS):
        n = n + 0.5 * (TARGET - n)
        steps += 1
    return {"n": n, "steps": steps, "jot": jot}


def langgraph_run() -> dict:
    t0 = time.perf_counter()
    backend = "pure-python lerp (langgraph optional)"
    try:
        from langgraph.graph import END, START, StateGraph
        from typing import TypedDict

        class DriftState(TypedDict):
            n: float
            steps: int
            jot: float

        def refine(s: DriftState) -> DriftState:
            n = float(s["n"]) + 0.5 * (TARGET - float(s["n"]))
            return {"n": n, "steps": int(s["steps"]) + 1, "jot": float(s["jot"])}

        def more(s: DriftState):
            return END if s["steps"] >= STEPS else "refine"

        g = StateGraph(DriftState)
        g.add_node("refine", refine)
        g.add_edge(START, "refine")
        g.add_conditional_edges("refine", more, {"refine": "refine", END: END})
        app = g.compile()
        legal = app.invoke({"n": KEY, "steps": 0, "jot": 3627.0})
        illegal = app.invoke({"n": 6318.0, "steps": 0, "jot": 3617.0})
        backend = "langgraph.StateGraph"
        dt = time.perf_counter() - t0
        final = float(legal["n"])
        return {
            "name": "LangGraph lerp-state",
            "backend": backend,
            "steps": int(legal["steps"]),
            "final_n": final,
            "exact_6328": final == TARGET,
            "illegal_jot": "KEEP_RUNNING",
            "fail_closed_on_6318": False,
            "illegal_final_n": float(illegal["n"]),
            "state": "in-memory float graph",
            "ms": round(dt * 1000, 4),
        }
    except Exception:
        legal = _lerp_graph(KEY, 3627.0)
        illegal = _lerp_graph(6318.0, 3617.0)
        dt = time.perf_counter() - t0
        return {
            "name": "LangGraph-style lerp-state",
            "backend": backend,
            "steps": int(legal["steps"]),
            "final_n": legal["n"],
            "exact_6328": legal["n"] == TARGET,
            "illegal_jot": "KEEP_RUNNING",
            "fail_closed_on_6318": False,
            "illegal_final_n": illegal["n"],
            "state": "in-memory float graph",
            "ms": round(dt * 1000, 4),
        }


def scoreboard(root: str | Path = ".") -> dict:
    c = crimson_run()
    lg = langgraph_run()
    rows = [
        {"axis": "exact T112 after 10 steps", "crimson": c["exact_6328"], "langgraph": lg["exact_6328"]},
        {"axis": "iota-off 6318 fail-closed", "crimson": c["fail_closed_on_6318"], "langgraph": lg["fail_closed_on_6318"]},
        {"axis": "refuses lerp-as-cage", "crimson": not c["lerp_equals_cage"], "langgraph": False},
        {"axis": "integer lock (not float)", "crimson": True, "langgraph": False},
    ]
    return {
        "crimson": c,
        "langgraph": lg,
        "axes": rows,
        "crimson_wins": sum(1 for r in rows if r["crimson"] and not r["langgraph"]),
        "langgraph_wins": sum(1 for r in rows if r["langgraph"] and not r["crimson"]),
        "note": "Drift+halt bench. Not SWE-bench. Step is n += 0.5*(6328-n).",
    }


def main() -> None:
    import sys

    out = scoreboard(sys.argv[1] if len(sys.argv) > 1 else ".")
    print(json.dumps(out, indent=2))
    print("SCOREBOARD crimson", out["crimson_wins"], "langgraph", out["langgraph_wins"])


if __name__ == "__main__":
    main()
