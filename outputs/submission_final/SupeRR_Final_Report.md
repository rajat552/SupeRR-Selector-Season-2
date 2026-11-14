# SupeRR Selector Season 2 — Round 1 Intelligence Submission
## Evaluating Cricket Performance Under Pressure: Multiverse Analysis & Rajasthan Royals Recruitment Strategy
**Byline:** Submission by Rajat Aggarwal | Participant — SupeRR Selector Season 2 (Round 1)  
**Date:** November 2026  
**Analytical Scope:** Primary Historical Universe (837 matches, 193,988 deliveries)  
**Pre-Registration Protocol:** Locked at `outputs/model_v4/PREREGISTRATION.md` (Zero post-hoc deviations)  

---

<!-- PAGE 1 -->
# Page 1: Executive Summary & Dual Top-10 Consensus Lists

### One-Line Pressure Definition
> **A delivery is classified as High-Pressure when the defending-side or batting-side pre-delivery leverage index reaches or exceeds 0.50 (evaluated via logistic sigmoid centered at 0.425 with slope $k = 12.5$ / scale 0.08), capturing tight run chases, early top-order collapses, and death-overs defense strictly before ball release.**

### Pre-Registered Ranking Rule & Multi % Definition
- **Ranking Rule:** Ordered by multiverse top-10 frequency; ties broken by lower median rank; must pass $\ge 50\%$ eligibility across valid specifications and $\ge 800/1000$ bootstrap draws.
- **Metric Clarification:** **Multi %** denotes the share of valid specifications in which the player finishes inside the Top 10 (not a probability of future success).

### Three Core Empirical Findings
1. **Multiverse Specification Sensitivity & Ability Dominance:** Evaluating 15,150 specifications per role (3,196,444 player-specification evaluations) demonstrates that underlying player ability accounts for 76.58% (batting) and 65.73% (bowling) of percentile rank variance. Methodological choices create ranking sensitivity through player $\times$ dimension interactions (21.44% of rank variance for batters, 32.79% for bowlers), which is why reporting consensus frequencies across the multiverse is vastly more reliable than relying on any single specification.
2. **Pre-Registered Bootstrap Filter Removes Volatile Assets:** Applying the 1,000-draw stability hurdle ($\ge 800$ draws) eliminated sample-dependent fringe candidates (Matthew Wade [ID: 796] qualified in only 720/1,000 draws; Mujeeb Ur Rahman [ID: 6450] in 744/1,000; Naveen ul Haq [ID: 5809] in 513/1,000), promoting resilient contributors (Rashid Khan, Noor Ahmad, Prasidh Krishna).
3. **Rajasthan Royals 2026 Phase Audit:** Phase-level auditing from raw data reveals that while RR's death bowling was league-average overall (ER 10.60 vs league 10.67), Sandeep Sharma (ER 13.70) and Tushar Deshpande (ER 12.38) were expensive individuals. In the middle overs, spin economy lagged league par (Jadeja 8.39, Bishnoi 10.11 vs league 8.97). At the death, Donovan Ferreira (SR 221.7) lacked an explosive second death hitter (Hetmyer SR 121.1). The consensus targets offer direct tactical options, if available at auction.

### Table 1A: Consensus Top-10 Batters
*Ranked by Multiverse Frequency, Shrunk High-Pressure Impact & Lift under Pre-Registered Decision Rule.*

| Rank | Player Name | Player ID | Tier | Multiverse Top-10 % | Median Rank [IQR] | Canon Score | Shrunk PWI | Raw Lift | HP Balls | Boot Draws | Participant Recommendation |
| :---: | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **1** | Shashank Singh | 2756 | Tier 1 | 94.9% | 5.0 [3.0] | 2.89 | +32.2 | +22.2 | 327 | 996 / 1000 | Priority if available |
| **2** | Tim David | 6396 | Tier 1 | 92.1% | 1.0 [2.0] | 3.99 | +42.9 | +9.0 | 570 | 1000 / 1000 | Watchlist |
| **3** | Naman Dhir | 37052 | Tier 1 | 88.6% | 4.0 [5.0] | 3.44 | +34.7 | +35.4 | 186 | 908 / 1000 | Priority if available |
| **4** | Dinesh Karthik | 143 | Tier 2 | 78.3% | 5.0 [7.0] | 2.75 | +34.4 | +16.1 | 250 | 994 / 1000 | Historical benchmark – retired player; RCB Coach |
| **5** | Heinrich Klaasen | 4260 | Tier 2 | 74.4% | 7.0 [7.0] | 2.89 | +24.9 | +3.4 | 459 | 999 / 1000 | Watchlist |
| **6** | Suryakumar Yadav | 1699 | Tier 2 | 73.1% | 8.0 [6.0] | 1.96 | +25.4 | -4.6 | 657 | 1000 / 1000 | Watchlist |
| **7** | Rinku Singh | 4708 | Tier 2 | 63.1% | 9.0 [7.0] | 2.74 | +31.0 | +17.9 | 507 | 1000 / 1000 | Priority if available |
| **8** | Romario Shepherd | 6726 | Tier 2 | 55.5% | 6.0 [6.0] | 3.20 | +28.7 | +5.0 | 431 | 1000 / 1000 | Watchlist |
| **9** | Andre Russell | 1318 | Tier 2 | 54.2% | 10.0 [10.0] | 2.69 | +31.8 | +1.0 | 347 | 1000 / 1000 | Historical benchmark – retired from IPL; KKR Coach |
| **10** | Rashid Khan | 4722 | Tier 3 | 47.9% | 8.0 [9.0] | 3.02 | +28.1 | +40.3 | 377 | 994 / 1000 | Priority if available |

### Table 1B: Consensus Top-10 Bowlers
*Ranked by Multiverse Frequency, Defending Shrunk Impact & Lift under Pre-Registered Decision Rule.*

| Rank | Player Name | Player ID | Tier | Multiverse Top-10 % | Median Rank [IQR] | Canon Score | Shrunk PWI | Raw Lift | HP Balls | Boot Draws | Participant Recommendation |
| :---: | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **1** | Sunil Narine | 781 | Tier 1 | 100.0% | 3.0 [1.0] | 3.13 | +6.57 | +0.64 | 422 | 1000 / 1000 | Watchlist |
| **2** | Jasprit Bumrah | 2933 | Tier 1 | 99.2% | 2.0 [2.0] | 2.91 | +7.61 | +0.33 | 332 | 999 / 1000 | Watchlist |
| **3** | Rashid Khan | 4722 | Tier 1 | 93.5% | 5.0 [4.0] | 2.86 | +5.59 | +2.75 | 706 | 1000 / 1000 | Priority if available |
| **4** | Matheesha Pathirana | 8661 | Tier 1 | 83.4% | 3.0 [4.0] | 2.00 | +5.34 | +1.21 | 307 | 1000 / 1000 | Watchlist |
| **5** | Eshan Malinga | 39657 | Tier 2 | 71.9% | 6.0 [5.0] | 2.33 | +3.85 | +3.39 | 176 | 912 / 1000 | Priority if available |
| **6** | Nathan Ellis | 7920 | Tier 2 | 54.8% | 7.0 [6.0] | 2.36 | +5.50 | +3.15 | 229 | 988 / 1000 | Priority if available (traded CSK -> SRH) |
| **7** | Noor Ahmad | 7967 | Tier 3 | 40.1% | 12.0 [11.0] | 1.10 | +2.54 | -0.21 | 351 | 1000 / 1000 | Priority if available |
| **8** | Arshdeep Singh | 6464 | Tier 3 | 35.1% | 12.0 [7.0] | 1.46 | +1.90 | +0.99 | 593 | 1000 / 1000 | Watchlist (traded PBKS -> MI) |
| **9** | Prasidh Krishna | 4489 | Tier 3 | 31.7% | 13.0 [8.0] | 1.13 | +2.96 | +2.67 | 234 | 994 / 1000 | Watchlist |
| **10** | Bhuvneshwar Kumar | 360 | Tier 3 | 27.2% | 17.0 [18.0] | 1.24 | +3.25 | -1.31 | 361 | 1000 / 1000 | Watchlist |

