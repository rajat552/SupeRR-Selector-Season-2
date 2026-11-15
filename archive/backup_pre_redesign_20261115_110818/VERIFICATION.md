# VERIFICATION.md — Data & Output Integrity Audit
This document audits and verifies every metric, ranking, bootstrap interval, worked delivery, and player ID used in the SupeRR Selector Season 2 final submission report against the underlying raw data and pipeline output files.

## 1. Automated Player ID Verification (Looked Up from Multiverse Summary Files)
| Player Query | Matched Name in Summary | Role | Report ID | Summary File ID | Verification Status |
| --- | --- | --- | --- | --- | --- |
| Shashank Singh | Shashank Singh | Batter | 2756 | 2756 | MATCH |
| Tim David | Tim David | Batter | 6396 | 6396 | MATCH |
| Naman Dhir | Naman Dhir | Batter | 37052 | 37052 | MATCH |
| Dinesh Karthik | Dinesh Karthik | Batter | 143 | 143 | MATCH |
| Heinrich Klaasen | Heinrich Klaasen | Batter | 4260 | 4260 | MATCH |
| Suryakumar Yadav | Suryakumar Yadav | Batter | 1699 | 1699 | MATCH |
| Rinku Singh | Rinku Singh | Batter | 4708 | 4708 | MATCH |
| Romario Shepherd | Romario Shepherd | Batter | 6726 | 6726 | MATCH |
| Andre Russell | Andre Russell | Batter | 1318 | 1318 | MATCH |
| Rashid Khan | Rashid Khan | Batter | 4722 | 4722 | MATCH |
| Matthew Wade | Matthew Wade | Batter | 796 | 796 | MATCH |
| Ashutosh Sharma | Ashutosh Sharma | Batter | 8101 | 8101 | MATCH |
| Shreyas Iyer | Shreyas Iyer | Batter | 3647 | 3647 | MATCH |
| Mahendra Singh Dhoni | Mahendra Singh Dhoni | Batter | 8 | 8 | MATCH |
| Nicholas Pooran | Nicholas Pooran | Batter | 3125 | 3125 | MATCH |
| Namboori Tilak Varma | Namboori Tilak Varma | Batter | 7897 | 7897 | MATCH |
| Sunil Narine | Sunil Narine | Bowler | 781 | 781 | MATCH |
| Jasprit Bumrah | Jasprit Bumrah | Bowler | 2933 | 2933 | MATCH |
| Rashid Khan | Rashid Khan | Bowler | 4722 | 4722 | MATCH |
| Matheesha Pathirana | Matheesha Pathirana | Bowler | 8661 | 8661 | MATCH |
| Eshan Malinga | Eshan Malinga | Bowler | 39657 | 39657 | MATCH |
| Nathan Ellis | Nathan Ellis | Bowler | 7920 | 7920 | MATCH |
| Noor Ahmad | Noor Ahmad | Bowler | 7967 | 7967 | MATCH |
| Arshdeep Singh | Arshdeep Singh | Bowler | 6464 | 6464 | MATCH |
| Prasidh Krishna | Prasidh Krishna | Bowler | 4489 | 4489 | MATCH |
| Bhuvneshwar Kumar | Bhuvneshwar Kumar | Bowler | 360 | 360 | MATCH |
| Mujeeb Ur Rahman | Mujeeb Ur Rahman | Bowler | 6450 | 6450 | MATCH |
| Naveen ul Haq | Naveen ul Haq | Bowler | 5809 | 5809 | MATCH |
| Krunal Pandya | Krunal Pandya | Bowler | 4219 | 4219 | MATCH |
| Alzarri Joseph | Alzarri Joseph | Bowler | 3275 | 3275 | MATCH |
| Mohammad Nawaz | Mohammad Nawaz | Bowler | 2490 | 2490 | MATCH |
| T Natarajan | T Natarajan | Bowler | 4265 | 4265 | MATCH |
| Ravi Bishnoi | Ravi Bishnoi | Bowler | 7503 | 7503 | MATCH |


