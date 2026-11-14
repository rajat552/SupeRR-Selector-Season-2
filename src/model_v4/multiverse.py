"""Comprehensive Multiverse (Specification-Curve) Analysis Engine for Model V4.

Implements the pre-registered 8-dimensional specification grid:
- Dimension P: Pressure definition (P1, P2, P3, P4, P5; and P0 reference for bowlers)
- Dimension W: Wickets-fallen in context baseline (W0: no, W1: yes)
- Dimension F: Competition/format scope (F1: IPL+all T20I, F2: IPL+full member T20I, F3: IPL only)
- Dimension M: Scoring model (Model A, Model B, Model C)
- Dimension V: Wicket valuation (4.0, 6.0, 8.0, context-marginal)
- Dimension K: Empirical Bayes shrinkage strength (60, 120, 180)
- Dimension G: Eligibility gate (lenient, standard, strict; scaled for P5)
- Dimension S: Composite metric weights (Base + 6 one-at-a-time perturbations)
"""

from __future__ import annotations

import itertools
import json
import time
from pathlib import Path
from typing import Dict, List, Optional, Sequence, Tuple
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy import stats
from sklearn.linear_model import Ridge, LogisticRegression

from .data_loader import load_clean_dataset, FULL_MEMBER_TEAMS
from .state_builder import build_match_state
from .opponent_strength import attach_opponent_elo
from .pressure_model import (
    compute_pressure_weights,
    compute_v1_pressure_index,
    compute_bowler_pressure_index,
    grouped_kish_neff,
)
from .batting_features import add_batting_features, summarize_batter_roles
from .bowling_features import add_bowling_features, summarize_bowler_styles
from .context_baselines import (
    BAT_HIERARCHY,
    BAT_HIERARCHY_V2,
    BOWL_HIERARCHY,
    assign_wickets_bucket,
    add_lpo_context_baselines,
)
from .shrinkage import (
    attach_wicket_values,
    estimate_context_wicket_value_table,
    eb_shrink_rate,
    fit_empirical_beta_prior,
    beta_binomial_consistency,
)
from .eligibility import EligibilityGate, apply_eligibility_gate
from .impact_models import zscore, fit_model_c_and_score
from .bootstrap import run_stratified_bootstrap

ROOT_DIR = Path(__file__).resolve().parents[2]
OUT_DIR = ROOT_DIR / "outputs" / "model_v4"
CHART_DIR = OUT_DIR / "charts"

# Dimension S: Composite weight vectors (renormalized)
WEIGHT_VECTORS: Dict[str, Tuple[float, float, float]] = {
    "S0_base": (0.50, 0.30, 0.20),
    "S1_plus_w1": (0.60 / 1.10, 0.30 / 1.10, 0.20 / 1.10),
    "S2_minus_w1": (0.40 / 0.90, 0.30 / 0.90, 0.20 / 0.90),
    "S3_plus_w2": (0.50 / 1.10, 0.40 / 1.10, 0.20 / 1.10),
    "S4_minus_w2": (0.50 / 0.90, 0.20 / 0.90, 0.20 / 0.90),
    "S5_plus_w3": (0.50 / 1.10, 0.30 / 1.10, 0.30 / 1.10),
    "S6_minus_w3": (0.50 / 0.90, 0.30 / 0.90, 0.10 / 0.90),
}

# Dimension G: Eligibility gates
GATES: Dict[str, Dict[str, int]] = {
    "lenient": {"min_balls": 200, "min_hp_balls": 80, "min_hp_matches": 8},
    "standard": {"min_balls": 300, "min_hp_balls": 120, "min_hp_matches": 10},
    "strict": {"min_balls": 400, "min_hp_balls": 150, "min_hp_matches": 12},
}

# P5 scaled gates (ratio ~0.47 for bat, ~0.55 for bowl)
GATES_P5_BAT: Dict[str, Dict[str, int]] = {
    "lenient": {"min_balls": 200, "min_hp_balls": 38, "min_hp_matches": 4},
    "standard": {"min_balls": 300, "min_hp_balls": 56, "min_hp_matches": 5},
    "strict": {"min_balls": 400, "min_hp_balls": 70, "min_hp_matches": 6},
}

