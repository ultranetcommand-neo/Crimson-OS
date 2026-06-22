#!/usr/bin/env python3
"""Geometric Unity Physics MCP — phase-labeled read-only corpus tools."""

from __future__ import annotations

import json

from mcp.server.fastmcp import FastMCP

from corpus import (
    CORPUS_INDEX,
    HF_DATASET,
    PHASE_REGISTER_TABLE,
    PROOF_ANCHOR,
    corpus_dir,
    jhtdb_verdict,
    read_doc,
)

mcp = FastMCP(
    "geometric-unity-physics",
    instructions=(
        "Phase-labeled Geometric Unity physics register. "
        "CRYSTAL theorem (cos θ = ⅓) is separate from LIQUID/NEGATIVE empirical lemmas. "
        "Poole manifold = external CA benchmark, not co-authorship."
    ),
)


@mcp.tool()
def get_proof_anchor() -> str:
    """Return the CRYSTAL theorem anchor: F₂ ↪ SO(3), cos θ = ⅓."""
    return PROOF_ANCHOR


@mcp.tool()
def get_phase_register() -> str:
    """Return the theorem vs lemma vs NEGATIVE register separation table."""
    return PHASE_REGISTER_TABLE


@mcp.tool()
def get_jhtdb_verdict() -> str:
    """Return parsed JHTDB ablation verdict including candidate_beats_random (honest negative)."""
    return json.dumps(jhtdb_verdict(), indent=2)


@mcp.tool()
def list_physics_corpus() -> str:
    """List all readable physics documents with phase labels and summaries."""
    rows = []
    for doc_id, meta in sorted(CORPUS_INDEX.items()):
        path = corpus_dir() / meta["file"]
        rows.append(
            {
                "doc_id": doc_id,
                "file": meta["file"],
                "phase": meta["phase"],
                "register": meta["register"],
                "summary": meta["summary"],
                "exists": path.is_file(),
            }
        )
    return json.dumps(
        {
            "corpus_dir": str(corpus_dir()),
            "hf_mirror": HF_DATASET,
            "documents": rows,
        },
        indent=2,
    )


@mcp.tool()
def read_physics_doc(doc_id: str) -> str:
    """Read a physics corpus document by doc_id (e.g. proof, reproduce, riesz_proof, ca_preprint)."""
    doc = read_doc(doc_id)
    header = (
        f"# {doc['doc_id']} · {doc['phase']} · {doc['register']}\n"
        f"Path: {doc['path']}\n"
        f"Summary: {doc['summary']}\n\n---\n\n"
    )
    return header + doc["content"]


if __name__ == "__main__":
    mcp.run()