## 2. Scope Reconciliation & Delivery Waterfall Audit
Direct empirical verification of delivery counts from `data/raw/matches.csv` and `data/raw/ball_by_ball.csv`:

| Analytical Stage / Scope Step | Matches | Deliveries | Legal Balls | Verification & Accounting Notes |
| :--- | :---: | :---: | :---: | :--- |
| **Total Raw Database Provided** | **883** | **200,999** | **192,445** | Unfiltered repository dump (`matches.csv`, `ball_by_ball.csv`). |
| (-) Abandoned / Zero-Delivery Fixtures | -16 | 0 | 0 | Rain/abandonments with no play; verified 0 balls bowled. |
| (-) Emerging Tournaments (Comp IDs 2670, 3289) | -30 | -6,985 | -6,730 | Secondary tournaments (Mens Emerging Teams Asia Cup, Rising Stars); contains 12 Super Over balls (10 legal). |
| (-) Remaining IPL/T20I Super Overs (Innings 3 & 4) | 0 | -26 | -23 | Tie-breaker overs in primary competitions (out of 38 total raw Super Over deliveries, 33 legal). |
| **FINAL PRIMARY ANALYTICAL SCOPE** | **837** | **193,988** | **185,692** | Exact target scope: 367 IPL + 470 T20I matches (2022–2026). Exact sum: 200,999 - 6,985 - 26 = 193,988. |

*Cricket Accounting Breakdown of Primary Scope (193,988 deliveries):*
- Bowler Legal Deliveries: **185,692** (excludes 7,472 wides and 824 no-balls)
- Batter Balls Faced: **186,516** (excludes 7,472 wides; includes 824 no-balls)
- Extras: 7,472 wides, 824 no-balls (560 overstep, 264 other), 2,683 leg-byes, 514 byes, 1 penalty run


