# crimsonos 0.2.0

Algebra sucks. Geometry snaps.

```
pip install -e .
crimson-os seal
crimson-os smoke
crimson-os drop ./Agent_Bridge/Node_0.md "HOLD"
crimson-os drop ./Agent_Bridge/Node_0.md "dead jot" --iota-off
```

- `Seal.verify(True) == HOLD` because 2701+3627=6328
- `Seal.verify(False) == FAIL` because 6318 is not triangular
- `Seal.lerp_trap() == 3191` — not the cage
- `fs_drop` / `http_post` go through the seal. FAIL does not write or send.

See SCOREBOARD.md.