GATES_P5_BOWL: Dict[str, Dict[str, int]] = {
    "lenient": {"min_balls": 200, "min_hp_balls": 44, "min_hp_matches": 4},
    "standard": {"min_balls": 300, "min_hp_balls": 66, "min_hp_matches": 5},
    "strict": {"min_balls": 400, "min_hp_balls": 82, "min_hp_matches": 7},
}


def build_raw_foundation() -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """Load and construct primary base dataset with match state, ELO, and features."""
    bbb, matches, pe, player_lookup = load_clean_dataset()
    df = build_match_state(bbb)
    df, _ = attach_opponent_elo(df, matches=matches)
    df = add_batting_features(df, pe)
    df = add_bowling_features(df)
    if "wickets_bucket" not in df.columns:
        df["wickets_bucket"] = assign_wickets_bucket(df["pre_wickets"])
    return df, matches, pe, player_lookup


def attach_pressure_variants(df: pd.DataFrame) -> pd.DataFrame:
    """Attach all 5 batting pressure definitions and 6 bowler pressure definitions."""
    work = df.copy()

    # Base continuous indices
    if "pressure_index_bat" not in work.columns:
        work = compute_v1_pressure_index(work)
    if "pressure_index_bowl" not in work.columns:
        work = compute_bowler_pressure_index(work)

    # Batting pressure definitions
    work["pw_bat_P1"] = compute_pressure_weights(work["pressure_index_bat"], mode="sigmoid", center=0.40, scale=0.08)
    work["nw_bat_P1"] = 1.0 - work["pw_bat_P1"]

    work["pw_bat_P2"] = compute_pressure_weights(work["pressure_index_bat"], mode="sigmoid", center=0.425, scale=0.08)
    work["nw_bat_P2"] = 1.0 - work["pw_bat_P2"]

    work["pw_bat_P3"] = compute_pressure_weights(work["pressure_index_bat"], mode="sigmoid", center=0.45, scale=0.08)
    work["nw_bat_P3"] = 1.0 - work["pw_bat_P3"]

    # Batting P4: discrete threshold (PI >= 0.50 vs < 0.35)
    work["pw_bat_P4"] = np.where(work["pressure_index_bat"] >= 0.50, 1.0, 0.0)
    work["nw_bat_P4"] = np.where(work["pressure_index_bat"] < 0.35, 1.0, 0.0)

    # Batting P5: Definition C
    bat_hp_inn2 = (
        (work["innings"] == 2)
        & (work["pre_balls_remaining"] <= 48)
        & (work["pre_rrr"] >= 7.0)
        & (work["pre_rrr"] <= 15.0)
        & (work["pre_wickets"] <= 7)
    )
    bat_hp_inn1 = (
        (work["innings"] == 1)
        & (
            ((work["overid"] <= 8) & (work["pre_wickets"] >= 3))
            | ((work["overid"] <= 14) & (work["pre_wickets"] >= 5))
        )
    )
    work["pw_bat_P5"] = (bat_hp_inn2 | bat_hp_inn1).astype(float)
    work["nw_bat_P5"] = 1.0 - work["pw_bat_P5"]

    # Bowler pressure definitions
    work["pw_bowl_P1"] = compute_pressure_weights(work["pressure_index_bowl"], mode="sigmoid", center=0.40, scale=0.08)
    work["nw_bowl_P1"] = 1.0 - work["pw_bowl_P1"]

    work["pw_bowl_P2"] = compute_pressure_weights(work["pressure_index_bowl"], mode="sigmoid", center=0.425, scale=0.08)
    work["nw_bowl_P2"] = 1.0 - work["pw_bowl_P2"]

    work["pw_bowl_P3"] = compute_pressure_weights(work["pressure_index_bowl"], mode="sigmoid", center=0.45, scale=0.08)
    work["nw_bowl_P3"] = 1.0 - work["pw_bowl_P3"]

    # Bowler P4: defending discrete threshold
    work["pw_bowl_P4"] = np.where(work["pressure_index_bowl"] >= 0.50, 1.0, 0.0)
    work["nw_bowl_P4"] = np.where(work["pressure_index_bowl"] < 0.35, 1.0, 0.0)

    # Bowler P5: Definition C
    bowl_hp_inn2 = (
        (work["innings"] == 2)
        & (work["pre_balls_remaining"] <= 48)
        & (work["pre_rrr"] >= 6.0)
        & (work["pre_rrr"] <= 12.0)
        & (work["pre_wickets"] <= 6)
    )
    bowl_hp_inn1 = (
        (work["innings"] == 1)
        & (work["overid"] >= 16)
        & (work["pre_wickets"] <= 4)
    )
    work["pw_bowl_P5"] = (bowl_hp_inn2 | bowl_hp_inn1).astype(float)
    work["nw_bowl_P5"] = 1.0 - work["pw_bowl_P5"]

    # Bowler P0: Legacy V2 single-index (reference only)
    work["pw_bowl_P0"] = compute_pressure_weights(work["pressure_index_bat"], mode="sigmoid", center=0.425, scale=0.08)
    work["nw_bowl_P0"] = 1.0 - work["pw_bowl_P0"]

    return work


