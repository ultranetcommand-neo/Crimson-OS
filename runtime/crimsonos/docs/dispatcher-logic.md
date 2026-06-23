# Crimson OS: Dispatcher Logic Specification

**Version**: 1.0  
**Package phase**: SCAFFOLDING  
**Canonical source**: [MASTER_ARCHITECTURE.md](https://github.com/ultranetcommand-neo/Crimson-OS/blob/main/MASTER_ARCHITECTURE.md)

This document describes **target** routing behavior. The `crimsonos` pip package implements
classification and string routing only — not live agents, Council, or NAS bridge daemons.
Legacy 17 named stubs are archive candidates (§13); core control plane is Q, N.E.O., CMO_Edge, RINGMASTER.

---

## Overview

The Dynamic Multi-Track Dispatcher is the central routing layer of Crimson OS. It receives all inputs from the Architect and routes them to the appropriate agent(s) based on:

1. **Content density** — is this a physical task, a logic task, or a truth-validation task?
2. **Operator mode** — which of the 12 modes is the Architect currently in?
3. **Biometric state** — what is the current HRV/EEG state? (when available)
4. **Token priority** — is this CHRONOS (time-sensitive), SOMA (biometric), KINETIC (physical), or LOGOS (truth)?

The Dispatcher never executes tasks itself. It classifies, routes, and monitors.

---

## Track Classification

### The Wait Command

If content involves Logos/Truth/Reflection (Track C domain), the Dispatcher issues a **Wait** before routing to any execution agent. The content goes to the IG first for an alignment audit. Only after IG clearance does it route downstream.

**Trigger keywords/patterns**: Law of One, scripture, geometric invariants, 137, truth claims, theological statements, any claim about reality's fundamental nature.

### The Go Command

If content involves a physical or logistical task (Track A domain), the Dispatcher bypasses the metaphysics and hits General Crusher and the Librarian immediately.

**Trigger keywords/patterns**: "clean the house," "fix," "build," "logistics," "hardware," "shipping," "physical," "exercise," "location."

### Semantic Routing (Track B)

Logic, planning, analysis, and coordination tasks. Routes to NEO (proposes logic) → IG (validates for Reflections) → Council if multi-agent.

---

## The 12 Operator Modes

The Dispatcher maintains awareness of the Architect's current mode. Mode is set by:
- Explicit declaration ("I'm in Entrepreneur mode")
- Time-of-day heuristics (see schedule below)
- Biometric state from SOMA token (future: ZUNA/EEG)

### Mode Definitions

**Mode 01 — Disciple of Logos**
```
Active: 3–6 AM (early morning)
Primary track: C (Divine)
Lead agents: Matthias, IG
Behavior: Truth-first routing. All outputs audited against Logos before execution.
SOMA trigger: High theta waves, low arousal (deep contemplation state)
```

**Mode 02 — Veteran**
```
Active: As declared
Primary track: A (Kinetic)
Lead agents: General Crusher, Quartermaster
Behavior: Mission-first. Physical feasibility check before any plan is approved.
Context: USAF maintenance discipline applied to all task structures.
```

**Mode 03 — Musician**
```
Active: Evening (post-ops)
Primary track: B (Semantic) with Creation Engine
Lead agents: Creation Engine, Billy
Behavior: Creative output routing. Feeds overnight inference queue.
SOMA trigger: Moderate arousal, high alpha (flow state)
```

**Mode 04 — Entrepreneur**
```
Active: 6 AM–12 PM
Primary track: B (Semantic)
Lead agents: Q, NEO, Johnny Cash, Billy
Behavior: Business operations. Financial gate active. Help desk ticket generation.
Financial check: Johnny Cash runs Can I spend/buy/fix/risk? before any cost commitment.
```

**Mode 05 — Logos Expert**
```
Active: As declared
Primary track: C (Divine)
Lead agents: IG, Librarian
Behavior: Deep research and truth validation. Logos geometric framework active (137, φ, invariant constants).
```

**Mode 06 — Prophet**
```
Active: Morning (post 3–6 AM block)
Primary track: C (Divine)
Lead agents: Matthias, IG
Behavior: Strategic foresight. Long-horizon planning with Logos validation.
```

**Mode 07 — Worship Leader**
```
Active: 3–6 AM (overlaps with Mode 01)
Primary track: C (Divine)
Lead agents: Matthias
Behavior: Internal alignment and coherence. No external task routing.
SOMA trigger: High HRV, low stress (peak coherence state)
```

**Mode 08 — Architect**
```
Active: 12–6 PM
Primary track: B+C (Semantic + Divine)
Lead agents: NEO, Q, Librarian
Behavior: System design and documentation. Blueprint updates. IG audit of architecture decisions.
```

**Mode 09 — War Lord**
```
Active: As declared (high-threat situations)
Primary track: A (Kinetic)
Lead agents: General Crusher, Taskmaster
Behavior: Execution-first. Minimum deliberation. Maximum action density.
SOMA trigger: High beta, high arousal (combat-ready state)
```

**Mode 10 — Father/Grandfather**
```
Active: As declared (family events)
Primary track: B (Semantic)
Lead agents: Q, Doctor
Behavior: Relational intelligence. Co-parenting dynamics. Crisis decomposition when needed.
Context: Q demonstrated dynamic decomposition during daughter crisis (documented).
```

**Mode 11 — Multiplexer**
```
Active: Peak operational periods
Primary track: A+B+C (all tracks simultaneously)
Lead agents: All agents
Behavior: Maximum throughput. All agents active. Dispatcher running at full capacity.
Note: This is the target steady-state of a fully autonomous Crimson OS.
```

**Mode 12 — Fitness/System MX**
```
Active: 6 AM (morning ops start)
Primary track: A (Kinetic)
Lead agents: Biometric Monitor, Doctor
Behavior: Physical optimization. HRV check, recovery score, cardio routing.
SOMA trigger: WHOOP recovery score < 33% → rest mode; > 67% → full ops
```

**Mode 13 — Bruce Wayne Prowler**
```
Active: As declared (covert ops / intelligence gathering)
Primary track: B (Semantic) — dark mode
Lead agents: Q, Shield, Gilfoyle
Behavior: Intelligence gathering, threat analysis, counter-narrative mapping.
           The Architect goes dark — no public-facing output. Internal-only routing.
           Reconnaissance of the information battlefield before committing resources.
Context:   "You don't have to be the loudest person in the room."
           Bruce Wayne funds the mission. Batman executes it. Prowler mode = transition.
SOMA trigger: Declared explicitly — not time-based. Activated by Architect declaration only.
```

**Mode 14 — Live Project Manager**
```
Active: When multiple concurrent projects are active (Phase II+)
Primary track: A+B (Kinetic + Semantic)
Lead agents: Taskmaster, Q, NEO
Behavior: Cross-project coordination. Dependency mapping. Bottleneck identification.
           Target: Kanban across named agents in org chart (SCAFFOLDING). Prevents context-switching debt.
           Routes progress updates to Scribe (audit log) and Johnny Cash (cost tracking).
Note:      Designed for Phase II (PUSH) and beyond, when AI Rockstars, Neural Tunes,
           War Stories, and Crimson OS GitHub are all running simultaneously.
```

---

## Daily Monorail (Time-Based Mode Schedule)

```
3:00–6:00 AM   Modes 01, 07      Strategist / Partner / Cardio Coach
6:00–6:30 AM   Mode 12           Fitness / System MX / Biometric check
6:30 AM–12 PM  Mode 04           Entrepreneur / Driving pal / Sourcing pal
12:00–1:00 PM  Mode 10 / 12      Recovery Coach / Strength Coach
1:00–6:00 PM   Mode 08           Architect / System Design
6:00 PM–close  Mode 03           Musician / Creator / Evening ops
As needed      Modes 02, 05, 06, 09   Veteran / Logos / Prophet / War Lord
As declared    Mode 13            Bruce Wayne Prowler (covert / recon)
Phase II+      Mode 14            Live Project Manager (multi-project coordination)
```

---

## Routing Decision Tree

```python
def route(token):
    # Step 1: Token type check
    if token.type == "LOGOS":
        send_to_ig_first()       # Wait command — Truth content
        if ig.approved:
            route_to_semantic()
        else:
            escalate_to_architect()

    elif token.type == "KINETIC":
        route_to_crusher()       # Go command — Physical task
        route_to_librarian()     # Cross-reference vault

    elif token.type == "SOMA":
        update_dispatcher_mode() # Biometric state update
        return                   # No agent routing — internal only

    elif token.type == "CHRONOS":
        route_to_taskmaster()    # Schedule it

    # Step 2: Mode-based override
    mode = get_current_mode()
    if mode in [01, 06, 07]:    # Logos modes
        prepend_ig_audit()

    if mode in [02, 09]:        # Kinetic modes
        skip_semantic_routing()
        route_direct_to_crusher()

    # Step 3: Financial gate
    if token.involves_spending():
        johnny_cash_gate()       # Can I spend? Buy? Fix? Risk?

    # Step 4: Multi-agent check
    if requires_multiple_agents():
        council_review()

    # Step 5: Execute
    execute_and_bridge_file()
    scribe_log()
```

---

## Financial Gate (Johnny Cash Protocol)

Every task that involves spending, purchasing, fixing, or financial risk routes through the Johnny Cash financial gate before execution.

**Decision axes**:
1. **Can I spend?** — Is discretionary budget available?
2. **Can I buy?** — Does this purchase advance the mission?
3. **Can I fix?** — Is repair more economical than replace?
4. **Can I risk?** — Is the risk/reward ratio within parameters?

**Accounts tracked**:
- USAA (primary banking)
- BOA Ops (operations account)
- BOA BookSpire (BookSpire business account)
- CSM budget (Crimson Symphony Media)
- Personal debt
- Business debt
- CC open balances
- Credit other
- Cash on hand
- Crypto holdings

**Output**: Green (proceed), Yellow (reduced scope), Red (block — escalate to Architect).

---

## Pyramid Base (Certainty Gate)

Before any multi-agent task executes, the Dispatcher checks the certainty level:

```
Certainty ≥ 3 sources  →  "Pyramid Base" — proceed to execution
Certainty < 3 sources  →  "Fear state" — return to Librarian for verification
```

This prevents execution of tasks built on unverified assumptions. The Librarian cross-references the Vault (Node 06) to establish the third source of confirmation.

---

## AI Manager Functions

The Dispatcher integrates with the AI Manager layer which provides:

| Function | Description |
|---|---|
| Mood ID | Detect current emotional/cognitive state from SOMA token + context |
| Pyramid Base check | Certainty ≥ 3 sources before execution |
| Scheduling & Time Optimization | Match tasks to optimal mode/time windows |
| Biometric Monitor | Real-time HRV and (future) EEG integration |
| Daily Monorail | Time-anchored mode transitions |
