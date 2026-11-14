"""Cross-definition robustness, weight perturbation, and model selection scoring audit for Model V3."""

from __future__ import annotations

import itertools
from pathlib import Path
from typing import Dict, List, Tuple
import numpy as np
import pandas as pd
from scipy.stats import zscore

ROOT = Path(__file__).resolve().parents[2]

from src.model_v4.data_loader import load_clean_dataset
from src.model_v4.state_builder import build_match_state
from src.model_v4.context_baselines import assign_wickets_bucket


def build_definition_c(df: pd.DataFrame, player_lookup: pd.DataFrame) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """
    Definition C: Simple Independent Definition
    - Batter pressure = live chase (<= 48 balls left, rrr 7-15, <= 7 down)
      OR 1st-innings collapse (>= 3 down by over 8 or >= 5 down by over 14).
    - Bowler pressure = defending a close chase (<= 48 balls left, rrr 6-12, <= 6 down)
      OR 1st-innings overs 16-20 with <= 4 down.
    - Expected values per format x phase x wickets bucket x innings.
    - Minimum 100 pressure balls.
    """
    work = df.copy()
    if "wickets_bucket" not in work.columns:
        work["wickets_bucket"] = assign_wickets_bucket(work["pre_wickets"])

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
    work["c_hp_bat"] = bat_hp_inn2 | bat_hp_inn1

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
    work["c_hp_bowl"] = bowl_hp_inn2 | bowl_hp_inn1

    cell_cols = ["comp_category", "phase", "wickets_bucket", "innings"]

    # 1. Batting under Definition C
    bat_df = work[work["is_batter_ball_faced"]].copy()
    bat_exp = (
        bat_df.groupby(cell_cols)
        .agg(
            tot_b=("runs", "count"),
            tot_r=("runs", "sum"),
            tot_w=("is_striker_dismissed", "sum"),
        )
        .reset_index()
    )
    bat_exp["c_exp_rpb"] = bat_exp["tot_r"] / bat_exp["tot_b"]
    bat_exp["c_exp_out"] = bat_exp["tot_w"].astype(float) / bat_exp["tot_b"]

    bat_df = bat_df.merge(bat_exp[cell_cols + ["c_exp_rpb", "c_exp_out"]], on=cell_cols, how="left")
    bat_df["c_imp"] = (bat_df["runs"] - bat_df["c_exp_rpb"]) + 6.0 * (
        bat_df["c_exp_out"] - bat_df["is_striker_dismissed"].astype(float)
    )

    bat_p = (
        bat_df[bat_df["c_hp_bat"]]
        .groupby("striker_id")
        .agg(
            c_hp_balls=("runs", "count"),
            c_hp_imp_sum=("c_imp", "sum"),
        )
        .reset_index()
    )
    bat_p["c_hp_impact"] = 100.0 * bat_p["c_hp_imp_sum"] / bat_p["c_hp_balls"]

    bat_n = (
        bat_df[~bat_df["c_hp_bat"]]
        .groupby("striker_id")
        .agg(
            c_norm_balls=("runs", "count"),
            c_norm_imp_sum=("c_imp", "sum"),
        )
        .reset_index()
    )
    bat_n["c_norm_impact"] = 100.0 * bat_n["c_norm_imp_sum"] / bat_n["c_norm_balls"]

    bat_c = (
        bat_p.merge(bat_n, on="striker_id", how="left")
        .merge(player_lookup.rename(columns={"player_id": "striker_id"}), on="striker_id", how="left")
    )
    bat_c["c_lift"] = bat_c["c_hp_impact"] - bat_c["c_norm_impact"]
    bat_c_elig = bat_c[bat_c["c_hp_balls"] >= 100].sort_values("c_hp_impact", ascending=False).reset_index(drop=True)
    bat_c_elig["rank_c"] = np.arange(1, len(bat_c_elig) + 1)

    # 2. Bowling under Definition C
    bowl_df = work[work["is_legal_ball"]].copy()
    bowl_exp = (
        bowl_df.groupby(cell_cols)
        .agg(
            tot_b=("bowler_runs_conceded", "count"),
            tot_r=("bowler_runs_conceded", "sum"),
            tot_w=("is_bowler_wicket", "sum"),
        )
        .reset_index()
    )
    bowl_exp["c_exp_rpb"] = bowl_exp["tot_r"] / bowl_exp["tot_b"]
    bowl_exp["c_exp_wkt"] = bowl_exp["tot_w"].astype(float) / bowl_exp["tot_b"]

    bowl_df = bowl_df.merge(bowl_exp[cell_cols + ["c_exp_rpb", "c_exp_wkt"]], on=cell_cols, how="left")
    bowl_df["c_imp"] = (bowl_df["c_exp_rpb"] - bowl_df["bowler_runs_conceded"]) + 6.0 * (
        bowl_df["is_bowler_wicket"].astype(float) - bowl_df["c_exp_wkt"]
    )

    bowl_p = (
        bowl_df[bowl_df["c_hp_bowl"]]
        .groupby("bowler_id")
        .agg(
            c_hp_balls=("bowler_runs_conceded", "count"),
            c_hp_imp_sum=("c_imp", "sum"),
        )
        .reset_index()
    )
    bowl_p["c_hp_impact"] = 24.0 * bowl_p["c_hp_imp_sum"] / bowl_p["c_hp_balls"]

    bowl_n = (
        bowl_df[~bowl_df["c_hp_bowl"]]
        .groupby("bowler_id")
        .agg(
            c_norm_balls=("bowler_runs_conceded", "count"),
            c_norm_imp_sum=("c_imp", "sum"),
        )
        .reset_index()
    )
    bowl_n["c_norm_impact"] = 24.0 * bowl_n["c_norm_imp_sum"] / bowl_n["c_norm_balls"]

    bowl_c = (
        bowl_p.merge(bowl_n, on="bowler_id", how="left")
        .merge(player_lookup.rename(columns={"player_id": "bowler_id"}), on="bowler_id", how="left")
    )
    bowl_c["c_lift"] = bowl_c["c_hp_impact"] - bowl_c["c_norm_impact"]
    bowl_c_elig = bowl_c[bowl_c["c_hp_balls"] >= 100].sort_values("c_hp_impact", ascending=False).reset_index(drop=True)
    bowl_c_elig["rank_c"] = np.arange(1, len(bowl_c_elig) + 1)

    return bat_c_elig, bowl_c_elig