---

<!-- PAGE 2 -->
# Page 2: Problem Understanding, Scope & Cricket Accounting

### 1. Problem Framing & Operational Mandate
In T20 cricket analytics, evaluating players on aggregate averages or raw boundary counts introduces severe survival bias. An uncontested boundary struck during a blowout cannot be equated with a boundary struck when requiring 12 runs off 4 balls against disciplined execution. My mandate in Round 1 of SupeRR Selector Season 2 is to construct a leakage-safe, empirically grounded ranking of players by performance in high-pressure situations *compared with their usual performance*, while directly addressing Rajasthan Royals' tactical needs for the IPL 2027 auction.

To eliminate post-hoc narrative fitting, I conducted a full multiverse (specification-curve) analysis governed by an immutable pre-registration protocol (`outputs/model_v4/PREREGISTRATION.md`). Evaluating 15,150 specifications per role (3,196,444 evaluations) across eight orthogonal dimensions prevents arbitrary cutoffs from driving outcomes. Statistical rankings derive strictly from match data, while external franchise facts are maintained as practical availability context.

### 2. Historical Data Scope & Strict Cricket Accounting
The primary analytical universe spans January 2022 to November 2026. Following strict competition criteria, I excluded secondary representative tournaments (comp IDs 2670 and 3289: 30 matches, 6,985 deliveries, which include 12 Super Over balls), the remaining 26 Super Over deliveries in IPL/T20I fixtures (out of 38 total raw Super Over deliveries across all competitions), and 16 abandoned matches with zero deliveries bowled:
$$\text{Primary Scope Deliveries} = 200{,}999 - 6{,}985 - 26 = 193{,}988 \text{ deliveries}$$
The primary audit universe contains exactly **837 matches** (367 IPL, 470 T20I), **193,988 deliveries**, and **185,692 legal balls** (7,472 wides, 824 no-balls; 186,516 batter balls faced).

Rigorous cricket accounting was implemented at the delivery level:
- **Player Identity Disambiguation:** Joins and aggregations are keyed strictly on unique integer `player_id`. Name-string joins were strictly prohibited to resolve homonyms in raw data (e.g., Abdul Samad IDs 7446 vs 6922; Rashid Khan IDs 4722 vs 20172).
- **Fair Bowling & Extras Accounting:** Bowler runs conceded strictly exclude byes and leg-byes. Non-legal deliveries (wides, oversteps, and other no-balls) are credited to batting extras while charging bowler runs conceded. Wides are non-legal and do not increment batter balls faced. Oversteps and other no-balls increment batter balls faced.
- **Wicket Attribution:** Bowler wickets strictly exclude run outs, retired out, and obstructing the field (normalizing raw typos such as 'Obstracting the field').
- **Revised Overs Unit:** In rain-affected matches, columns `first_inn_revised_overs` and `second_inn_revised_overs` in `matches.csv` record balls (e.g., 114.0 balls = 19.0 overs), not decimal overs.

---

<!-- PAGE 3 -->
# Page 3: Situational Mechanics & Worked Real Deliveries

### 3. Batter-Side vs. Defending Bowler Pressure Formulations
Pressure is asymmetric between batting and bowling. In a run chase where the batting team is 70/8 needing 110 runs from 30 balls, the batting team faces extreme collapse pressure, but the defending team is in commanding control and faces near-zero pressure. A single unified pressure index conflates these dynamics.

- **Batting Pressure Formulation:**
  In innings 1, pressure reflects top-order collapse and resource loss:
  PI_{{bat}, 1} = 0.50 S_{{collapse}} + 0.30 S_{{crr}} + 0.20 S_{{death}}
  In innings 2, chase urgency and boundary deficits govern leverage:
  PI_{{bat}, 2} = 0.50 S_{{rrr}} + 0.30 S_{{wkts}} + 0.20 S_{{urgency}} + {boost}_{{close}}
  Continuous weights use a logistic sigmoid centered at $x_0 = 0.425$ with slope $k = 12.5$ (scale $s = 0.08$):
  w_k = {1}{1 + e^{-12.5(PI_k - 0.425)}} = {1}{1 + e^{-(PI_k - 0.425)/0.08}}
- **Defending Bowler Formulation:**
  In innings 1, pressure evaluates opponent onslaughts (CRR > par with $\le 3$ wickets down) and death overs (16–20 with $\le 5$ wickets down), with a collapse damper when opponents lose $\ge 6$ wickets. In innings 2, leverage peaks during balanced chases (RRR ratio 0.7–1.5 with chasing side having $\ge 4$ wickets in hand); when the chasing side loses $\ge 7$ wickets, tail-damping reduces leverage to 0.20.

### Real Deliveries Worked Examples (from `data/raw/ball_by_ball.csv`)
1. **Batting High Pressure (Match ID 14148, IPL 2022, Innings 2, Over 15, Ball 5 [Ball 15.5; state shown is after 14.4 overs]):**
   - *Context:* Chasing target 193; match score 104/5 in 14.4 overs; 32 legal balls remaining; 89 runs required ($RRR = 16.69$).
   - *Batter:* Shashank Singh (`player_id`: 2756) | *Bowler:* Wanindu Hasaranga (`player_id`: 4900).
   - *Continuous Leverage:* $PI_{{bat}} = 0.8648$. Sigmoid weight: $w = {1}{1 + e^{-(0.8648 - 0.425)/0.08}} = {0.9959}$.
   - *Outcome:* Six runs struck off the delivery (`runs`: 6, `is_striker_dismissed`: False, `is_boundary_bat`: True).
   - *LPO Baseline:* `ctx_bat_rpb` = 1.1087 runs; `ctx_bat_out_prob` = 0.0396 dismissals.
   - *Impact Accounting:* Runs above expected $= 6 - 1.1087 = +4.8913$. Dismissal cost avoidance ($V=6.0$): $0 - (0.0396 \times 6.0) = +0.2379$. Net single-delivery value: ${+5.1292}$ runs, carrying a pressure weight of $0.9959$.
2. **Defending Bowler High Pressure (Match ID 40749, IPL 2025, Innings 2, Over 15, Ball 5 [Ball 15.5; state shown is after 14.4 overs]):**
   - *Context:* Rain-affected DLS match with a revised target of 147 in 19 overs (114 balls). Match score 113/2 in 14.4 overs; 26 balls remaining; 34 runs required ($RRR = 7.85$).
   - *Bowler:* Jasprit Bumrah (`player_id`: 2933) | *Striker:* Shubman Gill (`player_id`: 6288).
   - *Continuous Defending Leverage:* $PI_{{bowl}} = 0.7958$. Sigmoid weight: $w = {0.9904}$.
   - *Outcome:* Shubman Gill dismissed **Bowled**, conceding 0 runs (`bowler_runs_conceded`: 0, `is_wicket`: 1, `dismissal_type`: 'Bowled').
   - *LPO Baseline:* `ctx_bowl_rpb` = 1.6681 runs; `ctx_bowl_wkt_prob` = 0.0489 wickets.
   - *Impact Accounting:* Runs saved below expected $= 1.6681 - 0 = +1.6681$. Wicket value ($V=6.0$): $(1 - 0.0489) \times 6.0 = +5.7064$. Net delivery value: ${+7.3745}$ runs, carrying a pressure weight of $0.9904$.

---

