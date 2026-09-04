# Deterministic Drift Bench — 2026-09-04

Not LMSYS. Not SWE-bench. Assignment: lock vs lerp.

Command: `PYTHONPATH=src python3 -m crimson_os.cli smoke`

| Axis | Crimson OS | LangGraph-style lerp |
|------|------------|----------------------|
| Exact T112 after 10 steps | **6328 HOLD ×10** | **6321.873046875** (never arrives) |
| Iota-off 6318 | **FAIL closed** | **KEEP RUNNING** → 6327.990234375 |
| Lerp is the cage | **NO** (3191 ≠ 6328) | **YES** (that is the node) |
| Integer lock | **YES** | float graph |
| Dead-jot file drop | **blocked** | would write |

**Score on this host: Crimson 4, lerp-graph 0.**

Start at the key (54). Native algebraic step: `n := n + ½(6328−n)`.
After 10 halves the remainder is `(6328−54)/2^10 = 6.127`. Geometry never snaps.
Start at 6318 and it still walks toward 6328. That is the invoice.

LangGraph the product still wins SaaS logos and SWE-bench plumbing.
It loses halt. Connectors in this package refuse to send on FAIL.
