"""Full execution pipeline for Model V4 Multiverse Analysis & Submission Generation."""

from __future__ import annotations

import hashlib
import json
import time
from pathlib import Path
from typing import Dict, List, Tuple
import numpy as np
import pandas as pd

from . import build_foundation_dataset
from .data_loader import load_clean_dataset, RAW_DIR
from .multiverse import (
    ROOT_DIR,
    OUT_DIR,
    CHART_DIR,
    build_raw_foundation,
    evaluate_multiverse,
    analyze_multiverse_summary,
    run_variance_decomposition,
    plot_specification_curves,
    run_walk_forward_evaluation,
)
from .impact_models import compute_player_base_metrics, score_model_b
from .bootstrap import run_stratified_bootstrap
from .eligibility import BENCHMARK_GATE

MANIFEST_PATH = ROOT_DIR / "outputs" / "model_v2" / "integrity_manifest_pre.json"


def verify_v1_checksums() -> Dict[str, int]:
    """Verify all 39 V1/raw checksums."""
    manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
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


def main():
    t_start = time.perf_counter()
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    CHART_DIR.mkdir(parents=True, exist_ok=True)

    print("=== Step 0: Verifying V1 Immutability Manifest ===")
    chk = verify_v1_checksums()
    print(f"Checksum verification: {chk['checked']} files checked, {chk['mismatches']} mismatches.")
    assert chk["mismatches"] == 0, "V1 files modified! Aborting."

    parquet_path = OUT_DIR / "multiverse_ranks.parquet"
    if parquet_path.exists():
        print(f"\n=== Found existing multiverse ranks at {parquet_path} ===")
        multiverse_ranks_df = pd.read_parquet(parquet_path)
        print(f"Loaded {len(multiverse_ranks_df)} records.")
    else:
        print("\n=== Step 1: Loading Raw Data & Foundation Dataset ===")
        df_raw, matches, pe, player_lookup = build_raw_foundation()
        print(f"Loaded primary dataset: {len(df_raw)} deliveries across {len(matches)} matches.")

        print("\n=== Step 2: Executing Full Multiverse Grid ===")
        t_multi_start = time.perf_counter()
        multiverse_ranks_df = evaluate_multiverse(df_raw, matches, player_lookup)
        t_multi_end = time.perf_counter()
        multi_runtime = t_multi_end - t_multi_start
        print(f"Multiverse completed in {multi_runtime:.2f}s ({multi_runtime/60.0:.2f} min).")
        print(f"Total specification records generated: {len(multiverse_ranks_df)}")
        multiverse_ranks_df.to_parquet(parquet_path, index=False)
        print(f"Saved multiverse ranks to {parquet_path}")

    print("\n=== Step 3: Summarizing Multiverse Statistics ===")
    summary_bat = analyze_multiverse_summary(multiverse_ranks_df, "batter")
    summary_bowl = analyze_multiverse_summary(multiverse_ranks_df, "bowler")

    summary_bat.to_csv(OUT_DIR / "multiverse_summary_batters.csv", index=False)
    summary_bowl.to_csv(OUT_DIR / "multiverse_summary_bowlers.csv", index=False)
    print(f"Summary generated: {len(summary_bat)} batters, {len(summary_bowl)} bowlers evaluated.")

    print("\n=== Step 4: Running ANOVA Variance Decomposition ===")
    decomp_bat = run_variance_decomposition(multiverse_ranks_df, "batter")
    decomp_bowl = run_variance_decomposition(multiverse_ranks_df, "bowler")
    decomp = pd.concat([decomp_bat, decomp_bowl], ignore_index=True)
    decomp.to_csv(OUT_DIR / "variance_decomposition.csv", index=False)
    print("Variance decomposition saved to outputs/model_v4/variance_decomposition.csv")

    print("\n=== Step 5: Canonical Baseline & Stratified Bootstrap ===")
    df_canon, matches, pe, player_lookup, _ = build_foundation_dataset()

    canon_bat, _ = compute_player_base_metrics(df_canon, player_lookup, role="batter", wicket_mode=6.0, shrink_k=120.0, gate=BENCHMARK_GATE)
    canon_bat = score_model_b(canon_bat, role="batter")

    canon_bowl, _ = compute_player_base_metrics(df_canon, player_lookup, role="bowler", wicket_mode=6.0, shrink_k=120.0, gate=BENCHMARK_GATE)
    canon_bowl = score_model_b(canon_bowl, role="bowler")

    # Save unfiltered canonical rankings
    unfiltered_bat = canon_bat[canon_bat["is_eligible"]].sort_values("model_b_score", ascending=False).reset_index(drop=True)
    unfiltered_bat["canonical_rank"] = np.arange(1, len(unfiltered_bat) + 1)
    unfiltered_bat.to_csv(OUT_DIR / "unfiltered_all_batters.csv", index=False)
    unfiltered_bat.head(10).to_csv(OUT_DIR / "unfiltered_top10_batters.csv", index=False)

    unfiltered_bowl = canon_bowl[canon_bowl["is_eligible"]].sort_values("model_b_score", ascending=False).reset_index(drop=True)
    unfiltered_bowl["canonical_rank"] = np.arange(1, len(unfiltered_bowl) + 1)
    unfiltered_bowl.to_csv(OUT_DIR / "unfiltered_all_bowlers.csv", index=False)
    unfiltered_bowl.head(10).to_csv(OUT_DIR / "unfiltered_top10_bowlers.csv", index=False)

    boot_bat_path = OUT_DIR / "bootstrap_canonical_batters.csv"
    boot_bowl_path = OUT_DIR / "bootstrap_canonical_bowlers.csv"

    if boot_bat_path.exists() and boot_bowl_path.exists():
        print("Loading existing 1,000-draw bootstrap results...")
        boot_bat = pd.read_csv(boot_bat_path)
        boot_bowl = pd.read_csv(boot_bowl_path)
    else:
        print("Running 1,000-draw stratified bootstrap on canonical specification...")
        boot_bat, meta_bat = run_stratified_bootstrap(df_canon, player_lookup, role="batter", model_name="model_b", n_boot=1000, seed=42)
        boot_bowl, meta_bowl = run_stratified_bootstrap(df_canon, player_lookup, role="bowler", model_name="model_b", n_boot=1000, seed=42)
        boot_bat.to_csv(boot_bat_path, index=False)
        boot_bowl.to_csv(boot_bowl_path, index=False)

    print("\n=== Step 6: Applying Pre-Registered Selection Rule ===")
    def apply_rule(summary_df: pd.DataFrame, boot_df: pd.DataFrame, canon_df: pd.DataFrame, role: str) -> Tuple[pd.DataFrame, pd.DataFrame, List[str]]:
        id_col = "striker_id" if role == "batter" else "bowler_id"

        # Step 1: Candidate pool >= 50% eligibility
        pool = summary_df[summary_df["elig_share"] >= 0.50].copy()

        # Merge bootstrap eligible draws
        boot_sub = boot_df[[id_col, "valid_eligible_iters", "top10_inclusion_frequency"]].rename(
            columns={id_col: "player_id", "valid_eligible_iters": "eligible_draws", "top10_inclusion_frequency": "top10_draws_freq"}
        )
        pool = pool.merge(boot_sub, on="player_id", how="left")
        pool["eligible_draws"] = pool["eligible_draws"].fillna(0).astype(int)
        pool["top10_draws_freq"] = pool["top10_draws_freq"].fillna(0.0)

        # Merge canonical score
        c_sub = canon_df[[id_col, "model_b_score", "shrunk_wp_impact", "shrunk_norm_impact", "raw_pressure_lift", "maint_lift", "hp_balls"]].rename(
            columns={id_col: "player_id", "raw_pressure_lift": "raw_lift"}
        )
        pool = pool.merge(c_sub, on="player_id", how="left")

        # Step 2: Sort by multiverse top10_freq desc, break ties by lower median rank asc
        pool = pool.sort_values(by=["top10_freq", "median_rank", "iqr_rank"], ascending=[False, True, True]).reset_index(drop=True)

        # Step 3: Stability check: eligible in >= 800 / 1000 bootstrap draws
        selected = []
        removed_instability = []
        for _, p in pool.iterrows():
            if p["eligible_draws"] >= 800:
                selected.append(p)
                if len(selected) == 10:
                    break
            else:
                removed_instability.append(f"{p['player_name']} (draws: {p['eligible_draws']})")

        final_top10 = pd.DataFrame(selected)

        # Step 4: Confidence Tiers
        def assign_tier(freq: float) -> str:
            if freq >= 0.80:
                return "Tier 1 (Core Consensus)"
            elif freq >= 0.50:
                return "Tier 2 (Strong Contender)"
            else:
                return "Tier 3 (Context-Dependent)"

        final_top10["tier"] = final_top10["top10_freq"].apply(assign_tier)
        final_top10["final_rank"] = np.arange(1, len(final_top10) + 1)

        return final_top10, pool, removed_instability

    final_top10_bat, pool_bat, removed_bat = apply_rule(summary_bat, boot_bat, unfiltered_bat, "batter")
    final_top10_bowl, pool_bowl, removed_bowl = apply_rule(summary_bowl, boot_bowl, unfiltered_bowl, "bowler")

    final_top10_bat.to_csv(OUT_DIR / "final_top10_batters.csv", index=False)
    final_top10_bowl.to_csv(OUT_DIR / "final_top10_bowlers.csv", index=False)

    print("Final Top 10 Batters:")
    print(final_top10_bat[["final_rank", "player_name", "tier", "top10_freq", "median_rank", "eligible_draws", "model_b_score"]])
    print("\nFinal Top 10 Bowlers:")
    print(final_top10_bowl[["final_rank", "player_name", "tier", "top10_freq", "median_rank", "eligible_draws", "model_b_score"]])
    print(f"\nRemoved due to stability check (<800 bootstrap draws): Batters: {removed_bat}; Bowlers: {removed_bowl}")

    print("\n=== Step 7: Generating Specification Curve Charts ===")
    plot_specification_curves(multiverse_ranks_df, summary_bat, "batter", top_n=15)
    plot_specification_curves(multiverse_ranks_df, summary_bowl, "bowler", top_n=15)
    print("Specification curves saved to outputs/model_v4/charts/")

    print("\n=== Step 8: Evaluating Walk-Forward Temporal Stability ===")
    wf_df = run_walk_forward_evaluation(df_canon, player_lookup, summary_bat, summary_bowl)
    wf_df.to_csv(OUT_DIR / "walk_forward_rankings.csv", index=False)
    print("Walk-forward stability results:")
    print(wf_df)

    t_total = time.perf_counter() - t_start
    print(f"\nPipeline finished in {t_total:.2f}s ({t_total/60.0:.2f} min).")


if __name__ == "__main__":
    main()
