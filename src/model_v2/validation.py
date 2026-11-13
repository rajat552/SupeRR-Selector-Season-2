"""Sensitivity and robustness suites (LOSO, format, pressure, wicket, eligibility, shrinkage k)."""

from __future__ import annotations

from typing import Dict, List, Sequence, Tuple
import numpy as np
import pandas as pd
from scipy.stats import spearmanr

from .context_baselines import DEFAULT_MIN_CELL_N, add_lpo_context_baselines
from .eligibility import (
    BENCHMARK_GATE,
    ELIGIBILITY_GATE_SWEEP,
    EligibilityGate,
    apply_eligibility_gate,
    identify_near_misses,
)
from .impact_models import compute_player_base_metrics, score_model_a, score_model_b
from .pressure_model import compute_pressure_features
from .shrinkage import (
    DEFAULT_SHRINK_K,
    SHRINK_K_GRID,
    estimate_context_wicket_value_table,
    evaluate_k_shrinkage_sensitivity,
)


def _compare_to_reference(
    ref_df: pd.DataFrame,
    cand_df: pd.DataFrame,
    id_col: str,
    score_col: str,
) -> Dict[str, object]:
    """Compute Spearman correlation and Top-10 overlap against reference ranking."""
    ref_top10 = list(ref_df.sort_values(score_col, ascending=False).head(10)[id_col])
    cand_sorted = cand_df.sort_values(score_col, ascending=False)
    cand_top10 = list(cand_sorted.head(10)[id_col])
    cand_top10_names = list(cand_sorted.head(10)["player_name"])

    merged = ref_df[[id_col, score_col]].merge(
        cand_df[[id_col, score_col]], on=id_col, suffixes=("_ref", "_cand")
    )
    if len(merged) >= 3:
        rho = float(spearmanr(merged[f"{score_col}_ref"], merged[f"{score_col}_cand"]).statistic)
    else:
        rho = float("nan")

    return {
        "n_eligible": int(len(cand_df)),
        "n_common_with_ref": int(len(merged)),
        "top10_overlap": int(len(set(ref_top10) & set(cand_top10))),
        "spearman_rho": rho,
        "top10_players": " | ".join(str(x) for x in cand_top10_names),
    }


def _score_canonical(
    df: pd.DataFrame,
    player_lookup: pd.DataFrame,
    role: str,
    model_name: str = "model_b",
    gate: EligibilityGate = BENCHMARK_GATE,
    shrink_k: float = DEFAULT_SHRINK_K,
    wicket_mode: str | float = 6.0,
) -> pd.DataFrame:
    base, _ = compute_player_base_metrics(
        df,
        player_lookup,
        role=role,
        wicket_mode=wicket_mode,
        shrink_k=shrink_k,
        gate=gate,
    )
    elig = base[base["is_eligible"]].copy()
    elig = score_model_a(elig)
    elig = score_model_b(elig, role=role)
    score_col = f"{model_name}_score"
    return elig.sort_values(score_col, ascending=False).reset_index(drop=True)


def run_loso_sensitivity(
    df: pd.DataFrame,
    player_lookup: pd.DataFrame,
    ref_bat: pd.DataFrame,
    ref_bowl: pd.DataFrame,
    model_name: str = "model_b",
    min_cell_n: int = DEFAULT_MIN_CELL_N,
) -> pd.DataFrame:
    """Leave-One-Season-Out (LOSO) stability across 2022..2026."""
    score_col = f"{model_name}_score"
    seasons = sorted(df["season_year"].unique().tolist())
    rows = []
    for yr in seasons:
        sub = df[df["season_year"] != yr].copy()
        sub = add_lpo_context_baselines(sub, min_cell_n=min_cell_n)
        for role, id_col, ref_df in [
            ("batter", "striker_id", ref_bat),
            ("bowler", "bowler_id", ref_bowl),
        ]:
            cand = _score_canonical(sub, player_lookup, role=role, model_name=model_name)
            stats = _compare_to_reference(ref_df, cand, id_col=id_col, score_col=score_col)
            rows.append(
                {
                    "role": role,
                    "dropped_season": int(yr),
                    "model_name": model_name,
                    **stats,
                }
            )
    return pd.DataFrame(rows)


