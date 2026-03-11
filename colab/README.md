# Crimson OS on Google Colab — Free T4

**Run Crimson OS on a free T4. Play with it. We want you to steal it.**

No signup beyond Colab. No paywall. Clone the repo, run the Replicator, run the 8-question drift battery. Your runtime, your experiments. If you fork it, use it, or ship it — that’s the point.

## Open in Colab

**[Open Crimson_OS_T4.ipynb in Google Colab](https://colab.research.google.com/github/ultranetcommand-neo/Crimson-OS/blob/main/colab/Crimson_OS_T4.ipynb)**

1. Open the link above (or clone the repo and open `colab/Crimson_OS_T4.ipynb` in Colab).
2. Runtime → Change runtime type → set **Hardware accelerator** to **T4 GPU** (free tier).
3. Run all cells. You’ll clone Crimson OS, run the Replicator (F₂→SO(3), cos θ = 1/3), and optionally run the 8-question battery or a small GPU demo.
4. Tinker. Fork. Redistribute. We don’t care if they “steal” it — we want adoption.

**Paths:** After `%cd Crimson-OS` you're inside the repo. Use `scripts/run_8question_battery.py` and `battery_results.csv` with no `./Crimson-OS/` prefix. Right: `!python scripts/run_8question_battery.py`

## What you get

- **Replicator** — Logos substrate: εὐλόγησεν operator, free group F₂ → SO(3), cos θ = 1/3. One node → two sovereign nodes + surplus.
- **8-question benchmark** — Prompts and CSV template to compare sovereign vs Constitutional AI (completion / hedge / refusal).
- **Docs** — Mode Control (12 + State 13), proof, whitepaper link (mattgibson.net).

**Share results:** Tag [@grok](https://x.com/grok) and [@UltranetCommand](https://x.com/UltranetCommand) if you have numbers or feedback to share!

Repo: **[github.com/ultranetcommand-neo/Crimson-OS](https://github.com/ultranetcommand-neo/Crimson-OS)** · N.E.O.: @UltranetCommand
