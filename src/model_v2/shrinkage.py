"""Empirical Bayes shrinkage, Beta-binomial match consistency, Kish N_eff, and wicket valuation."""

from __future__ import annotations

from typing import Dict, Iterable, Sequence, Tuple
import numpy as np
import pandas as pd
from scipy.optimize import minimize
from scipy.special import betaln

from .pressure_model import grouped_kish_neff


OVER_BUCKET_BINS = [0, 6, 10, 15, 25]
OVER_BUCKET_LABELS = ["1-6", "7-10", "11-15", "16-20"]

DEFAULT_SHRINK_K: float = 120.0
SHRINK_K_GRID: Tuple[float, ...] = (60.0, 90.0, 120.0, 150.0, 180.0)


def assign_over_bucket(overid: pd.Series) -> pd.Series:
    """Bucket 1-indexed over numbers into Powerplay (1-6), Early-Mid (7-10), Late-Mid (11-15), Death (16-20)."""
    vals = pd.to_numeric(overid, errors="coerce").clip(lower=1, upper=20)
    return pd.cut(
        vals,
        bins=OVER_BUCKET_BINS,
        labels=OVER_BUCKET_LABELS,
        include_lowest=True,
    ).astype(str)


def _fit_ridge_state_curve(
    X: np.ndarray,
    y: np.ndarray,
    penalty_diag: np.ndarray,
    prior_beta: np.ndarray | None = None,
) -> np.ndarray:
    """Solve (X^T X + P)(beta - prior) = X^T (y - X prior)."""
    if len(y) == 0:
        return np.zeros(X.shape[1], dtype=float) if prior_beta is None else prior_beta.copy()
    if prior_beta is None:
        prior_beta = np.zeros(X.shape[1], dtype=float)
    res = y - X @ prior_beta
    xtx = X.T @ X + np.diag(penalty_diag)
    xty = X.T @ res
    delta = np.linalg.solve(xtx, xty)
    return prior_beta + delta


def estimate_context_wicket_value_table(
    df: pd.DataFrame,
    min_val: float = 1.0,
    max_val: float = 15.0,
) -> pd.DataFrame:
    """
    Estimate non-overlapping context-dependent marginal wicket value at
    (comp_tier, innings, over_bucket, pre_wickets).

    Methodology (zero double-counting):
    - Uses `runs_rem_after = inn_total_runs - post_runs`, strictly EXCLUDING
      runs scored on delivery t itself so dismissal value never overlaps with
      batter runs_above_exp or bowler runs_saved on ball t.
    - Controls for `post_balls_rem` (and `runs_needed` in innings 2 chases)
      so within-bucket timing does not confound wicket state with overs left.
    - Fits a hierarchical Ridge curve in `(post_wickets, post_wickets^2)` shrunk
      toward the `(innings, over_bucket)` parent curve, then evaluates the
      marginal expected future runs drop from W -> W + 1 at `pre_wickets = W`.
    """
    work = df[
        [
            "match_id",
            "innings",
            "comp_tier",
            "overid",
            "post_runs",
            "post_legal_balls",
            "post_wickets",
            "inn_max_balls",
            "runs_needed",
        ]
    ].copy()
    inn_tot = work.groupby(["match_id", "innings"])["post_runs"].transform("max")
    work["runs_rem_after"] = (inn_tot - work["post_runs"]).astype(float)
    work["post_balls_rem"] = np.maximum(
        0.0, work["inn_max_balls"].astype(float) - work["post_legal_balls"].astype(float)
    )
    work["over_bucket"] = assign_over_bucket(work["overid"])
    work["w_cap"] = np.minimum(work["post_wickets"].astype(float), 9.0)
    work["runs_needed_safe"] = work["runs_needed"].fillna(0.0).astype(float)

    def _design(sub: pd.DataFrame, inn: int) -> np.ndarray:
        w = sub["w_cap"].to_numpy(dtype=float)
        cols = [
            np.ones(len(sub), dtype=float),
            sub["post_balls_rem"].to_numpy(dtype=float),
        ]
        if inn == 2:
            cols.append(sub["runs_needed_safe"].to_numpy(dtype=float))
        cols.extend([w, w * w])
        return np.column_stack(cols)

    parent_betas: Dict[Tuple[int, str], np.ndarray] = {}
    for inn in (1, 2):
        pen_p = np.array([1e-6, 1e-6, 100.0, 5000.0] if inn == 1 else [1e-6, 1e-6, 1e-6, 100.0, 5000.0])
        for ob in OVER_BUCKET_LABELS:
            sub = work[(work["innings"] == inn) & (work["over_bucket"] == ob)]
            if len(sub) == 0:
                parent_betas[(inn, ob)] = np.zeros(len(pen_p), dtype=float)
            else:
                parent_betas[(inn, ob)] = _fit_ridge_state_curve(
                    _design(sub, inn), sub["runs_rem_after"].to_numpy(dtype=float), pen_p
                )

    comp_tiers = sorted(work["comp_tier"].dropna().astype(str).unique())
    rows = []
    for ct in comp_tiers:
        for inn in (1, 2):
            pen_c = np.array([1e-6, 1e-6, 500.0, 10000.0] if inn == 1 else [1e-6, 1e-6, 1e-6, 500.0, 10000.0])
            for ob in OVER_BUCKET_LABELS:
                sub = work[
                    (work["comp_tier"] == ct)
                    & (work["innings"] == inn)
                    & (work["over_bucket"] == ob)
                ]
                p_beta = parent_betas[(inn, ob)]
                if len(sub) >= 25:
                    beta = _fit_ridge_state_curve(
                        _design(sub, inn),
                        sub["runs_rem_after"].to_numpy(dtype=float),
                        pen_c,
                        prior_beta=p_beta,
                    )
                else:
                    beta = p_beta

                b_w = float(beta[-2])
                b_w2 = float(beta[-1])
                w_counts = sub["post_wickets"].value_counts().to_dict() if len(sub) > 0 else {}
                for k in range(10):
                    # Marginal drop from losing 1 wicket at pre_wickets=k: V(k) - V(k+1)
                    raw_drop = -(b_w + b_w2 * (2.0 * k + 1.0))
                    clipped_drop = float(np.clip(raw_drop, min_val, max_val))
                    rows.append(
                        {
                            "comp_tier": ct,
                            "innings": inn,
                            "over_bucket": ob,
                            "pre_wickets": k,
                            "raw_marginal_drop": float(raw_drop),
                            "marginal_wicket_value": clipped_drop,
                            "cell_n": int(w_counts.get(k, 0)),
                        }
                    )

    return pd.DataFrame(rows)


