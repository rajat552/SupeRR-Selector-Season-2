"""Publication-ready 12-chart visualization suite for Model V3."""

from __future__ import annotations

from pathlib import Path
from typing import Dict
import numpy as np
import pandas as pd
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches


RR_PINK = "#E61E64"
RR_NAVY = "#1D3557"
RR_SLATE = "#457B9D"
RR_TEAL = "#2A9D8F"
RR_GOLD = "#E9C46A"
RR_ORANGE = "#F4A261"
RR_GRAY = "#6C757D"
RR_LIGHT = "#F8F9FA"


def _setup_style() -> None:
    plt.rcParams.update(
        {
            "figure.facecolor": "white",
            "axes.facecolor": "white",
            "axes.edgecolor": "#CCCCCC",
            "axes.grid": True,
            "grid.alpha": 0.25,
            "grid.linestyle": "--",
            "font.size": 9.5,
            "axes.titlesize": 11.5,
            "axes.titleweight": "bold",
            "axes.labelsize": 10,
        }
    )


def _save(fig: plt.Figure, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(path, dpi=220, bbox_inches="tight")
    plt.close(fig)


def plot_01_02_top10_ranking(
    top10_df: pd.DataFrame,
    role: str,
    out_path: Path,
) -> None:
    """01 / 02: Top 10 ranking with Rank 1 at top, observed vs EB-shrunk impact, N and Kish N_eff."""
    _setup_style()
    df_p = top10_df.sort_values("rank", ascending=True).reset_index(drop=True)
    y = np.arange(len(df_p))

    obs_col = "wp_impact_100" if role == "batter" else "wp_impact_24"
    unit_lbl = "per 100 Balls" if role == "batter" else "per 24 Legal Balls"

    fig, ax = plt.subplots(figsize=(11.5, 6.8))
    ax.barh(
        y - 0.16,
        df_p[obs_col],
        height=0.30,
        color=RR_SLATE,
        alpha=0.45,
        label="Observed Pressure-Weighted Impact",
    )
    ax.barh(
        y + 0.16,
        df_p["shrunk_wp_impact"],
        height=0.30,
        color=RR_PINK,
        alpha=0.92,
        label="EB-Shrunk Pressure Impact (via Kish $N_{eff}$)",
    )

    ax.axvline(0.0, color=RR_NAVY, linewidth=0.9, linestyle="--")
    labels = [
        f"#{int(r['rank'])}  {r['player_name']}  (Score: {r['pressure_score']:+.2f})"
        for _, r in df_p.iterrows()
    ]
    ax.set_yticks(y)
    ax.set_yticklabels(labels, fontsize=9.5, fontweight="bold")
    ax.invert_yaxis()  # Rank 1 at top!

    max_val = float(max(df_p[obs_col].max(), df_p["shrunk_wp_impact"].max(), 1.0))
    ax.set_xlim(min(0.0, float(df_p["shrunk_wp_impact"].min()) - 1.0), max_val * 1.38)

    for idx, r in df_p.iterrows():
        x_txt = max(float(r[obs_col]), float(r["shrunk_wp_impact"])) + max_val * 0.02
        ax.text(
            x_txt,
            idx,
            f"N_hp={int(r['hp_balls'])}, N_eff={r['pressure_neff']:.0f}, EB-Cons={r['eb_consistency']*100:.1f}%",
            va="center",
            fontsize=8.2,
            color=RR_NAVY,
        )

    title_role = "Batters" if role == "batter" else "Bowlers"
    ax.set_xlabel(f"Context-Adjusted Pressure Impact ({unit_lbl})")
    ax.set_title(
        f"Model V3 Top 10 {title_role} Under Pressure (Rank 1 at Top)\n"
        "Observed vs Empirical-Bayes Shrunk Impact, Sample Size (N_hp) & Kish N_eff"
    )
    ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.11), ncol=2, frameon=True)
    _save(fig, out_path)


