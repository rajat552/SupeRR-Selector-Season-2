"""Batting pressure reliability evaluation and ranking model."""

import numpy as np
import pandas as pd


def _zscore(s: pd.Series) -> pd.Series:
    std = s.std(ddof=0)
    if std == 0 or np.isnan(std):
        return pd.Series(0.0, index=s.index)
    return (s - s.mean()) / std


def evaluate_batters(
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
    Evaluate and rank batters on pressure lift, absolute pressure impact,
    and cross-match consistency.
    """
    bat = df[df["is_batter_ball_faced"]].copy()
    bat["is_striker_dismissed"] = (
        bat["is_team_wicket"] & (bat["dismissed_player_id"] == bat["striker_id"])
    ).astype(float)
    bat["runs_above_exp"] = bat["runs"] - bat["ctx_bat_rpb"]
    bat["surv_above_exp"] = bat["ctx_bat_out_prob"] - bat["is_striker_dismissed"]
    bat["is_dot"] = (bat["runs"] == 0).astype(float)
    bat["is_bnd"] = (bat["is_four"] | bat["is_six"]).astype(float)

    def _agg_subset(sub: pd.DataFrame, prefix: str) -> pd.DataFrame:
        g = (
            sub.groupby("striker_id")
            .agg(
                balls=("runs", "count"),
                matches=("match_id", "nunique"),
                runs=("runs", "sum"),
                outs=("is_striker_dismissed", "sum"),
                rae_sum=("runs_above_exp", "sum"),
                surv_sum=("surv_above_exp", "sum"),
                dots=("is_dot", "sum"),
                bnds=("is_bnd", "sum"),
            )
            .reset_index()
        )
        g[f"{prefix}_sr"] = 100.0 * g["runs"] / g["balls"]
        g[f"{prefix}_avg"] = np.where(g["outs"] > 0, g["runs"] / g["outs"], g["runs"])
        g[f"{prefix}_dot_pct"] = 100.0 * g["dots"] / g["balls"]
        g[f"{prefix}_bnd_pct"] = 100.0 * g["bnds"] / g["balls"]
        g[f"{prefix}_rae_100"] = 100.0 * g["rae_sum"] / g["balls"]
        g[f"{prefix}_surv_100"] = 100.0 * g["surv_sum"] / g["balls"]
        g[f"{prefix}_impact_100"] = (
            g[f"{prefix}_rae_100"] + wicket_weight * g[f"{prefix}_surv_100"]
        )
        return g.rename(
            columns={
                "balls": f"{prefix}_balls",
                "matches": f"{prefix}_matches",
                "runs": f"{prefix}_runs",
                "outs": f"{prefix}_outs",
            }
        )[
            [
                "striker_id",
                f"{prefix}_balls",
                f"{prefix}_matches",
                f"{prefix}_runs",
                f"{prefix}_outs",
                f"{prefix}_sr",
                f"{prefix}_avg",
                f"{prefix}_dot_pct",
                f"{prefix}_bnd_pct",
                f"{prefix}_rae_100",
                f"{prefix}_surv_100",
                f"{prefix}_impact_100",
            ]
        ]

    tot = _agg_subset(bat, "tot")
    hp = _agg_subset(bat[bat["is_high_pressure"]], "hp")
    lp = _agg_subset(bat[bat["is_low_pressure"]], "lp")

    # Cross-match consistency in high-pressure appearances (>= 6 HP balls in match)
    hp_match = (
        bat[bat["is_high_pressure"]]
        .groupby(["striker_id", "match_id"])
        .agg(
            m_balls=("runs", "count"),
            m_rae=("runs_above_exp", "sum"),
            m_surv=("surv_above_exp", "sum"),
        )
        .reset_index()
    )
    hp_match = hp_match[hp_match["m_balls"] >= 6].copy()
    hp_match["m_impact"] = hp_match["m_rae"] + wicket_weight * hp_match["m_surv"]
    hp_match["beat_par"] = (hp_match["m_impact"] > 0).astype(float)

    cons = (
        hp_match.groupby("striker_id")
        .agg(
            hp_qual_matches=("match_id", "nunique"),
            consistency_rate=("beat_par", "mean"),
        )
        .reset_index()
    )

    # IPL vs T20I split in high pressure
    hp_fmt = (
        bat[bat["is_high_pressure"]]
        .groupby(["striker_id", "comp_category"])["runs"]
        .count()
        .unstack(fill_value=0)
        .reset_index()
        .rename(columns={"IPL": "hp_balls_ipl", "T20I": "hp_balls_t20i"})
    )
    if "hp_balls_ipl" not in hp_fmt.columns:
        hp_fmt["hp_balls_ipl"] = 0
    if "hp_balls_t20i" not in hp_fmt.columns:
        hp_fmt["hp_balls_t20i"] = 0

    hp_elite = (
        bat[bat["is_high_pressure"] & (bat["comp_tier"].isin(["IPL", "T20I_Full"]))]
        .groupby("striker_id")["runs"]
        .count()
        .rename("hp_balls_elite")
        .reset_index()
    )

    merged = (
        tot.merge(hp, on="striker_id", how="inner")
        .merge(lp, on="striker_id", how="inner")
        .merge(cons, on="striker_id", how="left")
        .merge(hp_fmt, on="striker_id", how="left")
        .merge(hp_elite, on="striker_id", how="left")
        .merge(
            player_lookup.rename(columns={"player_id": "striker_id"}),
            on="striker_id",
            how="left",
        )
    )
    merged["hp_balls_elite"] = merged["hp_balls_elite"].fillna(0).astype(int)

    # Eligibility filter
    elig = merged[
        (merged["tot_balls"] >= min_total_balls)
        & (merged["hp_balls"] >= min_hp_balls)
        & (merged["hp_balls_elite"] >= min_hp_elite_balls)
        & (merged["hp_matches"] >= min_hp_matches)
        & (merged["lp_balls"] >= 60)
        & (merged["hp_impact_100"] > 0)
    ].copy()

    elig["consistency_rate"] = elig["consistency_rate"].fillna(0.5)
    # Floor LP baseline at -15.0 to avoid rewarding terrible low-pressure baselines
    lp_baseline_capped = np.maximum(elig["lp_impact_100"], -15.0)
    elig["raw_delta_impact"] = elig["hp_impact_100"] - lp_baseline_capped
    elig["raw_delta_sr"] = elig["hp_sr"] - elig["lp_sr"]

    # Empirical Bayes shrinkage toward 0
    w_hp = elig["hp_balls"] / (elig["hp_balls"] + shrink_k)
    elig["shrunk_delta_impact"] = w_hp * elig["raw_delta_impact"]
    elig["shrunk_hp_impact"] = w_hp * elig["hp_impact_100"]

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
