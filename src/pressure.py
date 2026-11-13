"""Pressure Index (PI_t) and discrete situational regime construction."""

import numpy as np
import pandas as pd


def compute_pressure_index(
    df: pd.DataFrame, high_thresh: float = 0.50, low_thresh: float = 0.35
) -> pd.DataFrame:
    """
    Compute zero-look-ahead Pressure Index PI_t in [0, 1] for both innings,
    plus discrete situational regime tags for interpretability.
    """
    out = df.copy()

    # 1. Competition-season par run rate (RPO) and expected wickets by ball bucket
    comp_par = (
        out.groupby(["comp_category", "season_year"])
        .agg(tot_r=("total_runs", "sum"), tot_b=("is_legal_ball", "sum"))
        .assign(par_rpo=lambda x: 6.0 * x["tot_r"] / x["tot_b"])
        .reset_index()[["comp_category", "season_year", "par_rpo"]]
    )
    out = out.merge(comp_par, on=["comp_category", "season_year"], how="left")

    # Empirical expected wickets fallen at each overid in 1st innings
    exp_wkts = (
        out[out["innings"] == 1]
        .groupby(["comp_category", "overid"])["pre_wickets"]
        .mean()
        .rename("exp_wickets")
        .reset_index()
    )
    out = out.merge(exp_wkts, on=["comp_category", "overid"], how="left")
    out["exp_wickets"] = out["exp_wickets"].fillna(0.0)

    # 2. First-Innings Pressure Components
    wicket_excess = np.maximum(0.0, out["pre_wickets"] - out["exp_wickets"])
    s_collapse = np.clip(wicket_excess / 2.2, 0.0, 1.0)
    # Also reward raw early collapse regardless of average
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
    pi_1 = np.clip(0.50 * s_collapse + 0.30 * crr_deficit + 0.20 * death_1st, 0.0, 1.0)

    # 3. Second-Innings Pressure Components
    rrr_ratio = np.where(
        out["innings"] == 2,
        out["pre_rrr"] / np.maximum(6.0, out["par_rpo"]),
        0.0,
    )
    # S_rrr rises from rrr_ratio = 0.65 (easy) to 1.45 (tough)
    s_rrr = np.clip((rrr_ratio - 0.65) / 0.80, 0.0, 1.0)

    # Dead-chase / garbage-time damping:
    # (a) Practically won: rrr_ratio < 0.55 and >= 5 wickets in hand
    won_damp = np.where(
        (rrr_ratio < 0.55) & (out["pre_wickets_in_hand"] >= 5), 0.35, 1.0
    )
    # (b) Practically lost: rrr_ratio > 2.2 and > 18 balls left
    lost_damp = np.where(
        (rrr_ratio > 2.20) & (out["pre_balls_remaining"] > 18), 0.40, 1.0
    )
    # (c) Very close finish (< 18 balls left, runs_needed <= 36 and > 0) keeps high tension
    close_finish_boost = np.where(
        (out["innings"] == 2)
        & (out["pre_balls_remaining"] <= 24)
        & (out["runs_needed"] > 0)
        & (out["runs_needed"] <= 48)
        & (rrr_ratio >= 0.75)
        & (rrr_ratio <= 2.20),
        0.20,
        0.0,
    )

    s_wkts_2 = np.where(
        out["runs_needed"] > 10,
        np.clip((out["pre_wickets"] - 1.0) / 5.5, 0.0, 1.0),
        0.0,
    )
    s_urgency_2 = np.clip(
        (out["inn_max_balls"] - out["pre_balls_remaining"]) / np.maximum(60.0, out["inn_max_balls"]),
        0.0,
        1.0,
    )

    pi_2_raw = 0.50 * s_rrr + 0.30 * s_wkts_2 + 0.20 * s_urgency_2 + close_finish_boost
    pi_2 = np.clip(pi_2_raw * won_damp * lost_damp, 0.0, 1.0)

    out["pressure_index"] = np.where(out["innings"] == 1, pi_1, pi_2)

    # Discrete regime tags for interpretability
    out["is_early_collapse"] = (
        ((out["overid"] <= 6) & (out["pre_wickets"] >= 2))
        | ((out["overid"] <= 10) & (out["pre_wickets"] >= 4))
    )
    out["is_tight_chase"] = (
        (out["innings"] == 2)
        & (out["pre_balls_remaining"] <= 36)
        & (out["pre_rrr"] >= 8.5)
        & (out["pre_rrr"] <= 16.5)
        & (out["pre_wickets_in_hand"] >= 2)
    )
    out["is_high_pressure"] = out["pressure_index"] >= high_thresh
    out["is_low_pressure"] = out["pressure_index"] < low_thresh

    return out