def plot_03_pressure_vs_normal_impact(
    bat_all: pd.DataFrame,
    bowl_all: pd.DataFrame,
    out_path: Path,
) -> None:
    """03: Shrunk Pressure Impact vs Shrunk Normal Impact (no elite-baseline penalty)."""
    _setup_style()
    fig, axes = plt.subplots(1, 2, figsize=(14.0, 6.2))

    # Hand-tuned collision-free offsets (dx, dy) in points
    bat_offsets = {
        "Tim David": (6, 4),
        "Dinesh Karthik": (6, 4),
        "Naman Dhir": (-15, 10),
        "Matthew Wade": (-95, 6),
        "Reeza Hendricks": (6, -14),
        "Shashank Singh": (6, 6),
        "Heinrich Klaasen": (6, -12),
        "Rinku Singh": (6, 4),
        "Andre Russell": (-85, -12),
        "Ashutosh Sharma": (6, -12),
        "Suryakumar Yadav": (6, -4),
    }

    bowl_offsets = {
        "Sunil Narine": (-85, 8),
        "Jasprit Bumrah": (6, 4),
        "Jamie Overton": (-15, 10),
        "Mustafizur Rahman": (6, -14),
        "Mohit Sharma": (-85, -12),
        "Sai Kishore": (-75, 8),
        "Sufiyan Muqeem": (-12, -15),
        "Mohsin Khan": (6, 8),
        "Mohammad Nawaz": (6, -14),
        "Josh Hazlewood": (6, -10),
        "Varun Chakravarthy": (6, -2),
        "Kuldeep Yadav": (6, 4),
    }

    specs = [
        (
            axes[0],
            bat_all,
            "Batters (Impact per 100 Balls)",
            {"Ashutosh Sharma", "Suryakumar Yadav", "Rinku Singh", "Tim David", "Matthew Wade", "Naman Dhir"},
            bat_offsets,
        ),
        (
            axes[1],
            bowl_all,
            "Bowlers (Impact per 24 Legal Balls)",
            {"Jasprit Bumrah", "Sunil Narine", "Varun Chakravarthy", "Mustafizur Rahman", "Sai Kishore", "Sufiyan Muqeem", "Mohit Sharma"},
            bowl_offsets,
        ),
    ]

    for ax, df_r, subtitle, spot_names, offsets_map in specs:
        top10 = df_r[df_r["rank"] <= 10]
        rest = df_r[df_r["rank"] > 10]
        ax.scatter(
            rest["shrunk_norm_impact"],
            rest["shrunk_wp_impact"],
            s=32,
            color=RR_SLATE,
            alpha=0.45,
            label="Eligible Pool (Rank > 10)",
        )
        ax.scatter(
            top10["shrunk_norm_impact"],
            top10["shrunk_wp_impact"],
            s=75,
            color=RR_PINK,
            edgecolor=RR_NAVY,
            linewidth=0.8,
            zorder=4,
            label="Top 10 Ranked",
        )
        lim_min = min(float(df_r["shrunk_norm_impact"].min()), float(df_r["shrunk_wp_impact"].min())) - 2
        lim_max = max(float(df_r["shrunk_norm_impact"].max()), float(df_r["shrunk_wp_impact"].max())) + 2
        ax.plot([lim_min, lim_max], [lim_min, lim_max], color=RR_GRAY, linestyle="--", linewidth=1, label="Maintenance Line (HP = Normal)")
        ax.axhline(0, color="#BBBBBB", linewidth=0.8)
        ax.axvline(0, color="#BBBBBB", linewidth=0.8)

        label_rows = df_r[(df_r["rank"] <= 5) | df_r["player_name"].isin(spot_names)]
        for _, r in label_rows.iterrows():
            pname = str(r["player_name"]).strip()
            dx, dy = offsets_map.get(pname, (5, 4))
            ax.annotate(
                f"#{int(r['rank'])} {pname}",
                (float(r["shrunk_norm_impact"]), float(r["shrunk_wp_impact"])),
                textcoords="offset points",
                xytext=(dx, dy),
                fontsize=7.8,
                color=RR_NAVY,
                fontweight="bold" if r["rank"] <= 10 else "normal",
            )
        ax.set_xlabel("EB-Shrunk Normal-Pressure Baseline Impact")
        ax.set_ylabel("EB-Shrunk High-Pressure Impact")
        ax.set_title(subtitle)
        ax.legend(loc="lower right", fontsize=8.2)

    fig.suptitle("High-Pressure Performance vs Normal Baseline (Maintenance & Lift Without Elite Penalty)", fontsize=13, fontweight="bold")
    _save(fig, out_path)


def plot_04_pressure_performance_comparison(
    bat_all: pd.DataFrame,
    bowl_all: pd.DataFrame,
    out_path: Path,
) -> None:
    """04: Observed vs Shrunk Pressure Impact and Maintenance-Lift Comparison for Top 10 + Spotlight."""
    _setup_style()
    fig, axes = plt.subplots(1, 2, figsize=(15.5, 6.6))
    fig.subplots_adjust(wspace=0.38)

    for ax, df_r, obs_col, title, extras in [
        (axes[0], bat_all, "wp_impact_100", "Batters: Observed vs Shrunk vs Maint-Lift", ["Suryakumar Yadav", "Ashutosh Sharma"]),
        (axes[1], bowl_all, "wp_impact_24", "Bowlers: Observed vs Shrunk vs Maint-Lift", ["Varun Chakravarthy", "Kuldeep Yadav"]),
    ]:
        sel = df_r[(df_r["rank"] <= 10) | df_r["player_name"].isin(extras)].sort_values("rank").copy()
        y = np.arange(len(sel))
        h = 0.26
        ax.barh(y - h, sel[obs_col], height=h, color=RR_SLATE, alpha=0.55, label="Observed Pressure Impact")
        ax.barh(y, sel["shrunk_wp_impact"], height=h, color=RR_PINK, alpha=0.9, label="EB-Shrunk Pressure Impact")
        ax.barh(y + h, sel["maint_lift"], height=h, color=RR_TEAL, alpha=0.85, label="Attenuated Maint & Lift")
        ax.axvline(0.0, color=RR_NAVY, linewidth=0.8, linestyle="--")
        ax.set_yticks(y)
        ax.set_yticklabels([f"#{int(r['rank'])} {r['player_name']}" for _, r in sel.iterrows()], fontsize=8.8)
        ax.invert_yaxis()
        ax.set_xlabel("Impact Scale (per 100 Bat Balls / per 24 Bowl Balls)")
        ax.set_title(title)
        ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.12), ncol=2, fontsize=8.0)

    fig.suptitle("Observed vs Empirical-Bayes Shrunk Pressure Impact & Maintenance-Lift Decomposition", fontsize=13, fontweight="bold")
    _save(fig, out_path)


