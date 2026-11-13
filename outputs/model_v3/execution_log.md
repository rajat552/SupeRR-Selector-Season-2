# Model V3 Execution Log

- **Run Timestamp:** 2026-11-13 20:13:16 UTC
- **Primary Dataset Scope:** `837` matches (`367` IPL, `470` T20I), `193,988` deliveries (`185,692` legal balls)
- **Selected Canonical Model:** `model_b` (selected objectively via `model_comparison.csv`)
- **Bootstrap Resamples:** `1000` stratified by `(comp_category, season_year)` (`seed=42`), full LPO/shrinkage/consistency/eligibility recomputed inside every iteration
- **V1 Immutability Check:** `checked=39, mismatches=0`

## Wall-Clock Timings

| Stage | Runtime (s) |
|---|---:|
| `phase1_foundation_sec` | 4.890 |
| `model_c_oos_sec` | 12.402 |
| `model_comparison_sec` | 57.864 |
| `bootstrap_batters_1000_sec` | 8.704 |
| `bootstrap_bowlers_1000_sec` | 11.392 |
| `bootstrap_total_sec` | 20.274 |
| `ranking_and_profiles_sec` | 0.557 |
| `sensitivity_suite_sec` | 80.834 |
| `charts_sec` | 4.289 |
| `total_pipeline_sec` | 181.113 |

## Canonical Top 10 Batters

| Rank | Player ID | Player Name | Score | Shrunk PWI | EB Cons | Boot Median (p05-p95) | Top-10 Freq | N_hp | Kish N_eff |
|---:|---:|---|---:|---:|---:|---:|---:|---:|---:|
| 1 | 6396 | Tim David | +2.484 | +42.91 | 64.9% | 3.0 (1.0-16.0) | 87.3% | 570 | 744.3 |
| 2 | 37052 | Naman Dhir | +2.114 | +34.72 | 62.4% | 5.0 (1.0-32.0) | 64.9% | 186 | 286.7 |
| 3 | 768 | Reeza Hendricks | +1.757 | +31.49 | 60.6% | 8.0 (1.0-35.1) | 53.2% | 223 | 424.9 |
| 4 | 6726 | Romario Shepherd | +1.738 | +28.73 | 66.1% | 10.0 (2.0-36.0) | 51.2% | 431 | 507.4 |
| 5 | 4722 | Rashid Khan | +1.736 | +28.07 | 62.6% | 8.0 (1.0-40.3) | 58.8% | 377 | 427.9 |
| 6 | 2756 | Shashank Singh | +1.725 | +32.24 | 60.2% | 9.0 (1.0-44.0) | 56.3% | 327 | 402.1 |
| 7 | 143 | Dinesh Karthik | +1.678 | +34.40 | 58.4% | 10.5 (1.0-44.0) | 49.7% | 250 | 372.0 |
| 8 | 4708 | Rinku Singh | +1.601 | +31.01 | 59.9% | 10.0 (2.0-39.0) | 52.9% | 507 | 711.1 |
| 9 | 1318 | Andre Russell | +1.530 | +31.85 | 60.5% | 12.0 (2.0-54.0) | 47.0% | 347 | 490.0 |
| 10 | 4260 | Heinrich Klaasen | +1.482 | +24.88 | 65.6% | 15.0 (5.0-34.0) | 29.5% | 459 | 772.9 |

## Canonical Top 10 Bowlers

| Rank | Player ID | Player Name | Score | Shrunk PWI | EB Cons | Boot Median (p05-p95) | Top-10 Freq | N_hp | Kish N_eff |
|---:|---:|---|---:|---:|---:|---:|---:|---:|---:|
| 1 | 781 | Sunil Narine | +2.203 | +6.57 | 59.0% | 4.0 (1.0-17.0) | 84.9% | 422 | 893.3 |
| 2 | 2933 | Jasprit Bumrah | +2.141 | +7.61 | 54.2% | 4.0 (1.0-23.0) | 79.7% | 332 | 723.0 |
| 3 | 4722 | Rashid Khan | +1.994 | +5.59 | 58.0% | 6.0 (1.0-19.0) | 77.1% | 706 | 1560.2 |
| 4 | 7920 | Nathan Ellis | +1.699 | +5.50 | 53.2% | 8.0 (1.0-36.6) | 59.5% | 229 | 387.2 |
| 5 | 39657 | Eshan Malinga | +1.563 | +3.85 | 57.2% | 9.0 (1.0-38.4) | 48.6% | 176 | 420.0 |
| 6 | 8661 | Matheesha Pathirana | +1.448 | +5.34 | 50.9% | 10.0 (1.0-41.0) | 50.4% | 307 | 556.1 |
| 7 | 2490 | Mohammad Nawaz | +1.343 | +4.00 | 54.5% | 13.0 (2.0-44.0) | 41.8% | 242 | 579.8 |
| 8 | 6464 | Arshdeep Singh | +0.878 | +1.90 | 55.0% | 25.5 (9.0-55.0) | 7.7% | 593 | 1193.3 |
| 9 | 4219 | Krunal Pandya | +0.870 | +3.15 | 50.2% | 23.0 (5.0-63.0) | 18.4% | 372 | 740.8 |
| 10 | 4900 | Wanindu Hasaranga | +0.849 | +2.78 | 52.0% | 25.0 (8.0-55.0) | 8.5% | 504 | 1177.8 |

## Generated Charts (12 PNGs)

- `01_top10_batters_ranking.png`
- `02_top10_bowlers_ranking.png`
- `03_pressure_vs_normal_impact.png`
- `04_pressure_performance_comparison.png`
- `05_batter_role_analysis.png`
- `06_bowling_phase_analysis.png`
- `07_pressure_consistency_analysis.png`
- `08_bootstrap_rank_uncertainty.png`
- `09_ipl_vs_t20i_comparison.png`
- `10_player_sample_size_comparison.png`
- `11_model_sensitivity_comparison.png`
- `12_rr_recruitment_fit_matrix.png`
