# Requirements Traceability Matrix — SupeRR Selector Season 2 (Round 1)

This document establishes the end-to-end verification and compliance mapping between all official competition requirements and the final submission deliverables:
- **Source A:** Official Problem Statement (`data/raw/Round 1 Problem Statement _ SupeRR Selector Season 2.docx.pdf`)
- **Source B:** Live Unstop Competition Interface & Guidelines
- **Primary Deliverables:** `outputs/submission_v3/SupeRR_Round1_Report.pdf` (12–15 Page Executive Methodology Report), `outputs/submission_v3/source_register.md`, and reproducible analytical codebase (`src/model_v3/`).

---

## 1. Traceability Mapping

| ID | Requirement Source | Exact Requirement Description | Addressed In Report Section | Codebase / Output Artifact | Compliance Verification Status |
|---|---|---|---|---|---|
| **REQ-A1** | Source A | Two separate, ordered top-10 lists (batters and bowlers) ranked by performance under high pressure compared with usual performance. | **Page 1 / Section 1:** Executive Summary & Canonical Rankings | `outputs/model_v3/final_top10_batters.csv`<br>`outputs/model_v3/final_top10_bowlers.csv` | **FULLY COMPLIANT:** Both Top 10 lists appear prominently on Page 1, ordered 1–10 with composite score and tiering. |
| **REQ-A2** | Source A | Clear definition of high-pressure situations and justification for why this definition captures genuine match pressure. | **Section 2:** Mathematical Definition of High Pressure | `src/model_v3/pressure_model.py`<br>`outputs/model_v3/pressure_sensitivity.csv` | **FULLY COMPLIANT:** Pressure Index (PI) derived from pre-delivery context ($PI \ge 0.50$), capturing RRR, wickets down, and death overs without outcome leakage. |
| **REQ-A3** | Source A | Performance measurement methodology: exact metrics, expected/baseline performance calculations, and scoring logic. | **Section 3:** Performance Measurement & Leave-Player-Out Baselines | `src/model_v3/context_baselines.py`<br>`src/model_v3/impact_models.py` | **FULLY COMPLIANT:** Context-adjusted Run Expectancy (LPO cells with fallback), wicket valuations ($w=6.0$), and Empirical Bayes shrinkage via Kish $N_{eff}$. |
| **REQ-A4** | Source A | Fair comparisons across players: sample size handling, eligibility criteria, match context adjustments, and IPL vs T20I comparability. | **Section 4:** Fair Comparison Architecture & Cross-Format Harmonization | `src/model_v3/eligibility.py`<br>`src/model_v3/opponent_strength.py` | **FULLY COMPLIANT:** Pre-match Elo tracks, dual-role eligibility thresholds ($\ge 120$ HP balls or Kish $N_{eff} \ge 80$), and 800+ draw bootstrap stability filter. |
| **REQ-A5** | Source A | Detailed statistical evidence justifying each of the 20 player selections and their relative ordering. | **Section 5:** Deep-Dive Evidence for Top 10 Batters<br>**Section 6:** Deep-Dive Evidence for Top 10 Bowlers | `outputs/model_v3/batter_player_profiles.csv`<br>`outputs/model_v3/bowler_player_profiles.csv` | **FULLY COMPLIANT:** Complete player dossiers covering raw lift, shrunk PWI, phase splits, boundary/dot frequencies, and bootstrap rank CIs. |
| **REQ-A6** | Source A | Reliability and limitations: cross-match consistency, model uncertainty, bootstrap confidence intervals, and sensitivity analysis. | **Section 7:** Statistical Reliability, Consistency & Robustness Diagnostics | `outputs/model_v3/bootstrap_results_*.csv`<br>`outputs/model_v3/loso_sensitivity.csv`<br>`outputs/model_v3/wicket_sensitivity.csv` | **FULLY COMPLIANT:** 1,000-resample stratified match-cluster bootstrap, Beta-binomial shrinkage, LOSO validation, and wicket-sensitivity tests. |
| **REQ-A7** | Source A | Objective, reproducible rankings derived strictly from the supplied dataset, free from reputation bias or external overrides. | **Section 8:** Reproducibility, Auditing & Pipeline Integrity | `src/model_v3/run_pipeline.py`<br>`outputs/model_v2/integrity_manifest_pre.json` | **FULLY COMPLIANT:** 100% deterministic pipeline (`seed=42`), zero manual overrides; all 39 V1 baseline checksums verified bit-identical. |
| **REQ-A8** | Source A | Absence of arbitrary uncapped-player or auction-eligibility restrictions in statistical modeling. | **Section 1 & Section 8** | `src/model_v3/ranking.py` | **FULLY COMPLIANT:** All players evaluated purely on merit; practical franchise availability treated as external overlay without modifying scores. |
| **REQ-B1** | Source B | Submission via single PDF document upload (no dropdown fields in live Unstop interface). | **Entire Submission PDF** | `outputs/submission_v3/SupeRR_Round1_Report.pdf` | **FULLY COMPLIANT:** Self-contained 12–15 page PDF document formatted to publication standards. |
| **REQ-B2** | Source B | Page 1 layout: Both Top-10 lists, 1-line pressure definition, and 3 key findings displayed immediately. | **Page 1:** Executive Summary & Canonical Rankings | `outputs/submission_v3/SupeRR_Round1_Report.pdf` (Page 1) | **FULLY COMPLIANT:** Page 1 acts as a standalone executive dashboard for Rajasthan Royals leadership. |
| **REQ-B3** | Source B | Rajasthan Royals squad fit analysis: every one of the 20 players must have an actionable recruitment note for IPL 2027. | **Section 9:** Rajasthan Royals IPL 2027 Squad Architecture & Fit Dossier | `outputs/submission_v3/SupeRR_Round1_Report.pdf`<br>`outputs/model_v3/charts/12_rr_recruitment_fit_matrix.png` | **FULLY COMPLIANT:** Individual tactical notes for all 20 players addressing RR's 2026 tactical gaps (death bowling ER 11.39, middle-overs boundary drought). |
| **REQ-B4** | Source B | External player research and source register: public franchise, active status, and auction pathways backed by URLs and dates. | **Section 9 & Appendix B:** External Source Register | `outputs/submission_v3/source_register.md` | **FULLY COMPLIANT:** All claims backed by public sports journalism and official BCCI/IPL releases; unconfirmed retentions explicitly tagged "UNVERIFIED". |
| **REQ-B5** | Source B | Ground-truth RR 2026 performance figures recomputed strictly from raw data using `player_id`. | **Section 9:** RR 2026 Benchmark Context | `data/raw/*.csv`<br>`outputs/submission_v3/SupeRR_Round1_Report.md` | **FULLY COMPLIANT:** All figures re-calculated directly from `ball_by_ball.csv` and `matches.csv` (e.g., Sandeep Sharma 6 apps, 19.4 ov, ER 11.39). |

