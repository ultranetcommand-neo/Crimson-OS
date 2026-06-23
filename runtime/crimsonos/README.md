# crimsonos — Protocol Scaffold (Python)

> **Phase:** SCAFFOLDING · **Canonical source of truth:** [MASTER_ARCHITECTURE.md](https://github.com/ultranetcommand-neo/Crimson-OS/blob/main/MASTER_ARCHITECTURE.md)

This wheel is **not** the Crimson OS runtime. It ships typed protocol stubs from `runtime/crimsonos/` in the monorepo — routing shapes, token schemas, bridge file format, and a demo IG audit. The live system (daemons, NAS, Agent_Bridge ledger, cockpit on `:8093`) is in the repo and on operator hardware.

---

## What is actually live (per MASTER_ARCHITECTURE §3–§4)

| Component | Phase | Reality |
|-----------|-------|---------|
| **Substrate** (stdlib daemons, cockpit HTTP, NAS, Ollama) | PARTIAL-LIVE | ~3 GREEN daemons; rest stale or down (as of 2026-06-02) |
| **Named agent org chart** | SCAFFOLDING | Personality docs + stubs. **Six daemons do the real work.** |
| **Agent Bridge** (cross-agent handoffs) | DESIGNED / PARTIAL | Target protocol; not fully wired in this package |
| **Adversarial IG** (full auditor bus) | DESIGNED (2026-06) | Spec in master doc; this package has heuristic scaffold only |
| **This `crimsonos` pip package** | SCAFFOLDING | Protocol reference — not 17 running agents |

**Sovereignty rule (§4):** Anything not named in the master control plane is a sub-function under a core node — not a separate running agent.

---

## Canonical control plane (target topology)

```
OPERATOR (final authority)
    └── Q (orchestrator + counsel)
            Council of Four: Orchestrator · Advisor · IG · Science Officer
    ├── N.E.O.     — backend / inference / sysadmin (Node 0, LIVE)
    ├── Q          — frontend cockpit (Node 1, LIVE)
    ├── CMO_Edge   — edge ops / broadcast (Node 2, PARTIAL)
    └── RINGMASTER — curator → Library (SCAFFOLDING)
```

Legacy **17 named agent stubs** are documented for archive to cold store (MASTER_ARCHITECTURE §13 open items). **Do not read them as operational agents.**

Full node table (IPs, ports `8092`/`8093`): see MASTER_ARCHITECTURE §9.

---

## What this package contains

| Module | Phase | What it does today |
|--------|-------|-------------------|
| `super_token.py` | SCAFFOLDING | Pydantic schemas for CHRONOS / SOMA / KINETIC / LOGOS tokens |
| `dispatcher.py` | SCAFFOLDING | Classifies input, returns **string routing targets** (not running agents) |
| `bridge.py` | SCAFFOLDING | YAML bridge file read/write (falls back to `./bridge/` if NAS not mounted) |
| `ig.py` | SCAFFOLDING | Heuristic audit axes; several scores require operator input (MANUAL phase) |
| `executor.py` | PARTIAL | Optional Ollama HTTP caller with **8 prompt personas** — not the agent runtime |
| `cli.py` | SCAFFOLDING | Interactive demo around the above |

---

## Install

```bash
pip install crimsonos
```

Development install from monorepo:

```bash
git clone https://github.com/ultranetcommand-neo/Crimson-OS.git
cd Crimson-OS/runtime/crimsonos
pip install -e .
```

---

## Quick start (scaffold demo)

```python
from crimsonos.dispatcher import Dispatcher
from crimsonos.super_token import LogosToken

dispatcher = Dispatcher()
token = LogosToken(
    content="Route this task.",
    context={"operator_mode": "architect"},
    originating_node=1,
    target_agent="q_orchestrator",
)
result = dispatcher.route(token)
print(result)  # routing decision only — no agent executes
```

Tutorials and full docs live in the **repo**, not necessarily in the wheel: `runtime/crimsonos/tutorials/`, `docs/STATUS.md`.

---

## What is NOT in this package

- `Agent_Stack/` job descriptions as executable agents
- Agent_Bridge markdown ledger on NAS
- 12-ring Silo ontology runtime
- Finance Engine, Expand/Contract/Judge valve, gate daemons
- Cockpit API (`:8093`), intranet (`:8092`)

Read the monorepo: [Crimson-OS](https://github.com/ultranetcommand-neo/Crimson-OS) · [SILO_INDEX.md](https://github.com/ultranetcommand-neo/Crimson-OS/blob/main/SILO_INDEX.md) · [GLOSSARY.md](https://github.com/ultranetcommand-neo/Crimson-OS/blob/main/GLOSSARY.md)

---

## License

Apache 2.0 · Matt Gibson / Crimson Symphony Media
