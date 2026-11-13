"""
Independent Forensic Statistical Audit for SupeRR Selector Season 2 (Phase 0.5).
Reads directly from data/raw/ without importing src/ analytical modules as truth.
Generates all quantitative audit CSVs in outputs/model_audit/.
"""

import json
from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
RAW_DIR = ROOT / "data" / "raw"
EXISTING_OUT = ROOT / "outputs"
AUDIT_DIR = Path(__file__).resolve().parent

BOWLER_DISMISSALS = {"Caught", "Bowled", "LBW", "Stump", "Hit Wicket"}
FULL_MEMBERS = {
    "India", "Australia", "England", "South Africa", "New Zealand",
    "Pakistan", "West Indies", "Sri Lanka", "Bangladesh", "Afghanistan",
    "Zimbabwe", "Ireland",
}

CURRENT_TOP10_BAT = [
    "Reeza Hendricks", "Matthew Wade", "Naman Dhir", "Tim David",
    "Sanju Samson", "Shubman Gill", "Mark Chapman", "Glenn Maxwell",
    "Shai Hope", "Mohammad Rizwan",
]
CURRENT_TOP10_BOWL = [
    "Sufiyan Muqeem", "Sai Kishore", "Sunil Narine", "Mohammad Nawaz",
    "Mohit Sharma", "Mustafizur Rahman", "Kuldeep Yadav", "Jasprit Bumrah",
    "Mitchell Santner", "Abrar Ahmed",
]
EARLIER_REF_BAT = [
    "Suryakumar Yadav", "Naman Dhir", "Rinku Singh", "Ashutosh Sharma",
    "Shreyas Iyer", "Nitish Reddy", "Phil Salt", "Tristan Stubbs",
    "Glenn Phillips", "Tim David",
]
EARLIER_REF_BOWL = [
    "Jasprit Bumrah", "Sunil Narine", "Kuldeep Yadav", "Matheesha Pathirana",
    "Jamie Overton", "Jofra Archer", "Gerald Coetzee", "Mustafizur Rahman",
    "Hasan Mahmud", "Varun Chakravarthy",
]


def load_raw():
    return {
        "comp": pd.read_csv(RAW_DIR / "competitions.csv"),
        "teams": pd.read_csv(RAW_DIR / "teams.csv"),
        "matches": pd.read_csv(RAW_DIR / "matches.csv"),
        "pe": pd.read_csv(RAW_DIR / "playing_eleven.csv"),
        "ctpm": pd.read_csv(RAW_DIR / "competition_team_player_mapping.csv"),
        "bbb": pd.read_csv(RAW_DIR / "ball_by_ball.csv", low_memory=False),
    }


def independent_prepare(raw, include_other_t20=False, include_super_overs=False):
    comp = raw["comp"].copy()
    comp["comp_category"] = np.where(
        (comp["match_format"] == "T20") & (comp["comp_name"].str.contains("IPL", na=False)),
        "IPL",
        np.where(comp["match_format"] == "T20", "Other_T20", "T20I"),
    )
    matches = raw["matches"].merge(
        comp[["comp_id", "comp_name", "match_format", "season", "comp_category"]],
        on="comp_id",
        how="left",
    )
    matches["season_year"] = matches["match_date"].str.slice(0, 4).astype(int)
    matches["is_full_member_t20i"] = (
        (matches["comp_category"] == "T20I")
        & matches["home_team"].isin(FULL_MEMBERS)
        & matches["away_team"].isin(FULL_MEMBERS)
    )

    bbb = raw["bbb"].copy()
    bbb["dismissal_type"] = bbb["dismissal_type"].replace(
        {"Obstracting the field": "Obstructing the field"}
    )
    bbb["is_wide"] = bbb["extras_type"] == "wide"
    bbb["is_noball"] = bbb["extras_type"].isin(["Overstep", "other"])
    bbb["is_legal_ball"] = ~(bbb["is_wide"] | bbb["is_noball"])
    bbb["is_batter_ball_faced"] = ~bbb["is_wide"]
    bbb["total_runs"] = bbb["runs"] + bbb["extras1_runs"] + bbb["extras_2_runs"]
    bbb["bowler_runs_conceded"] = bbb["runs"] + np.where(
        bbb["is_wide"] | bbb["is_noball"], bbb["extras1_runs"], 0
    )
    bbb["is_team_wicket"] = bbb["is_wicket"].astype(bool)
    bbb["is_bowler_wicket"] = bbb["is_team_wicket"] & bbb["dismissal_type"].isin(BOWLER_DISMISSALS)

    mcols = [
        "match_id", "comp_id", "comp_name", "match_format", "season", "season_year",
        "comp_category", "is_full_member_t20i", "match_date", "stage", "knock_out",
        "first_inn_revised_overs", "second_inn_revised_overs", "revised_target", "result",
    ]
    bbb = bbb.merge(matches[mcols], on="match_id", how="left")
    if not include_other_t20:
        bbb = bbb[bbb["comp_category"] != "Other_T20"].copy()
    if not include_super_overs:
        bbb = bbb[bbb["innings"].isin([1, 2])].copy()

    bbb = bbb.sort_values(["match_id", "innings", "overid", "over_ball_num"]).reset_index(drop=True)

    # Canonical player lookup keyed strictly by player_id
    p_parts = [
        bbb[["striker_id", "striker_name"]].rename(columns={"striker_id": "player_id", "striker_name": "player_name"}),
        bbb[["non_striker_id", "non_striker_name"]].rename(columns={"non_striker_id": "player_id", "non_striker_name": "player_name"}),
        bbb[["bowler_id", "bowler_name"]].rename(columns={"bowler_id": "player_id", "bowler_name": "player_name"}),
        raw["ctpm"][["player_id", "player_name"]],
    ]
    pl = pd.concat(p_parts, ignore_index=True).dropna()
    pl["player_id"] = pl["player_id"].astype("int64")
    pl = (
        pl.groupby("player_id")["player_name"]
        .agg(lambda s: s.mode().iloc[0] if not s.mode().empty else s.iloc[0])
        .reset_index()
    )
    return bbb, matches, pl


