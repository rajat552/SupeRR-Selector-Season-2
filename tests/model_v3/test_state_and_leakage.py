"""Unit and leakage tests for pre-delivery state, Elo, continuous PI weights, and LPO baselines."""

from __future__ import annotations

import sys
from pathlib import Path
import numpy as np
import pandas as pd
import pytest

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.model_v3 import build_foundation_dataset
from src.model_v3.cricket_accounting import apply_cricket_accounting
from src.model_v3.state_builder import build_match_state
from src.model_v3.opponent_strength import (
    DEFAULT_BASE_ELO,
    attach_opponent_elo,
    compute_pre_match_elo,
)
from src.model_v3.pressure_model import (
    compute_pressure_features,
    compute_pressure_weights,
    kish_effective_sample_size,
)
from src.model_v3.context_baselines import add_lpo_context_baselines
from src.pressure import compute_pressure_index as v1_compute_pressure_index
from src.state_builder import build_match_state as v1_build_match_state
from src.data_loader import load_clean_dataset as v1_load_clean_dataset


@pytest.fixture(scope="module")
def foundation_data():
    return build_foundation_dataset(include_other_t20=False, include_super_overs=False)


def test_zero_lookahead_pre_delivery_state_and_revised_balls():
    """
    Verify strict zero look-ahead pre-delivery state:
    - Delivery t uses only 1..t-1.
    - Changing outcome of ball t does not alter pre_* on ball t (only t+1).
    - first_inn_revised_overs / second_inn_revised_overs are treated as BALLS (e.g. 114.0).
    - revised_target overrides inn1_total_runs + 1.
    """
    base_rows = [
        # Innings 1: 114-ball innings, 3 balls
        {"match_id": 100, "innings": 1, "overid": 1, "over_ball_num": 1, "batting_team_id": 1, "bowling_team_id": 2, "striker_id": 11, "bowler_id": 21, "runs": 4, "extras_type": np.nan, "extras1_runs": 0, "extras_2_runs": 0, "is_wicket": False, "dismissal_type": np.nan, "dismissed_player_id": np.nan, "is_four": 1, "is_six": 0, "first_inn_revised_overs": 114.0, "second_inn_revised_overs": 60.0, "revised_target": 95.0},
        {"match_id": 100, "innings": 1, "overid": 1, "over_ball_num": 2, "batting_team_id": 1, "bowling_team_id": 2, "striker_id": 11, "bowler_id": 21, "runs": 0, "extras_type": "wide", "extras1_runs": 1, "extras_2_runs": 0, "is_wicket": False, "dismissal_type": np.nan, "dismissed_player_id": np.nan, "is_four": 0, "is_six": 0, "first_inn_revised_overs": 114.0, "second_inn_revised_overs": 60.0, "revised_target": 95.0},
        {"match_id": 100, "innings": 1, "overid": 1, "over_ball_num": 3, "batting_team_id": 1, "bowling_team_id": 2, "striker_id": 11, "bowler_id": 21, "runs": 1, "extras_type": np.nan, "extras1_runs": 0, "extras_2_runs": 0, "is_wicket": True, "dismissal_type": "RunOut", "dismissed_player_id": 12, "is_four": 0, "is_six": 0, "first_inn_revised_overs": 114.0, "second_inn_revised_overs": 60.0, "revised_target": 95.0},
        # Innings 2: 60-ball chase, revised_target = 95
        {"match_id": 100, "innings": 2, "overid": 1, "over_ball_num": 1, "batting_team_id": 2, "bowling_team_id": 1, "striker_id": 31, "bowler_id": 41, "runs": 6, "extras_type": np.nan, "extras1_runs": 0, "extras_2_runs": 0, "is_wicket": False, "dismissal_type": np.nan, "dismissed_player_id": np.nan, "is_four": 0, "is_six": 1, "first_inn_revised_overs": 114.0, "second_inn_revised_overs": 60.0, "revised_target": 95.0},
        {"match_id": 100, "innings": 2, "overid": 1, "over_ball_num": 2, "batting_team_id": 2, "bowling_team_id": 1, "striker_id": 31, "bowler_id": 41, "runs": 0, "extras_type": np.nan, "extras1_runs": 0, "extras_2_runs": 0, "is_wicket": False, "dismissal_type": np.nan, "dismissed_player_id": np.nan, "is_four": 0, "is_six": 0, "first_inn_revised_overs": 114.0, "second_inn_revised_overs": 60.0, "revised_target": 95.0},
    ]
    df_a = build_match_state(apply_cricket_accounting(pd.DataFrame(base_rows)))

    # Mutate outcome of delivery index 2 (inn 1 ball 3) and delivery index 4 (inn 2 ball 2)
    mut_rows = [dict(r) for r in base_rows]
    mut_rows[2]["runs"] = 6
    mut_rows[4]["is_wicket"] = True
    df_b = build_match_state(apply_cricket_accounting(pd.DataFrame(mut_rows)))

    # Pre-state on delivery 0, 1, 2 in inn1 must be identical before delivery 2
    assert df_a.loc[0, "pre_runs"] == 0 and df_a.loc[0, "pre_legal_balls"] == 0
    assert df_a.loc[1, "pre_runs"] == 4 and df_a.loc[1, "pre_legal_balls"] == 1
    assert df_a.loc[2, "pre_runs"] == 5 and df_a.loc[2, "pre_legal_balls"] == 1  # wide did not advance legal balls
    assert df_a.loc[2, "pre_runs"] == df_b.loc[2, "pre_runs"]
    assert df_a.loc[4, "pre_wickets"] == df_b.loc[4, "pre_wickets"]

    # Revised overs treated directly as balls
    assert df_a.loc[0, "inn_max_balls"] == 114.0
    assert df_a.loc[0, "pre_balls_remaining"] == 114.0
    assert df_a.loc[3, "inn_max_balls"] == 60.0
    assert df_a.loc[3, "target"] == 95.0
    assert df_a.loc[3, "runs_needed"] == 95.0
    assert df_a.loc[4, "runs_needed"] == 89.0
    assert df_a.loc[4, "pre_balls_remaining"] == 59.0
    assert np.isclose(df_a.loc[4, "pre_rrr"], 6.0 * 89.0 / 59.0)


