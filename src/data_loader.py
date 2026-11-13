"""Read-only data ingestion and cleaning for SupeRR Selector Season 2."""

from pathlib import Path
from typing import Dict, Tuple
import pandas as pd


RAW_DIR = Path(__file__).resolve().parents[1] / "data" / "raw"

BOWLER_WICKET_TYPES = {"Caught", "Bowled", "LBW", "Stump", "Hit Wicket"}

# Full-member T20I teams (for sensitivity checks)
FULL_MEMBER_TEAMS = {
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


def build_player_lookup(
    bbb: pd.DataFrame, ctpm: pd.DataFrame
) -> pd.DataFrame:
    """Create canonical player_id -> player_name mapping (keyed strictly on player_id)."""
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
    # Take most frequent / first canonical name per player_id
    lookup = (
        combined.groupby("player_id")["player_name"]
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
    Return cleaned (bbb, matches, playing_eleven, player_lookup) ready for state reconstruction.
    """
    raw = load_raw_tables(raw_dir)
    comp = raw["competitions"].copy()
    comp["comp_category"] = comp.apply(classify_competition, axis=1)

    matches = raw["matches"].merge(
        comp[["comp_id", "comp_name", "match_format", "season", "comp_category"]],
        on="comp_id",
        how="left",
    )
    matches["season_year"] = (
        matches["match_date"].str.slice(0, 4).astype(int)
    )
    matches["is_full_member_t20i"] = (
        (matches["comp_category"] == "T20I")
        & matches["home_team"].isin(FULL_MEMBER_TEAMS)
        & matches["away_team"].isin(FULL_MEMBER_TEAMS)
    )

    # Deduplicate playing_eleven on (match_id, team_id, player_id)
    pe = raw["playing_eleven"].copy()
    pe = pe.sort_values(
        ["match_id", "team_id", "player_id", "is_played", "batting_order"],
        ascending=[True, True, True, False, True],
    ).drop_duplicates(subset=["match_id", "team_id", "player_id"], keep="first")

    bbb = raw["ball_by_ball"].copy()

    # Standardize dismissal_type typo
    bbb["dismissal_type"] = bbb["dismissal_type"].replace(
        {"Obstracting the field": "Obstructing the field"}
    )

    # Delivery classification flags
    bbb["is_wide"] = bbb["extras_type"] == "wide"
    bbb["is_noball"] = bbb["extras_type"].isin(["Overstep", "other"])
    bbb["is_legal_ball"] = ~(bbb["is_wide"] | bbb["is_noball"])
    bbb["is_batter_ball_faced"] = ~bbb["is_wide"]

    bbb["total_runs"] = bbb["runs"] + bbb["extras1_runs"] + bbb["extras_2_runs"]
    # Bowler-conceded runs: batter runs + wides + no-balls (excluding byes/legbyes/penalty)
    bbb["bowler_runs_conceded"] = bbb["runs"] + bbb["extras1_runs"].where(
        bbb["is_wide"] | bbb["is_noball"], 0
    )

    bbb["is_team_wicket"] = bbb["is_wicket"].astype(bool)
    bbb["is_bowler_wicket"] = bbb["is_wicket"].astype(bool) & bbb[
        "dismissal_type"
    ].isin(BOWLER_WICKET_TYPES)

    # Merge match metadata
    match_cols = [
        "match_id",
        "comp_id",
        "comp_name",
        "match_format",
        "season",
        "season_year",
        "comp_category",
        "is_full_member_t20i",
        "match_date",
        "stage",
        "venue_id",
        "venue_country",
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

    # Keep only matches that actually have ball-by-ball records
    active_match_ids = set(bbb["match_id"].unique())
    matches = matches[matches["match_id"].isin(active_match_ids)].copy()

    bbb = bbb.sort_values(
        ["match_id", "innings", "overid", "over_ball_num"]
    ).reset_index(drop=True)

    player_lookup = build_player_lookup(bbb, raw["ctpm"])
    return bbb, matches, pe, player_lookup

