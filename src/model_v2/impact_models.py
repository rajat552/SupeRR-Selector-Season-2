"""Models A, B, and C (Regularized Continuous Pressure Interaction + OOS Validation) for Model V2."""

from __future__ import annotations

from typing import Dict, List, Sequence, Tuple
import numpy as np
import pandas as pd
from scipy import sparse
from sklearn.linear_model import LogisticRegression, Ridge
from sklearn.metrics import brier_score_loss, log_loss, mean_absolute_error, mean_squared_error, r2_score

from .batting_features import summarize_batter_roles
from .bowling_features import summarize_bowler_styles
from .eligibility import EligibilityGate, BENCHMARK_GATE, apply_eligibility_gate, compute_player_exposure_table
from .shrinkage import (
    DEFAULT_SHRINK_K,
    attach_wicket_values,
    beta_binomial_consistency,
    compare_consistency_priors,
    eb_shrink_rate,
    fit_empirical_beta_prior,
)


def zscore(s: pd.Series | np.ndarray) -> pd.Series:
    """Population z-score with zero-variance guard."""
    arr = pd.Series(s, dtype=float)
    std = float(arr.std(ddof=0))
    if std == 0.0 or np.isnan(std):
        return pd.Series(0.0, index=arr.index)
    return (arr - float(arr.mean())) / std


def _cluster_se_mean(values: np.ndarray, cluster_ids: np.ndarray) -> float:
    """Cluster-robust standard error of the sample mean (clustered by match_id)."""
    df_tmp = pd.DataFrame({"val": values, "cid": cluster_ids})
    g = df_tmp.groupby("cid", sort=False)["val"].agg(["sum", "count"])
    n_tot = float(len(values))
    n_cl = float(len(g))
    if n_cl <= 1.0 or n_tot <= 0.0:
        return float("nan")
    mu = float(np.mean(values))
    # Centered cluster sums: sum_{t in c} (v_t - mu)
    u_c = g["sum"].to_numpy(dtype=float) - mu * g["count"].to_numpy(dtype=float)
    # Finite-cluster correction G/(G-1)
    var_hat = (n_cl / (n_cl - 1.0)) * float(np.sum(u_c * u_c)) / (n_tot * n_tot)
    return float(np.sqrt(max(0.0, var_hat)))


def _decile_calibration(y_true: np.ndarray, y_prob: np.ndarray) -> Tuple[float, float, float]:
    """
    Compute logistic calibration slope & intercept (logit(p) -> y) plus
    max absolute decile calibration error (ECE-style check).
    """
    p = np.clip(y_prob.astype(float), 1e-6, 1.0 - 1e-6)
    logit_p = np.log(p / (1.0 - p))
    if np.std(logit_p) < 1e-9 or len(np.unique(y_true)) < 2:
        return float("nan"), float("nan"), float("nan")
    # Unpenalized logistic recalibration (very large C)
    lr = LogisticRegression(C=1e6, solver="lbfgs", max_iter=500)
    lr.fit(logit_p.reshape(-1, 1), y_true.astype(int))
    slope = float(lr.coef_[0, 0])
    intercept = float(lr.intercept_[0])

    # Decile calibration max absolute gap
    q_bins = pd.qcut(p, q=10, labels=False, duplicates="drop")
    cal_df = pd.DataFrame({"bin": q_bins, "y": y_true, "p": p}).groupby("bin").mean()
    max_decile_err = float(np.max(np.abs(cal_df["y"] - cal_df["p"])))
    return slope, intercept, max_decile_err


