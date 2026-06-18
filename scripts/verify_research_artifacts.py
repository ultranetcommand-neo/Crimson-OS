#!/usr/bin/env python3
"""CI verifier — research artifacts and published negative verdict integrity."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ABLATION = ROOT / "Geometric_Unity_Validation" / "jhtdb_ablation_results.json"
PROOF = ROOT / "Geometric_Unity_Validation" / "proof.md"
SCHEMA = ROOT / "schemas" / "build_log_entry.schema.json"

REQUIRED_VERDICT_KEYS = {
    "candidate_beats_random",
    "vf_matched_H22_positive_wins",
    "bootstrap_95ci_excludes_zero",
}


def fail(msg: str) -> None:
    print(f"VERIFY FAIL: {msg}", file=sys.stderr)
    sys.exit(1)


def ok(msg: str) -> None:
    print(f"VERIFY OK: {msg}")


def main() -> int:
    errors: list[str] = []

    if not PROOF.exists():
        errors.append("Geometric_Unity_Validation/proof.md missing")
    else:
        ok("proof.md present")

    if not SCHEMA.exists():
        errors.append("schemas/build_log_entry.schema.json missing")
    else:
        schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
        if "register" not in str(schema.get("properties", {})):
            errors.append("schema missing register field")
        else:
            ok("build log schema present")

    if not ABLATION.exists():
        errors.append("jhtdb_ablation_results.json missing")
    else:
        data = json.loads(ABLATION.read_text(encoding="utf-8"))
        verdict = data.get("verdict")
        if not isinstance(verdict, dict):
            errors.append("jhtdb_ablation_results.json: verdict block missing")
        else:
            missing = REQUIRED_VERDICT_KEYS - set(verdict.keys())
            if missing:
                errors.append(f"verdict missing keys: {sorted(missing)}")
            else:
                ok("jhtdb verdict block complete")
            if verdict.get("candidate_beats_random") is not False:
                errors.append(
                    "candidate_beats_random must remain false (published negative)"
                )
            else:
                ok("published negative intact: candidate_beats_random=false")

        if data.get("seed") != 1337:
            errors.append("pre-registered seed 1337 mismatch")
        if data.get("n_points") != 4000:
            errors.append("pre-registered n_points 4000 mismatch")

    if errors:
        for e in errors:
            print(f"VERIFY FAIL: {e}", file=sys.stderr)
        return 1

    print("VERIFY OK: all checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())