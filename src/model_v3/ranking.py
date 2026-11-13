"""Canonical ranking assembly and detailed player profile generation for Model V2."""

from __future__ import annotations

from typing import Dict, List, Sequence, Tuple
import numpy as np
import pandas as pd

from .shrinkage import eb_shrink_rate


def assemble_canonical_rankings(
    scored_df: pd.DataFrame,
    boot_df: pd.DataFrame,
    role: str,
    selected_model: str = "model_b",
) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """
    Assemble final ordered full-pool and Top-10 ranking tables with Model A/B/C
    cross-ranks, Kish N_eff, EB-shrunk metrics, and 1,000-resample bootstrap CIs.
    """
    id_col = "striker_id" if role == "batter" else "bowler_id"
    score_col = f"{selected_model}_score"

    out = scored_df.copy()
    for m in ("model_a", "model_b", "model_c"):
        col = f"{m}_score"
        if col in out.columns:
            out[f"{m}_rank"] = out[col].rank(ascending=False, method="min").astype(int)

    out["canonical_model"] = selected_model
    out["pressure_score"] = out[score_col]
    out = out.sort_values("pressure_score", ascending=False).reset_index(drop=True)
    out["rank"] = np.arange(1, len(out) + 1)

    boot_cols = [
        id_col,
        "n_boot",
        "valid_eligible_iters",
        "ineligible_iters",
        "absent_iters",
        "boot_median_rank",
        "boot_mean_rank",
        "boot_p05_rank",
        "boot_p95_rank",
        "boot_ci_width",
        "boot_mean_score",
        "boot_sd_score",
        "top10_inclusion_frequency",
    ]
    b_sub = boot_df[[c for c in boot_cols if c in boot_df.columns]].copy()
    out = out.merge(b_sub, on=id_col, how="left")

    # Separate practical context flag (never alters statistical rank)
    out["has_ipl_hp_exposure"] = out["hp_balls_ipl"] > 0
    out["practical_context_flag"] = np.where(
        out["hp_balls_ipl"] == 0,
        "Zero_IPL_HP_Exposure",
        np.where(~out["in_ipl_2025_2026"], "No_IPL_2025_2026_Record", "Active_IPL_2025_2026"),
    )

    unfiltered_top10 = out.head(10).copy()

    # D3 & D4: Final Top 10 restricted to players eligible in >= 800 bootstrap draws, with statistical tiers
    filtered_pool = out[out["valid_eligible_iters"] >= 800].copy().reset_index(drop=True)
    top10 = filtered_pool.head(10).copy()
    top10["unfiltered_rank"] = top10["rank"]
    top10["final_rank"] = np.arange(1, len(top10) + 1)
    top10["rank"] = top10["final_rank"]

    # Assign statistical tiers per D4
    if role == "batter":
        top10["tier"] = np.where(
            top10["pressure_score"] >= 2.00,
            "Tier 1",
            np.where(top10["pressure_score"] >= 1.50, "Tier 2", "Tier 3"),
        )
    else:
        top10["tier"] = np.where(
            top10["pressure_score"] >= 2.10,
            "Tier 1",
            np.where(top10["pressure_score"] >= 1.20, "Tier 2", "Tier 3"),
        )

    return out, top10