def compute_player_base_metrics(
    df: pd.DataFrame,
    player_lookup: pd.DataFrame,
    role: str,
    wicket_mode: str | float = 6.0,
    shrink_k: float = DEFAULT_SHRINK_K,
    gate: EligibilityGate = BENCHMARK_GATE,
) -> Tuple[pd.DataFrame, Dict[str, object]]:
    """
    Compute comprehensive delivery-aggregated, continuous-pressure-weighted,
    discrete-HP/LP, phase, format, and shrunk player metrics for all players.
    """
    work, wkt_table = attach_wicket_values(df, wicket_mode=wicket_mode)
    exposure = compute_player_exposure_table(work, player_lookup, role=role)
    elig_mask = apply_eligibility_gate(exposure, gate)
    exposure["is_eligible"] = elig_mask

    if role == "batter":
        id_col = "striker_id"
        scale = 100.0
        sub = work[work["is_batter_ball_faced"]].copy()
        sub["_unit"] = 1.0
        sub["_runs"] = sub["runs"].astype(float)
        sub["_evt"] = sub["is_striker_dismissed"].astype(float)
        sub["_rae"] = sub["_runs"] - sub["ctx_bat_rpb"].astype(float)
        sub["_wkt_comp"] = (
            sub["ctx_bat_out_prob"].astype(float) - sub["_evt"]
        ) * sub["wicket_value"].astype(float)
        sub["_dot"] = sub["is_dot_bat"].astype(float)
        sub["_bnd"] = sub["is_boundary_bat"].astype(float)
    elif role == "bowler":
        id_col = "bowler_id"
        scale = 24.0
        sub = work.copy()
        sub["_unit"] = sub["is_legal_ball"].astype(float)
        sub["_runs"] = sub["bowler_runs_conceded"].astype(float)
        sub["_evt"] = sub["is_bowler_wicket"].astype(float)
        sub["_rae"] = sub["ctx_bowl_rpb"].astype(float) * sub["_unit"] - sub["_runs"]
        sub["_wkt_comp"] = (
            sub["_evt"] - sub["ctx_bowl_wkt_prob"].astype(float) * sub["_unit"]
        ) * sub["wicket_value"].astype(float)
        sub["_dot"] = sub["is_dot_bowl"].astype(float)
        sub["_bnd"] = sub["is_boundary_conceded"].astype(float)
    else:
        raise ValueError(f"Unsupported role: {role!r}")

    sub["_imp"] = sub["_rae"] + sub["_wkt_comp"]
    pw = sub["pressure_weight"].to_numpy(dtype=float)
    nw = sub["normal_weight"].to_numpy(dtype=float)
    hp_ind = sub["is_high_pressure"].to_numpy(dtype=float)
    lp_ind = sub["is_low_pressure"].to_numpy(dtype=float)

    def _weighted_agg(wt: np.ndarray, prefix: str) -> pd.DataFrame:
        tmp = pd.DataFrame(
            {
                id_col: sub[id_col].to_numpy(),
                "_w_unit": wt * sub["_unit"].to_numpy(dtype=float),
                "_w_runs": wt * sub["_runs"].to_numpy(dtype=float),
                "_w_evt": wt * sub["_evt"].to_numpy(dtype=float),
                "_w_rae": wt * sub["_rae"].to_numpy(dtype=float),
                "_w_wktc": wt * sub["_wkt_comp"].to_numpy(dtype=float),
                "_w_imp": wt * sub["_imp"].to_numpy(dtype=float),
                "_w_dot": wt * sub["_dot"].to_numpy(dtype=float),
                "_w_bnd": wt * sub["_bnd"].to_numpy(dtype=float),
            }
        )
        g = tmp.groupby(id_col, as_index=False).sum()
        den = g["_w_unit"].to_numpy(dtype=float)
        safe_den = np.where(den > 0.0, den, np.nan)
        out = pd.DataFrame({id_col: g[id_col]})
        out[f"{prefix}_w_balls"] = den
        out[f"{prefix}_runs"] = g["_w_runs"]
        out[f"{prefix}_{'outs' if role == 'batter' else 'wkts'}"] = g["_w_evt"]
        if role == "batter":
            out[f"{prefix}_sr"] = np.where(den > 0.0, 100.0 * g["_w_runs"] / safe_den, 0.0)
            out[f"{prefix}_avg"] = np.where(
                g["_w_evt"] > 0.0, g["_w_runs"] / g["_w_evt"], g["_w_runs"]
            )
            out[f"{prefix}_rae_100"] = np.where(den > 0.0, 100.0 * g["_w_rae"] / safe_den, 0.0)
            out[f"{prefix}_wktval_100"] = np.where(den > 0.0, 100.0 * g["_w_wktc"] / safe_den, 0.0)
            out[f"{prefix}_impact_100"] = np.where(den > 0.0, 100.0 * g["_w_imp"] / safe_den, 0.0)
        else:
            out[f"{prefix}_er"] = np.where(den > 0.0, 6.0 * g["_w_runs"] / safe_den, 0.0)
            out[f"{prefix}_sr"] = np.where(
                g["_w_evt"] > 0.0, den / g["_w_evt"], np.nan
            )
            out[f"{prefix}_rso"] = np.where(den > 0.0, 6.0 * g["_w_rae"] / safe_den, 0.0)
            out[f"{prefix}_wktval_24"] = np.where(den > 0.0, 24.0 * g["_w_wktc"] / safe_den, 0.0)
            out[f"{prefix}_impact_24"] = np.where(den > 0.0, 24.0 * g["_w_imp"] / safe_den, 0.0)
        out[f"{prefix}_dot_pct"] = np.where(den > 0.0, 100.0 * g["_w_dot"] / safe_den, 0.0)
        out[f"{prefix}_bnd_pct"] = np.where(den > 0.0, 100.0 * g["_w_bnd"] / safe_den, 0.0)
        return out

    tot_agg = _weighted_agg(np.ones(len(sub), dtype=float), "tot")
    wp_agg = _weighted_agg(pw, "wp")
    norm_agg = _weighted_agg(nw, "norm")
    hp_agg = _weighted_agg(hp_ind, "hp")
    lp_agg = _weighted_agg(lp_ind, "lp")

    # Format splits (IPL vs T20I) under continuous pressure weight
    for fmt_name, fmt_mask in [
        ("ipl", (sub["comp_category"] == "IPL").to_numpy(dtype=float)),
        ("t20i", (sub["comp_category"] == "T20I").to_numpy(dtype=float)),
    ]:
        f_agg = _weighted_agg(pw * fmt_mask, f"wp_{fmt_name}")
        imp_col = f"wp_{fmt_name}_impact_{100 if role == 'batter' else 24}"
        f_keep = f_agg[[id_col, f"wp_{fmt_name}_w_balls", imp_col]].rename(
            columns={
                f"wp_{fmt_name}_w_balls": f"wp_w_balls_{fmt_name}",
                imp_col: f"wp_impact_{fmt_name}",
            }
        )
        exposure = exposure.merge(f_keep, on=id_col, how="left")

    # Cross-match consistency (discrete HP >= 6 balls in match AND continuous sum_w >= 4.0)
    m_col = "boot_match_instance_id" if "boot_match_instance_id" in sub.columns else "match_id"
    sub["_hp_unit"] = hp_ind * sub["_unit"].to_numpy(dtype=float)
    sub["_hp_imp"] = hp_ind * sub["_imp"].to_numpy(dtype=float)
    sub["_wp_unit"] = pw * sub["_unit"].to_numpy(dtype=float)
    sub["_wp_imp"] = pw * sub["_imp"].to_numpy(dtype=float)

    m_grp = sub.groupby([id_col, m_col], as_index=False)[
        ["_hp_unit", "_hp_imp", "_wp_unit", "_wp_imp"]
    ].sum()
    hp_q = m_grp[m_grp["_hp_unit"] >= 6.0].copy()
    hp_q["pos"] = (hp_q["_hp_imp"] > 1e-12).astype(int)
    cons_hp = hp_q.groupby(id_col, as_index=False).agg(
        hp_pos_matches=("pos", "sum"),
        hp_qual_m=("pos", "count"),
    )
    wp_q = m_grp[m_grp["_wp_unit"] >= 4.0].copy()
    wp_q["pos"] = (wp_q["_wp_imp"] > 1e-12).astype(int)
    cons_wp = wp_q.groupby(id_col, as_index=False).agg(
        wp_pos_matches=("pos", "sum"),
        wp_qual_matches=("pos", "count"),
    )

    merged = (
        exposure.merge(tot_agg, on=id_col, how="left")
        .merge(wp_agg, on=id_col, how="left")
        .merge(norm_agg, on=id_col, how="left")
        .merge(hp_agg, on=id_col, how="left")
        .merge(lp_agg, on=id_col, how="left")
        .merge(cons_hp, on=id_col, how="left")
        .merge(cons_wp, on=id_col, how="left")
    )
    for col in ("hp_pos_matches", "hp_qual_m", "wp_pos_matches", "wp_qual_matches"):
        merged[col] = merged[col].fillna(0).astype(int)
    merged["wp_w_balls_ipl"] = merged["wp_w_balls_ipl"].fillna(0.0)
    merged["wp_w_balls_t20i"] = merged["wp_w_balls_t20i"].fillna(0.0)

    # Role / Style metadata
    if role == "batter":
        role_sum = summarize_batter_roles(df)
        merged = merged.merge(
            role_sum[
                [
                    "striker_id",
                    "primary_batting_role",
                    "top_share",
                    "middle_share",
                    "finisher_share",
                    "role_uncertain_rate",
                    "median_batting_order",
                ]
            ],
            on="striker_id",
            how="left",
        )
    else:
        style_sum = summarize_bowler_styles(df)
        merged = merged.merge(
            style_sum[
                [
                    "bowler_id",
                    "pace_or_spin",
                    "primary_bowling_type",
                    "bowling_arm",
                    "bowling_style_group",
                    "pp_share",
                    "middle_share",
                    "death_share",
                ]
            ],
            on="bowler_id",
            how="left",
        )

    imp_suffix = "100" if role == "batter" else "24"
    wp_col = f"wp_impact_{imp_suffix}"
    hp_col = f"hp_impact_{imp_suffix}"
    norm_col = f"norm_impact_{imp_suffix}"
    tot_col = f"tot_impact_{imp_suffix}"

    merged["shrunk_wp_impact"] = eb_shrink_rate(
        merged[wp_col], merged["pressure_neff"], k=shrink_k, prior_mean=0.0
    )
    merged["shrunk_hp_impact"] = eb_shrink_rate(
        merged[hp_col], merged["hp_balls"], k=shrink_k, prior_mean=0.0
    )
    merged["shrunk_norm_impact"] = eb_shrink_rate(
        merged[norm_col], merged["normal_neff"], k=shrink_k, prior_mean=0.0
    )
    merged["shrunk_tot_impact"] = eb_shrink_rate(
        merged[tot_col], merged["tot_balls"], k=shrink_k, prior_mean=0.0
    )

    # Shrunk IPL vs T20I impact
    merged["shrunk_wp_impact_ipl"] = eb_shrink_rate(
        merged["wp_impact_ipl"].fillna(0.0), merged["wp_w_balls_ipl"], k=shrink_k, prior_mean=0.0
    )
    merged["shrunk_wp_impact_t20i"] = eb_shrink_rate(
        merged["wp_impact_t20i"].fillna(0.0), merged["wp_w_balls_t20i"], k=shrink_k, prior_mean=0.0
    )

    # Fit empirical Beta prior on eligible pool (or >=3 qual matches if small synthetic test)
    fit_mask = merged["is_eligible"] & (merged["hp_qual_m"] >= 3)
    if int(fit_mask.sum()) < 10:
        fit_mask = merged["hp_qual_m"] >= 3
    alpha_0, beta_0 = fit_empirical_beta_prior(
        merged.loc[fit_mask, "hp_pos_matches"],
        merged.loc[fit_mask, "hp_qual_m"],
    )
    cons_cmp, _ = compare_consistency_priors(
        merged["hp_pos_matches"], merged["hp_qual_m"]
    )
    merged["raw_consistency"] = cons_cmp["raw_consistency"].to_numpy()
    merged["beta55_consistency"] = cons_cmp["beta55_consistency"].to_numpy()
    merged["eb_consistency"] = beta_binomial_consistency(
        merged["hp_pos_matches"], merged["hp_qual_m"], alpha_0=alpha_0, beta_0=beta_0
    )

    meta = {
        "beta_alpha_0": float(alpha_0),
        "beta_beta_0": float(beta_0),
        "wicket_mode": wicket_mode,
        "shrink_k": float(shrink_k),
        "wicket_table": wkt_table,
    }
    return merged, meta


