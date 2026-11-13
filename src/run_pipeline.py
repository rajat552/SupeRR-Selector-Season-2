"""End-to-end reproducible pipeline for SupeRR Selector Season 2 Round 1."""

import json
from pathlib import Path
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from data_loader import load_clean_dataset
from state_builder import build_match_state
from pressure import compute_pressure_index
from baselines import add_context_baselines
from batting_model import evaluate_batters
from bowling_model import evaluate_bowlers
from validation_tests import run_sensitivity_checks, run_match_bootstrap


OUT_DIR = Path(__file__).resolve().parents[1] / "outputs"
CHART_DIR = OUT_DIR / "charts"


def plot_top10_bar(df_top: pd.DataFrame, title: str, out_path: Path) -> None:
    """Create a horizontal bar chart comparing Normal vs High-Pressure impact for Top 10."""
    fig, ax = plt.subplots(figsize=(10, 6))
    y = range(len(df_top) - 1, -1, -1)
    names = [f"#{r['rank']} {r['player_name']}" for _, r in df_top.iterrows()]

    if "hp_impact_100" in df_top.columns:
        hp_col, lp_col = "hp_impact_100", "lp_impact_100"
        xlabel = "Context-Adjusted Impact per 100 Balls (Runs + Wicket Value)"
    else:
        hp_col, lp_col = "hp_impact_24", "lp_impact_24"
        xlabel = "Context-Adjusted Impact per 24 Balls (Runs Saved + Wicket Value)"

    ax.barh([i + 0.18 for i in y], df_top[hp_col], height=0.35, color="#E61E64", label="High Pressure (PI >= 0.50)")
    ax.barh([i - 0.18 for i in y], df_top[lp_col], height=0.35, color="#1D3557", alpha=0.75, label="Normal / Low Pressure (PI < 0.35)")
    ax.axvline(0, color="black", linewidth=0.8, linestyle="--")
    ax.set_yticks(list(y))
    ax.set_yticklabels(names, fontsize=10)
    ax.set_xlabel(xlabel, fontsize=10)
    ax.set_title(title, fontsize=12, fontweight="bold")
    ax.legend(loc="lower right")
    plt.tight_layout()
    plt.savefig(out_path, dpi=200)
    plt.close(fig)


def plot_bootstrap_ci(df_top: pd.DataFrame, title: str, out_path: Path) -> None:
    """Plot bootstrap median rank and 5th-95th percentile confidence intervals."""
    fig, ax = plt.subplots(figsize=(9, 5.5))
    y = range(len(df_top) - 1, -1, -1)
    names = [f"#{r['rank']} {r['player_name']} ({r['prob_top10']*100:.0f}%)" for _, r in df_top.iterrows()]

    med = df_top["boot_median_rank"]
    err_low = med - df_top["boot_p05_rank"]
    err_high = df_top["boot_p95_rank"] - med

    ax.errorbar(
        med,
        list(y),
        xerr=[err_low, err_high],
        fmt="o",
        color="#E61E64",
        ecolor="#1D3557",
        elinewidth=2,
        capsize=4,
    )
    ax.axvline(10.5, color="gray", linestyle="--", linewidth=1, label="Top-10 Cutoff")
    ax.set_yticks(list(y))
    ax.set_yticklabels(names, fontsize=9.5)
    ax.set_xlabel("Bootstrap Rank (Median & 5th-95th Percentile CI)", fontsize=10)
    ax.set_title(title, fontsize=11.5, fontweight="bold")
    ax.invert_xaxis()
    ax.legend(loc="lower left")
    plt.tight_layout()
    plt.savefig(out_path, dpi=200)
    plt.close(fig)


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    CHART_DIR.mkdir(parents=True, exist_ok=True)

    bbb, matches, pe, pl = load_clean_dataset()
    df = add_context_baselines(compute_pressure_index(build_match_state(bbb)))

    bat = evaluate_batters(df, pl)
    bowl = evaluate_bowlers(df, pl)

    sens = run_sensitivity_checks(df, pl)
    bat_boot, bowl_boot = run_match_bootstrap(df, bat, bowl, n_boot=300)

    bat_full = bat.merge(bat_boot, on="striker_id", how="left")
    bowl_full = bowl.merge(bowl_boot, on="bowler_id", how="left")

    bat_full.to_csv(OUT_DIR / "batter_rankings_all.csv", index=False)
    bowl_full.to_csv(OUT_DIR / "bowler_rankings_all.csv", index=False)
    bat_full.head(10).to_csv(OUT_DIR / "top10_batters.csv", index=False)
    bowl_full.head(10).to_csv(OUT_DIR / "top10_bowlers.csv", index=False)

    with open(OUT_DIR / "sensitivity_summary.json", "w", encoding="utf-8") as f:
        json.dump(sens, f, indent=2)

    plot_top10_bar(
        bat_full.head(10),
        "Top 10 Batters Under Pressure: High-Pressure vs Normal Impact",
        CHART_DIR / "top10_batters_impact.png",
    )
    plot_top10_bar(
        bowl_full.head(10),
        "Top 10 Bowlers Under Pressure: High-Pressure vs Normal Impact",
        CHART_DIR / "top10_bowlers_impact.png",
    )
    plot_bootstrap_ci(
        bat_full.head(10),
        "Top 10 Batters: Match-Level Bootstrap Rank Stability (300 Resamples)",
        CHART_DIR / "top10_batters_bootstrap.png",
    )
    plot_bootstrap_ci(
        bowl_full.head(10),
        "Top 10 Bowlers: Match-Level Bootstrap Rank Stability (300 Resamples)",
        CHART_DIR / "top10_bowlers_bootstrap.png",
    )
    print("Pipeline complete. Outputs written to:", OUT_DIR)


if __name__ == "__main__":
    main()

