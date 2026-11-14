# V5 Analytical Architecture, Pre-Registration Protocol & Plan
**SupeRR Selector Season 2 — Round 1 Analytics Challenge**
**Author:** Principal ML Engineer, Senior Cricket Data Scientist & IPL Recruitment Analyst
**Date:** 2026-11-14 | **Pre-Registration Status:** Locked (Pre-Execution)
**Baseline Default:** V4 Multiverse Model (`outputs/final_package/SupeRR_Final_Report.pdf`)
**Hard Freeze Deadline:** 17 November 2026, 9:00 PM IST (Competition Deadline: 18 Nov 2026, 11:59 PM IST)

---

## 1. Executive Context & Architectural Governance

The SupeRR Selector Season 2 challenge requires identifying and ranking the most reliable players under pressure in T20 cricket (IPL and T20Is from 2022 to 2026) compared with their usual performance levels, providing an evidence-backed recruitment strategy for Rajasthan Royals ahead of the IPL 2027 auction.

The audited **V4 Multiverse pipeline** represents the verified baseline, evaluating 15,150 specifications per role across 3,196,444 player-specification evaluations and 1,000 stratified match-cluster bootstrap draws. 

The **V5 initiative** is an adversarial, statistically principled challenger model designed to rigorously evaluate whether:
1. Pressure weighting, continuous sigmoid scaling, and discrete thresholding can be mathematically disentangled without ambiguity;
2. Regularized hierarchical partial pooling (separating run-scoring and dismissal hazards) or exposure-adjusted match-level reliability modeling outperforms the V4 specification curve out-of-sample;
3. Out-of-sample temporal predictive stability on unseen seasons (2025 selection, 2026 confirmation) can improve without widening bootstrap rank-interval uncertainty.

### Strict Governance & Immutability Rules
- **Protected Paths (Read-Only):** `data/raw/*`, `src/model_v2/*`, `src/model_v3/*`, `src/model_v4/*`, `tests/model_v2/*`, `tests/model_v3/*`, `tests/model_v4/*`, `outputs/model_v2/*`, `outputs/model_v3/*`, `outputs/model_v4/*`, `outputs/data_audit/*`, `outputs/submission_final/*`, `outputs/final_package/*`, `archive/*`.
- **Minimal File Footprint:**
  - `src/model_v5/` (mirrored from V4; only necessary architectural enhancements added)
  - `tests/model_v5/` (unit and statistical test suite for V5)
  - `outputs/model_v5/` containing only:
    1. `V5_PLAN.md` (this locked protocol)
    2. `V5_LOG.md` (execution history, runtimes, SHA-256 fingerprints, deviations)
    3. `v5_results.xlsx` (multi-tab comprehensive workbook)
    4. `charts/` (maximum 8 publication-grade charts)
    5. `V5_REPORT.md` and `V5_REPORT.pdf` (12–16 pages if V5 is adopted; 2-page comparison note if V4 is retained)
- **Time-Box Guarantee:** V5 must be fully run, tested, and verified by **17 Nov 2026, 9:00 PM IST**. If any failure occurs or the deadline is breached, V5 is halted immediately and the verified V4 deliverable is retained.

---

## 2. What We Will Change and Why (Part-by-Part Technical Specification)

### Part 2 — Data Re-Audit & Scope Verification
- **What We Will Prove:**
  - Full scope reconstruction via unique delivery IDs:
    - Raw input: 200,999 delivery records across 883 matches.
    - Exclusion of `Other_T20` (`comp_id` 2670, 3289): 30 matches, 6,985 deliveries.
    - Exclusion of Super Overs (`innings` 3 and 4): 38 total deliveries across all competitions, of which 12 occurred in `Other_T20`. The net incremental exclusion is exactly 26 deliveries.
    - Final Primary Scope: 200,999 - 6,985 - 26 = 193,988 deliveries across 837 matches with deliveries (367 IPL, 470 T20I), comprising exactly 185,692 legal deliveries.
    - Abandoned fixtures: 16 matches with zero deliveries recorded.
  - **DLS Match Accounting Reconciliation:**
    - Reconcile the earlier historical mention of "19 DLS matches" with the schema reality:
    - Exactly 19 matches in `matches.csv` contain the explicit substring `"DLS"` or `"D/L"` in their text `result` column.
    - However, exactly **34 matches** in the primary 837-match scope contain at least one non-null Duckworth-Lewis-Stern / rain-curtailment field (`first_inn_revised_overs`, `second_inn_revised_overs`, or `revised_target`).
    - Of these 34 matches: 23 have `revised_target` populated; 25 have `second_inn_revised_overs` populated; 25 have `first_inn_revised_overs` populated.
    - All revised overs columns store ball counts (e.g., 114.0 = 19 overs), never fractional overs.
  - **Cricket Accounting Standards:**
    - Extras: Wides are non-legal and not faced by batter; No-balls (`Overstep`, `other`) are non-legal for bowler, legal faced ball for batter; Byes/Leg-byes are legal balls, excluded from bowler runs conceded.
    - Bowler wickets strictly exclude `RunOut`, `Retire Out`, and `Obstructing the field`.
    - Disambiguate homonyms strictly by `player_id` (e.g. Abdul Samad 7446 vs 6922; Rashid Khan 4722 vs 20172).
  - **Output:** Stored in `v5_results.xlsx` (Sheet 1: `data_waterfall`).

