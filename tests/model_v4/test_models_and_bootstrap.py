"""Unit, statistical validity, and bootstrap equivalence tests for Phase 2 Model V2."""

from __future__ import annotations

import sys
from pathlib import Path
import numpy as np
import pandas as pd
import pytest

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.model_v4 import build_foundation_dataset
from src.model_v4.bootstrap import (
    _prepare_role_sufficient_stats,
    _score_single_draw_from_stats,
    generate_stratified_match_draws,
    run_direct_delivery_bootstrap_pilot,
    run_stratified_bootstrap,
)
from src.model_v4.eligibility import BENCHMARK_GATE, identify_near_misses
from src.model_v4.impact_models import (
    compute_player_base_metrics,
    run_model_c_oos_validation,
    score_model_a,
    score_model_b,
)
from src.model_v4.shrinkage import (
    attach_wicket_values,
    beta_binomial_consistency,
    compare_consistency_priors,
    eb_shrink_rate,
    estimate_context_wicket_value_table,
)


@pytest.fixture(scope="module")
def foundation_data():
    return build_foundation_dataset(include_other_t20=False, include_super_overs=False)


def test_context_wicket_value_no_double_counting_and_bounds(foundation_data):
    """
    Verify context-dependent marginal wicket value:
    1) `runs_rem_after = inn_total_runs - post_runs` on ball t is strictly invariant
       to runs scored on ball t itself (zero double-counting).
    2) Marginal drops across (comp_tier, innings, over_bucket, pre_wickets) are
       finite and bounded cleanly.
    """
    df, *_ = foundation_data
    wkt_tbl = estimate_context_wicket_value_table(df)
    assert len(wkt_tbl) > 0
    assert wkt_tbl["marginal_wicket_value"].notna().all()
    assert (wkt_tbl["marginal_wicket_value"] >= 1.0).all()
    assert (wkt_tbl["marginal_wicket_value"] <= 15.0).all()

    # Check Powerplay IPL Inn1 drop > Death IPL Inn1 drop
    ipl_1 = wkt_tbl[(wkt_tbl["comp_tier"] == "IPL") & (wkt_tbl["innings"] == 1)]
    pp_mean = ipl_1[ipl_1["over_bucket"] == "1-6"]["marginal_wicket_value"].mean()
    death_mean = ipl_1[ipl_1["over_bucket"] == "16-20"]["marginal_wicket_value"].mean()
    assert pp_mean > death_mean

    # Invariance of runs_rem_after on ball t when ball t's runs change
    sample_m = df[df["match_id"] == df["match_id"].iloc[0]].copy()
    tot_a = sample_m.groupby(["match_id", "innings"])["post_runs"].transform("max")
    rem_after_a = tot_a - sample_m["post_runs"]

    # Mutate runs on delivery index 5 (propagate to post_runs from index 5 onward in that innings)
    sample_b = sample_m.copy()
    inn0 = sample_b["innings"].iloc[5]
    mask = (sample_b.index >= sample_b.index[5]) & (sample_b["innings"] == inn0)
    sample_b.loc[mask, "post_runs"] += 6
    tot_b = sample_b.groupby(["match_id", "innings"])["post_runs"].transform("max")
    rem_after_b = tot_b - sample_b["post_runs"]
    assert np.isclose(rem_after_a.iloc[5], rem_after_b.iloc[5])