def build_player_profiles(
    df: pd.DataFrame,
    rankings_df: pd.DataFrame,
    role: str,
    profile_player_ids: Sequence[int] | None = None,
    wicket_weight: float = 6.0,
    shrink_k: float = 120.0,
) -> pd.DataFrame:
    """
    Build detailed multi-dimensional player profiles (phase splits, pace/spin or
    bat-hand matchup splits, IPL vs T20I splits, observed vs shrunk metrics)
    for Top 10 + spotlight / top-30 eligible candidates.
    """
    id_col = "striker_id" if role == "batter" else "bowler_id"
    if profile_player_ids is None:
        # Include top 30 ranked + spotlight players if present in eligible pool
        spotlight = {8101, 1699, 10203, 5577, 2933, 3644, 781, 6396, 37052, 2258, 6288}
        top_ids = list(rankings_df.head(30)[id_col].astype(int))
        extra_ids = [
            int(pid)
            for pid in rankings_df[id_col].astype(int)
            if int(pid) in spotlight and int(pid) not in top_ids
        ]
        target_ids = top_ids + extra_ids
    else:
        target_ids = [int(x) for x in profile_player_ids]

    if role == "batter":
        sub = df[df["is_batter_ball_faced"] & df["striker_id"].isin(target_ids)].copy()
        sub["_unit"] = 1.0
        sub["_runs"] = sub["runs"].astype(float)
        sub["_evt"] = sub["is_striker_dismissed"].astype(float)
        sub["_imp"] = (sub["_runs"] - sub["ctx_bat_rpb"]) + wicket_weight * (
            sub["ctx_bat_out_prob"] - sub["_evt"]
        )
        scale = 100.0
        split_col = "pace_or_spin"
        split_vals = [("pace", "Pace"), ("spin", "Spin")]
    else:
        sub = df[df["bowler_id"].isin(target_ids)].copy()
        sub["_unit"] = sub["is_legal_ball"].astype(float)
        sub["_runs"] = sub["bowler_runs_conceded"].astype(float)
        sub["_evt"] = sub["is_bowler_wicket"].astype(float)
        sub["_imp"] = (sub["ctx_bowl_rpb"] * sub["_unit"] - sub["_runs"]) + wicket_weight * (
            sub["_evt"] - sub["ctx_bowl_wkt_prob"] * sub["_unit"]
        )
        scale = 24.0
        split_col = "batting_hand"
        split_vals = [("rhb", "RHB"), ("lhb", "LHB")]

    pw_col = "pressure_weight_bat" if role == "batter" else "pressure_weight_bowl"
    hp_col = "is_high_pressure_bat" if role == "batter" else "is_high_pressure_bowl"
    actual_pw = pw_col if pw_col in sub.columns else "pressure_weight"
    actual_hp = hp_col if hp_col in sub.columns else "is_high_pressure"

    sub["_wp_u"] = sub[actual_pw].to_numpy(dtype=float) * sub["_unit"].to_numpy(dtype=float)
    sub["_wp_imp"] = sub[actual_pw].to_numpy(dtype=float) * sub["_imp"].to_numpy(dtype=float)

    base_sub = rankings_df[rankings_df[id_col].isin(target_ids)].copy()

    def _agg_slice(mask: pd.Series, tag: str) -> pd.DataFrame:
        s = sub[mask]
        if len(s) == 0:
            return pd.DataFrame(columns=[id_col, f"{tag}_balls", f"{tag}_wp_impact", f"{tag}_shrunk_wp_impact"])
        g = s.groupby(id_col, as_index=False)[["_unit", "_wp_u", "_wp_imp"]].sum()
        # Kish N_eff inside slice
        w2 = (
            s.assign(_w2=s["_wp_u"] ** 2)
            .groupby(id_col, as_index=False)["_w2"]
            .sum()
        )
        g = g.merge(w2, on=id_col, how="left")
        neff = np.divide(g["_wp_u"] ** 2, g["_w2"], out=np.zeros(len(g)), where=g["_w2"] > 0.0)
        raw_imp = np.divide(
            scale * g["_wp_imp"],
            g["_wp_u"],
            out=np.zeros(len(g)),
            where=g["_wp_u"] > 0.0,
        )
        g[f"{tag}_balls"] = g["_unit"].astype(int)
        g[f"{tag}_wp_impact"] = raw_imp
        g[f"{tag}_shrunk_wp_impact"] = eb_shrink_rate(raw_imp, neff, k=shrink_k, prior_mean=0.0)
        return g[[id_col, f"{tag}_balls", f"{tag}_wp_impact", f"{tag}_shrunk_wp_impact"]]

    prof = base_sub.copy()
    for phase in ("Powerplay", "Middle", "Death"):
        tag = phase.lower()
        sl = _agg_slice(sub["phase"] == phase, tag)
        prof = prof.merge(sl, on=id_col, how="left")

    for tag, val in split_vals:
        sl = _agg_slice(sub[split_col].astype(str).str.lower() == val.lower(), tag)
        prof = prof.merge(sl, on=id_col, how="left")

    # Best pressure match performance per player
    hp_m = (
        sub[sub[actual_hp]]
        .groupby([id_col, "match_id", "match_date", "comp_category"], as_index=False)
        .agg(
            m_hp_balls=("_unit", "sum"),
            m_hp_runs=("_runs", "sum"),
            m_hp_evt=("_evt", "sum"),
            m_hp_imp=("_imp", "sum"),
        )
    )
    hp_m = hp_m[hp_m["m_hp_balls"] >= 6].sort_values(
        [id_col, "m_hp_imp"], ascending=[True, False]
    )
    best_m = hp_m.drop_duplicates(subset=[id_col], keep="first").rename(
        columns={
            "match_id": "best_hp_match_id",
            "match_date": "best_hp_match_date",
            "comp_category": "best_hp_match_format",
            "m_hp_balls": "best_hp_match_balls",
            "m_hp_imp": "best_hp_match_impact",
        }
    )
    prof = prof.merge(
        best_m[
            [
                id_col,
                "best_hp_match_id",
                "best_hp_match_date",
                "best_hp_match_format",
                "best_hp_match_balls",
                "best_hp_match_impact",
            ]
        ],
        on=id_col,
        how="left",
    )
    return prof.sort_values("rank").reset_index(drop=True)