def test_elo_separation_and_strict_temporal_order():
    """
    Verify Elo ratings:
    1. IPL and T20I are completely isolated.
    2. Same-date matches NEVER see each other's outcomes (strict match_date < current_match_date).
    3. Mutating a future match's winner never affects earlier matches' pre-match Elos.
    4. Abandoned/No Result matches produce 0 Elo change; Tied without winner gives 0.5 score.
    """
    matches = pd.DataFrame(
        [
            {"match_id": 1, "comp_category": "IPL", "match_date": "2024-04-01", "match_number": 1, "home_team_id": 1, "away_team_id": 2, "win_team_id": 1, "result": "Team 1 Won"},
            {"match_id": 2, "comp_category": "IPL", "match_date": "2024-04-01", "match_number": 2, "home_team_id": 1, "away_team_id": 3, "win_team_id": 3, "result": "Team 3 Won"},
            {"match_id": 3, "comp_category": "IPL", "match_date": "2024-04-02", "match_number": 3, "home_team_id": 1, "away_team_id": 2, "win_team_id": np.nan, "result": "No Result"},
            {"match_id": 4, "comp_category": "IPL", "match_date": "2024-04-03", "match_number": 4, "home_team_id": 1, "away_team_id": 2, "win_team_id": 2, "result": "Team 2 Won"},
            # Same team_id=1 playing in T20I must start fresh at DEFAULT_BASE_ELO
            {"match_id": 5, "comp_category": "T20I", "match_date": "2024-04-05", "match_number": 1, "home_team_id": 1, "away_team_id": 9, "win_team_id": 1, "result": "Team 1 Won"},
        ]
    )
    elo = compute_pre_match_elo(matches, base_elo=1500.0, k_factor=24.0)

    # Both same-day IPL matches on 2024-04-01 must see exact base_elo=1500.0 for team 1
    m1 = elo[elo["match_id"] == 1].iloc[0]
    m2 = elo[elo["match_id"] == 2].iloc[0]
    assert m1["home_pre_elo"] == 1500.0 and m1["away_pre_elo"] == 1500.0
    assert m2["home_pre_elo"] == 1500.0 and m2["away_pre_elo"] == 1500.0

    # Match 3 (No Result) should leave Match 4 pre-match Elos identical to Match 3 pre-match Elos
    m3 = elo[elo["match_id"] == 3].iloc[0]
    m4 = elo[elo["match_id"] == 4].iloc[0]
    assert np.isclose(m3["home_pre_elo"], m4["home_pre_elo"])
    assert np.isclose(m3["away_pre_elo"], m4["away_pre_elo"])

    # T20I isolation: team 1 starts at 1500.0 in T20I despite IPL history
    m5 = elo[elo["match_id"] == 5].iloc[0]
    assert m5["home_pre_elo"] == DEFAULT_BASE_ELO

    # Future-outcome invariance: flipping match 4 winner cannot alter matches 1, 2, 3
    matches_flip = matches.copy()
    matches_flip.loc[matches_flip["match_id"] == 4, "win_team_id"] = 1
    elo_flip = compute_pre_match_elo(matches_flip, base_elo=1500.0, k_factor=24.0)
    pd.testing.assert_frame_equal(
        elo[elo["match_id"].isin([1, 2, 3])].reset_index(drop=True),
        elo_flip[elo_flip["match_id"].isin([1, 2, 3])].reset_index(drop=True),
    )


