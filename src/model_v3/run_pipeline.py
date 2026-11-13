"""End-to-end Model V2 reproducible pipeline entry point."""

from __future__ import annotations

import json
import hashlib
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict
import pandas as pd

from . import build_foundation_dataset
from .bootstrap import run_stratified_bootstrap
from .eligibility import BENCHMARK_GATE
from .impact_models import run_model_c_oos_validation
from .model_comparison import evaluate_models_abc
from .ranking import assemble_canonical_rankings, build_player_profiles
from .validation import (
    run_eligibility_and_shrinkage_sensitivity,
    run_format_sensitivity,
    run_loso_sensitivity,
    run_pressure_sensitivity,
    run_wicket_sensitivity,
)
from .visualization import generate_all_charts


ROOT_DIR = Path(__file__).resolve().parents[2]
OUT_DIR = ROOT_DIR / "outputs" / "model_v3"
CHART_DIR = OUT_DIR / "charts"
MANIFEST_PATH = ROOT_DIR / "outputs" / "model_v2" / "integrity_manifest_pre.json"
EXT_RESEARCH_PATH = ROOT_DIR / "outputs" / "model_v2" / "external_player_research.csv"


def verify_v1_immutability(manifest_path: Path = MANIFEST_PATH) -> Dict[str, int]:
    """Read-only verification of V1/raw/audit SHA-256 checksums."""
    if not manifest_path.exists():
        return {"checked": 0, "mismatches": 0}
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    files_map = manifest.get("files", manifest)
    checked = 0
    mismatches = 0
    for rel_path, expected_info in files_map.items():
        if isinstance(expected_info, dict) and "sha256" in expected_info:
            expected_hash = expected_info["sha256"]
        elif isinstance(expected_info, str):
            expected_hash = expected_info
        else:
            continue
        fp = ROOT_DIR / rel_path
        checked += 1
        if not fp.exists():
            mismatches += 1
            continue
        actual_hash = hashlib.sha256(fp.read_bytes()).hexdigest()
        if actual_hash != expected_hash:
            mismatches += 1
    return {"checked": checked, "mismatches": mismatches}