def precompute_cache(
    df: pd.DataFrame,
    matches: pd.DataFrame,
    f_scope: str,
    w_def: str,
) -> pd.DataFrame:
    """Precompute format-filtered and context-baseline-attached delivery dataframe."""
    # Filter format
    if f_scope == "F1_all":
        sub_matches = matches
    elif f_scope == "F2_full_member":
        f2_mask = (matches["comp_category"] == "IPL") | (
            (matches["comp_category"] == "T20I")
            & matches["home_team"].isin(FULL_MEMBER_TEAMS)
            & matches["away_team"].isin(FULL_MEMBER_TEAMS)
        )
        sub_matches = matches[f2_mask]
    elif f_scope == "F3_ipl_only":
        sub_matches = matches[matches["comp_category"] == "IPL"]
    else:
        raise ValueError(f"Unknown format scope: {f_scope}")

    m_ids = set(sub_matches["match_id"].unique())
    work = df[df["match_id"].isin(m_ids)].copy()

    # Assign context hierarchy
    if w_def == "W1_wickets":
        bat_hier = BAT_HIERARCHY
        bowl_hier = BOWL_HIERARCHY
    else:
        bat_hier = BAT_HIERARCHY_V2
        bowl_hier = [
            [c for c in lvl if c != "wickets_bucket"]
            for lvl in BOWL_HIERARCHY
        ]
        # Deduplicate levels
        dedup_bowl = []
        for lvl in bowl_hier:
            if lvl not in dedup_bowl:
                dedup_bowl.append(lvl)
        bowl_hier = dedup_bowl

    work = add_lpo_context_baselines(work, bat_hierarchy=bat_hier, bowl_hierarchy=bowl_hier)
    work, _ = attach_wicket_values(work, wicket_mode="context")
    work["wkt_val_ctx"] = work["wicket_value"]
    return work


