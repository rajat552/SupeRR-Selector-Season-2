# SupeRR Selector Season 2 — Official Analytics Deliverable

Data-driven identification and ranking of the **Top 10 Batters** and **Top 10 Bowlers** who perform most reliably under high-pressure T20 match situations across **IPL** and **T20 International (T20I)** cricket (2022–2026), directly informing Rajasthan Royals' auction strategy for IPL 2027.

---

## 1. Project Overview

This repository contains the complete, reproducible, and audited analytical pipeline for **SupeRR Selector Season 2 (Round 1)**. 

- **Official Model:** **V4 Multiverse Model** — The sole official, authoritative analytical framework evaluating 15,150 specifications per player role across a full specification-curve universe.
- **Historical Context:** V1 served as the initial competition baseline; V2 and V3 were intermediate analytical iterations; V5 was an invalid experimental challenger archived outside the active pipeline.
- **Primary Deliverables:** Consolidated in [`outputs/final_package/`](file:///c:/Users/LENOVO/OneDrive/Desktop/SupeRR-Selector-Season-2/outputs/final_package/).

---

## 2. Competition Objective

To evaluate high-pressure performance in T20 cricket (2022–2026) and identify the **Top 10 Batters** and **Top 10 Bowlers** who consistently elevate their impact under pressure, addressing Rajasthan Royals' tactical gaps ahead of the IPL 2027 auction:
1. **Death-Overs Bowling Execution:** Reinforcing depth seam bowling (overs 16–20) where individual volatility hurt RR in 2026.
2. **Middle-Overs Spin Control:** Complementing Ravindra Jadeja with a defensive/wicket-taking spin partner (overs 7–15).
3. **Death-Overs Batting Power:** Providing a second Indian death hitter to partner Donovan Ferreira.

---

## 3. Dataset Structure and Scope

All models operate strictly on the read-only competition data located in [`data/raw/`](file:///c:/Users/LENOVO/OneDrive/Desktop/SupeRR-Selector-Season-2/data/raw/):
- **Core Tables:** `competitions.csv`, `teams.csv`, `matches.csv`, `playing_eleven.csv`, `competition_team_player_mapping.csv`, `ball_by_ball.csv`.
- **Primary Analytical Scope:**
  - Includes: All **IPL** (367 matches) and **T20I** (470 matches) fixtures from 2022 to 2026 (**837 matches**, **193,988 total deliveries**, **185,692 legal deliveries**).
  - Excludes: `Other_T20` (`comp_id` 2670 and 3289 — 30 matches, 6,985 balls), Super Overs (innings 3 & 4 — 38 balls), and 16 abandoned/no-result matches with zero deliveries.
- **Rigorous Cricket Accounting:**
  - Wides: Counted as non-legal deliveries, 0 balls faced for batter, credited as runs conceded to bowler.
  - No-balls (`Overstep` / `other`): Counted as non-legal deliveries for bowler, but credited as ball faced for batter.
  - Byes & Leg-byes: Legal deliveries, excluded from bowler runs conceded.
  - Bowler Wickets: Excludes run-outs, retired out, and obstructing the field.
  - Revised Overs Units: `matches.csv` revised over fields store legal **balls** (e.g., 114.0 = 19 overs), properly parsed.
  - Deduplication: Player identity strictly joins on `player_id` (resolving homonyms like Abdul Samad, Rashid Khan, Haider Ali).

---

## 4. V4 Model Methodology

The V4 framework addresses researcher degrees of freedom by running a **multiverse specification curve analysis** over **15,150 discrete specifications** per role:
- **Zero Look-Ahead Guarantee:** All match states (runs, wickets, balls remaining, CRR, RRR, phase) and opponent Elo ratings are strictly pre-delivery.
- **Continuous Pressure Index:** Continuous logistic weighting functions replace arbitrary discrete cutoffs, ensuring robust effective sample sizes ($N_{\text{eff}}$) via Kish's formula.
- **Leave-Player-Out (LPO) Context Baselines:** Every expected run and wicket baseline subtracts player $i$'s own deliveries from cell $c$, eliminating self-contamination.
- **Empirical Bayes (EB) Shrinkage:** Shrunk towards league-average priors using Beta-Binomial / Normal models to prevent small-sample fluke domination.
- **Stratified Bootstrap:** 1,000 cluster-bootstrap iterations by match to obtain non-parametric 90% confidence intervals.
- **Pre-Registered Selection Rule:** Players must pass eligibility gates, achieve $\ge 800$ valid bootstrap draws, and are ranked by multiverse consensus.

---

## 5. Pressure-Performance Evaluation Approach

Pressure is defined across two distinct tactical dimensions:
1. **Chasing / Defending Pressure (2nd Innings):** Function of balls remaining, runs required, wickets in hand, and required run rate (RRR) vs current run rate (CRR).
2. **Setting Pressure (1st Innings):** Function of phase, projected par score, wickets lost, and over progression.
3. **Continuous Logistic Weighting:**
   $$w_i = \frac{1}{1 + e^{-k (P_i - P_0)}}$$
   Deliveries under extreme pressure receive weights approaching 1.0, while low-leverage situations down-weight towards 0.0.

---

## 6. Batter and Bowler Ranking Methodology

### Official Top 10 Batters
| Rank | Player Name | Player ID | Tier | Multiverse Top-10 Freq | Median Rank [IQR] | Canonical Score | Shrunk PWI | Boot 90% CI | Classification |
|:---:|:---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---|
| 1 | Shashank Singh | 2756 | Core | 99.4% | 1 [1] | 2.89 | +2.0 | [1, 5] | Rises under pressure |
| 2 | Tim David | 6396 | Core | 94.7% | 2 [2] | 3.99 | +1.7 | [1, 7] | Rises under pressure |
| 3 | Naman Dhir | 37052 | Core | 92.1% | 3 [2] | 3.44 | +1.7 | [1, 8] | Rises under pressure |
| 4 | Dinesh Karthik | 143 | Core | 88.5% | 4 [3] | 2.75 | +1.6 | [2, 10] | Rises under pressure |
| 5 | Heinrich Klaasen | 4260 | Core | 84.2% | 5 [3] | 2.89 | +1.5 | [2, 11] | Elite all the time |
| 6 | Suryakumar Yadav | 1699 | Core | 81.0% | 6 [4] | 1.96 | +1.4 | [3, 12] | Elite all the time |
| 7 | Rinku Singh | 4708 | Core | 76.8% | 7 [4] | 2.74 | +1.3 | [3, 14] | Rises under pressure |
| 8 | Romario Shepherd | 6726 | High Potential | 71.3% | 8 [5] | 3.20 | +1.2 | [4, 16] | Rises under pressure |
| 9 | Andre Russell | 1318 | High Potential | 66.7% | 9 [5] | 2.69 | +1.1 | [4, 17] | Elite all the time |
| 10 | Rashid Khan | 4722 | High Potential | 62.4% | 10 [6] | 3.02 | +1.0 | [5, 19] | Rises under pressure |

### Official Top 10 Bowlers
| Rank | Player Name | Player ID | Tier | Multiverse Top-10 Freq | Median Rank [IQR] | Canonical Score | Shrunk PWI | Boot 90% CI | Classification |
|:---:|:---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---|
| 1 | Sunil Narine | 781 | Core | 98.6% | 1 [1] | 3.13 | +2.2 | [1, 4] | Elite all the time |
| 2 | Jasprit Bumrah | 2933 | Core | 96.2% | 2 [1] | 2.91 | +2.0 | [1, 5] | Elite all the time |
| 3 | Rashid Khan | 4722 | Core | 93.8% | 3 [2] | 2.86 | +1.9 | [1, 6] | Elite all the time |
| 4 | Matheesha Pathirana | 8661 | Core | 89.1% | 4 [3] | 2.00 | +1.7 | [2, 9] | Rises under pressure |
| 5 | Eshan Malinga | 39657 | Core | 85.4% | 5 [3] | 2.33 | +1.5 | [2, 10] | Rises under pressure |
| 6 | Nathan Ellis | 7920 | Core | 80.9% | 6 [4] | 2.36 | +1.4 | [3, 12] | Rises under pressure |
| 7 | Noor Ahmad | 7967 | Core | 77.3% | 7 [4] | 1.10 | +1.3 | [3, 14] | Elite all the time |
| 8 | Arshdeep Singh | 6464 | High Potential | 72.5% | 8 [5] | 1.46 | +1.2 | [4, 15] | Rises under pressure |
| 9 | Prasidh Krishna | 4489 | High Potential | 68.0% | 9 [5] | 1.13 | +1.1 | [4, 17] | Context-dependent |
| 10 | Bhuvneshwar Kumar | 360 | High Potential | 63.8% | 10 [6] | 1.24 | +1.0 | [5, 18] | Elite all the time |

---

## 7. Project Architecture

```text
SupeRR-Selector-Season-2/
├── data/
│   └── raw/                          # Read-only competition data (PDF + 6 CSV tables)
├── docs/                             # Competition documentation & governance specifications
│   ├── 00_COMPETITION_OVERVIEW.md    # Challenge brief and evaluation criteria
│   ├── 01_PROBLEM_DEFINITION.md      # Mathematical framing and audit synthesis
│   ├── 02_DATA_DICTIONARY.md         # Schema definitions & variable descriptions
│   └── maintenance/                  # Repository audit & historical records
├── notebooks/                        # Research & exploratory analysis notebooks (01 to 05)
├── outputs/
│   ├── final_package/                # OFFICIAL SUBMISSION DELIVERABLE BUNDLE
│   │   ├── SupeRR_Final_Report.pdf   # Canonical 15-page publication-quality report
│   │   ├── SupeRR_Final_Report.md    # Source Markdown for report
│   │   ├── final_top10_batters.csv   # Authoritative batter ranking CSV
│   │   ├── final_top10_bowlers.csv   # Authoritative bowler ranking CSV
│   │   ├── VERIFICATION.md           # Numerical and player integrity verification
│   │   ├── REQUIREMENTS_MATRIX.md    # Requirements traceability matrix
│   │   ├── source_register.md        # Public external facts register (BCCI/IPL rules)
│   │   ├── PREREGISTRATION.md        # Pre-registered multiverse protocol
│   │   ├── REPRODUCIBILITY.md        # Bitwise reproduction comparison tables
│   │   ├── RUN_LOG.md                # System runtime and command log
│   │   ├── notebooks_executed/       # Executed HTML/PDF notebook exports
│   │   └── data_audit/               # Audited Step 0 raw data profiles & charts
│   ├── data_audit/                   # Step 0 raw data audit profiles & validation files
│   ├── model_v4/                     # V4 multiverse specifications, summaries & charts
│   └── submission_final/             # Report compilation scripts & assets
├── src/
│   ├── run_v4.py                     # Single documented execution entrypoint
│   ├── model_v4/                     # Sole official V4 model package
│   │   ├── __init__.py
│   │   ├── run_multiverse_pipeline.py
│   │   ├── multiverse.py
│   │   ├── impact_models.py
│   │   ├── pressure_model.py
│   │   ├── context_baselines.py
│   │   ├── opponent_strength.py
│   │   ├── cricket_accounting.py
│   │   ├── state_builder.py
│   │   ├── data_loader.py
│   │   ├── eligibility.py
│   │   ├── shrinkage.py
│   │   ├── bootstrap.py
│   │   └── visualization.py
│   └── *.py                          # Audited V1 baseline modules (immutable reference)
├── tests/
│   ├── model_v4/                     # Essential unit & statistical test suite (21 tests)
│   ├── model_v2/                     # Regression tests for V2 components
│   └── model_v3/                     # Regression tests for V3 components
├── archive/                          # Historical material safely preserved outside active flow
│   ├── experimental_v5_invalid/      # Invalidated V5 challenger record
│   └── old_reports/                  # Historical V2 & V3 draft submissions
├── .gitignore                        # Professional repository exclusions
├── AGENTS.md                         # Workspace governance & engineering rules
├── README.md                         # Authoritative project overview & execution guide
└── requirements.txt                  # Pinned dependencies
```

---

## 8. Installation Instructions

The project requires **Python 3.11–3.13**. To set up the virtual environment:

```powershell
# 1. Create and activate virtual environment
python -m venv venv
.\venv\Scripts\Activate.ps1

# 2. Install pinned dependencies
pip install -r requirements.txt
```

---

## 9. Exact Command to Run the Official V4 Pipeline

To execute the official V4 Multiverse Model pipeline end-to-end:

```powershell
python src/run_v4.py
```

*Alternative equivalent command:*
```powershell
python -m src.model_v4.run_multiverse_pipeline
```

---

## 10. Exact Command to Run Tests

To execute the official V4 unit and statistical validation suite (21 tests):

```powershell
pytest tests/model_v4 -q
```

To run the complete test suite across all model versions (54 tests):

```powershell
pytest tests/model_v2 tests/model_v3 tests/model_v4 -q
```

---

## 11. Location of the Final PDF and Ranking CSVs

- **Canonical Final Report (PDF):**
  [`outputs/final_package/SupeRR_Final_Report.pdf`](file:///c:/Users/LENOVO/OneDrive/Desktop/SupeRR-Selector-Season-2/outputs/final_package/SupeRR_Final_Report.pdf)
- **Top 10 Batters (CSV):**
  [`outputs/final_package/final_top10_batters.csv`](file:///c:/Users/LENOVO/OneDrive/Desktop/SupeRR-Selector-Season-2/outputs/final_package/final_top10_batters.csv)
- **Top 10 Bowlers (CSV):**
  [`outputs/final_package/final_top10_bowlers.csv`](file:///c:/Users/LENOVO/OneDrive/Desktop/SupeRR-Selector-Season-2/outputs/final_package/final_top10_bowlers.csv)
- **Report Markdown Source:**
  [`outputs/final_package/SupeRR_Final_Report.md`](file:///c:/Users/LENOVO/OneDrive/Desktop/SupeRR-Selector-Season-2/outputs/final_package/SupeRR_Final_Report.md)

---

## 12. Reproducibility and Verification Instructions

1. **Verify V1 Immutability Manifest (39/39 Checksums):**
   ```powershell
   python -c "from src.model_v4.run_multiverse_pipeline import verify_v1_checksums; print(verify_v1_checksums())"
   ```
   *Expected Output:* `{'checked': 39, 'mismatches': 0}`

2. **Recompile the Final PDF Report:**
   ```powershell
   python outputs/submission_final/compile_final_report.py
   ```

3. **Run the Automated PDF & Player Verification Suite:**
   ```powershell
   python outputs/submission_final/build_verification.py
   ```

4. **Detailed Verification Logs:**
   Refer to [`outputs/final_package/VERIFICATION.md`](file:///c:/Users/LENOVO/OneDrive/Desktop/SupeRR-Selector-Season-2/outputs/final_package/VERIFICATION.md) and [`outputs/final_package/REPRODUCIBILITY.md`](file:///c:/Users/LENOVO/OneDrive/Desktop/SupeRR-Selector-Season-2/outputs/final_package/REPRODUCIBILITY.md) for full delivery-by-delivery worked calculations, ANOVA tables, and audit logs.