def plot_05_batter_role_analysis(
    bat_all: pd.DataFrame,
    bat_profiles: pd.DataFrame,
    out_path: Path,
) -> None:
    """05: Batter role analysis (Top 1-3, Middle 4-5, Finisher 6+) and Top-10 phase breakdown."""
    _setup_style()
    fig, axes = plt.subplots(1, 2, figsize=(14.0, 6.2))

    roles = ["Top 1-3", "Middle 4-5", "Finisher 6+"]
    ax1 = axes[0]

    role_offsets = {
        "Heinrich Klaasen": (8, 6),
        "Suryakumar Yadav": (8, -10),
        "Tim David": (8, 6),
        "Matthew Wade": (8, -10),
        "Reeza Hendricks": (8, 4),
        "Quinton de Kock": (8, -8),
    }

    for idx, rl in enumerate(roles):
        sub = bat_all[bat_all["primary_batting_role"] == rl]
        vals = sub["shrunk_wp_impact"].to_numpy()
        jitter = np.linspace(-0.18, 0.18, len(vals)) if len(vals) > 1 else np.array([0.0])
        ax1.scatter(np.full(len(vals), idx) + jitter, vals, alpha=0.55, color=RR_SLATE, s=34)
        if len(vals) > 0:
            med = float(np.median(vals))
            ax1.hlines(med, idx - 0.25, idx + 0.25, colors=RR_PINK, linewidths=2.5, label="Role Median" if idx == 0 else None)
        top_role = sub.sort_values("rank").head(2)
        for _, r in top_role.iterrows():
            pname = str(r["player_name"]).strip()
            dx, dy = role_offsets.get(pname, (8, 2))
            ax1.annotate(
                f"#{int(r['rank'])} {pname}",
                (idx, float(r["shrunk_wp_impact"])),
                textcoords="offset points",
                xytext=(dx, dy),
                fontsize=7.8,
                color=RR_NAVY,
            )
    ax1.axhline(0, color=RR_GRAY, linestyle="--", linewidth=0.9)
    ax1.set_xticks(range(len(roles)))
    ax1.set_xticklabels([f"{r}\n(n={int((bat_all['primary_batting_role']==r).sum())})" for r in roles])
    ax1.set_ylabel("EB-Shrunk Pressure Impact (per 100 Balls)")
    ax1.set_title("Eligible Pool Pressure Impact by Primary Batting Role")
    ax1.set_xlim(-0.55, 2.7)
    ax1.legend(loc="lower right")

    ax2 = axes[1]
    top10_p = bat_profiles[bat_profiles["rank"] <= 10].sort_values("rank")
    y = np.arange(len(top10_p))
    h = 0.26
    ax2.barh(y - h, top10_p["powerplay_shrunk_wp_impact"].fillna(0), height=h, color=RR_SLATE, label="Powerplay (1-6)")
    ax2.barh(y, top10_p["middle_shrunk_wp_impact"].fillna(0), height=h, color=RR_TEAL, label="Middle (7-15)")
    ax2.barh(y + h, top10_p["death_shrunk_wp_impact"].fillna(0), height=h, color=RR_PINK, label="Death (16-20)")
    ax2.axvline(0, color=RR_NAVY, linewidth=0.8, linestyle="--")
    ax2.set_yticks(y)
    ax2.set_yticklabels([f"#{int(r['rank'])} {r['player_name']} ({r['primary_batting_role']})" for _, r in top10_p.iterrows()], fontsize=8.2)
    ax2.invert_yaxis()
    ax2.set_xlabel("Phase-Specific Shrunk Pressure Impact (per 100 Balls)")
    ax2.set_title("Top 10 Batters: Phase-by-Phase Pressure Impact")
    ax2.legend(loc="lower right", fontsize=8.2)

    fig.suptitle("Dynamic Batting Role & Phase Analysis (Top 1-3 vs Middle 4-5 vs Finisher 6+)", fontsize=13, fontweight="bold")
    _save(fig, out_path)


def plot_06_bowling_phase_analysis(
    bowl_all: pd.DataFrame,
    bowl_profiles: pd.DataFrame,
    out_path: Path,
) -> None:
    """06: Bowling phase breakdown (Top 10) and Pace vs Spin pressure impact."""
    _setup_style()
    fig, axes = plt.subplots(1, 2, figsize=(14.0, 6.2))

    ax1 = axes[0]
    top10_p = bowl_profiles[bowl_profiles["rank"] <= 10].sort_values("rank")
    y = np.arange(len(top10_p))
    h = 0.26
    ax1.barh(y - h, top10_p["powerplay_shrunk_wp_impact"].fillna(0), height=h, color=RR_SLATE, label="Powerplay (1-6)")
    ax1.barh(y, top10_p["middle_shrunk_wp_impact"].fillna(0), height=h, color=RR_TEAL, label="Middle (7-15)")
    ax1.barh(y + h, top10_p["death_shrunk_wp_impact"].fillna(0), height=h, color=RR_PINK, label="Death (16-20)")
    ax1.axvline(0, color=RR_NAVY, linewidth=0.8, linestyle="--")
    ax1.set_yticks(y)
    ax1.set_yticklabels([f"#{int(r['rank'])} {r['player_name']} ({r['pace_or_spin']})" for _, r in top10_p.iterrows()], fontsize=8.2)
    ax1.invert_yaxis()
    ax1.set_xlabel("Phase-Specific Shrunk Pressure Impact (per 24 Legal Balls)")
    ax1.set_title("Top 10 Bowlers: Phase-by-Phase Pressure Impact")
    ax1.legend(loc="lower right", fontsize=8.2)

    ax2 = axes[1]
    styles = ["Pace", "Spin"]

    bowl_offsets = {
        "Jasprit Bumrah": (8, 4),
        "Jamie Overton": (-82, 4),
        "Mustafizur Rahman": (8, -8),
        "Sunil Narine": (8, 4),
        "Sufiyan Muqeem": (8, 7),
        "Sai Kishore": (-82, -4),
    }

    for idx, st in enumerate(styles):
        sub = bowl_all[bowl_all["pace_or_spin"] == st]
        vals = sub["shrunk_wp_impact"].to_numpy()
        jitter = np.linspace(-0.18, 0.18, len(vals)) if len(vals) > 1 else np.array([0.0])
        ax2.scatter(np.full(len(vals), idx) + jitter, vals, alpha=0.55, color=RR_SLATE, s=34)
        if len(vals) > 0:
            med = float(np.median(vals))
            ax2.hlines(med, idx - 0.25, idx + 0.25, colors=RR_PINK, linewidths=2.5, label="Median" if idx == 0 else None)
        for _, r in sub.sort_values("rank").head(3).iterrows():
            pname = str(r["player_name"]).strip()
            dx, dy = bowl_offsets.get(pname, (8, 2))
            ax2.annotate(
                f"#{int(r['rank'])} {pname}",
                (idx, float(r["shrunk_wp_impact"])),
                textcoords="offset points",
                xytext=(dx, dy),
                fontsize=7.8,
                color=RR_NAVY,
            )
    ax2.axhline(0, color=RR_GRAY, linestyle="--", linewidth=0.9)
    ax2.set_xticks(range(len(styles)))
    ax2.set_xticklabels([f"{s}\n(n={int((bowl_all['pace_or_spin']==s).sum())})" for s in styles])
    ax2.set_ylabel("EB-Shrunk Pressure Impact (per 24 Legal Balls)")
    ax2.set_title("Pace vs Spin Pressure Impact Across Eligible Pool")
    ax2.set_xlim(-0.6, 1.65)
    ax2.legend(loc="lower right")

    fig.suptitle("Bowling Phase & Pace/Spin Pressure Performance Analysis", fontsize=13, fontweight="bold")
    _save(fig, out_path)


