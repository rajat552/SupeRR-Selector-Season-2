"""Stratified match-cluster bootstrap (1,000 resamples) with full LPO/shrinkage recomputation."""

from __future__ import annotations

import time
from typing import Dict, List, Sequence, Tuple
import numpy as np
import pandas as pd
from scipy import sparse

from .context_baselines import BAT_HIERARCHY, BOWL_HIERARCHY, DEFAULT_MIN_CELL_N, add_lpo_context_baselines
from .eligibility import BENCHMARK_GATE, EligibilityGate
from .impact_models import compute_player_base_metrics, score_model_a, score_model_b, zscore
from .shrinkage import DEFAULT_SHRINK_K, attach_wicket_values, beta_binomial_consistency, eb_shrink_rate, fit_empirical_beta_prior


def generate_stratified_match_draws(
    df: pd.DataFrame,
    n_boot: int = 1000,
    seed: int = 42,
) -> Tuple[np.ndarray, np.ndarray]:
    """
    Generate `n_boot` stratified match-cluster bootstrap multiplicity matrices.
    Stratifies strictly by (comp_category, season_year), preserving exact match
    counts per IPL/T20I season cell.

    Returns:
        unique_match_ids: sorted array of shape (M,)
        counts_matrix: integer array of shape (n_boot, M) with row sums == M
    """
    m_meta = (
        df[["match_id", "comp_category", "season_year"]]
        .drop_duplicates(subset=["match_id"])
        .sort_values("match_id")
        .reset_index(drop=True)
    )
    unique_match_ids = m_meta["match_id"].to_numpy(dtype="int64")
    n_matches = len(unique_match_ids)

    strata_indices: List[np.ndarray] = []
    for _, grp in m_meta.groupby(["comp_category", "season_year"], sort=True):
        strata_indices.append(grp.index.to_numpy(dtype=int))

    rng = np.random.default_rng(seed)
    counts_matrix = np.zeros((n_boot, n_matches), dtype=np.int32)
    for b in range(n_boot):
        for idx_arr in strata_indices:
            drawn = rng.choice(idx_arr, size=len(idx_arr), replace=True)
            counts_matrix[b] += np.bincount(drawn, minlength=n_matches).astype(np.int32)
    return unique_match_ids, counts_matrix