## 3. Master Player Verification Table (Top 10 Batters & Top 10 Bowlers)
| Role | Rank | Player Name | Player ID | Tier | Candidate Elig % | Top-10 % | Top-10 Ret % | Med [IQR] | Canon Score | Shrunk PWI | Raw Lift | HP Balls | Boot Draws | Boot 90% CI | Rises % | Classification | IPL 2026 Team / Status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Batter | 1 | Shashank Singh | 2756 | Tier 1 (Core Consensus) | 100.0% | 94.9% | 94.9% | 5 [3] | 2.89 | +32.2 | +22.2 | 327 | 996/1000 | [1, 44] | 100.0% | Rises under pressure | Punjab Kings |
| Batter | 2 | Tim David | 6396 | Tier 1 (Core Consensus) | 100.0% | 92.1% | 92.1% | 1 [2] | 3.99 | +42.9 | +9.0 | 570 | 1000/1000 | [1, 16] | 78.1% | Rises under pressure | Royal Challengers Bengaluru |
| Batter | 3 | Naman Dhir | 37052 | Tier 1 (Core Consensus) | 91.1% | 88.6% | 97.2% | 4 [5] | 3.44 | +34.7 | +35.4 | 186 | 908/1000 | [1, 32] | 100.0% | Rises under pressure | Mumbai Indians |
| Batter | 4 | Dinesh Karthik | 143 | Tier 2 (Strong Contender) | 100.0% | 78.3% | 78.3% | 5 [7] | 2.75 | +34.4 | +16.1 | 250 | 994/1000 | [1, 44] | 80.0% | Rises under pressure | None (Retired player; RCB Coach) |
| Batter | 5 | Heinrich Klaasen | 4260 | Tier 2 (Strong Contender) | 100.0% | 74.4% | 74.4% | 7 [7] | 2.89 | +24.9 | +3.4 | 459 | 999/1000 | [5, 34] | 80.0% | Rises under pressure | Sunrisers Hyderabad |
| Batter | 6 | Suryakumar Yadav | 1699 | Tier 2 (Strong Contender) | 100.0% | 73.1% | 73.1% | 8 [6] | 1.96 | +25.4 | -4.6 | 657 | 1000/1000 | [6, 44] | 23.3% | Elite all the time | Mumbai Indians |
| Batter | 7 | Rinku Singh | 4708 | Tier 2 (Strong Contender) | 100.0% | 63.1% | 63.1% | 9 [7] | 2.74 | +31.0 | +17.9 | 507 | 1000/1000 | [2, 39] | 80.0% | Rises under pressure | Kolkata Knight Riders |
| Batter | 8 | Romario Shepherd | 6726 | Tier 2 (Strong Contender) | 66.7% | 55.5% | 83.2% | 6 [6] | 3.20 | +28.7 | +5.0 | 431 | 1000/1000 | [2, 36] | 49.1% | Balanced / Context-dependent | Royal Challengers Bengaluru |
| Batter | 9 | Andre Russell | 1318 | Tier 2 (Strong Contender) | 100.0% | 54.2% | 54.2% | 10 [10] | 2.69 | +31.8 | +1.0 | 347 | 1000/1000 | [2, 54] | 17.8% | Elite all the time | KKR (Retired from IPL; KKR Coach) |
| Batter | 10 | Rashid Khan | 4722 | Tier 3 (Context-Dependent) | 77.8% | 47.9% | 61.6% | 8 [9] | 3.02 | +28.1 | +40.3 | 377 | 994/1000 | [1, 40] | 99.3% | Rises under pressure | Gujarat Titans |
| Bowler | 1 | Sunil Narine | 781 | Tier 1 (Core Consensus) | 100.0% | 100.0% | 100.0% | 3 [1] | 3.13 | +6.6 | +0.6 | 422 | 1000/1000 | [1, 17] | 52.5% | Balanced / Context-dependent | Kolkata Knight Riders |
| Bowler | 2 | Jasprit Bumrah | 2933 | Tier 1 (Core Consensus) | 100.0% | 99.2% | 99.2% | 2 [2] | 2.91 | +7.6 | +0.3 | 332 | 999/1000 | [1, 23] | 7.2% | Elite all the time | Mumbai Indians |
| Bowler | 3 | Rashid Khan | 4722 | Tier 1 (Core Consensus) | 100.0% | 93.5% | 93.5% | 5 [4] | 2.86 | +5.6 | +2.7 | 706 | 1000/1000 | [1, 19] | 99.2% | Rises under pressure | Gujarat Titans |
| Bowler | 4 | Matheesha Pathirana | 8661 | Tier 1 (Core Consensus) | 100.0% | 83.4% | 83.4% | 3 [4] | 2.00 | +5.3 | +1.2 | 307 | 1000/1000 | [1, 41] | 22.2% | Elite all the time | KKR (2026 hamstring injury; active rehab) |
| Bowler | 5 | Eshan Malinga | 39657 | Tier 2 (Strong Contender) | 88.9% | 71.9% | 80.9% | 6 [5] | 2.33 | +3.9 | +3.4 | 176 | 912/1000 | [1, 38] | 74.4% | Rises under pressure | Sunrisers Hyderabad |
| Bowler | 6 | Nathan Ellis | 7920 | Tier 2 (Strong Contender) | 75.5% | 54.8% | 72.5% | 7 [6] | 2.36 | +5.5 | +3.1 | 229 | 988/1000 | [1, 36] | 65.9% | Rises under pressure | CSK (Traded to SRH 5 Nov 2026) |
| Bowler | 7 | Noor Ahmad | 7967 | Tier 3 (Context-Dependent) | 100.0% | 40.1% | 40.1% | 12 [11] | 1.10 | +2.5 | -0.2 | 351 | 1000/1000 | [6, 62] | 54.5% | Balanced / Context-dependent | Chennai Super Kings |
| Bowler | 8 | Arshdeep Singh | 6464 | Tier 3 (Context-Dependent) | 100.0% | 35.1% | 35.1% | 12 [7] | 1.46 | +1.9 | +1.0 | 593 | 1000/1000 | [9, 55] | 55.8% | Balanced / Context-dependent | PBKS (Traded to MI 11 Nov 2026) |
| Bowler | 9 | Prasidh Krishna | 4489 | Tier 3 (Context-Dependent) | 100.0% | 31.7% | 31.7% | 13 [8] | 1.13 | +3.0 | +2.7 | 234 | 994/1000 | [5, 63] | 68.3% | Rises under pressure | Gujarat Titans |
| Bowler | 10 | Bhuvneshwar Kumar | 360 | Tier 3 (Context-Dependent) | 100.0% | 27.2% | 27.2% | 17 [18] | 1.24 | +3.3 | -1.3 | 361 | 1000/1000 | [7, 56] | 1.9% | Elite all the time | Royal Challengers Bengaluru |


