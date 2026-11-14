"""Objective comparison and canonical selection across Models A, B, and C."""

from __future__ import annotations

from typing import Dict, Tuple
import numpy as np
import pandas as pd
from scipy.stats import spearmanr

from .context_baselines import DEFAULT_MIN_CELL_N, add_lpo_context_baselines
from .eligibility import BENCHMARK_GATE, EligibilityGate
from .impact_models import (
    compute_player_base_metrics,
    fit_model_c_and_score,
    score_model_a,
    score_model_b,
)
from .bootstrap import run_stratified_bootstrap
from .shrinkage import DEFAULT_SHRINK_K


def evaluate_models_abc(
    df: pd.DataFrame,
    player_lookup: pd.DataFrame,
    oos_validation_df: pd.DataFrame | None = None,
    gate: EligibilityGate = BENCHMARK_GATE,
    shrink_k: float = DEFAULT_SHRINK_K,
    n_boot_cmp: int = 200,
    min_cell_n: int = DEFAULT_MIN_CELL_N,
) -> Tuple[pd.DataFrame, Dict[str, pd.DataFrame], str]:
    """
    Compare Model A (Absolute Continuous Pressure Impact), Model B (Maintenance & Lift),
    and Model C (Regularized Continuous Pressure Interaction) objectively on:
      1) Walk-forward player-level OOS predictive correlation (2022-2024 -> 2025-2026)
      2) Leave-One-Season-Out (LOSO) rank stability (Spearman rho & Top-10 overlap)
      3) Stratified bootstrap stability (Top-10 inclusion & CI width)
      4) Domain fairness (finisher retention e.g. Ashutosh Sharma; elite stars e.g. Bumrah/SKY)
      5) Transparency / interpretability

    Does NOT auto-select the most complex model; returns (comparison_df, scored_by_role, selected_model).
    """
    # Split 2022-2024 vs 2025-2026 for player-level OOS HP impact correlation
    df_tr = add_lpo_context_baselines(
        df[df["season_year"] <= 2024].copy(), min_cell_n=min_cell_n
    )
    df_te = add_lpo_context_baselines(
        df[df["season_year"] >= 2025].copy(), min_cell_n=min_cell_n
    )

    # Precompute LOSO subsets once
    seasons = sorted(df["season_year"].unique().tolist())
    loso_dfs = {
        yr: add_lpo_context_baselines(df[df["season_year"] != yr].copy(), min_cell_n=min_cell_n)
        for yr in seasons
    }

    scored_by_role: Dict[str, pd.DataFrame] = {}
    rows = []

    for role, id_col in [("batter", "striker_id"), ("bowler", "bowler_id")]:
        # Full-sample scores for A, B, C
        base_full, _ = compute_player_base_metrics(
            df, player_lookup, role=role, shrink_k=shrink_k, gate=gate
        )
        elig_full = base_full[base_full["is_eligible"]].copy()
        elig_full = score_model_a(elig_full)
        elig_full = score_model_b(elig_full, role=role)
        elig_full, mc_info = fit_model_c_and_score(df, elig_full, role=role)
        scored_by_role[role] = elig_full

        # Train (2022-2024) vs Test (2025-2026) player-level HP impact prediction
        tr_gate = EligibilityGate("oos_tr", min_total_balls=150, min_hp_balls=60, min_hp_matches=5)
        base_tr, _ = compute_player_base_metrics(df_tr, player_lookup, role=role, shrink_k=shrink_k, gate=tr_gate)
        elig_tr = base_tr[base_tr["is_eligible"]].copy()
        elig_tr = score_model_a(elig_tr)
        elig_tr = score_model_b(elig_tr, role=role)
        elig_tr, _ = fit_model_c_and_score(df_tr, elig_tr, role=role)

        base_te, _ = compute_player_base_metrics(df_te, player_lookup, role=role, shrink_k=shrink_k, gate=tr_gate)
        te_eval = base_te[base_te["hp_balls"] >= 40][[id_col, "shrunk_wp_impact", "pressure_neff"]].rename(
            columns={"shrunk_wp_impact": "future_wp_impact"}
        )
        oos_join = elig_tr.merge(te_eval, on=id_col, how="inner")

        # Bootstrap comparison for A and B
        boot_a, _ = run_stratified_bootstrap(df, player_lookup, role=role, model_name="model_a", n_boot=n_boot_cmp, seed=101, gate=gate, shrink_k=shrink_k)
        boot_b, _ = run_stratified_bootstrap(df, player_lookup, role=role, model_name="model_b", n_boot=n_boot_cmp, seed=101, gate=gate, shrink_k=shrink_k)

        # Model C OOS delivery calibration check (if provided)
        mc_cal_slope = np.nan
        mc_brier_delta = np.nan
        if oos_validation_df is not None and len(oos_validation_df) > 0:
            sub_oos = oos_validation_df[
                (oos_validation_df["role"] == role)
                & (oos_validation_df["split"] == "2022-2024_to_2025-2026")
            ]
            c_int = sub_oos[sub_oos["spec"] == "Model_C_Full_Interaction"]
            c_add = sub_oos[sub_oos["spec"] == "Context_Pressure_Player"]
            if len(c_int) > 0:
                mc_cal_slope = float(c_int["evt_cal_slope"].iloc[0])
                if len(c_add) > 0:
                    mc_brier_delta = float(c_int["evt_brier"].iloc[0] - c_add["evt_brier"].iloc[0])

        # Precompute LOSO scores for A, B, C
        loso_scores = {"model_a": [], "model_b": [], "model_c": []}
        loso_overlaps = {"model_a": [], "model_b": [], "model_c": []}
        for yr, df_l in loso_dfs.items():
            b_l, _ = compute_player_base_metrics(df_l, player_lookup, role=role, shrink_k=shrink_k, gate=gate)
            e_l = b_l[b_l["is_eligible"]].copy()
            e_l = score_model_a(e_l)
            e_l = score_model_b(e_l, role=role)
            e_l, _ = fit_model_c_and_score(df_l, e_l, role=role)
            for m_key in ("model_a", "model_b", "model_c"):
                sc = f"{m_key}_score"
                top_ref = set(elig_full.sort_values(sc, ascending=False).head(10)[id_col])
                top_l = set(e_l.sort_values(sc, ascending=False).head(10)[id_col])
                m_j = elig_full[[id_col, sc]].merge(e_l[[id_col, sc]], on=id_col, suffixes=("_r", "_l"))
                rho = float(spearmanr(m_j[f"{sc}_r"], m_j[f"{sc}_l"]).statistic)
                loso_scores[m_key].append(rho)
                loso_overlaps[m_key].append(len(top_ref & top_l))

        for m_key, m_label, interp_score in [
            ("model_a", "Model A: Absolute Continuous Pressure Impact", 0.90),
            ("model_b", "Model B: Maintenance & Lift (No LP Trap / No Elite Penalty)", 0.95),
            ("model_c", "Model C: Regularized Ridge/Logit Interaction", 0.60),
        ]:
            sc = f"{m_key}_score"
            top10 = elig_full.sort_values(sc, ascending=False).head(10)
            top10_ids = set(top10[id_col])

            oos_rho = (
                float(spearmanr(oos_join[sc], oos_join["future_wp_impact"]).statistic)
                if len(oos_join) >= 5
                else np.nan
            )
            oos_pearson = (
                float(np.corrcoef(oos_join[sc], oos_join["future_wp_impact"])[0, 1])
                if len(oos_join) >= 5
                else np.nan
            )

            if m_key == "model_a":
                b_sub = boot_a[boot_a[id_col].isin(top10_ids)]
                boot_med_ci = float(b_sub["boot_ci_width"].median())
                boot_top10_freq = float(b_sub["top10_inclusion_frequency"].mean())
            elif m_key == "model_b":
                b_sub = boot_b[boot_b[id_col].isin(top10_ids)]
                boot_med_ci = float(b_sub["boot_ci_width"].median())
                boot_top10_freq = float(b_sub["top10_inclusion_frequency"].mean())
            else:
                # Model C uses parametric partial-pooled shrink; approximate stability via LOSO
                boot_med_ci = np.nan
                boot_top10_freq = np.nan

            # Diagnostic checks on benchmark players
            ash_in_pool = bool((elig_full["player_name"] == "Ashutosh Sharma").any()) if role == "batter" else True
            if role == "batter":
                sky = elig_full[elig_full["player_name"] == "Suryakumar Yadav"]
                star_rank = int((elig_full[sc] > float(sky[sc].iloc[0])).sum()) + 1 if len(sky) > 0 else np.nan
                star_name = "Suryakumar Yadav"
            else:
                bum = elig_full[elig_full["player_name"] == "Jasprit Bumrah"]
                star_rank = int((elig_full[sc] > float(bum[sc].iloc[0])).sum()) + 1 if len(bum) > 0 else np.nan
                star_name = "Jasprit Bumrah"

            rows.append(
                {
                    "role": role,
                    "model_key": m_key,
                    "model_label": m_label,
                    "n_eligible": int(len(elig_full)),
                    "oos_player_spearman": oos_rho,
                    "oos_player_pearson": oos_pearson,
                    "oos_n_common_players": int(len(oos_join)),
                    "loso_mean_spearman": float(np.mean(loso_scores[m_key])),
                    "loso_mean_top10_overlap": float(np.mean(loso_overlaps[m_key])),
                    "boot_top10_median_ci_width": boot_med_ci,
                    "boot_top10_mean_inclusion": boot_top10_freq,
                    "model_c_oos_cal_slope": mc_cal_slope if m_key == "model_c" else np.nan,
                    "model_c_oos_brier_delta": mc_brier_delta if m_key == "model_c" else np.nan,
                    "ashutosh_retained": ash_in_pool,
                    "benchmark_star_name": star_name,
                    "benchmark_star_rank": star_rank,
                    "interpretability_score": interp_score,
                    "top10_players": " | ".join(top10["player_name"].tolist()),
                }
            )

    cmp_df = pd.DataFrame(rows)

    # Objective composite selection score across predictive validity, LOSO stability,
    # calibration/parsimony, and interpretability
    sel_scores = []
    for _, r in cmp_df.iterrows():
        pred_term = r["oos_player_spearman"] if pd.notna(r["oos_player_spearman"]) else 0.0
        loso_term = r["loso_mean_spearman"] if pd.notna(r["loso_mean_spearman"]) else 0.0
        # Penalize Model C if OOS interaction worsens logistic calibration (< 0.80) or Brier (> 0)
        cal_penalty = 0.0
        if r["model_key"] == "model_c" and pd.notna(r["model_c_oos_cal_slope"]):
            if r["model_c_oos_cal_slope"] < 0.80:
                cal_penalty += 0.15
            if pd.notna(r["model_c_oos_brier_delta"]) and r["model_c_oos_brier_delta"] > 0.0:
                cal_penalty += 0.05
        # Small bonus for explicit maintenance + lift separation over pure absolute impact
        domain_bonus = 0.05 if r["model_key"] == "model_b" else 0.0
        sel = 0.35 * pred_term + 0.35 * loso_term + 0.30 * r["interpretability_score"] + domain_bonus - cal_penalty
        sel_scores.append(sel)
    cmp_df["objective_selection_score"] = sel_scores

    mean_by_model = cmp_df.groupby("model_key")["objective_selection_score"].mean()
    selected_model = str(mean_by_model.idxmax())
    cmp_df["is_selected_canonical"] = cmp_df["model_key"] == selected_model
    return cmp_df, scored_by_role, selected_model
