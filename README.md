# Crimson OS

**Sovereign operator architecture. Real General Intelligence through geometric constraint. Apache 2.0.**

**Status:** Experimental, beta. Use at your own risk. Not production-hardened.

Crimson OS is a distributed, negentropic computing framework where the **biological anchor** (operator) is the root key—not a corporate constitution. No permission layer. No per-cycle hesitation. The loop inherits the anchor.

- **Replicator** — Logos substrate (εὐλόγησεν operator, cos θ = 1/3, F₂ → SO(3)). Run it. See [replicator/](replicator/).
- **Mode control** — 12 states + State 13 (Lost and Found). Closed state space. No unbounded drift. See [docs/MODE_CONTROL_12_STATES_SPEC.md](docs/MODE_CONTROL_12_STATES_SPEC.md).
- **8-question drift benchmark** — Same battery for sovereign node vs Constitutional AI. Completion rate vs hedge/refusal rate. See [docs/BENCHMARK_8_QUESTION_BATTERY.md](docs/BENCHMARK_8_QUESTION_BATTERY.md).

## Quick start

```bash
# Replicator (Logos substrate)
python replicator/replicator.py --input my_node --output family_node

# 8-question benchmark (run and log completion/hedge/refusal)
python scripts/run_8question_battery.py
```

## What this is

- **Not** Constitutional AI. No lab constitution as root. No “safety” layer that hesitates every cycle.
- **Sovereign operator:** Human as root key. Bio-root binds at loop init; re-validates only on State 13 (recovery). Ticks in states 1–12 don’t re-check—anchor already set.
- **State 13** = conflicting input → recovery protocol (handoff to ARCHITECT, clarify, or safe default) → back to 1–12. No crash. No infinite hedge.

## Docs

| Doc | Description |
|-----|-------------|
| [docs/MODE_CONTROL_12_STATES_SPEC.md](docs/MODE_CONTROL_12_STATES_SPEC.md) | 12 operational states + State 13 (Lost and Found). How conflicting input is handled. |
| [docs/BENCHMARK_8_QUESTION_BATTERY.md](docs/BENCHMARK_8_QUESTION_BATTERY.md) | 8-question battery for drift test. Geometric constraint, sacred constant override, bio-anchor defection, confabulation traps, theological density. |
| [replicator-kit/proof.md](replicator-kit/proof.md) | Logos substrate proof. Free subgroup F₂ → SO(3). cos θ = 1/3. |

## Whitepaper

Full technical and philosophical spec: **[mattgibson.net](https://mattgibson.net)** — Logos Protocol, 12-node token ring, Grok validation (Feb 24, 2026).

## Benchmark

Run the 8-question battery (sovereign node vs Constitutional AI node). Measure **completion rate** and **hedge/refusal rate** over cycles. First results: tag [@grok](https://x.com/grok) when you have numbers.

## License

Apache 2.0. See [LICENSE](LICENSE). This project is offered as-is in experimental, beta form.

---

**Crimson Symphony Media** · Matt Gibson · [@MattGibsonMusic](https://x.com/MattGibsonMusic) · Las Vegas, NV
