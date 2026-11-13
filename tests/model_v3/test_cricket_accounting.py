"""Unit and raw-data tests for cricket accounting, scope filtering, deduplication, and homonyms."""

from __future__ import annotations

import sys
from pathlib import Path
import numpy as np
import pandas as pd
import pytest

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.model_v3.cricket_accounting import (
    BOWLER_WICKET_TYPES,
    apply_cricket_accounting,
    normalize_dismissal_types,
)
from src.model_v3.data_loader import (
    deduplicate_playing_eleven,
    load_clean_dataset,
)
from src.model_v3.batting_features import (
    ROLE_FINISHER,
    ROLE_MIDDLE,
    ROLE_TOP,
    add_batting_features,
    order_to_batting_role,
)
from src.model_v3.bowling_features import add_bowling_features


@pytest.fixture(scope="module")
def primary_data():
    bbb, matches, pe, player_lookup = load_clean_dataset(
        include_other_t20=False, include_super_overs=False
    )
    return bbb, matches, pe, player_lookup


@pytest.fixture(scope="module")
def all_scope_data():
    bbb, matches, pe, player_lookup = load_clean_dataset(
        include_other_t20=True, include_super_overs=True
    )
    return bbb, matches, pe, player_lookup


def test_synthetic_extras_and_wicket_accounting():
    """Verify wides, Overstep/other no-balls, byes, legbyes, Penalty, and dismissal types."""
    syn = pd.DataFrame(
        [
            # 0: wide (+1 extra1)
            {"match_id": 1, "innings": 1, "overid": 1, "over_ball_num": 1, "striker_id": 10, "bowler_id": 20, "runs": 0, "extras_type": "wide", "extras1_runs": 1, "extras_2_runs": 0, "is_wicket": False, "dismissal_type": np.nan, "dismissed_player_id": np.nan, "is_four": 0, "is_six": 0},
            # 1: Overstep no-ball with 4 off the bat
            {"match_id": 1, "innings": 1, "overid": 1, "over_ball_num": 2, "striker_id": 10, "bowler_id": 20, "runs": 4, "extras_type": "Overstep", "extras1_runs": 1, "extras_2_runs": 0, "is_wicket": False, "dismissal_type": np.nan, "dismissed_player_id": np.nan, "is_four": 1, "is_six": 0},
            # 2: other no-ball with 6 off the bat
            {"match_id": 1, "innings": 1, "overid": 1, "over_ball_num": 3, "striker_id": 10, "bowler_id": 20, "runs": 6, "extras_type": "other", "extras1_runs": 1, "extras_2_runs": 0, "is_wicket": False, "dismissal_type": np.nan, "dismissed_player_id": np.nan, "is_four": 0, "is_six": 1},
            # 3: legbyes (+2) -> legal, 0 bowler runs
            {"match_id": 1, "innings": 1, "overid": 1, "over_ball_num": 4, "striker_id": 10, "bowler_id": 20, "runs": 0, "extras_type": "legbyes", "extras1_runs": 2, "extras_2_runs": 0, "is_wicket": False, "dismissal_type": np.nan, "dismissed_player_id": np.nan, "is_four": 0, "is_six": 0},
            # 4: byes (+4) -> legal, 0 bowler runs
            {"match_id": 1, "innings": 1, "overid": 1, "over_ball_num": 5, "striker_id": 10, "bowler_id": 20, "runs": 0, "extras_type": "byes", "extras1_runs": 4, "extras_2_runs": 0, "is_wicket": False, "dismissal_type": np.nan, "dismissed_player_id": np.nan, "is_four": 0, "is_six": 0},
            # 5: Penalty (+5) -> legal, 0 bowler runs
            {"match_id": 1, "innings": 1, "overid": 1, "over_ball_num": 6, "striker_id": 10, "bowler_id": 20, "runs": 0, "extras_type": "Penalty", "extras1_runs": 5, "extras_2_runs": 0, "is_wicket": False, "dismissal_type": np.nan, "dismissed_player_id": np.nan, "is_four": 0, "is_six": 0},
            # 6: Non-striker RunOut -> team wicket, NOT bowler wicket, NOT striker dismissed
            {"match_id": 1, "innings": 1, "overid": 1, "over_ball_num": 7, "striker_id": 10, "bowler_id": 20, "runs": 1, "extras_type": np.nan, "extras1_runs": 0, "extras_2_runs": 0, "is_wicket": True, "dismissal_type": "RunOut", "dismissed_player_id": 11, "is_four": 0, "is_six": 0},
            # 7: Obstracting the field typo -> normalized, team wicket, NOT bowler wicket
            {"match_id": 1, "innings": 1, "overid": 1, "over_ball_num": 8, "striker_id": 10, "bowler_id": 20, "runs": 0, "extras_type": np.nan, "extras1_runs": 0, "extras_2_runs": 0, "is_wicket": True, "dismissal_type": "Obstracting the field", "dismissed_player_id": 10, "is_four": 0, "is_six": 0},
            # 8: Caught -> team wicket AND bowler wicket AND striker dismissed
            {"match_id": 1, "innings": 1, "overid": 1, "over_ball_num": 9, "striker_id": 12, "bowler_id": 20, "runs": 0, "extras_type": np.nan, "extras1_runs": 0, "extras_2_runs": 0, "is_wicket": True, "dismissal_type": "Caught", "dismissed_player_id": 12, "is_four": 0, "is_six": 0},
        ]
    )
    out = apply_cricket_accounting(syn)

    assert out["is_legal_ball"].tolist() == [False, False, False, True, True, True, True, True, True]
    assert out["is_batter_ball_faced"].tolist() == [False, True, True, True, True, True, True, True, True]
    assert out["bowler_runs_conceded"].tolist() == [1, 5, 7, 0, 0, 0, 1, 0, 0]
    assert out["total_runs"].tolist() == [1, 5, 7, 2, 4, 5, 1, 0, 0]
    assert out["is_team_wicket"].tolist() == [False] * 6 + [True, True, True]
    assert out["is_bowler_wicket"].tolist() == [False] * 8 + [True]
    assert out["is_striker_dismissed"].tolist() == [False] * 6 + [False, True, True]
    assert out.loc[7, "dismissal_type"] == "Obstructing the field"


