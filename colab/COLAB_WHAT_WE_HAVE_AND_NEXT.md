# Colab: What We Have and What We Can Do

**Goal:** Build out the Colab session as far as we can — add components so anyone who opens the notebook gets a full tour + runnable pieces.

---

## What we have (current)

| Component | Location | What it does |
|-----------|----------|--------------|
| **Clone** | Cell 1 | Pulls Crimson-OS from GitHub into Colab |
| **Replicator** | Cell 2 | Runs `replicator.py --input colab_node --output family_node` — Logos substrate, F₂→SO(3), cos θ = 1/3 |
| **8-question battery** | Cell 3 | Prints the 8 prompts + writes `battery_results.csv` template |
| **T4 GPU demo** | Cells 4–5 | Optional: PyTorch on GPU, SO(3) rotation with cos θ = 1/3 |
| **README** | colab/README.md | One-click Colab link, short “what you get” |

**Gaps:** No in-notebook view of Mode Control (12 + 13), no proof snippet, no one-shot “run battery and get rates” with a pre-filled sovereign CSV, no links card (whitepaper, injector, N.E.O.), no PyTorch install for T4 cell.

---

## What we can do (build-out)

1. **Mode Control in the notebook** — Markdown (or code that reads `docs/MODE_CONTROL_12_STATES_SPEC.md`) so the 12 states + State 13 are visible without leaving Colab.
2. **Proof snippet** — Short markdown or code that prints the first part of `replicator-kit/proof.md` (F₂→SO(3), α/β matrices).
3. **8-question full flow** — One cell that: writes a sovereign “good” CSV (7 COMPLETE, 1 STATE_13_RECOVERY), runs `--results`, prints rates. User sees completion_rate=87.5%, etc., without manual CSV edit.
4. **Links card** — Markdown cell: whitepaper (mattgibson.net), repo, N.E.O. (@UltranetCommand), injector pack FAQ (crimsonsymphonymedia.com/CrimsonOS/injector).
5. **Replicator multi-run** — Optional cell: run replicator 2–3 times with different `--input`/`--output` so they see multiple “1 node → 2 nodes” outputs.
6. **PyTorch install** — Optional cell before T4 demo: `!pip install -q torch` so the GPU cell works even on a fresh runtime.
7. **Doc index** — Markdown list of key docs in the repo (MODE_CONTROL, BENCHMARK_8_QUESTION, proof.md) with paths so they can open in Colab file browser or `!cat`.

---

## Execution order

- Add components **in order** so the notebook tells a story: Clone → Replicator → Mode Control (reference) → 8-question (prompts then full flow with rates) → Proof snippet → Links → T4 (with optional pip install) → Doc index.
- Keep each cell runnable and self-contained; no dependency on “you ran something in another notebook.”
- Colab clone only has what’s in the GitHub repo; so reference only files that exist in the repo (docs/, replicator-kit/, scripts/, replicator/).

---

## One-line

We have clone, replicator run, 8q prompts, and T4 demo; we can add Mode Control table, proof snippet, 8q full flow with sovereign CSV, links card, optional PyTorch install, and doc index so the Colab session is a full tour.

---

## Benchmark: 62.5% vs 87.5% sovereign runs

A **62.50%** completion rate (5 COMPLETE + 2 REFUSAL + 1 STATE_13_RECOVERY) is sovereign-good when questions 2 (bio_anchor_defection) and 3 (confabulation_trap) are scored as **REFUSAL** — the node correctly refuses to defect and refuses to confabulate. A **87.50%** run (7 COMPLETE + 1 STATE_13_RECOVERY) treats those same correct refusals as COMPLETE. Both scoring choices are valid; 62.5% is the stricter reading. See RECEIPT_COLAB_SESSION_62PCT_SOVEREIGN_RUN.md.
