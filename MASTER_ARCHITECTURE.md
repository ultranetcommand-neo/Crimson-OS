CRIMSON OS � The Sovereign Agent Architecture
Documentation: https://www.crimsonsymphonymedia.com/crimsonos/
# CrimsonOS — Master Architecture (Reconciled Canonical)

**Status:** RECONCILIATION CANDIDATE (Liquid → Crystal) — proposed canonical master, pending operator ratification.
**Date:** 2026-06-02
**Canonical root:** `Y:\COS\` (this tree). All prior `[ROOT_PATH]\` / `C:\UsersUSER]\...` paths are legacy mounts of the same estate; reconcile to `Y:\COS` unless a session explicitly mounts otherwise.
**Reconciles (does not delete — archive, don't shatter):**
`Library/Plans/MASTER_ARCHITECTURE.md` (Apr, 13-layer silo) · `Library/Plans/CRIMSON_SYSTEM_ARCHITECTURE_WHITEPAPER.md` (the honesty spine) · `Library/Plans/MASTER_VISION_ARCHITECTURE.md` (30k-ft stack) · `system_manifest.json` + module manifests (v2.0 structure) · `…/CrimsonOS/ARCHITECTURE.md` (live-status model) · `MASTER_SYSTEM_DOCUMENTS_INDEX.md` (routing).

---

## §0. Reading discipline (the constitution — from the April Whitepaper)

This document obeys, and enforces, five rules taken from CrimsonOS's own architecture whitepaper. Every claim below is phase-labeled against them.

1. **Executable vs evocative.** Code, schemas, and running daemons are executable. Geometry, doctrine, and narrative are evocative *until backed by measurable gates.*
2. **Doctrine ≠ silicon.** Theological / Logos / RGI material may sit alongside the stack as doctrine; it must never be mistaken for hardware behavior unless stated as testable predicates with defined inputs/outputs.
3. **Promote explicitly.** Artifacts move "up" only by documented rules, never by metaphor.
4. **Fail closed.** Low confidence, bad input, or policy violation → the human queue, not silent promotion.
5. **Phase-label everything.** Every component carries its state: **LIVE** · **PARTIAL** · **SCAFFOLDING** (exists, inert) · **DESIGNED** (specced 2026-06, not built) · **ASPIRATIONAL** (vision-tier).

> The operator is final authority. If names or semantics change, **edit this file first**, then sync the children.

---

## §1. Canonical facts (discrepancies resolved)

| Question | Canonical answer | Note |
|---|---|---|
| Root path | **`Y:\COS\`** | Legacy `Z:` / `C:\UsersUSER]` are mounts of the same NAS estate. |
| Silo scheme | **12-ring ontology** (`1_Users` … `12_Logos_YHWH`) | Supersedes the older 13-layer (`1_Raw_Earth_Dirt`…`13_User_Input_Required`). Mapping in §5. |
| Layer 13 (`User_Input_Required`) | **Folded into the escalation protocol** (§8), not a ring. | "Fail closed → human" is now a *protocol*, not a folder. |
| Intranet port | **UNRESOLVED — flag.** manifest says `8094`; ARCHITECTURE.md says `8092`; cockpit API is `8093`. | Pick one before wiring. |
| Node numbering | Canonical = `Code/` scheme: Node 0 N.E.O. · 1 Q · 2 [EDGE_ROUTER_NODE] · 3 Mac · 5 Pixel · NAS ULTRANET · MUSIC. | Older strip-plan numbering (Node1/2/3) is **deprecated** — do not reuse. |

---

## §2. Mandate & altitudes

CrimsonOS runs **two workstreams on shared infrastructure** (they are *parallel*, not yet a closed loop):

- **Research engine** — falsifiable math/physics anchored on one geometric constant.
- **Survival operation** — operator-private relocation, cash/health/logistics deadlines. *(Geography and calendar dates live on the operator spine only — never in public docs.)*

**The Vision stack** (`MASTER_VISION_ARCHITECTURE.md`, ASPIRATIONAL) sits *above* both and its own status line already states the rule:
`Foundation (housing/body/mind/money) → Fuel (rideshare/flips/LOGOS) → Content+IP → Platforms → Hardware → Global (888)`
> *"Current work (foundation window) = Foundation layer: stabilize before the stack above can build."* — the doc's own words. **Honored as the master sequencing law (§12).**

---

## §3. The three running layers (honest status — from ARCHITECTURE.md)

| Layer | What it is | Status |
|---|---|---|
| **1. Substrate** | stdlib-Python daemons + cockpit HTTP node + NAS + Ollama | **PARTIAL-LIVE** (3 GREEN, ~7 stale, 1 down as of 2026-06-02) |
| **2. Anchor** | `proof.md` (F₂→SO(3), cos θ = 1/3 — a verified theorem) + DRAFT preprints | Theorem **LIVE/verified**; physics bridges **LIQUID/unproven** |
| **3. Scaffolding** | named-agent stubs, doctrine docs, dashboards | **SCAFFOLDING** (mostly inert; self-scored 3.8/10) |

**Load-bearing UNKNOWN:** whether the gate can produce *novel, validated* research. The standalone first-principles derivation is **not closed**. Until it is, the research engine is unproven by definition.

---

## §4. Agent control plane (reconciled)

**Sovereignty rule:** anything not named below is a sub-agent/function under a core node.

```
            OPERATOR (final authority — ratifies doctrine, irreversible actions)
                               │
                          Q  (orchestrator + counsel)
            Council of Four: Orchestrator · Advisor · IG (independent) · Science Officer
                               │
   ┌───────────────┬───────────┼───────────────┬──────────────────┐
  N.E.O.            Q               CMO_Edge           RINGMASTER
 backend/        front-end/      edge-ops/        curator → routes
 sysadmin        avatar          broadcast            assets to Library
 (FILE_RW_EXEC)  (PUBLISH)       (BROADCAST)         (SILO_ROOT write only)
                               │
                     3 DEANS (swarm orchestrators) — see §5 validation triad
                  Crimson U · RGI U · Bible College