def _prepare_role_sufficient_stats(
    df_with_wkt: pd.DataFrame,
    unique_match_ids: np.ndarray,
    role: str,
) -> Dict[str, object]:
    """
    Precompute sparse match-to-cell / match-to-player-cell LPO matrices and
    (match, player, finest_cell) bucket sufficient statistics for exact, fast
    vectorized bootstrap recomputation.
    """
    n_matches = len(unique_match_ids)
    mid_to_idx = {int(m): i for i, m in enumerate(unique_match_ids)}

    if role == "batter":
        id_col = "striker_id"
        hierarchy = BAT_HIERARCHY
        obs = df_with_wkt[df_with_wkt["is_batter_ball_faced"]].copy()
        obs["_denom"] = 1.0
        obs["_num1"] = obs["runs"].astype(float)
        obs["_num2"] = obs["is_striker_dismissed"].astype(float)
        obs["_unit"] = 1.0
    elif role == "bowler":
        id_col = "bowler_id"
        hierarchy = BOWL_HIERARCHY
        obs = df_with_wkt.copy()
        obs["_denom"] = obs["is_legal_ball"].astype(float)
        obs["_num1"] = obs["bowler_runs_conceded"].astype(float)
        obs["_num2"] = obs["is_bowler_wicket"].astype(float)
        obs["_unit"] = obs["is_legal_ball"].astype(float)
    else:
        raise ValueError(f"Unsupported role: {role!r}")

    obs["_m_idx"] = obs["match_id"].map(mid_to_idx).to_numpy(dtype=int)
    player_ids = np.sort(obs[id_col].unique().astype("int64"))
    pid_to_idx = {int(pid): i for i, pid in enumerate(player_ids)}
    obs["_p_idx"] = obs[id_col].map(pid_to_idx).to_numpy(dtype=int)

    finest_cols = list(hierarchy[0])
    pair_cols = ["_p_idx"] + finest_cols
    pairs_df = (
        obs[pair_cols]
        .drop_duplicates()
        .sort_values(pair_cols)
        .reset_index(drop=True)
    )
    pairs_df["_pair_idx"] = np.arange(len(pairs_df), dtype=int)
    obs = obs.merge(pairs_df, on=pair_cols, how="left")

    # Build sparse LPO matrices per hierarchy level
    level_specs = []
    for cols in hierarchy:
        cols_list = list(cols)
        if not cols_list:
            # Global level: 1 cell, n_players player-cells
            m_cell = np.zeros((n_matches, 3), dtype=float)
            np.add.at(m_cell, (obs["_m_idx"].to_numpy(), 0), obs["_denom"].to_numpy())
            np.add.at(m_cell, (obs["_m_idx"].to_numpy(), 1), obs["_num1"].to_numpy())
            np.add.at(m_cell, (obs["_m_idx"].to_numpy(), 2), obs["_num2"].to_numpy())

            p_idx = obs["_p_idx"].to_numpy()
            m_idx = obs["_m_idx"].to_numpy()
            n_p = len(player_ids)
            mp_denom = sparse.csr_matrix((obs["_denom"].to_numpy(), (m_idx, p_idx)), shape=(n_matches, n_p))
            mp_num1 = sparse.csr_matrix((obs["_num1"].to_numpy(), (m_idx, p_idx)), shape=(n_matches, n_p))
            mp_num2 = sparse.csr_matrix((obs["_num2"].to_numpy(), (m_idx, p_idx)), shape=(n_matches, n_p))
            level_specs.append(
                {
                    "is_global": True,
                    "m_cell_dense": m_cell,
                    "mp_mat": sparse.hstack([mp_denom, mp_num1, mp_num2], format="csr"),
                    "n_pcells": n_p,
                    "pair_to_pcell": pairs_df["_p_idx"].to_numpy(dtype=int),
                }
            )
            continue

        # Assign dense integer ids for cell_L and (player, cell_L)
        cell_df = pairs_df[cols_list].drop_duplicates().sort_values(cols_list).reset_index(drop=True)
        cell_df["_c_idx"] = np.arange(len(cell_df), dtype=int)
        pcell_df = pairs_df[["_p_idx"] + cols_list].drop_duplicates().sort_values(["_p_idx"] + cols_list).reset_index(drop=True)
        pcell_df["_pc_idx"] = np.arange(len(pcell_df), dtype=int)

        pair_to_cell = pairs_df.merge(cell_df, on=cols_list, how="left")["_c_idx"].to_numpy(dtype=int)
        pair_to_pcell = pairs_df.merge(pcell_df, on=["_p_idx"] + cols_list, how="left")["_pc_idx"].to_numpy(dtype=int)

        obs_c = obs.merge(cell_df, on=cols_list, how="left")["_c_idx"].to_numpy(dtype=int)
        obs_pc = obs.merge(pcell_df, on=["_p_idx"] + cols_list, how="left")["_pc_idx"].to_numpy(dtype=int)

        m_idx = obs["_m_idx"].to_numpy()
        n_c = len(cell_df)
        n_pc = len(pcell_df)
        d_arr = obs["_denom"].to_numpy()
        n1_arr = obs["_num1"].to_numpy()
        n2_arr = obs["_num2"].to_numpy()

        c_mat = sparse.hstack(
            [
                sparse.csr_matrix((d_arr, (m_idx, obs_c)), shape=(n_matches, n_c)),
                sparse.csr_matrix((n1_arr, (m_idx, obs_c)), shape=(n_matches, n_c)),
                sparse.csr_matrix((n2_arr, (m_idx, obs_c)), shape=(n_matches, n_c)),
            ],
            format="csr",
        )
        pc_mat = sparse.hstack(
            [
                sparse.csr_matrix((d_arr, (m_idx, obs_pc)), shape=(n_matches, n_pc)),
                sparse.csr_matrix((n1_arr, (m_idx, obs_pc)), shape=(n_matches, n_pc)),
                sparse.csr_matrix((n2_arr, (m_idx, obs_pc)), shape=(n_matches, n_pc)),
            ],
            format="csr",
        )
        level_specs.append(
            {
                "is_global": False,
                "c_mat": c_mat,
                "pc_mat": pc_mat,
                "n_cells": n_c,
                "n_pcells": n_pc,
                "pair_to_cell": pair_to_cell,
                "pair_to_pcell": pair_to_pcell,
            }
        )

    # Precompute delivery-level weighted quantities for (match, player, pair) buckets
    pw = obs["pressure_weight"].to_numpy(dtype=float)
    nw = obs["normal_weight"].to_numpy(dtype=float)
    hp = obs["is_high_pressure"].to_numpy(dtype=float)
    unit = obs["_unit"].to_numpy(dtype=float)
    runs = obs["_num1"].to_numpy(dtype=float)
    evt = obs["_num2"].to_numpy(dtype=float)
    wv = obs["wicket_value"].to_numpy(dtype=float)

    obs["_tot_u"] = unit
    obs["_hp_u"] = hp * unit
    obs["_w_u"] = pw * unit
    obs["_w_u2"] = obs["_w_u"] * obs["_w_u"]
    obs["_w_runs"] = pw * runs
    obs["_w_wktval_evt"] = pw * wv * evt
    obs["_w_wktval_unit"] = pw * wv * unit

    obs["_n_u"] = nw * unit
    obs["_n_u2"] = obs["_n_u"] * obs["_n_u"]
    obs["_n_runs"] = nw * runs
    obs["_n_wktval_evt"] = nw * wv * evt
    obs["_n_wktval_unit"] = nw * wv * unit

    obs["_hp_runs"] = hp * runs
    obs["_hp_wktval_evt"] = hp * wv * evt
    obs["_hp_wktval_unit"] = hp * wv * unit

    bucket_cols = [
        "_tot_u",
        "_hp_u",
        "_w_u",
        "_w_u2",
        "_w_runs",
        "_w_wktval_evt",
        "_w_wktval_unit",
        "_n_u",
        "_n_u2",
        "_n_runs",
        "_n_wktval_evt",
        "_n_wktval_unit",
        "_hp_runs",
        "_hp_wktval_evt",
        "_hp_wktval_unit",
    ]
    q_df = obs.groupby(["_m_idx", "_p_idx", "_pair_idx"], as_index=False)[bucket_cols].sum()

    # Match-player totals for eligibility & qualifying match consistency (m_hp_balls >= 6)
    mp_df = q_df.groupby(["_m_idx", "_p_idx"], as_index=False)[["_tot_u", "_hp_u"]].sum()
    mp_df["_has_hp_m"] = (mp_df["_hp_u"] > 0.0).astype(float)
    mp_df["_is_qual_m"] = mp_df["_hp_u"] >= 6.0

    # Sparse matrices from match -> player for fixed exposure sums
    mp_m = mp_df["_m_idx"].to_numpy(dtype=int)
    mp_p = mp_df["_p_idx"].to_numpy(dtype=int)
    n_p = len(player_ids)
    mat_tot_u = sparse.csr_matrix((mp_df["_tot_u"].to_numpy(), (mp_m, mp_p)), shape=(n_matches, n_p))
    mat_hp_u = sparse.csr_matrix((mp_df["_hp_u"].to_numpy(), (mp_m, mp_p)), shape=(n_matches, n_p))
    mat_hp_m = sparse.csr_matrix((mp_df["_has_hp_m"].to_numpy(), (mp_m, mp_p)), shape=(n_matches, n_p))

    # Qualifying match buckets for fast consistency impact summation
    qual_mp = mp_df[mp_df["_is_qual_m"]][["_m_idx", "_p_idx"]].reset_index(drop=True)
    qual_mp["_r_idx"] = np.arange(len(qual_mp), dtype=int)
    q_qual = q_df.merge(qual_mp, on=["_m_idx", "_p_idx"], how="inner")

    # Also sparse matrices for player pressure/normal exposure denominators & sums of squares
    qm = q_df["_m_idx"].to_numpy(dtype=int)
    qp = q_df["_p_idx"].to_numpy(dtype=int)
    mat_w_u = sparse.csr_matrix((q_df["_w_u"].to_numpy(), (qm, qp)), shape=(n_matches, n_p))
    mat_w_u2 = sparse.csr_matrix((q_df["_w_u2"].to_numpy(), (qm, qp)), shape=(n_matches, n_p))
    mat_n_u = sparse.csr_matrix((q_df["_n_u"].to_numpy(), (qm, qp)), shape=(n_matches, n_p))
    mat_n_u2 = sparse.csr_matrix((q_df["_n_u2"].to_numpy(), (qm, qp)), shape=(n_matches, n_p))
    mat_hp_u_q = sparse.csr_matrix((q_df["_hp_u"].to_numpy(), (qm, qp)), shape=(n_matches, n_p))

    return {
        "role": role,
        "id_col": id_col,
        "player_ids": player_ids,
        "n_pairs": len(pairs_df),
        "level_specs": level_specs,
        "q_df": q_df,
        "qual_mp": qual_mp,
        "q_qual": q_qual,
        "mat_tot_u": mat_tot_u,
        "mat_hp_u": mat_hp_u,
        "mat_hp_m": mat_hp_m,
        "mat_w_u": mat_w_u,
        "mat_w_u2": mat_w_u2,
        "mat_n_u": mat_n_u,
        "mat_n_u2": mat_n_u2,
        "mat_hp_u_q": mat_hp_u_q,
    }