def independent_state_and_pi(bbb: pd.DataFrame) -> pd.DataFrame:
    df = bbb.copy()
    df["inn_max_balls"] = np.where(
        df["innings"] == 1,
        df["first_inn_revised_overs"].fillna(120.0),
        df["second_inn_revised_overs"].fillna(120.0),
    )
    grp = df.groupby(["match_id", "innings"], sort=False)
    df["pre_runs"] = grp["total_runs"].cumsum() - df["total_runs"]
    df["pre_wickets"] = grp["is_team_wicket"].cumsum() - df["is_team_wicket"].astype(int)
    df["legal_int"] = df["is_legal_ball"].astype(int)
    df["pre_legal_balls"] = grp["legal_int"].cumsum() - df["legal_int"]
    df["pre_balls_remaining"] = np.maximum(1.0, df["inn_max_balls"] - df["pre_legal_balls"])
    df["pre_wickets_in_hand"] = np.maximum(0, 10 - df["pre_wickets"])
    df["phase"] = np.where(df["overid"] <= 6, "Powerplay", np.where(df["overid"] <= 15, "Middle", "Death"))
    df["pre_crr"] = np.where(df["pre_legal_balls"] > 0, 6.0 * df["pre_runs"] / df["pre_legal_balls"], 0.0)

    inn1 = df[df["innings"] == 1].groupby("match_id")["total_runs"].sum().rename("inn1_total_runs")
    df = df.merge(inn1, on="match_id", how="left")
    df["target"] = np.where(
        df["innings"] == 2,
        np.where(df["revised_target"].notna(), df["revised_target"], df["inn1_total_runs"] + 1.0),
        np.nan,
    )
    df["runs_needed"] = np.where(df["innings"] == 2, np.maximum(0.0, df["target"] - df["pre_runs"]), np.nan)
    df["pre_rrr"] = np.where(
        df["innings"] == 2,
        np.minimum(36.0, 6.0 * df["runs_needed"] / df["pre_balls_remaining"]),
        np.nan,
    )

    comp_par = (
        df.groupby(["comp_category", "season_year"])
        .agg(tot_r=("total_runs", "sum"), tot_b=("is_legal_ball", "sum"))
        .assign(par_rpo=lambda x: 6.0 * x["tot_r"] / x["tot_b"])
        .reset_index()[["comp_category", "season_year", "par_rpo"]]
    )
    df = df.merge(comp_par, on=["comp_category", "season_year"], how="left")

    exp_wkts = (
        df[df["innings"] == 1]
        .groupby(["comp_category", "overid"])["pre_wickets"]
        .mean()
        .rename("exp_wickets")
        .reset_index()
    )
    df = df.merge(exp_wkts, on=["comp_category", "overid"], how="left")
    df["exp_wickets"] = df["exp_wickets"].fillna(0.0)

    # PI_1
    w_ex = np.maximum(0.0, df["pre_wickets"] - df["exp_wickets"])
    s_col = np.clip(w_ex / 2.2 + np.where((df["overid"] <= 6) & (df["pre_wickets"] >= 2), 0.25, 0.0), 0.0, 1.0)
    crr_def = np.where(df["pre_legal_balls"] >= 18, np.clip((df["par_rpo"] - df["pre_crr"]) / 3.0, 0.0, 1.0), 0.0)
    d1 = np.where(df["overid"] >= 16, np.where(df["pre_wickets"] <= 6, 0.75, 0.45), np.where(df["overid"] >= 12, 0.25, 0.0))
    pi_1 = np.clip(0.50 * s_col + 0.30 * crr_def + 0.20 * d1, 0.0, 1.0)

    # PI_2
    rrr_ratio = np.where(df["innings"] == 2, df["pre_rrr"] / np.maximum(6.0, df["par_rpo"]), 0.0)
    s_rrr = np.clip((rrr_ratio - 0.65) / 0.80, 0.0, 1.0)
    won_d = np.where((rrr_ratio < 0.55) & (df["pre_wickets_in_hand"] >= 5), 0.35, 1.0)
    lost_d = np.where((rrr_ratio > 2.20) & (df["pre_balls_remaining"] > 18), 0.40, 1.0)
    cf_b = np.where(
        (df["innings"] == 2) & (df["pre_balls_remaining"] <= 24) & (df["runs_needed"] > 0)
        & (df["runs_needed"] <= 48) & (rrr_ratio >= 0.75) & (rrr_ratio <= 2.20),
        0.20, 0.0,
    )
    s_w2 = np.where(df["runs_needed"] > 10, np.clip((df["pre_wickets"] - 1.0) / 5.5, 0.0, 1.0), 0.0)
    s_u2 = np.clip((df["inn_max_balls"] - df["pre_balls_remaining"]) / np.maximum(60.0, df["inn_max_balls"]), 0.0, 1.0)
    pi_2 = np.clip((0.50 * s_rrr + 0.30 * s_w2 + 0.20 * s_u2 + cf_b) * won_d * lost_d, 0.0, 1.0)

    df["pressure_index"] = np.where(df["innings"] == 1, pi_1, pi_2)
    df["is_high_pressure"] = df["pressure_index"] >= 0.50
    df["is_low_pressure"] = df["pressure_index"] < 0.35
    df["is_mid_pressure"] = (df["pressure_index"] >= 0.35) & (df["pressure_index"] < 0.50)

    df["comp_tier"] = np.where(
        df["comp_category"] == "IPL", "IPL",
        np.where(df["is_full_member_t20i"], "T20I_Full", "T20I_Assoc"),
    )
    ctx_cols = ["comp_tier", "season_year", "phase"]

    bat_sub = df[df["is_batter_ball_faced"]].copy()
    bat_sub["is_striker_out"] = (bat_sub["is_team_wicket"] & (bat_sub["dismissed_player_id"] == bat_sub["striker_id"])).astype(float)
    bat_par = bat_sub.groupby(ctx_cols).agg(ctx_bat_rpb=("runs", "mean"), ctx_bat_out_prob=("is_striker_out", "mean")).reset_index()
    df = df.merge(bat_par, on=ctx_cols, how="left")

    bowl_par = (
        df.groupby(ctx_cols)
        .agg(br=("bowler_runs_conceded", "sum"), lb=("is_legal_ball", "sum"), bw=("is_bowler_wicket", "sum"))
        .assign(ctx_bowl_rpb=lambda x: x["br"] / x["lb"], ctx_bowl_wkt_prob=lambda x: x["bw"] / x["lb"])
        .reset_index()[ctx_cols + ["ctx_bowl_rpb", "ctx_bowl_wkt_prob"]]
    )
    df = df.merge(bowl_par, on=ctx_cols, how="left")
    return df


