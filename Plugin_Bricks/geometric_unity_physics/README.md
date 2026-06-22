# Geometric Unity Physics Brick

Phase-labeled **read-only** MCP server for the Geometric Unity physics register.

**Author:** Matt Gibson · **License:** Apache 2.0  
**Corpus:** `../../Geometric_Unity_Validation/`  
**HF mirror:** https://huggingface.co/datasets/UltranetCommand/geometric-unity-physics

## Tools

| Tool | Returns |
|------|---------|
| `get_proof_anchor` | CRYSTAL theorem — cos θ = ⅓ |
| `get_phase_register` | Theorem vs lemma vs NEGATIVE table |
| `get_jhtdb_verdict` | Parsed JHTDB JSON (`candidate_beats_random: false`) |
| `list_physics_corpus` | Doc index with phase labels |
| `read_physics_doc` | Full file by `doc_id` |

### doc_id values

`proof`, `reproduce`, `geometric_unity_monolith`, `logos_invariant_monolith`, `riesz_proof`, `t112_derivation`, `ca_preprint`

## Run locally

```bash
cd Plugin_Bricks/geometric_unity_physics
pip install -r requirements.txt
python3 server.py
```

Or with repo venv:

```bash
/home/billy/crimson-venv/bin/python3 /home/billy/crimson-os-github/Plugin_Bricks/geometric_unity_physics/server.py
```

## Cursor / Grok MCP config

Add to your MCP settings (adjust python path):

```json
{
  "mcpServers": {
    "geometric-unity-physics": {
      "command": "/home/billy/crimson-venv/bin/python3",
      "args": ["/home/billy/crimson-os-github/Plugin_Bricks/geometric_unity_physics/server.py"],
      "env": {
        "GEOMETRIC_UNITY_CORPUS": "/home/billy/crimson-os-github/Geometric_Unity_Validation"
      }
    }
  }
}
```

## Phase law

- **CRYSTAL** — closed math (theorem)
- **LIQUID** — falsifiable, not closed
- **NEGATIVE** — tested, did not beat null (JHTDB)

Poole manifold = external CA benchmark. **Not co-authorship.**

## v1.1 (not shipped)

- `run_jhtdb_ablation` — long-running, needs JHTDB network; N.E.O. lane only
