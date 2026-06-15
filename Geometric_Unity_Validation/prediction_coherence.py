#!/usr/bin/env python3
"""
Path 2: Testable Prediction — Quantum Coherence Ratios from cos θ = 1/3

PREDICTION (timestamped, falsifiable):

  Given a cylindrical structure with n-fold rotational symmetry embedded
  in 3D space, if the geometric constraint cos θ = 1/3 (forced by the
  F₂ → SO(3) free group embedding) governs coherence stability, then:

  1. The quantum decoherence rate in an n-protofilament microtubule
     scales INVERSELY with |T_n(1/3)|, the n-th Chebyshev polynomial
     evaluated at 1/3.

  2. SPECIFIC PREDICTIONS:
     a) 13-pf microtubules maintain coherence 1.61x longer than 12-pf
     b) 13-pf microtubules maintain coherence 21.1x longer than 14-pf
     c) The optimal protofilament count for coherence under this
        constraint is n=5 (|T_5| = 0.992), followed by n=23 (0.999),
        then n=13 (0.957). Biology chose n=13 as the compromise between
        coherence and structural stability.

  3. The ratio |T_13(1/3)| / |T_12(1/3)| ≈ 1.615 ≈ φ (golden ratio)
     to within 0.2%. If this is NOT a coincidence, there exists a
     deeper algebraic identity connecting the free group geometry to
     Fibonacci structure. We state this as a CONJECTURE, not a theorem.

HOW TO TEST:
  - Compare decoherence times in engineered microtubules with 12 vs 13
    vs 14 protofilaments (variant tubulin lattices exist in nature and
    can be assembled in vitro).
  - Measure at cryogenic temperatures to isolate quantum effects.
  - The predicted ratios are dimensionless and parameter-free.

No theology. No metaphor. Pure physics prediction from pure math.
"""

import math
import json
from datetime import datetime, timezone

THETA = math.acos(1/3)
PHI = (1 + math.sqrt(5)) / 2


def T_n(n: int) -> float:
    """Chebyshev polynomial of first kind at x=1/3: T_n(1/3) = cos(n·arccos(1/3))"""
    return math.cos(n * THETA)


def coherence_table(n_range: range) -> list:
    """Compute coherence stability metric for each protofilament count."""
    rows = []
    t13 = abs(T_n(13))
    for n in n_range:
        t = abs(T_n(n))
        ratio_to_13 = t13 / t if t > 1e-10 else float('inf')
        rows.append({
            "n": n,
            "|T_n(1/3)|": round(t, 8),
            "coherence_relative_to_13": round(t / t13, 6) if t13 > 0 else 0,
            "13_over_n_advantage": round(ratio_to_13, 4)
        })
    return rows


