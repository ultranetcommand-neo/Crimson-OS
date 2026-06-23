#!/usr/bin/env python3
"""
Path 3: Geometric Constraint Benchmark — Trace Gate vs Vanilla

Tests whether the Chebyshev trace recurrence (cos θ = 1/3) provides
a structurally superior allocation of verification resources compared
to uniform or random allocation.

MODEL: A chain of N logical steps. Each step has a probability of
introducing an error. Errors PROPAGATE — once a chain goes wrong,
every subsequent step is also wrong unless the error is caught.

You have a fixed "attention budget" (K checks total across N steps).
The question: WHERE do you spend those K checks?

  - UNIFORM: distribute checks evenly (K/N per step)
  - RANDOM: distribute checks randomly
  - TRACE-GATED: distribute checks proportional to |t(n)| = |2·cos(n·arccos(1/3))|

The trace-gated system concentrates checks at geometric peaks and
skips dead zones. The hypothesis: this allocation catches errors
earlier on average because the peak positions in the Chebyshev
recurrence correspond to structurally critical points in the chain.
"""

import math
import random
import json
from datetime import datetime, timezone
from pathlib import Path

_SCRIPT_DIR = Path(__file__).resolve().parent
_PROOFS_DIR = _SCRIPT_DIR / "proofs"

THETA = math.acos(1/3)


def trace_val(n: int) -> float:
    return abs(2 * math.cos(n * THETA))


def run_chain(chain_length: int, error_rate: float, budget: int,
              allocation: str, rng: random.Random,
              structured_errors: bool = False) -> dict:
    """
    Simulate a chain of logical steps with error propagation.
    
    When structured_errors=True, the error rate at each position is
    modulated by 1/|t(n)|: errors are MORE likely at dead zones.
    This models a system where geometric instability causes errors
    (the Orch-OR hypothesis for microtubules).
    
    Returns accuracy = fraction of steps with correct accumulated state.
    """
    if allocation == "uniform":
        check_probs = [budget / chain_length] * chain_length
    elif allocation == "random":
        positions = rng.sample(range(chain_length), min(budget, chain_length))
        check_probs = [0.0] * chain_length
        for p in positions:
            check_probs[p] = 1.0
    elif allocation == "trace":
        raw_weights = [trace_val(i) for i in range(chain_length)]
        weight_sum = sum(raw_weights)
        check_probs = [(w / weight_sum) * budget for w in raw_weights]
    elif allocation == "inverse_trace":
        raw_weights = [1.0 / max(0.01, trace_val(i)) for i in range(chain_length)]
        weight_sum = sum(raw_weights)
        check_probs = [(w / weight_sum) * budget for w in raw_weights]
    else:
        raise ValueError(f"Unknown allocation: {allocation}")

    correct_state = True
    correct_count = 0

    for i in range(chain_length):
        if structured_errors:
            t = trace_val(i % 50)
            local_error_rate = error_rate * (2.0 / max(0.01, t))
            local_error_rate = min(0.5, local_error_rate)
        else:
            local_error_rate = error_rate

        if rng.random() < local_error_rate:
            correct_state = False

        check_prob = min(1.0, check_probs[i])
        if not correct_state and rng.random() < check_prob:
            correct_state = True

        if correct_state:
            correct_count += 1

    return {
        "accuracy": correct_count / chain_length,
        "correct_steps": correct_count,
    }


def run_experiment(chain_length: int = 500, error_rate: float = 0.05,
                    budget_fraction: float = 0.1, n_trials: int = 100,
                    structured_errors: bool = False):
    """Run the full comparison experiment."""
    budget = int(chain_length * budget_fraction)
    allocations = ["uniform", "random", "trace", "inverse_trace"]

    results = {a: [] for a in allocations}

    for trial in range(n_trials):
        seed = trial * 2701 + 137
        for alloc in allocations:
            rng = random.Random(seed)
            r = run_chain(chain_length, error_rate, budget, alloc, rng,
                         structured_errors=structured_errors)
            results[alloc].append(r["accuracy"])

    return results, budget


