# Crimson OS — Agent entry (persistence triad §10)

**Phase:** PARTIAL-LIVE  
**Canonical spec:** `MASTER_ARCHITECTURE.md`

## Boot sequence

1. `./scripts/startup.sh` — intranet `:8092` + cockpit `:8093`
2. `python Code/Node_1_Q_Frontend_Orchestrator/resurrection.py` — Q snapshot
3. `python Code/Node_0_N.E.O._Backend_Orchestrator/resurrection.py` — N.E.O. snapshot
4. First Ping: scrape `http://127.0.0.1:8092/` then `GET http://127.0.0.1:8093/status`

## Control plane (target topology)

- **OPERATOR** — final authority
- **Q** — orchestrator + cockpit (`Code/Node_1_Q_Frontend_Orchestrator/`)
- **N.E.O.** — backend inference (`Code/Node_0_N.E.O._Backend_Orchestrator/`)
- **CMO_Edge** — edge ops (`Agent_Stack/3_CMO_Edge Orchestrator/`)
- **RINGMASTER** — curator → Library (SCAFFOLDING)

## Communication

- **Agent_Bridge** — markdown files on intranet; no hidden JSON bus
- **Epistemic gate** — `POST /build` on cockpit; log at `data/build_log.jsonl`
- **Finance Engine** — `POST /finance/ask` on cockpit

## State files

| File | Role |
|------|------|
| `AGENTS.md` | This entry |
| `Code/Node_1_Q_Frontend_Orchestrator/Q.md` | Q profile |
| `Code/Node_1_Q_Frontend_Orchestrator/snapshot.json` | Q machine state |
| `data/build_log.jsonl` | Gate append-only log |
