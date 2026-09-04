# Stranger path (this branch)

```
git clone -b smoke-0.2.0 https://github.com/ultranetcommand-neo/Crimson-OS.git
cd Crimson-OS/pkg
python3 -m pip install -e .
crimson-os seal
crimson-os smoke
crimson-os drop /tmp/bus.md HOLD
crimson-os drop /tmp/bus.md DEAD --iota-off
GITHUB_TOKEN=… crimson-os github-ping
```

Expected:

- iota-on HOLD
- iota-off FAIL
- lerp 3191.0
- smoke: crimson wins lock-vs-lerp
- second drop does not write
- github-ping hits api.github.com only if token present AND seal HOLD