def plot_07_pressure_consistency_analysis(
    bat_all: pd.DataFrame,
    bowl_all: pd.DataFrame,
    out_path: Path,
) -> None:
    """07: Unshrunk raw consistency vs Beta(5,5) vs empirically fitted Beta-binomial consistency."""
    _setup_style()
    fig, axes = plt.subplots(1, 2, figsize=(14.0, 6.0))

    cons_offsets = {
        # Batters
        "Matthew Wade": (-82, 8),
        "Reeza Hendricks": (-82, -10),
        "Naman Dhir": (6, 8),
        "Dinesh Karthik": (6, -10),
        "Heinrich Klaasen": (6, 6),
        "Tim David": (6, 6),
        # Bowlers
        "Sai Kishore": (-78, 8),
        "Sufiyan Muqeem": (-12, -16),
        "Jamie Overton": (6, 8),
        "Mohit Sharma": (6, -8),
        "Sunil Narine": (6, 4),
        "Mustafizur Rahman": (6, 6),
        "Jasprit Bumrah": (6, -8),
    }

    for ax, df_r, title in [
        (axes[0], bat_all, "Batters: Raw vs Empirical-Bayes Consistency"),
        (axes[1], bowl_all, "Bowlers: Raw vs Empirical-Bayes Consistency"),
    ]:
        ax.scatter(
            df_r["hp_qual_m"],
            df_r["raw_consistency"] * 100.0,
            alpha=0.35,
            color=RR_SLATE,
            s=32,
            label="Raw Unshrunk Match Rate (%)",
        )
        ax.scatter(
            df_r["hp_qual_m"],
            df_r["eb_consistency"] * 100.0,
            alpha=0.85,
            color=RR_PINK,
            s=40,
            label="EB Beta-Binomial Shrunk (%)",
        )
        # Draw shrinkage arrows for top 6 + smallest-sample extreme streaks
        highlights = pd.concat(
            [
                df_r[df_r["rank"] <= 5],
                df_r.sort_values("raw_consistency", ascending=False).head(3),
            ]
        ).drop_duplicates(subset=["player_name"])
        for _, r in highlights.iterrows():
            m = float(r["hp_qual_m"])
            y0 = float(r["raw_consistency"]) * 100.0
            y1 = float(r["eb_consistency"]) * 100.0
            pname = str(r["player_name"]).strip()
            dx, dy = cons_offsets.get(pname, (4, 3))
            ax.annotate(
                "",
                xy=(m, y1),
                xytext=(m, y0),
                arrowprops=dict(arrowstyle="->", color=RR_NAVY, alpha=0.55, lw=0.9),
            )
            ax.annotate(
                f"{pname} ({int(r['hp_pos_matches'])}/{int(m)})",
                (m, y1),
                textcoords="offset points",
                xytext=(dx, dy),
                fontsize=7.4,
                color=RR_NAVY,
            )
        ax.axhline(50.0, color=RR_GRAY, linestyle="--", linewidth=0.9, label="50% Par Benchmark")
        ax.set_xlabel("Qualifying High-Pressure Matches (m >= 6 HP Balls)")
        ax.set_ylabel("Positive-Impact Match Rate (%)")
        ax.set_title(title)
        ax.set_ylim(15, 105)
        ax.legend(loc="lower right", fontsize=8.2)

    fig.suptitle("Cross-Match Reliability: Empirical Bayes Shrinkage Eliminates Small-Match Streak Inflation", fontsize=13, fontweight="bold")
    _save(fig, out_path)


