"""Dynamic batting role and batter feature engineering for Model V2."""

from __future__ import annotations

import numpy as np
import pandas as pd


ROLE_TOP = "Top 1-3"
ROLE_MIDDLE = "Middle 4-5"
ROLE_FINISHER = "Finisher 6+"
ROLE_UNKNOWN = "Unknown"


def order_to_batting_role(order: pd.Series | float | int) -> pd.Series | str:
    """Map numeric batting order (1..13) to Top 1-3, Middle 4-5, or Finisher 6+."""
    if isinstance(order, pd.Series):
        vals = pd.to_numeric(order, errors="coerce")
        return pd.Series(
            np.where(
                vals.isna(),
                ROLE_UNKNOWN,
                np.where(
                    vals <= 3,
                    ROLE_TOP,
                    np.where(vals <= 5, ROLE_MIDDLE, ROLE_FINISHER),
                ),
            ),
            index=order.index,
        )
    if pd.isna(order):
        return ROLE_UNKNOWN
    val = float(order)
    if val <= 3:
        return ROLE_TOP
    if val <= 5:
        return ROLE_MIDDLE
    return ROLE_FINISHER


def add_batting_features(
    df: pd.DataFrame, playing_eleven: pd.DataFrame
) -> pd.DataFrame:
    """
    Assign dynamic batting roles (Top 1-3, Middle 4-5, Finisher 6+) combining
    playing_eleven.csv team-sheet order with realized delivery batting_order,
    and flag uncertain or mismatched roles.
    """
    out = df.copy()
    pe_cols = ["match_id", "team_id", "player_id", "batting_order"]
    optional_cols = [c for c in ("is_played", "is_impact") if c in playing_eleven.columns]
    pe_sub = playing_eleven[pe_cols + optional_cols].rename(
        columns={
            "team_id": "batting_team_id",
            "player_id": "striker_id",
            "batting_order": "pe_batting_order",
            "is_played": "pe_is_played",
            "is_impact": "pe_is_impact",
        }
    )

    # Ensure unique join key even if caller passed un-deduplicated pe
    pe_sub = pe_sub.drop_duplicates(
        subset=["match_id", "batting_team_id", "striker_id"], keep="first"
    )

    drop_existing = [
        c
        for c in (
            "pe_batting_order",
            "pe_is_played",
            "pe_is_impact",
            "batting_role_delivery",
            "batting_role_pe",
            "batting_role",
            "is_role_mismatch",
            "is_role_missing_pe",
            "is_role_uncertain",
            "batting_hand",
        )
        if c in out.columns
    ]
    if drop_existing:
        out = out.drop(columns=drop_existing)

    out = out.merge(
        pe_sub, on=["match_id", "batting_team_id", "striker_id"], how="left"
    )

    out["batting_role_delivery"] = order_to_batting_role(out["batting_order"])
    out["batting_role_pe"] = order_to_batting_role(out["pe_batting_order"])

    out["is_role_missing_pe"] = out["batting_role_pe"] == ROLE_UNKNOWN
    out["is_role_mismatch"] = (~out["is_role_missing_pe"]) & (
        out["batting_role_delivery"] != ROLE_UNKNOWN
    ) & (out["batting_role_delivery"] != out["batting_role_pe"])
    out["is_role_uncertain"] = out["is_role_mismatch"] | out["is_role_missing_pe"]

    # Dynamic realized batting role takes precedence, falling back to PE if needed
    out["batting_role"] = np.where(
        out["batting_role_delivery"] != ROLE_UNKNOWN,
        out["batting_role_delivery"],
        out["batting_role_pe"],
    )

    if "batting_type" in out.columns:
        out["batting_hand"] = out["batting_type"].fillna(ROLE_UNKNOWN)
    else:
        out["batting_hand"] = ROLE_UNKNOWN

    return out


def summarize_batter_roles(df: pd.DataFrame) -> pd.DataFrame:
    """Summarize each striker_id's role distribution and role-uncertainty flags."""
    bat = df[df["is_batter_ball_faced"]].copy()
    bat["_is_top"] = (bat["batting_role"] == ROLE_TOP).astype(int)
    bat["_is_mid"] = (bat["batting_role"] == ROLE_MIDDLE).astype(int)
    bat["_is_fin"] = (bat["batting_role"] == ROLE_FINISHER).astype(int)
    bat["_unc"] = bat["is_role_uncertain"].astype(int)

    agg = (
        bat.groupby("striker_id")
        .agg(
            balls_faced=("runs", "count"),
            top_balls=("_is_top", "sum"),
            middle_balls=("_is_mid", "sum"),
            finisher_balls=("_is_fin", "sum"),
            role_uncertain_balls=("_unc", "sum"),
            median_batting_order=("batting_order", "median"),
        )
        .reset_index()
    )
    agg["top_share"] = agg["top_balls"] / agg["balls_faced"]
    agg["middle_share"] = agg["middle_balls"] / agg["balls_faced"]
    agg["finisher_share"] = agg["finisher_balls"] / agg["balls_faced"]
    agg["role_uncertain_rate"] = agg["role_uncertain_balls"] / agg["balls_faced"]

    role_counts = agg[["top_balls", "middle_balls", "finisher_balls"]].to_numpy()
    role_names = np.array([ROLE_TOP, ROLE_MIDDLE, ROLE_FINISHER])
    agg["primary_batting_role"] = role_names[np.argmax(role_counts, axis=1)]

    return agg