### Part 3 — Pressure Definitions & Outcome Validation
- **What We Will Change & Disentangle:**
  - V4 models contained overlapping operational definitions between continuous pressure weights and discrete pressure slices. V5 explicitly separates and formalizes three distinct objects:
    1. **Raw Continuous Pressure Index ($PI \in [0, 1]$):**
       - 2nd Innings: Dynamic leverage function combining Required Run Rate ($RRR$), Balls Remaining ($B_{\text{rem}}$), and Wickets in Hand ($W_{\text{hand}}$).
       - 1st Innings: Early collapse leverage and late-overs acceleration urgency.
    2. **Continuous Logistic Weight ($w_k \in [0, 1]$):**
       $$w_k = \frac{1}{1 + \exp\left(-\frac{PI_k - x_0}{s}\right)}, \quad \text{Canonical: } x_0 = 0.425, \; s = 0.08$$
    3. **Discrete Pressure Thresholds:**
       - High Pressure ($HP$): $PI \ge 0.50$ (where $w_k \ge 0.718$).
       - Normal / Baseline ($Normal$): $PI < 0.35$ (where $w_k \le 0.280$).
       - Intermediate Buffer: $0.35 \le PI < 0.50$ (unambiguously excluded from discrete contrasts).
    - **Crucial Mathematical Proof:** Note that $w_k \ge 0.50 \iff PI_k \ge 0.425$. Thus, a threshold on $w$ is NOT interchangeable with a threshold on $PI$. V5 documents and implements these with absolute precision.
  - **Empirical Validation of Pressure Separation:**
    - Contrast $PI \ge 0.50$ vs $PI < 0.35$ on legal deliveries using match-clustered 95% confidence intervals.
    - Evaluate batting outcomes: Scoring rate / Strike Rate, dot ball %, boundary %, dismissal hazard.
    - Evaluate bowling outcomes: Defending-side pressure index; Economy Rate, dot ball %, boundary conceded %, wicket strike rate.
  - **Continuous Parameter Sensitivity Grid:**
    - Sigmoid centres: $x_0 \in \{0.40, 0.425, 0.45\}$
    - Sigmoid scale / bandwidth: $s \in \{0.06, 0.08, 0.12\}$
    - Structural enhancements: 1st innings early collapse acceleration, 2nd innings chase urgency, dead-chase damping (strictly pre-delivery state; zero look-ahead).
    - **Selection Rule:** Parameters selected strictly on cricket validity and empirical outcome separation, never on which players they promote. Labeled descriptive validation, not causal.
  - **Output:** Stored in `v5_results.xlsx` (Sheet 2: `pressure_validation`).

### Part 4 — Candidate Models & Regularization Architecture
- **Candidate Models Evaluated:**
  - **Model A (Absolute Pressure Performance):** Evaluates shrunk performance directly on high-pressure deliveries ($PWI_{\text{shrunk}}$).
  - **Model B (Maintenance & Lift):** Formulated rigorously as an attenuated baseline adjustment:
    $$Score = \alpha \cdot PWI_{\text{shrunk}} + (1 - \alpha) \cdot \text{Lift}_{\text{shrunk}} = PWI_{\text{shrunk}} - (1 - \alpha) \cdot \text{Normal}_{\text{shrunk}}, \quad \alpha = 0.60$$
  - **Candidate 1 (Model D — Regularized Hierarchical Player × Pressure Model):**
    - Partially pooled GLM decomposing performance into separate components:
      - Batting: Runs per ball (Poisson/Negative Binomial with log-link) and dismissal hazard (logistic link).
      - Bowling: Runs conceded per ball and wicket hazard.
      - Fixed effects: Phase, competition format, and opponent Elo rating.
      - Random/shrunk effects: Player baseline and player $\times$ pressure interaction effect.
  - **Candidate 2 (Model E — Exposure-Adjusted Match-Level Reliability Model):**
    - Evaluates match-to-match reliability under pressure using sample-weighted variance and consistency metrics across qualifying high-pressure match appearances with Kish $N_{\text{eff}}$ exposure weighting.
  - **Time-Boxed Execution:** Runtime of Candidate 1 and Candidate 2 will be estimated beforehand. If full MCMC or iterative Newton-Raphson cannot complete within the strict time limits, closed-form empirical Bayes / L2-regularized ridge approximations will be deployed. Any model unable to finish within budget will be pruned and logged.
  - **Shrinkage & Regularization Comparison:**
    - Prior weight: $K \in \{60, 120, 180\}$ evaluated on Kish effective sample size $N_{\text{eff}} = \frac{(\sum w)^2}{\sum w^2}$ versus raw ball counts.
    - Consistency prior: Uniform $\text{Beta}(1, 1)$ vs informative $\text{Beta}(5, 5)$ vs Empirical Bayes prior with posterior credible intervals.
    - **Unmixed Column Reporting:** In all tables and profiles, raw HP balls, sum of weights $\sum w$, Kish $N_{\text{eff}}$, qualifying matches, shrunk impact, and shrunk consistency are reported as distinct columns, never blended into opaque composites.
  - **Output:** Stored in `v5_results.xlsx` (Sheet 3: `model_comparison`).