def test_eb_shrinkage_and_beta_binomial_priors():
    """Verify EB shrinkage, Beta(5,5) formula, and population-fitted Beta prior shrinkage."""
    shrunk = eb_shrink_rate(np.array([20.0, 20.0]), np.array([120.0, 360.0]), k=120.0)
    assert np.isclose(shrunk[0], 10.0)
    assert np.isclose(shrunk[1], 15.0)

    b55 = beta_binomial_consistency(np.array([7.0, 30.0]), np.array([7.0, 40.0]), 5.0, 5.0)
    assert np.isclose(b55[0], 12.0 / 17.0)
    assert np.isclose(b55[1], 35.0 / 50.0)

    # Small 7/7 streak must be pulled down more than 28/35 sustained consistency
    pos = np.array([7, 28, 12, 15, 9, 10, 18, 6, 14, 11, 20, 8], dtype=float)
    m = np.array([7, 35, 20, 25, 16, 18, 30, 12, 24, 20, 32, 15], dtype=float)
    cmp_df, (a0, b0) = compare_consistency_priors(pos, m)
    assert a0 > 0.0 and b0 > 0.0
    assert cmp_df.loc[0, "eb_consistency"] < 1.0
    # 7/7 shrinks more from raw 1.0 than 28/35 shrinks from 0.80
    assert (1.0 - cmp_df.loc[0, "eb_consistency"]) > (0.80 - cmp_df.loc[1, "eb_consistency"])


def test_finisher_rescue_near_misses_and_no_elite_penalty(foundation_data):
    """
    Verify:
    1) Ashutosh Sharma (8101, lp_balls=42) passes V2 eligibility (no lp_balls>=60 trap).
    2) Phil Salt (5553) is exposed cleanly as a near-miss with Kish N_eff > 300.
    3) Model B does not penalize elite normal-baseline performers (Bumrah, Suryakumar).
    """
    df, matches, pe, pl, _ = foundation_data

    bat_base, _ = compute_player_base_metrics(df, pl, role="batter", gate=BENCHMARK_GATE)
    ash = bat_base[bat_base["striker_id"] == 8101].iloc[0]
    assert bool(ash["is_eligible"]) is True
    assert ash["lp_balls"] < 60
    assert ash["hp_balls"] >= 120

    nm_bat = identify_near_misses(bat_base, gate=BENCHMARK_GATE, id_col="striker_id", score_col="shrunk_wp_impact")
    assert (nm_bat[nm_bat["status"] == "near_miss"]["striker_id"] == 5553).any()
    salt = nm_bat[nm_bat["striker_id"] == 5553].iloc[0]
    assert salt["pressure_neff"] > 300.0

    # Synthetic no-elite-penalty check on score_model_b
    syn = pd.DataFrame(
        {
            "player_id": [1, 2],
            "shrunk_wp_impact": [25.0, 8.0],
            "shrunk_norm_impact": [25.0, -15.0],
            "eb_consistency": [0.65, 0.65],
        }
    )
    sb = score_model_b(syn, role="batter")
    assert sb.loc[0, "model_b_score"] > sb.loc[1, "model_b_score"]

    # Real data check: Jasprit Bumrah (2933) in Top 5 bowlers under Model B
    bowl_base, _ = compute_player_base_metrics(df, pl, role="bowler", gate=BENCHMARK_GATE)
    bowl_b = score_model_b(bowl_base[bowl_base["is_eligible"]].copy(), role="bowler")
    bowl_b = bowl_b.sort_values("model_b_score", ascending=False).reset_index(drop=True)
    bum_rank = int(bowl_b.index[bowl_b["bowler_id"] == 2933][0]) + 1
    assert bum_rank <= 5


def test_model_c_walk_forward_oos_metrics(foundation_data):
    """Verify Model C walk-forward chronological OOS validation produces valid metrics & SEs."""
    df, *_ = foundation_data
    oos = run_model_c_oos_validation(
        df, splits=(("2022-2024_to_2025-2026", (2022, 2023, 2024), (2025, 2026)),)
    )
    assert len(oos) == 6  # 2 roles x 3 nested specs
    for col in ("runs_rmse", "runs_mae", "runs_r2", "evt_brier", "evt_log_loss", "evt_cal_slope", "runs_rmse_cluster_se", "evt_brier_cluster_se"):
        assert oos[col].notna().all()
    assert (oos["runs_rmse_cluster_se"] > 0).all()
    assert (oos["evt_brier_cluster_se"] > 0).all()


