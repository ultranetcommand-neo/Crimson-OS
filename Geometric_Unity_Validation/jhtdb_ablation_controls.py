#!/usr/bin/env python3
"""JHTDB ablation controls — adversarial cutoffs, matched-n random subsamples, bootstrap CIs.

Fetches JHTDB once (seed 1337), reuses metrics for all filters. No post-fit tuning.
"""
from __future__ import annotations

import json
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
from zeep import Client

AUTH_TOKEN = "edu.jhu.pha.turbulence.testing-201302"
DATASET = "isotropic1024coarse"
N_POINTS = 4000
SEED = 1337
HIGH_ENSTROPHY_MULT = 3.0
BOOTSTRAP_N = 2000
CACHE_NAME = "jhtdb_metrics_cache.npz"
OUT_NAME = "jhtdb_ablation_results.json"


def generate_points(n: int) -> np.ndarray:
    return np.random.RandomState(SEED).uniform(0, 2 * np.pi, (n, 3))


def fetch_jhtdb(points: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    print(f"Connecting to JHTDB for {len(points)} points...")
    t0 = time.time()
    wsdl = "http://turbulence.pha.jhu.edu/service/turbulence.asmx?WSDL"
    client = Client(wsdl)
    Point3 = client.get_type("ns0:Point3")
    ArrayOfPoint3 = client.get_type("ns0:ArrayOfPoint3")
    pts = [Point3(x=float(p[0]), y=float(p[1]), z=float(p[2])) for p in points]
    points_array = ArrayOfPoint3(Point3=pts)

    grads = np.zeros((len(points), 3, 3))
    hessians = np.zeros((len(points), 3, 3))
    chunk = points_array.Point3

    print("  VelocityGradient...")
    res_a = client.service.GetVelocityGradient(
        authToken=AUTH_TOKEN,
        dataset=DATASET,
        time=0.0,
        spatialInterpolation="Fd4Lag4",
        temporalInterpolation="PCHIP",
        points=ArrayOfPoint3(Point3=chunk),
    )
    for j, vg in enumerate(res_a):
        grads[j] = [
            [vg["duxdx"], vg["duxdy"], vg["duxdz"]],
            [vg["duydx"], vg["duydy"], vg["duydz"]],
            [vg["duzdx"], vg["duzdy"], vg["duzdz"]],
        ]

    print("  PressureHessian...")
    res_h = client.service.GetPressureHessian(
        authToken=AUTH_TOKEN,
        dataset=DATASET,
        time=0.0,
        spatialInterpolation="Fd4Lag4",
        temporalInterpolation="PCHIP",
        points=ArrayOfPoint3(Point3=chunk),
    )
    for j, ph in enumerate(res_h):
        hessians[j] = [
            [ph["d2pdxdx"], ph["d2pdxdy"], ph["d2pdxdz"]],
            [ph["d2pdxdy"], ph["d2pdydy"], ph["d2pdydz"]],
            [ph["d2pdxdz"], ph["d2pdydz"], ph["d2pdzdz"]],
        ]

    print(f"  JHTDB fetch done in {time.time() - t0:.1f}s")
    return grads, hessians


def compute_metrics(grads: np.ndarray, hessians: np.ndarray) -> dict[str, np.ndarray]:
    rows: dict[str, list] = {
        "enstrophy": [],
        "cos2_phi1": [],
        "vf_accel": [],
        "H22": [],
    }
    for i in range(grads.shape[0]):
        a, h = grads[i], hessians[i]
        s = 0.5 * (a + a.T)
        omega = 0.5 * (a - a.T)
        w = np.array(
            [
                omega[2, 1] - omega[1, 2],
                omega[0, 2] - omega[2, 0],
                omega[1, 0] - omega[0, 1],
            ]
        )
        omega_sq = w @ w
        if omega_sq < 1e-10:
            continue
        w_hat = w / np.sqrt(omega_sq)
        evals, evecs = np.linalg.eigh(s)
        idx = np.argsort(evals)[::-1]
        evecs = evecs[:, idx]
        e1, e2 = evecs[:, 0], evecs[:, 1]
        lambda_2 = evals[idx][1]
        cos2_phi1 = (w_hat @ e1) ** 2
        cos2_phi2 = (w_hat @ e2) ** 2
        vf = 0.25 * omega_sq * cos2_phi2 - lambda_2**2
        h22 = e2 @ h @ e2
        rows["enstrophy"].append(omega_sq)
        rows["cos2_phi1"].append(cos2_phi1)
        rows["vf_accel"].append(vf)
        rows["H22"].append(h22)
    return {k: np.array(v) for k, v in rows.items()}


def subset_stats(metrics: dict[str, np.ndarray], mask: np.ndarray) -> dict:
    n = int(np.sum(mask))
    if n == 0:
        return {"n": 0, "mean_H22": None, "mean_vf": None, "ratio": None, "mean_cos2_phi1": None}
    vf = metrics["vf_accel"][mask]
    h22 = metrics["H22"][mask]
    mean_vf = float(np.mean(vf))
    mean_h22 = float(np.mean(h22))
    ratio = mean_h22 / mean_vf if mean_vf != 0 else None
    return {
        "n": n,
        "mean_cos2_phi1": float(np.mean(metrics["cos2_phi1"][mask])),
        "mean_vf": mean_vf,
        "mean_H22": mean_h22,
        "ratio": float(ratio) if ratio is not None else None,
        "frac_H22_positive": float(np.mean(h22 > 0)),
    }


def high_enstrophy_mask(metrics: dict[str, np.ndarray]) -> np.ndarray:
    thr = HIGH_ENSTROPHY_MULT * np.mean(metrics["enstrophy"])
    return metrics["enstrophy"] > thr


def bootstrap_ratio_ci(
    metrics: dict[str, np.ndarray],
    mask: np.ndarray,
    n_boot: int = BOOTSTRAP_N,
    seed: int = SEED,
) -> dict:
    idx = np.where(mask)[0]
    if len(idx) < 5:
        return {"n": len(idx), "ci_low": None, "ci_high": None, "median": None}
    rng = np.random.RandomState(seed + 1)
    ratios = []
    vf_all = metrics["vf_accel"]
    h22_all = metrics["H22"]
    for _ in range(n_boot):
        pick = rng.choice(idx, size=len(idx), replace=True)
        vf = vf_all[pick]
        h22 = h22_all[pick]
        m_vf = np.mean(vf)
        if abs(m_vf) < 1e-12:
            continue
        ratios.append(np.mean(h22) / m_vf)
    ratios = np.array(ratios)
    return {
        "n": len(idx),
        "median": float(np.median(ratios)),
        "ci_low": float(np.percentile(ratios, 2.5)),
        "ci_high": float(np.percentile(ratios, 97.5)),
    }


def vf_matched_control(
    metrics: dict[str, np.ndarray],
    base_mask: np.ndarray,
    n_trials: int = 100,
    vf_tolerance: float = 0.05,
    seed: int = SEED,
) -> dict:
    """Match candidate subset size and mean |VF_accel| from high-enstrophy pool (no cos2 filter)."""
    rng = np.random.RandomState(seed + 3)
    hi = high_enstrophy_mask(metrics)
    hi_idx = np.where(hi)[0]
    n_target = int(np.sum(base_mask))
    if n_target == 0:
        return {"n_trials": 0}

    target_vf = float(np.mean(np.abs(metrics["vf_accel"][base_mask])))
    vf_abs = np.abs(metrics["vf_accel"])

    ratios: list[float] = []
    pos_fracs: list[float] = []
    mean_h22s: list[float] = []
    matched_vf_errors: list[float] = []

    for _ in range(n_trials):
        best_pick = None
        best_err = float("inf")
        # Rejection sampling: draw subsets until mean |VF| within tolerance
        for _attempt in range(200):
            pick = rng.choice(hi_idx, size=n_target, replace=False)
            m_vf = float(np.mean(vf_abs[pick]))
            err = abs(m_vf - target_vf) / target_vf
            if err < best_err:
                best_err = err
                best_pick = pick
            if err <= vf_tolerance:
                break
        assert best_pick is not None
        mask = np.zeros(len(metrics["enstrophy"]), dtype=bool)
        mask[best_pick] = True
        st = subset_stats(metrics, mask)
        if st["ratio"] is not None:
            ratios.append(st["ratio"])
            pos_fracs.append(st["frac_H22_positive"])
            mean_h22s.append(st["mean_H22"])
            matched_vf_errors.append(best_err)

    cand = subset_stats(metrics, base_mask)
    ratios_a = np.array(ratios)
    pos_a = np.array(pos_fracs)
    return {
        "n_trials": len(ratios),
        "n_per_trial": n_target,
        "target_mean_abs_vf": target_vf,
        "vf_tolerance_frac": vf_tolerance,
        "candidate": {
            "mean_abs_vf": float(np.mean(np.abs(metrics["vf_accel"][base_mask]))),
            "frac_H22_positive": cand["frac_H22_positive"],
            "ratio": cand["ratio"],
            "mean_H22": cand["mean_H22"],
        },
        "control_ratio_median": float(np.median(ratios_a)),
        "control_ratio_mean": float(np.mean(ratios_a)),
        "control_frac_H22_positive_median": float(np.median(pos_a)),
        "control_frac_H22_positive_mean": float(np.mean(pos_a)),
        "control_mean_H22_median": float(np.median(mean_h22s)),
        "candidate_beats_control_on_H22_positive": (
            cand["frac_H22_positive"] is not None
            and float(np.median(pos_a)) is not None
            and cand["frac_H22_positive"] > float(np.median(pos_a))
        ),
        "mean_vf_match_error": float(np.mean(matched_vf_errors)),
    }


def permutation_control(
    metrics: dict[str, np.ndarray],
    base_mask: np.ndarray,
    n_trials: int = 500,
    seed: int = SEED,
) -> dict:
    """Shuffle cos2_phi1 within high-enstrophy pool; re-apply cos2<=1/9 cutoff."""
    rng = np.random.RandomState(seed + 4)
    hi = high_enstrophy_mask(metrics)
    hi_idx = np.where(hi)[0]
    cos2_hi = metrics["cos2_phi1"][hi_idx].copy()
    n_target = int(np.sum(base_mask))
    cutoff = 1.0 / 9.0

    cand = subset_stats(metrics, base_mask)
    perm_ratios: list[float] = []
    perm_pos: list[float] = []
    perm_ns: list[int] = []

    for _ in range(n_trials):
        shuffled = cos2_hi.copy()
        rng.shuffle(shuffled)
        fake_cos2 = metrics["cos2_phi1"].copy()
        fake_cos2[hi_idx] = shuffled
        mask = hi & (fake_cos2 <= cutoff)
        st = subset_stats(metrics, mask)
        perm_ns.append(st["n"])
        if st["ratio"] is not None and st["n"] > 0:
            perm_ratios.append(st["ratio"])
            perm_pos.append(st["frac_H22_positive"])

    perm_pos_a = np.array(perm_pos)
    perm_ratio_a = np.array(perm_ratios)
    cand_pos = cand["frac_H22_positive"] or 0.0
    p_value_pos = float(np.mean(perm_pos_a >= cand_pos)) if len(perm_pos_a) else None

    return {
        "n_trials": n_trials,
        "candidate_frac_H22_positive": cand_pos,
        "permuted_frac_H22_positive_median": float(np.median(perm_pos_a)) if len(perm_pos_a) else None,
        "permuted_frac_H22_positive_mean": float(np.mean(perm_pos_a)) if len(perm_pos_a) else None,
        "p_value_frac_H22_positive": p_value_pos,
        "candidate_ratio": cand["ratio"],
        "permuted_ratio_median": float(np.median(perm_ratio_a)) if len(perm_ratio_a) else None,
        "permuted_n_median": float(np.median(perm_ns)),
    }


def bootstrap_h22_positive_ci(
    metrics: dict[str, np.ndarray],
    mask: np.ndarray,
    n_boot: int = BOOTSTRAP_N,
    seed: int = SEED,
) -> dict:
    idx = np.where(mask)[0]
    if len(idx) < 5:
        return {"n": len(idx), "rate": None, "ci_low": None, "ci_high": None}
    h22 = metrics["H22"]
    rng = np.random.RandomState(seed + 5)
    rates = []
    for _ in range(n_boot):
        pick = rng.choice(idx, size=len(idx), replace=True)
        rates.append(float(np.mean(h22[pick] > 0)))
    rates_a = np.array(rates)
    return {
        "n": len(idx),
        "rate": float(np.mean(h22[idx] > 0)),
        "median": float(np.median(rates_a)),
        "ci_low": float(np.percentile(rates_a, 2.5)),
        "ci_high": float(np.percentile(rates_a, 97.5)),
    }


def two_thirds_null_test(
    metrics: dict[str, np.ndarray],
    mask: np.ndarray,
    null_rate: float = 2.0 / 3.0,
    n_boot: int = BOOTSTRAP_N,
    seed: int = SEED,
) -> dict:
    """Test whether observed H22>0 rate is consistent with 2/3 null."""
    boot = bootstrap_h22_positive_ci(metrics, mask, n_boot=n_boot, seed=seed)
    if boot["rate"] is None:
        return {"null_rate": null_rate, "consistent_with_two_thirds": None}
    # two-sided: fraction of bootstrap draws whose distance from null exceeds observed distance
    idx = np.where(mask)[0]
    h22 = metrics["H22"]
    rng = np.random.RandomState(seed + 6)
    obs = boot["rate"]
    rates = []
    for _ in range(n_boot):
        pick = rng.choice(idx, size=len(idx), replace=True)
        rates.append(float(np.mean(h22[pick] > 0)))
    rates_a = np.array(rates)
    obs_dist = abs(obs - null_rate)
    perm_dist = np.abs(rates_a - null_rate)
    p_two_sided = float(np.mean(perm_dist >= obs_dist))
    return {
        "null_rate": null_rate,
        "observed_rate": obs,
        "bootstrap_ci": [boot["ci_low"], boot["ci_high"]],
        "p_value_vs_two_thirds": p_two_sided,
        "consistent_with_two_thirds": boot["ci_low"] <= null_rate <= boot["ci_high"],
        "failure_rate": 1.0 - obs,
    }


def tighter_geometry_trend(filters: dict[str, dict]) -> dict:
    """Compare H22>0 across tightening cos2 cutoffs."""
    order = ["loose_1_2", "loose_1_4", "loose_1_6", "candidate_1_9", "tight_1_12"]
    series = []
    for name in order:
        st = filters.get(name, {})
        if st.get("frac_H22_positive") is not None:
            series.append({
                "filter": name,
                "cos2_cutoff": st.get("cos2_cutoff"),
                "n": st["n"],
                "frac_H22_positive": st["frac_H22_positive"],
            })
    # tighter cutoff = smaller cos2_cutoff value
    tightening_lowers_restore = None
    if len(series) >= 2:
        by_tight = sorted(series, key=lambda x: x["cos2_cutoff"])
        rates = [x["frac_H22_positive"] for x in by_tight]
        # smallest cutoff (tightest) first → should have lowest restore if margin hypothesis holds
        tightening_lowers_restore = rates[0] < rates[-1]
    return {
        "series": series,
        "tighter_cutoff_lowers_H22_positive": tightening_lowers_restore,
    }


def h22_vf_coupling(metrics: dict[str, np.ndarray], mask: np.ndarray) -> dict:
    """Coupling in danger zone: when VF drives singularity (VF>0), does H22 oppose?"""
    vf = metrics["vf_accel"][mask]
    h22 = metrics["H22"][mask]
    n = len(vf)
    if n == 0:
        return {"n": 0}
    danger = vf > 0
    n_danger = int(np.sum(danger))
    oppose = (vf > 0) & (h22 > 0)
    same_sign_both_pos = (vf > 0) & (h22 > 0)
    corr = float(np.corrcoef(vf, h22)[0, 1]) if n > 2 else None
    return {
        "n": n,
        "n_vf_positive": n_danger,
        "frac_vf_positive": float(n_danger / n),
        "frac_h22_positive_when_vf_positive": (
            float(np.mean(h22[danger] > 0)) if n_danger > 0 else None
        ),
        "frac_opposing_when_vf_positive": (
            float(np.mean(h22[danger] > 0)) if n_danger > 0 else None
        ),
        "pearson_vf_h22": corr,
        "mean_vf": float(np.mean(vf)),
        "mean_h22": float(np.mean(h22)),
    }


def h22_vf_sign_matched_test(
    metrics: dict[str, np.ndarray],
    base_mask: np.ndarray,
    n_trials: int = 200,
    vf_tolerance: float = 0.05,
    seed: int = SEED,
) -> dict:
    """VF-matched sign test: when VF>0 (singularity driver), does H22>0 (restoring oppose)?"""
    rng = np.random.RandomState(seed + 7)
    hi = high_enstrophy_mask(metrics)
    hi_idx = np.where(hi)[0]
    n_target = int(np.sum(base_mask))
    if n_target == 0:
        return {"n": 0}

    vf = metrics["vf_accel"]
    h22 = metrics["H22"]
    vf_abs = np.abs(vf)

    def sign_stats(mask: np.ndarray) -> dict:
        v, h = vf[mask], h22[mask]
        pos_vf = v > 0
        n = int(np.sum(mask))
        n_pv = int(np.sum(pos_vf))
        if n_pv == 0:
            return {"n": n, "n_vf_positive": 0}
        oppose = pos_vf & (h > 0)
        fail = pos_vf & (h <= 0)
        return {
            "n": n,
            "n_vf_positive": n_pv,
            "frac_vf_positive": float(n_pv / n),
            "frac_opposing_h22_when_vf_positive": float(np.mean(h[pos_vf] > 0)),
            "frac_failure_when_vf_positive": float(np.mean(h[pos_vf] <= 0)),
            "mean_h22_when_vf_positive": float(np.mean(h[pos_vf])),
            "mean_vf_when_positive": float(np.mean(v[pos_vf])),
            "mean_restoring_ratio_h22_over_vf": float(np.mean(h[pos_vf] / v[pos_vf])),
            "pearson_vf_h22_on_vf_positive": (
                float(np.corrcoef(v[pos_vf], h[pos_vf])[0, 1]) if n_pv > 2 else None
            ),
        }

    candidate = sign_stats(base_mask)
    target_vf = float(np.mean(vf_abs[base_mask]))

    control_opposing: list[float] = []
    control_ratio: list[float] = []
    control_mean_h22: list[float] = []

    for _ in range(n_trials):
        best_pick = None
        best_err = float("inf")
        for _attempt in range(200):
            pick = rng.choice(hi_idx, size=n_target, replace=False)
            m_vf = float(np.mean(vf_abs[pick]))
            err = abs(m_vf - target_vf) / target_vf
            if err < best_err:
                best_err = err
                best_pick = pick
            if err <= vf_tolerance:
                break
        mask = np.zeros(len(vf), dtype=bool)
        mask[best_pick] = True
        st = sign_stats(mask)
        if st.get("frac_opposing_h22_when_vf_positive") is not None:
            control_opposing.append(st["frac_opposing_h22_when_vf_positive"])
            control_ratio.append(st["mean_restoring_ratio_h22_over_vf"])
            control_mean_h22.append(st["mean_h22_when_vf_positive"])

    opp_a = np.array(control_opposing)
    cand_opp = candidate["frac_opposing_h22_when_vf_positive"]
    p_opp = float(np.mean(opp_a <= cand_opp)) if len(opp_a) else None

    boot_rng = np.random.RandomState(seed + 8)
    idx = np.where(base_mask)[0]
    boot_opp = []
    for _ in range(BOOTSTRAP_N):
        pick = boot_rng.choice(idx, size=len(idx), replace=True)
        v, h = vf[pick], h22[pick]
        pos = v > 0
        if np.sum(pos) > 0:
            boot_opp.append(float(np.mean(h[pos] > 0)))
    boot_opp_a = np.array(boot_opp)

    return {
        "target_mean_abs_vf": target_vf,
        "vf_tolerance_frac": vf_tolerance,
        "n_trials": len(control_opposing),
        "candidate": candidate,
        "control_opposing_median": float(np.median(opp_a)) if len(opp_a) else None,
        "control_opposing_mean": float(np.mean(opp_a)) if len(opp_a) else None,
        "control_opposing_std": float(np.std(opp_a)) if len(opp_a) else None,
        "control_ratio_median": float(np.median(control_ratio)) if control_ratio else None,
        "control_mean_h22_median": float(np.median(control_mean_h22)) if control_mean_h22 else None,
        "p_value_candidate_opposing_leq_control": p_opp,
        "candidate_lower_opposing_than_vf_matched": (
            cand_opp is not None
            and len(opp_a) > 0
            and cand_opp < float(np.median(opp_a))
        ),
        "bootstrap_opposing_ci": [
            float(np.percentile(boot_opp_a, 2.5)),
            float(np.percentile(boot_opp_a, 97.5)),
        ],
        "two_thirds_consistent_opposing": (
            boot_opp_a.size > 0
            and float(np.percentile(boot_opp_a, 2.5)) <= 2.0 / 3.0 <= float(np.percentile(boot_opp_a, 97.5))
        ),
    }


def random_matched_control(
    metrics: dict[str, np.ndarray],
    base_mask: np.ndarray,
    n_trials: int = 50,
    seed: int = SEED,
) -> dict:
    """Same n as base filter, random high-enstrophy points (ignore cos2_phi1)."""
    rng = np.random.RandomState(seed + 2)
    hi = high_enstrophy_mask(metrics)
    hi_idx = np.where(hi)[0]
    n_target = int(np.sum(base_mask))
    if n_target == 0 or len(hi_idx) < n_target:
        return {"n_trials": 0, "ratio_mean": None, "ratio_std": None}
    ratios = []
    for _ in range(n_trials):
        pick = rng.choice(hi_idx, size=n_target, replace=False)
        mask = np.zeros(len(metrics["enstrophy"]), dtype=bool)
        mask[pick] = True
        st = subset_stats(metrics, mask)
        if st["ratio"] is not None:
            ratios.append(st["ratio"])
    ratios = np.array(ratios)
    return {
        "n_trials": n_trials,
        "n_per_trial": n_target,
        "ratio_mean": float(np.mean(ratios)),
        "ratio_std": float(np.std(ratios)),
        "ratio_median": float(np.median(ratios)),
    }


def run_ablation(metrics: dict[str, np.ndarray]) -> dict:
    hi = high_enstrophy_mask(metrics)
    cutoffs = {
        "candidate_1_9": 1.0 / 9.0,
        "loose_1_6": 1.0 / 6.0,
        "loose_1_4": 1.0 / 4.0,
        "loose_1_2": 1.0 / 2.0,
        "tight_1_12": 1.0 / 12.0,
    }
    filters: dict[str, dict] = {}
    for name, c in cutoffs.items():
        mask = hi & (metrics["cos2_phi1"] <= c)
        filters[name] = {
            "cos2_cutoff": c,
            **subset_stats(metrics, mask),
        }

    # High enstrophy only (no geometric filter)
    filters["high_enstrophy_only"] = {
        "cos2_cutoff": None,
        **subset_stats(metrics, hi),
    }

    base_mask = hi & (metrics["cos2_phi1"] <= 1.0 / 9.0)
    candidate = filters["candidate_1_9"]
    rnd = random_matched_control(metrics, base_mask)
    vf_ctl = vf_matched_control(metrics, base_mask)
    perm = permutation_control(metrics, base_mask)

    two_thirds = two_thirds_null_test(metrics, base_mask)
    geom_trend = tighter_geometry_trend(filters)
    coupling = h22_vf_coupling(metrics, base_mask)
    sign_test = h22_vf_sign_matched_test(metrics, base_mask)

    return {
        "filters": filters,
        "bootstrap_candidate": bootstrap_ratio_ci(metrics, base_mask),
        "random_matched_control": rnd,
        "vf_matched_control": vf_ctl,
        "permutation_control": perm,
        "two_thirds_null_test": two_thirds,
        "tighter_geometry_trend": geom_trend,
        "h22_vf_coupling": coupling,
        "h22_vf_sign_matched_test": sign_test,
        "candidate_beats_random_median": (
            candidate["ratio"] is not None
            and rnd["ratio_median"] is not None
            and candidate["ratio"] > rnd["ratio_median"]
        ),
    }


def main() -> int:
    out_dir = Path(__file__).resolve().parent
    cache_path = out_dir / CACHE_NAME
    json_path = out_dir / OUT_NAME

    print("=" * 72)
    print("  JHTDB ABLATION CONTROLS")
    print(f"  dataset={DATASET}  n={N_POINTS}  seed={SEED}")
    print("=" * 72)

    if cache_path.exists():
        print(f"Loading cached metrics from {cache_path.name}")
        data = np.load(cache_path)
        metrics = {k: data[k] for k in ("enstrophy", "cos2_phi1", "vf_accel", "H22")}
    else:
        points = generate_points(N_POINTS)
        grads, hessians = fetch_jhtdb(points)
        metrics = compute_metrics(grads, hessians)
        np.savez(cache_path, **metrics)
        print(f"Cached metrics -> {cache_path.name}")

    n_valid = len(metrics["enstrophy"])
    print(f"\nValid points: {n_valid}")

    ablation = run_ablation(metrics)
    print("\nFILTER COMPARISON (high enstrophy + cos2_phi1 cutoff):")
    print(f"  {'filter':<22} {'n':>6} {'ratio':>10} {'H22>0':>8}")
    print("  " + "-" * 50)
    for name, st in ablation["filters"].items():
        r = st["ratio"]
        r_s = f"{r:.4f}" if r is not None else "n/a"
        pos = st.get("frac_H22_positive")
        pos_s = f"{pos:.2%}" if pos is not None else "n/a"
        print(f"  {name:<22} {st['n']:>6} {r_s:>10} {pos_s:>8}")

    boot = ablation["bootstrap_candidate"]
    print(f"\nBOOTSTRAP CI (candidate 1/9): median={boot['median']:.4f}  "
          f"95% CI [{boot['ci_low']:.4f}, {boot['ci_high']:.4f}]")

    rnd = ablation["random_matched_control"]
    print(f"\nRANDOM MATCHED CONTROL (n={rnd['n_per_trial']}, {rnd['n_trials']} trials):")
    print(f"  ratio median={rnd['ratio_median']:.4f}  mean={rnd['ratio_mean']:.4f} ± {rnd['ratio_std']:.4f}")

    vf = ablation["vf_matched_control"]
    print(f"\nVF-MATCHED CONTROL (|VF| tol ±{vf['vf_tolerance_frac']*100:.0f}%, {vf['n_trials']} trials):")
    print(f"  target |VF|={vf['target_mean_abs_vf']:.1f}")
    print(f"  candidate H22>0: {vf['candidate']['frac_H22_positive']:.2%}  "
          f"control median: {vf['control_frac_H22_positive_median']:.2%}")
    print(f"  candidate mean H22: {vf['candidate']['mean_H22']:.2f}  "
          f"control median: {vf['control_mean_H22_median']:.2f}")
    print(f"  candidate beats control on H22>0: {vf['candidate_beats_control_on_H22_positive']}")

    perm = ablation["permutation_control"]
    print(f"\nPERMUTATION (shuffle cos2_phi1, {perm['n_trials']} trials):")
    print(f"  candidate H22>0: {perm['candidate_frac_H22_positive']:.2%}  "
          f"permuted median: {perm['permuted_frac_H22_positive_median']:.2%}")
    print(f"  p-value (perm >= candidate): {perm['p_value_frac_H22_positive']:.4f}")

    tt = ablation["two_thirds_null_test"]
    print(f"\n2/3 NULL TEST (H22>0 rate vs 66.67%):")
    print(f"  observed={tt['observed_rate']:.2%}  failure_rate={tt['failure_rate']:.2%}")
    print(f"  95% CI [{tt['bootstrap_ci'][0]:.2%}, {tt['bootstrap_ci'][1]:.2%}]")
    print(f"  consistent with 2/3: {tt['consistent_with_two_thirds']}  p={tt['p_value_vs_two_thirds']:.4f}")

    gt = ablation["tighter_geometry_trend"]
    print("\nTIGHTER GEOMETRY TREND (H22>0 vs cutoff):")
    for row in gt["series"]:
        print(f"  {row['filter']:<18} cutoff={row['cos2_cutoff']:.4f}  "
              f"n={row['n']:>4}  H22>0={row['frac_H22_positive']:.2%}")
    print(f"  tighter cutoff lowers restore rate: {gt['tighter_cutoff_lowers_H22_positive']}")

    cp = ablation["h22_vf_coupling"]
    print(f"\nH22-VF COUPLING (candidate subset):")
    print(f"  n={cp['n']}  VF>0: {cp['frac_vf_positive']:.2%}")
    if cp.get("frac_h22_positive_when_vf_positive") is not None:
        print(f"  H22>0 when VF>0: {cp['frac_h22_positive_when_vf_positive']:.2%}")
    print(f"  pearson(vf,h22)={cp['pearson_vf_h22']:.4f}")

    sg = ablation["h22_vf_sign_matched_test"]
    cs = sg["candidate"]
    print(f"\nH22-VF SIGN TEST (VF-matched, {sg['n_trials']} trials):")
    print(f"  candidate: VF>0 oppose rate={cs['frac_opposing_h22_when_vf_positive']:.2%}  "
          f"failure={cs['frac_failure_when_vf_positive']:.2%}")
    print(f"  candidate: mean H22|VF>0={cs['mean_h22_when_vf_positive']:.2f}  "
          f"H22/VF ratio={cs['mean_restoring_ratio_h22_over_vf']:.4f}")
    print(f"  VF-matched control oppose median={sg['control_opposing_median']:.2%}  "
          f"mean H22 median={sg['control_mean_h22_median']:.2f}")
    print(f"  candidate lower opposing than VF-matched: {sg['candidate_lower_opposing_than_vf_matched']}")
    print(f"  bootstrap opposing CI [{sg['bootstrap_opposing_ci'][0]:.2%}, "
          f"{sg['bootstrap_opposing_ci'][1]:.2%}]")

    cand_ratio = ablation["filters"]["candidate_1_9"]["ratio"]
    beats = cand_ratio is not None and cand_ratio > rnd["ratio_median"]
    print(f"\nCandidate (1/9) beats random matched median: {beats}")

    output = {
        "run_utc": datetime.now(timezone.utc).isoformat(),
        "dataset": DATASET,
        "n_points": N_POINTS,
        "seed": SEED,
        "n_valid": n_valid,
        "high_enstrophy_multiplier": HIGH_ENSTROPHY_MULT,
        **ablation,
        "verdict": {
            "candidate_ratio": cand_ratio,
            "random_median_ratio": rnd["ratio_median"],
            "candidate_beats_random": beats,
            "bootstrap_95ci_excludes_zero": boot["ci_low"] is not None and boot["ci_low"] > 0,
            "vf_matched_H22_positive_wins": vf["candidate_beats_control_on_H22_positive"],
            "permutation_p_value_H22_positive": perm["p_value_frac_H22_positive"],
            "two_thirds_consistent": tt["consistent_with_two_thirds"],
            "two_thirds_p_value": tt["p_value_vs_two_thirds"],
            "failure_rate_margin": tt["failure_rate"],
            "tighter_geometry_lowers_restore": gt["tighter_cutoff_lowers_H22_positive"],
            "sign_test_candidate_opposing_rate": cs["frac_opposing_h22_when_vf_positive"],
            "sign_test_vf_matched_opposing_median": sg["control_opposing_median"],
            "sign_test_candidate_lower_opposing": sg["candidate_lower_opposing_than_vf_matched"],
        },
    }
    json_path.write_text(json.dumps(output, indent=2), encoding="utf-8")
    print(f"\nResults -> {json_path}")

    # Mirror to Silo Gas capture
    silo = Path(__file__).resolve().parents[2] / (
        "Silo/8_Brain_Gas_Phase/Chat_Logs/Grok/jhtdb_ablation_results_2026-06-16.json"
    )
    if silo.parent.exists():
        silo.write_text(json.dumps(output, indent=2), encoding="utf-8")
        print(f"Mirror   -> {silo}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