def aggregate_player_stats(
    work_df: pd.DataFrame,
    role: str,
    p_def: str,
) -> pd.DataFrame:
    """Pre-aggregate delivery data to player-level summary statistics."""
    id_col = "striker_id" if role == "batter" else "bowler_id"
    name_col = "striker_name" if role == "batter" else "bowler_name"
    p_role = "bat" if role == "batter" else "bowl"

    pw_col = f"pw_{p_role}_{p_def}"
    nw_col = f"nw_{p_role}_{p_def}"

    if role == "batter":
        sub = work_df[work_df["is_batter_ball_faced"]].copy()
        sub["_unit"] = 1.0
        sub["_runs"] = sub["runs"].astype(float)
        sub["_evt"] = sub["is_striker_dismissed"].astype(float)
        sub["_rae"] = sub["_runs"] - sub["ctx_bat_rpb"].astype(float)
        sub["_wkt_diff"] = sub["ctx_bat_out_prob"].astype(float) - sub["_evt"]
    else:
        sub = work_df[work_df["is_legal_ball"]].copy()
        sub["_unit"] = 1.0
        sub["_runs"] = sub["bowler_runs_conceded"].astype(float)
        sub["_evt"] = sub["is_bowler_wicket"].astype(float)
        sub["_rae"] = sub["ctx_bowl_rpb"].astype(float) - sub["_runs"]
        sub["_wkt_diff"] = sub["_evt"] - sub["ctx_bowl_wkt_prob"].astype(float)

    pw = sub[pw_col].to_numpy(dtype=float)
    nw = sub[nw_col].to_numpy(dtype=float)
    unit = sub["_unit"].to_numpy(dtype=float)
    runs = sub["_runs"].to_numpy(dtype=float)
    evt = sub["_evt"].to_numpy(dtype=float)
    rae = sub["_rae"].to_numpy(dtype=float)
    wkt_diff = sub["_wkt_diff"].to_numpy(dtype=float)
    wkt_ctx = sub["wkt_val_ctx"].to_numpy(dtype=float) * wkt_diff

    # Discrete HP balls (PI >= 0.50 or Def C)
    is_hp = (pw >= 0.50).astype(float)

    tmp = pd.DataFrame({
        id_col: sub[id_col].to_numpy(),
        "player_name": sub[name_col].to_numpy(),
        "tot_balls": unit,
        "tot_runs": runs,
        "tot_evt": evt,
        "tot_rae": rae,
        "tot_wkt_diff": wkt_diff,
        "tot_wkt_ctx": wkt_ctx,

        "hp_balls": is_hp,
        "pw_balls": pw,
        "pw_sq": pw ** 2,
        "pw_runs": pw * runs,
        "pw_evt": pw * evt,
        "pw_rae": pw * rae,
        "pw_wkt_diff": pw * wkt_diff,
        "pw_wkt_ctx": pw * wkt_ctx,

        "nw_balls": nw,
        "nw_sq": nw ** 2,
        "nw_runs": nw * runs,
        "nw_evt": nw * evt,
        "nw_rae": nw * rae,
        "nw_wkt_diff": nw * wkt_diff,
        "nw_wkt_ctx": nw * wkt_ctx,
    })

    agg = tmp.groupby([id_col, "player_name"], as_index=False).sum()

    # Kish Neff
    agg["pw_neff"] = np.where(agg["pw_sq"] > 0, (agg["pw_balls"] ** 2) / agg["pw_sq"], 0.0)
    agg["nw_neff"] = np.where(agg["nw_sq"] > 0, (agg["nw_balls"] ** 2) / agg["nw_sq"], 0.0)

    # Cross-match qualifying counts
    sub["_pw_unit"] = pw * unit
    sub["_pw_imp_approx"] = pw * (rae + 6.0 * wkt_diff)
    sub["_hp_unit"] = is_hp * unit

    m_grp = sub.groupby([id_col, "match_id"], as_index=False).agg(
        m_hp_balls=("_hp_unit", "sum"),
        m_pw_balls=("_pw_unit", "sum"),
        m_pw_imp=("_pw_imp_approx", "sum"),
    )
    # Qual matches with HP
    hp_matches = m_grp[m_grp["m_hp_balls"] >= 6.0].groupby(id_col).agg(
        hp_matches=("m_hp_balls", "count"),
        hp_pos_matches=("m_pw_imp", lambda s: int(np.sum(s > 1e-12))),
    ).reset_index()

    agg = agg.merge(hp_matches, on=id_col, how="left")
    agg["hp_matches"] = agg["hp_matches"].fillna(0).astype(int)
    agg["hp_pos_matches"] = agg["hp_pos_matches"].fillna(0).astype(int)

    return agg