def score_model_a(eligible_df: pd.DataFrame) -> pd.DataFrame:
    """
    Model A: Absolute Context-Adjusted Pressure Impact.
    Uses LPO context-adjusted continuous pressure weights (shrunk via Kish N_eff),
    discrete HP tier impact, and Empirical Bayes Beta-binomial match consistency.
    """
    out = eligible_df.copy()
    out["model_a_z_wp"] = zscore(out["shrunk_wp_impact"])
    out["model_a_z_hp"] = zscore(out["shrunk_hp_impact"])
    out["model_a_z_cons"] = zscore(out["eb_consistency"])
    out["model_a_score"] = (
        0.50 * out["model_a_z_wp"]
        + 0.30 * out["model_a_z_hp"]
        + 0.20 * out["model_a_z_cons"]
    )
    return out


def score_model_b(
    eligible_df: pd.DataFrame,
    role: str,
    alpha_baseline: float = 0.35,
) -> pd.DataFrame:
    """
    Model B: Maintenance & Lift.
    - NO lp_balls >= 60 specialist-finisher exclusion.
    - NO elite-baseline penalty: combines absolute shrunk pressure performance
      with attenuated lift over a floored, EB-shrunk normal-pressure baseline
      (`shrunk_wp_impact - 0.35 * max(shrunk_norm_impact, lp_floor)`), plus
      Empirical Bayes Beta-binomial match consistency.
    """
    out = eligible_df.copy()
    lp_floor = -5.0 if role == "batter" else -3.0
    out["norm_baseline_floored"] = np.maximum(out["shrunk_norm_impact"], lp_floor)
    out["maint_lift"] = out["shrunk_wp_impact"] - alpha_baseline * out["norm_baseline_floored"]
    out["raw_pressure_lift"] = out["shrunk_wp_impact"] - out["shrunk_norm_impact"]

    out["model_b_z_abs"] = zscore(out["shrunk_wp_impact"])
    out["model_b_z_lift"] = zscore(out["maint_lift"])
    out["model_b_z_cons"] = zscore(out["eb_consistency"])
    out["model_b_score"] = (
        0.50 * out["model_b_z_abs"]
        + 0.30 * out["model_b_z_lift"]
        + 0.20 * out["model_b_z_cons"]
    )
    return out


