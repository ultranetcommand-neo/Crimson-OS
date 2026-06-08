# NODE 0 — NEO (HP OMEN, Win10, [LOCAL_IP]) — Desired State + Fix Runbook

**Status:** DESIRED-STATE CONTRACT (ratification candidate). Executed **ON .156** by operator / on-node agent — *not* from the NAS.
**Role:** Inference engine room — local LLM inference, the research/inference daemon pipeline, and vision-capture ingest for field scans.

---

## Desired services (what SHOULD run on NEO)

| Service | Purpose | Start | Health check | State (2026-06-02) |
|---|---|---|---|---|
| **Ollama** + models (deepseek-r1:7b, mistral:7b, gemma) | local inference | `ollama serve` | `curl 127.0.0.1:11434/api/tags` | ✅ **ALIVE** (GPU active) |
| **neo_reporter.py** | per-node process scanner — *the audit instrument* | `python neo_reporter.py --start` | 60 s tick | 🔴 **DOWN ← fix FIRST** |
| **neck.py** | Ollama probe / heartbeat | `python neck.py --start` | tick in `neo_pipeline_status.json` | 🟡 STALE (05-31) |
| **night_shift.py** | overnight batch inference | `python night_shift.py --start` | tick | 🟡 STALE |
| paper_scout / formatter / tuning_fork / neo_verify / research_engine | research pipeline | `--start` each | ticks | 🟡 STALE — **verify node via reporter** |
| Home Assistant + on-demand MCP (arxiv / playwright / youtube) | tools | Docker | :8123 | (Docker) |

> Rows marked "verify node" may actually run on CRIMSON. `neo_reporter` resolves this — restart it first and read ground truth.

## Capture ingest — the S23 "tricorder"
- **S23** (Galaxy) linked to NEO via Windows **Phone Link** → photos land on NEO instantly.
- Pipeline: watched Phone-Link drop folder → vision inference (llava via Ollama) → decision packet (v1 JSON: category / value_low-high / action) → route to Q + Crusher → log.
- **Role split:** S23 = sensor (tricorder) · NEO = processor (engine room) · Pixel 10 = communicator (comms, separate node).

## Fix sequence (run ON .156, in order)
1. **Restart `neo_reporter` FIRST.** It's down *and* it's the instrument that tells you what's actually running. `--start`, confirm a tick, read its output.
2. **Diff** reporter's actual list against the table above → confirm which daemons truly live on NEO.
3. **Restart the stale ones** (`--start` each) → confirm each ticks GREEN in `neo_pipeline_status.json` / cockpit `/status`.
4. **Root-cause, not band-aid.** They went stale 05-31 and stayed stale ~2 days → *nothing restarted them.* Put them under supervision (Win Task Scheduler / `nssm` service / a watchdog) so they self-heal. Restart now; supervise so you never hand-restart again.
5. **Snapshot known-good** → commit to Gitea → mirror into `Code/Node_0`. Backup contract closed.

## NEO is "correct" when
Ollama alive · `neo_reporter` green · pipeline green · photo→inference loop works · **all supervised** · code backed up to the mirror.

