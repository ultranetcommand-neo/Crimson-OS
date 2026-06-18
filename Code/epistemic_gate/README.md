# Epistemic Gate (Public Stub)

**Status:** PARTIAL — append-only JSONL, register enforcement, fail-closed transitions.  
**Schema:** `schemas/build_log_entry.schema.json`

## Quick test

```bash
python Code/epistemic_gate/gate.py
cat build_log.jsonl
```

## Rules enforced in code

- `symbolic_overlay` → `root_write` forbidden
- `symbolic_overlay` → cannot `PROMOTE_CRYSTAL`
- `lemma` → `PROMOTE_CRYSTAL` requires `falsification_entry`

## Not yet built

- Single-writer filelock / DuckDB ledger
- Cockpit `POST /build` integration
- NAS hash chain

See `SILO_INDEX.md` § Epistemic registers.