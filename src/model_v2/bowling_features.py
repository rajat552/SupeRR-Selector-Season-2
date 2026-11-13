"""Bowling archetype, pace/spin, and spell feature engineering for Model V2."""

from __future__ import annotations

import numpy as np
import pandas as pd


BOWLING_STYLE_GROUP_MAP: dict[str, str] = {
    "Right-arm Fast": "Pace_Fast",
    "Left-arm Fast": "Pace_Fast",
    "Right-arm fast-medium": "Pace_FastMedium",
    "Right-arm medium-fast": "Pace_FastMedium",
    "Left-arm fast-medium": "Pace_FastMedium",
    "Left-arm medium-fast": "Pace_FastMedium",
    "Right-arm medium": "Pace_Medium",
    "Left-arm medium": "Pace_Medium",
    "Right-arm Leg-Break": "Spin_Wrist",
    "Left-arm Chinaman": "Spin_Wrist",
    "Right-arm offbreak": "Spin_Finger",
    "Slow left-arm orthodox": "Spin_Finger",
}


def add_bowling_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Standardize pace_or_spin, bowling_type, bowling_arm, and bowling_style_group,
    and compute strict pre-delivery bowler legal balls bowled in the current innings.
    """
    out = df.copy()
    out["pace_or_spin"] = out["pace_or_spin"].fillna("Unknown").astype(str)
    out["bowling_type"] = out["bowling_type"].fillna("Unknown").astype(str)

    bt_lower = out["bowling_type"].str.lower()
    out["bowling_arm"] = np.where(
        bt_lower.str.contains("right-arm"),
        "Right-arm",
        np.where(bt_lower.str.contains("left-arm"), "Left-arm", "Unknown"),
    )
    out["bowling_style_group"] = (
        out["bowling_type"].map(BOWLING_STYLE_GROUP_MAP).fillna("Unknown")
    )

    # Strict zero-look-ahead balls already bowled by this bowler in this innings
    legal_int = out["is_legal_ball"].astype(int)
    out["bowler_pre_legal_balls_in_inn"] = (
        legal_int.groupby([out["match_id"], out["innings"], out["bowler_id"]]).cumsum()
        - legal_int
    )
    return out


def summarize_bowler_styles(df: pd.DataFrame) -> pd.DataFrame:
    """Summarize each bowler_id's primary pace/spin classification, bowling_type, and phase share."""
    legal = df[df["is_legal_ball"]].copy()
    legal["_pp"] = (legal["phase"] == "Powerplay").astype(int)
    legal["_mid"] = (legal["phase"] == "Middle").astype(int)
    legal["_death"] = (legal["phase"] == "Death").astype(int)

    def _mode(s: pd.Series) -> str:
        m = s.mode()
        return str(m.iloc[0]) if not m.empty else "Unknown"

    agg = (
        legal.groupby("bowler_id")
        .agg(
            legal_balls=("is_legal_ball", "count"),
            pace_or_spin=("pace_or_spin", _mode),
            primary_bowling_type=("bowling_type", _mode),
            bowling_arm=("bowling_arm", _mode),
            bowling_style_group=("bowling_style_group", _mode),
            pp_balls=("_pp", "sum"),
            middle_balls=("_mid", "sum"),
            death_balls=("_death", "sum"),
        )
        .reset_index()
    )
    agg["pp_share"] = agg["pp_balls"] / agg["legal_balls"]
    agg["middle_share"] = agg["middle_balls"] / agg["legal_balls"]
    agg["death_share"] = agg["death_balls"] / agg["legal_balls"]
    return agg
