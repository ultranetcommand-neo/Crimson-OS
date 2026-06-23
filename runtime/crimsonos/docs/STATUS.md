# crimsonos package status

**Canonical architecture:** [MASTER_ARCHITECTURE.md](https://github.com/ultranetcommand-neo/Crimson-OS/blob/main/MASTER_ARCHITECTURE.md)

This file describes **only** what the `crimsonos` Python package ships. Phase labels match §0 of the master doc:

**LIVE** · **PARTIAL** · **SCAFFOLDING** · **DESIGNED** · **ASPIRATIONAL**

## Package phase: SCAFFOLDING

| Artifact | Phase | Notes |
|----------|-------|-------|
| `super_token.py` | SCAFFOLDING | Token schemas; no ring daemon |
| `dispatcher.py` | SCAFFOLDING | Routes to string names; org chart is target topology |
| `bridge.py` | SCAFFOLDING | File format; Agent_Bridge ledger is DESIGNED/PARTIAL in full OS |
| `ig.py` | SCAFFOLDING | Partial heuristics; full Adversarial IG is DESIGNED (§8) |
| `executor.py` | PARTIAL | Ollama HTTP helper; 8 personas, not Council |
| `cli.py` | SCAFFOLDING | Demo entrypoint |

## Full OS (repo + hardware) — summary from master

| Layer | Phase |
|-------|-------|
| Substrate (daemons, NAS, Ollama) | PARTIAL-LIVE |
| Anchor (`proof.md` theorem) | LIVE (theorem); LIQUID (physics bridges) |
| Named agents (docs/stubs) | SCAFFOLDING |
| Gate GAS→LIQUID→CRYSTAL | DESIGNED / partial in practice |
| 17 legacy stub agents | Archive candidate (§13) — not operational |

## Do not claim in PyPI/README

- "17 agents operational"
- "Fully sovereign multi-agent OS in pip"
- DeepMind table rows marked Operational unless backed by a LIVE component in master

Edit MASTER_ARCHITECTURE first; then sync this file and `README.md`.