def plot_08_bootstrap_rank_uncertainty(
    bat_top10: pd.DataFrame,
    bowl_top10: pd.DataFrame,
    out_path: Path,
) -> None:
    """
    08: 1,000-resample stratified match-cluster bootstrap intervals.
    STRICT: Rank 1 on the LEFT (never inverted!) and Rank #1 at the top.
    """
    _setup_style()
    fig, axes = plt.subplots(1, 2, figsize=(16.5, 6.8))
    fig.subplots_adjust(wspace=0.45)

    for ax, df_t, title in [
        (axes[0], bat_top10, "Top 10 Batters: 1,000-Resample Rank Uncertainty"),
        (axes[1], bowl_top10, "Top 10 Bowlers: 1,000-Resample Rank Uncertainty"),
    ]:
        df_p = df_t.sort_values("rank", ascending=True).reset_index(drop=True)
        y = np.arange(len(df_p))
        med = df_p["boot_median_rank"].to_numpy(dtype=float)
        p05 = df_p["boot_p05_rank"].to_numpy(dtype=float)
        p95 = df_p["boot_p95_rank"].to_numpy(dtype=float)
        err_low = np.maximum(0.0, med - p05)
        err_high = np.maximum(0.0, p95 - med)

        ax.errorbar(
            med,
            y,
            xerr=[err_low, err_high],
            fmt="o",
            color=RR_PINK,
            ecolor=RR_NAVY,
            elinewidth=2.0,
            capsize=4,
            markersize=6.5,
            label="Median Rank & 5th-95th Percentile CI",
        )
        ax.axvline(10.5, color=RR_GRAY, linestyle="--", linewidth=1.1, label="Top-10 Cutoff (Rank 10.5)")
        ax.set_yticks(y)
        ax.set_yticklabels(
            [f"#{int(r['rank'])} {r['player_name']}" for _, r in df_p.iterrows()],
            fontsize=9.2,
            fontweight="bold",
        )
        ax.invert_yaxis()  # Rank #1 row at top

        max_x = float(max(np.nanmax(p95), 15.0))
        # Keep Rank 1 strictly on the LEFT!
        ax.set_xlim(0.5, max_x * 1.44)

        for idx, r in df_p.iterrows():
            inc_pct = float(r["top10_inclusion_frequency"]) * 100.0
            inel = int(r["ineligible_iters"]) if pd.notna(r["ineligible_iters"]) else 0
            note = f"Top-10 Freq: {inc_pct:.1f}%"
            if inel > 0:
                note += f" (inelig={inel})"
            ax.text(
                float(r["boot_p95_rank"]) + max_x * 0.02,
                idx,
                note,
                va="center",
                fontsize=7.8,
                color=RR_NAVY,
            )

        ax.set_xlabel("Bootstrap Rank (Rank 1 on Left; 5th-95th Percentile Interval)")
        ax.set_title(title)
        ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.12), ncol=2, fontsize=8.2)

    fig.suptitle(
        "Stratified Match-Cluster Bootstrap Rank Uncertainty (1,000 Resamples, Full LPO & Shrinkage Recomputed)",
        fontsize=12.5,
        fontweight="bold",
    )
    _save(fig, out_path)


def plot_09_ipl_vs_t20i_comparison(
    bat_all: pd.DataFrame,
    bowl_all: pd.DataFrame,
    out_path: Path,
) -> None:
    """09: IPL vs T20I pressure impact comparison highlighting format specialists vs dual-format stars."""
    _setup_style()
    fig, axes = plt.subplots(1, 2, figsize=(14.0, 6.0))

    fmt_offsets = {
        # Batters
        "Tim David": (6, 4),
        "Matthew Wade": (6, -8),
        "Naman Dhir": (6, 4),
        "Dinesh Karthik": (6, 4),
        "Reeza Hendricks": (6, 4),
        "Shashank Singh": (6, 4),
        "Heinrich Klaasen": (-68, 8),
        "Rinku Singh": (6, -8),
        "Andre Russell": (6, -6),
        "Ashutosh Sharma": (6, -8),
        # Bowlers
        "Sunil Narine": (6, 4),
        "Jasprit Bumrah": (6, 4),
        "Mustafizur Rahman": (6, -8),
        "Jamie Overton": (6, 6),
        "Mohit Sharma": (-75, 2),
        "Sai Kishore": (6, -10),
        "Sufiyan Muqeem": (-15, 8),
        "Mohsin Khan": (6, 8),
        "Mohammad Nawaz": (-15, -15),
        "Josh Hazlewood": (6, 4),
    }

    for ax, df_r, title in [
        (axes[0], bat_all, "Batters: IPL vs T20I Shrunk Pressure Impact"),
        (axes[1], bowl_all, "Bowlers: IPL vs T20I Shrunk Pressure Impact"),
    ]:
        zero_ipl = df_r["hp_balls_ipl"] == 0
        zero_t20i = df_r["hp_balls_t20i"] == 0
        dual = (~zero_ipl) & (~zero_t20i)

        ax.scatter(
            df_r.loc[dual, "shrunk_wp_impact_t20i"],
            df_r.loc[dual, "shrunk_wp_impact_ipl"],
            s=np.clip(df_r.loc[dual, "pressure_neff"] * 0.15, 25, 160),
            color=RR_TEAL,
            alpha=0.72,
            edgecolor=RR_NAVY,
            linewidth=0.5,
            label="Dual-Format (IPL + T20I)",
        )
        ax.scatter(
            df_r.loc[zero_ipl, "shrunk_wp_impact_t20i"],
            df_r.loc[zero_ipl, "shrunk_wp_impact_ipl"],
            s=65,
            color=RR_ORANGE,
            marker="^",
            edgecolor=RR_NAVY,
            label="T20I-Only HP Exposure (0 IPL HP Balls)",
        )
        ax.scatter(
            df_r.loc[zero_t20i, "shrunk_wp_impact_t20i"],
            df_r.loc[zero_t20i, "shrunk_wp_impact_ipl"],
            s=65,
            color=RR_PINK,
            marker="s",
            edgecolor=RR_NAVY,
            label="IPL-Only HP Exposure (0 T20I HP Balls)",
        )

        ax.axhline(0, color=RR_GRAY, linestyle="--", linewidth=0.8)
        ax.axvline(0, color=RR_GRAY, linestyle="--", linewidth=0.8)

        for _, r in df_r[df_r["rank"] <= 10].iterrows():
            pname = str(r["player_name"]).strip()
            dx, dy = fmt_offsets.get(pname, (4, 4))
            ax.annotate(
                f"#{int(r['rank'])} {pname}",
                (float(r["shrunk_wp_impact_t20i"]), float(r["shrunk_wp_impact_ipl"])),
                textcoords="offset points",
                xytext=(dx, dy),
                fontsize=7.6,
                color=RR_NAVY,
            )

        ax.set_xlabel("EB-Shrunk T20I Pressure Impact")
        ax.set_ylabel("EB-Shrunk IPL Pressure Impact")
        ax.set_title(title)
        ax.legend(loc="lower right", fontsize=8.0)

    fig.suptitle("Cross-Format Evidence: Dual-Format Performers vs Format Specialists (Sized by Kish N_eff)", fontsize=12.5, fontweight="bold")
    _save(fig, out_path)


