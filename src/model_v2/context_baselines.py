"""Leakage-safe Leave-Player-Out (LPO) hierarchical context baselines for Model V2."""

from __future__ import annotations

from typing import Dict, List, Sequence
import numpy as np
import pandas as pd


DEFAULT_MIN_CELL_N: int = 50

BAT_HIERARCHY: List[List[str]] = [
    ["comp_tier", "season_year", "phase", "batting_role", "opp_tier_bat"],
    ["comp_tier", "season_year", "phase", "batting_role"],
    ["comp_tier", "season_year", "phase"],
    ["comp_tier", "phase"],
    ["phase"],
    [],
]

BOWL_HIERARCHY: List[List[str]] = [
    ["comp_tier", "season_year", "phase", "pace_or_spin", "opp_tier_bowl"],
    ["comp_tier", "season_year", "phase", "pace_or_spin"],
    ["comp_tier", "season_year", "phase"],
    ["comp_tier", "phase"],
    ["phase"],
    [],
]


def _compute_lpo_hierarchy(
    obs_df: pd.DataFrame,
    target_df: pd.DataFrame,
    player_col: str,
    num_cols: Sequence[str],
    denom_col: str,
    hierarchy: Sequence[Sequence[str]],
    out_col_map: Dict[str, str],
    level_col: str,
    lpo_n_col: str,
    min_cell_n: int = DEFAULT_MIN_CELL_N,
) -> pd.DataFrame:
    """
    Compute Leave-Player-Out (LPO) hierarchical rates on `obs_df` and map them
    onto `target_df`.

    For every player i and finest cell c in hierarchy[0]:
    - Walk hierarchy from level 0 (most specific) to coarsest (global LPO).
    - At level L, compute n_{-i, c_L} = n_{c_L} - n_{i, c_L}.
    - Accept level L if n_{-i, c_L} >= min_cell_n (for non-empty cell keys) or
      n_{-i, global} > 0 at the global LPO level [].
    - If even global LPO is empty (e.g., 1-player synthetic edge case), fall back
      to global mean across obs_df.
    """
    finest_cols = list(hierarchy[0])
    key_cols = [player_col] + finest_cols

    pairs = target_df[key_cols].drop_duplicates().reset_index(drop=True)
    n_pairs = len(pairs)

    assigned = np.zeros(n_pairs, dtype=bool)
    chosen_level = np.full(n_pairs, -1, dtype=int)
    chosen_lpo_n = np.zeros(n_pairs, dtype=float)
    rates: Dict[str, np.ndarray] = {
        c: np.full(n_pairs, np.nan, dtype=float) for c in num_cols
    }

    agg_cols = list(num_cols) + [denom_col]

    for lvl_idx, cols in enumerate(hierarchy):
        cols_list = list(cols)
        if cols_list:
            cell_agg = obs_df.groupby(cols_list, as_index=False)[agg_cols].sum()
            p_agg = obs_df.groupby([player_col] + cols_list, as_index=False)[
                agg_cols
            ].sum()

            merged_cell = pairs[cols_list].merge(cell_agg, on=cols_list, how="left")
            merged_p = pairs[[player_col] + cols_list].merge(
                p_agg, on=[player_col] + cols_list, how="left"
            )

            cell_denom = merged_cell[denom_col].fillna(0.0).to_numpy(dtype=float)
            p_denom = merged_p[denom_col].fillna(0.0).to_numpy(dtype=float)
            lpo_denom = cell_denom - p_denom
            accept = (~assigned) & (lpo_denom >= float(min_cell_n))
        else:
            tot_sums = obs_df[agg_cols].sum()
            p_agg = obs_df.groupby(player_col, as_index=False)[agg_cols].sum()
            merged_p = pairs[[player_col]].merge(p_agg, on=player_col, how="left")

            cell_denom = np.full(n_pairs, float(tot_sums[denom_col]), dtype=float)
            p_denom = merged_p[denom_col].fillna(0.0).to_numpy(dtype=float)
            lpo_denom = cell_denom - p_denom
            accept = (~assigned) & (lpo_denom > 0.0)

        if np.any(accept):
            for c in num_cols:
                if cols_list:
                    cell_num = merged_cell[c].fillna(0.0).to_numpy(dtype=float)
                else:
                    cell_num = np.full(n_pairs, float(tot_sums[c]), dtype=float)
                p_num = merged_p[c].fillna(0.0).to_numpy(dtype=float)
                lpo_num = cell_num - p_num
                rates[c][accept] = lpo_num[accept] / lpo_denom[accept]

            chosen_level[accept] = lvl_idx
            chosen_lpo_n[accept] = lpo_denom[accept]
            assigned |= accept

        if np.all(assigned):
            break

    if not np.all(assigned):
        rem = ~assigned
        tot_denom = float(obs_df[denom_col].sum()) if len(obs_df) > 0 else 0.0
        for c in num_cols:
            fallback_val = (
                float(obs_df[c].sum()) / tot_denom if tot_denom > 0.0 else 0.0
            )
            rates[c][rem] = fallback_val
        chosen_level[rem] = len(hierarchy)
        chosen_lpo_n[rem] = 0.0

    for raw_c, out_c in out_col_map.items():
        pairs[out_c] = rates[raw_c]
    pairs[level_col] = chosen_level
    pairs[lpo_n_col] = chosen_lpo_n

    return target_df[key_cols].merge(pairs, on=key_cols, how="left")