<!-- PAGE 4 -->
# Page 4: Performance Measurement, Baselines & Shrinkage

### 4. Leave-Player-Out (LPO) Hierarchical Baselines
To measure performance above expectation fairly, every delivery must be compared against a context-specific baseline. Using unadjusted aggregate averages conflates player skill with usage patterns. I implemented a leakage-safe **Leave-Player-Out (LPO) Hierarchical Context Baseline** where player $i$'s own deliveries are subtracted from cell $c$:
\hat{\mu}_{-i, c} = {\sum_{j \ne i, j \in c} y_j}{\sum_{j \ne i, j \in c} n_j}
When cell sample size after subtracting player $i$ falls below 50, the baseline backs up the hierarchy (from format $\times$ season $\times$ phase $\times$ wickets bucket $\times$ opposition tier, to phase and format levels).

### 5. Wicket Valuation & Empirical Bayes Regularization
- **Wicket Value:** Wicket value is set to **6.0 runs** as a fixed analytical choice, avoiding double-counting the runs conceded on delivery $k$. The context-marginal empirical estimate (**7.82 runs**) is evaluated as a sensitivity variant across the multiverse.
- **Empirical Bayes Shrinkage:** High-pressure sample sizes vary. I apply Empirical Bayes shrinkage toward zero based on Kish's effective sample size $N_{{eff}} = (\sum w_k)^2 / \sum w_k^2$:
{PWI}_{{shrunk}} = {N_{{eff}}}{N_{{eff}} + K} \cdot {PWI}_{{raw}} \quad (K = 120)

### 6. Scoring Models & Comparison with Usual Performance
- **Model Choice:** On empirical predictive criteria, Model A (absolute high-pressure output) is slightly ahead of Model B for batters. However, Model B is selected as the primary scoring framework because the competition brief explicitly requires ranking players by performance in high-pressure situations *compared with their usual performance*:
{Score}_{{Model B}} = 0.50 \cdot z({PWI}_{{shrunk}}) + 0.30 \cdot z({MaintLift}_{{shrunk}}) + 0.20 \cdot z({Consistency}_{{EB}})
where ${MaintLift} = {PWI}_{{shrunk}} - 0.35 \cdot \max({Normal}_{{shrunk}}, {floor})$. This balances absolute ability with baseline resilience.

---

<!-- PAGE 5 -->
# Page 5: Fair Comparisons, Eligibility & Multiverse Architecture

### 7. Governance Layers for Fair Comparisons
- **Multi-Tier Eligibility Gates:** Lenient ($\ge 200$ balls, $\ge 80$ HP balls, $\ge 8$ HP matches); Standard Benchmark ($\ge 300$ balls, $\ge 120$ HP balls, $\ge 10$ HP matches); Strict ($\ge 400$ balls, $\ge 150$ HP balls, $\ge 12$ HP matches). In the multiverse selection rule, a candidate must qualify in $\ge 50\%$ of valid specifications.
- **Format Scope Governance:** Evaluates three tracks: (F1) IPL + All T20I, (F2) IPL + Full-Member T20I, and (F3) IPL Only.
- **Cluster-Robust Match Sampling:** Deliveries within the same match share conditions; variance estimation and bootstrap draws are clustered at the match level.

### 8. Specification Grid Architecture
The multiverse evaluates **15,150 specifications per role** (3,196,444 player-specification evaluations across both roles):
{Total Specifications} = 30\,(P \times W \times F) \times [504\,({Model A/B specs}) + 1\,({Model C spec})] = 15,150
The 3,196,444 evaluation rows sum the eligible players evaluated in each specification (32–136 batters, 46–184 bowlers), including 3,030 bowler P0 reference specifications that are retained for audit diagnostics but excluded from candidate selection.

- **P (Pressure Definition):** P1 (sigmoid center 0.40), P2 (0.425), P3 (0.45), P4 (discrete $PI \ge 0.50$ vs $< 0.35$), P5 (Definition C collapse/chase criteria).
- **W (Wickets in Baseline):** W0 (no wicket conditioning), W1 (wickets buckets 0–2, 3–5, 6+).
- **M (Scoring Model):** Model A (absolute), Model B (maintenance & lift), Model C (interaction ridge regression).
- **V (Wicket Value):** 4.0, 6.0 (fixed choice), 8.0, and context-marginal (7.82 runs).
- **K (Shrinkage Strength):** $K = 60, 120, 180$.
- **F (Format Scope):** F1 (all), F2 (full member), F3 (IPL only).
- **G (Eligibility Gate):** Lenient, standard, strict.
- **S (Metric Weights):** Base $(0.50, 0.30, 0.20)$ plus 6 local perturbations.

---

<!-- PAGE 6 -->
# Page 6: Multiverse Specification Curve & Variance Decomposition

### 9. Specification Curves & Robustness Analysis
Evaluating 15,150 specifications confirms that top-ranked players consistently appear across specifications. The specification curves display ordered player median ranks alongside IQR intervals.