def plot_10_player_sample_size_comparison(
    bat_all: pd.DataFrame,
    bowl_all: pd.DataFrame,
    near_miss_df: pd.DataFrame,
    out_path: Path,
) -> None:
    """10: Total balls N, discrete HP balls, and Kish N_eff across Top 10 + near-misses / V1 rescues."""
    _setup_style()
    fig, axes = plt.subplots(1, 2, figsize=(15.5, 6.6))
    fig.subplots_adjust(wspace=0.38)

    # Build combined spotlight tables
    for ax, df_r, role, id_col, title in [
        (axes[0], bat_all, "batter", "striker_id", "Batters: Raw N_hp vs Kish N_eff (Incl. Rescues & Near-Misses)"),
        (axes[1], bowl_all, "bowler", "bowler_id", "Bowlers: Raw N_hp vs Kish N_eff"),
    ]:
        top_sub = df_r[df_r["rank"] <= 10].copy()
        top_sub["disp_label"] = [f"#{int(r['rank'])} {r['player_name']}" for _, r in top_sub.iterrows()]

        if role == "batter" and near_miss_df is not None and len(near_miss_df) > 0:
            nm_pool = near_miss_df[
                (near_miss_df["role"] == "batter") & (near_miss_df["status"] == "near_miss")
            ].copy()
            # Ensure Phil Salt (5553) is showcased alongside top near-miss
            salt_row = nm_pool[nm_pool["striker_id"] == 5553]
            other_row = nm_pool[nm_pool["striker_id"] != 5553].head(1)
            nm_b = pd.concat([salt_row, other_row], ignore_index=True).head(2)
            nm_b["disp_label"] = [f"[NM] {r['player_name']}" for _, r in nm_b.iterrows()]
            sel = pd.concat(
                [
                    top_sub[["disp_label", "tot_balls", "hp_balls", "pressure_neff"]],
                    nm_b[["disp_label", "tot_balls", "hp_balls", "pressure_neff"]],
                ],
                ignore_index=True,
            )
        else:
            sel = top_sub[["disp_label", "tot_balls", "hp_balls", "pressure_neff"]].copy()

        y = np.arange(len(sel))
        h = 0.34
        ax.barh(y - h / 2, sel["hp_balls"], height=h, color=RR_SLATE, label="Discrete HP Balls (PI >= 0.50)")
        ax.barh(y + h / 2, sel["pressure_neff"], height=h, color=RR_PINK, label="Kish Effective Sample Size (N_eff)")
        ax.axvline(120, color=RR_NAVY, linestyle="--", linewidth=1.0, label="Benchmark HP Gate (120)")
        ax.set_yticks(y)
        ax.set_yticklabels(sel["disp_label"], fontsize=8.6)
        ax.invert_yaxis()
        for idx, r in sel.iterrows():
            x_pos = max(float(r["hp_balls"]), float(r["pressure_neff"])) + 12.0
            ax.text(x_pos, idx, f"N_tot={int(r['tot_balls'])}", va="center", fontsize=7.8, color=RR_NAVY)
        ax.set_xlim(0, float(max(sel["hp_balls"].max(), sel["pressure_neff"].max())) * 1.28)
        ax.set_xlabel("Balls / Effective Pressure Sample Size")
        ax.set_title(title)
        ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.12), ncol=2, fontsize=8.0)

    fig.suptitle("Sample Depth Comparison: Discrete HP Balls vs Continuous Kish N_eff & Total Exposure N", fontsize=12.5, fontweight="bold")
    _save(fig, out_path)