def _recompute_lpo_from_stats(
    c_vec: np.ndarray,
    level_specs: List[Dict[str, object]],
    n_pairs: int,
    min_cell_n: int = DEFAULT_MIN_CELL_N,
) -> Tuple[np.ndarray, np.ndarray]:
    """Recompute exact LPO context baselines (ctx_rpb, ctx_evt) for a single bootstrap draw."""
    assigned = np.zeros(n_pairs, dtype=bool)
    ctx_rpb = np.zeros(n_pairs, dtype=float)
    ctx_evt = np.zeros(n_pairs, dtype=float)

    c_row = c_vec.reshape(1, -1).astype(float)
    tot_denom_global = 0.0
    tot_num1_global = 0.0
    tot_num2_global = 0.0

    for spec in level_specs:
        if spec["is_global"]:
            g_sums = (c_row @ spec["m_cell_dense"]).ravel()
            tot_denom_global = float(g_sums[0])
            tot_num1_global = float(g_sums[1])
            tot_num2_global = float(g_sums[2])

            pc_sums = np.asarray(c_row @ spec["mp_mat"]).ravel()
            n_pc = spec["n_pcells"]
            p_d = pc_sums[:n_pc]
            p_1 = pc_sums[n_pc : 2 * n_pc]
            p_2 = pc_sums[2 * n_pc :]
            idx_pc = spec["pair_to_pcell"]
            lpo_d = tot_denom_global - p_d[idx_pc]
            lpo_1 = tot_num1_global - p_1[idx_pc]
            lpo_2 = tot_num2_global - p_2[idx_pc]
            accept = (~assigned) & (lpo_d > 0.0)
        else:
            c_sums = np.asarray(c_row @ spec["c_mat"]).ravel()
            n_c = spec["n_cells"]
            c_d = c_sums[:n_c]
            c_1 = c_sums[n_c : 2 * n_c]
            c_2 = c_sums[2 * n_c :]

            pc_sums = np.asarray(c_row @ spec["pc_mat"]).ravel()
            n_pc = spec["n_pcells"]
            p_d = pc_sums[:n_pc]
            p_1 = pc_sums[n_pc : 2 * n_pc]
            p_2 = pc_sums[2 * n_pc :]

            idx_c = spec["pair_to_cell"]
            idx_pc = spec["pair_to_pcell"]
            lpo_d = c_d[idx_c] - p_d[idx_pc]
            lpo_1 = c_1[idx_c] - p_1[idx_pc]
            lpo_2 = c_2[idx_c] - p_2[idx_pc]
            accept = (~assigned) & (lpo_d >= float(min_cell_n))

        if np.any(accept):
            ctx_rpb[accept] = lpo_1[accept] / lpo_d[accept]
            ctx_evt[accept] = lpo_2[accept] / lpo_d[accept]
            assigned |= accept

        if np.all(assigned):
            break

    if not np.all(assigned):
        rem = ~assigned
        if tot_denom_global > 0.0:
            ctx_rpb[rem] = tot_num1_global / tot_denom_global
            ctx_evt[rem] = tot_num2_global / tot_denom_global
    return ctx_rpb, ctx_evt