def add_lpo_context_baselines(
    df: pd.DataFrame, min_cell_n: int = DEFAULT_MIN_CELL_N
) -> pd.DataFrame:
    """
    Add leakage-safe Leave-Player-Out (LPO) hierarchical context baselines for
    both batting and bowling across:
      - Batting:  (comp_tier, season_year, phase, batting_role, opp_tier_bat)
      - Bowling:  (comp_tier, season_year, phase, pace_or_spin, opp_tier_bowl)

    Falls back up the hierarchy whenever (n_cell - n_{i,cell}) < min_cell_n.
    """
    out = df.copy()

    drop_cols = [
        c
        for c in (
            "ctx_bat_rpb",
            "ctx_bat_out_prob",
            "ctx_bat_dot_prob",
            "ctx_bat_bnd_prob",
            "ctx_bat_level",
            "ctx_bat_lpo_n",
            "ctx_bowl_rpb",
            "ctx_bowl_wkt_prob",
            "ctx_bowl_dot_prob",
            "ctx_bowl_bnd_prob",
            "ctx_bowl_level",
            "ctx_bowl_lpo_n",
        )
        if c in out.columns
    ]
    if drop_cols:
        out = out.drop(columns=drop_cols)

    # 1. Batting LPO baselines (estimated strictly on batter balls faced: ~is_wide)
    bat_obs = out[out["is_batter_ball_faced"]].copy()
    bat_obs["_bat_denom"] = 1.0
    bat_obs["_runs_f"] = bat_obs["runs"].astype(float)
    bat_obs["_out_f"] = bat_obs["is_striker_dismissed"].astype(float)
    bat_obs["_dot_f"] = bat_obs["is_dot_bat"].astype(float)
    bat_obs["_bnd_f"] = bat_obs["is_boundary_bat"].astype(float)

    bat_mapped = _compute_lpo_hierarchy(
        obs_df=bat_obs,
        target_df=out,
        player_col="striker_id",
        num_cols=["_runs_f", "_out_f", "_dot_f", "_bnd_f"],
        denom_col="_bat_denom",
        hierarchy=BAT_HIERARCHY,
        out_col_map={
            "_runs_f": "ctx_bat_rpb",
            "_out_f": "ctx_bat_out_prob",
            "_dot_f": "ctx_bat_dot_prob",
            "_bnd_f": "ctx_bat_bnd_prob",
        },
        level_col="ctx_bat_level",
        lpo_n_col="ctx_bat_lpo_n",
        min_cell_n=min_cell_n,
    )
    for col in (
        "ctx_bat_rpb",
        "ctx_bat_out_prob",
        "ctx_bat_dot_prob",
        "ctx_bat_bnd_prob",
        "ctx_bat_level",
        "ctx_bat_lpo_n",
    ):
        out[col] = bat_mapped[col].to_numpy()

    # 2. Bowling LPO baselines (legal balls in denominator, bowler_runs_conceded / wickets in numerator)
    bowl_obs = out.copy()
    bowl_obs["_bowl_denom"] = bowl_obs["is_legal_ball"].astype(float)
    bowl_obs["_conceded_f"] = bowl_obs["bowler_runs_conceded"].astype(float)
    bowl_obs["_wkt_f"] = bowl_obs["is_bowler_wicket"].astype(float)
    bowl_obs["_dot_bowl_f"] = bowl_obs["is_dot_bowl"].astype(float)
    bowl_obs["_bnd_bowl_f"] = bowl_obs["is_boundary_conceded"].astype(float)

    bowl_mapped = _compute_lpo_hierarchy(
        obs_df=bowl_obs,
        target_df=out,
        player_col="bowler_id",
        num_cols=["_conceded_f", "_wkt_f", "_dot_bowl_f", "_bnd_bowl_f"],
        denom_col="_bowl_denom",
        hierarchy=BOWL_HIERARCHY,
        out_col_map={
            "_conceded_f": "ctx_bowl_rpb",
            "_wkt_f": "ctx_bowl_wkt_prob",
            "_dot_bowl_f": "ctx_bowl_dot_prob",
            "_bnd_bowl_f": "ctx_bowl_bnd_prob",
        },
        level_col="ctx_bowl_level",
        lpo_n_col="ctx_bowl_lpo_n",
        min_cell_n=min_cell_n,
    )
    for col in (
        "ctx_bowl_rpb",
        "ctx_bowl_wkt_prob",
        "ctx_bowl_dot_prob",
        "ctx_bowl_bnd_prob",
        "ctx_bowl_level",
        "ctx_bowl_lpo_n",
    ):
        out[col] = bowl_mapped[col].to_numpy()

    return out