def score_player_stats(
    agg_df: pd.DataFrame,
    role: str,
    p_def: str,
    v_val: float | str,
    k_shrink: float,
    g_gate: str,
) -> pd.DataFrame:
    """Compute shrunk impacts and eligibility for given (V, K, G) configuration."""
    scale = 100.0 if role == "batter" else 24.0
    out = agg_df.copy()

    # Eligibility gate
    if p_def == "P5":
        gate_dict = GATES_P5_BAT[g_gate] if role == "batter" else GATES_P5_BOWL[g_gate]
    else:
        gate_dict = GATES[g_gate]

    out["is_eligible"] = (
        (out["tot_balls"] >= gate_dict["min_balls"])
        & (out["hp_balls"] >= gate_dict["min_hp_balls"])
        & (out["hp_matches"] >= gate_dict["min_hp_matches"])
    )

    # Compute raw impact per ball
    if v_val == "context":
        pw_imp_raw = out["pw_rae"] + out["pw_wkt_ctx"]
        nw_imp_raw = out["nw_rae"] + out["nw_wkt_ctx"]
        hp_imp_raw = (out["pw_rae"] + out["pw_wkt_ctx"])  # under discrete, same
    else:
        v_num = float(v_val)
        pw_imp_raw = out["pw_rae"] + v_num * out["pw_wkt_diff"]
        nw_imp_raw = out["nw_rae"] + v_num * out["nw_wkt_diff"]
        hp_imp_raw = out["pw_rae"] + v_num * out["pw_wkt_diff"]

    pw_rate = np.where(out["pw_balls"] > 0, scale * pw_imp_raw / out["pw_balls"], 0.0)
    nw_rate = np.where(out["nw_balls"] > 0, scale * nw_imp_raw / out["nw_balls"], 0.0)
    hp_rate = np.where(out["hp_balls"] > 0, scale * hp_imp_raw / np.maximum(1.0, out["hp_balls"]), 0.0)

    # Shrunk impacts
    out["shrunk_wp_impact"] = eb_shrink_rate(pw_rate, out["pw_neff"], k=k_shrink, prior_mean=0.0)
    out["shrunk_norm_impact"] = eb_shrink_rate(nw_rate, out["nw_neff"], k=k_shrink, prior_mean=0.0)
    out["shrunk_hp_impact"] = eb_shrink_rate(hp_rate, out["hp_balls"], k=k_shrink, prior_mean=0.0)

    # Lift
    lp_floor = -5.0 if role == "batter" else -3.0
    out["norm_floored"] = np.maximum(out["shrunk_norm_impact"], lp_floor)
    out["maint_lift"] = out["shrunk_wp_impact"] - 0.35 * out["norm_floored"]
    out["raw_lift"] = out["shrunk_wp_impact"] - out["shrunk_norm_impact"]

    # Beta-binomial consistency on eligible pool
    elig_sub = out[out["is_eligible"] & (out["hp_matches"] >= 3)]
    if len(elig_sub) >= 10:
        a0, b0 = fit_empirical_beta_prior(elig_sub["hp_pos_matches"], elig_sub["hp_matches"])
    else:
        a0, b0 = 1.0, 1.0
    out["eb_consistency"] = beta_binomial_consistency(
        out["hp_pos_matches"], out["hp_matches"], alpha_0=a0, beta_0=b0
    )

    return out