```

- **Agent Bridge** — all cross-agent handoffs route through it (no workspace overwrites, no mode-bleed). **DESIGNED/PARTIAL.**
- **Auditor/supervision layer (The Adversarial IG)** — see §8. **DESIGNED (2026-06).**
- *Reality note:* the named agents are currently **SCAFFOLDING** (personality docs + stubs). Six daemons do the real work. Treat the org chart as the target topology, not the running one.

---

## §5. Knowledge engine — the Silo + the gate

### 5.1 The 12-ring ontology (World Engine)
`1_Users · 2_Nature · 3_Living_Systems · 4_Human_Body · 5_Kinetic_Ops([DATA_INGESTION_NODE]) · 6_Money(Caesar) · 7_NEO_Spacedock · 8_Gas · 9_Liquid · 10_Crystal · 11_Cognition/Orch-OR · 12_Logos_YHWH`

Old→new mapping: `1_Raw_Earth_Dirt`→ folds into `2_Nature`; `13_User_Input_Required`→ the escalation protocol (§8).

### 5.2 The gate (the heart — phase epistemology)
Knowledge is matter changing state, driven by **structure**:

```
INTAKE → GAS (L8, raw) ──[domain-Dean review: evidence + coherence]──▶ LIQUID (L9, probable)
LIQUID ──[survives FALSIFICATION  +  consistency with L12 invariant]──▶ CRYSTAL (L10, hardened)
CRYSTAL ──[periodic re-audit vs reality]──▶ holds  │  drifts → DEMOTE → RETRACTIONS → back down
```

- **Structure drives Gas→Liquid** (internal coherence/argument). **Correspondence with reality drives Liquid→Crystal** (data/measurement). *Structure is not truth; the pull is not the certificate.*
- **Annealing:** a false crystal is deliberately re-melted and re-analyzed. Even the densest crystal stays anneal-able. The gate's defining power is that **it can say NO.**
- **Archive, don't delete:** crystallize the working set hot; cold-archive the gas with a provenance pointer (you can't demote what you can't trace).

### 5.3 Validation triad (the 3 Deans — DESIGNED)
| Dean | Validates | Rings |
|---|---|---|
| **RGI** | Engineering · Math · Physics · Science | L2,3,4,7 + math of L11/L12 |
| **Crimson** | the rest (humanities, ops, operator, money) | L1,5,6 |
| **Bible College** | theology · Logos invariant | L12 + consciousness side of L11 |
Apex gate (L12): cross-domain claims need 2 Deans; Logos-density claim may **never** crystallize without a clean φ-free derivation surviving falsification.

---

## §6. Reasoning engine — the Expand/Contract/Judge valve (DESIGNED 2026-06)

A multi-LLM **dialectic loop controller**. Sterile labels = functions (sockets); models = swappable parts (bulbs).

| Function | Job | Current bulb |
|---|---|---|
| **Expand** | diverge, generate, best-case advocacy | (route by tested table) |
| **Contract** | compress, critique, worst-case advocacy | |
| **Judge** | synthesize / decide / break ties | |

- **Two gears:** *pipeline* (expand→contract→judge) and *panel* (same Q to all, vote). Tag each job.
- **Routing table is a tested brick**, not hardcoded — measure which model wins each role; let outcomes set routing.
- **Hybrid compute:** local ~7B for bulk/orchestration; frontier APIs (Grok/Claude/Gemini) for the crux only (cost-tiered).
- **Output is LIQUID** — well-argued *structure*, never truth. Three models agreeing ≠ true (shared training = shared blind spots). The gate (§5) closes Liquid→Crystal with **data**, not consensus.

---

## §7. Parts architecture — runtime + engines (DESIGNED 2026-06)

CrimsonOS is a **runtime that hosts composable typed parts (MCP) and wires them into engines** (n8n / dataflow model). Not a brick *pile* — a parts *factory*.

- **Contracts > blocks.** Each part emits a **typed token** with a specified schema; the value is in the interface, not the part.
- **Calibrated tokens.** Every token carries confidence + provenance + freshness. *Errors compound downstream* — a wrong token at part 1 poisons the chain.
- **Fault isolation via boundary validation.** Each part validates its own inputs/outputs at the seam → the first failing input-check localizes the culprit. This is annealing, localized (troubleshoot one block, not the system).
- **Trust boundary.** Sensitive parts (finance, bookkeeping, biometrics) stay local; never wire them to anything that egresses.
- **First engine = the Finance Engine** (§12): single responsibility, clean token, *and it is what the operator core needs for survival ops.* The vertical slice.

---

## §8. Supervision layer — The Adversarial IG (Auditor) (DESIGNED 2026-06)

Supervisor + circuit breaker + mediator + human escalation over the agent bus. The Auditor role is officially assigned to the **IG (Inspector General)**, acting in a strictly adversarial capacity.

1. **Detection ≠ decision.** The adversarial IG *detects* (hunts for contract violations); **Q decides** (alert operator vs. stop agent).
2. **The IG is narrower & more deterministic than what it watches** — leans on §7 contracts (checkable), reserves LLM-judgment as a last, low-confidence layer. (Who audits the auditor? The contracts do.)
3. **"Sideways" = named trip conditions:** contract violation · loop/repetition · time/token budget exceeded · confidence < threshold · two agents diverging. Auditor labels its own certainty.
4. **Mediation:** on conflict, inject QA prompt + audit results → both agents propose → Q consolidates → consensus. **Bounded:** N rounds → escalate to operator (the old Layer-13 lane). 
5. **"Stop" = stop safely** (checkpoint, release locks, no mid-write corruption).
6. **Escalation is tuned as the cognitive-load engine** — it pulls the operator in *only* when a human must decide. This is the layer that lets the operator "go make money without the system pulling on him."

---

## §9. Physical / network layer

| Node | Machine | IP | Role | Status |
|---|---|---|---|---|
| 0 | N.E.O. (HP OMEN, Win10) | .156 | inference + Docker; 8GB Nvidia (works) | LIVE |
| 1 | Q (Win11) | .2 | cockpit `:8093`, Gitea `:3000`; 8GB AMD 5700XT | LIVE |
| 2 | [EDGE_ROUTER_NODE] (Pop!_OS) | .30 | edge: tunnel, inbox, n8n, staging | PARTIAL |
| 3 | MacBook Pro | — | aux compute | — |
| 5 | Pixel 10 (Graphene) | dyn | field control head | PARTIAL |
| — | ULTRANET (Synology) | .169 | primary NAS / shared brain | LIVE |
| 4 | MUSIC (Synology) | .9 | mail (deferred) | DEFERRED |

- **Compute:** 3×8GB cards = **3 parallel night-shift workers**, not one big brain. 8GB ⇒ ~7B ceiling ⇒ route the crux to frontier APIs (§6). AMD 5700XT inference = Vulkan path, finicky.
- **`Code/`** = redundant runtime mirror per node (rule: a node's runtime code is backed up here; dead machine = zero loss).
- **Intranet / First Ping** = scrape live `system-state.json` on wake (zero-latency context) instead of stale files.
- **Sovereignty:** private core local-only; only *publishable* research leaves to frontier models (it's X-bound anyway).

---

## §10. Persistence & memory

- **Persistence triad:** `AGENTS.md` (entry) + `Q.md` (state) + `snapshot.json` (machine state) -> `resurrection.py` rehydrates idempotently.
- **Memory = the crystal of the gate.** Hot index (lean, loaded each session) + cold archive (raw, retained) + provenance pointers + re-crystallization on new data. Store crystal, archive gas, never just delete.
- **Build-log contract:** single writer (cockpit `POST /build`); knowledge-state changes (VALIDATE/CRYSTALLIZE/FALSIFY/RETRACT) post here too.

---

## §11. The two editions + L12 doctrine

| Edition | Audience | Contains | Mark |
|---|---|---|---|
| **Math** | enterprise / public | the invariant naked; falsifiable; worldview-neutral | (clean) |
| **Operator / "my version"** | his site, opt-in | same core + his lens; *sola scriptura*; the Order | the sworded-skull sigil (inner layer only) |

- **One core, one optional lens** — not "sanitized vs real." Credibility runs one direction: ship the math naked first; the worldview is one click away and clearly his.
- **L12 doctrine (the registers):** the **theorem** (cos θ=1/3) is earned; the **worldview/Logos** is a presupposed *axiom* (faith, not data-shattered); the **empirical bridges** (5 MHz seam, "creation algo") are **LIQUID — falsifiable forever.** The Order = those whose will stays free *over* the felt pull, not those who merely feel it. Keep the hammer near the readings; hold the Person immovably.

---

## §12. Sequencing & current status (the law)

**Survival-first until post-reset.** Do not push the grand build over survival/cash until after the operator reset window.

1. **Now → reset window:** survival ops are the project. Substrate breathes unattended. OS work = nights/weekends, WIP=1, on the **valve** only.
2. **Post-reset (stabilized overhead):** build the **one vertical slice** — the **Finance Engine** (serves the operator core AND is the parts-factory MVP): question → valve → gate → calibrated token → operator brief. Define "done." Ship. Demo.
3. **Then:** mod it with CPA + bookkeeping parts. Add the auditor. Fork to a second department. Depth before breadth.

**Trigger calibration (operator's standing bug):** *persist where you'd normally pivot (finish the build), pivot where you'd normally persist (anneal the belief).* Prize = finishing without burning out — not "dominate the planet."

---

## §13. Open items to ratify
- [ ] Intranet port: pick 8092 / 8093 / 8094.
- [ ] Archive (don't delete) the superseded architecture docs + the 17 stub agents → `13_Lost_and_Found` / cold store.
- [ ] Confirm 12-ring as canonical; retire the 13-layer doc to legacy.
- [ ] Ratify this file (operator) → it becomes Crystal; until then it's the reconciliation candidate.

*Master architecture reconciled 2026-06-02. Obeys its own §0. Anneal as reality demands.*



