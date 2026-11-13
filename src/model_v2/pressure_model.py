"""Pressure Index reconstruction (V1 benchmark), continuous pressure weights, and Kish N_eff."""

from __future__ import annotations

import numpy as np
import pandas as pd


def compute_v1_pressure_index(
    df: pd.DataFrame, high_thresh: float = 0.50, low_thresh: float = 0.35
) -> pd.DataFrame:
    """
    Reconstruct V1 Pressure Index PI_t in [0, 1] and discrete situational regime tags
    for exact V1 benchmarking.
    """
    out = df.copy()

    # Drop pre-existing par_rpo / exp_wickets if re-running on an enriched df
    for col in ("par_rpo", "exp_wickets"):
        if col in out.columns:
            out = out.drop(columns=[col])

    comp_par = (
        out.groupby(["comp_category", "season_year"])
        .agg(tot_r=("total_runs", "sum"), tot_b=("is_legal_ball", "sum"))
        .assign(
            par_rpo=lambda x: np.where(
                x["tot_b"] > 0, 6.0 * x["tot_r"] / x["tot_b"], 7.5
            )
        )
        .reset_index()[["comp_category", "season_year", "par_rpo"]]
    )
    out = out.merge(comp_par, on=["comp_category", "season_year"], how="left")

    inn1 = out[out["innings"] == 1]
    if len(inn1) > 0:
        exp_wkts = (
            inn1.groupby(["comp_category", "overid"])["pre_wickets"]
            .mean()
            .rename("exp_wickets")
            .reset_index()
        )
        out = out.merge(exp_wkts, on=["comp_category", "overid"], how="left")
    else:
        out["exp_wickets"] = 0.0
    out["exp_wickets"] = out["exp_wickets"].fillna(0.0)

    # First-Innings Pressure Components
    wicket_excess = np.maximum(0.0, out["pre_wickets"] - out["exp_wickets"])
    s_collapse = np.clip(wicket_excess / 2.2, 0.0, 1.0)
    early_collapse_boost = np.where(
        (out["overid"] <= 6) & (out["pre_wickets"] >= 2), 0.25, 0.0
    )
    s_collapse = np.clip(s_collapse + early_collapse_boost, 0.0, 1.0)

    crr_deficit = np.where(
        out["pre_legal_balls"] >= 18,
        np.clip((out["par_rpo"] - out["pre_crr"]) / 3.0, 0.0, 1.0),
        0.0,
    )
    death_1st = np.where(
        out["overid"] >= 16,
        np.where(out["pre_wickets"] <= 6, 0.75, 0.45),
        np.where(out["overid"] >= 12, 0.25, 0.0),
    )
    pi_1 = np.clip(
        0.50 * s_collapse + 0.30 * crr_deficit + 0.20 * death_1st, 0.0, 1.0
    )

    # Second-Innings Pressure Components
    pre_rrr_safe = out["pre_rrr"].fillna(0.0)
    runs_needed_safe = out["runs_needed"].fillna(0.0)
    rrr_ratio = np.where(
        out["innings"] == 2,
        pre_rrr_safe / np.maximum(6.0, out["par_rpo"]),
        0.0,
    )
    s_rrr = np.clip((rrr_ratio - 0.65) / 0.80, 0.0, 1.0)

    won_damp = np.where(
        (rrr_ratio < 0.55) & (out["pre_wickets_in_hand"] >= 5), 0.35, 1.0
    )
    lost_damp = np.where(
        (rrr_ratio > 2.20) & (out["pre_balls_remaining"] > 18), 0.40, 1.0
    )
    close_finish_boost = np.where(
        (out["innings"] == 2)
        & (out["pre_balls_remaining"] <= 24)
        & (runs_needed_safe > 0)
        & (runs_needed_safe <= 48)
        & (rrr_ratio >= 0.75)
        & (rrr_ratio <= 2.20),
        0.20,
        0.0,
    )

    s_wkts_2 = np.where(
        runs_needed_safe > 10,
        np.clip((out["pre_wickets"] - 1.0) / 5.5, 0.0, 1.0),
        0.0,
    )
    s_urgency_2 = np.clip(
        (out["inn_max_balls"] - out["pre_balls_remaining"])
        / np.maximum(60.0, out["inn_max_balls"]),
        0.0,
        1.0,
    )

    pi_2_raw = 0.50 * s_rrr + 0.30 * s_wkts_2 + 0.20 * s_urgency_2 + close_finish_boost
    pi_2 = np.clip(pi_2_raw * won_damp * lost_damp, 0.0, 1.0)

    out["pressure_index"] = np.where(out["innings"] == 1, pi_1, pi_2)

    out["is_early_collapse"] = (
        ((out["overid"] <= 6) & (out["pre_wickets"] >= 2))
        | ((out["overid"] <= 10) & (out["pre_wickets"] >= 4))
    )
    out["is_tight_chase"] = (
        (out["innings"] == 2)
        & (out["pre_balls_remaining"] <= 36)
        & (pre_rrr_safe >= 8.5)
        & (pre_rrr_safe <= 16.5)
        & (out["pre_wickets_in_hand"] >= 2)
    )
    out["is_high_pressure"] = out["pressure_index"] >= high_thresh
    out["is_low_pressure"] = out["pressure_index"] < low_thresh

    return out


