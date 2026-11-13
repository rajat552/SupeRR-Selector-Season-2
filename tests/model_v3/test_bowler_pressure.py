"""Unit and statistical tests for bowler-side pressure index and baseline hierarchy (Model V3)."""

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
from src.model_v3.pressure_model import (
    compute_v1_pressure_index,
    compute_bowler_pressure_index,
    compute_pressure_features,
)
from src.model_v3.context_baselines import BAT_HIERARCHY_V2, add_lpo_context_baselines
from src.model_v3.impact_models import compute_player_base_metrics, score_model_a, score_model_b


@pytest.fixture(scope="module")
def dataset():
    df, matches, pe, player_lookup, match_elo = build_foundation_dataset()
    return df, matches, pe, player_lookup


def test_bowler_pressure_no_lookahead(dataset):
    """Test that bowler pressure index depends strictly on pre-delivery state with zero look-ahead."""
    df, _, _, _ = dataset
    sample = df.sample(n=50, random_state=42).copy()
    original_pi = compute_bowler_pressure_index(sample)["pressure_index_bowl"].to_numpy()

    # Mutate post-delivery outcome variables
    mutated = sample.copy()
    mutated["runs"] = 6
    mutated["total_runs"] = 6
    mutated["bowler_runs_conceded"] = 6
    mutated["is_bowler_wicket"] = True
    mutated["is_wicket"] = True
    mutated["dismissal_type"] = "bowled"
    mutated["is_dot_bat"] = False
    mutated["is_dot_bowl"] = False
    mutated["is_boundary_bat"] = True
    mutated["is_boundary_conceded"] = True

    mutated_pi = compute_bowler_pressure_index(mutated)["pressure_index_bowl"].to_numpy()
    np.testing.assert_allclose(
        original_pi,
        mutated_pi,
        rtol=1e-12,
        atol=1e-12,
        err_msg="Bowler pressure index altered by post-delivery outcomes (look-ahead detected).",
    )


def test_bowler_hp_wickets_down_share(dataset):
    """Test that the share of bowler high-pressure balls with 6+ wickets down is strictly < 15%."""
    df, _, _, _ = dataset
    hp_bowl = df[df["is_high_pressure_bowl"]]
    assert len(hp_bowl) > 0, "No bowler high-pressure balls identified."

    share_ge6 = float((hp_bowl["pre_wickets"] >= 6).mean())
    assert share_ge6 < 0.15, (
        f"Share of bowler HP deliveries with 6+ wickets down is {share_ge6:.1%}, "
        "which exceeds the required 15% threshold."
    )

    # Also check tailender share (#8+)
    if "batting_order" in hp_bowl.columns:
        share_tail = float((hp_bowl["batting_order"] >= 8).mean())
        assert share_tail < 0.10, (
            f"Share of bowler HP deliveries to batters at #8+ is {share_tail:.1%}, "
            "which exceeds 10%."
        )


def test_batting_pipeline_invariance_to_bowler_pressure(dataset):
    """Test that the batting pipeline output is unchanged when only the bowler index changes."""
    df, _, _, player_lookup = dataset

    # Batter pressure columns must match legacy V1/V2 exactly
    np.testing.assert_allclose(
        df["pressure_index_bat"].to_numpy(),
        df["pressure_index"].to_numpy(),
        rtol=1e-12,
        atol=1e-12,
    )
    np.testing.assert_allclose(
        df["pressure_weight_bat"].to_numpy(),
        df["pressure_weight"].to_numpy(),
        rtol=1e-12,
        atol=1e-12,
    )
    np.testing.assert_array_equal(
        df["is_high_pressure_bat"].to_numpy(),
        df["is_high_pressure"].to_numpy(),
    )

    # 1. Under V2 batting baseline hierarchy, batting scores match V2 exactly
    df_v2 = add_lpo_context_baselines(df, bat_hierarchy=BAT_HIERARCHY_V2)
    bat_base_v2, _ = compute_player_base_metrics(df_v2, player_lookup, role="batter")
    elig_bat_v2 = bat_base_v2[bat_base_v2["is_eligible"]].copy()
    elig_bat_v2 = score_model_a(elig_bat_v2)
    elig_bat_v2 = score_model_b(elig_bat_v2, role="batter")

    v2_top_bat_path = ROOT / "outputs" / "model_v2" / "final_top10_batters.csv"
    if v2_top_bat_path.exists():
        v2_top = pd.read_csv(v2_top_bat_path)
        v3_top_v2hier = elig_bat_v2.sort_values("model_b_score", ascending=False).head(10)
        np.testing.assert_array_equal(
            v3_top_v2hier["striker_id"].to_numpy(),
            v2_top["striker_id"].to_numpy(),
            err_msg="Batting Top 10 IDs changed when introducing bowler pressure index under V2 hierarchy.",
        )
        np.testing.assert_allclose(
            v3_top_v2hier["model_b_score"].to_numpy(),
            v2_top["pressure_score"].to_numpy(),
            rtol=1e-5,
            atol=1e-5,
            err_msg="Batting Top 10 scores changed when introducing bowler pressure index under V2 hierarchy.",
        )

    # 2. Under promoted canonical V3 hierarchy (with wickets_bucket), check core candidates
    bat_base, _ = compute_player_base_metrics(df, player_lookup, role="batter")
    elig_bat = bat_base[bat_base["is_eligible"]].copy()
    elig_bat = score_model_a(elig_bat)
    elig_bat = score_model_b(elig_bat, role="batter")
    top_bat_names = elig_bat.sort_values("model_b_score", ascending=False).head(10)["player_name"].tolist()
    assert "Tim David" in top_bat_names
    assert "Naman Dhir" in top_bat_names
    assert "Shashank Singh" in top_bat_names
    assert "Romario Shepherd" in top_bat_names

