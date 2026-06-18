# Crimson OS — Silo Index (Public Aperture)

**Purpose:** One-page map for external reviewers (Copilot, autoarxiv, contributors).  
**Date:** 2026-06-18  
**Scope:** Public GitHub only — no NAS, biometrics, finance, or operator-private corpus.  
**Canonical spec:** `MASTER_ARCHITECTURE.md` · **Gate:** GAS → LIQUID → CRYSTAL

## Concept maps (Logos Invariant — 5 spokes)

| Asset | Path |
|---|---|
| Operator mind-map (5 validation spokes) | [`docs/images/logos_invariant_map.jpg`](docs/images/logos_invariant_map.jpg) |
| NotebookLM export (full resolution) | [`docs/images/notebooklm_logos_invariant.png`](docs/images/notebooklm_logos_invariant.png) |

**Spoke → repo:** Geometric & Mathematical → `Geometric_Unity_Validation/` · Physical & Biological → L3/L4/L11 + JHTDB/CCDE · Linguistic & Theological → L12 `logos.md` · Crimson OS Architecture → `MASTER_ARCHITECTURE.md` · Core Methodology → GAS→LIQUID→CRYSTAL gate.

---

## Phase labels (read every row through this)

| Tag | Meaning |
|---|---|
| **CRYSTAL** | Verified theorem, published run artifact, or operator-ratified doctrine |
| **LIQUID** | Argued + falsifiable; not closed |
| **LIVE** | Runnable or deployed today |
| **PARTIAL** | Exists; stale or incomplete |
| **SCAFFOLDING** | Named structure; mostly inert |
| **DESIGNED** | Specced; not built |
| **ASPIRATIONAL** | Vision-tier; must not load boot path |

**Reviewer rule:** Consensus does not count. Start with `Geometric_Unity_Validation/REPRODUCE.md` and `jhtdb_ablation_results.json` — includes **negative** headline results.

---

## Epistemic registers (symbolic vs objective)

**Status:** **DOCUMENTATION ONLY** — not enforced in silicon on the public repo today.

| Register | Meaning | Example | Typical ring |
|---|---|---|---|
| **`physical_state`** | Immutable measurement / textbook invariant | ¹²C: 6p/6n/6e; cos(109.5°)≈−⅓ | L2–L4 |
| **`closed_math`** | Integer proof; no physics claim | 37/73; T₁₂=6328 | L12 |
| **`theorem`** | Earned geometry | cos θ = ⅓; F₂↪SO(3) | L10/L12 |
| **`lemma`** | Explicit bridge between registers | supplement −⅓ ↔ embedding +⅓ | L9→L10 |
| **`symbolic_overlay`** | Human/cultural mapping; `root_write: false` | 666↔materialism; 777↔ascension | L12 (Operator) |

**Protected truth layer (today):** `MASTER_ARCHITECTURE.md` §0 (doctrine ≠ silicon), §11 (Math vs Operator editions), ring placement in this index, per-file `register` headers, `schemas/build_log_entry.schema.json`, and `Code/epistemic_gate/gate.py` (append-only stub). **Not built:** single-writer filelock/DuckDB ledger, cockpit `POST /build`, `nas_ledger_client.py` (Gemini cites this — **not in repo**; `neo_tetrahedron.py` uses **simulated** `_read_nas_ledger`).

**Carbon partition:** `Silo/2_Nature_Physical_World/carbon_isotopes.md` — physical counts vs partitioned overlays.

---

## The 12 rings (ontology)

```
L1 Users ──► L2 Nature ──► L3 Living ──► L4 Body ──► L5 Kinetic ──► L6 Money
    │                                                              │
    └────────────────────── L7 Spacedock ◄─────────────────────────┘
                                    │
              L8 Gas ──► L9 Liquid ──► L10 Crystal ──► L11 Cognition ──► L12 Logos
```

| Ring | Path | One-line purpose | Phase | Public artifacts |
|---|---|---|---|---|
| **L1** | `Silo/1_Users/` | Operator identity, preferences, escalation identity | SCAFFOLDING | README stub |
| **L2** | `Silo/2_Nature_Physical_World/` | Physics, materials, environmental constraints | PARTIAL | `carbon_isotopes.md` (`physical_state`) |
| **L3** | `Silo/3_Living_Systems/` | Biology, ecology, living-system models | SCAFFOLDING | README stub |
| **L4** | `Silo/4_Human_Body/` | Biometrics lane, health substrate (Doctor Crusher) | DESIGNED | README stub · see `docs/CCDE.md` §3 |
| **L5** | `Silo/5_Kinetic_Ops/` | Crew chief / kinetic ops, hardware veto, C-141 intake | SCAFFOLDING | README · CCDE Class II/IV |
| **L6** | `Silo/6_Money_Manager_Caesar/` | Finance, logistics, threat archetypes | SCAFFOLDING | README stub |
| **L7** | `Silo/7_N.E.O._Spacedock/` | Hardware experiments, cluster/WVU lane | ASPIRATIONAL | README stub |
| **L8** | `Silo/8_Brain_Gas_Phase/` | Raw intake — unverified LLM / telemetry | SCAFFOLDING | README stub |
| **L9** | `Silo/9_Brain_Liquid_Phase/` | Probable claims after adversarial review | LIQUID | README stub · JHTDB suite |
| **L10** | `Silo/10_Brain_Crystal_Phase/` | Hardened truths — anneal-able | PARTIAL | `crystal_phase_truth.md` |
| **L11** | `Silo/11_Cognition_Neuroscience_Orch_Or/` | Consciousness / Orch-OR bridge | LIQUID | `cognitive_substrate_map.md` · manifest |
| **L12** | `Silo/12_Logos_YHWH/` | Logos invariant, checksum, theology register | MIXED | `logos.md` · manifest · `Sola_Scriptura_*.md` |

