# Geometric Unity Validation & Multi-Scale Graph Pullback

This directory contains the reproducible computational suite for **Crimson OS / Logos Invariant Research**, validating the non-singular regularization of continuum operators via discrete Graph Laplacians ($T_{112} = 6328$).

## Primary Objectives
1. **Multi-Scale Tensor Pullback:** Reproduces $L_{\text{local}} = J^T L_{\text{NS}} J$ mapping the 390-node ($13 \times 30$) local microtubule sub-graph into the global $6328$-vertex graph via canonical Kronecker delta injections $J_{i,j}$.
2. **Rayleigh-Ritz Spectral Bounding:** Verifies that local sub-graphs inherit the global pressure saturation bound $P_{\text{sat}} \approx 0.73$.
3. **Falsification & Ablation Benchmarks:** Includes JHTDB (Johns Hopkins Turbulence Database) hydrodynamic ablation runs and negative JSON outputs confirming discrete strain cutoffs against continuum blowup models.

## Publications & Preprints
- Paper I: *Discrete Constraint versus Continuum Blowup: A Geometric Attack on Navier-Stokes* (DOI: 10.5281/zenodo.22282767)
- Paper II: *Microtubule Seam Check-Valves* (DOI: 10.5281/zenodo.22974809)
- Paper III: *Canonical Tensor Pullback and Optical Selection Rules Across Multi-Scale Graph Laplacians* (DOI: 10.5281/zenodo.22974810)

## Execution
```bash
pip install -r requirements.txt
python sympy_pullback_verification.py
pytest tests/