def evaluate_multiverse(
    df: pd.DataFrame,
    matches: pd.DataFrame,
    player_lookup: pd.DataFrame,
) -> pd.DataFrame:
    """Execute the complete specification grid across both roles."""
    p_defs_bat = ["P1", "P2", "P3", "P4", "P5"]
    p_defs_bowl = ["P1", "P2", "P3", "P4", "P5", "P0"]
    w_defs = ["W0_no_wickets", "W1_wickets"]
    f_scopes = ["F1_all", "F2_full_member", "F3_ipl_only"]
    v_vals = [4.0, 6.0, 8.0, "context"]
    k_shrinks = [60.0, 120.0, 180.0]
    g_gates = ["lenient", "standard", "strict"]
    m_models = ["Model_A", "Model_B"]

    all_ranks_records: List[Dict[str, object]] = []

    # 1. Attach pressure variants to primary dataframe once
    df_with_p = attach_pressure_variants(df)

    # 2. Iterate caches across (F, W)
    for f_scope in f_scopes:
        for w_def in w_defs:
            print(f"Building cache for {f_scope} | {w_def}...")
            cache_df = precompute_cache(df_with_p, matches, f_scope, w_def)

            for role in ["batter", "bowler"]:
                id_col = "striker_id" if role == "batter" else "bowler_id"
                p_role = "bat" if role == "batter" else "bowl"
                p_defs = p_defs_bat if role == "batter" else p_defs_bowl

                for p_def in p_defs:
                    agg_player = aggregate_player_stats(cache_df, role, p_def)

                    # Vectorized loop over (V, K, G)
                    for v_val in v_vals:
                        v_str = f"V_{v_val}" if isinstance(v_val, (int, float)) else "V_ctx"
                        for k_shrink in k_shrinks:
                            k_str = f"K_{int(k_shrink)}"
                            for g_gate in g_gates:
                                scored = score_player_stats(agg_player, role, p_def, v_val, k_shrink, g_gate)
                                elig = scored[scored["is_eligible"]].copy()
                                if len(elig) == 0:
                                    continue

                                # Z-scores
                                z_abs = zscore(elig["shrunk_wp_impact"]).to_numpy()
                                z_hp = zscore(elig["shrunk_hp_impact"]).to_numpy()
                                z_lift = zscore(elig["maint_lift"]).to_numpy()
                                z_cons = zscore(elig["eb_consistency"]).to_numpy()

                                for m_model in m_models:
                                    for s_name, (w1, w2, w3) in WEIGHT_VECTORS.items():
                                        spec_id = f"{role}_{p_def}_{w_def}_{f_scope}_{m_model}_{v_str}_{k_str}_{g_gate}_{s_name}"

                                        if m_model == "Model_A":
                                            spec_score = w1 * z_abs + w2 * z_hp + w3 * z_cons
                                        else:  # Model_B
                                            spec_score = w1 * z_abs + w2 * z_lift + w3 * z_cons

                                        # Ranks (1 = highest score)
                                        order = np.argsort(-spec_score)
                                        ranks = np.empty_like(order)
                                        ranks[order] = np.arange(1, len(order) + 1)

                                        p_ids = elig[id_col].to_numpy()
                                        p_names = elig["player_name"].to_numpy()
                                        wp_imps = elig["shrunk_wp_impact"].to_numpy()
                                        norm_imps = elig["shrunk_norm_impact"].to_numpy()
                                        raw_lifts = elig["raw_lift"].to_numpy()
                                        maint_lifts = elig["maint_lift"].to_numpy()
                                        hp_bs = elig["hp_balls"].to_numpy()

                                        is_valid = not (role == "bowler" and p_def == "P0")

                                        for i in range(len(elig)):
                                            all_ranks_records.append({
                                                "spec_id": spec_id,
                                                "role": role,
                                                "p_def": p_def,
                                                "w_def": w_def,
                                                "f_scope": f_scope,
                                                "m_model": m_model,
                                                "v_val": str(v_val),
                                                "k_shrink": k_shrink,
                                                "g_gate": g_gate,
                                                "s_weights": s_name,
                                                "player_id": int(p_ids[i]),
                                                "player_name": str(p_names[i]),
                                                "score": float(spec_score[i]),
                                                "rank": int(ranks[i]),
                                                "is_eligible": True,
                                                "is_valid": is_valid,
                                                "shrunk_wp_impact": float(wp_imps[i]),
                                                "shrunk_norm_impact": float(norm_imps[i]),
                                                "raw_lift": float(raw_lifts[i]),
                                                "maint_lift": float(maint_lifts[i]),
                                                "hp_balls": float(hp_bs[i]),
                                            })

                    # Run Model C for this (P, W, F) at canonical V=6, K=120, G=standard
                    m_c_spec_id = f"{role}_{p_def}_{w_def}_{f_scope}_Model_C_V_6.0_K_120_standard_S0_base"
                    c_scored = score_player_stats(agg_player, role, p_def, 6.0, 120.0, "standard")
                    c_elig = c_scored[c_scored["is_eligible"]].copy()
                    if len(c_elig) >= 5:
                        # Set current pressure weights for Model C
                        cache_df[f"pressure_weight_{p_role}"] = cache_df[f"pw_{p_role}_{p_def}"]
                        c_fit_df, _ = fit_model_c_and_score(cache_df, c_elig, role=role, wicket_weight=6.0)
                        c_scores = c_fit_df["model_c_score"].to_numpy()
                        c_order = np.argsort(-c_scores)
                        c_ranks = np.empty_like(c_order)
                        c_ranks[c_order] = np.arange(1, len(c_order) + 1)

                        c_ids = c_fit_df[id_col].to_numpy()
                        c_names = c_fit_df["player_name"].to_numpy()
                        c_wp = c_fit_df["shrunk_wp_impact"].to_numpy()
                        c_norm = c_fit_df["shrunk_norm_impact"].to_numpy()
                        c_rlift = c_fit_df["raw_lift"].to_numpy()
                        c_mlift = c_fit_df["maint_lift"].to_numpy()
                        c_hpb = c_fit_df["hp_balls"].to_numpy()

                        is_valid = not (role == "bowler" and p_def == "P0")
                        for i in range(len(c_fit_df)):
                            all_ranks_records.append({
                                "spec_id": m_c_spec_id,
                                "role": role,
                                "p_def": p_def,
                                "w_def": w_def,
                                "f_scope": f_scope,
                                "m_model": "Model_C",
                                "v_val": "6.0",
                                "k_shrink": 120.0,
                                "g_gate": "standard",
                                "s_weights": "S0_base",
                                "player_id": int(c_ids[i]),
                                "player_name": str(c_names[i]),
                                "score": float(c_scores[i]),
                                "rank": int(c_ranks[i]),
                                "is_eligible": True,
                                "is_valid": is_valid,
                                "shrunk_wp_impact": float(c_wp[i]),
                                "shrunk_norm_impact": float(c_norm[i]),
                                "raw_lift": float(c_rlift[i]),
                                "maint_lift": float(c_mlift[i]),
                                "hp_balls": float(c_hpb[i]),
                            })

    multiverse_ranks_df = pd.DataFrame.from_records(all_ranks_records)
    return multiverse_ranks_df


