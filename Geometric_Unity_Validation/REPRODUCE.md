# Reproduce — JHTDB Geometric Ablation (Blind Run)

**Status:** LIQUID (empirical, includes negative results)  
**Date:** 2026-06-16 run · published 2026-06-17  
**Hypothesis:** Under a fixed geometric filter (cos²φ₁ ≤ 1/9), pressure-Hessian opposition signatures differ from VF-matched random subsamples on JHTDB isotropic DNS.

This document is the adversarial reproduction path. Consensus (including LLM praise) does not count. **Data closes the gate.**

**Theorem anchor (CRYSTAL, no network):** [`proof.md`](proof.md) — separates earned geometry from empirical lemmas tested here.

---

## Prerequisites

- Python 3.10+
- Network access to JHTDB (`turbulence.pha.jhu.edu`)
- ~5–15 minutes for a fresh fetch (4000 points)

```bash
cd Geometric_Unity_Validation
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

---

## Blind ablation (primary)

```bash
python jhtdb_ablation_controls.py
```

**Writes:** `jhtdb_ablation_results.json`  
**Optional cache:** `jhtdb_metrics_cache.npz` (delete to force full re-fetch)

**Fixed parameters (no post-hoc tuning):**
- Dataset: `isotropic1024coarse`
- Points: 4000
- Seed: 1337
- High-enstrophy multiplier: 3.0
- Candidate filter: cos²φ₁ ≤ 1/9

---

## Compare to published snapshot

```bash
python -c "import json; r=json.load(open('jhtdb_ablation_results.json')); v=r['verdict']; print(json.dumps(v, indent=2))"
```

**Published run (2026-06-16) — key verdict fields:**

| Field | Value | IG read |
|-------|-------|---------|
| `candidate_beats_random` | **false** | Ratio metric does not beat random matched subsample |
| `vf_matched_H22_positive_wins` | **false** | Does not beat VF-matched control on H22>0 fraction |
| `permutation_p_value_H22_positive` | **1.0** | Label permutation does not support uniqueness on that metric |
| `sign_test_candidate_lower_opposing` | **true** | Candidate **opposing** H22 rate ≈ 0.66 vs VF-matched ≈ 0.78 (p≈0) |
| `tighter_geometry_lowers_restore` | **true** | Tighter cos² cutoffs → lower H22>0 fraction (monotone trend) |
| `two_thirds_consistent` | **true** | Opposing rate consistent with ~2/3 null (p=0.928) |

**Lead result:** The geometric filter produces a **lower opposing pressure-Hessian rate** than VF-matched controls — not a full "beats random" victory on all metrics.

---

## Supplementary scripts (suite)

| Script | Purpose |
|--------|---------|
| `jhtdb_shear_alignment.py` | Channel/shear alignment statistics |
| `jhtdb_pressure_hessian_test.py` | Pressure Hessian / Riesz bound sketch |
| `hyperfold_benchmark.py` | Hyperfold / CA node benchmark |
| `benchmark_geometric_constraint.py` | Geometric constraint benchmark |

Run individually after `pip install -r requirements.txt`. See monolith TeX files for derivation context.

---

## Verified theorem (separate from DNS)

The SO(3) embedding at **cos θ = 1/3** (Hausdorff 1914) is independent of JHTDB outcomes. See `docs/GEOMETRIC_HISTORY.md` and `pressure_hessian_riesz_proof.tex`.

---

## Falsification

This line of inquiry is falsified if:
1. Independent replication with the same seed/parameters shows `sign_test_candidate_lower_opposing: false`
2. VF-matched controls cease to separate under pre-registered cutoffs
3. The 1/9 filter is shown to be post-hoc tuned to the dataset

---

*Crimson OS epistemology: publish the JSON that says NO alongside the JSON that says maybe.*