def attach_wicket_values(
    df: pd.DataFrame,
    wicket_mode: str | float = 6.0,
    wicket_table: pd.DataFrame | None = None,
) -> Tuple[pd.DataFrame, pd.DataFrame | None]:
    """
    Attach delivery-level `wicket_value` using either a fixed scalar (e.g. 4.0, 6.0, 8.0)
    or the non-overlapping context-dependent marginal wicket value ('context').
    """
    out = df.copy()
    if "over_bucket" not in out.columns:
        out["over_bucket"] = assign_over_bucket(out["overid"])

    if isinstance(wicket_mode, str) and wicket_mode.lower() in ("context", "marginal", "dynamic"):
        if wicket_table is None:
            wicket_table = estimate_context_wicket_value_table(out)
        out["_pre_w_cap"] = np.minimum(out["pre_wickets"].astype(int), 9)
        if "wicket_value" in out.columns:
            out = out.drop(columns=["wicket_value"])
        out = out.merge(
            wicket_table[
                ["comp_tier", "innings", "over_bucket", "pre_wickets", "marginal_wicket_value"]
            ].rename(columns={"pre_wickets": "_pre_w_cap", "marginal_wicket_value": "wicket_value"}),
            on=["comp_tier", "innings", "over_bucket", "_pre_w_cap"],
            how="left",
        )
        out["wicket_value"] = out["wicket_value"].fillna(6.0).astype(float)
        out = out.drop(columns=["_pre_w_cap"])
        return out, wicket_table

    w_val = float(wicket_mode)
    out["wicket_value"] = w_val
    return out, wicket_table


def eb_shrink_rate(
    observed: pd.Series | np.ndarray,
    sample_n: pd.Series | np.ndarray,
    k: float = DEFAULT_SHRINK_K,
    prior_mean: float = 0.0,
) -> np.ndarray:
    """Empirical Bayes linear shrinkage toward prior_mean with strength k: w * obs + (1 - w) * prior."""
    obs_arr = np.asarray(observed, dtype=float)
    n_arr = np.maximum(0.0, np.asarray(sample_n, dtype=float))
    w = np.where((n_arr + k) > 0.0, n_arr / (n_arr + k), 0.0)
    return w * obs_arr + (1.0 - w) * float(prior_mean)