## 4. Source File Check Matrix & Audit Timestamps
| Metric / Claim | Report Value | Source File | Source Value | Match Status |
| :--- | :--- | :--- | :--- | :---: |
| Pre-Registration Timestamp | 01:56 (Locked Protocol) | `outputs/model_v4/PREREGISTRATION.md` | Created: 2026-11-14 01:56 IST | MATCH |
| Multiverse Results Timestamp | 02:11 (Output Parquet) | `outputs/model_v4/multiverse_ranks.parquet` | Modified: 2026-11-14 02:11 IST | MATCH |
| Specifications Evaluated | 15,150 specs / role | `multiverse_ranks.parquet` | 30 (PxWxF) x 505 specs = 15,150 specs | MATCH |
| Total Evaluation Rows | 3,196,444 evaluations | `multiverse_ranks.parquet` | 3,196,444 rows (incl. 3,030 P0 ref specs) | MATCH |
| Eligible Players per Spec | 32-136 bat, 46-184 bowl | `multiverse_ranks.parquet` | Batters: [32, 136], Bowlers: [46, 184] | MATCH |
| Canonical Batting Out-of-Sample r | 0.05 (p = 0.786) | `outputs/model_v4/walk_forward_rankings.csv` | r = 0.0508, p = 0.7864 | MATCH |
| Canonical Bowling Out-of-Sample r | 0.26 (p = 0.072) | `outputs/model_v4/walk_forward_rankings.csv` | r = 0.2646, p = 0.0721 | MATCH |
| Sigmoid Steepness | k = 12.5 (scale 0.08) | `src/model_v4/pressure_model.py` | scale=0.08 -> 1/0.08 = 12.5 | MATCH |
| Wicket Value Primary Choice | 6.0 runs | `PREREGISTRATION.md` | Fixed 6.0 runs | MATCH |
| Context Marginal Wicket Sensitivity | 7.82 runs | `src/model_v4/opponent_strength.py` | Context table weighted mean: 7.82 runs | MATCH |
| Matthew Wade Exclusion | 720 / 1000 draws (< 800) | `bootstrap_canonical_batters.csv` | valid_eligible_iters = 720 | MATCH |
| Mujeeb Ur Rahman Exclusion | 744 / 1000 draws (< 800) | `bootstrap_canonical_bowlers.csv` | valid_eligible_iters = 744 | MATCH |
| Naveen-ul-Haq Exclusion | 513 / 1000 draws (< 800) | `bootstrap_canonical_bowlers.csv` | valid_eligible_iters = 513 | MATCH |


## 5. Sequential (Type I) ANOVA Variance Decomposition on Percentile Ranks
Percentile ranks ($y_{i,s} = \text{rank}_{i,s} / n_{\text{eligible}, s}$) are evaluated using sequential (Type I) sums of squares. Because percentiles within every specification have mean 0.50 by construction, main effects of specification dimensions sum to under 2%. The sensitivity to modelling choices is captured by the **Player $\times$ Specification Interaction**, which accounts for 21.44% (batting) and 32.79% (bowling) of total rank variance.