def _build_sparse_design_matrices(
    df_train: pd.DataFrame,
    df_eval: pd.DataFrame | None,
    role: str,
) -> Tuple[
    sparse.csr_matrix,
    sparse.csr_matrix | None,
    Dict[str, slice],
    np.ndarray,
    float,
]:
    """
    Build sparse design matrices for Model C:
    Outcome = Context effects + Pressure effect + Player effects + Player x Pressure interaction.
    """
    id_col = "striker_id" if role == "batter" else "bowler_id"
    role_col = "batting_role" if role == "batter" else "pace_or_spin"
    opp_col = "opp_tier_bat" if role == "batter" else "opp_tier_bowl"
    elo_col = "pre_match_opp_elo_bat" if role == "batter" else "pre_match_opp_elo_bowl"

    def _context_blocks(d: pd.DataFrame, categories: Dict[str, List[str]] | None = None, elo_stats: Tuple[float, float] | None = None):
        cat_cols = ["comp_tier", "phase", role_col, opp_col, "innings"]
        blocks = []
        used_cats: Dict[str, List[str]] = {}
        for col in cat_cols:
            vals = d[col].astype(str)
            if categories is None:
                cats = sorted(vals.unique().tolist())
            else:
                cats = categories[col]
            used_cats[col] = cats
            cat_idx = pd.Categorical(vals, categories=cats).codes
            valid = cat_idx >= 0
            rows = np.nonzero(valid)[0]
            mat = sparse.csr_matrix(
                (np.ones(len(rows), dtype=float), (rows, cat_idx[valid])),
                shape=(len(d), len(cats)),
            )
            blocks.append(mat)
        elo_vals = d[elo_col].fillna(1500.0).to_numpy(dtype=float)
        if elo_stats is None:
            mu_e = float(np.mean(elo_vals))
            sd_e = float(np.std(elo_vals)) or 1.0
        else:
            mu_e, sd_e = elo_stats
        elo_z = ((elo_vals - mu_e) / sd_e).reshape(-1, 1)
        blocks.append(sparse.csr_matrix(elo_z))
        # Continuous pressure main effect
        p_w = d["pressure_weight"].to_numpy(dtype=float).reshape(-1, 1)
        blocks.append(sparse.csr_matrix(p_w))
        return sparse.hstack(blocks, format="csr"), used_cats, (mu_e, sd_e)

    X_ctx_tr, cats, elo_stats = _context_blocks(df_train)

    player_ids = np.sort(df_train[id_col].unique())
    pid_to_idx = {int(pid): i for i, pid in enumerate(player_ids)}

    def _player_blocks(d: pd.DataFrame) -> Tuple[sparse.csr_matrix, sparse.csr_matrix]:
        codes = d[id_col].map(pid_to_idx).fillna(-1).to_numpy(dtype=int)
        valid = codes >= 0
        rows = np.nonzero(valid)[0]
        cols = codes[valid]
        p_main = sparse.csr_matrix(
            (np.ones(len(rows), dtype=float), (rows, cols)),
            shape=(len(d), len(player_ids)),
        )
        pw_vals = d["pressure_weight"].to_numpy(dtype=float)[valid]
        p_inter = sparse.csr_matrix(
            (pw_vals, (rows, cols)),
            shape=(len(d), len(player_ids)),
        )
        return p_main, p_inter

    P_tr, PI_tr = _player_blocks(df_train)
    X_tr = sparse.hstack([X_ctx_tr, P_tr, PI_tr], format="csr")

    n_ctx = X_ctx_tr.shape[1]
    n_p = len(player_ids)
    slices = {
        "context": slice(0, n_ctx - 1),
        "pressure": slice(n_ctx - 1, n_ctx),
        "player": slice(n_ctx, n_ctx + n_p),
        "interaction": slice(n_ctx + n_p, n_ctx + 2 * n_p),
    }

    X_ev = None
    if df_eval is not None:
        X_ctx_ev, _, _ = _context_blocks(df_eval, categories=cats, elo_stats=elo_stats)
        P_ev, PI_ev = _player_blocks(df_eval)
        X_ev = sparse.hstack([X_ctx_ev, P_ev, PI_ev], format="csr")

    mean_w = float(df_train["pressure_weight"].mean())
    return X_tr, X_ev, slices, player_ids, mean_w