def analyze_multiverse_summary(
    multiverse_ranks_df: pd.DataFrame,
    role: str,
) -> pd.DataFrame:
    """Compute player summary statistics across all valid specifications."""
    sub = multiverse_ranks_df[(multiverse_ranks_df["role"] == role) & multiverse_ranks_df["is_valid"]].copy()
    total_valid_specs = sub["spec_id"].nunique()

    # Per player aggregation
    g = sub.groupby(["player_id", "player_name"])

    summary_records = []
    for (pid, pname), group in g:
        n_elig = len(group)
        elig_share = n_elig / total_valid_specs

        ranks = group["rank"].to_numpy()
        top10_hits = np.sum(ranks <= 10)
        top10_freq = top10_hits / total_valid_specs
        top10_retention = top10_hits / n_elig if n_elig > 0 else 0.0

        med_rank = float(np.median(ranks))
        q25 = float(np.percentile(ranks, 25))
        q75 = float(np.percentile(ranks, 75))
        iqr = q75 - q25
        best_rank = int(np.min(ranks))
        worst_rank = int(np.max(ranks))

        raw_lifts = group["raw_lift"].to_numpy()
        rises_share = float(np.mean(raw_lifts > 0.0))

        mean_shrunk_pwi = float(group["shrunk_wp_impact"].mean())
        mean_raw_lift = float(group["raw_lift"].mean())
        mean_maint_lift = float(group["maint_lift"].mean())
        mean_hp_balls = float(group["hp_balls"].mean())

        summary_records.append({
            "player_id": pid,
            "player_name": pname,
            "role": role,
            "elig_specs": n_elig,
            "total_specs": total_valid_specs,
            "elig_share": elig_share,
            "top10_hits": int(top10_hits),
            "top10_freq": top10_freq,
            "top10_retention": top10_retention,
            "median_rank": med_rank,
            "iqr_rank": iqr,
            "q25_rank": q25,
            "q75_rank": q75,
            "best_rank": best_rank,
            "worst_rank": worst_rank,
            "rises_under_pressure_share": rises_share,
            "mean_shrunk_pwi": mean_shrunk_pwi,
            "mean_raw_lift": mean_raw_lift,
            "mean_maint_lift": mean_maint_lift,
            "mean_hp_balls": mean_hp_balls,
        })

    summary_df = pd.DataFrame(summary_records)
    # Sort strictly by top10_freq desc, then lower median_rank asc
    summary_df = summary_df.sort_values(
        by=["top10_freq", "median_rank", "iqr_rank"],
        ascending=[False, True, True],
    ).reset_index(drop=True)
    return summary_df


def run_variance_decomposition(
    multiverse_ranks_df: pd.DataFrame,
    role: str,
) -> pd.DataFrame:
    """Run ANOVA variance decomposition on ranks across modeling dimensions."""
    sub = multiverse_ranks_df[(multiverse_ranks_df["role"] == role) & multiverse_ranks_df["is_valid"]].copy()

    # Restrict to players eligible across at least 80% of specs for balanced decomposition
    common_pids = sub["player_id"].value_counts()[lambda s: s >= 0.80 * sub["spec_id"].nunique()].index
    sub = sub[sub["player_id"].isin(common_pids)].copy()

    total_ss = np.sum((sub["rank"] - sub["rank"].mean()) ** 2)

    factors = ["p_def", "w_def", "f_scope", "m_model", "v_val", "k_shrink", "g_gate", "s_weights", "player_id"]
    decomp_records = []

    for f in factors:
        means = sub.groupby(f)["rank"].transform("mean")
        ss_f = np.sum((means - sub["rank"].mean()) ** 2)
        pct_var = 100.0 * ss_f / total_ss
        decomp_records.append({
            "role": role,
            "dimension": f,
            "sum_of_squares": ss_f,
            "pct_variance_explained": pct_var,
        })

    decomp_df = pd.DataFrame(decomp_records).sort_values("pct_variance_explained", ascending=False).reset_index(drop=True)
    return decomp_df