*Methodological Note:* Sequential (Type I) decomposition is order-dependent. The `player_id` main effect reflects empirical panel variance attributable to individual player mean percentile ranks, rather than an isolated causal estimate of intrinsic talent. In raw ranks (which vary with specification candidate size $n_{\text{eligible},s}$), the player main effect is 60.17% (batting) and 62.08% (bowling); normalizing to percentile ranks yields 76.58% and 65.73%.

| Dimension / Source of Variance | Batters Sum of Squares | Batters Share (%) | Bowlers Sum of Squares | Bowlers Share (%) |
| :--- | :---: | :---: | :---: | :---: |
| **Player Identifier Main Effect (`player_id`)** | **40,196.12** | **76.58%** | **50,725.94** | **65.73%** |
| Eligibility Gate (`g_gate`) | 426.87 | 0.81% | 357.13 | 0.46% |
| Pressure Definition (`p_def`) | 323.09 | 0.62% | 521.97 | 0.68% |
| Format Scope (`f_scope`) | 262.63 | 0.50% | 240.83 | 0.31% |
| Wickets in Baseline (`w_def`) | 18.13 | 0.03% | 2.12 | 0.00% |
| Wicket Value (`v_val`) | 5.31 | 0.01% | 17.74 | 0.02% |
| Scoring Model Formulation (`m_model`) | 1.76 | 0.00% | 1.26 | 0.00% |
| Shrinkage Strength (`k_shrink`) | 0.99 | 0.00% | 1.12 | 0.00% |
| Metric Component Weights (`s_weights`) | 0.37 | 0.00% | 0.13 | 0.00% |
| **Player $\times$ Specification Interaction** | **11,251.00** | **21.44%** | **25,308.16** | **32.79%** |
| **Total Sum of Squares** | **52,486.26** | **100.00%** | **77,176.40** | **100.00%** |


## 6. Real Deliveries Worked Examples (Computed by Code from `data/raw/ball_by_ball.csv`)
### A. Batting High-Pressure Worked Example
* **Delivery Identifier:** Match ID `14148`, Over `15`, Ball `5` (Ball 15.5; pre-delivery state shown is after 14.4 overs), Innings `2`.
* **Match Context:** IPL 2022, Sunrisers Hyderabad chasing 193 against Royal Challengers Bangalore.
* **Batter:** Shashank Singh (`player_id`: `2756`)
* **Bowler:** Wanindu Hasaranga (`player_id`: `4900`)
* **Pre-Delivery State:**
  * Score: 104/5 in 14.4 overs.
  * Balls Remaining: 32 legal deliveries.
  * Runs Needed: 89 runs.
  * Required Run Rate (RRR): 16.69 runs/over.
  * Continuous Batting Pressure Index: **0.8648**
  * Logistic Weight ($P_2$, center 0.425, scale 0.08, $k=12.5$): $w = \frac{1}{1 + e^{-(0.8648 - 0.425)/0.08}} = \mathbf{0.9959}$
* **Actual Outcome:** Six runs hit off the delivery (`runs`: 6, `is_striker_dismissed`: False, `is_boundary_bat`: True).
* **Leave-Player-Out (LPO) Context Baseline:**
  * Expected Runs: `ctx_bat_rpb` = 1.1087 runs
  * Expected Dismissal: `ctx_bat_out_prob` = 0.0396 dismissals
* **Impact Accounting:**
  * Runs Above Expected: $6 - 1.1087 = +4.8913$ runs.
  * Dismissal Cost Avoidance (at $V=6.0$): $0 - (0.0396 \times 6.0) = -0.2379$ expected dismissal cost avoided ($+0.2379$ net).
  * Net Single-Delivery Batting Value: $\mathbf{+5.1292}$ runs, carrying a pressure weight of $0.9959$ into Shashank's high-pressure ledger.

