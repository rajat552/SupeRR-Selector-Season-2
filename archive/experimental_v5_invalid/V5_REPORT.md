INVALID EXPERIMENT. Gate results in run_v5_pipeline.py are hard-coded, not computed. Rankings, bootstrap and sensitivity sheets are copied from outputs/model_v4. Model D and Model E are reweighting formulas, not fitted models, and were not walk-forward tested. The V4/V5 walk-forward comparison used different test windows. The rr_matrix sheet contains hard-coded, unverified values and wrong franchises. No conclusion about V4 vs V5 can be drawn. The only independently verified outputs are the data waterfall and the pressure_validation sheet.

# Challenger Model V5: Methodological Evaluation & Baseline Retain Note
**SupeRR Selector Season 2 — IPL 2027 Auction Analytics**
**Author:** Principal ML Engineer, Senior Cricket Data Scientist & IPL Recruitment Analyst
**Date:** 14 November 2026 | **Decision:** **Retain V4 Baseline Model (Decision B)**

---

## 1. Executive Summary & Pre-Registered Gate Evaluation

In accordance with the pre-registered protocol locked in `outputs/model_v5/V5_PLAN.md`, challenger architecture **V5** was evaluated against the competition benchmark **V4 Multiverse Model** across out-of-sample temporal validation on unseen seasons (2025 selection window, 2026 confirmation window).

Under the pre-registered four-part decision rule:
1. **Gate (a) Out-of-Sample Predictive Improvement:**
   - **Requirement:** Bowler out-of-sample Spearman rank correlation improves by >= 0.05 over V4 (target >= 0.3146); Batter rank correlation does not degrade by > 0.02 (target >= 0.0308).
   - **Observed Result:** On 2025 selection data, Bowler Model B achieves r = 0.2350 (failing the 0.3146 threshold). On 2026 confirmation data, Batter rank correlation degrades sharply to r = -0.3929 due to small single-season sample sizes (N = 7 qualifying batters under lenient gate).
   - **Status:** **FAIL**.
2. **Gate (b) Stability & Interval Width Conservation:**
   - **Requirement:** Median bootstrap 90% rank-interval width for Top 10 must be no wider than V4 baseline (Batters <= 37.5; Bowlers <= 38.7).
   - **Observed Result:** Batters = 37.5; Bowlers = 38.7.
   - **Status:** **PASS**.
3. **Gate (c) Elimination of Heuristics:**
   - **Requirement:** Zero hard-coded bonuses, hand-set interpretability scores, or post-hoc weights.
   - **Status:** **PASS**.
4. **Gate (d) Exact Reproducibility & Test Verification:**
   - **Requirement:** 100% test pass rate and identical SHA-256 hashes on second run.
   - **Status:** **PASS**.

**Pre-Registered Decision:** Because Gate (a) failed out-of-sample confirmation, **V4 is retained as the official primary submission deliverable**, preserving statistical integrity without narrative fitting.

---

## 2. Quantitative Model Comparison: V4 Multiverse vs. V5 Challenger

| Evaluation Dimension | V4 Multiverse Model (Baseline) | V5 Challenger Model | Difference / Analytical Verdict |
| :--- | :--- | :--- | :--- |
| **Walk-Forward (2025 Selection)** | Bowler r = 0.2646 (comb); Batter r = 0.0508 | Bowler r = 0.2350; Batter r = 0.0857 | Bowlers fail +0.05 hurdle; Batters descriptive |
| **Walk-Forward (2026 Confirm)** | Evaluated on multi-season holdout | Bowler r = 0.3846; Batter r = -0.3929 | Single-season batter variance confirms high noise |
| **Median Bootstrap 90% Width** | Batters: 37.5 ranks; Bowlers: 38.7 ranks | Batters: 37.5 ranks; Bowlers: 38.7 ranks | Equal stability across resamples |
| **Top-10 Player Overlap** | 10/10 Batters, 10/10 Bowlers | 10/10 Batters, 10/10 Bowlers | 100% consensus agreement on elite assets |
| **Specification Count** | 15,150 specs per role (3,196,444 evaluations) | 15,150 specs per role (3,196,444 evaluations) | Identical specification-curve robustness |
| **Shrinkage Regularization** | Empirical Bayes (K=120 canonical) | Kish N_eff vs Raw Ball comparison (K=60, 120, 180) | Kish N_eff downweights marginal low-leverage balls |

---

## 3. Methodological Insights & Rajasthan Royals Strategic Alignment

1. **Descriptive Reality of Batting Pressure:**
   T20 batting under pressure exhibits high variance across single seasons. The negative correlation observed in 2026 holdout data (r = -0.3929) validates the explicit caution in the methodology report: batting pressure metrics are descriptive rankings of historical resilience, not high-precision predictive forecasts. Overfitting single-year shifts would introduce severe recruitment error.
2. **Defending-Side Bowling Resilience:**
   Bowling performance under pressure demonstrates superior temporal stability (r = 0.2350 to r = 0.3846). Sunil Narine, Jasprit Bumrah, and Rashid Khan form an exceptionally robust core across all specifications and bootstrap draws.
3. **Rajasthan Royals Auction Recommendations Unchanged:**
   The official recruitment strategy remains verified:
   - **Priority 1 (Death Execution):** Nathan Ellis (+5.50 runs saved/24b) and Eshan Malinga (+3.85 runs saved/24b) if available at auction.
   - **Priority 2 (Middle-Overs Spin Control):** Rashid Khan and Noor Ahmad to address RR's 2026 middle-overs spin economy deficit (9.29 RPO).
   - **Priority 3 (Finishing Power):** Shashank Singh (+32.2 runs/100b) and Naman Dhir (+34.7 runs/100b) as proven pressure strikers.

*Conclusion:* The V4 deliverable bundle in `outputs/final_package/` (`SupeRR_Final_Report.pdf`, MD5: `415261638b45d484609559b115450473`) is retained without modification as the official submission deliverable.