def _score_single_draw_from_stats(
    c_vec: np.ndarray,
    stats: Dict[str, object],
    gate: EligibilityGate,
    shrink_k: float,
    model_name: str,
    min_cell_n: int,
) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """
    Compute exact per-player scores, ranks, eligibility mask, and presence mask
    for a single bootstrap draw vector `c_vec`.
    """
    role = stats["role"]
    n_p = len(stats["player_ids"])
    sign = 1.0 if role == "batter" else -1.0
    scale = 100.0 if role == "batter" else 24.0
    lp_floor = -5.0 if role == "batter" else -3.0

    ctx_rpb, ctx_evt = _recompute_lpo_from_stats(
        c_vec, stats["level_specs"], stats["n_pairs"], min_cell_n=min_cell_n
    )

    c_row = c_vec.reshape(1, -1).astype(float)
    tot_u = np.asarray(c_row @ stats["mat_tot_u"]).ravel()
    hp_u = np.asarray(c_row @ stats["mat_hp_u"]).ravel()
    hp_m = np.asarray(c_row @ stats["mat_hp_m"]).ravel()
    w_u = np.asarray(c_row @ stats["mat_w_u"]).ravel()
    w_u2 = np.asarray(c_row @ stats["mat_w_u2"]).ravel()
    n_u = np.asarray(c_row @ stats["mat_n_u"]).ravel()
    n_u2 = np.asarray(c_row @ stats["mat_n_u2"]).ravel()

    present = tot_u > 0.0
    elig = (
        (tot_u >= gate.min_total_balls)
        & (hp_u >= gate.min_hp_balls)
        & (hp_m >= gate.min_hp_matches)
    )
    neff_p = np.divide(np.square(w_u), w_u2, out=np.zeros_like(w_u), where=w_u2 > 0.0)
    neff_n = np.divide(np.square(n_u), n_u2, out=np.zeros_like(n_u), where=n_u2 > 0.0)
    if gate.min_pressure_neff > 0.0:
        elig &= neff_p >= gate.min_pressure_neff

    q_df = stats["q_df"]
    qm = q_df["_m_idx"].to_numpy(dtype=int)
    qp = q_df["_p_idx"].to_numpy(dtype=int)
    q_pair = q_df["_pair_idx"].to_numpy(dtype=int)
    c_q = c_vec[qm].astype(float)

    rpb_q = ctx_rpb[q_pair]
    evt_q = ctx_evt[q_pair]

    w_imp_q = c_q * (
        sign * (q_df["_w_runs"].to_numpy() - rpb_q * q_df["_w_u"].to_numpy())
        + sign * (evt_q * q_df["_w_wktval_unit"].to_numpy() - q_df["_w_wktval_evt"].to_numpy())
    )
    n_imp_q = c_q * (
        sign * (q_df["_n_runs"].to_numpy() - rpb_q * q_df["_n_u"].to_numpy())
        + sign * (evt_q * q_df["_n_wktval_unit"].to_numpy() - q_df["_n_wktval_evt"].to_numpy())
    )
    hp_imp_q = c_q * (
        sign * (q_df["_hp_runs"].to_numpy() - rpb_q * q_df["_hp_u"].to_numpy())
        + sign * (evt_q * q_df["_hp_wktval_unit"].to_numpy() - q_df["_hp_wktval_evt"].to_numpy())
    )

    w_imp_p = np.bincount(qp, weights=w_imp_q, minlength=n_p)
    n_imp_p = np.bincount(qp, weights=n_imp_q, minlength=n_p)
    hp_imp_p = np.bincount(qp, weights=hp_imp_q, minlength=n_p)

    wp_rate = np.where(w_u > 0.0, scale * w_imp_p / np.where(w_u > 0.0, w_u, 1.0), 0.0)
    norm_rate = np.where(n_u > 0.0, scale * n_imp_p / np.where(n_u > 0.0, n_u, 1.0), 0.0)
    hp_rate = np.where(hp_u > 0.0, scale * hp_imp_p / np.where(hp_u > 0.0, hp_u, 1.0), 0.0)

    shrunk_wp = eb_shrink_rate(wp_rate, neff_p, k=shrink_k, prior_mean=0.0)
    shrunk_norm = eb_shrink_rate(norm_rate, neff_n, k=shrink_k, prior_mean=0.0)
    shrunk_hp = eb_shrink_rate(hp_rate, hp_u, k=shrink_k, prior_mean=0.0)

    # Match-level qualifying consistency inside draw
    qual_mp = stats["qual_mp"]
    q_qual = stats["q_qual"]
    n_r = len(qual_mp)
    if n_r > 0:
        qq_pair = q_qual["_pair_idx"].to_numpy(dtype=int)
        qq_r = q_qual["_r_idx"].to_numpy(dtype=int)
        qq_imp = (
            sign * (q_qual["_hp_runs"].to_numpy() - ctx_rpb[qq_pair] * q_qual["_hp_u"].to_numpy())
            + sign * (ctx_evt[qq_pair] * q_qual["_hp_wktval_unit"].to_numpy() - q_qual["_hp_wktval_evt"].to_numpy())
        )
        m_imp = np.bincount(qq_r, weights=qq_imp, minlength=n_r)
        is_pos = (m_imp > 1e-12).astype(float)
        r_m = qual_mp["_m_idx"].to_numpy(dtype=int)
        r_p = qual_mp["_p_idx"].to_numpy(dtype=int)
        c_r = c_vec[r_m].astype(float)
        pos_m_p = np.bincount(r_p, weights=c_r * is_pos, minlength=n_p)
        tot_m_p = np.bincount(r_p, weights=c_r, minlength=n_p)
    else:
        pos_m_p = np.zeros(n_p, dtype=float)
        tot_m_p = np.zeros(n_p, dtype=float)

    fit_mask = elig & (tot_m_p >= 3.0)
    if int(np.sum(fit_mask)) < 10:
        fit_mask = tot_m_p >= 3.0
    alpha_0, beta_0 = fit_empirical_beta_prior(pos_m_p[fit_mask], tot_m_p[fit_mask])
    eb_cons = beta_binomial_consistency(pos_m_p, tot_m_p, alpha_0=alpha_0, beta_0=beta_0)

    scores = np.full(n_p, np.nan, dtype=float)
    ranks = np.full(n_p, np.nan, dtype=float)
    if np.sum(elig) > 0:
        if model_name == "model_a":
            s_elig = (
                0.50 * zscore(shrunk_wp[elig]).to_numpy()
                + 0.30 * zscore(shrunk_hp[elig]).to_numpy()
                + 0.20 * zscore(eb_cons[elig]).to_numpy()
            )
        elif model_name == "model_b":
            maint_lift = shrunk_wp[elig] - 0.35 * np.maximum(shrunk_norm[elig], lp_floor)
            s_elig = (
                0.50 * zscore(shrunk_wp[elig]).to_numpy()
                + 0.30 * zscore(maint_lift).to_numpy()
                + 0.20 * zscore(eb_cons[elig]).to_numpy()
            )
        else:
            raise ValueError(f"Unsupported bootstrap model_name: {model_name!r}")

        scores[elig] = s_elig
        ranks[elig] = pd.Series(s_elig).rank(ascending=False, method="min").to_numpy()

    return scores, ranks, elig, present


