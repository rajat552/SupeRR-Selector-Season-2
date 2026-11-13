"""Cricket delivery-level and dismissal accounting rules for Model V2."""

from __future__ import annotations

import pandas as pd


BOWLER_WICKET_TYPES: frozenset[str] = frozenset(
    {"Caught", "Bowled", "LBW", "Stump", "Hit Wicket"}
)
NON_BOWLER_WICKET_TYPES: frozenset[str] = frozenset(
    {"RunOut", "Retire Out", "Obstructing the field"}
)
DISMISSAL_TYPO_MAP: dict[str, str] = {
    "Obstracting the field": "Obstructing the field"
}
WIDE_EXTRAS_TYPE: str = "wide"
NOBALL_EXTRAS_TYPES: frozenset[str] = frozenset({"Overstep", "other"})
NON_BOWLER_EXTRAS_TYPES: frozenset[str] = frozenset({"byes", "legbyes", "Penalty"})


def normalize_dismissal_types(series: pd.Series) -> pd.Series:
    """Standardize known raw typos in dismissal_type while preserving nulls."""
    return series.replace(DISMISSAL_TYPO_MAP)


def apply_cricket_accounting(bbb: pd.DataFrame) -> pd.DataFrame:
    """
    Apply strict T20 cricket accounting flags and run/wicket columns to ball-by-ball data.

    Rules enforced:
    - 'wide': non-legal delivery, NOT a batter ball faced, extras1_runs charged to bowler.
    - 'Overstep' and 'other': no-balls -> non-legal delivery for bowler, batter runs count,
      IS a batter ball faced, runs + extras1_runs charged to bowler.
    - 'byes', 'legbyes': legal deliveries; extras excluded from bowler_runs_conceded.
    - 'Penalty': excluded from bowler_runs_conceded.
    - Bowler wickets: only Caught, Bowled, LBW, Stump, Hit Wicket.
    - Team wickets: all is_wicket=True events (including RunOut, Retire Out, Obstructing).
    - Striker dismissed: is_team_wicket AND (dismissed_player_id == striker_id), preserving
      non-striker run-outs accurately.
    """
    df = bbb.copy()

    if "dismissal_type" in df.columns:
        df["dismissal_type"] = normalize_dismissal_types(df["dismissal_type"])

    extras1 = df["extras1_runs"].fillna(0)
    extras2 = df["extras_2_runs"].fillna(0) if "extras_2_runs" in df.columns else 0
    runs = df["runs"].fillna(0)

    df["is_wide"] = df["extras_type"] == WIDE_EXTRAS_TYPE
    df["is_noball"] = df["extras_type"].isin(NOBALL_EXTRAS_TYPES)
    df["is_legal_ball"] = ~(df["is_wide"] | df["is_noball"])
    df["is_batter_ball_faced"] = ~df["is_wide"]

    df["total_runs"] = runs + extras1 + extras2
    df["bowler_runs_conceded"] = runs + extras1.where(
        df["is_wide"] | df["is_noball"], 0
    )

    df["is_team_wicket"] = df["is_wicket"].fillna(False).astype(bool)
    df["is_bowler_wicket"] = df["is_team_wicket"] & df["dismissal_type"].isin(
        BOWLER_WICKET_TYPES
    )

    if "dismissed_player_id" in df.columns and "striker_id" in df.columns:
        df["is_striker_dismissed"] = df["is_team_wicket"] & (
            df["dismissed_player_id"] == df["striker_id"]
        )
    else:
        df["is_striker_dismissed"] = False

    is_four = df["is_four"].fillna(False).astype(bool) if "is_four" in df.columns else False
    is_six = df["is_six"].fillna(False).astype(bool) if "is_six" in df.columns else False

    df["is_dot_bat"] = df["is_batter_ball_faced"] & (runs == 0)
    df["is_boundary_bat"] = df["is_batter_ball_faced"] & (is_four | is_six)
    df["is_dot_bowl"] = df["is_legal_ball"] & (df["bowler_runs_conceded"] == 0)
    df["is_boundary_conceded"] = is_four | is_six

    return df
