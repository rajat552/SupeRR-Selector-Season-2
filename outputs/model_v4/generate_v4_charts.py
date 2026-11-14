"""Generate high-resolution figures for Model V4 Multiverse Analysis & Submission Report."""

from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
OUT_DIR = ROOT / "outputs" / "model_v4"
CHART_DIR = OUT_DIR / "charts"
CHART_DIR.mkdir(parents=True, exist_ok=True)

# Set consistent plotting style
plt.rcParams["font.sans-serif"] = "DejaVu Sans"
plt.rcParams["axes.edgecolor"] = "#CCCCCC"
plt.rcParams["axes.linewidth"] = 0.8


def plot_variance_decomposition():
    df = pd.read_csv(OUT_DIR / "variance_decomposition.csv")

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5), sharey=True)

    bat = df[df["role"] == "batter"].sort_values("pct_variance_explained", ascending=True)
    bowl = df[df["role"] == "bowler"].sort_values("pct_variance_explained", ascending=True)

    # Rename dimension labels for clarity
    label_map = {
        "player_id": "Individual Player Ability",
        "f_scope": "Format Scope (IPL vs T20I)",
        "g_gate": "Eligibility Gate (Volume Cutoff)",
        "p_def": "Pressure Definition (P1-P5)",
        "w_def": "Wicket State in Baseline (W0/W1)",
        "v_val": "Wicket Run Valuation (V=4,6,8,ctx)",
        "m_model": "Scoring Model (A vs B vs C)",
        "k_shrink": "Empirical Bayes Shrinkage (K)",
        "s_weights": "Component Weights (S0-S6)",
    }

    y_pos = np.arange(len(bat))

    ax1.barh(y_pos, bat["pct_variance_explained"], color="#1f77b4", alpha=0.85)
    ax1.set_yticks(y_pos)
    ax1.set_yticklabels([label_map.get(d, d) for d in bat["dimension"]], fontsize=10)
    ax1.set_xlabel("% Variance Explained", fontsize=11)
    ax1.set_title("Batters: Variance Decomposition", fontsize=12, fontweight="bold")
    ax1.grid(axis="x", linestyle="--", alpha=0.5)

    for i, v in enumerate(bat["pct_variance_explained"]):
        ax1.text(v + 0.5, i, f"{v:.1f}%", va="center", fontsize=9, fontweight="bold")

    ax2.barh(y_pos, bowl["pct_variance_explained"], color="#E61E64", alpha=0.85)
    ax2.set_xlabel("% Variance Explained", fontsize=11)
    ax2.set_title("Bowlers: Variance Decomposition", fontsize=12, fontweight="bold")
    ax2.grid(axis="x", linestyle="--", alpha=0.5)

    for i, v in enumerate(bowl["pct_variance_explained"]):
        ax2.text(v + 0.5, i, f"{v:.1f}%", va="center", fontsize=9, fontweight="bold")

    plt.suptitle("ANOVA Variance Decomposition Across 3.19M Multiverse Specifications", fontsize=14, y=1.02)
    plt.tight_layout()
    plt.savefig(CHART_DIR / "fig1_variance_decomposition.png", dpi=300, bbox_inches="tight")
    plt.close()


def plot_maintenance_vs_lift():
    all_bat = pd.read_csv(OUT_DIR / "unfiltered_all_batters.csv")
    top10_bat = pd.read_csv(OUT_DIR / "final_top10_batters.csv")

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.scatter(all_bat["shrunk_norm_impact"], all_bat["raw_pressure_lift"], color="#CCCCCC", alpha=0.6, s=30, label="Other Eligible Batters")
    ax.scatter(top10_bat["shrunk_norm_impact"], top10_bat["raw_lift"], color="#1f77b4", s=90, edgecolors="black", label="Consensus Top 10 Batters")

    for _, row in top10_bat.iterrows():
        ax.annotate(
            row["player_name"],
            (row["shrunk_norm_impact"], row["raw_lift"]),
            xytext=(5, 4),
            textcoords="offset points",
            fontsize=9,
            fontweight="bold"
        )

    ax.axhline(0, color="gray", linestyle="--", alpha=0.7)
    ax.axvline(0, color="gray", linestyle="--", alpha=0.7)
    ax.set_xlabel("Normal-Pressure Impact (Runs/100b above exp)", fontsize=11)
    ax.set_ylabel("Raw Pressure Lift (HP Impact minus Normal Impact)", fontsize=11)
    ax.set_title("Batting Resilience Landscape: Maintenance vs. Pressure Lift", fontsize=13, fontweight="bold")
    ax.legend(frameon=True)
    ax.grid(True, linestyle="--", alpha=0.4)
    plt.tight_layout()
    plt.savefig(CHART_DIR / "fig2_maintenance_vs_lift_batters.png", dpi=300)
    plt.close()

    # Bowlers
    all_bowl = pd.read_csv(OUT_DIR / "unfiltered_all_bowlers.csv")
    top10_bowl = pd.read_csv(OUT_DIR / "final_top10_bowlers.csv")

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.scatter(all_bowl["shrunk_norm_impact"], all_bowl["raw_pressure_lift"], color="#CCCCCC", alpha=0.6, s=30, label="Other Eligible Bowlers")
    ax.scatter(top10_bowl["shrunk_norm_impact"], top10_bowl["raw_lift"], color="#E61E64", s=90, edgecolors="black", label="Consensus Top 10 Bowlers")

    for _, row in top10_bowl.iterrows():
        ax.annotate(
            row["player_name"],
            (row["shrunk_norm_impact"], row["raw_lift"]),
            xytext=(5, 4),
            textcoords="offset points",
            fontsize=9,
            fontweight="bold"
        )

    ax.axhline(0, color="gray", linestyle="--", alpha=0.7)
    ax.axvline(0, color="gray", linestyle="--", alpha=0.7)
    ax.set_xlabel("Normal-Pressure Impact (Runs saved/24b above exp)", fontsize=11)
    ax.set_ylabel("Raw Pressure Lift (HP Impact minus Normal Impact)", fontsize=11)
    ax.set_title("Bowling Resilience Landscape: Maintenance vs. Pressure Lift", fontsize=13, fontweight="bold")
    ax.legend(frameon=True)
    ax.grid(True, linestyle="--", alpha=0.4)
    plt.tight_layout()
    plt.savefig(CHART_DIR / "fig3_maintenance_vs_lift_bowlers.png", dpi=300)
    plt.close()