def compute_pressure_weights(
    pi: pd.Series | np.ndarray,
    mode: str = "sigmoid",
    center: float = 0.425,
    scale: float = 0.08,
) -> np.ndarray:
    """
    Map Pressure Index PI_t in [0, 1] to continuous pressure weight w_t in [0, 1]
    across ALL deliveries without discarding the 0.35 <= PI < 0.50 band.

    Modes:
    - 'sigmoid': smooth logistic centered at midpoint 0.425 of V1 thresholds (default).
    - 'linear': w_t = clip(PI_t, 0, 1).
    """
    pi_arr = np.asarray(pi, dtype=float)
    if mode == "sigmoid":
        if scale <= 0:
            raise ValueError("scale must be positive for sigmoid pressure weights.")
        z = np.clip((pi_arr - center) / scale, -60.0, 60.0)
        w = 1.0 / (1.0 + np.exp(-z))
        return np.clip(w, 0.0, 1.0)
    if mode == "linear":
        return np.clip(pi_arr, 0.0, 1.0)
    raise ValueError(f"Unsupported pressure weight mode: {mode!r}")


def kish_effective_sample_size(weights: pd.Series | np.ndarray) -> float:
    """
    Compute Kish's effective sample size:
        N_eff = (sum w_t)^2 / sum(w_t^2).
    Returns 0.0 when weights are empty or all zero.
    """
    w = np.asarray(weights, dtype=float)
    w = w[np.isfinite(w) & (w >= 0.0)]
    if w.size == 0:
        return 0.0
    sum_w = float(np.sum(w))
    sum_w2 = float(np.sum(w * w))
    if sum_w2 <= 0.0:
        return 0.0
    return (sum_w * sum_w) / sum_w2


def grouped_kish_neff(
    df: pd.DataFrame, group_col: str, weight_col: str = "pressure_weight"
) -> pd.Series:
    """Vectorized Kish N_eff per group."""
    tmp = pd.DataFrame(
        {
            group_col: df[group_col].values,
            "_w": df[weight_col].astype(float).values,
            "_w2": np.square(df[weight_col].astype(float).values),
        }
    )
    agg = tmp.groupby(group_col)[["_w", "_w2"]].sum()
    return pd.Series(
        np.where(agg["_w2"] > 0.0, np.square(agg["_w"]) / agg["_w2"], 0.0),
        index=agg.index,
        name="kish_neff",
    )


def compute_pressure_features(
    df: pd.DataFrame,
    high_thresh: float = 0.50,
    low_thresh: float = 0.35,
    weight_mode: str = "sigmoid",
    center: float = 0.425,
    scale: float = 0.08,
) -> pd.DataFrame:
    """
    Compute both V1 discrete pressure tags (for benchmarking) and V2 continuous
    pressure weights (w_t in [0, 1]) over ALL deliveries.
    """
    out = compute_v1_pressure_index(
        df, high_thresh=high_thresh, low_thresh=low_thresh
    )
    out["pressure_weight"] = compute_pressure_weights(
        out["pressure_index"], mode=weight_mode, center=center, scale=scale
    )
    out["normal_weight"] = 1.0 - out["pressure_weight"]
    out["is_intermediate_pressure"] = (
        (out["pressure_index"] >= low_thresh) & (out["pressure_index"] < high_thresh)
    )
    return out