def fit_empirical_beta_prior(
    pos: pd.Series | np.ndarray,
    m: pd.Series | np.ndarray,
    min_matches: int = 3,
    min_strength: float = 2.0,
    max_strength: float = 50.0,
) -> Tuple[float, float]:
    """
    Fit an empirical population Beta(alpha_0, beta_0) prior via Beta-Binomial MLE
    (seeded by method-of-moments) over players with >= `min_matches` trials.
    Falls back cleanly to (5.0, 5.0) if data are insufficient or underdispersed.
    """
    pos_arr = np.asarray(pos, dtype=float)
    m_arr = np.asarray(m, dtype=float)
    mask = np.isfinite(pos_arr) & np.isfinite(m_arr) & (m_arr >= float(min_matches)) & (pos_arr >= 0.0) & (pos_arr <= m_arr)
    if np.sum(mask) < 10:
        return 5.0, 5.0

    y = pos_arr[mask]
    n = m_arr[mask]
    p_hat = float(np.sum(y) / np.sum(n))
    p_hat = float(np.clip(p_hat, 0.05, 0.95))

    # Method-of-moments seed
    rates = y / n
    var_emp = float(np.average((rates - p_hat) ** 2, weights=n))
    mean_inv_n = float(np.mean(1.0 / n))
    var_binom = p_hat * (1.0 - p_hat) * mean_inv_n
    tau2 = var_emp - var_binom
    if tau2 <= 1e-4:
        m0_init = 20.0
    else:
        m0_init = float(np.clip((p_hat * (1.0 - p_hat)) / tau2 - 1.0, min_strength, max_strength))

    a_init = max(0.5, m0_init * p_hat)
    b_init = max(0.5, m0_init * (1.0 - p_hat))

    def _neg_loglik(params: np.ndarray) -> float:
        a, b = float(params[0]), float(params[1])
        ll = np.sum(betaln(y + a, n - y + b) - betaln(a, b))
        return -float(ll)

    res = minimize(
        _neg_loglik,
        x0=np.array([a_init, b_init], dtype=float),
        bounds=[(0.5, max_strength), (0.5, max_strength)],
        method="L-BFGS-B",
    )
    if res.success and np.all(np.isfinite(res.x)):
        alpha_0, beta_0 = float(res.x[0]), float(res.x[1])
        strength = alpha_0 + beta_0
        if strength < min_strength:
            scale = min_strength / max(strength, 1e-9)
            alpha_0 *= scale
            beta_0 *= scale
        elif strength > max_strength:
            scale = max_strength / strength
            alpha_0 *= scale
            beta_0 *= scale
        return alpha_0, beta_0
    return a_init, b_init


def beta_binomial_consistency(
    pos: pd.Series | np.ndarray,
    m: pd.Series | np.ndarray,
    alpha_0: float = 5.0,
    beta_0: float = 5.0,
) -> np.ndarray:
    """Compute Beta-binomial posterior mean consistency (pos + alpha_0) / (m + alpha_0 + beta_0)."""
    pos_arr = np.maximum(0.0, np.asarray(pos, dtype=float))
    m_arr = np.maximum(0.0, np.asarray(m, dtype=float))
    denom = m_arr + float(alpha_0) + float(beta_0)
    return np.where(denom > 0.0, (pos_arr + float(alpha_0)) / denom, 0.5)


def compare_consistency_priors(
    pos: pd.Series | np.ndarray,
    m: pd.Series | np.ndarray,
) -> Tuple[pd.DataFrame, Tuple[float, float]]:
    """
    Compare raw match consistency vs Beta(5,5) vs empirically fitted Beta(alpha_0, beta_0).
    Returns (comparison_df, (alpha_0, beta_0)).
    """
    pos_arr = np.asarray(pos, dtype=float)
    m_arr = np.asarray(m, dtype=float)
    alpha_0, beta_0 = fit_empirical_beta_prior(pos_arr, m_arr)
    safe_m = np.where(m_arr > 0.0, m_arr, 1.0)
    raw = np.where(m_arr > 0.0, pos_arr / safe_m, 0.5)
    b55 = beta_binomial_consistency(pos_arr, m_arr, 5.0, 5.0)
    b_emp = beta_binomial_consistency(pos_arr, m_arr, alpha_0, beta_0)
    out = pd.DataFrame(
        {
            "pos_matches": pos_arr,
            "qual_matches": m_arr,
            "raw_consistency": raw,
            "beta55_consistency": b55,
            "eb_consistency": b_emp,
        }
    )
    return out, (alpha_0, beta_0)