def plot_specification_curves(
    multiverse_ranks_df: pd.DataFrame,
    summary_df: pd.DataFrame,
    role: str,
    top_n: int = 15,
) -> None:
    """Generate specification curve charts for the top N players."""
    top_players = summary_df.head(top_n)

    fig, axes = plt.subplots(nrows=3, ncols=5, figsize=(20, 12), sharey=True)
    axes = axes.flatten()

    for idx, (_, p_row) in enumerate(top_players.iterrows()):
        pid = p_row["player_id"]
        pname = p_row["player_name"]
        t10_f = p_row["top10_freq"]
        med_r = p_row["median_rank"]

        p_specs = multiverse_ranks_df[
            (multiverse_ranks_df["player_id"] == pid)
            & (multiverse_ranks_df["role"] == role)
            & multiverse_ranks_df["is_valid"]
        ].sort_values("rank")

        ax = axes[idx]
        ax.plot(np.arange(len(p_specs)), p_specs["rank"].to_numpy(), color="#1f77b4", lw=1.5)
        ax.axhline(10.5, color="red", linestyle="--", alpha=0.7, label="Top 10 cutoff")
        ax.set_title(f"{pname}\nTop-10: {t10_f:.1%}, Med: {med_r:.0f}", fontsize=10)
        ax.set_ylim(0.5, 40.5)
        ax.invert_yaxis()
        ax.grid(True, alpha=0.3)
        if idx % 5 == 0:
            ax.set_ylabel("Rank in Specification")
        if idx >= 10:
            ax.set_xlabel("Sorted Specifications")

    plt.suptitle(f"Multiverse Specification Curves — Top {top_n} {role.capitalize()}s", fontsize=15, y=0.98)
    plt.tight_layout()
    plt.savefig(CHART_DIR / f"multiverse_spec_curves_{role}.png", dpi=300)
    plt.close()


def run_walk_forward_evaluation(
    df: pd.DataFrame,
    player_lookup: pd.DataFrame,
    summary_bat: pd.DataFrame,
    summary_bowl: pd.DataFrame,
) -> pd.DataFrame:
    """Evaluate temporal stability: 2022-2024 predicting 2025-2026."""
    df_with_p = attach_pressure_variants(df)
    if "wkt_val_ctx" not in df_with_p.columns:
        df_with_p, _ = attach_wicket_values(df_with_p, wicket_mode="context")
        df_with_p["wkt_val_ctx"] = df_with_p["wicket_value"]
    results = []

    for role in ["batter", "bowler"]:
        id_col = "striker_id" if role == "batter" else "bowler_id"
        sub_df = df_with_p[df_with_p["is_batter_ball_faced"] if role == "batter" else df_with_p["is_legal_ball"]].copy()

        train = sub_df[sub_df["season_year"].astype(int).isin([2022, 2023, 2024])]
        test = sub_df[sub_df["season_year"].astype(int).isin([2025, 2026])]

        # Pre-aggregate train and test
        agg_train = aggregate_player_stats(train, role, "P2")
        scored_train = score_player_stats(agg_train, role, "P2", 6.0, 120.0, "lenient")

        agg_test = aggregate_player_stats(test, role, "P2")
        scored_test = score_player_stats(agg_test, role, "P2", 6.0, 120.0, "lenient")

        # Merge on eligible in both
        common = scored_train[scored_train["is_eligible"]].merge(
            scored_test[scored_test["is_eligible"]],
            on=id_col,
            suffixes=("_train", "_test"),
        )

        corr_canon, p_canon = stats.spearmanr(common["shrunk_wp_impact_train"], common["shrunk_wp_impact_test"])

        # Consensus ranking correlation
        sum_df = summary_bat if role == "batter" else summary_bowl
        merged_sum = common.merge(sum_df[[id_col if id_col in sum_df.columns else "player_id", "top10_freq"]], left_on=id_col, right_on=id_col if id_col in sum_df.columns else "player_id")
        corr_cons, p_cons = stats.spearmanr(merged_sum["top10_freq"], merged_sum["shrunk_wp_impact_test"])

        results.append({
            "role": role,
            "n_common_players": len(common),
            "canonical_spearman_corr": corr_canon,
            "canonical_p_value": p_canon,
            "consensus_spearman_corr": corr_cons,
            "consensus_p_value": p_cons,
        })

    wf_df = pd.DataFrame(results)
    return wf_df