def zscore(s):
    sd = s.std(ddof=0)
    return (s - s.mean()) / sd if sd > 0 else pd.Series(0.0, index=s.index)


def compute_all_batters(df, pl):
    bat = df[df["is_batter_ball_faced"]].copy()
    bat["is_out"] = (bat["is_team_wicket"] & (bat["dismissed_player_id"] == bat["striker_id"])).astype(float)
    bat["rae"] = bat["runs"] - bat["ctx_bat_rpb"]
    bat["surv"] = bat["ctx_bat_out_prob"] - bat["is_out"]

    def agg_b(sub, p):
        g = sub.groupby("striker_id").agg(
            balls=("runs", "count"),
            matches=("match_id", "nunique"),
            innings_cnt=("match_id", lambda s: sub.loc[s.index, ["match_id", "innings"]].drop_duplicates().shape[0]),
            runs=("runs", "sum"),
            outs=("is_out", "sum"),
            rae_sum=("rae", "sum"),
            surv_sum=("surv", "sum"),
        ).reset_index()
        g[f"{p}_sr"] = 100.0 * g["runs"] / g["balls"]
        g[f"{p}_rae_100"] = 100.0 * g["rae_sum"] / g["balls"]
        g[f"{p}_surv_100"] = 100.0 * g["surv_sum"] / g["balls"]
        g[f"{p}_impact_100"] = g[f"{p}_rae_100"] + 6.0 * g[f"{p}_surv_100"]
        return g.rename(columns={"balls": f"{p}_balls", "matches": f"{p}_matches", "innings_cnt": f"{p}_innings", "runs": f"{p}_runs", "outs": f"{p}_outs"})

    tot = agg_b(bat, "tot")
    hp = agg_b(bat[bat["is_high_pressure"]], "hp")
    lp = agg_b(bat[bat["is_low_pressure"]], "lp")
    mid = bat[bat["is_mid_pressure"]].groupby("striker_id")["runs"].count().rename("mid_balls").reset_index()

    hp_m = bat[bat["is_high_pressure"]].groupby(["striker_id", "match_id"]).agg(
        mb=("runs", "count"), mrae=("rae", "sum"), msurv=("surv", "sum")
    ).reset_index()
    hp_m = hp_m[hp_m["mb"] >= 6].copy()
    hp_m["beat"] = ((hp_m["mrae"] + 6.0 * hp_m["msurv"]) > 0).astype(float)
    cons = hp_m.groupby("striker_id").agg(hp_qual_matches=("match_id", "nunique"), consistency_rate=("beat", "mean")).reset_index()

    tier_hp = bat[bat["is_high_pressure"]].groupby(["striker_id", "comp_tier"])["runs"].count().unstack(fill_value=0).reset_index()
    for c in ["IPL", "T20I_Full", "T20I_Assoc"]:
        if c not in tier_hp.columns:
            tier_hp[c] = 0
    tier_hp = tier_hp.rename(columns={"IPL": "hp_balls_ipl", "T20I_Full": "hp_balls_t20i_full", "T20I_Assoc": "hp_balls_t20i_assoc"})
    tier_hp["hp_balls_elite"] = tier_hp["hp_balls_ipl"] + tier_hp["hp_balls_t20i_full"]

    last_info = bat.groupby("striker_id").agg(last_match_date=("match_date", "max"), teams_played=("batting_team_id", "nunique")).reset_index()

    m = (
        tot.merge(hp, on="striker_id", how="left")
        .merge(lp, on="striker_id", how="left")
        .merge(mid, on="striker_id", how="left")
        .merge(cons, on="striker_id", how="left")
        .merge(tier_hp, on="striker_id", how="left")
        .merge(last_info, on="striker_id", how="left")
        .merge(pl.rename(columns={"player_id": "striker_id"}), on="striker_id", how="left")
    )
    for col in ["hp_balls", "lp_balls", "mid_balls", "hp_matches", "hp_qual_matches", "hp_balls_ipl", "hp_balls_t20i_full", "hp_balls_t20i_assoc", "hp_balls_elite"]:
        m[col] = m[col].fillna(0).astype(int)

    m["is_eligible_current"] = (
        (m["tot_balls"] >= 300)
        & (m["hp_balls"] >= 120)
        & (m["hp_balls_elite"] >= 80)
        & (m["hp_matches"] >= 10)
        & (m["lp_balls"] >= 60)
        & (m["hp_impact_100"].fillna(-999) > 0)
    )

    elig = m[m["is_eligible_current"]].copy()
    elig["consistency_rate"] = elig["consistency_rate"].fillna(0.5)
    lp_cap = np.maximum(elig["lp_impact_100"], -15.0)
    elig["raw_delta_impact"] = elig["hp_impact_100"] - lp_cap
    w = elig["hp_balls"] / (elig["hp_balls"] + 120.0)
    elig["shrunk_delta_impact"] = w * elig["raw_delta_impact"]
    elig["shrunk_hp_impact"] = w * elig["hp_impact_100"]
    elig["pressure_score"] = (
        0.40 * zscore(elig["shrunk_delta_impact"])
        + 0.40 * zscore(elig["shrunk_hp_impact"])
        + 0.20 * zscore(elig["consistency_rate"])
    )
    elig = elig.sort_values("pressure_score", ascending=False).reset_index(drop=True)
    elig["current_rank"] = np.arange(1, len(elig) + 1)

    m = m.merge(elig[["striker_id", "shrunk_delta_impact", "shrunk_hp_impact", "pressure_score", "current_rank"]], on="striker_id", how="left")
    return m, elig


