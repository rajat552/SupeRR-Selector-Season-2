"""Zero-look-ahead pre-delivery match-state reconstruction."""

import numpy as np
import pandas as pd


def assign_phase(overid: pd.Series) -> pd.Series:
    """Assign standard T20 innings phase: Powerplay (1-6), Middle (7-15), Death (16-20)."""
    return pd.Series(
        np.where(
            overid <= 6,
            "Powerplay",
            np.where(overid <= 15, "Middle", "Death"),
        ),
        index=overid.index,
    )


def build_match_state(bbb: pd.DataFrame) -> pd.DataFrame:
    """
    Reconstruct strict pre-delivery match state for every ball t using only
    deliveries 1..t-1 within the same (match_id, innings).
    """
    df = bbb.sort_values(
        ["match_id", "innings", "overid", "over_ball_num"]
    ).copy()

    # Max legal balls in the innings (revised_overs columns are stored in balls!)
    df["inn_max_balls"] = np.where(
        df["innings"] == 1,
        df["first_inn_revised_overs"].fillna(120.0),
        df["second_inn_revised_overs"].fillna(120.0),
    )

    grp = df.groupby(["match_id", "innings"], sort=False)

    # Cumulative totals including current ball, then subtract current ball for pre-delivery state
    df["post_runs"] = grp["total_runs"].cumsum()
    df["pre_runs"] = df["post_runs"] - df["total_runs"]

    df["post_wickets"] = grp["is_team_wicket"].cumsum()
    df["pre_wickets"] = df["post_wickets"] - df["is_team_wicket"].astype(int)

    df["legal_ball_int"] = df["is_legal_ball"].astype(int)
    df["post_legal_balls"] = grp["legal_ball_int"].cumsum()
    df["pre_legal_balls"] = df["post_legal_balls"] - df["legal_ball_int"]

    df["pre_balls_remaining"] = np.maximum(
        1.0, df["inn_max_balls"] - df["pre_legal_balls"]
    )
    df["pre_wickets_in_hand"] = np.maximum(0, 10 - df["pre_wickets"])

    df["phase"] = assign_phase(df["overid"])

    # Current Run Rate before delivery t
    df["pre_crr"] = np.where(
        df["pre_legal_balls"] > 0,
        6.0 * df["pre_runs"] / df["pre_legal_balls"],
        0.0,
    )

    # First innings total runs for each match (used as target+1 when not D/L revised)
    inn1_totals = (
        df[df["innings"] == 1]
        .groupby("match_id")["total_runs"]
        .sum()
        .rename("inn1_total_runs")
    )
    df = df.merge(inn1_totals, on="match_id", how="left")

    df["target"] = np.where(
        df["innings"] == 2,
        np.where(
            df["revised_target"].notna(),
            df["revised_target"],
            df["inn1_total_runs"] + 1.0,
        ),
        np.nan,
    )

    df["runs_needed"] = np.where(
        df["innings"] == 2,
        np.maximum(0.0, df["target"] - df["pre_runs"]),
        np.nan,
    )

    df["pre_rrr"] = np.where(
        df["innings"] == 2,
        np.minimum(36.0, 6.0 * df["runs_needed"] / df["pre_balls_remaining"]),
        np.nan,
    )

    return df