![Batting Specification Curves](file:///c:/Users/LENOVO/OneDrive/Desktop/SupeRR-Selector-Season-2/outputs/model_v4/charts/multiverse_spec_curves_batter.png)

### 10. Sequential (Type I) ANOVA on Percentile Ranks
Percentile ranks ($y_{i,s} = {rank}_{i,s} / n_{{eligible}, s}$) are evaluated using sequential (Type I) sums of squares summing to exactly 100.00%. Because percentiles within every specification have mean 0.50 by construction, main effects of specification dimensions sum to under 2%. Methodological sensitivity is captured by the **Player $\times$ Specification Interaction**, which accounts for 21.44% (batting) and 32.79% (bowling) of total rank variance. Note: In raw ranks (which vary with specification candidate size $n_{\text{eligible},s}$), the player main effect is 60.17% (batting) and 62.08% (bowling); normalizing to percentile ranks yields 76.58% and 65.73%.

| Dimension / Source of Variance | Batters Sum of Squares | Batters Share (%) | Bowlers Sum of Squares | Bowlers Share (%) | Interpretation |
| :--- | :---: | :---: | :---: | :---: | :--- |
| **Player Identifier Main Effect (`player_id`)** | **40,196.12** | **76.58%** | **50,725.94** | **65.73%** | **Empirical panel variance attributable to individual player mean ranks (non-causal).** |
| Eligibility Gate (`g_gate`) | 426.87 | 0.81% | 357.13 | 0.46% | Volume thresholds shift qualification of specialist finishers. |
| Pressure Definition (`p_def`) | 323.09 | 0.62% | 521.97 | 0.68% | Continuous sigmoids vs discrete cuts vs Def C reorder borderline players. |
| Format Scope (`f_scope`) | 262.63 | 0.50% | 240.83 | 0.31% | Domestic IPL vs international depth shifts player sample volumes. |
| Wickets in Baseline (`w_def`) | 18.13 | 0.03% | 2.12 | 0.00% | Conditioning match state baselines on wickets in hand. |
| Wicket Value (`v_val`) | 5.31 | 0.01% | 17.74 | 0.02% | Fixed 4.0/6.0/8.0 vs context-marginal 7.82 runs valuation. |
| Scoring Model Formulation (`m_model`) | 1.76 | 0.00% | 1.26 | 0.00% | Model A (absolute) vs Model B (lift) formulation shift. |
| Shrinkage Strength (`k_shrink`) | 0.99 | 0.00% | 1.12 | 0.00% | Regularization penalty strength ($K=60, 120, 180$). |
| Metric Component Weights (`s_weights`) | 0.37 | 0.00% | 0.13 | 0.00% | Local perturbations of run/wicket/boundary weights. |
| **Player $\times$ Specification Interaction** | **11,251.00** | **21.44%** | **25,308.16** | **32.79%** | **Measures individual player sensitivity across specifications.** |
| **Total Sum of Squares** | **52,486.26** | **100.00%** | **77,176.40** | **100.00%** | **Sequential decomposition sums to exactly 100.00%.** |

---

<!-- PAGE 7 -->
# Page 7: Top 10 Batters — Profiles (Ranks 1 to 5)

### Table 2A: Full Top-10 Batters Performance Matrix
| Rank | Player Name (ID) | Tier | Shrunk PWI | Normal | Raw Lift | Maint Lift | HP Balls | Multi % | Med [IQR] | Boot 90% CI | Rises % | Classification |
| :---: | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :--- |
| 1 | Shashank Singh (2756) | Tier 1 | +32.2 | +10.0 | +22.2 | +28.7 | 327 | 94.9% | 5.0 [3.0] | [1, 44] | 100.0% | Rises under pressure |
| 2 | Tim David (6396) | Tier 1 | +42.9 | +33.9 | +9.0 | +31.0 | 570 | 92.1% | 1.0 [2.0] | [1, 16] | 78.1% | Rises under pressure |
| 3 | Naman Dhir (37052) | Tier 1 | +34.7 | -0.7 | +35.4 | +35.0 | 186 | 88.6% | 4.0 [5.0] | [1, 32] | 100.0% | Rises under pressure |
| 4 | Dinesh Karthik (143) | Tier 2 | +34.4 | +18.3 | +16.1 | +28.0 | 250 | 78.3% | 5.0 [7.0] | [1, 44] | 80.0% | Rises under pressure |
| 5 | Heinrich Klaasen (4260) | Tier 2 | +24.9 | +21.5 | +3.4 | +17.4 | 459 | 74.4% | 7.0 [7.0] | [5, 34] | 80.0% | Rises under pressure |
| 6 | Suryakumar Yadav (1699) | Tier 2 | +25.4 | +30.0 | -4.6 | +14.9 | 657 | 73.1% | 8.0 [6.0] | [6, 44] | 23.3% | Elite all the time |
| 7 | Rinku Singh (4708) | Tier 2 | +31.0 | +13.1 | +17.9 | +26.4 | 507 | 63.1% | 9.0 [7.0] | [2, 39] | 80.0% | Rises under pressure |
| 8 | Romario Shepherd (6726) | Tier 2 | +28.7 | +23.7 | +5.0 | +20.4 | 431 | 55.5% | 6.0 [6.0] | [2, 36] | 49.1% | Balanced / Context-dep |
| 9 | Andre Russell (1318) | Tier 2 | +31.8 | +30.9 | +1.0 | +21.0 | 347 | 54.2% | 10.0 [10.0] | [2, 54] | 17.8% | Elite all the time |
| 10 | Rashid Khan (4722) | Tier 3 | +28.1 | -12.2 | +40.3 | +32.3 | 377 | 47.9% | 8.0 [9.0] | [1, 40] | 99.3% | Rises under pressure |

### Detailed Profiles (Ranks 1 to 5)
1. **Shashank Singh (`player_id`: 2756) — Tier 1 | Classification: Rises under pressure**
   - *Metrics:* Multiverse Top-10: 94.9%, Median Rank 5.0 [IQR 3.0], Shrunk PWI: +32.2 runs/100b, Raw Lift: +22.2 runs/100b, HP Balls: 327.
   - *Bootstrap Stability:* 996 / 1,000 eligible draws; 90% rank interval [1, 44].
   - *Resilience:* Rises under pressure in 100.0% of specifications.
   - *IPL 2026 Team (Raw Data):* Punjab Kings. Availability for IPL 2027: UNVERIFIED.
   - *Rajasthan Royals Tactical Fit:* Strong target, if available at auction, to partner Donovan Ferreira in death-overs hitting.
2. **Tim David (`player_id`: 6396) — Tier 1 | Classification: Rises under pressure**
   - *Metrics:* Multiverse Top-10: 92.1%, Median Rank 1.0 [IQR 2.0], Shrunk PWI: +42.9 runs/100b, Raw Lift: +9.0 runs/100b, HP Balls: 570.
   - *Bootstrap Stability:* 1,000 / 1,000 eligible draws; 90% rank interval [1, 16].
   - *Resilience:* Rises under pressure in 78.1% of specifications.
   - *IPL 2026 Team (Raw Data):* Royal Challengers Bengaluru. Availability for IPL 2027: UNVERIFIED.
   - *Rajasthan Royals Tactical Fit:* High-impact boundary asset, if available at auction, to provide overseas death-overs boundary power.
3. **Naman Dhir (`player_id`: 37052) — Tier 1 | Classification: Rises under pressure**
   - *Metrics:* Multiverse Top-10: 88.6%, Median Rank 4.0 [IQR 5.0], Shrunk PWI: +34.7 runs/100b, Raw Lift: +35.4 runs/100b, HP Balls: 186.
   - *Bootstrap Stability:* 908 / 1,000 eligible draws; 90% rank interval [1, 32].
   - *Resilience:* Rises under pressure in 100.0% of specifications.
   - *IPL 2026 Team (Raw Data):* Mumbai Indians. Availability for IPL 2027: UNVERIFIED.
   - *Rajasthan Royals Tactical Fit:* High-lift Indian middle-order option, if available at auction, providing versatile acceleration.
4. **Dinesh Karthik (`player_id`: 143) — Tier 2 | Classification: Rises under pressure**
   - *Metrics:* Candidate Eligibility: 100.0%, Multiverse Top-10: 78.3%, Median Rank 5.0 [IQR 7.0], Shrunk PWI: +34.4 runs/100b, Raw Lift: +16.1 runs/100b, HP Balls: 250.
   - *Bootstrap Stability:* 994 / 1,000 eligible draws; 90% rank interval [1, 44].
   - *Resilience:* Rises under pressure in 80.0% of specifications.
   - *Status:* Historical benchmark — retired from active IPL play after the 2024 season; active Royal Challengers Bengaluru Batting Coach & Mentor (2025–2026).
   - *Rajasthan Royals Tactical Fit:* Retained as an empirical performance benchmark rather than an actionable recruitment target.
5. **Heinrich Klaasen (`player_id`: 4260) — Tier 2 | Classification: Rises under pressure**
   - *Metrics:* Multiverse Top-10: 74.4%, Median Rank 7.0 [IQR 7.0], Shrunk PWI: +24.9 runs/100b, Raw Lift: +3.4 runs/100b, HP Balls: 459.
   - *Bootstrap Stability:* 999 / 1,000 eligible draws; 90% rank interval [5, 34].
   - *Resilience:* Rises under pressure in 80.0% of specifications.
   - *IPL 2026 Team (Raw Data):* Sunrisers Hyderabad. Availability for IPL 2027: UNVERIFIED.
   - *Rajasthan Royals Tactical Fit:* Premier middle-overs boundary engine, if available at auction, maintaining high baseline output.

---

<!-- PAGE 8 -->
# Page 8: Top 10 Batters — Profiles (Ranks 6 to 10) & Landscape

### Detailed Profiles (Ranks 6 to 10)
6. **Suryakumar Yadav (`player_id`: 1699) — Tier 2 | Classification: Elite all the time**
   - *Metrics:* Multiverse Top-10: 73.1%, Median Rank 8.0 [IQR 6.0], Shrunk PWI: +25.4 runs/100b, Raw Lift: -4.6 runs/100b, HP Balls: 657.
   - *Bootstrap Stability:* 1,000 / 1,000 eligible draws; 90% rank interval [6, 44].
   - *Resilience:* Rises under pressure in 23.3% of specifications (reflecting an already elite normal baseline of +30.0 runs/100b).
   - *IPL 2026 Team (Raw Data):* Mumbai Indians. Availability for IPL 2027: UNVERIFIED.
   - *Rajasthan Royals Tactical Fit:* Dominant middle-overs boundary creator, if available at auction, whose high output holds against defensive fields.
7. **Rinku Singh (`player_id`: 4708) — Tier 2 | Classification: Rises under pressure**
   - *Metrics:* Multiverse Top-10: 63.1%, Median Rank 9.0 [IQR 7.0], Shrunk PWI: +31.0 runs/100b, Raw Lift: +17.9 runs/100b, HP Balls: 507.
   - *Bootstrap Stability:* 1,000 / 1,000 eligible draws; 90% rank interval [2, 39].
   - *Resilience:* Rises under pressure in 80.0% of specifications.
   - *IPL 2026 Team (Raw Data):* Kolkata Knight Riders. Availability for IPL 2027: UNVERIFIED.
   - *Rajasthan Royals Tactical Fit:* High-performing left-handed chase finisher, if available at auction, with consistent execution.
8. **Romario Shepherd (`player_id`: 6726) — Tier 2 | Classification: Balanced / Context-dependent**
   - *Metrics:* Multiverse Top-10: 55.5%, Median Rank 6.0 [IQR 6.0], Shrunk PWI: +28.7 runs/100b, Raw Lift: +5.0 runs/100b, HP Balls: 431.
   - *Bootstrap Stability:* 1,000 / 1,000 eligible draws; 90% rank interval [2, 36].
   - *Resilience:* Rises under pressure in 49.1% of specifications.
   - *IPL 2026 Team (Raw Data):* Royal Challengers Bengaluru. Availability for IPL 2027: UNVERIFIED.
   - *Rajasthan Royals Tactical Fit:* Explosive lower-order hitter, if available at auction, adding depth to death-overs batting.
9. **Andre Russell (`player_id`: 1318) — Tier 2 | Classification: Elite all the time**
   - *Metrics:* Candidate Eligibility: 100.0%, Multiverse Top-10: 54.2%, Median Rank 10.0 [IQR 10.0], Shrunk PWI: +31.8 runs/100b, Raw Lift: +1.0 runs/100b, HP Balls: 347.
   - *Bootstrap Stability:* 1,000 / 1,000 eligible draws; 90% rank interval [2, 54].
   - *Resilience:* Elite across all match states in 82.2% of specifications (normal baseline +30.9 runs/100b).
   - *Status:* Historical benchmark — retired from IPL on 30 Nov 2025; active Kolkata Knight Riders Power Coach for IPL 2026 while continuing in select non-IPL leagues.
   - *Rajasthan Royals Tactical Fit:* Prime baseline for elite late-innings power-hitting.
10. **Rashid Khan (`player_id`: 4722) — Tier 3 | Classification: Rises under pressure**
    - *Metrics:* Multiverse Top-10: 47.9%, Median Rank 8.0 [IQR 9.0], Shrunk PWI: +28.1 runs/100b, Raw Lift: +40.3 runs/100b, HP Balls: 377.
    - *Bootstrap Stability:* 994 / 1,000 eligible draws; 90% rank interval [1, 40].
    - *Resilience:* Rises under pressure in 99.3% of specifications (elevating from normal baseline of -12.2 to +28.1 runs/100b).
    - *IPL 2026 Team (Raw Data):* Gujarat Titans. Availability for IPL 2027: UNVERIFIED.
    - *Rajasthan Royals Tactical Fit:* Dual-threat asset, if available at auction, providing lower-order batting lift alongside frontline bowling.

![Batting Maintenance vs Lift](file:///c:/Users/LENOVO/OneDrive/Desktop/SupeRR-Selector-Season-2/outputs/model_v4/charts/fig2_maintenance_vs_lift_batters.png)

---

<!-- PAGE 9 -->
# Page 9: Top 10 Bowlers — Profiles (Ranks 1 to 5)

### Table 2B: Full Top-10 Bowlers Performance Matrix
| Rank | Player Name (ID) | Tier | Shrunk PWI | Normal | Raw Lift | Maint Lift | HP Balls | Multi % | Med [IQR] | Boot 90% CI | Rises % | Classification |
| :---: | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :--- |
| 1 | Sunil Narine (781) | Tier 1 | +6.57 | +5.93 | +0.64 | +4.50 | 422 | 100.0% | 3.0 [1.0] | [1, 17] | 52.5% | Balanced / Context-dep |
| 2 | Jasprit Bumrah (2933) | Tier 1 | +7.61 | +7.28 | +0.33 | +5.06 | 332 | 99.2% | 2.0 [2.0] | [1, 23] | 7.2% | Elite all the time |
| 3 | Rashid Khan (4722) | Tier 1 | +5.59 | +2.84 | +2.75 | +4.60 | 706 | 93.5% | 5.0 [4.0] | [1, 19] | 99.2% | Rises under pressure |
| 4 | Matheesha Pathirana (8661) | Tier 1 | +5.34 | +4.13 | +1.21 | +3.89 | 307 | 83.4% | 3.0 [4.0] | [1, 41] | 22.2% | Elite all the time |
| 5 | Eshan Malinga (39657) | Tier 2 | +3.85 | +0.46 | +3.39 | +3.69 | 176 | 71.9% | 6.0 [5.0] | [1, 38] | 74.4% | Rises under pressure |
| 6 | Nathan Ellis (7920) | Tier 2 | +5.50 | +2.35 | +3.15 | +4.68 | 229 | 54.8% | 7.0 [6.0] | [1, 36] | 65.9% | Rises under pressure |
| 7 | Noor Ahmad (7967) | Tier 3 | +2.54 | +2.75 | -0.21 | +1.58 | 351 | 40.1% | 12.0 [11.0] | [6, 62] | 54.5% | Balanced / Context-dep |
| 8 | Arshdeep Singh (6464) | Tier 3 | +1.90 | +0.91 | +0.99 | +1.58 | 593 | 35.1% | 12.0 [7.0] | [9, 55] | 55.8% | Balanced / Context-dep |
| 9 | Prasidh Krishna (4489) | Tier 3 | +2.96 | +0.29 | +2.67 | +2.86 | 234 | 31.7% | 13.0 [8.0] | [5, 63] | 68.3% | Rises under pressure |
| 10 | Bhuvneshwar Kumar (360) | Tier 3 | +3.25 | +4.56 | -1.31 | +1.65 | 361 | 27.2% | 17.0 [18.0] | [7, 56] | 1.9% | Elite all the time |

### Detailed Profiles (Ranks 1 to 5)
1. **Sunil Narine (`player_id`: 781) — Tier 1 | Classification: Balanced / Context-dependent**
   - *Metrics:* Multiverse Top-10: 100.0% (99.97%), Median Rank 3.0 [IQR 1.0], Defending Shrunk Impact: +6.57 runs/24b, Raw Lift: +0.64 runs/24b, HP Balls: 422.
   - *Bootstrap Stability:* 1,000 / 1,000 eligible draws; 90% rank interval [1, 17].
   - *Resilience:* Rises under pressure in 52.5% of specifications.
   - *IPL 2026 Team (Raw Data):* Kolkata Knight Riders. Availability for IPL 2027: UNVERIFIED.
   - *Rajasthan Royals Tactical Fit:* Defensive spin controller, if available at auction, to restrict middle-overs run rates.
2. **Jasprit Bumrah (`player_id`: 2933) — Tier 1 | Classification: Elite all the time**
   - *Metrics:* Multiverse Top-10: 99.2%, Median Rank 2.0 [IQR 2.0], Defending Shrunk Impact: +7.61 runs/24b, Raw Lift: +0.33 runs/24b, HP Balls: 332.
   - *Bootstrap Stability:* 999 / 1,000 eligible draws; 90% rank interval [1, 23].
   - *Resilience:* Rises under pressure in 7.2% of specifications (reflecting a baseline of +7.28 runs saved/24b).
   - *IPL 2026 Team (Raw Data):* Mumbai Indians. Availability for IPL 2027: UNVERIFIED.
   - *Rajasthan Royals Tactical Fit:* Frontline pace anchor across all match phases, if available at auction.
3. **Rashid Khan (`player_id`: 4722) — Tier 1 | Classification: Rises under pressure**
   - *Metrics:* Multiverse Top-10: 93.5%, Median Rank 5.0 [IQR 4.0], Defending Shrunk Impact: +5.59 runs/24b, Raw Lift: +2.75 runs/24b, HP Balls: 706.
   - *Bootstrap Stability:* 1,000 / 1,000 eligible draws; 90% rank interval [1, 19].
   - *Resilience:* Rises under pressure in 99.2% of specifications.
   - *IPL 2026 Team (Raw Data):* Gujarat Titans. Availability for IPL 2027: UNVERIFIED.
   - *Rajasthan Royals Tactical Fit:* Attacking wrist-spin option, if available at auction, addressing middle-overs economy deficits.
4. **Matheesha Pathirana (`player_id`: 8661) — Tier 1 | Classification: Elite all the time**
   - *Metrics:* Candidate Eligibility: 100.0%, Multiverse Top-10: 83.4%, Median Rank 3.0 [IQR 4.0], Defending Shrunk Impact: +5.34 runs/24b, Raw Lift: +1.21 runs/24b, HP Balls: 307.
   - *Bootstrap Stability:* 1,000 / 1,000 eligible draws; 90% rank interval [1, 41].
   - *Resilience:* Elite across all match states in 77.8% of specifications.
   - *IPL 2026 Team (Raw Data):* Kolkata Knight Riders (mapped in `competition_team_player_mapping.csv`). Availability: UNVERIFIED. Note: Sustained confirmed hamstring injury on 16 May 2026 (replaced by Luvnith Sisodia); actively rehabilitating; do not assume 2027 unavailability.
   - *Rajasthan Royals Tactical Fit:* Specialist death bowler, if available at auction, providing strong run restriction (+5.34 runs saved/24b).
5. **Eshan Malinga (`player_id`: 39657) — Tier 2 | Classification: Rises under pressure**
   - *Metrics:* Multiverse Top-10: 71.9%, Median Rank 6.0 [IQR 5.0], Defending Shrunk Impact: +3.85 runs/24b, Raw Lift: +3.39 runs/24b, HP Balls: 176.
   - *Bootstrap Stability:* 912 / 1,000 eligible draws; 90% rank interval [1, 38].
   - *Resilience:* Rises under pressure in 74.4% of specifications.
   - *IPL 2026 Team (Raw Data):* Sunrisers Hyderabad (mapped in `competition_team_player_mapping.csv`). Availability: UNVERIFIED.
   - *Rajasthan Royals Tactical Fit:* Emerging pace option, if available at auction, demonstrating significant lift (+3.39) under leverage.

---

<!-- PAGE 10 -->
# Page 10: Top 10 Bowlers — Profiles (Ranks 6 to 10) & Landscape

### Detailed Profiles (Ranks 6 to 10)
6. **Nathan Ellis (`player_id`: 7920) — Tier 2 | Classification: Rises under pressure**
   - *Metrics:* Candidate Eligibility: 75.5%, Multiverse Top-10: 54.8% (retains top 10 in 72.5% when eligible), Median Rank 7.0 [IQR 6.0], Defending Shrunk Impact: +5.50 runs/24b, Raw Lift: +3.15 runs/24b, HP Balls: 229.
   - *Bootstrap Stability:* 988 / 1,000 eligible draws; 90% rank interval [1, 36].
   - *Resilience:* Rises under pressure in 65.9% of specifications.
   - *IPL 2026 Team (Raw Data):* Chennai Super Kings (mapped in `competition_team_player_mapping.csv`; traded CSK to Sunrisers Hyderabad on 5 Nov 2026 in an all-cash INR 2.00 Cr transaction [Official]). Availability: UNVERIFIED.
   - *Rajasthan Royals Tactical Fit:* Tactical death-overs target, if available at auction, to replace high-economy supporting overs.
7. **Noor Ahmad (`player_id`: 7967) — Tier 3 | Classification: Balanced / Context-dependent**
   - *Metrics:* Multiverse Top-10: 40.1%, Median Rank 12.0 [IQR 11.0], Defending Shrunk Impact: +2.54 runs/24b, Raw Lift: -0.21 runs/24b, HP Balls: 351.
   - *Bootstrap Stability:* 1,000 / 1,000 eligible draws; 90% rank interval [6, 62].
   - *Resilience:* Rises under pressure in 54.5% of specifications.
   - *IPL 2026 Team (Raw Data):* Chennai Super Kings (mapped in `competition_team_player_mapping.csv`). Availability: UNVERIFIED.
   - *Rajasthan Royals Tactical Fit:* Left-arm wrist-spinner, if available at auction, providing middle-overs control.
8. **Arshdeep Singh (`player_id`: 6464) — Tier 3 | Classification: Balanced / Context-dependent**
   - *Metrics:* Candidate Eligibility: 100.0%, Multiverse Top-10: 35.1%, Median Rank 12.0 [IQR 7.0], Defending Shrunk Impact: +1.90 runs/24b, Raw Lift: +0.99 runs/24b, HP Balls: 593.
   - *Bootstrap Stability:* 1,000 / 1,000 eligible draws; 90% rank interval [9, 55].
   - *Resilience:* Rises under pressure in 55.8% of specifications.
   - *IPL 2026 Team (Raw Data):* Punjab Kings in raw data (mapped in `competition_team_player_mapping.csv`; traded PBKS to Mumbai Indians on 11 Nov 2026 in player-swap for Hardik Pandya [Official]). Availability: UNVERIFIED.
   - *Rajasthan Royals Tactical Fit:* Indian left-arm seam option across powerplay and death overs, if available at auction.
9. **Prasidh Krishna (`player_id`: 4489) — Tier 3 | Classification: Rises under pressure**
   - *Metrics:* Multiverse Top-10: 31.7%, Median Rank 13.0 [IQR 8.0], Defending Shrunk Impact: +2.96 runs/24b, Raw Lift: +2.67 runs/24b, HP Balls: 234.
   - *Bootstrap Stability:* 994 / 1,000 eligible draws; 90% rank interval [5, 63].
   - *Resilience:* Rises under pressure in 68.3% of specifications.
   - *IPL 2026 Team (Raw Data):* Gujarat Titans (mapped in `competition_team_player_mapping.csv`). Availability: UNVERIFIED.
   - *Rajasthan Royals Tactical Fit:* Hit-the-deck pace bowler with strong raw lift (+2.67), if available at auction.
10. **Bhuvneshwar Kumar (`player_id`: 360) — Tier 3 | Classification: Elite all the time**
    - *Metrics:* Multiverse Top-10: 27.2%, Median Rank 17.0 [IQR 18.0], Defending Shrunk Impact: +3.25 runs/24b, Raw Lift: -1.31 runs/24b, HP Balls: 361.
    - *Bootstrap Stability:* 1,000 / 1,000 eligible draws; 90% rank interval [7, 56].
    - *Resilience:* Rises under pressure in 1.9% of specifications (reflecting an elite normal baseline of +4.56 runs saved/24b).
    - *IPL 2026 Team (Raw Data):* Royal Challengers Bengaluru (mapped in `competition_team_player_mapping.csv`). Availability: UNVERIFIED.
    - *Rajasthan Royals Tactical Fit:* Experienced new-ball swing bowler with disciplined control, if available at auction.

![Bowling Maintenance vs Lift](file:///c:/Users/LENOVO/OneDrive/Desktop/SupeRR-Selector-Season-2/outputs/model_v4/charts/fig3_maintenance_vs_lift_bowlers.png)

---

<!-- PAGE 11 -->
# Page 11: Rajasthan Royals 2026 Campaign Audit & Tactical Planning

### 11. Audited Rajasthan Royals 2026 Squad Performance (from raw data)
To ensure recommendations solve concrete franchise deficits, I audited RR's 2026 IPL campaign directly from `matches.csv`, `ball_by_ball.csv`, and `playing_eleven.csv`. RR played 16 matches, captained primarily by Riyan Parag (14 matches) with Yashasvi Jaiswal leading in 2 matches (Sanju Samson represented Chennai Super Kings in 2026).

| Player Name | Player ID | Actual Apps | Runs Scored | Balls Faced | Bat SR | Overs Bowled | Runs Conceded | Wickets Taken | Economy Rate |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| Vaibhav Sooryavanshi | 50284 | 16 | 776 | 327 | 237.31 | 0.0 | 0 | 0 | &mdash; |
| Dhruv Jurel | 7260 | 16 | 515 | 333 | 154.65 | 0.0 | 0 | 0 | &mdash; |
| Yashasvi Jaiswal | 6819 | 16 | 427 | 280 | 152.50 | 0.0 | 0 | 0 | &mdash; |
| Jofra Archer | 3298 | 16 | 64 | 47 | 136.17 | 60.0 | 559 | 25 | 9.32 |
| Donovan Ferreira | 8182 | 15 | 317 | 177 | 179.10 | 3.0 | 41 | 1 | 13.67 |
| Riyan Parag [C] | 6423 | 14 | 309 | 196 | 157.65 | 4.0 | 38 | 2 | 9.50 |
| Ravindra Jadeja | 152 | 14 | 266 | 197 | 135.03 | 33.0 | 277 | 10 | 8.39 |
| Nandre Burger | 7312 | 13 | 14 | 9 | 155.56 | 43.5 | 440 | 14 | 10.11 |
| Brijesh Sharma | 67036 | 13 | 2 | 4 | 50.00 | 45.5 | 450 | 14 | 9.89 |
| Ravi Bishnoi | 7503 | 9 | 0 | 3 | 0.00 | 26.0 | 257 | 11 | 9.88 |
| Shimron Hetmyer | 3297 | 8 | 78 | 69 | 113.04 | 0.0 | 0 | 0 | &mdash; |
| Tushar Deshpande | 6806 | 7 | 26 | 14 | 185.71 | 23.0 | 275 | 4 | 11.96 |
| Sandeep Sharma | 2411 | 6 | 0 | 0 | &mdash; | 19.4 | 224 | 5 | 11.39 |
| Kuldeep Sen | 7545 | 0 | 0 | 0 | &mdash; | 0.0 | 0 | 0 | &mdash; |

### 12. Phase-Level Evidence & Strategic Recruitment Opportunities
Auditing deliveries by match phase from `data/raw` identifies three tactical focal areas for Rajasthan Royals:

1. **Death-Overs Bowling Execution (Overs 16–20):**
   - RR's team economy rate at the death was **10.60**, closely matching the league death average of **10.67** (indicating league-average team performance overall).
   - However, individual variance was severe: Jofra Archer (ER 9.35) and Nandre Burger (ER 9.33) bowled well, whereas Sandeep Sharma conceded **13.70** runs/over across 46 death balls and Tushar Deshpande conceded **12.38** across 48 death balls.
   - *Recruitment Opportunity:* If available at auction, targeted death seamers like Nathan Ellis (+5.50 shrunk impact) or Eshan Malinga (+3.39 raw lift) provide options to replace expensive supporting death overs.
2. **Middle-Overs Spin Economy (Overs 7–15):**
   - In the middle overs, RR's spin group conceded **9.29** runs/over across all spinners (9.19 for Jadeja, Punja, and Bishnoi) compared to the league spin average of **8.97** (a visible control gap).
   - While Ravindra Jadeja maintained a solid economy of **8.39**, secondary spinners conceded higher rates: Yash Punja (41503) posted ER **9.54** and Ravi Bishnoi posted ER **10.11** (with a dot ball rate of only 21.9%).
   - *Recruitment Opportunity:* If available at auction, adding a controlling wrist-spinner like Noor Ahmad or Rashid Khan would help bridge the middle-overs spin economy gap.
3. **Death-Overs Batting Support (Overs 16–20):**
   - At the death, Donovan Ferreira produced a strike rate of **221.7** across 83 death balls (well above the league death average of 169.4).
   - However, secondary death hitters lacked comparable boundary production: Ravindra Jadeja recorded SR **140.5**, Shubham Dubey recorded SR **146.3**, and Shimron Hetmyer scored at SR **121.1** (78 runs off 69 balls overall).
   - *Recruitment Opportunity:* RR requires a second, preferably Indian, death hitter. If available at auction, Shashank Singh (+22.2 raw lift) or Naman Dhir (+35.4 raw lift) would effectively complement Ferreira.

---

<!-- PAGE 12 -->
# Page 12: Model Reliability, Limitations & Walk-Forward Validation

### 13. Walk-Forward Temporal Validation (2022–2024 $\to$ 2025–2026)
To evaluate out-of-sample predictive validity honestly, models trained on 2022–2024 data were tested against out-of-sample 2025–2026 performance:
- **Canonical Model ($P2, W1, M=B, V=6, K=120, F={all}, G={standard}$):**
  - Batting Rank Correlation: $r = 0.0508$ ($p = 0.7864$).
  - Bowling Rank Correlation: $r = 0.2646$ ($p = 0.0721$).
- **Methodological Takeaway:** Batting pressure rankings are **descriptive, not predictive**. High-pressure batting over a single season or two-season window contains substantial noise, situational variance, and role volatility. Historical pressure metrics describe what occurred under specific match conditions rather than guaranteeing future replication. Bowling pressure performance demonstrates modest stability ($r = 0.26$), but still contains significant season-to-season variation.

### 14. Bootstrap Stability Hurdle & Excluded Candidates
Applying the 1,000-draw stratified match bootstrap hurdle ($\ge 800$ valid eligible resamples) removed volatile fringe players:
- **Matthew Wade (`player_id`: 796):** Achieved 52.96% multiverse top-10 frequency and median rank 4.0, but only qualified in **720 / 1,000** bootstrap resamples. In 28% of resampled universes, his sample size fell below the threshold. His exclusion promoted Rashid Khan (#10) into the final batting list.
- **Mujeeb Ur Rahman (`player_id`: 6450):** Achieved 49.14% multiverse top-10 frequency, but qualified in only **744 / 1,000** bootstrap resamples.
- **Naveen ul Haq (`player_id`: 5809):** Achieved 48.74% multiverse top-10 frequency, but qualified in only **513 / 1,000** bootstrap resamples.
- Their removal promoted Prasidh Krishna (#9) and Bhuvneshwar Kumar (#10) into the final bowling list.

![Bootstrap Stability Distributions](file:///c:/Users/LENOVO/OneDrive/Desktop/SupeRR-Selector-Season-2/outputs/model_v4/charts/fig4_bootstrap_stability_batters.png)

---

<!-- PAGE 13 -->
# Page 13: Players Next in Line (Ranks 11–15) & Strategic Alternatives

### 15. Batters Next in Line (Ranks 11 to 15)
| Rank | Player Name | Player ID | Multiverse Top-10 % | Median Rank [IQR] | Bootstrap Eligible Draws | Strategic Role & Tactical Context |
| :---: | :--- | :---: | :---: | :---: | :---: | :--- |
| **11** | Ashutosh Sharma | 8101 | 38.20% | 9.0 [11.0] | 662 / 1000 | Lower-order finisher (+29.7 raw lift); sample volatility in bootstrap resamples. |
| **12** | Shreyas Iyer | 3647 | 32.62% | 14.0 [12.0] | 999 / 1000 | Middle-order spin anchor; solid baseline but moderate pressure lift (+4.2). |
| **13** | Mahendra Singh Dhoni | 8 | 23.79% | 14.0 [12.0] | 978 / 1000 | Veteran death finisher (+14.8 raw lift); lower volume in international format scope. |
| **14** | Nicholas Pooran | 3125 | 12.61% | 22.0 [14.0] | 1000 / 1000 | High baseline overseas middle-order hitter; qualifies across all specifications. |
| **15** | Namboori Tilak Varma | 7897 | 11.50% | 24.0 [15.0] | 1000 / 1000 | Versatile Indian top/middle-order batter with solid cross-format baseline. |

*(Note: Reeza Hendricks achieved 26.37% top-10 frequency across specifications where he qualified, but was excluded from the candidate pool because his overall eligibility was 35.59%, below the pre-registered 50% candidate gate).*

### 16. Bowlers Next in Line (Ranks 11 to 15)
| Rank | Player Name | Player ID | Multiverse Top-10 % | Median Rank [IQR] | Bootstrap Eligible Draws | Strategic Role & Tactical Context |
| :---: | :--- | :---: | :---: | :---: | :---: | :--- |
| **11** | Krunal Pandya | 4219 | 26.17% | 14.0 [12.0] | 1000 / 1000 | Defensive left-arm orthodox spinner (+2.41 raw lift); excellent economy discipline. |
| **12** | Alzarri Joseph | 3275 | 26.14% | 24.0 [15.0] | 1000 / 1000 | Overseas pace strike option; effective in short high-leverage bursts. |
| **13** | Mohammad Nawaz | 2490 | 24.85% | 11.0 [10.0] | 990 / 1000 | Left-arm spinner (+2.15 raw lift); derived strictly from international T20I matches. |
| **14** | T Natarajan | 4265 | 22.40% | 18.0 [11.0] | 1000 / 1000 | Specialized Indian death bowler; strong consistency under pressure. |
| **15** | Ravi Bishnoi | 7503 | 21.80% | 19.0 [12.0] | 1000 / 1000 | Attacking Indian leg-spinner; currently on RR roster (ER 9.88 in 2026). |

*(Note: Abbas Afridi achieved 27.83% top-10 frequency across lenient specifications, but qualified in only 40.03% of specifications, failing the 50% candidate gate. Pakistani players have historically not participated in the IPL player auction since 2008 and 2027 auction registration/eligibility remains unconfirmed; their metrics derive strictly from international T20Is).*

---

<!-- PAGE 14 -->
# Page 14: Technical Appendices & Verification Register

### Appendix A: Canonical Baseline Unfiltered Rankings (Specification P2-W1-Model B)
| Rank | Unfiltered Batter | PWI | Raw Lift | Rank | Unfiltered Bowler | PWI | Raw Lift |
| :---: | :--- | :---: | :---: | :---: | :--- | :---: | :---: |
| 1 | Tim David (6396) | +42.9 | +9.0 | 1 | Sunil Narine (781) | +6.57 | +0.64 |
| 2 | Naman Dhir (37052) | +34.7 | +35.4 | 2 | Jasprit Bumrah (2933) | +7.61 | +0.33 |
| 3 | Matthew Wade* (796) | +31.7 | +35.7 | 3 | Rashid Khan (4722) | +5.59 | +2.75 |
| 4 | Romario Shepherd (6726) | +28.7 | +5.0 | 4 | Nathan Ellis (7920) | +5.50 | +3.15 |
| 5 | Rashid Khan (4722) | +28.1 | +40.3 | 5 | Eshan Malinga (39657) | +3.85 | +3.39 |
| 6 | Reeza Hendricks^ (768) | +31.5 | +27.8 | 6 | Matheesha Pathirana (8661) | +5.34 | +1.21 |
| 7 | Shashank Singh (2756) | +32.2 | +22.2 | 7 | Mujeeb Ur Rahman* (6450) | +5.06 | +3.48 |
| 8 | Heinrich Klaasen (4260) | +24.9 | +3.4 | 8 | Naveen ul Haq* (5809) | +3.20 | +2.24 |
| 9 | Ashutosh Sharma (8101) | +31.6 | +29.7 | 9 | Bhuvneshwar Kumar (360) | +3.25 | -1.31 |
| 10 | Dinesh Karthik (143) | +34.4 | +16.1 | 10 | Krunal Pandya (4219) | +3.22 | +2.41 |

*\*Removed by bootstrap stability hurdle (<800 draws). ^Excluded by 50% candidate eligibility gate.*

### Appendix B: Exact Pipeline Reproduction Commands
```powershell
# 1. Run Complete Multiverse Pipeline (15,150 specs / role; 3,196,444 evaluations):
python -m src.model_v4.run_multiverse_pipeline

# 2. Run Comprehensive Unit & Statistical Validation Suite (54 passed):
python -m pytest tests/model_v2 tests/model_v3 tests/model_v4 -q

# 3. Verify Player IDs, Checksums & Sequential Variance Decomposition:
python outputs/submission_final/build_verification.py
```

### Appendix C: Verified External Fact Register & Availability Status
Every player's IPL 2026 team is confirmed directly from `data/raw/competition_team_player_mapping.csv`. External retirement/trade claims are sourced directly from `outputs/final_package/source_register.md` or official league portals:
- **Nathan Ellis (`player_id`: 7920):** Mapped to CSK in IPL 2026 raw data; traded CSK to Sunrisers Hyderabad on 5 Nov 2026 in an all-cash INR 2.00 Cr transaction (*iplt20.com* / SRH Official, 2026-11-05; accessed 2026-11-14). [Official]
- **Arshdeep Singh (`player_id`: 6464):** Mapped to PBKS in IPL 2026 raw data; traded PBKS to Mumbai Indians on 11 Nov 2026 in player-swap for Hardik Pandya (*iplt20.com*, 2026-11-11; accessed 2026-11-14). [Official]
- **Matheesha Pathirana (`player_id`: 8661):** Sustained confirmed hamstring injury on 16 May 2026 and replaced by Luvnith Sisodia for remainder of season; actively rehabilitating; do not assume 2027 unavailability (*KKR / ESPNcricinfo*, 2026-05-18; accessed 2026-11-14). [Official / Reputable Media]
- **Andre Russell (`player_id`: 1318):** Retired from IPL on 30 Nov 2025; appointed KKR Power Coach for IPL 2026 while continuing in select non-IPL leagues (*The Hindu*, 2025-11-30; accessed 2026-11-12). [Reputable Media]
- **Dinesh Karthik (`player_id`: 143):** Retired after IPL 2024; active RCB Batting Coach & Mentor (*India TV News*, 2024-07-01; accessed 2026-11-12). [Reputable Media]
- **Matthew Wade (`player_id`: 796):** Retired from international cricket and Australian domestic cricket (BBL / state) to take up coaching duties (*cricket.com.au*, 2024-10-29 & 2026-09-17; accessed 2026-11-14). [Official]
- **Pakistani Players (BCCI / IPL Historical Record 2008–2026):** Have historically not participated in the IPL player auction since 2008; 2027 auction registration/eligibility remains unconfirmed. [Historical Record]
- **All other IPL 2027 Auction statuses:** Strictly marked **UNVERIFIED** as the official BCCI IPL 2027 auction registration list remains unpublished.

*End of Report — SupeRR Selector Season 2 Round 1 Submission.*