---

## 3. Pre-Registered Decision Rule (Part 5)

To prevent researcher degrees of freedom, confirmation bias, or narrative fitting, the adoption of V5 over V4 is governed by a strictly locked four-part decision rule:

### Temporal Validation Design
- **Development & Training Window:** 2022–2024 seasons (all matches).
- **Model Selection Window:** 2025 season (unseen out-of-sample data).
- **Final Confirmation Window:** 2026 season (held-out test data, never touched during model design or hyperparameter tuning).

### Pre-Registered Adoption Gates
V5 will be adopted if and only if **ALL FOUR** of the following quantitative conditions are satisfied on the 2025 selection data AND confirmed on the 2026 confirmation data:

1. **Gate (a) — Out-of-Sample Predictive Improvement:**
   - For Bowlers: Out-of-sample Spearman rank correlation improves by $\ge 0.05$ over V4 ($r_{\text{V5, bow}} \ge r_{\text{V4, bow}} + 0.05 = 0.2646 + 0.0500 = 0.3146$).
   - For Batters: Out-of-sample Spearman rank correlation does not worsen by more than $0.02$ compared to V4 ($r_{\text{V5, bat}} \ge r_{\text{V4, bat}} - 0.02 = 0.0508 - 0.0200 = 0.0308$).
2. **Gate (b) — Stability & Interval Width Conservation:**
   - The median 90% bootstrap rank-interval width for the Top-10 players under V5 must be **no wider than V4's baseline interval widths**:
     - Batters: $\text{Median Width}_{\text{top10}} \le 37.5$ ranks.
     - Bowlers: $\text{Median Width}_{\text{top10}} \le 38.725$ ranks.
3. **Gate (c) — Elimination of Heuristics:**
   - The model must contain zero hard-coded bonuses, hand-set interpretability scores, or post-hoc weights in the ranking and selection formula.
4. **Gate (d) — Reproducibility & Test Verification:**
   - 100% of unit, statistical, and integration tests pass, and V5 produces bitwise identical SHA-256 ranking hashes on an independent second execution.

### Definitive Decision Branches
- **Decision A (Adopt V5):** All 4 gates pass. V5 becomes the new recommended analytical engine; full 12–16 page report compiled.
- **Decision B (Retain V4 Baseline):** One or more gates fail. V4 remains the official primary submission; a concise 2-page comparative analytical note is generated documenting why V4 was retained.
- **Decision C (Retain V4, Experimental V5):** V5 shows theoretical promise on 2025 but fails confirmation on 2026; retained as an experimental branch.
- **Decision D (Further Work Needed):** Technical failure or deadline breach.

---

## 4. Multiverse Grid & Validation Suite (Part 6)

- **Multiverse Architecture:** Reuses the V4 multiverse design unless a structural improvement is proven under Part 4.
  - Dimension $P$ (Pressure): 5 specifications per role.
  - Dimension $W$ (Wickets baseline): 2 specifications ($W0, W1$).
  - Dimension $F$ (Format scope): 3 specifications ($F1$ All, $F2$ Elite ICC, $F3$ IPL).
  - Dimension $M$ (Models): Model A (504 specs), Model B (504 specs), Model C (1 spec).
  - Total specifications: $30 \times (504 + 1) = 15,150$ specs per role.
  - Total player-specification evaluations: 3,196,444 rows (sum of eligible candidates across all specs; excluding 3,030 bowler P0 reference specs).
- **Validation Protocols:**
  - 1,000 stratified match-cluster bootstrap draws (reporting exact count of valid resamples).
  - Leave-One-Season-Out (LOSO) cross-validation across 2022, 2023, 2024, 2025, 2026.
  - Eligibility gate sensitivity (Lenient vs Standard vs Strict).
  - Wicket valuation sensitivity ($V \in \{4, 6, 8, \text{ctx}\}$).
  - Shrinkage sensitivity ($K \in \{60, 120, 180\}$).
  - Chronological pre-match Elo ratings frozen (zero future information leakage).
  - Clarification: Bootstrap inclusion indicates ranking stability across resampled matches, never future success probability.