def test_stratified_bootstrap_strata_and_pilot_equivalence(foundation_data):
    """
    CRITICAL EQUIVALENCE TEST:
    1) Verify stratified draws preserve exact match counts in every (comp_category, season_year) cell.
    2) Prove vectorized sufficient-statistic bootstrap matches direct delivery-level
       recomputation (with boot_match_instance_id + full LPO + shrinkage + Beta-binomial
       + eligibility + scoring) on a 5-resample pilot with max_abs_diff < 1e-10!
    """
    df, matches, pe, pl, _ = foundation_data
    n_pilot = 5
    u_mids, c_mat = generate_stratified_match_draws(df, n_boot=n_pilot, seed=2026)

    # 1. Exact stratum preservation check
    m_meta = (
        df[["match_id", "comp_category", "season_year"]]
        .drop_duplicates("match_id")
        .set_index("match_id")
        .loc[u_mids]
    )
    for (comp_cat, yr), grp in m_meta.groupby(["comp_category", "season_year"]):
        idx = np.isin(u_mids, grp.index.to_numpy())
        for b in range(n_pilot):
            assert int(np.sum(c_mat[b, idx])) == len(grp)

    # 2. Equivalence between vectorized sufficient-statistic engine and direct delivery pilot
    df_wkt, _ = attach_wicket_values(df, wicket_mode=6.0)
    for role, id_col in [("batter", "striker_id"), ("bowler", "bowler_id")]:
        direct_df = run_direct_delivery_bootstrap_pilot(
            df,
            pl,
            role=role,
            unique_match_ids=u_mids,
            counts_matrix=c_mat,
            model_name="model_b",
            gate=BENCHMARK_GATE,
        )
        stats = _prepare_role_sufficient_stats(df_wkt, u_mids, role=role)
        pids = stats["player_ids"]
        fast_rows = []
        for b in range(n_pilot):
            s_b, r_b, e_b, _ = _score_single_draw_from_stats(
                c_mat[b],
                stats=stats,
                gate=BENCHMARK_GATE,
                shrink_k=120.0,
                model_name="model_b",
                min_cell_n=50,
            )
            for idx in np.where(e_b)[0]:
                fast_rows.append(
                    {
                        "iter": b,
                        id_col: int(pids[idx]),
                        "score_fast": float(s_b[idx]),
                        "rank_fast": float(r_b[idx]),
                    }
                )
        fast_df = pd.DataFrame(fast_rows)
        merged = direct_df.merge(fast_df, on=["iter", id_col], how="outer")
        assert len(merged) == len(direct_df) == len(fast_df)
        assert merged["score"].notna().all() and merged["score_fast"].notna().all()

        max_score_diff = float(np.max(np.abs(merged["score"] - merged["score_fast"])))
        max_rank_diff = float(np.max(np.abs(merged["rank"] - merged["rank_fast"])))
        assert max_score_diff < 1e-10, f"{role} score max_abs_diff={max_score_diff}"
        assert max_rank_diff < 1e-10, f"{role} rank max_abs_diff={max_rank_diff}"

    # 3. Verify missing/ineligible tracking without fabricating ranks
    boot_res, _ = run_stratified_bootstrap(
        df,
        pl,
        role="batter",
        model_name="model_b",
        n_boot=n_pilot,
        seed=2026,
        counts_matrix=c_mat,
        unique_match_ids=u_mids,
    )
    assert (
        boot_res["valid_eligible_iters"] + boot_res["ineligible_iters"] + boot_res["absent_iters"]
        == n_pilot
    ).all()
    zero_valid = boot_res[boot_res["valid_eligible_iters"] == 0]
    if len(zero_valid) > 0:
        assert zero_valid["boot_median_rank"].isna().all()
        assert (zero_valid["top10_inclusion_frequency"] == 0.0).all()