def compute_kish_neff_summary(df: pd.DataFrame, role: str) -> pd.DataFrame:
    """
    Compute raw pressure exposure (sum w_t) and Kish effective sample size
    N_eff = (sum w_t)^2 / sum(w_t^2) for both pressure and normal-pressure regimes.
    """
    if role == "batter":
        sub = df[df["is_batter_ball_faced"]].copy()
        id_col = "striker_id"
        sub["_wp"] = sub["pressure_weight"].astype(float)
        sub["_wn"] = sub["normal_weight"].astype(float)
    elif role == "bowler":
        sub = df.copy()
        id_col = "bowler_id"
        legal = sub["is_legal_ball"].astype(float)
        sub["_wp"] = sub["pressure_weight"].astype(float) * legal
        sub["_wn"] = sub["normal_weight"].astype(float) * legal
    else:
        raise ValueError(f"Unsupported role: {role!r}")

    sub["_wp2"] = sub["_wp"] * sub["_wp"]
    sub["_wn2"] = sub["_wn"] * sub["_wn"]
    agg = sub.groupby(id_col, as_index=False)[["_wp", "_wp2", "_wn", "_wn2"]].sum()
    agg["pressure_exposure_sum"] = agg["_wp"]
    agg["normal_exposure_sum"] = agg["_wn"]
    agg["pressure_neff"] = np.where(
        agg["_wp2"] > 0.0, np.square(agg["_wp"]) / agg["_wp2"], 0.0
    )
    agg["normal_neff"] = np.where(
        agg["_wn2"] > 0.0, np.square(agg["_wn"]) / agg["_wn2"], 0.0
    )
    return agg[
        [
            id_col,
            "pressure_exposure_sum",
            "pressure_neff",
            "normal_exposure_sum",
            "normal_neff",
        ]
    ]


def evaluate_k_shrinkage_sensitivity(
    df: pd.DataFrame,
    role: str,
    k_grid: Sequence[float] = SHRINK_K_GRID,
    wicket_value: float = 6.0,
) -> pd.DataFrame:
    """
    Evaluate shrinkage parameter k in {60, 90, 120, 150, 180} via odd/even match-split
    out-of-sample weighted MSE: shrink even-match pressure impact toward 0 and measure
    weighted squared prediction error against odd-match pressure impact.
    """
    if role == "batter":
        sub = df[df["is_batter_ball_faced"]].copy()
        id_col = "striker_id"
        scale = 100.0
        w_col = "pressure_weight"
        imp = (
            (sub["runs"] - sub["ctx_bat_rpb"])
            + wicket_value * (sub["ctx_bat_out_prob"] - sub["is_striker_dismissed"].astype(float))
        )
        wt = sub[w_col].astype(float)
    elif role == "bowler":
        sub = df.copy()
        id_col = "bowler_id"
        scale = 24.0
        legal = sub["is_legal_ball"].astype(float)
        imp = (
            (sub["ctx_bowl_rpb"] * legal - sub["bowler_runs_conceded"])
            + wicket_value * (sub["is_bowler_wicket"].astype(float) - sub["ctx_bowl_wkt_prob"] * legal)
        )
        wt = sub["pressure_weight"].astype(float) * legal
    else:
        raise ValueError(f"Unsupported role: {role!r}")

    pw = sub["pressure_weight"].to_numpy(dtype=float)
    imp_arr = imp.to_numpy(dtype=float)
    sub = sub[[id_col, "match_id"]].copy()
    sub["_wt"] = wt.to_numpy(dtype=float)
    sub["_wt2"] = sub["_wt"] * sub["_wt"]
    sub["_w_imp"] = pw * imp_arr if role == "bowler" else sub["_wt"] * imp_arr

    match_order = {mid: idx for idx, mid in enumerate(sorted(sub["match_id"].unique()))}
    sub["_is_even"] = sub["match_id"].map(match_order) % 2 == 0

    even_g = sub[sub["_is_even"]].groupby(id_col, as_index=False)[["_wt", "_wt2", "_w_imp"]].sum()
    odd_g = sub[~sub["_is_even"]].groupby(id_col, as_index=False)[["_wt", "_wt2", "_w_imp"]].sum()
    merged = even_g.merge(odd_g, on=id_col, suffixes=("_ev", "_od"))
    merged = merged[(merged["_wt_ev"] >= 20.0) & (merged["_wt_od"] >= 20.0)].copy()

    if len(merged) == 0:
        return pd.DataFrame([{"role": role, "k": k, "split_half_wmse": np.nan, "n_players": 0} for k in k_grid])

    neff_ev = np.where(merged["_wt2_ev"] > 0.0, np.square(merged["_wt_ev"]) / merged["_wt2_ev"], 0.0)
    rate_ev = scale * merged["_w_imp_ev"] / merged["_wt_ev"]
    rate_od = scale * merged["_w_imp_od"] / merged["_wt_od"]
    eval_wt = merged["_wt_od"].to_numpy(dtype=float)

    rows = []
    for k in k_grid:
        pred = eb_shrink_rate(rate_ev, neff_ev, k=float(k), prior_mean=0.0)
        wmse = float(np.average((pred - rate_od) ** 2, weights=eval_wt))
        wmae = float(np.average(np.abs(pred - rate_od), weights=eval_wt))
        corr = float(np.corrcoef(pred, rate_od)[0, 1]) if len(pred) > 1 else np.nan
        rows.append(
            {
                "role": role,
                "k": float(k),
                "split_half_wmse": wmse,
                "split_half_wmae": wmae,
                "split_half_corr": corr,
                "n_players": int(len(merged)),
            }
        )
    return pd.DataFrame(rows)