def plot_11_model_sensitivity_comparison(
    model_cmp_df: pd.DataFrame,
    loso_df: pd.DataFrame,
    wicket_df: pd.DataFrame,
    out_path: Path,
) -> None:
    """11: Model comparison (A/B/C), LOSO stability, and wicket-value sensitivity."""
    _setup_style()
    fig, axes = plt.subplots(1, 3, figsize=(16.5, 5.4))
    fig.subplots_adjust(wspace=0.32)

    # Panel A: Model A vs B vs C OOS Spearman & LOSO Spearman
    ax1 = axes[0]
    m_keys = ["model_a", "model_b", "model_c"]
    m_labels = ["Model A\n(Abs Press)", "Model B\n(Maint+Lift)", "Model C\n(Ridge/Logit)"]
    x = np.arange(len(m_keys))
    w = 0.34
    bat_cmp = model_cmp_df[model_cmp_df["role"] == "batter"].set_index("model_key").loc[m_keys]
    bowl_cmp = model_cmp_df[model_cmp_df["role"] == "bowler"].set_index("model_key").loc[m_keys]
    ax1.bar(x - w / 2, bat_cmp["oos_player_spearman"], width=w, color=RR_PINK, label="Bat OOS r_s")
    ax1.bar(x + w / 2, bowl_cmp["oos_player_spearman"], width=w, color=RR_NAVY, label="Bowl OOS r_s")
    ax1.set_xticks(x)
    ax1.set_xticklabels(m_labels)
    ax1.set_ylabel("2022-24 -> 2025-26 Player OOS Spearman")
    ax1.set_title("A. Walk-Forward OOS Validity")
    ax1.legend(loc="lower right", fontsize=8.0)

    # Panel B: LOSO Spearman across seasons 2022-2026
    ax2 = axes[1]
    for role, col, marker in [("batter", RR_PINK, "o"), ("bowler", RR_NAVY, "s")]:
        sub = loso_df[loso_df["role"] == role].sort_values("dropped_season")
        ax2.plot(sub["dropped_season"], sub["spearman_rho"], marker=marker, lw=2.0, color=col, label=f"{role.title()} LOSO rho")
    ax2.set_ylim(0.80, 1.01)
    ax2.set_xlabel("Dropped Season")
    ax2.set_ylabel("Spearman rho vs Full Sample")
    ax2.set_title("B. Leave-One-Season-Out (LOSO)")
    ax2.legend(loc="lower left", fontsize=8.2)

    # Panel C: Wicket-value sensitivity (4, 6, 8, Context)
    ax3 = axes[2]
    w_modes = ["fixed_4.0", "fixed_6.0", "fixed_8.0", "context_marginal"]
    w_lbls = ["w=4", "w=6", "w=8", "Context\nMarginal"]
    xw = np.arange(len(w_modes))
    wb = wicket_df[wicket_df["role"] == "batter"].set_index("wicket_mode").loc[w_modes]
    ww = wicket_df[wicket_df["role"] == "bowler"].set_index("wicket_mode").loc[w_modes]
    ax3.bar(xw - 0.17, wb["spearman_rho"], width=0.34, color=RR_PINK, label="Bat rho")
    ax3.bar(xw + 0.17, ww["spearman_rho"], width=0.34, color=RR_TEAL, label="Bowl rho")
    ax3.set_ylim(0.80, 1.02)
    ax3.set_xticks(xw)
    ax3.set_xticklabels(w_lbls)
    ax3.set_ylabel("Spearman rho vs Canonical")
    ax3.set_title("C. Wicket-Value Sensitivity")
    ax3.legend(loc="lower left", fontsize=8.2)

    fig.suptitle("Model Robustness, Walk-Forward Validity & Sensitivity Comparison", fontsize=13, fontweight="bold")
    _save(fig, out_path)


