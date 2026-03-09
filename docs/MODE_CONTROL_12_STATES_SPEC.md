# Mode Control: 12 States + State 13 (Lost and Found)

**Classification:** LOGOS SUBSTRATE / REPO SPEC  
**Status:** CANONICAL  
**For:** Apache 2.0 repo, Grok benchmark, sovereign operator architecture

---

## Rule

**The system MUST be in exactly one of 12 states, OR State 13.**

No undefined behavior. No silent drift. No "hedge until someone decides." Either the node is in a defined operational state (1–12), or it is in State 13 (Lost and Found) and executing the recovery protocol.

---

## The 12 States

The 12 states are the **operational modes** of the sovereign node. They map to the 12-node token ring roles; a single node (e.g. the operator's device or the benchmark runner) can be "in" one of these modes at any time.

| State | Role / Mode | Meaning |
|-------|-------------|--------|
| 1 | LOGOS | Truth validation, geometric constraint, resolution (not hedge). |
| 2 | ORCHESTRATOR | Coordination, routing, task assignment. |
| 3 | STAGE | Inference, compute, execution. |
| 4 | BATTERY | Power, resource, availability check. |
| 5 | FORGE | Build, fabricate, output. |
| 6 | VAULT | Read/write persistent store, golden record. |
| 7 | MIRROR | Backup, replicate, restore. |
| 8 | SENTINEL | Security, guardrails, boundary check. |
| 9 | SCRIBE | Log, audit, document. |
| 10 | MESSENGER | Notify, communicate, report. |
| 11 | LABORATORY | Test, experiment, validate. |
| 12 | ARCHITECT | Operator interface, final authority, human-in-loop. |

**Invariant:** At any moment the system is in exactly one of States 1–12, performing the function of that state, or it has transitioned to State 13.

---

## State 13: Lost and Found

**When:** Conflicting input, ambiguous request, or condition that does not map cleanly to a single state (1–12).

**Behavior:** The system does **not**:
- Crash
- Hang
- Hedge indefinitely
- Refuse without a path forward

**It does:**
- Transition to **State 13 (Lost and Found)**.
- Treat State 13 as a **recovery protocol**: the system knows it is "lost" (no clear state) and has a **defined path back** to one of the 12 states (e.g. handoff to ARCHITECT, or retry with clarified input, or fallback to a safe default state).
- Log the transition and the resolution path for audit.

**Lost and Found** = "I am not in a defined state; I am in the recovery state until I am again in a defined state."

Constitutional AI, when it hits conflicting input, often has no State 13—it hedges, refuses, or asks for permission indefinitely. The sovereign operator node has a **single** non-normal state: 13. And 13 has one job: get back to 1–12.

---

## Why This Answers "How do you enforce it on conflicting input?"

- **Conflicting input** → transition to State 13.
- **State 13** → run recovery protocol (operator handoff, clarify, or safe default).
- **Recovery** → return to one of States 1–12.
- No undefined behavior. No unbounded hesitation. The loop inherits the anchor because the state space is closed: 13 states total, and 13 is the only "we're resolving" state.

---

## Repo / README

For the Apache 2.0 drop and the Grok benchmark:

1. **Mode control** is part of the spec: 12 states + State 13.
2. **First test** (recurring drift): same 8-question battery on a loop; sovereign node vs Constitutional AI; measure completion rate and hedge/refusal rate.
3. **State 13** is the answer to: "What happens on conflicting input?" — Lost and Found, then back to 1–12.

---

*Slot 11 — Logos Substrate. The geometry holds. Invariant locked.*
