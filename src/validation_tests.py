"""Robustness, sensitivity, and match-level bootstrap validation tests."""

import numpy as np
import pandas as pd
from scipy.stats import spearmanr

from data_loader import load_clean_dataset
from state_builder import build_match_state
from pressure import compute_pressure_index
from baselines import add_context_baselines
from batting_model import evaluate_batters
from bowling_model import evaluate_bowlers


def run_sensitivity_checks(df_base: pd.DataFrame, pl: pd.DataFrame) -> dict:
    """Run pressure-threshold and competition-scope sensitivity checks."""
    bat_primary = evaluate_batters(df_base, pl)
    bowl_primary = evaluate_bowlers(df_base, pl)
    top10_bat_ids = set(bat_primary.head(10)["striker_id"])
    top10_bowl_ids = set(bowl_primary.head(10)["bowler_id"])

    results = {"threshold_sensitivity": [], "scope_sensitivity": []}

    # 1. Pressure threshold sensitivity (0.45, 0.50, 0.55)
    for ht in [0.45, 0.50, 0.55]:
        df_t = df_base.copy()
        df_t["is_high_pressure"] = df_t["pressure_index"] >= ht
        b_t = evaluate_batters(df_t, pl)
        w_t = evaluate_bowlers(df_t, pl)

        b_m = bat_primary[["striker_id", "pressure_score"]].merge(
            b_t[["striker_id", "pressure_score"]], on="striker_id", suffixes=("_p", "_t")
        )
        w_m = bowl_primary[["bowler_id", "pressure_score"]].merge(
            w_t[["bowler_id", "pressure_score"]], on="bowler_id", suffixes=("_p", "_t")
        )
        results["threshold_sensitivity"].append(
            {
                "high_thresh": ht,
                "bat_top10_overlap": len(top10_bat_ids & set(b_t.head(10)["striker_id"])),
                "bat_spearman": float(spearmanr(b_m["pressure_score_p"], b_m["pressure_score_t"]).statistic),
                "bowl_top10_overlap": len(top10_bowl_ids & set(w_t.head(10)["bowler_id"])),
                "bowl_spearman": float(spearmanr(w_m["pressure_score_p"], w_m["pressure_score_t"]).statistic),
            }
        )

    # 2. Scope sensitivity: IPL + Full-Member T20I only
    df_fm = df_base[df_base["comp_tier"].isin(["IPL", "T20I_Full"])].copy()
    b_fm = evaluate_batters(df_fm, pl)
    w_fm = evaluate_bowlers(df_fm, pl)
    b_m2 = bat_primary[["striker_id", "pressure_score"]].merge(
        b_fm[["striker_id", "pressure_score"]], on="striker_id", suffixes=("_p", "_fm")
    )
    w_m2 = bowl_primary[["bowler_id", "pressure_score"]].merge(
        w_fm[["bowler_id", "pressure_score"]], on="bowler_id", suffixes=("_p", "_fm")
    )
    results["scope_sensitivity"].append(
        {
            "scope": "IPL + Full-Member T20I only",
            "bat_top10_overlap": len(top10_bat_ids & set(b_fm.head(10)["striker_id"])),
            "bat_spearman": float(spearmanr(b_m2["pressure_score_p"], b_m2["pressure_score_fm"]).statistic),
            "bowl_top10_overlap": len(top10_bowl_ids & set(w_fm.head(10)["bowler_id"])),
            "bowl_spearman": float(spearmanr(w_m2["pressure_score_p"], w_m2["pressure_score_fm"]).statistic),
        }
    )

    return results