def test_continuous_pressure_weights_and_kish_neff():
    """
    Verify continuous pressure weights w_t in [0, 1], zero discarded intermediate band,
    and analytical properties of Kish effective sample size.
    """
    pi = np.array([0.0, 0.25, 0.35, 0.425, 0.50, 0.75, 1.0])
    w = compute_pressure_weights(pi, mode="sigmoid", center=0.425, scale=0.08)

    assert np.all((w >= 0.0) & (w <= 1.0))
    assert np.all(np.diff(w) > 0.0)
    assert np.isclose(w[3], 0.5)

    # Kish N_eff: equal weights -> N_eff == N
    assert np.isclose(kish_effective_sample_size(np.ones(10)), 10.0)
    assert np.isclose(kish_effective_sample_size(np.full(10, 0.3)), 10.0)
    # Single dominant weight + zeros -> N_eff == 1
    assert np.isclose(kish_effective_sample_size(np.array([1.0, 0.0, 0.0, 0.0])), 1.0)
    # Empty / all-zero -> 0.0
    assert kish_effective_sample_size(np.array([])) == 0.0
    assert kish_effective_sample_size(np.zeros(5)) == 0.0
    # General: 0 < N_eff <= N
    neff = kish_effective_sample_size(w)
    assert 0.0 < neff <= len(w)


def test_lpo_context_baselines_no_self_leakage_and_fallback():
    """
    Verify Leave-Player-Out (LPO) strictly excludes player i's own deliveries and falls
    back to parent cell when (n_cell - n_{i,cell}) < 50.
    """
    rows = []
    # Cell A (IPL, 2024, Powerplay, Top 1-3, High):
    # - Player 1 has 20 balls scoring 6 runs each (6.0 rpb)
    # - Player 2 has 60 balls scoring 1 run each (1.0 rpb)
    # LPO for Player 1 in Cell A: n_{-1} = 60 >= 50 -> exact 1.0 rpb (zero influence from Player 1's 6.0 rpb!)
    # LPO for Player 2 in Cell A: n_{-2} = 20 < 50 -> MUST fall back to Level 1 (drop opp_tier_bat)!
    for _ in range(20):
        rows.append({"comp_tier": "IPL", "season_year": 2024, "phase": "Powerplay", "batting_role": "Top 1-3", "opp_tier_bat": "High", "pace_or_spin": "Pace", "opp_tier_bowl": "High", "striker_id": 1, "bowler_id": 101, "runs": 6, "bowler_runs_conceded": 6, "is_wide": False, "is_noball": False, "is_legal_ball": True, "is_batter_ball_faced": True, "is_striker_dismissed": False, "is_bowler_wicket": False, "is_dot_bat": False, "is_boundary_bat": True, "is_dot_bowl": False, "is_boundary_conceded": True})
    for _ in range(60):
        rows.append({"comp_tier": "IPL", "season_year": 2024, "phase": "Powerplay", "batting_role": "Top 1-3", "opp_tier_bat": "High", "pace_or_spin": "Pace", "opp_tier_bowl": "High", "striker_id": 2, "bowler_id": 102, "runs": 1, "bowler_runs_conceded": 1, "is_wide": False, "is_noball": False, "is_legal_ball": True, "is_batter_ball_faced": True, "is_striker_dismissed": False, "is_bowler_wicket": False, "is_dot_bat": False, "is_boundary_bat": False, "is_dot_bowl": False, "is_boundary_conceded": False})
    # Cell B (same comp_tier, season_year, phase, batting_role, but opp_tier_bat = Low):
    # - Player 3 has 50 balls scoring 0 runs each -> lifts Level 1 LPO count for Player 2 to 20 + 50 = 70 >= 50!
    for _ in range(50):
        rows.append({"comp_tier": "IPL", "season_year": 2024, "phase": "Powerplay", "batting_role": "Top 1-3", "opp_tier_bat": "Low", "pace_or_spin": "Spin", "opp_tier_bowl": "Low", "striker_id": 3, "bowler_id": 103, "runs": 0, "bowler_runs_conceded": 0, "is_wide": False, "is_noball": False, "is_legal_ball": True, "is_batter_ball_faced": True, "is_striker_dismissed": False, "is_bowler_wicket": False, "is_dot_bat": True, "is_boundary_bat": False, "is_dot_bowl": True, "is_boundary_conceded": False})

    df = pd.DataFrame(rows)
    res = add_lpo_context_baselines(df, min_cell_n=50)

    p1 = res[res["striker_id"] == 1].iloc[0]
    assert p1["ctx_bat_level"] == 0
    assert p1["ctx_bat_lpo_n"] == 60.0
    assert np.isclose(p1["ctx_bat_rpb"], 1.0)

    p2 = res[res["striker_id"] == 2].iloc[0]
    # In V3, Level 0 has wickets_bucket + opp_tier_bat; Level 1 drops wickets_bucket but keeps opp_tier_bat (count=20 < 50);
    # Level 2 drops opp_tier_bat, merging Cell A and Cell B (20 + 50 = 70 >= 50).
    assert p2["ctx_bat_level"] == 2
    assert p2["ctx_bat_lpo_n"] == 70.0  # 20 from player 1 + 50 from player 3
    assert np.isclose(p2["ctx_bat_rpb"], (20 * 6.0 + 50 * 0.0) / 70.0)

    # Bowler 101 has 20 balls; LPO in Level 0 has bowler 102 (60 balls) >= 50 -> exact 1.0 rpb
    b101 = res[res["bowler_id"] == 101].iloc[0]
    assert b101["ctx_bowl_level"] == 0
    assert np.isclose(b101["ctx_bowl_rpb"], 1.0)


