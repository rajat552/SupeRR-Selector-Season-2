"""Read-only data ingestion, deduplication, and scope filtering for Model V2."""

from __future__ import annotations

from pathlib import Path
from typing import Dict, Tuple
import numpy as np
import pandas as pd

from .cricket_accounting import apply_cricket_accounting


RAW_DIR = Path(__file__).resolve().parents[2] / "data" / "raw"

FULL_MEMBER_TEAMS: frozenset[str] = frozenset(
    {
        "India",
        "Australia",
        "England",
        "South Africa",
        "New Zealand",
        "Pakistan",
        "West Indies",
        "Sri Lanka",
        "Bangladesh",
        "Afghanistan",
        "Zimbabwe",
        "Ireland",
    }
)


def load_raw_tables(raw_dir: Path = RAW_DIR) -> Dict[str, pd.DataFrame]:
    """Load all six original CSV files without modifying any raw data."""
    return {
        "competitions": pd.read_csv(raw_dir / "competitions.csv"),
        "teams": pd.read_csv(raw_dir / "teams.csv"),
        "matches": pd.read_csv(raw_dir / "matches.csv"),
        "playing_eleven": pd.read_csv(raw_dir / "playing_eleven.csv"),
        "ctpm": pd.read_csv(raw_dir / "competition_team_player_mapping.csv"),
        "ball_by_ball": pd.read_csv(raw_dir / "ball_by_ball.csv", low_memory=False),
    }


def classify_competition(row: pd.Series) -> str:
    """Classify competitions into IPL, T20I, or Other_T20."""
    if row["match_format"] == "T20" and "IPL" in str(row["comp_name"]):
        return "IPL"
    if row["match_format"] == "T20":
        return "Other_T20"
    return "T20I"


def assign_comp_tier(comp_category: pd.Series, is_full_member_t20i: pd.Series) -> pd.Series:
    """Assign hierarchical competition tier: IPL, T20I_Full, T20I_Assoc, or Other_T20."""
    return pd.Series(
        np.where(
            comp_category == "IPL",
            "IPL",
            np.where(
                comp_category == "Other_T20",
                "Other_T20",
                np.where(is_full_member_t20i, "T20I_Full", "T20I_Assoc"),
            ),
        ),
        index=comp_category.index,
    )


def deduplicate_playing_eleven(pe: pd.DataFrame) -> pd.DataFrame:
    """
    Deduplicate playing_eleven on (match_id, team_id, player_id),
    prioritizing is_played=True first and lowest non-null batting_order.
    """
    out = pe.copy()
    out["_is_played_sort"] = out["is_played"].fillna(False).astype(bool)
    out = out.sort_values(
        ["match_id", "team_id", "player_id", "_is_played_sort", "batting_order"],
        ascending=[True, True, True, False, True],
        na_position="last",
    )
    out = out.drop_duplicates(
        subset=["match_id", "team_id", "player_id"], keep="first"
    ).drop(columns=["_is_played_sort"])
    return out.reset_index(drop=True)


def build_player_lookup(bbb: pd.DataFrame, ctpm: pd.DataFrame) -> pd.DataFrame:
    """
    Create canonical player_id -> player_name lookup keyed strictly on player_id.
    Never collapses homonyms sharing identical player_name strings.
    """
    striker_map = bbb[["striker_id", "striker_name"]].rename(
        columns={"striker_id": "player_id", "striker_name": "player_name"}
    )
    non_striker_map = bbb[["non_striker_id", "non_striker_name"]].rename(
        columns={"non_striker_id": "player_id", "non_striker_name": "player_name"}
    )
    bowler_map = bbb[["bowler_id", "bowler_name"]].rename(
        columns={"bowler_id": "player_id", "bowler_name": "player_name"}
    )
    ctpm_map = ctpm[["player_id", "player_name"]]

    combined = pd.concat(
        [striker_map, non_striker_map, bowler_map, ctpm_map], ignore_index=True
    ).dropna(subset=["player_id", "player_name"])
    combined["player_id"] = combined["player_id"].astype("int64")

    lookup = (
        combined.groupby("player_id", sort=True)["player_name"]
        .agg(lambda s: s.mode().iloc[0] if not s.mode().empty else s.iloc[0])
        .reset_index()
    )
    return lookup


def load_clean_dataset(
    include_other_t20: bool = False,
    include_super_overs: bool = False,
    raw_dir: Path = RAW_DIR,
) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """
    Return cleaned (bbb, matches, playing_eleven, player_lookup) ready for state
    reconstruction and feature engineering.

    Primary scope (default): 837 matches (367 IPL + 470 T20I), 193,988 deliveries.
    """
    raw = load_raw_tables(raw_dir)
    comp = raw["competitions"].copy()
    comp["comp_category"] = comp.apply(classify_competition, axis=1)

    matches = raw["matches"].merge(
        comp[["comp_id", "comp_name", "match_format", "season", "comp_category"]],
        on="comp_id",
        how="left",
    )
    matches["season_year"] = matches["match_date"].astype(str).str.slice(0, 4).astype(int)
    matches["is_full_member_t20i"] = (
        (matches["comp_category"] == "T20I")
        & matches["home_team"].isin(FULL_MEMBER_TEAMS)
        & matches["away_team"].isin(FULL_MEMBER_TEAMS)
    )
    matches["comp_tier"] = assign_comp_tier(
        matches["comp_category"], matches["is_full_member_t20i"]
    )

    pe = deduplicate_playing_eleven(raw["playing_eleven"])
    bbb = apply_cricket_accounting(raw["ball_by_ball"])

    match_cols = [
        "match_id",
        "comp_id",
        "comp_name",
        "match_format",
        "season",
        "season_year",
        "comp_category",
        "comp_tier",
        "is_full_member_t20i",
        "match_date",
        "match_number",
        "stage",
        "venue_id",
        "venue_country",
        "home_team_id",
        "away_team_id",
        "knock_out",
        "first_inn_revised_overs",
        "second_inn_revised_overs",
        "revised_target",
        "win_team_id",
        "result",
    ]
    bbb = bbb.merge(matches[match_cols], on="match_id", how="left")

    if not include_other_t20:
        bbb = bbb[bbb["comp_category"] != "Other_T20"].copy()
        matches = matches[matches["comp_category"] != "Other_T20"].copy()

    if not include_super_overs:
        bbb = bbb[bbb["innings"].isin([1, 2])].copy()

    active_match_ids = set(bbb["match_id"].unique())
    matches = matches[matches["match_id"].isin(active_match_ids)].copy()

    sort_cols = ["match_id", "innings", "overid", "over_ball_num"]
    if "innings_ball_num" in bbb.columns:
        sort_cols.append("innings_ball_num")
    bbb = bbb.sort_values(sort_cols).reset_index(drop=True)

    player_lookup = build_player_lookup(bbb, raw["ctpm"])
    return bbb, matches.reset_index(drop=True), pe, player_lookup