def fit_model_c_and_score(
    df: pd.DataFrame,
    eligible_df: pd.DataFrame,
    role: str,
    ridge_alpha_runs: float = 150.0,
    logistic_c_wkt: float = 0.5,
    wicket_weight: float = 6.0,
    hp_eval_weight: float = 0.85,
) -> Tuple[pd.DataFrame, Dict[str, object]]:
    """
    Fit Model C (Ridge for runs + L2-regularized Logistic Regression for dismissals/wickets)
    with Context + Pressure + Player + Player x Pressure interaction effects,
    and score eligible players cleanly.
    """
    id_col = "striker_id" if role == "batter" else "bowler_id"
    if role == "batter":
        work = df[df["is_batter_ball_faced"]].copy()
        y_runs = work["runs"].to_numpy(dtype=float)
        y_evt = work["is_striker_dismissed"].astype(int).to_numpy()
        scale = 100.0
    elif role == "bowler":
        work = df[df["is_legal_ball"]].copy()
        y_runs = work["bowler_runs_conceded"].to_numpy(dtype=float)
        y_evt = work["is_bowler_wicket"].astype(int).to_numpy()
        scale = 24.0
    else:
        raise ValueError(f"Unsupported role: {role!r}")

    X_tr, _, slices, player_ids, _ = _build_sparse_design_matrices(work, None, role=role)

    ridge_runs = Ridge(alpha=ridge_alpha_runs, solver="lsqr", tol=1e-5, max_iter=1000)
    ridge_runs.fit(X_tr, y_runs)
    alpha_runs = ridge_runs.coef_[slices["player"]]
    beta_runs = ridge_runs.coef_[slices["interaction"]]

    logit_evt = LogisticRegression(C=logistic_c_wkt, solver="lbfgs", max_iter=500)
    logit_evt.fit(X_tr, y_evt)
    alpha_evt = logit_evt.coef_[0, slices["player"]]
    beta_evt = logit_evt.coef_[0, slices["interaction"]]

    # Average marginal probability slope dp/d(logit) = mean(p*(1-p))
    p_base = float(np.mean(y_evt))
    dp_dlogit = p_base * (1.0 - p_base)

    if role == "batter":
        # Runs above expectation at HP (hp_eval_weight) + survival above expectation
        hp_runs_per_ball = alpha_runs + hp_eval_weight * beta_runs
        hp_surv_per_ball = -dp_dlogit * (alpha_evt + hp_eval_weight * beta_evt)
        hp_imp = scale * (hp_runs_per_ball + wicket_weight * hp_surv_per_ball)
        lift_imp = scale * (beta_runs - wicket_weight * dp_dlogit * beta_evt)
    else:
        # Bowler runs saved = -(runs conceded coef), wickets above exp = +dp_dlogit * evt_coef
        hp_rs_per_ball = -(alpha_runs + hp_eval_weight * beta_runs)
        hp_wae_per_ball = dp_dlogit * (alpha_evt + hp_eval_weight * beta_evt)
        hp_imp = scale * (hp_rs_per_ball + wicket_weight * hp_wae_per_ball)
        lift_imp = scale * (-beta_runs + wicket_weight * dp_dlogit * beta_evt)

    mc_tbl = pd.DataFrame(
        {
            id_col: player_ids.astype("int64"),
            "model_c_hp_impact": hp_imp,
            "model_c_pressure_lift": lift_imp,
            "model_c_runs_coef": alpha_runs,
            "model_c_runs_inter_coef": beta_runs,
            "model_c_wkt_logit_coef": alpha_evt,
            "model_c_wkt_inter_coef": beta_evt,
        }
    )

    out = eligible_df.merge(mc_tbl, on=id_col, how="left")
    for col in ("model_c_hp_impact", "model_c_pressure_lift"):
        out[col] = out[col].fillna(0.0)

    out["model_c_z_hp"] = zscore(out["model_c_hp_impact"])
    out["model_c_z_lift"] = zscore(out["model_c_pressure_lift"])
    out["model_c_z_cons"] = zscore(out["eb_consistency"])
    out["model_c_score"] = (
        0.55 * out["model_c_z_hp"]
        + 0.25 * out["model_c_z_lift"]
        + 0.20 * out["model_c_z_cons"]
    )

    info = {
        "in_sample_runs_r2": float(r2_score(y_runs, ridge_runs.predict(X_tr))),
        "in_sample_evt_brier": float(brier_score_loss(y_evt, logit_evt.predict_proba(X_tr)[:, 1])),
        "n_train_rows": int(len(work)),
        "n_players": int(len(player_ids)),
    }
    return out, info


