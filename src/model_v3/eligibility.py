"""Sample-size eligibility gates, gate-sweep sensitivity, and near-miss exposure for Model V2."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Sequence, Tuple
import numpy as np
import pandas as pd

from .shrinkage import compute_kish_neff_summary


@dataclass(frozen=True)
class EligibilityGate:
    """Configurable sample-size eligibility criteria (NO lp_balls >= 60 trap)."""

    name: str
    min_total_balls: int = 300
    min_hp_balls: int = 120
    min_hp_matches: int = 10
    min_hp_elite_balls: int = 0
    min_pressure_neff: float = 0.0


BENCHMARK_GATE = EligibilityGate(
    name="benchmark_300_120_10",
    min_total_balls=300,
    min_hp_balls=120,
    min_hp_matches=10,
)

ELIGIBILITY_GATE_SWEEP: Tuple[EligibilityGate, ...] = (
    EligibilityGate("lenient_200_80_8", min_total_balls=200, min_hp_balls=80, min_hp_matches=8),
    EligibilityGate("benchmark_300_120_10", min_total_balls=300, min_hp_balls=120, min_hp_matches=10),
    EligibilityGate("strict_400_150_12", min_total_balls=400, min_hp_balls=150, min_hp_matches=12),
    EligibilityGate("very_strict_500_180_15", min_total_balls=500, min_hp_balls=180, min_hp_matches=15),
    EligibilityGate(
        "neff_300_150neff_10",
        min_total_balls=300,
        min_hp_balls=0,
        min_hp_matches=10,
        min_pressure_neff=150.0,
    ),
)


def compute_player_exposure_table(
    df: pd.DataFrame,
    player_lookup: pd.DataFrame,
    role: str,
) -> pd.DataFrame:
    """
    Compute complete sample-size, format-split, and Kish N_eff exposure metrics
    per player_id without discarding any candidates.
    """
    if role == "batter":
        sub = df[df["is_batter_ball_faced"]].copy()
        id_col = "striker_id"
        sub["_ball_unit"] = 1
        hp_col = "is_high_pressure_bat" if "is_high_pressure_bat" in sub.columns else "is_high_pressure"
        lp_col = "is_low_pressure_bat" if "is_low_pressure_bat" in sub.columns else "is_low_pressure"
        int_col = "is_intermediate_pressure_bat" if "is_intermediate_pressure_bat" in sub.columns else "is_intermediate_pressure"
    elif role == "bowler":
        sub = df.copy()
        id_col = "bowler_id"
        sub["_ball_unit"] = sub["is_legal_ball"].astype(int)
        hp_col = "is_high_pressure_bowl" if "is_high_pressure_bowl" in sub.columns else "is_high_pressure"
        lp_col = "is_low_pressure_bowl" if "is_low_pressure_bowl" in sub.columns else "is_low_pressure"
        int_col = "is_intermediate_pressure_bowl" if "is_intermediate_pressure_bowl" in sub.columns else "is_intermediate_pressure"
    else:
        raise ValueError(f"Unsupported role: {role!r}")

    sub["_hp_ball"] = np.where(sub[hp_col], sub["_ball_unit"], 0)
    sub["_lp_ball"] = np.where(sub[lp_col], sub["_ball_unit"], 0)
    sub["_int_ball"] = np.where(sub[int_col], sub["_ball_unit"], 0)
    sub["_hp_elite"] = np.where(
        sub[hp_col] & sub["comp_tier"].isin(["IPL", "T20I_Full"]),
        sub["_ball_unit"],
        0,
    )
    sub["_hp_ipl"] = np.where(
        sub[hp_col] & (sub["comp_category"] == "IPL"),
        sub["_ball_unit"],
        0,
    )
    sub["_hp_t20i"] = np.where(
        sub[hp_col] & (sub["comp_category"] == "T20I"),
        sub["_ball_unit"],
        0,
    )
    sub["_tot_ipl"] = np.where(sub["comp_category"] == "IPL", sub["_ball_unit"], 0)
    sub["_tot_t20i"] = np.where(sub["comp_category"] == "T20I", sub["_ball_unit"], 0)

    tot_agg = sub.groupby(id_col, as_index=False).agg(
        tot_balls=("_ball_unit", "sum"),
        tot_matches=("match_id", "nunique"),
        hp_balls=("_hp_ball", "sum"),
        lp_balls=("_lp_ball", "sum"),
        interm_balls=("_int_ball", "sum"),
        hp_balls_elite=("_hp_elite", "sum"),
        hp_balls_ipl=("_hp_ipl", "sum"),
        hp_balls_t20i=("_hp_t20i", "sum"),
        tot_balls_ipl=("_tot_ipl", "sum"),
        tot_balls_t20i=("_tot_t20i", "sum"),
        last_match_date=("match_date", "max"),
    )

    hp_match_col = "boot_match_instance_id" if "boot_match_instance_id" in sub.columns else "match_id"
    hp_sub = sub[sub[hp_col] & (sub["_ball_unit"] > 0)]
    hp_m = (
        hp_sub.groupby(id_col)[hp_match_col]
        .nunique()
        .rename("hp_matches")
        .reset_index()
    )

    # Qualifying HP matches (>= 6 HP balls in a single match)
    m_hp_balls = (
        hp_sub.groupby([id_col, hp_match_col], as_index=False)["_ball_unit"]
        .sum()
        .rename(columns={"_ball_unit": "m_hp_balls"})
    )
    hp_qual = (
        m_hp_balls[m_hp_balls["m_hp_balls"] >= 6]
        .groupby(id_col)[hp_match_col]
        .nunique()
        .rename("hp_qual_matches")
        .reset_index()
    )

    neff = compute_kish_neff_summary(df, role=role)

    out = (
        tot_agg.merge(hp_m, on=id_col, how="left")
        .merge(hp_qual, on=id_col, how="left")
        .merge(neff, on=id_col, how="left")
        .merge(
            player_lookup.rename(columns={"player_id": id_col}),
            on=id_col,
            how="left",
        )
    )
    for col in ("hp_matches", "hp_qual_matches"):
        out[col] = out[col].fillna(0).astype(int)
    for col in (
        "pressure_exposure_sum",
        "pressure_neff",
        "normal_exposure_sum",
        "normal_neff",
    ):
        out[col] = out[col].fillna(0.0).astype(float)

    ipl_2526_ids = set(
        sub.loc[
            (sub["comp_category"] == "IPL") & (sub["season_year"] >= 2025),
            id_col,
        ].unique()
    )
    out["in_ipl_2025_2026"] = out[id_col].isin(ipl_2526_ids)
    out = out[out["tot_balls"] > 0].reset_index(drop=True)
    return out


def apply_eligibility_gate(
    exposure_df: pd.DataFrame,
    gate: EligibilityGate = BENCHMARK_GATE,
) -> pd.Series:
    """Return boolean mask indicating whether each player satisfies `gate`."""
    return (
        (exposure_df["tot_balls"] >= gate.min_total_balls)
        & (exposure_df["hp_balls"] >= gate.min_hp_balls)
        & (exposure_df["hp_matches"] >= gate.min_hp_matches)
        & (exposure_df["hp_balls_elite"] >= gate.min_hp_elite_balls)
        & (exposure_df["pressure_neff"] >= gate.min_pressure_neff)
    )


def identify_near_misses(
    player_df: pd.DataFrame,
    gate: EligibilityGate = BENCHMARK_GATE,
    id_col: str = "striker_id",
    score_col: str | None = None,
) -> pd.DataFrame:
    """
    Expose high-performing or near-threshold candidates who narrowly miss the
    benchmark gate (e.g., Phil Salt missing hp_balls=112<120 and hp_matches=9<10
    despite 1,643 total balls and N_eff=354.8), plus note V1 lp_balls<60 rescues
    (e.g., Ashutosh Sharma).
    """
    pass_v2 = apply_eligibility_gate(player_df, gate)
    near_mask = (~pass_v2) & (
        (player_df["tot_balls"] >= int(0.75 * gate.min_total_balls))
        & (
            (player_df["hp_balls"] >= int(0.70 * gate.min_hp_balls))
            | (player_df["pressure_neff"] >= float(gate.min_hp_balls))
        )
        & (player_df["hp_matches"] >= max(1, gate.min_hp_matches - 3))
    )
    rescued_mask = pass_v2 & (player_df["lp_balls"] < 60)

    rows = []
    for flag, subset in [("near_miss", player_df[near_mask]), ("rescued_from_v1_lp_trap", player_df[rescued_mask])]:
        for _, r in subset.iterrows():
            reasons: List[str] = []
            if r["tot_balls"] < gate.min_total_balls:
                reasons.append(f"tot_balls={int(r['tot_balls'])}<{gate.min_total_balls}")
            if r["hp_balls"] < gate.min_hp_balls:
                reasons.append(f"hp_balls={int(r['hp_balls'])}<{gate.min_hp_balls}")
            if r["hp_matches"] < gate.min_hp_matches:
                reasons.append(f"hp_matches={int(r['hp_matches'])}<{gate.min_hp_matches}")
            if flag == "rescued_from_v1_lp_trap":
                reasons.append(f"V1 excluded lp_balls={int(r['lp_balls'])}<60; V2 eligible")
            rows.append(
                {
                    id_col: int(r[id_col]),
                    "player_name": r.get("player_name", ""),
                    "status": flag,
                    "tot_balls": int(r["tot_balls"]),
                    "hp_balls": int(r["hp_balls"]),
                    "lp_balls": int(r["lp_balls"]),
                    "hp_matches": int(r["hp_matches"]),
                    "pressure_neff": round(float(r["pressure_neff"]), 2),
                    "metric_value": float(r[score_col]) if score_col and score_col in r else np.nan,
                    "reason": "; ".join(reasons),
                }
            )
    if not rows:
        return pd.DataFrame(
            columns=[
                id_col,
                "player_name",
                "status",
                "tot_balls",
                "hp_balls",
                "lp_balls",
                "hp_matches",
                "pressure_neff",
                "metric_value",
                "reason",
            ]
        )
    return pd.DataFrame(rows).sort_values(["status", "pressure_neff"], ascending=[True, False]).reset_index(drop=True)
