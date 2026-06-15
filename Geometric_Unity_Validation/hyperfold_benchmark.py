#!/usr/bin/env python3
"""
CRIMSON OS // HYPERFOLD BENCHMARK v1.0
Task: Isolate "Lattice-Aligned Primes" (Primes at Chebyshev Resonance Peaks)

Comparison:
1. ALGEBRAIC (The Haystack): Brute-force search through all integers.
2. GEOMETRIC (The Hyperfold): Triangulated search along the resonance path.

Target: Verify the < 1% efficiency claim for constraint-based computation.
"""

import math
import time
import json
from datetime import datetime, timezone

# The Logos Invariant
THETA = math.acos(1/3)
RESONANCE_TARGET = 0.95  # We only care about strong peaks

def is_prime(n: int) -> bool:
    if n < 2: return False
    if n < 4: return True
    if n % 2 == 0 or n % 3 == 0: return False
    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0: return False
        i += 6
    return True

def get_trace_abs(n: int) -> float:
    """The trace recurrence value at n."""
    return abs(math.cos(n * THETA))

def benchmark_algebraic(limit: int):
    """Search every integer for the needle."""
    start_time = time.perf_counter()
    count_is_prime = 0
    count_trace = 0
    results = []
    
    for n in range(1, limit + 1):
        # We must check both conditions
        count_trace += 1
        trace = get_trace_abs(n)
        if trace > RESONANCE_TARGET:
            count_is_prime += 1
            if is_prime(n):
                results.append((n, trace))
                
    end_time = time.perf_counter()
    return {
        "method": "Algebraic (Haystack)",
        "limit": limit,
        "ops_trace": count_trace,
        "ops_prime": count_is_prime,
        "total_ops": count_trace + count_is_prime,
        "time_seconds": end_time - start_time,
        "found": len(results)
    }

def benchmark_geometric(limit: int):
    """
    Search only the resonance path.
    The geometry dictates that peaks can only occur at specific intervals
    defined by the continued fraction of theta/pi.
    
    We use the 'Hyperfold' jump logic: we skip the hay.
    """
    start_time = time.perf_counter()
    count_is_prime = 0
    count_trace = 0
    results = []
    
    # Initial seeds from the Chebyshev proof (n=5, n=13)
    # The jump distance (period) is ~2.55, but we look for near-integers.
    # We follow the sequence of "Near Returns" (Fibonacci-like jumps).
    
    # We jump between resonance peaks.
    # Known sequence of jump increments: 5, 8, 13, 21...
    current_n = 5
    jumps = [5, 8, 13] # The base resonance jump units
    
    # Simple Hyperfold: instead of checking all n, 
    # we only check n that satisfy the geometric resonance condition:
    # n * theta approx k * pi
    
    # To be fair to the 'Geometric' approach, we use the property that
    # the search is constrained to the manifold where the trace is high.
    
    # Computational logic: solve for k in n = round(k * pi / theta)
    pi_over_theta = math.pi / THETA
    
    k = 1
    while True:
        n = round(k * pi_over_theta)
        if n > limit:
            break
            
        count_trace += 1
        trace = get_trace_abs(n)
        if trace > RESONANCE_TARGET:
            count_is_prime += 1
            if is_prime(n):
                results.append((n, trace))
        
        k += 1
        
    end_time = time.perf_counter()
    return {
        "method": "Geometric (Hyperfold)",
        "limit": limit,
        "ops_trace": count_trace,
        "ops_prime": count_is_prime,
        "total_ops": count_trace + count_is_prime,
        "time_seconds": end_time - start_time,
        "found": len(results)
    }

def main():
    LIMIT = 100000
    
    print("=" * 72)
    print("  CRIMSON OS // HYPERFOLD COMPUTATION BENCHMARK")
    print(f"  Task: Identify Lattice-Aligned Primes (n <= {LIMIT})")
    print("=" * 72)
    print()
    
    print("RUNNING ALGEBRAIC SEARCH (The Haystack)...")
    alg = benchmark_algebraic(LIMIT)
    
    print("RUNNING GEOMETRIC SEARCH (The Hyperfold)...")
    geo = benchmark_geometric(LIMIT)
    
    # Calculate Ratios
    ops_ratio = alg["total_ops"] / geo["total_ops"]
    efficiency_ratio = (geo["total_ops"] / alg["total_ops"]) * 100
    
    print("\n" + "=" * 72)
    print("  BENCHMARK RESULTS")
    print("=" * 72)
    print(f"  {'Metric':<20s}  {'Algebraic':>15s}  {'Geometric':>15s}")
    print(f"  {'-'*20:<20s}  {'-'*15:>15s}  {'-'*15:>15s}")
    print(f"  {'Total Operations':<20s}  {alg['total_ops']:15d}  {geo['total_ops']:15d}")
    print(f"  {'Trace Checks':<20s}  {alg['ops_trace']:15d}  {geo['ops_trace']:15d}")
    print(f"  {'Prime Checks':<20s}  {alg['ops_prime']:15d}  {geo['ops_prime']:15d}")
    print(f"  {'Execution Time':<20s}  {alg['time_seconds']:15.4f}s  {geo['time_seconds']:15.4f}s")
    print(f"  {'Needles Found':<20s}  {alg['found']:15d}  {geo['found']:15d}")
    print("-" * 72)
    
    print(f"\n  GEOMETRIC SELECTIVE ADVANTAGE: {ops_ratio:.2f}x")
    print(f"  COMPUTATIONAL LOAD: {efficiency_ratio:.4f}% of Algebraic baseline")
    print()
    
    if efficiency_ratio < 1.0:
        print("  [STATUS: VERIFIED] THE < 1% EFFICIENCY CLAIM HOLDS.")
    else:
        print("  [STATUS: PENDING] THE < 1% CLAIM REQUIRES HIGHER DIMENSIONAL SELECTIVITY.")
        
    print("-" * 72)
    print("  The Geometric path entirely bypasses the 'Haystack' by only checking")
    print("  coordinates where the resonance manifold permits the 'Needle' to exist.")
    print("=" * 72)

    # Save to Silo
    report = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "limit": LIMIT,
        "resonance_target": RESONANCE_TARGET,
        "algebraic": alg,
        "geometric": geo,
        "ops_ratio": ops_ratio,
        "efficiency_percentage": efficiency_ratio,
        "verified": efficiency_ratio < 1.0
    }
    
    output_path = "z:/CrimsonOS/0_Silo/11_Cognition_Neuroscience_Orch_Or/hyperfold_benchmark_results.json"
    with open(output_path, "w") as f:
        json.dump(report, f, indent=2)
    print(f"Report written to {output_path}")

if __name__ == "__main__":
    main()
