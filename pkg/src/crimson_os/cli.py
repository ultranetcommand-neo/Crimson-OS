#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(prog="crimson-os")
    sub = p.add_subparsers(dest="cmd")
    sub.add_parser("seal", help="print HOLD/FAIL")
    s = sub.add_parser("smoke", help="drift bench vs lerp-state")
    s.add_argument("target", nargs="?", default=".")
    d = sub.add_parser("drop", help="append text to a bus file through the seal")
    d.add_argument("path")
    d.add_argument("text")
    d.add_argument("--iota-off", action="store_true")
    args = p.parse_args(argv)

    if args.cmd == "seal":
        from .seal import Seal

        print("iota-on", Seal.verify(True))
        print("iota-off", Seal.verify(False))
        print("lerp", Seal.lerp_trap())
        return 0
    if args.cmd == "smoke":
        from .bench_drift import scoreboard

        out = scoreboard(args.target)
        print(json.dumps(out, indent=2))
        print("SCOREBOARD crimson", out["crimson_wins"], "langgraph", out["langgraph_wins"])
        return 0 if out["crimson_wins"] > out["langgraph_wins"] else 1
    if args.cmd == "drop":
        from .connectors import fs_drop

        print(json.dumps(fs_drop(args.path, args.text, iota_on=not args.iota_off)))
        return 0
    p.print_help()
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