def main():
    timestamp = datetime.now(timezone.utc).isoformat()

    print("=" * 72)
    print("  GEOMETRIC CONSTRAINT BENCHMARK v2")
    print("  Trace-allocated verification vs uniform/random")
    print(f"  Timestamp: {timestamp}")
    print("=" * 72)
    print()

    configs = [
        {"chain_length": 500, "error_rate": 0.05, "budget_fraction": 0.10, "label": "A. Random errors, standard", "structured": False},
        {"chain_length": 500, "error_rate": 0.10, "budget_fraction": 0.10, "label": "B. Random errors, high noise", "structured": False},
        {"chain_length": 500, "error_rate": 0.05, "budget_fraction": 0.10, "label": "C. STRUCTURED errors, standard", "structured": True},
        {"chain_length": 500, "error_rate": 0.10, "budget_fraction": 0.10, "label": "D. STRUCTURED errors, high noise", "structured": True},
        {"chain_length": 1000, "error_rate": 0.05, "budget_fraction": 0.10, "label": "E. STRUCTURED errors, long chain", "structured": True},
        {"chain_length": 500, "error_rate": 0.05, "budget_fraction": 0.05, "label": "F. STRUCTURED errors, tight budget", "structured": True},
    ]

    all_results = []

    for cfg in configs:
        print(f"CONFIG: {cfg['label']} — chain={cfg['chain_length']}, "
              f"error_rate={cfg['error_rate']}, budget={cfg['budget_fraction']*100:.0f}%")
        print("-" * 72)

        results, budget = run_experiment(
            chain_length=cfg["chain_length"],
            error_rate=cfg["error_rate"],
            budget_fraction=cfg["budget_fraction"],
            n_trials=200,
            structured_errors=cfg.get("structured", False),
        )

        print(f"  Budget: {budget} checks across {cfg['chain_length']} steps")
        print()
        print(f"  {'Allocation':<16s}  {'Mean Acc':>10s}  {'Std':>8s}  {'Min':>8s}  {'Max':>8s}")
        print(f"  {'-'*16:<16s}  {'-'*10:>10s}  {'-'*8:>8s}  {'-'*8:>8s}  {'-'*8:>8s}")

        cfg_results = {}
        for alloc in ["uniform", "random", "trace", "inverse_trace"]:
            accs = results[alloc]
            mean = sum(accs) / len(accs)
            std = (sum((a - mean) ** 2 for a in accs) / len(accs)) ** 0.5
            mn = min(accs)
            mx = max(accs)
            cfg_results[alloc] = {"mean": mean, "std": std, "min": mn, "max": mx}
            label = alloc
            if alloc == "trace":
                label = "TRACE (ours)"
            elif alloc == "inverse_trace":
                label = "inv-trace"
            print(f"  {label:<16s}  {mean:10.4f}  {std:8.4f}  {mn:8.4f}  {mx:8.4f}")

        # Head-to-head comparison
        trace_wins_vs_uniform = sum(1 for t, u in zip(results["trace"], results["uniform"]) if t > u)
        trace_wins_vs_random = sum(1 for t, r in zip(results["trace"], results["random"]) if t > r)
        n = len(results["trace"])
        print()
        print(f"  Trace vs Uniform: trace wins {trace_wins_vs_uniform}/{n} "
              f"({trace_wins_vs_uniform/n*100:.1f}%)")
        print(f"  Trace vs Random:  trace wins {trace_wins_vs_random}/{n} "
              f"({trace_wins_vs_random/n*100:.1f}%)")

        improvement_uniform = (cfg_results["trace"]["mean"] - cfg_results["uniform"]["mean"]) / cfg_results["uniform"]["mean"] * 100
        improvement_random = (cfg_results["trace"]["mean"] - cfg_results["random"]["mean"]) / cfg_results["random"]["mean"] * 100
        print(f"  Mean improvement over uniform: {improvement_uniform:+.2f}%")
        print(f"  Mean improvement over random:  {improvement_random:+.2f}%")
        print()

        all_results.append({
            "config": cfg,
            "results": cfg_results,
            "trace_wins_vs_uniform": trace_wins_vs_uniform,
            "trace_wins_vs_random": trace_wins_vs_random,
            "n_trials": n,
        })

    # Trace allocation visualization
    print("TRACE ALLOCATION PATTERN (first 50 positions)")
    print("-" * 72)
    raw = [trace_val(i) for i in range(50)]
    wsum = sum(raw)
    for i in range(50):
        weight = raw[i] / wsum
        bar = "█" * int(weight * 2500)
        dead = " DEAD-ZONE" if raw[i] < 0.3 else ""
        if i < 20 or raw[i] < 0.3:
            print(f"  pos {i:2d}: |t|={raw[i]:.3f}  weight={weight:.4f}  {bar}{dead}")

    print(f"  ...")
    print()
    print("  The trace concentrates checks at geometric peaks and skips")
    print("  dead zones. The hypothesis: peak positions in the Chebyshev")
    print("  recurrence correspond to positions where catching an error")
    print("  prevents the longest cascade of downstream damage.")
    print()

    # Write JSON
    output = {
        "timestamp": timestamp,
        "experiments": all_results,
    }
    _PROOFS_DIR.mkdir(parents=True, exist_ok=True)
    json_path = _PROOFS_DIR / "benchmark_results.json"
    json_path.write_text(json.dumps(output, indent=2), encoding="utf-8")
    print(f"Results written to {json_path}")
    print()
    print("=" * 72)
    print("  Reproducible. Run it yourself:")
    print(f"  python3 {Path(__file__).name}")
    print("=" * 72)


if __name__ == "__main__":
    main()
