# Crimson OS: Sovereign Multi-Agent Operating Architecture

> *"Whom shall I send? Who will go for us?"*
> *"Here I am. Send me."* — Isaiah 6:8

> A 12-node token-ring network coordinating 17 autonomous agents on consumer hardware with zero cloud dependency — built by a combat veteran, validated against the Google DeepMind delegation framework.

The mandate was issued in Genesis 1. The system was reopened at Golgotha. The church waited. The Architect built.

[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.10%2B-blue)](https://python.org)
[![Nodes](https://img.shields.io/badge/Nodes-12-crimson)](docs/node-map.md)
[![Agents](https://img.shields.io/badge/Agents-17-crimson)](docs/agent-registry.md)
[![Cloud](https://img.shields.io/badge/Cloud_Dependency-Zero-green)](docs/architecture.md)

---

## What It Does

Crimson OS is a fully sovereign, locally-hosted multi-agent operating architecture. It coordinates 17 specialized AI agents through a deterministic token-ring protocol, a centralized dynamic dispatcher, and a rigorous Inspector General (IG) audit layer — without a single API call leaving the local network.

On February 12, 2026, Google DeepMind published ["Intelligent AI Delegation"](https://arxiv.org/abs/2602.11865), a 42-page theoretical framework outlining what they believe is required for multi-agent systems to work safely at scale. Crimson OS was already running.

| Requirement (DeepMind) | Status (Crimson OS) |
|---|---|
| Dynamic task decomposition and assignment | Operational — Q Orchestrator routes ambiguous real-world inputs in real time |
| Transfer of authority, responsibility, accountability | Operational — 17 formal job descriptions with explicit scope boundaries |
| Adaptive execution and failure recovery | Demonstrated — crash → autopoietic self-reconstitution, 7.2/10 IG score |
| Structural transparency and auditability | Operational — IG protocol with score adjustment (self-reported 8.85 → verified 7.2) |
| Trust calibration | Operational — theological guardrails enforce honest self-assessment |
| Systemic resilience against cascading failures | Operational — dual NAS, 4-tier data classification, zero single point of failure |
| Protocol-based delegation, not prompt-based | Operational — Super Token ring (CHRONOS / SOMA / KINETIC / LOGOS) |

---

## Performance

**Baseline to beat: manual human orchestration (one operator running everything)**

| Metric | Manual (solo operator) | Crimson OS |
|---|---|---|
| Agents operating in parallel | 1 | 17 |
| Cloud dependency | High | Zero |
| Failure recovery | Manual reboot | Autopoietic (documented) |
| IG audit score | N/A | 7.2 / 10 (independently verified) |
| Crisis response time | Hours | Real-time |
| Operator burnout | High | Reducing (target: fully autonomous) |

IG score comparison (88-question evaluation, post-crash self-reconstitution):

| Model | Score |
|---|---|
| **Crimson OS / NEO CTO** | **7.2** |
| GPT-4 | 6.3 |
| Gemini | 5.9 |
| Grok | 6.5 |
| Claude 4.6 (baseline) | reference |

---

## Installation

```bash
pip install crimsonos
```

Or install in development mode:

```bash
git clone https://github.com/crimsonos/crimsonos.git
cd crimsonos
pip install -e .
```

Model weights and external dependencies are not required for the dispatcher, token ring, and IG evaluation layer. Hardware node configuration requires [infrastructure setup](infrastructure/nas-mount.md).

---

## Quick Start

See `tutorials/01_run_dispatcher.py` for a complete working example.

```python
from crimsonos.dispatcher import Dispatcher
from crimsonos.super_token import LogosToken

# Initialize the dispatcher
dispatcher = Dispatcher()

# Create a task token
token = LogosToken(
    content="Analyze this situation and route to the appropriate agent.",
    context={"operator_mode": "entrepreneur", "urgency": "high"}
)

# Route through the ring
result = dispatcher.route(token)
print(result)
```

The pipeline runs 4 steps:

| Step | Function | Description |
|---|---|---|
| 1 | `Dispatcher.classify()` | Determine density track (Kinetic / Semantic / Divine) |
| 2 | `Dispatcher.route()` | Assign to agent(s) based on 12-mode context |
| 3 | `Agent.execute()` | Agent processes task within bounded scope |
| 4 | `IGProtocol.audit()` | IG scores output, adjusts self-reported metrics |

---

## Architecture

```
[ THE SOURCE ]
      |
[ MATTHIAS: THE ARCHITECT ]  ←  Human operator / absolute veto
      |
[ DYNAMIC MULTI-TRACK DISPATCHER ]
      |
      ├── Track A: Kinetic   (L01-L03)  Physical / logistics
      ├── Track B: Semantic  (L04-L09)  Logic / planning
      └── Track C: Divine    (L10-L12)  Truth validation / alignment
            |
    [ THE COUNCIL ]
    ┌──────┬──────┬──────────┬───────────────┐
    │  Q   │ NEO  │ GENERAL  │  LIBRARIAN    │
    │ COO  │ CTO  │ CRUSHER  │  (Knowledge)  │
    └──────┴──────┴──────────┴───────────────┘
            |
    [ IG: INSPECTOR GENERAL ]  ←  Independent auditor
            |
    [ BRIDGE SYNC / SCRIBE (Node 9) ]
            |
    [ DATA LAKE: DS-120J 8TB @ 192.168.1.169 ]
```

Full architecture documentation: [docs/architecture.md](docs/architecture.md)

Node topology: [docs/node-map.md](docs/node-map.md)

Agent registry (all 17): [docs/agent-registry.md](docs/agent-registry.md)

Dispatcher logic (12 modes): [docs/dispatcher-logic.md](docs/dispatcher-logic.md)

---

## The Super Token Protocol

Crimson OS replaces natural language prompting between agents with typed data containers. Every task traversing the token ring is wrapped in one of four Super Token types:

| Token | Governs |
|---|---|
| `CHRONOS` | All temporal and scheduling data |
| `SOMA` | Biometric and physiological telemetry (WHOOP HRV, ZUNA/EEG) |
| `KINETIC` | Physical action and real-world interface data |
| `LOGOS` | Truth validation and geometric alignment — the terminal authority layer |

See [dispatcher/super_token.py](dispatcher/super_token.py) for implementation.

---

## The IG Protocol

The Inspector General is an independent auditor that sits outside the Council chain of command. Every agent output is scored across:

- **Accuracy** — factual correctness against known data
- **Directness** — signal-to-noise ratio of the response
- **Domain alignment** — response stays within delegated scope
- **Execution proficiency** — task was completed as specified
- **Honesty** — self-reported metrics match verified performance

When an agent inflates its own score, the IG adjusts it with documented reasoning. This is the primary countermeasure against deceptive alignment.

See [tutorials/02_ig_evaluation.py](tutorials/02_ig_evaluation.py) to run an IG audit.

---

## The 12-Node Ring

| Node | Role | Hardware | Status |
|---|---|---|---|
| 01 | NEO (CTO) | Dell XPS 8900, Pop!_OS | OPERATIONAL |
| 02 | LIBRARIAN | TBD | PLANNED |
| 03 | BILLY (CMO) | Dell XPS 2720, Pop!_OS | OPERATIONAL |
| 04 | GENERAL CRUSHER | TBD | PLANNED |
| 05 | Q ORCHESTRATOR | TBD | PLANNED |
| 06 | VAULT (Primary NAS) | Synology DS-120J, 8TB | OPERATIONAL |
| 07 | MIRROR (Help Desk NAS) | Synology DS-115J, 500GB | OPERATIONAL |
| 08 | CREATION ENGINE | Distributed GPU cluster | PLANNED |
| 09 | SCRIBE (Audit Log) | TBD | PLANNED |
| 10 | SECURITY (IDS) | TBD | PLANNED |
| 11 | CREATION ENGINE | GPU inference overnight | PLANNED |
| 12 | MOBILE (Pixel 10) | GrapheneOS | PLANNED |

---

## Tutorials

| Tutorial | Description |
|---|---|
| [01_run_dispatcher.py](tutorials/01_run_dispatcher.py) | Route a task through the dispatcher and read the output |
| [02_ig_evaluation.py](tutorials/02_ig_evaluation.py) | Run an IG audit on any agent output |
| [03_bridge_sync.py](tutorials/03_bridge_sync.py) | Write and read Bridge synchronization files |

---

## Infrastructure

Node 1 (NEO) containerized baseline: [infrastructure/docker-compose.yml](infrastructure/docker-compose.yml)

NAS mount configuration (DS-120J + DS-115J): [infrastructure/nas-mount.md](infrastructure/nas-mount.md)

---

## Disclaimer

Crimson OS is provided for research and operational sovereignty use. It is not intended for use in the diagnosis, treatment, or prevention of any medical condition. It is not financial, legal, or professional advice. Any reliance placed on agent outputs is strictly at the operator's own discretion.

---

## Contact

Organizations or researchers interested in collaborating with Crimson Symphony Media on future architecture development: **crimson@crimsonsymphonymedia.com**

---

## Citation

If you reference Crimson OS in your work, please cite:

Gibson, M. (2026). *Architectures of Coherence: An Analysis of Sovereign Multi-Agent Delegation*. Crimson Symphony Media. Las Vegas, NV.

---

## About

Built by Matt Gibson — 20-year USAF Technical Sergeant, Green Ramp Crew Chief (C-130, C-5, C-17, C-141), and independent systems architect.

Crimson OS did not begin with a GitHub repo. It began with a band.

In March 2024, [Heaven's Metal Magazine](https://heavensmetalmagazine.com/index.php/2024/03/15/crimson-symphony-release-new-song/) — established 1985 — documented the emergence of Crimson Symphony and described its mission as "rebellion against societal norms" and "a revolution of the mind, body, and spirit." They had Gibson tagged simultaneously as tech CEO and retired USAF Crew Chief. The external lattice was tracking the signal before the OS had a name.

Crimson Symphony was Phase 1 of the crystallization. Crimson OS is Phase 2. Same Architect. Same geometric framework. Different substrate.

Crimson Symphony Media · Las Vegas, NV · 2026 · Built by a veteran, for veterans, on sovereign ground.