def run_model_c_oos_validation(
    df: pd.DataFrame,
    splits: Sequence[Tuple[str, Sequence[int], Sequence[int]]] = (
        ("2022-2024_to_2025-2026", (2022, 2023, 2024), (2025, 2026)),
        ("2022-2023_to_2024", (2022, 2023), (2024,)),
        ("2022-2024_to_2025", (2022, 2023, 2024), (2025,)),
        ("2022-2025_to_2026", (2022, 2023, 2024, 2025), (2026,)),
    ),
    ridge_alpha_runs: float = 150.0,
    logistic_c_wkt: float = 0.5,
) -> pd.DataFrame:
    """
    Chronological walk-forward out-of-sample validation for Model C across
    Context-only, Context+Player+Pressure, and Full Interaction specs,
    reporting RMSE, MAE, R2, Brier, log-loss, decile calibration, and match-cluster SEs.
    """
    records = []
    for role in ("batter", "bowler"):
        if role == "batter":
            base = df[df["is_batter_ball_faced"]].copy()
            y_runs_col = "runs"
            y_evt_col = "is_striker_dismissed"
        else:
            base = df[df["is_legal_ball"]].copy()
            y_runs_col = "bowler_runs_conceded"
            y_evt_col = "is_bowler_wicket"

        for split_name, train_yrs, test_yrs in splits:
            tr = base[base["season_year"].isin(train_yrs)]
            te = base[base["season_year"].isin(test_yrs)]
            if len(tr) == 0 or len(te) == 0:
                continue

            X_tr_full, X_te_full, slices, _, _ = _build_sparse_design_matrices(tr, te, role=role)
            y_r_tr = tr[y_runs_col].to_numpy(dtype=float)
            y_r_te = te[y_runs_col].to_numpy(dtype=float)
            y_e_tr = tr[y_evt_col].astype(int).to_numpy()
            y_e_te = te[y_evt_col].astype(int).to_numpy()
            te_clusters = te["match_id"].to_numpy()

            # Nested specs via column slicing
            ctx_end = slices["pressure"].stop
            pl_end = slices["player"].stop
            specs = [
                ("Context_Pressure_Only", slice(0, ctx_end)),
                ("Context_Pressure_Player", slice(0, pl_end)),
                ("Model_C_Full_Interaction", slice(0, X_tr_full.shape[1])),
            ]

            for spec_name, col_slice in specs:
                Xtr = X_tr_full[:, col_slice]
                Xte = X_te_full[:, col_slice]

                # 1. Runs model
                rr = Ridge(alpha=ridge_alpha_runs, solver="lsqr", tol=1e-5, max_iter=1000)
                rr.fit(Xtr, y_r_tr)
                pred_r = rr.predict(Xte)
                sq_err = (y_r_te - pred_r) ** 2
                abs_err = np.abs(y_r_te - pred_r)
                mse = float(np.mean(sq_err))
                rmse = float(np.sqrt(mse))
                mae = float(np.mean(abs_err))
                r2 = float(r2_score(y_r_te, pred_r))
                mse_se = _cluster_se_mean(sq_err, te_clusters)
                rmse_cluster_se = float(mse_se / (2.0 * max(rmse, 1e-9)))
                mae_cluster_se = _cluster_se_mean(abs_err, te_clusters)

                # 2. Binary dismissal / wicket model
                lr = LogisticRegression(C=logistic_c_wkt, solver="lbfgs", max_iter=500)
                lr.fit(Xtr, y_e_tr)
                pred_p = np.clip(lr.predict_proba(Xte)[:, 1], 1e-6, 1.0 - 1e-6)
                brier_vec = (y_e_te - pred_p) ** 2
                brier = float(np.mean(brier_vec))
                brier_cluster_se = _cluster_se_mean(brier_vec, te_clusters)
                ll = float(log_loss(y_e_te, pred_p))
                cal_slope, cal_int, max_dec_err = _decile_calibration(y_e_te, pred_p)

                records.append(
                    {
                        "role": role,
                        "split": split_name,
                        "spec": spec_name,
                        "n_train": int(len(tr)),
                        "n_test": int(len(te)),
                        "n_test_matches": int(te["match_id"].nunique()),
                        "runs_rmse": rmse,
                        "runs_rmse_cluster_se": rmse_cluster_se,
                        "runs_mae": mae,
                        "runs_mae_cluster_se": mae_cluster_se,
                        "runs_r2": r2,
                        "evt_brier": brier,
                        "evt_brier_cluster_se": brier_cluster_se,
                        "evt_log_loss": ll,
                        "evt_cal_slope": cal_slope,
                        "evt_cal_intercept": cal_int,
                        "evt_max_decile_cal_err": max_dec_err,
                    }
                )
    return pd.DataFrame(records)