def plot_bootstrap_stability():
    top10_bat = pd.read_csv(OUT_DIR / "final_top10_batters.csv")
    boot_bat = pd.read_csv(OUT_DIR / "bootstrap_canonical_batters.csv")
    top_boot_bat = top10_bat.merge(boot_bat.rename(columns={"striker_id": "player_id"}), on="player_id")

    fig, ax = plt.subplots(figsize=(10, 5))
    y_pos = np.arange(len(top_boot_bat))

    # Error bar from p05 to p95
    x_err = [
        top_boot_bat["boot_median_rank"] - top_boot_bat["boot_p05_rank"],
        top_boot_bat["boot_p95_rank"] - top_boot_bat["boot_median_rank"]
    ]
    ax.errorbar(
        top_boot_bat["boot_median_rank"],
        y_pos,
        xerr=x_err,
        fmt="o",
        color="#1f77b4",
        ecolor="#1f77b4",
        elinewidth=2,
        capsize=4,
        markersize=7
    )
    ax.set_yticks(y_pos)
    ax.set_yticklabels(top_boot_bat["player_name_x"], fontsize=10, fontweight="bold")
    ax.invert_yaxis()
    ax.set_xlabel("Bootstrap Rank Distribution (Median & 90% Empirical CI)", fontsize=11)
    ax.set_title("Batting Top 10 Bootstrap Stability (1,000 Stratified Draws)", fontsize=13, fontweight="bold")
    ax.axvline(10.5, color="red", linestyle="--", alpha=0.7, label="Top 10 boundary")
    ax.grid(axis="x", linestyle="--", alpha=0.4)
    ax.legend()
    plt.tight_layout()
    plt.savefig(CHART_DIR / "fig4_bootstrap_stability_batters.png", dpi=300)
    plt.close()

    # Bowler bootstrap stability
    top10_bowl = pd.read_csv(OUT_DIR / "final_top10_bowlers.csv")
    boot_bowl = pd.read_csv(OUT_DIR / "bootstrap_canonical_bowlers.csv")
    top_boot_bowl = top10_bowl.merge(boot_bowl.rename(columns={"bowler_id": "player_id"}), on="player_id")

    fig, ax = plt.subplots(figsize=(10, 5))
    y_pos = np.arange(len(top_boot_bowl))

    x_err = [
        top_boot_bowl["boot_median_rank"] - top_boot_bowl["boot_p05_rank"],
        top_boot_bowl["boot_p95_rank"] - top_boot_bowl["boot_median_rank"]
    ]
    ax.errorbar(
        top_boot_bowl["boot_median_rank"],
        y_pos,
        xerr=x_err,
        fmt="o",
        color="#E61E64",
        ecolor="#E61E64",
        elinewidth=2,
        capsize=4,
        markersize=7
    )
    ax.set_yticks(y_pos)
    ax.set_yticklabels(top_boot_bowl["player_name_x"], fontsize=10, fontweight="bold")
    ax.invert_yaxis()
    ax.set_xlabel("Bootstrap Rank Distribution (Median & 90% Empirical CI)", fontsize=11)
    ax.set_title("Bowling Top 10 Bootstrap Stability (1,000 Stratified Draws)", fontsize=13, fontweight="bold")
    ax.axvline(10.5, color="red", linestyle="--", alpha=0.7, label="Top 10 boundary")
    ax.grid(axis="x", linestyle="--", alpha=0.4)
    ax.legend()
    plt.tight_layout()
    plt.savefig(CHART_DIR / "fig5_bootstrap_stability_bowlers.png", dpi=300)
    plt.close()


def main():
    plot_variance_decomposition()
    plot_maintenance_vs_lift()
    plot_bootstrap_stability()
    print("All additional figures successfully created in outputs/model_v4/charts/")


if __name__ == "__main__":
    main()