def run_stratified_bootstrap(
    df: pd.DataFrame,
    player_lookup: pd.DataFrame,
    role: str,
    model_name: str = "model_b",
    n_boot: int = 1000,
    seed: int = 42,
    gate: EligibilityGate = BENCHMARK_GATE,
    shrink_k: float = DEFAULT_SHRINK_K,
    wicket_mode: str | float = 6.0,
    min_cell_n: int = DEFAULT_MIN_CELL_N,
    counts_matrix: np.ndarray | None = None,
    unique_match_ids: np.ndarray | None = None,
) -> Tuple[pd.DataFrame, Dict[str, float]]:
    """
    Run full stratified match-cluster bootstrap (1,000 resamples by default) using
    exact sufficient-statistic algebra. Recomputes LPO baselines, Beta-binomial
    prior & consistency, eligibility gates, and full-pool rankings in EVERY draw.

    Tracks `absent_iters` and `ineligible_iters` transparently without fabricating ranks.
    """
    t0 = time.perf_counter()
    df_wkt, _ = attach_wicket_values(df, wicket_mode=wicket_mode)
    if unique_match_ids is None or counts_matrix is None:
        unique_match_ids, counts_matrix = generate_stratified_match_draws(
            df_wkt, n_boot=n_boot, seed=seed
        )
    else:
        n_boot = counts_matrix.shape[0]

    stats = _prepare_role_sufficient_stats(df_wkt, unique_match_ids, role=role)
    player_ids = stats["player_ids"]
    id_col = stats["id_col"]
    n_p = len(player_ids)

    all_ranks = np.full((n_boot, n_p), np.nan, dtype=float)
    all_scores = np.full((n_boot, n_p), np.nan, dtype=float)
    all_elig = np.zeros((n_boot, n_p), dtype=bool)
    all_present = np.zeros((n_boot, n_p), dtype=bool)

    for b in range(n_boot):
        s_b, r_b, e_b, p_b = _score_single_draw_from_stats(
            counts_matrix[b],
            stats=stats,
            gate=gate,
            shrink_k=shrink_k,
            model_name=model_name,
            min_cell_n=min_cell_n,
        )
        all_scores[b] = s_b
        all_ranks[b] = r_b
        all_elig[b] = e_b
        all_present[b] = p_b

    elapsed = time.perf_counter() - t0

    rows = []
    for i, pid in enumerate(player_ids):
        elig_i = all_elig[:, i]
        pres_i = all_present[:, i]
        n_elig = int(np.sum(elig_i))
        n_absent = int(np.sum(~pres_i))
        n_inelig = int(np.sum(pres_i & (~elig_i)))
        valid_ranks = all_ranks[elig_i, i]
        valid_scores = all_scores[elig_i, i]

        if n_elig > 0:
            med_rk = float(np.median(valid_ranks))
            mean_rk = float(np.mean(valid_ranks))
            p05_rk = float(np.percentile(valid_ranks, 5))
            p95_rk = float(np.percentile(valid_ranks, 95))
            mean_sc = float(np.mean(valid_scores))
            sd_sc = float(np.std(valid_scores, ddof=0))
            top10_freq = float(np.sum(valid_ranks <= 10.0) / float(n_boot))
        else:
            med_rk = np.nan
            mean_rk = np.nan
            p05_rk = np.nan
            p95_rk = np.nan
            mean_sc = np.nan
            sd_sc = np.nan
            top10_freq = 0.0

        rows.append(
            {
                id_col: int(pid),
                "n_boot": int(n_boot),
                "valid_eligible_iters": n_elig,
                "ineligible_iters": n_inelig,
                "absent_iters": n_absent,
                "boot_median_rank": med_rk,
                "boot_mean_rank": mean_rk,
                "boot_p05_rank": p05_rk,
                "boot_p95_rank": p95_rk,
                "boot_ci_width": p95_rk - p05_rk if np.isfinite(p95_rk) and np.isfinite(p05_rk) else np.nan,
                "boot_mean_score": mean_sc,
                "boot_sd_score": sd_sc,
                "top10_inclusion_frequency": top10_freq,
            }
        )

    res_df = pd.DataFrame(rows).merge(
        player_lookup.rename(columns={"player_id": id_col}),
        on=id_col,
        how="left",
    )
    meta = {
        "role": role,
        "model_name": model_name,
        "n_boot": int(n_boot),
        "runtime_seconds": float(elapsed),
    }
    return res_df, meta


