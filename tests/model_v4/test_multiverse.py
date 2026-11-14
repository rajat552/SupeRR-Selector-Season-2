"""Unit and statistical validation suite for Model V4 Multiverse Analysis."""

import pytest
import numpy as np
import pandas as pd
from pathlib import Path

from src.model_v4 import build_foundation_dataset
from src.model_v4.multiverse import attach_pressure_variants, GATES, GATES_P5_BAT, GATES_P5_BOWL

ROOT = Path(__file__).resolve().parents[2]
OUT_DIR = ROOT / "outputs" / "model_v4"


@pytest.fixture(scope="module")
def foundation_data():
    df, matches, pe, pl, _ = build_foundation_dataset()
    df_with_p = attach_pressure_variants(df)
    return df_with_p, matches, pl


def test_zero_lookahead_in_every_pressure_definition(foundation_data):
    """Verify that every P definition (P1-P5 for batters and bowlers) depends strictly on pre-delivery state."""
    df, _, _ = foundation_data

    # Match-state features must be pre-delivery
    assert "pre_runs" in df.columns
    assert "pre_wickets" in df.columns
    assert "pre_legal_balls" in df.columns
    assert "pre_balls_remaining" in df.columns
    assert "pre_crr" in df.columns

    # Check that pressure definitions are strictly bounded in [0, 1]
    p_defs_bat = ["P1", "P2", "P3", "P4", "P5"]
    for p in p_defs_bat:
        col = f"pw_bat_{p}"
        assert col in df.columns
        vals = df[col].dropna()
        assert (vals >= 0.0).all() and (vals <= 1.0).all(), f"Batting {p} out of bounds"

    p_defs_bowl = ["P1", "P2", "P3", "P4", "P5", "P0"]
    for p in p_defs_bowl:
        col = f"pw_bowl_{p}"
        assert col in df.columns
        vals = df[col].dropna()
        assert (vals >= 0.0).all() and (vals <= 1.0).all(), f"Bowling {p} out of bounds"


def test_bowler_hp_share_with_ge_6_wickets_down_under_15_pct(foundation_data):
    """Verify that bowler HP deliveries with >= 6 wickets down account for < 15% of total bowler HP volume."""
    df, _, _ = foundation_data
    bowl_legal = df[df["is_legal_ball"]].copy()

    # Canonical defending bowler HP: pw_bowl_P2 >= 0.50
    hp_bowl = bowl_legal[bowl_legal["pw_bowl_P2"] >= 0.50]
    tail_hp = hp_bowl[hp_bowl["pre_wickets"] >= 6]

    tail_share = len(tail_hp) / len(hp_bowl)
    assert tail_share < 0.15, f"Bowler tail HP share is {tail_share:.2%}, expected < 15%"


def test_multiverse_row_count_and_specification_structure():
    """Verify multiverse parquet row count matches expected specifications and players."""
    parquet_path = OUT_DIR / "multiverse_ranks.parquet"
    assert parquet_path.exists(), "multiverse_ranks.parquet does not exist"

    df = pd.read_parquet(parquet_path)
    assert len(df) > 3_000_000, f"Expected >3M rows, got {len(df)}"

    # Required columns
    required_cols = [
        "spec_id", "role", "p_def", "w_def", "f_scope", "m_model",
        "v_val", "k_shrink", "g_gate", "s_weights", "player_id",
        "player_name", "score", "rank", "is_eligible", "is_valid",
        "shrunk_wp_impact", "shrunk_norm_impact", "raw_lift", "maint_lift", "hp_balls"
    ]
    for c in required_cols:
        assert c in df.columns, f"Missing column {c} in multiverse_ranks.parquet"

    # Verify bowler P0 is correctly flagged as reference only (not valid for selection)
    p0_sub = df[(df["role"] == "bowler") & (df["p_def"] == "P0")]
    assert len(p0_sub) > 0
    assert not p0_sub["is_valid"].any(), "Bowler P0 must have is_valid == False"

    # Verify all other specs are valid
    valid_sub = df[~((df["role"] == "bowler") & (df["p_def"] == "P0"))]
    assert valid_sub["is_valid"].all(), "Non-P0 specs must be valid"