def run_format_sensitivity(
    df: pd.DataFrame,
    player_lookup: pd.DataFrame,
    ref_bat: pd.DataFrame,
    ref_bowl: pd.DataFrame,
    model_name: str = "model_b",
    min_cell_n: int = DEFAULT_MIN_CELL_N,
) -> pd.DataFrame:
    """
    Evaluate format stability across:
    1) Primary (IPL + All T20I)
    2) IPL + Full-Member T20I only
    3) IPL-only (both benchmark 300/120/10 and format-adjusted 200/80/8)
    4) T20I-only (both benchmark 300/120/10 and format-adjusted 200/80/8)
    """
    score_col = f"{model_name}_score"
    specs = [
        ("Primary_IPL_plus_All_T20I", df, BENCHMARK_GATE),
        (
            "IPL_plus_FullMember_T20I",
            df[df["comp_tier"].isin(["IPL", "T20I_Full"])].copy(),
            BENCHMARK_GATE,
        ),
        (
            "IPL_only_benchmark_gate",
            df[df["comp_category"] == "IPL"].copy(),
            BENCHMARK_GATE,
        ),
        (
            "IPL_only_200_80_8",
            df[df["comp_category"] == "IPL"].copy(),
            EligibilityGate("ipl_200_80_8", 200, 80, 8),
        ),
        (
            "T20I_only_benchmark_gate",
            df[df["comp_category"] == "T20I"].copy(),
            BENCHMARK_GATE,
        ),
        (
            "T20I_only_200_80_8",
            df[df["comp_category"] == "T20I"].copy(),
            EligibilityGate("t20i_200_80_8", 200, 80, 8),
        ),
    ]

    rows = []
    for scope_name, sub_raw, gate in specs:
        sub = sub_raw if scope_name == "Primary_IPL_plus_All_T20I" else add_lpo_context_baselines(sub_raw, min_cell_n=min_cell_n)
        for role, id_col, ref_df in [
            ("batter", "striker_id", ref_bat),
            ("bowler", "bowler_id", ref_bowl),
        ]:
            cand = _score_canonical(sub, player_lookup, role=role, model_name=model_name, gate=gate)
            stats = _compare_to_reference(ref_df, cand, id_col=id_col, score_col=score_col)
            rows.append(
                {
                    "role": role,
                    "scope": scope_name,
                    "gate": gate.name,
                    "n_matches": int(sub["match_id"].nunique()),
                    "n_deliveries": int(len(sub)),
                    **stats,
                }
            )
    return pd.DataFrame(rows)


def run_pressure_sensitivity(
    df: pd.DataFrame,
    player_lookup: pd.DataFrame,
    ref_bat: pd.DataFrame,
    ref_bowl: pd.DataFrame,
    model_name: str = "model_b",
) -> pd.DataFrame:
    """Evaluate sensitivity across pressure thresholds (0.45/0.50/0.55) and continuous weighting schemes."""
    score_col = f"{model_name}_score"
    configs = [
        ("sigmoid_c0.425_s0.08_hp0.50_primary", 0.50, 0.35, "sigmoid", 0.425, 0.08),
        ("sigmoid_c0.425_s0.08_hp0.45", 0.45, 0.35, "sigmoid", 0.425, 0.08),
        ("sigmoid_c0.425_s0.08_hp0.55", 0.55, 0.35, "sigmoid", 0.425, 0.08),
        ("sigmoid_c0.400_s0.08_hp0.50", 0.50, 0.35, "sigmoid", 0.400, 0.08),
        ("sigmoid_c0.450_s0.08_hp0.50", 0.50, 0.35, "sigmoid", 0.450, 0.08),
        ("sigmoid_c0.425_s0.12_hp0.50", 0.50, 0.35, "sigmoid", 0.425, 0.12),
        ("linear_pi_weight_hp0.50", 0.50, 0.35, "linear", 0.425, 0.08),
    ]
    rows = []
    for cfg_name, ht, lt, wmode, ctr, scl in configs:
        df_p = compute_pressure_features(
            df,
            high_thresh=ht,
            low_thresh=lt,
            weight_mode=wmode,
            center=ctr,
            scale=scl,
        )
        for role, id_col, ref_df in [
            ("batter", "striker_id", ref_bat),
            ("bowler", "bowler_id", ref_bowl),
        ]:
            cand = _score_canonical(df_p, player_lookup, role=role, model_name=model_name)
            stats = _compare_to_reference(ref_df, cand, id_col=id_col, score_col=score_col)
            rows.append(
                {
                    "role": role,
                    "pressure_config": cfg_name,
                    "high_thresh": ht,
                    "weight_mode": wmode,
                    "center": ctr,
                    "scale": scl,
                    "hp_delivery_share": float(df_p["is_high_pressure"].mean()),
                    "mean_pressure_weight": float(df_p["pressure_weight"].mean()),
                    **stats,
                }
            )
    return pd.DataFrame(rows)


