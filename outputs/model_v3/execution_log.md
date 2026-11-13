# Model V3 Execution Log

- **Run Timestamp:** 2026-11-13 18:40:40 UTC
- **Primary Dataset Scope:** `837` matches (`367` IPL, `470` T20I), `193,988` deliveries (`185,692` legal balls)
- **Selected Canonical Model:** `model_b` (selected objectively via `model_comparison.csv`)
- **Bootstrap Resamples:** `1000` stratified by `(comp_category, season_year)` (`seed=42`), full LPO/shrinkage/consistency/eligibility recomputed inside every iteration
- **V1 Immutability Check:** `checked=39, mismatches=0`

## Wall-Clock Timings

| Stage | Runtime (s) |
|---|---:|
| `phase1_foundation_sec` | 5.499 |
| `model_c_oos_sec` | 13.559 |
| `model_comparison_sec` | 54.510 |
| `bootstrap_batters_1000_sec` | 7.895 |
| `bootstrap_bowlers_1000_sec` | 10.020 |
| `bootstrap_total_sec` | 18.047 |
| `ranking_and_profiles_sec` | 0.521 |
| `sensitivity_suite_sec` | 106.031 |
| `charts_sec` | 9.376 |
| `total_pipeline_sec` | 207.547 |

## Canonical Top 10 Batters

| Rank | Player ID | Player Name | Score | Shrunk PWI | EB Cons | Boot Median (p05-p95) | Top-10 Freq | N_hp | Kish N_eff |
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

| Rank | Player ID | Player Name | Score | Shrunk PWI | EB Cons | Boot Median (p05-p95) | Top-10 Freq | N_hp | Kish N_eff |
|---:|---:|---|---:|---:|---:|---:|---:|---:|---:|
| 1 | 781 | Sunil Narine | +2.203 | +6.57 | 59.0% | 4.0 (1.0-17.0) | 84.9% | 422 | 893.3 |
| 2 | 2933 | Jasprit Bumrah | +2.141 | +7.61 | 54.2% | 4.0 (1.0-23.0) | 79.7% | 332 | 723.0 |
| 3 | 4722 | Rashid Khan | +1.994 | +5.59 | 58.0% | 6.0 (1.0-19.0) | 77.1% | 706 | 1560.2 |
| 4 | 7920 | Nathan Ellis | +1.699 | +5.50 | 53.2% | 8.0 (1.0-36.6) | 59.5% | 229 | 387.2 |
| 5 | 7699 | Abbas Afridi | +1.682 | +5.83 | 52.7% | 7.0 (1.0-28.0) | 34.8% | 124 | 209.9 |
| 6 | 39657 | Eshan Malinga | +1.563 | +3.85 | 57.2% | 9.0 (1.0-38.4) | 48.6% | 176 | 420.0 |
| 7 | 6450 | Mujeeb Ur Rahman | +1.549 | +5.05 | 53.4% | 9.0 (2.0-31.0) | 41.2% | 147 | 439.5 |
| 8 | 8661 | Matheesha Pathirana | +1.448 | +5.34 | 50.9% | 10.0 (1.0-41.0) | 50.4% | 307 | 556.1 |
| 9 | 2490 | Mohammad Nawaz | +1.343 | +4.00 | 54.5% | 13.0 (2.0-44.0) | 41.8% | 242 | 579.8 |
| 10 | 5809 | Naveen ul Haq | +1.082 | +3.62 | 51.1% | 17.0 (5.0-47.0) | 14.3% | 121 | 326.2 |

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