**Not a ring:** `Silo/13_Archive_Strays/` — cold storage for demoted / superseded docs.  
**Escalation protocol:** Human veto (legacy “Layer 13”) — `MASTER_ARCHITECTURE.md` §8, Bin 13 in Crusher spec. Not a knowledge ring.

---

## Gate placement (what promotes where)

| Artifact | Ring | Register | Phase | Falsification entry |
|---|---|---|---|---|
| F₂↪SO(3), cos θ = 1/3 | L10 / L12 | `theorem` | **CRYSTAL** | `Geometric_Unity_Validation/proof.md` · monolith TeX |
| JHTDB pressure-Hessian ablation | L9 | `lemma` (empirical) | **LIQUID** | `REPRODUCE.md` → `jhtdb_ablation_controls.py` |
| `candidate_beats_random: false` | L9 | `lemma` (empirical) | **LIQUID** (honest negative) | `jhtdb_ablation_results.json` |
| ¹²C / ¹³C particle counts | L2 | `physical_state` | **CRYSTAL** | `carbon_isotopes.md` |
| cos(109.5°) ≈ −⅓ (sp³ carbon) | L2 | `physical_state` | **CRYSTAL** | Textbook geometry; bridge to +⅓ = `lemma` |
| 37/73 gematria checksum | L12 | `closed_math` | **CRYSTAL** | `logos.md` · monolith TeX |
| 666↔materialism, 777↔ascension | L12 | `symbolic_overlay` | **OPERATOR** | `root_write: false` · `carbon_isotopes.md` § overlays |
| 112 MHz carrier | L9 | `lemma` (hypothesis) | **DESIGNED** | No measurement cited |
| Orch-OR / microtubule QC | L11 | `lemma` | **LIQUID** | Literature bridge only |
| CCDE 8-class taxonomy | L5/L8–L10 | `symbolic_overlay` (ops) | **DESIGNED** | `docs/CCDE.md` |
| Agent org chart (Q, NEO, CMO) | Agent_Stack | — | **SCAFFOLDING** | Personality docs; 6 daemons do real work |
| Live daemon health | Code/Node_0 | — | **PARTIAL** | Not provable from GitHub alone |

---

## Load-bearing paths (start here)

| File | Why read it |
|---|---|
| `MASTER_ARCHITECTURE.md` | Reconciled master — phases, gate, nodes, sequencing law |
| `Geometric_Unity_Validation/proof.md` | CRYSTAL theorem anchor (separate from LIQUID lemmas) |
| `Geometric_Unity_Validation/REPRODUCE.md` | Blind reproduction; adversarial instructions |
| `Code/epistemic_gate/gate.py` | Register-enforced gate stub (append-only JSONL) |
| `scripts/startup.ps1` · `scripts/health_check.ps1` | Local intranet bootstrap + verifier |
| `Geometric_Unity_Validation/jhtdb_ablation_results.json` | Published verdict — **includes failures** |
| `docs/CCDE.md` | Crew Chief Diagnostic Engine — bifurcated engineering + provenance |
| `GLOSSARY.md` | Term definitions (RGI, gate, nodes) |
| `system_manifest.json` | Machine-readable routing for agents |

---

## Intentionally **not** in this repo

Private operator estate stays off GitHub:

- NAS / ULTRANET friction logs and hash-chained build ledger
- Live biometrics (Polar H10, Whoop)
- Finance detail, relocation logistics, DisruptPTSD clinical intake
- Full `OneDrive/Desktop/Truth` corpus
- Cockpit runtime state (`neo_pipeline_status.json` on Node 0)

Presence of stubs in L1/L4/L6 does **not** imply those datasets are published.

---

## External reviewer script (paste with this file)

```
Task: Audit Crimson OS using SILO_INDEX.md only.
1. List every CRYSTAL claim and cite the exact file that earns it.
2. List every claim marked LIVE that has no runnable proof in-repo.
3. Confirm whether jhtdb_ablation_results.json negative results are
   honestly represented in README and MASTER_ARCHITECTURE.
4. Flag circular dependencies between L11, L12, and L10.
5. Do not praise the architecture. Output: table of findings + severity.
```

---

## Related repos & editions

| Surface | URL / path |
|---|---|
| Public repo | https://github.com/ultranetcommand-neo/Crimson-OS |
| Operator site | https://www.crimsonsymphonymedia.com/crimsonos/ |
| Math edition | `Geometric_Unity_Validation/` (worldview-neutral runnable core) |
| Operator edition | `Sola_Scriptura_Systematic_Theology.md` (optional lens — same gate) |

*Silo index v1.2 — public aperture only. Operator ratifies → promote to CRYSTAL.*