def compute_all_bowlers(df, pl):
    bowl = df.copy()
    bowl["legal_int"] = bowl["is_legal_ball"].astype(int)
    bowl["wkt_int"] = bowl["is_bowler_wicket"].astype(int)
    bowl["rs"] = bowl["ctx_bowl_rpb"] * bowl["legal_int"] - bowl["bowler_runs_conceded"]
    bowl["wae"] = bowl["wkt_int"] - bowl["ctx_bowl_wkt_prob"] * bowl["legal_int"]

    def agg_w(sub, p):
        g = sub.groupby("bowler_id").agg(
            balls=("legal_int", "sum"),
            matches=("match_id", "nunique"),
            runs=("bowler_runs_conceded", "sum"),
            wkts=("wkt_int", "sum"),
            rs_sum=("rs", "sum"),
            wae_sum=("wae", "sum"),
        ).reset_index()
        g = g[g["balls"] > 0].copy()
        g[f"{p}_er"] = 6.0 * g["runs"] / g["balls"]
        g[f"{p}_rso"] = 6.0 * g["rs_sum"] / g["balls"]
        g[f"{p}_wap_24"] = 24.0 * g["wae_sum"] / g["balls"]
        g[f"{p}_impact_24"] = 4.0 * g[f"{p}_rso"] + 6.0 * g[f"{p}_wap_24"]
        return g.rename(columns={"balls": f"{p}_balls", "matches": f"{p}_matches", "runs": f"{p}_runs", "wkts": f"{p}_wkts"})

    tot = agg_w(bowl, "tot")
    hp = agg_w(bowl[bowl["is_high_pressure"]], "hp")
    lp = agg_w(bowl[bowl["is_low_pressure"]], "lp")
    mid = bowl[bowl["is_mid_pressure"]].groupby("bowler_id")["legal_int"].sum().rename("mid_balls").reset_index()

    hp_m = bowl[bowl["is_high_pressure"]].groupby(["bowler_id", "match_id"]).agg(
        mb=("legal_int", "sum"), mrs=("rs", "sum"), mwae=("wae", "sum")
    ).reset_index()
    hp_m = hp_m[hp_m["mb"] >= 6].copy()
    hp_m["beat"] = ((hp_m["mrs"] + 6.0 * hp_m["mwae"]) > 0).astype(float)
    cons = hp_m.groupby("bowler_id").agg(hp_qual_matches=("match_id", "nunique"), consistency_rate=("beat", "mean")).reset_index()

    tier_hp = bowl[bowl["is_high_pressure"]].groupby(["bowler_id", "comp_tier"])["legal_int"].sum().unstack(fill_value=0).reset_index()
    for c in ["IPL", "T20I_Full", "T20I_Assoc"]:
        if c not in tier_hp.columns:
            tier_hp[c] = 0
    tier_hp = tier_hp.rename(columns={"IPL": "hp_balls_ipl", "T20I_Full": "hp_balls_t20i_full", "T20I_Assoc": "hp_balls_t20i_assoc"})
    tier_hp["hp_balls_elite"] = tier_hp["hp_balls_ipl"] + tier_hp["hp_balls_t20i_full"]

    last_info = bowl.groupby("bowler_id").agg(last_match_date=("match_date", "max"), teams_played=("bowling_team_id", "nunique")).reset_index()

    m = (
        tot.merge(hp, on="bowler_id", how="left")
        .merge(lp, on="bowler_id", how="left")
        .merge(mid, on="bowler_id", how="left")
        .merge(cons, on="bowler_id", how="left")
        .merge(tier_hp, on="bowler_id", how="left")
        .merge(last_info, on="bowler_id", how="left")
        .merge(pl.rename(columns={"player_id": "bowler_id"}), on="bowler_id", how="left")
    )
    for col in ["hp_balls", "lp_balls", "mid_balls", "hp_matches", "hp_qual_matches", "hp_balls_ipl", "hp_balls_t20i_full", "hp_balls_t20i_assoc", "hp_balls_elite"]:
        m[col] = m[col].fillna(0).astype(int)

    m["is_eligible_current"] = (
        (m["tot_balls"] >= 300)
        & (m["hp_balls"] >= 120)
        & (m["hp_balls_elite"] >= 80)
        & (m["hp_matches"] >= 10)
        & (m["lp_balls"] >= 60)
        & (m["hp_impact_24"].fillna(-999) > 0)
    )

    elig = m[m["is_eligible_current"]].copy()
    elig["consistency_rate"] = elig["consistency_rate"].fillna(0.5)
    lp_cap = np.maximum(elig["lp_impact_24"], -10.0)
    elig["raw_delta_impact"] = elig["hp_impact_24"] - lp_cap
    w = elig["hp_balls"] / (elig["hp_balls"] + 120.0)
    elig["shrunk_delta_impact"] = w * elig["raw_delta_impact"]
    elig["shrunk_hp_impact"] = w * elig["hp_impact_24"]
    elig["pressure_score"] = (
        0.40 * zscore(elig["shrunk_delta_impact"])
        + 0.40 * zscore(elig["shrunk_hp_impact"])
        + 0.20 * zscore(elig["consistency_rate"])
    )
    elig = elig.sort_values("pressure_score", ascending=False).reset_index(drop=True)
    elig["current_rank"] = np.arange(1, len(elig) + 1)

    m = m.merge(elig[["bowler_id", "shrunk_delta_impact", "shrunk_hp_impact", "pressure_score", "current_rank"]], on="bowler_id", how="left")
    return m, elig