def test_full_foundation_pipeline_on_raw_data(foundation_data):
    """End-to-end verification on real 837-match primary dataset + V1 PI benchmark match."""
    df, matches, pe, player_lookup, match_elo = foundation_data

    assert len(df) == 193_988
    assert df["match_id"].nunique() == 837
    assert len(match_elo) == 837

    # Zero NaNs in critical V2 foundation columns
    required_cols = [
        "pre_runs",
        "pre_wickets",
        "pre_legal_balls",
        "pre_balls_remaining",
        "pre_crr",
        "phase",
        "pre_match_opp_elo",
        "pre_match_opp_elo_bat",
        "pre_match_opp_elo_bowl",
        "opp_tier_bat",
        "opp_tier_bowl",
        "pressure_index",
        "pressure_weight",
        "normal_weight",
        "batting_role",
        "pace_or_spin",
        "bowling_type",
        "ctx_bat_rpb",
        "ctx_bat_out_prob",
        "ctx_bowl_rpb",
        "ctx_bowl_wkt_prob",
    ]
    for col in required_cols:
        assert col in df.columns, f"Missing column {col}"
        assert df[col].isna().sum() == 0, f"Unexpected NaNs in {col}"

    # Every innings starts at strict 0 pre-state
    first_balls = df.groupby(["match_id", "innings"]).first()
    assert (first_balls["pre_runs"] == 0).all()
    assert (first_balls["pre_wickets"] == 0).all()
    assert (first_balls["pre_legal_balls"] == 0).all()

    # All deliveries get continuous pressure weights in [0, 1] without discarding intermediate band
    assert (df["pressure_weight"] >= 0.0).all() and (df["pressure_weight"] <= 1.0).all()
    assert df["is_intermediate_pressure"].sum() == 26_870

    # V1 PI_t benchmark: must match V1 src/pressure.py to machine precision
    bbb_v1, _, _, _ = v1_load_clean_dataset()
    df_v1 = v1_compute_pressure_index(v1_build_match_state(bbb_v1))
    assert np.allclose(df["pressure_index"].to_numpy(), df_v1["pressure_index"].to_numpy(), atol=1e-12)

    # LPO min_cell_n=50 invariant: whenever level < 5 (non-global), lpo_n >= 50
    non_global_bat = df[df["ctx_bat_level"] < 5]
    assert (non_global_bat["ctx_bat_lpo_n"] >= 50).all()
    non_global_bowl = df[df["ctx_bowl_level"] < 5]
    assert (non_global_bowl["ctx_bowl_lpo_n"] >= 50).all()
