# SupeRR Selector Season 2: V4 Multiverse Reproducibility Audit
**Auditor:** Rajat Aggarwal (Senior Cricket Data Scientist)
**Date:** 2026-11-14 | **Result: 100% BITWISE & MATHEMATICAL REPRODUCIBILITY CONFIRMED**

## 1. Reproducibility Comparison Table

| Output File | Evaluation Metric | Reference Value | Rerun Value | Maximum Absolute Difference | Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `final_top10_batters.csv` | Player identity, ordering, tiers & core metrics | 10 players | 10 players | `0.00e+00` | **PASS** |
| `final_top10_bowlers.csv` | Player identity, ordering, tiers & core metrics | 10 players | 10 players | `0.00e+00` | **PASS** |
| `multiverse_summary_batters.csv` | top10_freq & median_rank across all evaluated players | 149 rows | 149 rows | `0.00e+00` | **PASS** |
| `multiverse_summary_bowlers.csv` | top10_freq & median_rank across all evaluated players | 185 rows | 185 rows | `0.00e+00` | **PASS** |
| `bootstrap_canonical_batters.csv` | valid_eligible_iters, boot_p05_rank, boot_p95_rank (seed=42) | 824 rows | 824 rows | `0.00e+00` | **PASS** |
| `bootstrap_canonical_bowlers.csv` | valid_eligible_iters, boot_p05_rank, boot_p95_rank (seed=42) | 596 rows | 596 rows | `0.00e+00` | **PASS** |
| `walk_forward_rankings.csv` | canonical & consensus spearman_corr (2022-2024 vs 2025-2026) | 2 rows | 2 rows | `0.00e+00` | **PASS** |
| `variance_decomposition.csv` | Sequential Type I ANOVA sum_of_squares | 18 rows | 18 rows | `0.00e+00` | **PASS** |

## 2. Top-10 Finalist List Equivalence Confirmation

- **Batters:** Exactly identical 10 players, in identical order, with identical consensus frequencies, bootstrap draws, and confidence tiers (Shashank Singh #1, Tim David #2, Naman Dhir #3, Dinesh Karthik #4, Heinrich Klaasen #5, Suryakumar Yadav #6, Rinku Singh #7, Romario Shepherd #8, Andre Russell #9, Rashid Khan #10).
- **Bowlers:** Exactly identical 10 players, in identical order, with identical consensus frequencies, bootstrap draws, and confidence tiers (Sunil Narine #1, Jasprit Bumrah #2, Rashid Khan #3, Matheesha Pathirana #4, Eshan Malinga #5, Nathan Ellis #6, Noor Ahmad #7, Arshdeep Singh #8, Prasidh Krishna #9, Bhuvneshwar Kumar #10).

**Conclusion:** The Model V4 pipeline executes with zero divergence from reference outputs across all specifications and bootstrap iterations.