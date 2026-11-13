"""Bowling pressure reliability evaluation and ranking model."""

import numpy as np
import pandas as pd


def _zscore(s: pd.Series) -> pd.Series:
    std = s.std(ddof=0)
    if std == 0 or np.isnan(std):
        return pd.Series(0.0, index=s.index)
    return (s - s.mean()) / std


def evaluate_bowlers(
    df: pd.DataFrame,
    player_lookup: pd.DataFrame,
    min_total_balls: int = 300,
    min_hp_balls: int = 120,
    min_hp_elite_balls: int = 80,
    min_hp_matches: int = 10,
    shrink_k: float = 120.0,
    wicket_weight: float = 6.0,
) -> pd.DataFrame:
    """
    Evaluate and rank bowlers on pressure lift, absolute pressure impact,
    and cross-match consistency.
    """
    bowl = df.copy()
    bowl["legal_int"] = bowl["is_legal_ball"].astype(int)
    bowl["wkt_int"] = bowl["is_bowler_wicket"].astype(int)
    bowl["exp_runs"] = bowl["ctx_bowl_rpb"] * bowl["legal_int"]
    bowl["exp_wkts"] = bowl["ctx_bowl_wkt_prob"] * bowl["legal_int"]
    bowl["runs_saved"] = bowl["exp_runs"] - bowl["bowler_runs_conceded"]
    bowl["wkts_above_exp"] = bowl["wkt_int"] - bowl["exp_wkts"]
    bowl["is_dot_bowl"] = (
        bowl["is_legal_ball"] & (bowl["bowler_runs_conceded"] == 0)
    ).astype(int)
    bowl["is_bnd_conceded"] = (bowl["is_four"] | bowl["is_six"]).astype(int)

    def _agg_subset(sub: pd.DataFrame, prefix: str) -> pd.DataFrame:
        g = (
            sub.groupby("bowler_id")
            .agg(
                legal_balls=("legal_int", "sum"),
                matches=("match_id", "nunique"),
                runs_conceded=("bowler_runs_conceded", "sum"),
                wkts=("wkt_int", "sum"),
                runs_saved_sum=("runs_saved", "sum"),
                wae_sum=("wkts_above_exp", "sum"),
                dots=("is_dot_bowl", "sum"),
                bnds=("is_bnd_conceded", "sum"),
            )
            .reset_index()
        )
        g = g[g["legal_balls"] > 0].copy()
        g[f"{prefix}_er"] = 6.0 * g["runs_conceded"] / g["legal_balls"]
        g[f"{prefix}_sr"] = np.where(
            g["wkts"] > 0, g["legal_balls"] / g["wkts"], np.nan
        )
        g[f"{prefix}_dot_pct"] = 100.0 * g["dots"] / g["legal_balls"]
        g[f"{prefix}_bnd_pct"] = 100.0 * g["bnds"] / g["legal_balls"]
        g[f"{prefix}_rso"] = 6.0 * g["runs_saved_sum"] / g["legal_balls"]
        g[f"{prefix}_wap_24"] = 24.0 * g["wae_sum"] / g["legal_balls"]
        g[f"{prefix}_impact_24"] = (
            4.0 * g[f"{prefix}_rso"] + wicket_weight * g[f"{prefix}_wap_24"]
        )
        return g.rename(
            columns={
                "legal_balls": f"{prefix}_balls",
                "matches": f"{prefix}_matches",
                "runs_conceded": f"{prefix}_runs",
                "wkts": f"{prefix}_wkts",
            }
        )[
            [
                "bowler_id",
                f"{prefix}_balls",
                f"{prefix}_matches",
                f"{prefix}_runs",
                f"{prefix}_wkts",
                f"{prefix}_er",
                f"{prefix}_sr",
                f"{prefix}_dot_pct",
                f"{prefix}_bnd_pct",
                f"{prefix}_rso",
                f"{prefix}_wap_24",
                f"{prefix}_impact_24",
            ]
        ]

    tot = _agg_subset(bowl, "tot")
    hp = _agg_subset(bowl[bowl["is_high_pressure"]], "hp")
    lp = _agg_subset(bowl[bowl["is_low_pressure"]], "lp")

    # Cross-match consistency in high-pressure spells (>= 6 HP legal balls in match)
    hp_match = (
        bowl[bowl["is_high_pressure"]]
        .groupby(["bowler_id", "match_id"])
        .agg(
            m_balls=("legal_int", "sum"),
            m_rs=("runs_saved", "sum"),
            m_wae=("wkts_above_exp", "sum"),
        )
        .reset_index()
    )
    hp_match = hp_match[hp_match["m_balls"] >= 6].copy()
    hp_match["m_impact"] = hp_match["m_rs"] + wicket_weight * hp_match["m_wae"]
    hp_match["beat_par"] = (hp_match["m_impact"] > 0).astype(float)

    cons = (
        hp_match.groupby("bowler_id")
        .agg(
            hp_qual_matches=("match_id", "nunique"),
            consistency_rate=("beat_par", "mean"),
        )
        .reset_index()
    )

    hp_fmt = (
        bowl[bowl["is_high_pressure"]]
        .groupby(["bowler_id", "comp_category"])["legal_int"]
        .sum()
        .unstack(fill_value=0)
        .reset_index()
        .rename(columns={"IPL": "hp_balls_ipl", "T20I": "hp_balls_t20i"})
    )
    if "hp_balls_ipl" not in hp_fmt.columns:
        hp_fmt["hp_balls_ipl"] = 0
    if "hp_balls_t20i" not in hp_fmt.columns:
        hp_fmt["hp_balls_t20i"] = 0

    hp_elite = (
        bowl[bowl["is_high_pressure"] & (bowl["comp_tier"].isin(["IPL", "T20I_Full"]))]
        .groupby("bowler_id")["legal_int"]
        .sum()
        .rename("hp_balls_elite")
        .reset_index()
    )

    merged = (
        tot.merge(hp, on="bowler_id", how="inner")
        .merge(lp, on="bowler_id", how="inner")
        .merge(cons, on="bowler_id", how="left")
        .merge(hp_fmt, on="bowler_id", how="left")
        .merge(hp_elite, on="bowler_id", how="left")
        .merge(
            player_lookup.rename(columns={"player_id": "bowler_id"}),
            on="bowler_id",
            how="left",
        )
    )
    merged["hp_balls_elite"] = merged["hp_balls_elite"].fillna(0).astype(int)

    elig = merged[
        (merged["tot_balls"] >= min_total_balls)
        & (merged["hp_balls"] >= min_hp_balls)
        & (merged["hp_balls_elite"] >= min_hp_elite_balls)
        & (merged["hp_matches"] >= min_hp_matches)
        & (merged["lp_balls"] >= 60)
        & (merged["hp_impact_24"] > 0)
    ].copy()

    elig["consistency_rate"] = elig["consistency_rate"].fillna(0.5)
    lp_baseline_capped = np.maximum(elig["lp_impact_24"], -10.0)
    elig["raw_delta_impact"] = elig["hp_impact_24"] - lp_baseline_capped
    elig["raw_delta_er"] = elig["hp_er"] - elig["lp_er"]

    w_hp = elig["hp_balls"] / (elig["hp_balls"] + shrink_k)
    elig["shrunk_delta_impact"] = w_hp * elig["raw_delta_impact"]
    elig["shrunk_hp_impact"] = w_hp * elig["hp_impact_24"]

    elig["z_delta"] = _zscore(elig["shrunk_delta_impact"])
    elig["z_abs_hp"] = _zscore(elig["shrunk_hp_impact"])
    elig["z_cons"] = _zscore(elig["consistency_rate"])

    elig["pressure_score"] = (
        0.40 * elig["z_delta"]
        + 0.40 * elig["z_abs_hp"]
        + 0.20 * elig["z_cons"]
    )

    elig = elig.sort_values("pressure_score", ascending=False).reset_index(drop=True)
    elig["rank"] = np.arange(1, len(elig) + 1)
    return elig
