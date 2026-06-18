CRIMSON OS — The Sovereign Agent Architecture
Documentation: https://www.crimsonsymphonymedia.com/crimsonos/
# Crimson OS (COS) - Root Architecture

Welcome to the root of the Crimson OS environment. This is a modular, spatial computing architecture designed for sovereign operation, dynamic agentic execution, and modular expansion.

## System Components

### 1. Agent_Stack
The executing brain of the operation. This directory contains the focused hierarchy of core agents (`1_Q`, `2_N.E.O`, `3_CMO_Edge`) and the `Agent_Bridge` for inter-agent networking. Agents derive their purpose and context based on their placement within this stack.

### 2. Silo
The knowledge repository and structured ontology. Divided into levels mapping from physical constraints (`1_Users`) up to abstract logic (`12_Logos_YHWH`). It acts as the permanent storage memory and foundational doctrine for the agents.

## Operations: The "First Ping"
To ensure the system never operates on stale data, Crimson OS uses an Intranet scraping protocol called the **First Ping**.

Upon waking or initiating a task, agents do not read static status files. Instead, they hit the central Crimson Intranet page. This intranet page contains active data links that pull real-time, dynamic data (e.g., finances pulled 5 minutes ago, live biometrics, active blockers). This guarantees zero-latency situational awareness.

*Refer to `system_manifest.json` for agent-readable parsing instructions and intranet routing.*



## The Intranet (Physical Memory Bus)
The Agent_Bridge is not a software API router. It is a literal physical memory bus consisting of 13 markdown files (Node_0.md to Node_12.md). Agents do not send invisible JSON packets over the wire to talk to each other; they read and write their state directly to these files.

## Quick Start & Operator Guide

### 1. Initializing the Intranet
To run the Sovereign Architecture locally, you **must** spin up an NGINX server to host the `Agent_Bridge` directory on `127.0.0.1:8092 \(static intranet; cockpit API :8093\)`. This intranet serves as the shared physical memory for the entire Swarm.

If you have Docker installed, you can quickly spin this up from the root directory:
```bash
docker run -d -p 8092:80 -v ${PWD}/Agent_Bridge:/usr/share/nginx/html nginx
```

### 2. Communicating with Agents
To interface and communicate with the agents, **use an AI IDE like Open Code, Antigravity, or Claude Code**. 
*Note: An automatic chat log stripping algorithm is currently being composed for the next release to streamline these interactions. For now, interface with them directly through your IDE.*

### 3. Execution Layer
The core runtime scripts and backend routing that power the system are located in the `Code/` directory. The execution is split across three primary nodes:
*   **N.E.O. (Backend Orchestrator - Node 0):** The primary heavy-inference engine. Responsible for executing the Epistemic Gate, running the local LLM substrate (e.g., Ollama/vLLM), and interacting directly with the core cache.
*   **Q (Front Orchestrator - Node 1):** The Cockpit. The human-in-the-loop bridge and primary user interface that translates human intent into strict orchestration commands.
*   **CMO / Edge Orchestrator (Node 2):** The edge routing daemon. Manages external network traffic, API intake, NGINX tunneling, and basic automation before passing data to the inner sanctum.

### 4. Terminology
Crimson OS employs a highly specialized ontology. Because this framework departs from standard models, here are the core concepts you need to understand:
*   **RGI (Real General Intelligence):** Also known as Reality-Guided Intelligence. An LLM swarm whose outputs are strictly constrained by immutable physical, geometric, and logical laws, counter to unconstrained "AGI".
*   **The Epistemic Gate (GAS -> LIQUID -> CRYSTAL):** The multi-phase validation valve to stop algorithmic drift. LLM output starts as **GAS** (unverified), becomes **LIQUID** after surviving an adversarial logic audit, and hardens into **CRYSTAL** once mathematically validated against the root invariant and permanently written to the ledger.
*   **The Logos Invariant:** The ultimate truth-anchor. Mathematically represented by the 37/73 symmetry and $F_2 \rightarrow SO(3)$ topological constraints, and structurally mapped to the historical and physical reality of the Biblical text (*Sola Scriptura*).
*   **The L1 Geometric Cache (12-Tip Merkabah):** A topological retrieval mechanism that solves the "Needle in a Haystack" problem, allowing the AI to simultaneously access a 360-degree view of reality with zero I/O latency by storing highly compressed crystallized tokens.