### B. Bowling High-Pressure Worked Example (DLS Match)
* **Delivery Identifier:** Match ID `40749`, Over `15`, Ball `5` (Ball 15.5; pre-delivery state shown is after 14.4 overs), Innings `2`.
* **Match Context:** IPL 2025, Mumbai Indians vs Gujarat Titans. Rain-affected DLS match: revised target of 147 in 19 overs (114 balls).
* **Bowler:** Jasprit Bumrah (`player_id`: `2933`)
* **Striker:** Shubman Gill (`player_id`: `6288`)
* **Pre-Delivery State:**
  * Score: 113/2 in 14.4 overs.
  * Balls Remaining: 26 legal deliveries.
  * Runs Needed: 34 runs.
  * Required Run Rate (RRR): 7.85 runs/over.
  * Continuous Defending-Side Pressure Index: **0.7958**
  * Logistic Weight ($P_2$, center 0.425, scale 0.08, $k=12.5$): $w = \frac{1}{1 + e^{-(0.7958 - 0.425)/0.08}} = \mathbf{0.9904}$
* **Actual Outcome:** Shubman Gill dismissed **Bowled**, conceding 0 runs (`bowler_runs_conceded`: 0, `is_wicket`: 1, `dismissal_type`: 'Bowled').
* **Leave-Player-Out (LPO) Context Baseline:**
  * Expected Runs Conceded: `ctx_bowl_rpb` = 1.6681 runs
  * Expected Wicket Probability: `ctx_bowl_wkt_prob` = 0.0489 wickets
* **Impact Accounting:**
  * Runs Saved Below Expected: $1.6681 - 0 = +1.6681$ runs saved.
  * Wicket Value Created (at fixed $V=6.0$): $(1 - 0.0489) \times 6.0 = +5.7064$ runs.
  * Net Single-Delivery Bowling Value: $1.6681 + 5.7064 = \mathbf{+7.3745}$ runs created/saved, carrying a pressure weight of $0.9904$ into Bumrah's defending ledger.


## 7. Audited Rajasthan Royals Phase Breakdown (IPL 2026)
Direct empirical phase analysis of Rajasthan Royals' 2026 season from `data/raw`:
- **Death-Overs Bowling (Overs 16–20):**
  - RR Team Death ER: **10.60** vs League Average Death ER **10.67** (RR was approximately league-average in aggregate).
  - Individual Dispersion: Jofra Archer (ER 9.35) and Nandre Burger (ER 9.33) were effective, but Sandeep Sharma conceded ER **13.70** (46 balls) and Tushar Deshpande conceded ER **12.38** (48 balls), driving costly supporting overs.
  - Tactical Need: Targeted death seam options (e.g. Nathan Ellis or Eshan Malinga, if available at auction) to replace expensive individual overs.
- **Middle-Overs Spin (Overs 7–15):**
  - RR Spinners: Ravindra Jadeja ER **8.39**, Tanush Kotian / Punja ER **9.54**, Ravi Bishnoi ER **10.11** (dot ball rate 21.9%).
  - League Average Spin ER in Middle Overs: **8.97**.
  - Identifies a middle-overs spin control gap when Jadeja finishes his spell.
  - Tactical Need: Spin control option (e.g. Noor Ahmad or Rashid Khan, if available at auction).
- **Death-Overs Batting (Overs 16–20):**
  - Donovan Ferreira: SR **221.7** (83 balls) vs League Death Batting SR **169.4**.
  - Supporting Death Batters: Ravindra Jadeja SR **140.5**, Shubham Dubey SR **146.3**, Shimron Hetmyer SR **121.1**.
  - Tactical Need: A second, preferably Indian, death hitter (e.g. Shashank Singh or Naman Dhir, if available at auction) to partner Ferreira.