def run_direct_delivery_bootstrap_pilot(
    df: pd.DataFrame,
    player_lookup: pd.DataFrame,
    role: str,
    unique_match_ids: np.ndarray,
    counts_matrix: np.ndarray,
    model_name: str = "model_b",
    gate: EligibilityGate = BENCHMARK_GATE,
    shrink_k: float = DEFAULT_SHRINK_K,
    wicket_mode: str | float = 6.0,
    min_cell_n: int = DEFAULT_MIN_CELL_N,
) -> pd.DataFrame:
    """
    Direct delivery-level bootstrap reference implementation for pilot equivalence
    testing (creates explicit `boot_match_instance_id` copies and re-runs
    `add_lpo_context_baselines` + `compute_player_base_metrics` from scratch).
    """
    df_wkt, _ = attach_wicket_values(df, wicket_mode=wicket_mode)
    id_col = "striker_id" if role == "batter" else "bowler_id"
    score_col = f"{model_name}_score"

    match_groups = {int(mid): grp for mid, grp in df_wkt.groupby("match_id", sort=False)}
    n_boot = counts_matrix.shape[0]
    records = []

    for b in range(n_boot):
        parts = []
        inst_counter = 0
        for m_idx, mult in enumerate(counts_matrix[b]):
            if mult <= 0:
                continue
            m_df = match_groups[int(unique_match_ids[m_idx])]
            for _ in range(int(mult)):
                inst_counter += 1
                copy_m = m_df.copy()
                copy_m["boot_match_instance_id"] = inst_counter
                parts.append(copy_m)

        boot_df = pd.concat(parts, ignore_index=True)
        boot_df = add_lpo_context_baselines(boot_df, min_cell_n=min_cell_n)
        base, _ = compute_player_base_metrics(
            boot_df,
            player_lookup,
            role=role,
            wicket_mode=wicket_mode,
            shrink_k=shrink_k,
            gate=gate,
        )
        elig = base[base["is_eligible"]].copy()
        if model_name == "model_a":
            scored = score_model_a(elig)
        elif model_name == "model_b":
            scored = score_model_b(elig, role=role)
        else:
            raise ValueError(f"Unsupported model_name: {model_name!r}")
        scored["boot_rank"] = scored[score_col].rank(ascending=False, method="min")
        for _, r in scored.iterrows():
            records.append(
                {
                    "iter": b,
                    id_col: int(r[id_col]),
                    "score": float(r[score_col]),
                    "rank": float(r["boot_rank"]),
                }
            )
    return pd.DataFrame(records)