def run_cross_definition_analysis():
    # Load V2 rankings (Definition A)
    v2_bat = pd.read_csv(ROOT / "outputs" / "model_v2" / "all_batter_rankings.csv")
    v2_bowl = pd.read_csv(ROOT / "outputs" / "model_v2" / "all_bowler_rankings.csv")

    # Load V3 rankings (Definition B)
    v3_bat = pd.read_csv(ROOT / "outputs" / "model_v4" / "all_batter_rankings.csv")
    v3_bowl = pd.read_csv(ROOT / "outputs" / "model_v4" / "all_bowler_rankings.csv")

    # Build Definition C
    bbb, matches, pe, player_lookup = load_clean_dataset()
    df = build_match_state(bbb)
    c_bat, c_bowl = build_definition_c(df, player_lookup)

    # Cross-definition merge for batters (union of all eligible players across A, B, C)
    bat_ids = sorted(list(set(v3_bat["striker_id"]) | set(v2_bat["striker_id"]) | set(c_bat["striker_id"])))
    bat_merge = pd.DataFrame({"striker_id": bat_ids})
    bat_merge = bat_merge.merge(player_lookup.rename(columns={"player_id": "striker_id"}), on="striker_id", how="left")
    bat_merge = bat_merge.merge(v2_bat[["striker_id", "rank"]].rename(columns={"rank": "rank_a"}), on="striker_id", how="left")
    bat_merge = bat_merge.merge(v3_bat[["striker_id", "rank"]].rename(columns={"rank": "rank_b"}), on="striker_id", how="left")
    bat_merge = bat_merge.merge(c_bat[["striker_id", "rank_c", "c_hp_balls"]], on="striker_id", how="left")
    bat_merge["discipline"] = "batter"
    bat_merge["player_id"] = bat_merge["striker_id"]

    # Cross-definition merge for bowlers (union of all eligible players across A, B, C)
    bowl_ids = sorted(list(set(v3_bowl["bowler_id"]) | set(v2_bowl["bowler_id"]) | set(c_bowl["bowler_id"])))
    bowl_merge = pd.DataFrame({"bowler_id": bowl_ids})
    bowl_merge = bowl_merge.merge(player_lookup.rename(columns={"player_id": "bowler_id"}), on="bowler_id", how="left")
    bowl_merge = bowl_merge.merge(v2_bowl[["bowler_id", "rank"]].rename(columns={"rank": "rank_a"}), on="bowler_id", how="left")
    bowl_merge = bowl_merge.merge(v3_bowl[["bowler_id", "rank"]].rename(columns={"rank": "rank_b"}), on="bowler_id", how="left")
    bowl_merge = bowl_merge.merge(c_bowl[["bowler_id", "rank_c", "c_hp_balls"]], on="bowler_id", how="left")
    bowl_merge["discipline"] = "bowler"
    bowl_merge["player_id"] = bowl_merge["bowler_id"]

    # Save full definition robustness CSV
    full_rob = pd.concat([bat_merge, bowl_merge], ignore_index=True)
    out_path = ROOT / "outputs" / "model_v4" / "definition_robustness.csv"
    full_rob.to_csv(out_path, index=False)
    print(f"Saved {out_path} ({len(full_rob)} rows)")

    # Weight perturbation analysis on (0.50, 0.30, 0.20)
    print("\n=== WEIGHT PERTURBATION STABILITY ===")
    delta_grid = [-0.10, 0.0, 0.10]
    weight_combos = []
    for d1, d2, d3 in itertools.product(delta_grid, delta_grid, delta_grid):
        w1, w2, w3 = 0.50 + d1, 0.30 + d2, 0.20 + d3
        if w1 > 0 and w2 > 0 and w3 > 0:
            tot = w1 + w2 + w3
            weight_combos.append((round(w1 / tot, 4), round(w2 / tot, 4), round(w3 / tot, 4)))
    weight_combos = sorted(list(set(weight_combos)))

    for role_name, df_rank, id_col in [("Batters", v3_bat, "striker_id"), ("Bowlers", v3_bowl, "bowler_id")]:
        base_top10 = set(df_rank.head(10)[id_col])
        z_abs = zscore(df_rank["shrunk_wp_impact"])
        z_lift = zscore(df_rank["maint_lift"])
        z_cons = zscore(df_rank["eb_consistency"])

        overlaps = []
        for w1, w2, w3 in weight_combos:
            pert_score = w1 * z_abs + w2 * z_lift + w3 * z_cons
            order = np.argsort(-pert_score)[:10]
            pert_top10 = set(df_rank.iloc[order][id_col])
            overlaps.append(len(base_top10 & pert_top10))

        print(f"{role_name} Top-10 Overlap with Base (0.5/0.3/0.2): min={min(overlaps)}/10, max={max(overlaps)}/10, mean={np.mean(overlaps):.2f}/10 across {len(weight_combos)} weight combinations")

    # Model A vs Model B Selection Scores without Interpretability Term
    print("\n=== MODEL SELECTION AUDIT (EMPIRICAL ONLY) ===")
    cmp_df = pd.read_csv(ROOT / "outputs" / "model_v4" / "model_comparison.csv")
    for role_name in ["batter", "bowler"]:
        sub_cmp = cmp_df[cmp_df["role"] == role_name]
        print(f"\nRole: {role_name.upper()}")
        for _, r in sub_cmp.iterrows():
            m_key = r["model_key"]
            pred = r["oos_player_spearman"] if pd.notna(r["oos_player_spearman"]) else 0.0
            loso = r["loso_mean_spearman"] if pd.notna(r["loso_mean_spearman"]) else 0.0
            interp = r["interpretability_score"]
            # Empirical-only composite: 0.50 * pred + 0.50 * loso
            emp_score = 0.50 * pred + 0.50 * loso
            orig_score = r["objective_selection_score"]
            print(f"  {m_key:7s}: OOS rho={pred:+.4f}, LOSO rho={loso:+.4f} | Empirical Score={emp_score:+.4f} | Original (with interp)={orig_score:+.4f}")


if __name__ == "__main__":
    run_cross_definition_analysis()

