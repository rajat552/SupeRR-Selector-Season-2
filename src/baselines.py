"""Competition-season-phase par baselines and context-adjusted residuals."""

import numpy as np
import pandas as pd


def add_context_baselines(df: pd.DataFrame) -> pd.DataFrame:
    """
    Add competition-season-phase expected par rates for batting and bowling
    so every delivery can be evaluated relative to its exact match context.
    """
    out = df.copy()
    out["comp_tier"] = np.where(
        out["comp_category"] == "IPL",
        "IPL",
        np.where(out["is_full_member_t20i"], "T20I_Full", "T20I_Assoc"),
    )
    ctx_cols = ["comp_tier", "season_year", "phase"]

    # Batting par (computed on batter balls faced: ~is_wide)
    bat_df = out[out["is_batter_ball_faced"]].copy()
    bat_df["is_striker_dismissed"] = (
        bat_df["is_team_wicket"]
        & (bat_df["dismissed_player_id"] == bat_df["striker_id"])
    ).astype(float)
    bat_df["is_dot_bat"] = (bat_df["runs"] == 0).astype(float)
    bat_df["is_boundary_bat"] = (bat_df["is_four"] | bat_df["is_six"]).astype(float)

    bat_par = (
        bat_df.groupby(ctx_cols)
        .agg(
            ctx_bat_rpb=("runs", "mean"),
            ctx_bat_out_prob=("is_striker_dismissed", "mean"),
            ctx_bat_dot_prob=("is_dot_bat", "mean"),
            ctx_bat_bnd_prob=("is_boundary_bat", "mean"),
        )
        .reset_index()
    )
    out = out.merge(bat_par, on=ctx_cols, how="left")

    # Bowling par (computed on legal balls for rate denominator, total bowler runs in numerator)
    bowl_par = (
        out.groupby(ctx_cols)
        .agg(
            tot_bowl_runs=("bowler_runs_conceded", "sum"),
            tot_legal_balls=("is_legal_ball", "sum"),
            tot_bowl_wkts=("is_bowler_wicket", "sum"),
        )
        .assign(
            ctx_bowl_rpb=lambda x: x["tot_bowl_runs"] / x["tot_legal_balls"],
            ctx_bowl_wkt_prob=lambda x: x["tot_bowl_wkts"] / x["tot_legal_balls"],
        )
        .reset_index()[ctx_cols + ["ctx_bowl_rpb", "ctx_bowl_wkt_prob"]]
    )
    out = out.merge(bowl_par, on=ctx_cols, how="left")

    return out