def plot_12_rr_recruitment_fit_matrix(
    bat_all: pd.DataFrame,
    bowl_all: pd.DataFrame,
    external_research_path: Path,
    out_path: Path,
) -> None:
    """
    12: Rajasthan Royals Recruitment Fit & Practical Feasibility Matrix.
    Statistical scores come strictly from data/raw/*.csv; external IPL 2027
    context is overlaid cleanly as separate practical flags (never altering ranks).
    """
    _setup_style()
    ext_map: Dict[str, Dict[str, str]] = {}
    if external_research_path.exists():
        ext_df = pd.read_csv(external_research_path)
        for _, r in ext_df.iterrows():
            ext_map[str(r["player_name"]).strip()] = {
                "franchise": str(r.get("latest_verified_franchise", "")),
                "active": str(r.get("active_status", "")),
                "avail": str(r.get("ipl_2027_availability_status", "")),
                "nat": str(r.get("nationality", "")),
            }

    def _classify_practical(row: pd.Series) -> str:
        name = str(row["player_name"]).strip()
        info = ext_map.get(name, {})
        active_l = info.get("active", "").lower()
        fran_l = info.get("franchise", "").lower()
        nat_l = info.get("nat", "").lower()
        if "retired" in active_l and "internationally retired" not in active_l:
            return "Retired / Coaching"
        if "pakistan" in nat_l or "ineligible" in active_l:
            return "No Demonstrated IPL Pathway"
        if "rajasthan royals" in fran_l:
            return "Current RR Core"
        if row["hp_balls_ipl"] == 0:
            return "Zero IPL Exposure"
        return "Active IPL Pool (2027 Unverified)"

    color_map = {
        "Current RR Core": RR_PINK,
        "Active IPL Pool (2027 Unverified)": RR_TEAL,
        "Zero IPL Exposure": RR_ORANGE,
        "Retired / Coaching": RR_GRAY,
        "No Demonstrated IPL Pathway": RR_NAVY,
    }

    fig, axes = plt.subplots(1, 2, figsize=(15.5, 6.8))
    fig.subplots_adjust(wspace=0.25)

    custom_matrix_offsets = {
        "Heinrich Klaasen": (6, 6),
        "Andre Russell": (-85, -4),
        "Rinku Singh": (6, 4),
        "Jamie Overton": (6, 6),
        "Mustafizur Rahman": (6, -10),
        "Rashid Khan": (-75, -2),
        "Tim David": (6, 4),
        "Jasprit Bumrah": (6, 4),
        "Sunil Narine": (-75, 4),
    }

    for ax, df_r, title in [
        (axes[0], bat_all.head(15).copy(), "Top 15 Batters: Statistical Score vs IPL Pressure Depth"),
        (axes[1], bowl_all.head(15).copy(), "Top 15 Bowlers: Statistical Score vs IPL Pressure Depth"),
    ]:
        df_r["practical_cat"] = df_r.apply(_classify_practical, axis=1)
        df_r["ipl_hp_share"] = 100.0 * df_r["hp_balls_ipl"] / np.maximum(1, df_r["hp_balls"])
        for cat, grp in df_r.groupby("practical_cat"):
            ax.scatter(
                grp["pressure_score"],
                grp["ipl_hp_share"],
                s=np.clip(grp["pressure_neff"] * 0.22, 55, 210),
                color=color_map.get(cat, RR_SLATE),
                edgecolor="black",
                linewidth=0.7,
                alpha=0.88,
                label=cat,
            )
        # Stagger offsets for clustered y=0% and y=100% points to avoid label overlap
        df_sorted = df_r.sort_values(["ipl_hp_share", "pressure_score"]).reset_index(drop=True)
        top_edge_idx = 0
        bot_edge_idx = 0
        for _, r in df_sorted.iterrows():
            pname = str(r["player_name"]).strip()
            y_v = float(r["ipl_hp_share"])
            if pname in custom_matrix_offsets:
                dx, dy = custom_matrix_offsets[pname]
            elif y_v >= 99.0:
                dy = 8 if top_edge_idx % 2 == 0 else -12
                dx = -42 if top_edge_idx == 0 else (6 if top_edge_idx == 2 else -10)
                top_edge_idx += 1
            elif y_v <= 2.0:
                dy = 8 if bot_edge_idx % 2 == 0 else -12
                dx = -30 if bot_edge_idx == 0 else (6 if bot_edge_idx == 2 else -10)
                bot_edge_idx += 1
            else:
                dx, dy = 5, 3
            ax.annotate(
                f"#{int(r['rank'])} {pname}",
                (float(r["pressure_score"]), y_v),
                textcoords="offset points",
                xytext=(dx, dy),
                fontsize=7.6,
                color=RR_NAVY,
            )
        min_x = float(df_r["pressure_score"].min())
        max_x = float(df_r["pressure_score"].max())
        ax.set_xlim(min_x - 0.12, max_x + 0.32)
        ax.set_xlabel("Model V3 Composite Pressure Score (Strict Data Merit)")
        ax.set_ylabel("IPL Share of High-Pressure Balls (%)")
        ax.set_ylim(-14, 115)
        ax.set_title(title)
        ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.12), ncol=2, fontsize=7.8)

    fig.suptitle(
        "Rajasthan Royals Recruitment Fit Matrix (Statistical Merit Strictly Separated from Practical Context; IPL 2027 Status Unverified)",
        fontsize=12.0,
        fontweight="bold",
    )
    _save(fig, out_path)


def generate_all_charts(
    bat_all: pd.DataFrame,
    bowl_all: pd.DataFrame,
    bat_profiles: pd.DataFrame,
    bowl_profiles: pd.DataFrame,
    model_cmp_df: pd.DataFrame,
    loso_df: pd.DataFrame,
    wicket_df: pd.DataFrame,
    near_miss_df: pd.DataFrame,
    chart_dir: Path,
    external_research_path: Path,
) -> Dict[str, Path]:
    """Generate all 12 required Model V3 publication charts."""
    chart_dir.mkdir(parents=True, exist_ok=True)
    paths = {
        "01": chart_dir / "01_top10_batters_ranking.png",
        "02": chart_dir / "02_top10_bowlers_ranking.png",
        "03": chart_dir / "03_pressure_vs_normal_impact.png",
        "04": chart_dir / "04_pressure_performance_comparison.png",
        "05": chart_dir / "05_batter_role_analysis.png",
        "06": chart_dir / "06_bowling_phase_analysis.png",
        "07": chart_dir / "07_pressure_consistency_analysis.png",
        "08": chart_dir / "08_bootstrap_rank_uncertainty.png",
        "09": chart_dir / "09_ipl_vs_t20i_comparison.png",
        "10": chart_dir / "10_player_sample_size_comparison.png",
        "11": chart_dir / "11_model_sensitivity_comparison.png",
        "12": chart_dir / "12_rr_recruitment_fit_matrix.png",
    }
    plot_01_02_top10_ranking(bat_all.head(10), role="batter", out_path=paths["01"])
    plot_01_02_top10_ranking(bowl_all.head(10), role="bowler", out_path=paths["02"])
    plot_03_pressure_vs_normal_impact(bat_all, bowl_all, out_path=paths["03"])
    plot_04_pressure_performance_comparison(bat_all, bowl_all, out_path=paths["04"])
    plot_05_batter_role_analysis(bat_all, bat_profiles, out_path=paths["05"])
    plot_06_bowling_phase_analysis(bowl_all, bowl_profiles, out_path=paths["06"])
    plot_07_pressure_consistency_analysis(bat_all, bowl_all, out_path=paths["07"])
    plot_08_bootstrap_rank_uncertainty(bat_all.head(10), bowl_all.head(10), out_path=paths["08"])
    plot_09_ipl_vs_t20i_comparison(bat_all, bowl_all, out_path=paths["09"])
    plot_10_player_sample_size_comparison(bat_all, bowl_all, near_miss_df, out_path=paths["10"])
    plot_11_model_sensitivity_comparison(model_cmp_df, loso_df, wicket_df, out_path=paths["11"])
    plot_12_rr_recruitment_fit_matrix(bat_all, bowl_all, external_research_path, out_path=paths["12"])
    return paths
