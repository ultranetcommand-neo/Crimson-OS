"""Corpus paths and phase register for Geometric Unity physics MCP."""

from __future__ import annotations

import json
import os
from pathlib import Path

BRICK_DIR = Path(__file__).resolve().parent
DEFAULT_CORPUS = BRICK_DIR.parent.parent / "Geometric_Unity_Validation"
HF_DATASET = "https://huggingface.co/datasets/UltranetCommand/geometric-unity-physics"


def corpus_dir() -> Path:
    env = os.environ.get("GEOMETRIC_UNITY_CORPUS") or os.environ.get("CRIMSON_OS_GU_PATH")
    if env:
        return Path(env).expanduser().resolve()
    return DEFAULT_CORPUS.resolve()


CORPUS_INDEX: dict[str, dict[str, str]] = {
    "proof": {
        "file": "proof.md",
        "phase": "CRYSTAL",
        "register": "theorem",
        "summary": "F₂ ↪ SO(3), cos θ = ⅓ — theorem anchor and register separation table",
    },
    "reproduce": {
        "file": "REPRODUCE.md",
        "phase": "LIQUID",
        "register": "empirical_gate",
        "summary": "Blind JHTDB ablation reproduction protocol",
    },
    "geometric_unity_monolith": {
        "file": "Geometric_Unity_Monolith.tex",
        "phase": "LIQUID",
        "register": "physics_narrative",
        "summary": "T₁₁₂=6328, E₈, CA, Navier-Stokes, Orch-OR unified monolith",
    },
    "logos_invariant_monolith": {
        "file": "The_Logos_Invariant_Monolith.tex",
        "phase": "LIQUID",
        "register": "scripture_geometry_bridge",
        "summary": "Scripture → geometry → biology chain monolith",
    },
    "riesz_proof": {
        "file": "pressure_hessian_riesz_proof.tex",
        "phase": "CRYSTAL",
        "register": "theorem_companion",
        "summary": "Pressure Hessian Riesz bound companion derivation",
    },
    "t112_derivation": {
        "file": "poole_gibson_t112_derivation.md",
        "phase": "LIQUID",
        "register": "ca_derivation",
        "summary": "T₁₁₂ / B5-7/S5-9 derivation; Poole manifold = external benchmark only",
    },
    "ca_preprint": {
        "file": "gibson_poole_preprint.md",
        "phase": "LIQUID",
        "register": "ca_empirical",
        "summary": "CA validation vs independent Poole-manifold benchmark (not co-authored)",
    },
}


def read_doc(doc_id: str) -> dict[str, str]:
    doc_id = doc_id.strip().lower().replace("-", "_")
    if doc_id not in CORPUS_INDEX:
        known = ", ".join(sorted(CORPUS_INDEX))
        raise ValueError(f"Unknown doc_id '{doc_id}'. Known: {known}")
    meta = CORPUS_INDEX[doc_id]
    path = corpus_dir() / meta["file"]
    if not path.is_file():
        raise FileNotFoundError(f"Corpus file missing: {path}")
    return {
        "doc_id": doc_id,
        "path": str(path),
        "phase": meta["phase"],
        "register": meta["register"],
        "summary": meta["summary"],
        "content": path.read_text(encoding="utf-8", errors="replace"),
    }


def jhtdb_verdict() -> dict:
    path = corpus_dir() / "jhtdb_ablation_results.json"
    if not path.is_file():
        raise FileNotFoundError(f"JHTDB results missing: {path}")
    data = json.loads(path.read_text(encoding="utf-8"))
    v = data.get("verdict") or {}
    beats_random = v.get("candidate_beats_random", data.get("candidate_beats_random"))
    beats_median = data.get("candidate_beats_random_median")
    verdict = {
        "phase": "LIQUID",
        "register": "empirical_lemma",
        "status": "NEGATIVE" if beats_random is False else "INCONCLUSIVE_OR_POSITIVE",
        "candidate_beats_random": beats_random,
        "candidate_beats_random_median": beats_median,
        "candidate_ratio": v.get("candidate_ratio"),
        "random_median_ratio": v.get("random_median_ratio"),
        "run_utc": data.get("run_utc"),
        "dataset": data.get("dataset"),
        "n_points": data.get("n_points"),
        "interpretation": (
            "NEGATIVE: published ablation did not beat VF-matched random subsamples. "
            "Theorem (cos θ = ⅓) is independent of this result."
            if beats_random is False
            else "See full jhtdb_ablation_results.json — verdict requires human read."
        ),
        "hf_mirror": HF_DATASET,
        "reproduce": "REPRODUCE.md — run jhtdb_ablation_controls.py",
    }
    return verdict


PHASE_REGISTER_TABLE = """| Claim | Register | Phase | Source |
|-------|----------|-------|--------|
| cos θ = ⅓ (F₂ ↪ SO(3)) | theorem | CRYSTAL | proof.md, riesz_proof.tex |
| JHTDB filter beats random | lemma (empirical) | LIQUID — NEGATIVE | jhtdb_ablation_results.json |
| Navier-Stokes global regularity from geometry | lemma | LIQUID | geometric_unity_monolith.tex |
| Orch-OR / 13 protofilaments | lemma | LIQUID | geometric_unity_monolith.tex |
| T₁₁₂ CA 99.96% match | lemma | LIQUID | ca_preprint, t112_derivation |
| Poole B5-7/S5-9 benchmark | external_reference | — | Not co-authorship |

Rule: CRYSTAL theorem does not auto-promote any LIQUID lemma."""

PROOF_ANCHOR = """# Proof Anchor — F₂ ↪ SO(3), cos θ = ⅓

**Phase:** CRYSTAL (earned geometry — independent of empirical bridges)

## Statement

There exists a rigid Hausdorff constraint for the minimum rotation angle θ at which
the free group F₂ embeds in SO(3):

    cos θ = 1/3

This is the Logos geometric anchor. Closed mathematics in the theorem register.

## Full derivation files

- riesz_proof → pressure_hessian_riesz_proof.tex
- geometric_unity_monolith → Geometric_Unity_Monolith.tex (broader narrative)

## Empirical gate (separate register)

Use get_jhtdb_verdict — includes negative result. Consensus does not count.
"""