def run_match_bootstrap(
    df: pd.DataFrame,
    bat_primary: pd.DataFrame,
    bowl_primary: pd.DataFrame,
    n_boot: int = 300,
    seed: int = 42,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """
    Fast match-level bootstrap on pre-computed player-match summaries
    to estimate rank uncertainty (median rank, 5th-95th percentile CI, P(Top10)).
    """
    rng = np.random.default_rng(seed)

    # Pre-aggregate batter-match stats
    bat = df[df["is_batter_ball_faced"]].copy()
    bat["is_striker_dismissed"] = (
        bat["is_team_wicket"] & (bat["dismissed_player_id"] == bat["striker_id"])
    ).astype(float)
    bat["rae"] = bat["runs"] - bat["ctx_bat_rpb"]
    bat["surv"] = bat["ctx_bat_out_prob"] - bat["is_striker_dismissed"]

    elig_bat_ids = set(bat_primary["striker_id"])
    bat_elig = bat[bat["striker_id"].isin(elig_bat_ids)]
    bm = (
        bat_elig.groupby(["match_id", "striker_id"])
        .agg(
            hp_balls=("is_high_pressure", "sum"),
            lp_balls=("is_low_pressure", "sum"),
            hp_rae=("rae", lambda s: s[bat_elig.loc[s.index, "is_high_pressure"]].sum()),
            hp_surv=("surv", lambda s: s[bat_elig.loc[s.index, "is_high_pressure"]].sum()),
            lp_rae=("rae", lambda s: s[bat_elig.loc[s.index, "is_low_pressure"]].sum()),
            lp_surv=("surv", lambda s: s[bat_elig.loc[s.index, "is_low_pressure"]].sum()),
        )
        .reset_index()
    )
    bm["hp_imp"] = bm["hp_rae"] + 6.0 * bm["hp_surv"]
    bm["lp_imp"] = bm["lp_rae"] + 6.0 * bm["lp_surv"]
    bm["hp_qual"] = (bm["hp_balls"] >= 6).astype(int)
    bm["hp_beat"] = ((bm["hp_balls"] >= 6) & (bm["hp_imp"] > 0)).astype(int)

    # Pre-aggregate bowler-match stats
    bowl = df.copy()
    bowl["legal_int"] = bowl["is_legal_ball"].astype(int)
    bowl["wkt_int"] = bowl["is_bowler_wicket"].astype(int)
    bowl["rs"] = bowl["ctx_bowl_rpb"] * bowl["legal_int"] - bowl["bowler_runs_conceded"]
    bowl["wae"] = bowl["wkt_int"] - bowl["ctx_bowl_wkt_prob"] * bowl["legal_int"]

    elig_bowl_ids = set(bowl_primary["bowler_id"])
    bowl_elig = bowl[bowl["bowler_id"].isin(elig_bowl_ids)]
    wm = (
        bowl_elig.groupby(["match_id", "bowler_id"])
        .agg(
            hp_balls=("legal_int", lambda s: s[bowl_elig.loc[s.index, "is_high_pressure"]].sum()),
            lp_balls=("legal_int", lambda s: s[bowl_elig.loc[s.index, "is_low_pressure"]].sum()),
            hp_rs=("rs", lambda s: s[bowl_elig.loc[s.index, "is_high_pressure"]].sum()),
            hp_wae=("wae", lambda s: s[bowl_elig.loc[s.index, "is_high_pressure"]].sum()),
            lp_rs=("rs", lambda s: s[bowl_elig.loc[s.index, "is_low_pressure"]].sum()),
            lp_wae=("wae", lambda s: s[bowl_elig.loc[s.index, "is_low_pressure"]].sum()),
        )
        .reset_index()
    )
    wm["hp_imp"] = wm["hp_rs"] + 6.0 * wm["hp_wae"]
    wm["lp_imp"] = wm["lp_rs"] + 6.0 * wm["lp_wae"]
    wm["hp_qual"] = (wm["hp_balls"] >= 6).astype(int)
    wm["hp_beat"] = ((wm["hp_balls"] >= 6) & (wm["hp_imp"] > 0)).astype(int)

    all_matches = df["match_id"].unique()
    n_m = len(all_matches)

    bat_ranks = {pid: [] for pid in elig_bat_ids}
    bowl_ranks = {pid: [] for pid in elig_bowl_ids}

    for _ in range(n_boot):
        sampled = rng.choice(all_matches, size=n_m, replace=True)
        m_counts = pd.Series(sampled).value_counts().rename("wt")

        # Batters
        b_s = bm.merge(m_counts, left_on="match_id", right_index=True, how="inner")
        for col in ["hp_balls", "lp_balls", "hp_imp", "lp_imp", "hp_qual", "hp_beat"]:
            b_s[col] = b_s[col] * b_s["wt"]
        bg = b_s.groupby("striker_id")[["hp_balls", "lp_balls", "hp_imp", "lp_imp", "hp_qual", "hp_beat"]].sum()
        bg = bg[(bg["hp_balls"] > 0) & (bg["lp_balls"] > 0)].copy()
        hp_i = 100.0 * bg["hp_imp"] / bg["hp_balls"]
        lp_i = np.maximum(100.0 * bg["lp_imp"] / bg["lp_balls"], -15.0)
        w = bg["hp_balls"] / (bg["hp_balls"] + 120.0)
        cons = np.where(bg["hp_qual"] > 0, bg["hp_beat"] / bg["hp_qual"], 0.5)
        score = (
            0.40 * ((w * (hp_i - lp_i) - (w * (hp_i - lp_i)).mean()) / (w * (hp_i - lp_i)).std(ddof=0))
            + 0.40 * ((w * hp_i - (w * hp_i).mean()) / (w * hp_i).std(ddof=0))
            + 0.20 * ((cons - cons.mean()) / max(1e-9, cons.std(ddof=0)))
        )
        r_b = score.rank(ascending=False)
        for pid, rk in r_b.items():
            bat_ranks[pid].append(rk)

        # Bowlers
        w_s = wm.merge(m_counts, left_on="match_id", right_index=True, how="inner")
        for col in ["hp_balls", "lp_balls", "hp_imp", "lp_imp", "hp_qual", "hp_beat"]:
            w_s[col] = w_s[col] * w_s["wt"]
        wg = w_s.groupby("bowler_id")[["hp_balls", "lp_balls", "hp_imp", "lp_imp", "hp_qual", "hp_beat"]].sum()
        wg = wg[(wg["hp_balls"] > 0) & (wg["lp_balls"] > 0)].copy()
        hp_i = 24.0 * wg["hp_imp"] / wg["hp_balls"]
        lp_i = np.maximum(24.0 * wg["lp_imp"] / wg["lp_balls"], -10.0)
        w = wg["hp_balls"] / (wg["hp_balls"] + 120.0)
        cons = np.where(wg["hp_qual"] > 0, wg["hp_beat"] / wg["hp_qual"], 0.5)
        score_w = (
            0.40 * ((w * (hp_i - lp_i) - (w * (hp_i - lp_i)).mean()) / (w * (hp_i - lp_i)).std(ddof=0))
            + 0.40 * ((w * hp_i - (w * hp_i).mean()) / (w * hp_i).std(ddof=0))
            + 0.20 * ((cons - cons.mean()) / max(1e-9, cons.std(ddof=0)))
        )
        r_w = score_w.rank(ascending=False)
        for pid, rk in r_w.items():
            bowl_ranks[pid].append(rk)

    bat_boot = pd.DataFrame(
        [
            {
                "striker_id": pid,
                "boot_median_rank": np.median(rks),
                "boot_p05_rank": np.percentile(rks, 5),
                "boot_p95_rank": np.percentile(rks, 95),
                "prob_top10": np.mean(np.array(rks) <= 10),
            }
            for pid, rks in bat_ranks.items()
            if len(rks) > 0
        ]
    )
    bowl_boot = pd.DataFrame(
        [
            {
                "bowler_id": pid,
                "boot_median_rank": np.median(rks),
                "boot_p05_rank": np.percentile(rks, 5),
                "boot_p95_rank": np.percentile(rks, 95),
                "prob_top10": np.mean(np.array(rks) <= 10),
            }
            for pid, rks in bowl_ranks.items()
            if len(rks) > 0
        ]
    )
    return bat_boot, bowl_boot
