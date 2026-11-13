"""Chronological pre-match rolling Elo opponent strength for Model V2."""

from __future__ import annotations

from typing import Dict, Tuple
import numpy as np
import pandas as pd


DEFAULT_BASE_ELO: float = 1500.0
DEFAULT_K_FACTOR: float = 24.0
DEFAULT_ELO_SCALE: float = 400.0
DEFAULT_LOW_TIER_CUTOFF: float = 1480.0
DEFAULT_HIGH_TIER_CUTOFF: float = 1525.0


def _expected_score(rating_a: float, rating_b: float, scale: float = DEFAULT_ELO_SCALE) -> float:
    return 1.0 / (1.0 + 10.0 ** ((rating_b - rating_a) / scale))


def classify_elo_tier(
    elo: pd.Series,
    low_cutoff: float = DEFAULT_LOW_TIER_CUTOFF,
    high_cutoff: float = DEFAULT_HIGH_TIER_CUTOFF,
) -> pd.Series:
    """
    Map pre-match Elo into deterministic zero-look-ahead opponent tiers:
    'Low' (< 1480), 'Mid' [1480, 1525), 'High' (>= 1525).
    """
    return pd.Series(
        np.where(
            elo < low_cutoff,
            "Low",
            np.where(elo < high_cutoff, "Mid", "High"),
        ),
        index=elo.index,
    )


def compute_pre_match_elo(
    matches: pd.DataFrame,
    base_elo: float = DEFAULT_BASE_ELO,
    k_factor: float = DEFAULT_K_FACTOR,
    elo_scale: float = DEFAULT_ELO_SCALE,
) -> pd.DataFrame:
    """
    Compute strict pre-match rolling Elo ratings SEPARATELY for each comp_category
    (e.g., IPL and T20I never share ratings).

    Strict leakage prevention:
    - Matches are sorted by (comp_category, match_date, match_id).
    - All matches on date D read team ratings produced ONLY by matches with
      match_date < D.
    - Rating updates from date D are buffered and applied AFTER every match on date D
      has recorded its pre-match Elos.
    - 'No Result' / 'Match Abandoned' matches do not alter Elo; 'Match Tied' with
      missing win_team_id is scored 0.5 / 0.5.
    """
    m = matches.copy()
    m["_match_date_dt"] = pd.to_datetime(m["match_date"])
    sort_cols = ["comp_category", "_match_date_dt", "match_id"]
    if "match_number" in m.columns:
        m["_match_num_str"] = m["match_number"].astype(str)
        sort_cols = ["comp_category", "_match_date_dt", "_match_num_str", "match_id"]
    m = m.sort_values(sort_cols).reset_index(drop=True)

    ratings_by_comp: Dict[str, Dict[int, float]] = {}
    records = []

    for (comp_cat, _dt), day_df in m.groupby(["comp_category", "_match_date_dt"], sort=False):
        ratings = ratings_by_comp.setdefault(str(comp_cat), {})
        day_deltas: Dict[int, float] = {}

        for row in day_df.itertuples(index=False):
            h_id = int(row.home_team_id)
            a_id = int(row.away_team_id)
            h_pre = float(ratings.get(h_id, base_elo))
            a_pre = float(ratings.get(a_id, base_elo))

            records.append(
                {
                    "match_id": int(row.match_id),
                    "comp_category": comp_cat,
                    "match_date": row.match_date,
                    "home_team_id": h_id,
                    "away_team_id": a_id,
                    "home_pre_elo": h_pre,
                    "away_pre_elo": a_pre,
                    "elo_diff_home": h_pre - a_pre,
                }
            )

            res_str = str(getattr(row, "result", "") or "")
            if res_str in ("No Result", "Match Abandoned"):
                continue

            win_id = getattr(row, "win_team_id", np.nan)
            if pd.isna(win_id):
                if "tie" in res_str.lower():
                    s_home = 0.5
                else:
                    continue
            else:
                win_int = int(win_id)
                if win_int == h_id:
                    s_home = 1.0
                elif win_int == a_id:
                    s_home = 0.0
                else:
                    continue

            e_home = _expected_score(h_pre, a_pre, scale=elo_scale)
            delta = k_factor * (s_home - e_home)
            day_deltas[h_id] = day_deltas.get(h_id, 0.0) + delta
            day_deltas[a_id] = day_deltas.get(a_id, 0.0) - delta

        for team_id, d in day_deltas.items():
            ratings[team_id] = ratings.get(team_id, base_elo) + d

    return pd.DataFrame(records)


def attach_opponent_elo(
    df: pd.DataFrame,
    matches: pd.DataFrame | None = None,
    match_elo: pd.DataFrame | None = None,
    base_elo: float = DEFAULT_BASE_ELO,
    k_factor: float = DEFAULT_K_FACTOR,
    low_cutoff: float = DEFAULT_LOW_TIER_CUTOFF,
    high_cutoff: float = DEFAULT_HIGH_TIER_CUTOFF,
) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """
    Attach pre-match Elo ratings and opponent tiers to every delivery so bootstrap
    resampling can keep pre_match_opp_elo_* fixed without recomputing from shuffled draws.

    Returns (df_with_elo, match_elo_table).
    """
    if match_elo is None:
        if matches is None:
            raise ValueError("Either matches or match_elo must be provided.")
        match_elo = compute_pre_match_elo(
            matches, base_elo=base_elo, k_factor=k_factor
        )

    out = df.merge(
        match_elo[
            [
                "match_id",
                "home_team_id",
                "away_team_id",
                "home_pre_elo",
                "away_pre_elo",
            ]
        ],
        on="match_id",
        how="left",
        suffixes=("", "_elo_ref"),
    )

    bat_is_home = out["batting_team_id"] == out["home_team_id"]
    out["pre_match_bat_team_elo"] = np.where(
        bat_is_home, out["home_pre_elo"], out["away_pre_elo"]
    )
    out["pre_match_bowl_team_elo"] = np.where(
        bat_is_home, out["away_pre_elo"], out["home_pre_elo"]
    )

    # Role-explicit opponent Elos (for batter, opponent is bowling_team; for bowler, batting_team)
    out["pre_match_opp_elo_bat"] = out["pre_match_bowl_team_elo"]
    out["pre_match_opp_elo_bowl"] = out["pre_match_bat_team_elo"]
    # Alias kept for generic inspection (opponent faced by the active batting side)
    out["pre_match_opp_elo"] = out["pre_match_opp_elo_bat"]

    out["opp_tier_bat"] = classify_elo_tier(
        out["pre_match_opp_elo_bat"], low_cutoff=low_cutoff, high_cutoff=high_cutoff
    )
    out["opp_tier_bowl"] = classify_elo_tier(
        out["pre_match_opp_elo_bowl"], low_cutoff=low_cutoff, high_cutoff=high_cutoff
    )

    drop_cols = [c for c in ("home_team_id_elo_ref", "away_team_id_elo_ref") if c in out.columns]
    if drop_cols:
        out = out.drop(columns=drop_cols)

    return out, match_elo