def main():
    AUDIT_DIR.mkdir(parents=True, exist_ok=True)
    raw = load_raw()

    # 1. Data scope comparison
    scopes = []
    for label, inc_o, inc_so, filt in [
        ("Raw All (incl Other_T20 + SuperOvers)", True, True, None),
        ("No SuperOvers (incl Other_T20)", True, False, None),
        ("Primary Scope (IPL + All T20I, Inn 1-2)", False, False, None),
        ("IPL + Full-Member T20I only", False, False, ["IPL", "T20I_Full"]),
        ("IPL only", False, False, ["IPL"]),
        ("T20I only (All)", False, False, ["T20I_Full", "T20I_Assoc"]),
    ]:
        b_s, _, pl_s = independent_prepare(raw, include_other_t20=inc_o, include_super_overs=inc_so)
        d_s = independent_state_and_pi(b_s)
        if filt is not None:
            d_s = d_s[d_s["comp_tier"].isin(filt)].copy()
        scopes.append({
            "scope": label,
            "deliveries": len(d_s),
            "legal_balls": int(d_s["is_legal_ball"].sum()),
            "matches": int(d_s["match_id"].nunique()),
            "high_pressure_deliveries": int(d_s["is_high_pressure"].sum()),
            "low_pressure_deliveries": int(d_s["is_low_pressure"].sum()),
            "intermediate_excluded_deliveries": int(d_s["is_mid_pressure"].sum()),
            "pct_high_pressure": round(100.0 * d_s["is_high_pressure"].mean(), 2),
            "pct_low_pressure": round(100.0 * d_s["is_low_pressure"].mean(), 2),
            "pct_intermediate": round(100.0 * d_s["is_mid_pressure"].mean(), 2),
        })
    pd.DataFrame(scopes).to_csv(AUDIT_DIR / "data_scope_comparison.csv", index=False)

    # 2. Primary independent recalculation
    bbb, matches, pl = independent_prepare(raw, include_other_t20=False, include_super_overs=False)
    df = independent_state_and_pi(bbb)
    bat_all, bat_elig = compute_all_batters(df, pl)
    bowl_all, bowl_elig = compute_all_bowlers(df, pl)

    # Compare against existing outputs/top10_*.csv
    old_bat = pd.read_csv(EXISTING_OUT / "top10_batters.csv")
    old_bowl = pd.read_csv(EXISTING_OUT / "top10_bowlers.csv")

    bat_val = old_bat[["striker_id", "player_name", "rank", "pressure_score", "hp_impact_100", "lp_impact_100", "hp_balls", "lp_balls", "hp_matches", "hp_qual_matches", "consistency_rate"]].merge(
        bat_all[["striker_id", "current_rank", "pressure_score", "hp_impact_100", "lp_impact_100", "hp_balls", "lp_balls", "mid_balls", "tot_balls", "hp_matches", "hp_innings", "hp_qual_matches", "consistency_rate", "hp_balls_ipl", "hp_balls_t20i_full", "hp_balls_t20i_assoc"]],
        on="striker_id",
        suffixes=("_existing", "_recalc"),
    )
    bat_val["abs_diff_impact"] = bat_val["hp_impact_100_recalc"] - bat_val["lp_impact_100_recalc"]
    bat_val["score_max_abs_err"] = (bat_val["pressure_score_existing"] - bat_val["pressure_score_recalc"]).abs()
    bat_val.to_csv(AUDIT_DIR / "batting_impact_validation.csv", index=False)

    bowl_val = old_bowl[["bowler_id", "player_name", "rank", "pressure_score", "hp_impact_24", "lp_impact_24", "hp_balls", "lp_balls", "hp_matches", "hp_qual_matches", "consistency_rate"]].merge(
        bowl_all[["bowler_id", "current_rank", "pressure_score", "hp_impact_24", "lp_impact_24", "hp_balls", "lp_balls", "mid_balls", "tot_balls", "hp_matches", "hp_qual_matches", "consistency_rate", "hp_balls_ipl", "hp_balls_t20i_full", "hp_balls_t20i_assoc"]],
        on="bowler_id",
        suffixes=("_existing", "_recalc"),
    )
    bowl_val["abs_diff_impact"] = bowl_val["hp_impact_24_recalc"] - bowl_val["lp_impact_24_recalc"]
    bowl_val["score_max_abs_err"] = (bowl_val["pressure_score_existing"] - bowl_val["pressure_score_recalc"]).abs()
    bowl_val.to_csv(AUDIT_DIR / "bowling_impact_validation.csv", index=False)

    # 3. Candidate reconciliation (Current Top 10 vs Earlier Reference Top 10)
    all_bat_names = sorted(set(CURRENT_TOP10_BAT) | set(EARLIER_REF_BAT))
    bat_rec = bat_all[bat_all["player_name"].isin(all_bat_names)].copy()
    bat_rec["in_current_top10"] = bat_rec["player_name"].isin(CURRENT_TOP10_BAT)
    bat_rec["in_earlier_ref"] = bat_rec["player_name"].isin(EARLIER_REF_BAT)
    def _bat_reason(r):
        if r["is_eligible_current"]:
            rk = int(r["current_rank"])
            return "In Current Top 10" if rk <= 10 else f"Eligible, ranked #{rk}"
        reasons = []
        if r["tot_balls"] < 300:
            reasons.append(f"tot_balls={int(r['tot_balls'])}<300")
        if r["hp_balls"] < 120:
            reasons.append(f"hp_balls={int(r['hp_balls'])}<120")
        if r["hp_balls_elite"] < 80:
            reasons.append(f"hp_balls_elite={int(r['hp_balls_elite'])}<80")
        if r["hp_matches"] < 10:
            reasons.append(f"hp_matches={int(r['hp_matches'])}<10")
        if r["lp_balls"] < 60:
            reasons.append(f"lp_balls={int(r['lp_balls'])}<60")
        if pd.isna(r["hp_impact_100"]) or r["hp_impact_100"] <= 0:
            reasons.append("hp_impact_100<=0")
        return "Ineligible: " + "; ".join(reasons)

    bat_rec["exclusion_reason"] = bat_rec.apply(_bat_reason, axis=1)
    bat_rec.sort_values(["in_current_top10", "in_earlier_ref", "current_rank"], ascending=[False, False, True]).to_csv(
        AUDIT_DIR / "batting_candidate_reconciliation.csv", index=False
    )

    all_bowl_names = sorted(set(CURRENT_TOP10_BOWL) | set(EARLIER_REF_BOWL))
    bowl_rec = bowl_all[bowl_all["player_name"].isin(all_bowl_names)].copy()
    bowl_rec["in_current_top10"] = bowl_rec["player_name"].isin(CURRENT_TOP10_BOWL)
    bowl_rec["in_earlier_ref"] = bowl_rec["player_name"].isin(EARLIER_REF_BOWL)

    def _bowl_reason(r):
        if r["is_eligible_current"]:
            rk = int(r["current_rank"])
            return "In Current Top 10" if rk <= 10 else f"Eligible, ranked #{rk}"
        reasons = []
        if r["tot_balls"] < 300:
            reasons.append(f"tot_balls={int(r['tot_balls'])}<300")
        if r["hp_balls"] < 120:
            reasons.append(f"hp_balls={int(r['hp_balls'])}<120")
        if r["hp_balls_elite"] < 80:
            reasons.append(f"hp_balls_elite={int(r['hp_balls_elite'])}<80")
        if r["hp_matches"] < 10:
            reasons.append(f"hp_matches={int(r['hp_matches'])}<10")
        if r["lp_balls"] < 60:
            reasons.append(f"lp_balls={int(r['lp_balls'])}<60")
        if pd.isna(r["hp_impact_24"]) or r["hp_impact_24"] <= 0:
            reasons.append("hp_impact_24<=0")
        return "Ineligible: " + "; ".join(reasons)

    bowl_rec["exclusion_reason"] = bowl_rec.apply(_bowl_reason, axis=1)
    bowl_rec.sort_values(["in_current_top10", "in_earlier_ref", "current_rank"], ascending=[False, False, True]).to_csv(
        AUDIT_DIR / "bowling_candidate_reconciliation.csv", index=False
    )

    # 4. Sample size validation across all 20 current + earlier candidates
    s_bat = bat_rec[["striker_id", "player_name", "tot_balls", "hp_balls", "mid_balls", "lp_balls", "hp_matches", "hp_qual_matches", "hp_balls_ipl", "hp_balls_t20i_full", "hp_balls_t20i_assoc", "is_eligible_current", "current_rank"]].assign(role="Batter").rename(columns={"striker_id": "player_id"})
    s_bowl = bowl_rec[["bowler_id", "player_name", "tot_balls", "hp_balls", "mid_balls", "lp_balls", "hp_matches", "hp_qual_matches", "hp_balls_ipl", "hp_balls_t20i_full", "hp_balls_t20i_assoc", "is_eligible_current", "current_rank"]].assign(role="Bowler").rename(columns={"bowler_id": "player_id"})
    pd.concat([s_bat, s_bowl], ignore_index=True).to_csv(AUDIT_DIR / "sample_size_validation.csv", index=False)

    # 5. Independent Bootstrap Audit: Compare existing unstratified (n=300) vs Stratified (IPL vs T20I, n=500)
    rng = np.random.default_rng(42)
    # Build player-match summaries for eligible pools
    bat_e = df[df["is_batter_ball_faced"] & df["striker_id"].isin(set(bat_elig["striker_id"]))].copy()
    bat_e["is_out"] = (bat_e["is_team_wicket"] & (bat_e["dismissed_player_id"] == bat_e["striker_id"])).astype(float)
    bat_e["imp"] = (bat_e["runs"] - bat_e["ctx_bat_rpb"]) + 6.0 * (bat_e["ctx_bat_out_prob"] - bat_e["is_out"])
    bm = bat_e.groupby(["match_id", "comp_category", "striker_id"]).agg(
        hp_b=("is_high_pressure", "sum"),
        lp_b=("is_low_pressure", "sum"),
        hp_i=("imp", lambda s: s[bat_e.loc[s.index, "is_high_pressure"]].sum()),
        lp_i=("imp", lambda s: s[bat_e.loc[s.index, "is_low_pressure"]].sum()),
    ).reset_index()
    bm["hp_q"] = (bm["hp_b"] >= 6).astype(int)
    bm["hp_bt"] = ((bm["hp_b"] >= 6) & (bm["hp_i"] > 0)).astype(int)

    bowl_e = df[df["bowler_id"].isin(set(bowl_elig["bowler_id"]))].copy()
    bowl_e["legal_int"] = bowl_e["is_legal_ball"].astype(int)
    bowl_e["wkt_int"] = bowl_e["is_bowler_wicket"].astype(int)
    bowl_e["imp"] = (bowl_e["ctx_bowl_rpb"] * bowl_e["legal_int"] - bowl_e["bowler_runs_conceded"]) + 6.0 * (bowl_e["wkt_int"] - bowl_e["ctx_bowl_wkt_prob"] * bowl_e["legal_int"])
    wm = bowl_e.groupby(["match_id", "comp_category", "bowler_id"]).agg(
        hp_b=("legal_int", lambda s: s[bowl_e.loc[s.index, "is_high_pressure"]].sum()),
        lp_b=("legal_int", lambda s: s[bowl_e.loc[s.index, "is_low_pressure"]].sum()),
        hp_i=("imp", lambda s: s[bowl_e.loc[s.index, "is_high_pressure"]].sum()),
        lp_i=("imp", lambda s: s[bowl_e.loc[s.index, "is_low_pressure"]].sum()),
    ).reset_index()
    wm["hp_q"] = (wm["hp_b"] >= 6).astype(int)
    wm["hp_bt"] = ((wm["hp_b"] >= 6) & (wm["hp_i"] > 0)).astype(int)

    ipl_matches = df[df["comp_category"] == "IPL"]["match_id"].unique()
    t20i_matches = df[df["comp_category"] == "T20I"]["match_id"].unique()

    strat_bat_ranks = {pid: [] for pid in bat_elig["striker_id"]}
    strat_bowl_ranks = {pid: [] for pid in bowl_elig["bowler_id"]}
    absent_bat = {pid: 0 for pid in bat_elig["striker_id"]}
    absent_bowl = {pid: 0 for pid in bowl_elig["bowler_id"]}

    n_boot = 500
    for _ in range(n_boot):
        m_ipl = rng.choice(ipl_matches, size=len(ipl_matches), replace=True)
        m_t20i = rng.choice(t20i_matches, size=len(t20i_matches), replace=True)
        mc = pd.Series(np.concatenate([m_ipl, m_t20i])).value_counts().rename("wt")

        # Batters
        bs = bm.merge(mc, left_on="match_id", right_index=True, how="inner")
        for c in ["hp_b", "lp_b", "hp_i", "lp_i", "hp_q", "hp_bt"]:
            bs[c] = bs[c] * bs["wt"]
        bg = bs.groupby("striker_id")[["hp_b", "lp_b", "hp_i", "lp_i", "hp_q", "hp_bt"]].sum()
        bg = bg[(bg["hp_b"] > 0) & (bg["lp_b"] > 0)].copy()
        for pid in strat_bat_ranks:
            if pid not in bg.index:
                absent_bat[pid] += 1
        hpi = 100.0 * bg["hp_i"] / bg["hp_b"]
        lpi = np.maximum(100.0 * bg["lp_i"] / bg["lp_b"], -15.0)
        w = bg["hp_b"] / (bg["hp_b"] + 120.0)
        cs = np.where(bg["hp_q"] > 0, bg["hp_bt"] / bg["hp_q"], 0.5)
        sc = 0.40 * zscore(w * (hpi - lpi)) + 0.40 * zscore(w * hpi) + 0.20 * zscore(pd.Series(cs, index=bg.index))
        rk = sc.rank(ascending=False)
        for pid, r in rk.items():
            strat_bat_ranks[pid].append(r)

        # Bowlers
        ws = wm.merge(mc, left_on="match_id", right_index=True, how="inner")
        for c in ["hp_b", "lp_b", "hp_i", "lp_i", "hp_q", "hp_bt"]:
            ws[c] = ws[c] * ws["wt"]
        wg = ws.groupby("bowler_id")[["hp_b", "lp_b", "hp_i", "lp_i", "hp_q", "hp_bt"]].sum()
        wg = wg[(wg["hp_b"] > 0) & (wg["lp_b"] > 0)].copy()
        for pid in strat_bowl_ranks:
            if pid not in wg.index:
                absent_bowl[pid] += 1
        hpi_w = 24.0 * wg["hp_i"] / wg["hp_b"]
        lpi_w = np.maximum(24.0 * wg["lp_i"] / wg["lp_b"], -10.0)
        w_w = wg["hp_b"] / (wg["hp_b"] + 120.0)
        cs_w = np.where(wg["hp_q"] > 0, wg["hp_bt"] / wg["hp_q"], 0.5)
        sc_w = 0.40 * zscore(w_w * (hpi_w - lpi_w)) + 0.40 * zscore(w_w * hpi_w) + 0.20 * zscore(pd.Series(cs_w, index=wg.index))
        rk_w = sc_w.rank(ascending=False)
        for pid, r in rk_w.items():
            strat_bowl_ranks[pid].append(r)

    boot_rows = []
    for _, r in old_bat.iterrows():
        pid = int(r["striker_id"])
        rks = np.array(strat_bat_ranks[pid])
        boot_rows.append({
            "role": "Batter", "player_id": pid, "player_name": r["player_name"],
            "full_sample_rank": int(r["rank"]),
            "existing_boot_median_n300": r["boot_median_rank"],
            "existing_boot_p05_n300": r["boot_p05_rank"],
            "existing_boot_p95_n300": r["boot_p95_rank"],
            "existing_top10_freq_n300": round(r["prob_top10"], 4),
            "strat_boot_median_n500": float(np.median(rks)),
            "strat_boot_p05_n500": float(np.percentile(rks, 5)),
            "strat_boot_p95_n500": float(np.percentile(rks, 95)),
            "strat_top10_freq_n500": round(float(np.mean(rks <= 10)), 4),
            "absent_iters_n500": absent_bat[pid],
        })
    for _, r in old_bowl.iterrows():
        pid = int(r["bowler_id"])
        rks = np.array(strat_bowl_ranks[pid])
        boot_rows.append({
            "role": "Bowler", "player_id": pid, "player_name": r["player_name"],
            "full_sample_rank": int(r["rank"]),
            "existing_boot_median_n300": r["boot_median_rank"],
            "existing_boot_p05_n300": r["boot_p05_rank"],
            "existing_boot_p95_n300": r["boot_p95_rank"],
            "existing_top10_freq_n300": round(r["prob_top10"], 4),
            "strat_boot_median_n500": float(np.median(rks)),
            "strat_boot_p05_n500": float(np.percentile(rks, 5)),
            "strat_boot_p95_n500": float(np.percentile(rks, 95)),
            "strat_top10_freq_n500": round(float(np.mean(rks <= 10)), 4),
            "absent_iters_n500": absent_bowl[pid],
        })
    pd.DataFrame(boot_rows).to_csv(AUDIT_DIR / "bootstrap_reconciliation.csv", index=False)

    # 6. Eligibility flags (Separate Statistical Leaderboard vs IPL 2027 Practical Feasibility)
    # Check 2025/2026 IPL participation and last match date from raw data
    ipl_25_26 = df[(df["comp_category"] == "IPL") & (df["season_year"] >= 2025)]
    ipl_bat_2526 = set(ipl_25_26["striker_id"].unique())
    ipl_bowl_2526 = set(ipl_25_26["bowler_id"].unique())

    flag_rows = []
    for _, r in old_bat.iterrows():
        pid = int(r["striker_id"])
        info = bat_all[bat_all["striker_id"] == pid].iloc[0]
        flags = []
        if info["hp_balls_ipl"] == 0:
            flags.append("Zero IPL high-pressure balls")
        elif info["hp_balls_ipl"] < 50:
            flags.append(f"Low IPL HP exposure ({info['hp_balls_ipl']} balls)")
        if pid not in ipl_bat_2526:
            flags.append("No IPL 2025-2026 batting record in dataset")
        if info["last_match_date"] < "2026-01-01":
            flags.append(f"Last dataset match {info['last_match_date']} (check retirement/active status)")
        if info["hp_qual_matches"] < 10:
            flags.append(f"Only {info['hp_qual_matches']} qualifying matches (>=6 HP balls) for consistency")
        if info["player_name"] in {"Mohammad Rizwan"}:
            flags.append("Pakistan national (practical IPL auction restriction; verify separately)")
        flag_rows.append({
            "role": "Batter", "current_rank": int(r["rank"]), "player_id": pid, "player_name": info["player_name"],
            "last_match_date": info["last_match_date"], "in_ipl_2025_2026": pid in ipl_bat_2526,
            "hp_balls_ipl": info["hp_balls_ipl"], "hp_balls_t20i_full": info["hp_balls_t20i_full"],
            "hp_balls_t20i_assoc": info["hp_balls_t20i_assoc"], "hp_qual_matches": info["hp_qual_matches"],
            "flags": "; ".join(flags) if flags else "Clear in dataset (verify IPL 2027 auction status externally)",
        })
    for _, r in old_bowl.iterrows():
        pid = int(r["bowler_id"])
        info = bowl_all[bowl_all["bowler_id"] == pid].iloc[0]
        flags = []
        if info["hp_balls_ipl"] == 0:
            flags.append("Zero IPL high-pressure balls")
        elif info["hp_balls_ipl"] < 50:
            flags.append(f"Low IPL HP exposure ({info['hp_balls_ipl']} balls)")
        if pid not in ipl_bowl_2526:
            flags.append("No IPL 2025-2026 bowling record in dataset")
        if info["last_match_date"] < "2026-01-01":
            flags.append(f"Last dataset match {info['last_match_date']} (check active status)")
        if info["hp_qual_matches"] < 10:
            flags.append(f"Only {info['hp_qual_matches']} qualifying matches (>=6 HP balls) for consistency")
        if info["player_name"] in {"Sufiyan Muqeem", "Mohammad Nawaz", "Abrar Ahmed"}:
            flags.append("Pakistan national (practical IPL auction restriction; verify separately)")
        flag_rows.append({
            "role": "Bowler", "current_rank": int(r["rank"]), "player_id": pid, "player_name": info["player_name"],
            "last_match_date": info["last_match_date"], "in_ipl_2025_2026": pid in ipl_bowl_2526,
            "hp_balls_ipl": info["hp_balls_ipl"], "hp_balls_t20i_full": info["hp_balls_t20i_full"],
            "hp_balls_t20i_assoc": info["hp_balls_t20i_assoc"], "hp_qual_matches": info["hp_qual_matches"],
            "flags": "; ".join(flags) if flags else "Clear in dataset (verify IPL 2027 auction status externally)",
        })
    pd.DataFrame(flag_rows).to_csv(AUDIT_DIR / "eligibility_flags.csv", index=False)
    print("Independent audit CSVs generated successfully.")


if __name__ == "__main__":
    main()