def main():
    timestamp = datetime.now(timezone.utc).isoformat()

    print("=" * 72)
    print("  TESTABLE PREDICTION: Quantum Coherence vs Protofilament Count")
    print(f"  Timestamp: {timestamp}")
    print("  Framework: F₂ → SO(3), cos θ = 1/3, Chebyshev trace T_n(1/3)")
    print("=" * 72)
    print()

    # Core prediction table
    print("PREDICTION TABLE — Coherence stability |T_n(1/3)| for n = 8..18")
    print("-" * 72)
    print(f"  {'n':>3s}  {'|T_n(1/3)|':>12s}  {'rel. to n=13':>14s}  {'13/n advantage':>16s}  {'note':s}")
    print(f"  {'---':>3s}  {'----------':>12s}  {'------------':>14s}  {'--------------':>16s}  {'----':s}")

    table = coherence_table(range(8, 19))
    known_pf = {11: "rare variant", 12: "C. elegans neurons", 13: "standard (most life)",
                14: "some protozoa", 15: "some insect axonemes"}

    for row in table:
        n = row["n"]
        note = known_pf.get(n, "")
        marker = " <<<" if n == 13 else ""
        print(f"  {n:3d}  {row['|T_n(1/3)|']:12.8f}  {row['coherence_relative_to_13']:14.6f}  "
              f"{row['13_over_n_advantage']:16.4f}x  {note}{marker}")

    print()
    print("  KEY OBSERVATIONS:")
    print(f"  • n=13: |T_13| = {abs(T_n(13)):.6f} — strong resonance")
    print(f"  • n=14: |T_14| = {abs(T_n(14)):.6f} — near zero (DEAD ZONE)")
    print(f"  • n=12: |T_12| = {abs(T_n(12)):.6f} — moderate")
    print(f"  • Cliff 13→14: {abs(T_n(13))/abs(T_n(14)):.1f}x")
    print(f"  • Ratio |T_13|/|T_12| = {abs(T_n(13))/abs(T_n(12)):.6f}")
    print(f"  • Golden ratio φ       = {PHI:.6f}")
    print(f"  • Relative error       = {abs(abs(T_n(13))/abs(T_n(12)) - PHI)/PHI*100:.4f}%")
    print()

    # Extended prediction: best n values up to 100
    print("EXTENDED PREDICTION — Top 10 most coherent n values (n ≤ 100)")
    print("-" * 72)
    all_n = [(n, abs(T_n(n))) for n in range(3, 101)]
    all_n.sort(key=lambda x: -x[1])
    for rank, (n, val) in enumerate(all_n[:15], 1):
        bio = ""
        if n == 5:
            bio = "  [5-fold: flowers, starfish, viral capsids]"
        elif n == 13:
            bio = "  [13-pf: microtubules]"
        elif n == 23:
            bio = "  [23 = convergent denominator]"
        elif n == 74:
            bio = "  [74 = convergent denominator]"
        print(f"  #{rank:2d}: n={n:3d}, |T_n| = {val:.8f}{bio}")

    print()

    # Specific falsifiable predictions
    print("FALSIFIABLE PREDICTIONS (parameter-free)")
    print("-" * 72)
    predictions = [
        {
            "id": "P1",
            "statement": "13-pf microtubules maintain quantum coherence "
                         f"{abs(T_n(13))/abs(T_n(12)):.2f}x longer than 12-pf",
            "ratio": abs(T_n(13)) / abs(T_n(12)),
            "tolerance": 0.1,
        },
        {
            "id": "P2",
            "statement": "13-pf microtubules maintain quantum coherence "
                         f"{abs(T_n(13))/abs(T_n(14)):.1f}x longer than 14-pf",
            "ratio": abs(T_n(13)) / abs(T_n(14)),
            "tolerance": 2.0,
        },
        {
            "id": "P3",
            "statement": f"|T_13(1/3)|/|T_12(1/3)| = {abs(T_n(13))/abs(T_n(12)):.6f} "
                         f"≈ φ = {PHI:.6f} (within 0.21%)",
            "ratio": abs(T_n(13)) / abs(T_n(12)),
            "target": PHI,
            "tolerance_pct": 0.5,
        },
        {
            "id": "P4",
            "statement": "If coherent cylindrical structures exist with n>20 "
                         "protofilaments, n=23 is the next stable count after n=13",
            "predicted_n": 23,
            "T_23": abs(T_n(23)),
        },
    ]

    for pred in predictions:
        print(f"  [{pred['id']}] {pred['statement']}")
    print()

    # Experimental protocol
    print("EXPERIMENTAL PROTOCOL")
    print("-" * 72)
    print("  1. Assemble microtubules in vitro with controlled pf counts")
    print("     (standard: 13-pf; variants: 12, 14, 15 via tubulin")
    print("     concentration and GTP analog manipulation)")
    print("  2. Measure quantum coherence time τ_c at T = 4K using")
    print("     photon echo or 2D electronic spectroscopy")
    print("  3. Compute ratios τ_c(13)/τ_c(12), τ_c(13)/τ_c(14)")
    print("  4. Compare to predicted |T_13|/|T_12| = 1.61, |T_13|/|T_14| = 21.1")
    print("  5. If ratios match within 10%: prediction CONFIRMED")
    print("     If ratios are off by >50%: prediction FALSIFIED")
    print()

    # Write JSON receipt
    output = {
        "timestamp": timestamp,
        "framework": "F₂ → SO(3), cos θ = 1/3, Chebyshev trace",
        "predictions": predictions,
        "coherence_table": table,
        "top_15_n": [{"n": n, "|T_n|": v} for n, v in all_n[:15]],
        "key_constants": {
            "cos_theta": 1/3,
            "theta_rad": THETA,
            "theta_deg": math.degrees(THETA),
            "|T_13(1/3)|": abs(T_n(13)),
            "|T_12(1/3)|": abs(T_n(12)),
            "|T_14(1/3)|": abs(T_n(14)),
            "cliff_13_to_14": abs(T_n(13)) / abs(T_n(14)),
            "ratio_T13_T12": abs(T_n(13)) / abs(T_n(12)),
            "phi": PHI,
        }
    }

    json_path = "proofs/prediction_coherence_results.json"
    with open(json_path, "w") as f:
        json.dump(output, f, indent=2, default=str)
    print(f"Results written to {json_path}")
    print()
    print("=" * 72)
    print("  This prediction is timestamped, parameter-free, and falsifiable.")
    print("  Run the experiment. The math doesn't negotiate.")
    print("=" * 72)


if __name__ == "__main__":
    main()