def run_wicket_sensitivity(
    df: pd.DataFrame,
    player_lookup: pd.DataFrame,
    ref_bat: pd.DataFrame,
    ref_bowl: pd.DataFrame,
    model_name: str = "model_b",
) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """
    Evaluate fixed wicket values w in {4.0, 6.0, 8.0} AND non-overlapping
    context-dependent marginal wicket value ('context').
    Returns (sensitivity_summary_df, context_wicket_table_df).
    """
    score_col = f"{model_name}_score"
    wkt_table = estimate_context_wicket_value_table(df)
    modes: List[Tuple[str, str | float]] = [
        ("fixed_4.0", 4.0),
        ("fixed_6.0", 6.0),
        ("fixed_8.0", 8.0),
        ("context_marginal", "context"),
    ]
    rows = []
    for label, w_mode in modes:
        for role, id_col, ref_df in [
            ("batter", "striker_id", ref_bat),
            ("bowler", "bowler_id", ref_bowl),
        ]:
            cand = _score_canonical(
                df, player_lookup, role=role, model_name=model_name, wicket_mode=w_mode
            )
            stats = _compare_to_reference(ref_df, cand, id_col=id_col, score_col=score_col)
            rows.append(
                {
                    "role": role,
                    "wicket_mode": label,
                    "mean_wicket_value": (
                        float(wkt_table["marginal_wicket_value"].mean())
                        if w_mode == "context"
                        else float(w_mode)
                    ),
                    **stats,
                }
            )
    return pd.DataFrame(rows), wkt_table


def run_eligibility_and_shrinkage_sensitivity(
    df: pd.DataFrame,
    player_lookup: pd.DataFrame,
    ref_bat: pd.DataFrame,
    ref_bowl: pd.DataFrame,
    model_name: str = "model_b",
) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """
    Sweep eligibility gates (200/80/8, 300/120/10, 400/150/12, 500/180/15, N_eff>=150)
    plus V1 lp_balls>=60 counterfactual trap, expose near-misses (Phil Salt) & rescues
    (Ashutosh Sharma), and evaluate shrinkage k in {60, 90, 120, 150, 180}.
    """
    score_col = f"{model_name}_score"
    elig_rows = []
    near_miss_frames = []

    for role, id_col, ref_df in [
        ("batter", "striker_id", ref_bat),
        ("bowler", "bowler_id", ref_bowl),
    ]:
        base_all, _ = compute_player_base_metrics(
            df, player_lookup, role=role, wicket_mode=6.0, shrink_k=DEFAULT_SHRINK_K, gate=BENCHMARK_GATE
        )
        nm = identify_near_misses(
            base_all,
            gate=BENCHMARK_GATE,
            id_col=id_col,
            score_col="shrunk_wp_impact",
        )
        nm["role"] = role
        near_miss_frames.append(nm)

        for gate in ELIGIBILITY_GATE_SWEEP:
            mask = apply_eligibility_gate(base_all, gate)
            cand = base_all[mask].copy()
            cand = score_model_a(cand)
            cand = score_model_b(cand, role=role)
            cand = cand.sort_values(score_col, ascending=False).reset_index(drop=True)
            stats = _compare_to_reference(ref_df, cand, id_col=id_col, score_col=score_col)
            elig_rows.append(
                {
                    "role": role,
                    "gate_name": gate.name,
                    "min_total_balls": gate.min_total_balls,
                    "min_hp_balls": gate.min_hp_balls,
                    "min_hp_matches": gate.min_hp_matches,
                    "min_pressure_neff": gate.min_pressure_neff,
                    "lp_balls_trap_active": False,
                    **stats,
                }
            )

        # Explicit counterfactual showing V1 lp_balls >= 60 trap impact
        v1_trap_mask = apply_eligibility_gate(base_all, BENCHMARK_GATE) & (base_all["lp_balls"] >= 60)
        cand_v1 = base_all[v1_trap_mask].copy()
        cand_v1 = score_model_a(cand_v1)
        cand_v1 = score_model_b(cand_v1, role=role)
        cand_v1 = cand_v1.sort_values(score_col, ascending=False).reset_index(drop=True)
        stats_v1 = _compare_to_reference(ref_df, cand_v1, id_col=id_col, score_col=score_col)
        elig_rows.append(
            {
                "role": role,
                "gate_name": "v1_counterfactual_with_lp60_trap",
                "min_total_balls": BENCHMARK_GATE.min_total_balls,
                "min_hp_balls": BENCHMARK_GATE.min_hp_balls,
                "min_hp_matches": BENCHMARK_GATE.min_hp_matches,
                "min_pressure_neff": 0.0,
                "lp_balls_trap_active": True,
                **stats_v1,
            }
        )

    # Shrinkage k sensitivity
    k_frames = [
        evaluate_k_shrinkage_sensitivity(df, role="batter", k_grid=SHRINK_K_GRID),
        evaluate_k_shrinkage_sensitivity(df, role="bowler", k_grid=SHRINK_K_GRID),
    ]
    k_df = pd.concat(k_frames, ignore_index=True)
    near_df = pd.concat(near_miss_frames, ignore_index=True)
    return pd.DataFrame(elig_rows), near_df, k_df