---

## 2. Section Structure of Submission Report (`SupeRR_Round1_Report.pdf`)

1. **Page 1:** Executive Summary, Canonical Batting & Bowling Top 10 Tables (with Statistical Tiers), One-Line Pressure Definition, and Three Core Strategic Findings.
2. **Section 2:** Mathematical Formalization of High Pressure (Pre-Delivery Win Probability, Pressure Index, and Match State Decomposition).
3. **Section 3:** Performance Measurement & Leave-Player-Out Context Baselines (Runs-Above-Par, Wicket Weighting, Kish $N_{eff}$, and Empirical Bayes Shrinkage).
4. **Section 4:** Fair Comparison Architecture (Sample Size Gates, Dual-Role Exposure, Elo Match Adjustment, and IPL vs T20I Comparability).
5. **Section 5:** Deep-Dive Performance Evidence — Top 10 Batters (Metrics, Profiles, Matchups, Phase Distributions, and Statistical Tiers).
6. **Section 6:** Deep-Dive Performance Evidence — Top 10 Bowlers (Metrics, Profiles, Matchups, Phase Distributions, and Statistical Tiers).
7. **Section 7:** Statistical Reliability, Consistency & Robustness Diagnostics (Stratified Match-Cluster Bootstrap, LOSO Stability, Wicket-Weight Sensitivity, and Definition Invariance).
8. **Section 8:** Limitations, Model Boundaries & Methodological Integrity (Boundary Conditions, Data Constraints, Zero Look-Ahead, and V1 Immutability).
9. **Section 9:** Rajasthan Royals IPL 2027 Recruitment & Squad Architecture Strategy (2026 Squad Deficits, Target Segmentation, Practical Overlays, and 20 Player Recruitment Fit Dossiers).
10. **Section 10:** Conclusion & Operational Roadmap for IPL 2027 Auction.
11. **Appendix A:** Complete Mathematical Formulations & Notation Reference.
12. **Appendix B:** External Source Register & Methodology Audit Log.