- **Outputs:** Stored in `v5_results.xlsx` (Sheets: `rankings`, `bootstrap`, `sensitivities`, `near_misses`).

---

## 5. Player Audit & Rajasthan Royals Recruitment Integration (Part 7)

- **Comprehensive Player Audit:**
  - Detailed diagnostic profiling for all V4 Top-10 players and near-misses: `player_id`, `player_name`, `role`, multiverse %, median rank, bootstrap eligible draws, 90% rank interval, raw HP balls, Kish $N_{\text{eff}}$, shrunk PWI, normal impact, raw lift, consistency score, and format split (IPL vs T20I).
  - Classification into 5 stability tiers: (1) Robust Core, (2) Context-Dependent, (3) Borderline, (4) Small-Sample Sensitive, (5) Pressure-Definition Sensitive.
  - Independent dual-qualification audit for two-way all-rounders (e.g., verifying whether Rashid Khan qualifies independently in both batting and bowling).
- **Rajasthan Royals 2027 Auction Context:**
  - Squad context derived strictly from empirical 2026 RR ball-by-ball records (e.g., death-overs economy rate, middle-overs spin control, lower-order boundary striking).
  - Empirical evaluation of target candidates: Ashutosh Sharma, Naman Dhir, Shashank Singh, Tim David, Mustafizur Rahman, Mohsin Khan, R. Sai Kishore.
  - Auction availability classified strictly as UNVERIFIED unless documented by a dated official franchise/BCCI release in `source_register.md`.
- **Outputs:** Stored in `v5_results.xlsx` (Sheets: `player_profiles`, `rr_matrix`).

---

## 6. Verification & Deliverable Packaging (Part 8)

- **Verification Tests:**
  - Run V1 `validation_tests.py` (immutability of V1 logic).
  - Run `tests/model_v2`, `tests/model_v3`, `tests/model_v4`, and `tests/model_v5` via `pytest`.
  - Verify 39/39 V1 checksums against `outputs/model_v2/integrity_manifest_pre.json`.
  - Verify V4 SHA-256 hashes against `outputs/model_v5/V5_LOG.md`.
  - Player mapping audit: 100% of `player_id` and name pairs checked against `competition_team_player_mapping.csv`.
- **Workbook Deliverable:** `outputs/model_v5/v5_results.xlsx` with exactly 9 sheets:
  1. `data_waterfall`
  2. `pressure_validation`
  3. `model_comparison`
  4. `rankings`
  5. `bootstrap`
  6. `sensitivities`
  7. `near_misses`
  8. `player_profiles`
  9. `rr_matrix`
- **Charts:** Maximum 8 publication-grade charts saved in `outputs/model_v5/charts/`.
- **Report & Document Inspection:**
  - If V5 is adopted: 12–16 page `V5_REPORT.pdf` compiled from `V5_REPORT.md`.
  - If V4 is retained: 2-page comparative technical note.
  - Page image export to PNG and automated scanner to ensure zero unrendered LaTeX tokens (`$`, `\`, `/cdot`, `/times`, `_/`, `**`).

---

## 7. Estimated Runtimes & Milestone Schedule

| Phase | Milestone / Component | Estimated Runtime | Safety Margin | Status |
| :--- | :--- | :--- | :--- | :--- |
| **Part 1** | Inspection, Fingerprinting, and Pre-Registration Plan | 2 minutes | — | **Completed (Awaiting Approval)** |
| **Part 2** | Data Re-Audit & Scope Proof (Waterfall & DLS checks) | 15 seconds | +30s | Scheduled |
| **Part 3** | Pressure Definitions & Outcome Separation Validation | 45 seconds | +60s | Scheduled |
| **Part 4** | Candidate Models (A, B, D, E) & Shrinkage Grid | 120 seconds | +120s | Scheduled |
| **Part 5** | Out-of-Sample Temporal Validation (2025 vs 2026 Gates) | 60 seconds | +60s | Scheduled |
| **Part 6** | Multiverse Pipeline & 1,000 Bootstrap Resamples | 300 seconds | +180s | Scheduled |
| **Part 7** | Player Profiles & Rajasthan Royals Workbook Generation | 30 seconds | +30s | Scheduled |
| **Part 8** | Full Test Suite, SHA-256 Verification & Report Build | 90 seconds | +60s | Scheduled |
| **Total** | **End-to-End Execution Pipeline** | **~11.0 minutes** | **~9.0 minutes** | **Well within 17 Nov Freeze** |

---
*Locked Pre-Registration Protocol: No modeling results have been generated prior to this document.*