def main(n_boot: int = 1000, seed: int = 42) -> None:
    """Run complete Model V2 pipeline and write all CSV, Markdown, and PNG deliverables."""
    t_start = time.perf_counter()
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    CHART_DIR.mkdir(parents=True, exist_ok=True)
    timings: Dict[str, float] = {}

    # 1. Foundation dataset (Phase 1)
    t0 = time.perf_counter()
    df, matches, pe, player_lookup, match_elo = build_foundation_dataset()
    timings["phase1_foundation_sec"] = time.perf_counter() - t0

    # 2. Model C walk-forward chronological OOS validation
    t0 = time.perf_counter()
    oos_val_df = run_model_c_oos_validation(df)
    oos_val_df.to_csv(OUT_DIR / "model_c_oos_validation.csv", index=False)
    timings["model_c_oos_sec"] = time.perf_counter() - t0

    # 3. Objective comparison across Models A, B, and C
    t0 = time.perf_counter()
    model_cmp_df, scored_by_role, selected_model = evaluate_models_abc(
        df,
        player_lookup,
        oos_validation_df=oos_val_df,
        gate=BENCHMARK_GATE,
        n_boot_cmp=200,
    )
    model_cmp_df.to_csv(OUT_DIR / "model_comparison.csv", index=False)
    timings["model_comparison_sec"] = time.perf_counter() - t0

    # 4. Full 1,000-resample stratified match-cluster bootstrap on canonical model
    t0 = time.perf_counter()
    boot_bat_df, boot_bat_meta = run_stratified_bootstrap(
        df,
        player_lookup,
        role="batter",
        model_name=selected_model,
        n_boot=n_boot,
        seed=seed,
        gate=BENCHMARK_GATE,
    )
    timings["bootstrap_batters_1000_sec"] = boot_bat_meta["runtime_seconds"]

    boot_bowl_df, boot_bowl_meta = run_stratified_bootstrap(
        df,
        player_lookup,
        role="bowler",
        model_name=selected_model,
        n_boot=n_boot,
        seed=seed,
        gate=BENCHMARK_GATE,
    )
    timings["bootstrap_bowlers_1000_sec"] = boot_bowl_meta["runtime_seconds"]
    timings["bootstrap_total_sec"] = time.perf_counter() - t0

    # 5. Assemble final rankings & detailed player profiles
    t0 = time.perf_counter()
    all_bat, top10_bat = assemble_canonical_rankings(
        scored_by_role["batter"], boot_bat_df, role="batter", selected_model=selected_model
    )
    all_bowl, top10_bowl = assemble_canonical_rankings(
        scored_by_role["bowler"], boot_bowl_df, role="bowler", selected_model=selected_model
    )

    all_bat.to_csv(OUT_DIR / "all_batter_rankings.csv", index=False)
    all_bowl.to_csv(OUT_DIR / "all_bowler_rankings.csv", index=False)
    top10_bat.to_csv(OUT_DIR / "final_top10_batters.csv", index=False)
    top10_bowl.to_csv(OUT_DIR / "final_top10_bowlers.csv", index=False)

    # Sort bootstrap outputs meaningfully (eligible canonical rank first, then inclusion freq)
    boot_bat_out = boot_bat_df.merge(
        all_bat[["striker_id", "rank", "pressure_score"]], on="striker_id", how="left"
    ).sort_values(["rank", "top10_inclusion_frequency"], ascending=[True, False], na_position="last")
    boot_bowl_out = boot_bowl_df.merge(
        all_bowl[["bowler_id", "rank", "pressure_score"]], on="bowler_id", how="left"
    ).sort_values(["rank", "top10_inclusion_frequency"], ascending=[True, False], na_position="last")
    boot_bat_out.to_csv(OUT_DIR / "bootstrap_results_batters.csv", index=False)
    boot_bowl_out.to_csv(OUT_DIR / "bootstrap_results_bowlers.csv", index=False)

    bat_profiles = build_player_profiles(df, all_bat, role="batter")
    bowl_profiles = build_player_profiles(df, all_bowl, role="bowler")
    bat_profiles.to_csv(OUT_DIR / "batter_player_profiles.csv", index=False)
    bowl_profiles.to_csv(OUT_DIR / "bowler_player_profiles.csv", index=False)
    timings["ranking_and_profiles_sec"] = time.perf_counter() - t0

    # 6. Sensitivity & robustness checks (LOSO, Format, Pressure, Wicket, Eligibility & Shrinkage k)
    t0 = time.perf_counter()
    loso_df = run_loso_sensitivity(
        df, player_lookup, all_bat, all_bowl, model_name=selected_model
    )
    format_df = run_format_sensitivity(
        df, player_lookup, all_bat, all_bowl, model_name=selected_model
    )
    pressure_df = run_pressure_sensitivity(
        df, player_lookup, all_bat, all_bowl, model_name=selected_model
    )
    wicket_df, wkt_table_df = run_wicket_sensitivity(
        df, player_lookup, all_bat, all_bowl, model_name=selected_model
    )
    elig_df, near_miss_df, k_df = run_eligibility_and_shrinkage_sensitivity(
        df, player_lookup, all_bat, all_bowl, model_name=selected_model
    )

    format_df.to_csv(OUT_DIR / "format_sensitivity.csv", index=False)
    pressure_df.to_csv(OUT_DIR / "pressure_sensitivity.csv", index=False)
    elig_df.to_csv(OUT_DIR / "eligibility_sensitivity.csv", index=False)
    wicket_df.to_csv(OUT_DIR / "wicket_sensitivity.csv", index=False)
    # Supplemental diagnostic tables
    loso_df.to_csv(OUT_DIR / "loso_sensitivity.csv", index=False)
    near_miss_df.to_csv(OUT_DIR / "near_miss_candidates.csv", index=False)
    k_df.to_csv(OUT_DIR / "shrinkage_k_sensitivity.csv", index=False)
    wkt_table_df.to_csv(OUT_DIR / "context_wicket_values.csv", index=False)
    timings["sensitivity_suite_sec"] = time.perf_counter() - t0

    # 7. Generate all 12 publication-ready charts
    t0 = time.perf_counter()
    chart_paths = generate_all_charts(
        bat_all=all_bat,
        bowl_all=all_bowl,
        bat_profiles=bat_profiles,
        bowl_profiles=bowl_profiles,
        model_cmp_df=model_cmp_df,
        loso_df=loso_df,
        wicket_df=wicket_df,
        near_miss_df=near_miss_df,
        chart_dir=CHART_DIR,
        external_research_path=EXT_RESEARCH_PATH,
    )
    timings["charts_sec"] = time.perf_counter() - t0
    timings["total_pipeline_sec"] = time.perf_counter() - t_start

    # 8. Integrity verification and execution log
    imm = verify_v1_immutability()
    now_iso = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")

    log_lines = [
        "# Model V3 Execution Log",
        "",
        f"- **Run Timestamp:** {now_iso}",
        f"- **Primary Dataset Scope:** `{df['match_id'].nunique()}` matches (`{int((matches['comp_category']=='IPL').sum())}` IPL, `{int((matches['comp_category']=='T20I').sum())}` T20I), `{len(df):,}` deliveries (`{int(df['is_legal_ball'].sum()):,}` legal balls)",
        f"- **Selected Canonical Model:** `{selected_model}` (selected objectively via `model_comparison.csv`)",
        f"- **Bootstrap Resamples:** `{n_boot}` stratified by `(comp_category, season_year)` (`seed={seed}`), full LPO/shrinkage/consistency/eligibility recomputed inside every iteration",
        f"- **V1 Immutability Check:** `checked={imm['checked']}, mismatches={imm['mismatches']}`",
        "",
        "## Wall-Clock Timings",
        "",
        "| Stage | Runtime (s) |",
        "|---|---:|",
    ]
    for k, v in timings.items():
        log_lines.append(f"| `{k}` | {v:.3f} |")

    log_lines.extend(
        [
            "",
            "## Canonical Top 10 Batters",
            "",
            "| Rank | Player ID | Player Name | Score | Shrunk PWI | EB Cons | Boot Median (p05-p95) | Top-10 Freq | N_hp | Kish N_eff |",
            "|---:|---:|---|---:|---:|---:|---:|---:|---:|---:|",
        ]
    )
    for _, r in top10_bat.iterrows():
        log_lines.append(
            f"| {int(r['rank'])} | {int(r['striker_id'])} | {r['player_name']} | {r['pressure_score']:+.3f} | "
            f"{r['shrunk_wp_impact']:+.2f} | {r['eb_consistency']*100:.1f}% | "
            f"{r['boot_median_rank']:.1f} ({r['boot_p05_rank']:.1f}-{r['boot_p95_rank']:.1f}) | "
            f"{r['top10_inclusion_frequency']*100:.1f}% | {int(r['hp_balls'])} | {r['pressure_neff']:.1f} |"
        )

    log_lines.extend(
        [
            "",
            "## Canonical Top 10 Bowlers",
            "",
            "| Rank | Player ID | Player Name | Score | Shrunk PWI | EB Cons | Boot Median (p05-p95) | Top-10 Freq | N_hp | Kish N_eff |",
            "|---:|---:|---|---:|---:|---:|---:|---:|---:|---:|",
        ]
    )
    for _, r in top10_bowl.iterrows():
        log_lines.append(
            f"| {int(r['rank'])} | {int(r['bowler_id'])} | {r['player_name']} | {r['pressure_score']:+.3f} | "
            f"{r['shrunk_wp_impact']:+.2f} | {r['eb_consistency']*100:.1f}% | "
            f"{r['boot_median_rank']:.1f} ({r['boot_p05_rank']:.1f}-{r['boot_p95_rank']:.1f}) | "
            f"{r['top10_inclusion_frequency']*100:.1f}% | {int(r['hp_balls'])} | {r['pressure_neff']:.1f} |"
        )

    log_lines.extend(
        [
            "",
            f"## Generated Charts ({len(chart_paths)} PNGs)",
            "",
        ]
    )
    for k, p in sorted(chart_paths.items()):
        log_lines.append(f"- `{p.name}`")

    (OUT_DIR / "execution_log.md").write_text("\n".join(log_lines) + "\n", encoding="utf-8")
    print(f"Model V2 pipeline complete in {timings['total_pipeline_sec']:.2f}s. Selected model: {selected_model}")
    print(f"Bootstrap 1,000-iter runtime: batters={timings['bootstrap_batters_1000_sec']:.2f}s, bowlers={timings['bootstrap_bowlers_1000_sec']:.2f}s")


if __name__ == "__main__":
    main()