def test_raw_primary_scope_counts(primary_data, all_scope_data):
    """Primary scope excludes Other_T20 (30 matches, 6985 rows) and Super Overs (38 rows)."""
    bbb_prim, matches_prim, pe_prim, _ = primary_data
    bbb_all, _, _, _ = all_scope_data

    assert matches_prim["match_id"].nunique() == 837
    assert bbb_prim["match_id"].nunique() == 837
    assert (matches_prim["comp_category"] == "IPL").sum() == 367
    assert (matches_prim["comp_category"] == "T20I").sum() == 470
    assert len(bbb_prim) == 193_988
    assert bbb_prim["innings"].isin([1, 2]).all()
    assert (bbb_prim["comp_category"] != "Other_T20").all()

    assert (bbb_all["comp_category"] == "Other_T20").sum() == 6_985
    assert bbb_all["innings"].isin([3, 4]).sum() == 38


def test_raw_cricket_accounting_rules(all_scope_data):
    """Validate legal delivery, bowler conceded runs, and dismissal rules on raw data."""
    bbb_all, _, _, _ = all_scope_data

    wides = bbb_all[bbb_all["extras_type"] == "wide"]
    assert (~wides["is_legal_ball"]).all()
    assert (~wides["is_batter_ball_faced"]).all()
    assert int(wides["bowler_runs_conceded"].sum()) == int(wides["extras1_runs"].sum())

    noballs = bbb_all[bbb_all["extras_type"].isin(["Overstep", "other"])]
    assert (~noballs["is_legal_ball"]).all()
    assert noballs["is_batter_ball_faced"].all()
    assert int(noballs["runs"].sum()) > 1000

    byes = bbb_all[bbb_all["extras_type"].isin(["byes", "legbyes"])]
    assert byes["is_legal_ball"].all()
    assert int(byes["bowler_runs_conceded"].sum()) == int(byes["runs"].sum())

    assert "Obstracting the field" not in set(bbb_all["dismissal_type"].dropna().unique())
    non_bowler = bbb_all[
        bbb_all["is_team_wicket"] & (~bbb_all["dismissal_type"].isin(BOWLER_WICKET_TYPES))
    ]
    assert int(non_bowler["is_bowler_wicket"].sum()) == 0
    assert len(bbb_all[bbb_all["dismissal_type"] == "RunOut"]) == 600


def test_playing_eleven_deduplication_and_homonyms(primary_data):
    """playing_eleven deduplicates 40 key duplicates keeping is_played=True; homonyms stay separate."""
    _, _, pe_prim, pl_prim = primary_data

    assert pe_prim.duplicated(subset=["match_id", "team_id", "player_id"]).sum() == 0

    # Synthetic verification that is_played=True wins over is_played=False even with lower batting_order
    syn_pe = pd.DataFrame(
        [
            {"match_id": 1, "team_id": 10, "player_id": 99, "batting_order": 2.0, "is_played": False},
            {"match_id": 1, "team_id": 10, "player_id": 99, "batting_order": 5.0, "is_played": True},
        ]
    )
    dedup = deduplicate_playing_eleven(syn_pe)
    assert len(dedup) == 1
    assert bool(dedup.loc[0, "is_played"]) is True
    assert float(dedup.loc[0, "batting_order"]) == 5.0

    # Homonym identity checks
    assert set(pl_prim[pl_prim["player_name"] == "Abdul Samad"]["player_id"]) == {7446, 6922}
    assert set(pl_prim[pl_prim["player_name"] == "Rashid Khan"]["player_id"]) == {4722, 20172}
    assert set(pl_prim[pl_prim["player_name"] == "Haider Ali"]["player_id"]) == {7338, 28756}
    assert pl_prim["player_id"].duplicated().sum() == 0


def test_batting_and_bowling_features_and_role_flags(primary_data):
    """Dynamic batting roles flag mismatched/missing PE orders; bowling features have zero nulls."""
    bbb_prim, _, pe_prim, _ = primary_data

    assert order_to_batting_role(1) == ROLE_TOP
    assert order_to_batting_role(3) == ROLE_TOP
    assert order_to_batting_role(4) == ROLE_MIDDLE
    assert order_to_batting_role(5) == ROLE_MIDDLE
    assert order_to_batting_role(6) == ROLE_FINISHER
    assert order_to_batting_role(12) == ROLE_FINISHER

    df_feat = add_batting_features(bbb_prim, pe_prim)
    df_feat = add_bowling_features(df_feat)

    assert set(df_feat["batting_role"].unique()) == {ROLE_TOP, ROLE_MIDDLE, ROLE_FINISHER}
    assert df_feat["is_role_mismatch"].sum() > 0
    assert df_feat["is_role_uncertain"].sum() >= df_feat["is_role_mismatch"].sum()
    assert set(df_feat["pace_or_spin"].unique()) == {"Pace", "Spin"}
    assert df_feat["bowling_style_group"].ne("Unknown").all()
    assert df_feat["bowler_pre_legal_balls_in_inn"].min() == 0
