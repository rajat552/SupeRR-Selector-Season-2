# Model V2 Execution Log

- **Run Timestamp:** 2026-11-12 15:22:19 UTC
- **Primary Dataset Scope:** `837` matches (`367` IPL, `470` T20I), `193,988` deliveries (`185,692` legal balls)
- **Selected Canonical Model:** `model_b` (selected objectively via `model_comparison.csv`)
- **Bootstrap Resamples:** `1000` stratified by `(comp_category, season_year)` (`seed=42`), full LPO/shrinkage/consistency/eligibility recomputed inside every iteration
- **V1 Immutability Check:** `checked=39, mismatches=0`

## Wall-Clock Timings

| Stage | Runtime (s) |
|---|---:|
| `phase1_foundation_sec` | 6.910 |
| `model_c_oos_sec` | 16.942 |
| `model_comparison_sec` | 72.278 |
| `bootstrap_batters_1000_sec` | 9.266 |
| `bootstrap_bowlers_1000_sec` | 10.183 |
| `bootstrap_total_sec` | 19.634 |
| `ranking_and_profiles_sec` | 0.690 |
| `sensitivity_suite_sec` | 83.184 |
| `charts_sec` | 6.849 |
| `total_pipeline_sec` | 206.488 |

## Canonical Top 10 Batters

| Rank | Player ID | Player Name | Score | Shrunk WP Impact | EB Cons | Boot Median (p05-p95) | Top-10 Freq | N_hp | Kish N_eff |
|---:|---:|---|---:|---:|---:|---:|---:|---:|---:|
| 1 | 6396 | Tim David | +2.434 | +41.75 | 63.0% | 3.0 (1.0-16.0) | 89.3% | 570 | 744.3 |
| 2 | 796 | Matthew Wade | +2.267 | +33.20 | 63.5% | 3.0 (1.0-14.0) | 64.9% | 158 | 254.9 |
| 3 | 37052 | Naman Dhir | +2.028 | +33.57 | 60.1% | 5.0 (1.0-33.0) | 66.1% | 186 | 286.7 |
| 4 | 143 | Dinesh Karthik | +1.764 | +36.24 | 56.2% | 8.0 (1.0-38.0) | 60.9% | 250 | 372.0 |
| 5 | 768 | Reeza Hendricks | +1.745 | +29.59 | 59.8% | 8.0 (2.0-35.1) | 54.3% | 223 | 424.9 |
| 6 | 2756 | Shashank Singh | +1.609 | +32.42 | 56.6% | 9.0 (1.0-45.0) | 55.6% | 327 | 402.1 |
| 7 | 4260 | Heinrich Klaasen | +1.608 | +25.20 | 65.0% | 12.0 (3.9-31.0) | 41.9% | 459 | 772.9 |
| 8 | 4708 | Rinku Singh | +1.445 | +28.87 | 58.1% | 11.0 (2.0-43.0) | 47.8% | 507 | 711.1 |
| 9 | 1318 | Andre Russell | +1.434 | +29.57 | 59.8% | 12.0 (2.0-55.0) | 45.7% | 347 | 490.0 |
| 10 | 8101 | Ashutosh Sharma | +1.335 | +24.97 | 58.3% | 12.0 (2.0-52.0) | 28.0% | 273 | 290.6 |

## Canonical Top 10 Bowlers

| Rank | Player ID | Player Name | Score | Shrunk WP Impact | EB Cons | Boot Median (p05-p95) | Top-10 Freq | N_hp | Kish N_eff |
|---:|---:|---|---:|---:|---:|---:|---:|---:|---:|
| 1 | 781 | Sunil Narine | +2.481 | +9.98 | 71.4% | 4.0 (1.0-13.0) | 90.5% | 454 | 739.6 |
| 2 | 2933 | Jasprit Bumrah | +1.995 | +9.61 | 65.3% | 7.0 (1.0-33.0) | 65.7% | 496 | 785.1 |
| 3 | 4373 | Mustafizur Rahman | +1.851 | +8.04 | 66.5% | 11.0 (2.0-38.0) | 49.3% | 500 | 749.5 |
| 4 | 2382 | Jamie Overton | +1.839 | +8.84 | 61.1% | 8.0 (1.0-41.0) | 46.9% | 165 | 250.6 |
| 5 | 2878 | Mohit Sharma | +1.736 | +7.69 | 63.2% | 12.0 (1.0-55.0) | 43.4% | 277 | 370.6 |
| 6 | 5577 | Sai Kishore | +1.708 | +7.72 | 63.1% | 6.0 (2.0-17.3) | 37.0% | 123 | 204.5 |
| 7 | 34485 | Sufiyan Muqeem | +1.665 | +7.90 | 62.2% | 10.0 (1.0-73.0) | 32.0% | 148 | 214.8 |
| 8 | 6669 | Mohsin Khan | +1.625 | +8.16 | 61.8% | 11.0 (1.0-61.4) | 41.3% | 163 | 283.6 |
| 9 | 2490 | Mohammad Nawaz | +1.556 | +7.94 | 60.9% | 13.0 (2.0-45.1) | 41.7% | 282 | 486.9 |
| 10 | 830 | Josh Hazlewood | +1.472 | +7.49 | 63.3% | 16.0 (2.0-53.0) | 34.9% | 436 | 692.8 |

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
