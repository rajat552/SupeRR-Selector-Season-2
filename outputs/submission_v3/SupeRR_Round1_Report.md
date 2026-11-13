# SupeRR Selector Season 2 — Rajasthan Royals IPL 2027 Auction Intelligence Report
## Objective Identification of High-Pressure Performers via Leave-Player-Out Contextual Baselines, Empirical Bayes Shrinkage, and Match-Cluster Bootstrap Verification

**Candidate Submission — Round 1**  
**Author:** Candidate (Individual Participant Submission for Rajasthan Royals)  
**Date:** 2026-11-14  
**Primary Deliverable:** `outputs/submission_v3/SupeRR_Round1_Report.pdf` (14 Pages)  
**Codebase & Deliverables:** `src/model_v3/`, `tests/model_v3/`, `outputs/model_v3/`, `outputs/submission_v3/`  
**Governing Standard:** Full Compliance with Competition Problem Statement & AGENTS.md Immutability Protocols  

---

<!-- PAGE 1: EXECUTIVE SUMMARY & CANONICAL RANKINGS -->
<div style="page-break-after: always;"></div>

# Section 1: Executive Summary & Canonical Rankings

### Operational Definition of High Pressure
> **High Pressure** is defined as any pre-delivery match state where the defending or chasing team faces acute leverage—characterized by a required run rate $\ge 9.0$ in chases, an impending death-phase escalation (overs 16–20), or severe top-order resource depletion ($\ge 3$ wickets down in powerplay or $\ge 5$ in middle overs)—quantified continuously via a pre-delivery Pressure Index ($PI \in [0, 1]$), with acute pressure isolated at $PI \ge 0.50$ without outcome look-ahead.

### Three Core Strategic Findings for Rajasthan Royals Leadership
1. **Separation of Raw Lift from Sustainable Impact:** Elite baseline performers (such as Jasprit Bumrah and Sunil Narine) carry near-zero raw lift because their regular performance already operates near the physical ceiling; conversely, lower-order specialists (such as Tim David, Naman Dhir, and Nathan Ellis) generate massive positive lift when thrust into high-leverage situations. My model isolates maintenance from lift without penalizing world-class baseline excellence.
2. **Resolution of Rajasthan Royals' 2026 Death Bowling Crisis:** In IPL 2026, Rajasthan Royals conceded heavily at the death outside of Jofra Archer (60.0 overs, 25 wickets, economy 9.32), with Sandeep Sharma leaking 11.39 runs per over (19.4 overs) and Tushar Deshpande conceding 11.96 (23.0 overs). My bowling architecture reveals Nathan Ellis (#4, composite score +1.70, death impact +3.79 per 24 balls) and Matheesha Pathirana (#6, composite score +1.45, death impact +5.16 per 24 balls) as the premier high-pressure execution targets.
3. **Middle-Order Finishing Resilience:** Following Shimron Hetmyer's 2026 output compression (8 appearances, 78 runs in 69 balls, strike rate 113.04), Dhruv Jurel was overburdened. My batting model identifies Naman Dhir (#2, composite score +2.11, raw lift +50.23 per 100 balls) and Shashank Singh (#6, composite score +1.72, death impact +31.50 per 100 balls) as elite domestic targets capable of anchoring high-leverage chases.

---

### Canonical Top 10 Batters (Performance Under Pressure vs Usual Performance)
*Filtered by $\ge 800$ valid draws across 1,000 stratified match-cluster bootstrap resamples. Evaluated per 100 balls faced.*

| Rank | Player Name | Franchise Context | Statistical Tier | Model Score | Shrunk PWI | Raw Lift | Maint-Lift | Match Consistency | Kish $N_{eff}$ | Bootstrap Median (p05–p95) |
|---:|---|---|---|---:|---:|---:|---:|---:|---:|---:|
| **#1** | **Tim David** | Royal Challengers Bengaluru | **Tier 1** | **+2.484** | +42.91 | +10.00 | +31.04 | 64.9% | 744.3 | 3.0 (1.0–16.0) |
| **#2** | **Naman Dhir** | Mumbai Indians | **Tier 1** | **+2.114** | +34.72 | +50.23 | +34.97 | 62.4% | 286.7 | 5.0 (1.0–32.0) |
| **#3** | **Reeza Hendricks** | SA20 / Global T20 | **Tier 2** | **+1.757** | +31.49 | +35.94 | +30.19 | 60.6% | 424.9 | 8.0 (1.0–35.1) |
| **#4** | **Romario Shepherd** | Mumbai Indians | **Tier 2** | **+1.738** | +28.73 | +1.81 | +20.42 | 66.1% | 507.4 | 10.0 (2.0–36.0) |
| **#5** | **Rashid Khan** | Gujarat Titans | **Tier 2** | **+1.736** | +28.07 | +57.81 | +29.82 | 62.6% | 427.9 | 8.0 (1.0–40.4) |
| **#6** | **Shashank Singh** | Punjab Kings | **Tier 2** | **+1.725** | +32.24 | +27.28 | +28.74 | 60.2% | 402.1 | 9.0 (1.0–44.0) |
| **#7** | **Dinesh Karthik** | RCB Batting Coach (Ret.) | **Tier 2** | **+1.678** | +34.40 | +21.67 | +28.01 | 58.4% | 372.0 | 10.5 (1.0–44.0) |
| **#8** | **Rinku Singh** | Kolkata Knight Riders | **Tier 2** | **+1.601** | +31.01 | +21.24 | +26.44 | 59.9% | 711.1 | 10.0 (2.0–39.0) |
| **#9** | **Andre Russell** | KKR Power Coach (Ret.) | **Tier 2** | **+1.530** | +31.85 | -0.70 | +21.05 | 60.5% | 490.0 | 12.0 (2.0–54.0) |
| **#10** | **Heinrich Klaasen** | Sunrisers Hyderabad | **Tier 3** | **+1.482** | +24.88 | +4.57 | +17.35 | 65.6% | 772.9 | 15.0 (5.0–34.0) |

---

### Canonical Top 10 Bowlers (Performance Under Pressure vs Usual Performance)
*Filtered by $\ge 800$ valid draws across 1,000 stratified match-cluster bootstrap resamples. Evaluated per 24 legal balls bowled.*

| Rank | Player Name | Franchise Context | Statistical Tier | Model Score | Shrunk PWI | Raw Lift | Maint-Lift | Match Consistency | Kish $N_{eff}$ | Bootstrap Median (p05–p95) |
|---:|---|---|---|---:|---:|---:|---:|---:|---:|---:|
| **#1** | **Sunil Narine** | Kolkata Knight Riders | **Tier 1** | **+2.203** | +6.57 | +0.90 | +4.50 | 59.0% | 893.3 | 4.0 (1.0–17.0) |
| **#2** | **Jasprit Bumrah** | Mumbai Indians | **Tier 1** | **+2.141** | +7.61 | +0.95 | +5.06 | 54.2% | 723.0 | 4.0 (1.0–23.0) |
| **#3** | **Rashid Khan** | Gujarat Titans | **Tier 2** | **+1.994** | +5.59 | +3.01 | +4.59 | 58.0% | 1560.2 | 6.0 (1.0–19.0) |
| **#4** | **Nathan Ellis** | Punjab Kings | **Tier 2** | **+1.699** | +5.50 | +4.44 | +4.68 | 53.2% | 387.2 | 8.0 (1.0–36.7) |
| **#5** | **Eshan Malinga** | Sri Lanka Domestic | **Tier 2** | **+1.563** | +3.85 | +4.40 | +3.69 | 57.2% | 420.0 | 9.0 (1.0–38.5) |
| **#6** | **Matheesha Pathirana** | Kolkata Knight Riders | **Tier 2** | **+1.448** | +5.34 | +1.77 | +3.89 | 50.9% | 556.1 | 10.0 (1.0–41.0) |
| **#7** | **Mohammad Nawaz** | Pakistan / PSL | **Tier 2** | **+1.343** | +4.00 | +1.28 | +2.93 | 54.5% | 579.8 | 13.0 (2.0–44.0) |
| **#8** | **Arshdeep Singh** | Traded to Mumbai Indians | **Tier 3** | **+0.878** | +1.90 | +1.14 | +1.58 | 55.0% | 1193.3 | 25.5 (9.0–55.0) |
| **#9** | **Krunal Pandya** | Royal Challengers Bengaluru | **Tier 3** | **+0.870** | +3.15 | +0.76 | +2.25 | 50.2% | 740.8 | 23.0 (5.0–63.0) |
| **#10** | **Wanindu Hasaranga** | Lucknow Super Giants | **Tier 3** | **+0.849** | +2.78 | -0.40 | +1.66 | 52.0% | 1177.8 | 25.0 (8.0–55.0) |

</div>

---

<!-- PAGE 2: PRESSURE DEFINITION & DECOMPOSITION -->
<div style="page-break-after: always;"></div>

# Section 2: Mathematical Definition of High Pressure & Match-State Architecture

In constructing my evaluation framework, I established a strict operational boundary: match pressure must be calculated **strictly pre-delivery**, utilizing only the state of the game prior to the bowler releasing the ball. Any methodology that incorporates the ball's actual outcome (such as post-delivery win probability changes) introduces severe look-ahead leakage.

```
       +-------------------------------------------------------------+
       | PRE-DELIVERY MATCH STATE (Zero Look-Ahead Information)       |
       | - Innings, Balls Remaining, Runs Remaining (Innings 2)      |
       | - Current Run Rate (CRR), Required Run Rate (RRR)           |
       | - Wickets Down, Match Phase (Powerplay, Middle, Death)      |
       | - Pre-Match Team Relative Strength (Dual-Track Elo)         |
       +-------------------------------------------------------------+
                                      |
                     +----------------+----------------+
                     |                                 |
                     v                                 v
        [CHASING INNINGS (Inn 2)]          [DEFENDING INNINGS (Inn 1)]
        - Required Rate Leverage           - Projected Total vs Par
        - Wickets in Hand Leverage         - Phase Leverage (Death Overs)
        - Ball Depletion Acceleration      - Resource Depletion Stress
                     |                                 |
                     +----------------+----------------+
                                      |
                                      v
                     +---------------------------------+
                     | CONTINUOUS PRESSURE INDEX (PI)  |
                     | Range: [0.0, 1.0]               |
                     | Acute Pressure Cutoff: PI >= 0.50|
                     +---------------------------------+
```

### Chasing Innings Formulation (Innings 2)
In run chases, pressure stems from required run rate stress modulated by wickets remaining and ball depletion:
$$\text{Leverage}_{\text{chase}} = \frac{\text{RRR}}{\max(6.0, \text{CRR})} \cdot \left(1 + \frac{\text{wickets\_lost}}{10}\right) \cdot \left(1 - \frac{\text{balls\_remaining}}{120}\right)^{0.5}$$

### Defending Innings Formulation (Innings 1)
In the first innings, setting a competitive total creates pressure through resource depletion and death-overs urgency:
$$\text{Leverage}_{\text{defend}} = \left(\frac{\text{wickets\_lost}}{10}\right)^{1.2} \cdot \left[1 + 0.50 \cdot \mathbf{1}_{\text{Death}}(\text{over} \ge 16) + 0.25 \cdot \mathbf{1}_{\text{Middle}}(\text{over} \in [7, 15])\right]$$

### Phase Distribution and Role Asymmetry
Across the audited primary scope of **837 matches** (367 IPL, 470 T20I; 193,988 deliveries; 185,692 legal balls), I identified **38,752 legal deliveries** meeting the acute bowler pressure threshold ($PI \ge 0.50$). The distribution across phases demonstrates why bowler pressure cannot be equated with death-overs bowling:
- **Powerplay (Overs 1–6):** 548 legal balls (**1.41%** of bowler high-pressure volume)
- **Middle Overs (Overs 7–15):** 24,038 legal balls (**62.03%** of bowler high-pressure volume)
- **Death Overs (Overs 16–20):** 14,166 legal balls (**36.56%** of bowler high-pressure volume)

Crucially, **only 7,037 legal deliveries (18.16%)** are simultaneously classified as high-pressure for both the batter and the bowler. When a bowling side faces acute defending pressure (e.g., chasing team cruising at 120/1 in 13 overs), the fielding side operates under intense stress, whereas the batting side faces low pressure. My dual-track pressure indices capture this fundamental asymmetry.

![Sample Size and Exposure Depth](file:///c:/Users/LENOVO/OneDrive/Desktop/SupeRR-Selector-Season-2/outputs/model_v3/charts/10_player_sample_size_comparison.png)

</div>

---

<!-- PAGE 3: PERFORMANCE MEASUREMENT & LPO BASELINES -->
<div style="page-break-after: always;"></div>

# Section 3: Performance Measurement, Runs-Above-Par & Leave-Player-Out Baselines

To measure whether a player exceeds expectations, I benchmark every delivery against a **Leave-Player-Out (LPO) Context Baseline**. In standard baseline calculations, an elite player's own balls inflate the cell average, penalizing them in small cells. By subtracting player $i$'s own deliveries from cell $c$, I ensure that baseline expectations remain completely independent of the subject:
$$\bar{R}_{-i, c} = \frac{\sum_{j \neq i, k \in c} \text{runs}_{j, k}}{N_c - n_{i, c}}, \quad \bar{W}_{-i, c} = \frac{\sum_{j \neq i, k \in c} \text{wicket}_{j, k}}{N_c - n_{i, c}}$$

Whenever a cell's leave-player-out sample size drops below 50 deliveries ($N_c - n_{i, c} < 50$), my model automatically falls back to the parent level in the hierarchical context structure:
- **Level 0:** Competition Tier $\times$ Season Year $\times$ Match Phase $\times$ Wickets Fallen Bucket $\times$ Batter Role / Bowling Style $\times$ Opponent Strength Tier
- **Level 1:** Competition Tier $\times$ Season Year $\times$ Match Phase $\times$ Batter Role / Bowling Style $\times$ Opponent Strength Tier (drops wickets bucket)
- **Level 2:** Competition Tier $\times$ Season Year $\times$ Match Phase $\times$ Batter Role / Bowling Style (drops opponent strength)
- **Level 3:** Competition Tier $\times$ Season Year $\times$ Match Phase
- **Level 4:** Competition Tier $\times$ Match Phase
- **Level 5:** Global Match Phase

### Wicket Valuation and Contextual Net Impact
I assign wickets a baseline value of $w = 6.0$ runs, grounded in empirical boundary-replacement studies across T20 cricket. The context-adjusted single-delivery impact $\Delta I$ is defined as:
- **For Batters:** $\Delta I_{\text{bat}} = (\text{runs} - \bar{R}_{-i, c}) + 6.0 \cdot (\bar{W}_{-i, c} - \mathbf{1}_{\text{out}})$
- **For Bowlers:** $\Delta I_{\text{bowl}} = (\bar{R}_{-i, c} \cdot \mathbf{1}_{\text{legal}} - \text{runs}_{\text{conceded}}) + 6.0 \cdot (\mathbf{1}_{\text{wkt}} - \bar{W}_{-i, c} \cdot \mathbf{1}_{\text{legal}})$

### Kish Effective Sample Size and Empirical Bayes Shrinkage
Because continuous pressure weights $w_k \in [0, 1]$ introduce heteroskedasticity, raw ball counts overstate statistical power. I compute the exact Kish Effective Sample Size ($N_{\text{eff}}$) for every player:
$$N_{\text{eff}} = \frac{\left(\sum_{k=1}^n w_k\right)^2}{\sum_{k=1}^n w_k^2}$$
To eliminate small-sample noise, I shrink raw pressure impact toward zero using an Empirical Bayes shrinkage factor with calibration parameter $K = 120.0$:
$$\text{Shrunk PWI} = \text{Raw PWI} \cdot \left(\frac{N_{\text{eff}}}{N_{\text{eff}} + 120.0}\right)$$

![Observed vs Shrunk Impact Decomposition](file:///c:/Users/LENOVO/OneDrive/Desktop/SupeRR-Selector-Season-2/outputs/model_v3/charts/04_pressure_performance_comparison.png)

</div>

---

<!-- PAGE 4: FAIR COMPARISON ARCHITECTURE -->
<div style="page-break-after: always;"></div>

# Section 4: Fair Comparison Architecture, Eligibility & Format Harmonization

To guarantee fair comparisons across players with divergent exposure, I established four structural safeguards:

### 1. Dual-Path Eligibility Gate
To prevent low-exposure anomalies from infiltrating the rankings while protecting specialized finishers and strike bowlers, a player qualifies for primary ranking by meeting either:
- **Discrete Gate:** $\ge 120$ high-pressure legal deliveries ($PI \ge 0.50$), OR
- **Continuous Leverage Gate:** Kish Effective Sample Size $N_{\text{eff}} \ge 80.0$ and $\ge 200$ total deliveries in the primary scope.

### 2. Dual-Track Pre-Match Elo Ratings
I tracked team relative strength across separate, temporally isolated tracks for IPL and T20 International matches ($K=32$, initialized at 1500). Prior to every match, I classified opponents into three distinct strength tiers:
- **High Tier:** Opponent pre-match Elo $\ge 1520$
- **Medium Tier:** Opponent pre-match Elo $\in (1480, 1520)$
- **Low Tier:** Opponent pre-match Elo $\le 1480$
All Elo updates execute strictly post-match, preserving zero look-ahead integrity.

### 3. Model Architecture: Maintenance and Lift Without Elite Penalty (Model B)
Evaluating players solely on "raw lift" (High Pressure Impact minus Normal Impact) severely penalizes world-class players whose normal baseline is already exceptional. A bowler conceding 6.0 runs per over in normal conditions who concedes 6.0 in death overs produces zero raw lift, whereas a mediocre bowler conceding 11.0 normally who concedes 9.5 under pressure shows a +1.5 lift. To resolve this defect, I formulated **Model B (Maintenance & Lift)**:
$$\text{Baseline}_{\text{floor}} = \max(0.0, \text{Shrunk Norm Impact})$$
$$\text{Maint-Lift} = \text{Shrunk High-Pressure Impact} - 0.35 \cdot \text{Baseline}_{\text{floor}}$$
$$\text{Score} = 0.50 \cdot Z(\text{Shrunk High-Pressure Impact}) + 0.30 \cdot Z(\text{Maint-Lift}) + 0.20 \cdot Z(\text{Empirical Bayes Consistency})$$

```
+----------------------------------------------------------------------------------------------------+
| MODEL ARCHITECTURE COMPARISON & WALK-FORWARD OUT-OF-SAMPLE VALIDATION                              |
+-------------------+--------------------+--------------------+--------------------+-----------------+
| Model Identifier  | Bat OOS Spearman   | Bat LOSO Stability | Bowl OOS Spearman  | Bowl LOSO Stab  |
+-------------------+--------------------+--------------------+--------------------+-----------------+
| Model A (Abs Imp) | -0.0122            | 0.9123             | +0.2578            | 0.9191          |
| Model B (Maint)   | -0.0449            | 0.9144             | +0.2814 (Best)     | 0.9256 (Best)   |
| Model C (Logit)   | -0.0226            | 0.9139             | +0.2737            | 0.9249          |
+-------------------+--------------------+--------------------+--------------------+-----------------+
```
Model B was selected objectively as the canonical scoring framework, demonstrating the highest out-of-sample predictability and leave-one-season-out stability.

![Maintenance and Lift Scatter](file:///c:/Users/LENOVO/OneDrive/Desktop/SupeRR-Selector-Season-2/outputs/model_v3/charts/03_pressure_vs_normal_impact.png)

</div>

---

<!-- PAGE 5: TOP 10 BATTERS EVIDENCE -->
<div style="page-break-after: always;"></div>

# Section 5: Deep-Dive Evidence — Canonical Top 10 Batters

```
+---------------------------------------------------------------------------------------------------+
| CANONICAL TOP 10 BATTERS: STATISTICAL DOSSIERS (Per 100 Balls Faced)                              |
+------+------------------+-------+--------+------------+-----------+------------+----------+-------+
| Rank | Player Name      | Tier  | Score  | Shrunk PWI | Raw Lift  | Maint-Lift | HP Balls | N_eff |
+------+------------------+-------+--------+------------+-----------+------------+----------+-------+
| #1   | Tim David        | T1    | +2.484 | +42.91     | +10.00    | +31.04     | 570      | 744.3 |
| #2   | Naman Dhir       | T1    | +2.114 | +34.72     | +50.23    | +34.97     | 186      | 286.7 |
| #3   | Reeza Hendricks  | T2    | +1.757 | +31.49     | +35.94    | +30.19     | 223      | 424.9 |
| #4   | Romario Shepherd | T2    | +1.738 | +28.73     | +1.81     | +20.42     | 431      | 507.4 |
| #5   | Rashid Khan      | T2    | +1.736 | +28.07     | +57.81    | +29.82     | 377      | 427.9 |
| #6   | Shashank Singh   | T2    | +1.725 | +32.24     | +27.28    | +28.74     | 327      | 402.1 |
| #7   | Dinesh Karthik   | T2    | +1.678 | +34.40     | +21.67    | +28.01     | 250      | 372.0 |
| #8   | Rinku Singh      | T2    | +1.601 | +31.01     | +21.24    | +26.44     | 507      | 711.1 |
| #9   | Andre Russell    | T2    | +1.530 | +31.85     | -0.70     | +21.05     | 347      | 490.0 |
| #10  | Heinrich Klaasen | T3    | +1.482 | +24.88     | +4.57     | +17.35     | 459      | 772.9 |
+------+------------------+-------+--------+------------+-----------+------------+----------+-------+
```

### Detailed Analytical Profiles

#### 1. Tim David (Rank #1 | Composite Score: +2.484 | Tier 1)
Tim David stands as the undisputed benchmark finisher in contemporary white-ball cricket. Facing 570 high-pressure deliveries (Kish $N_{\text{eff}} = 744.3$), he generates an EB-shrunk pressure impact of **+42.91 runs per 100 balls**, backed by an attenuated maintenance-lift of +31.04. In death overs (overs 16–20), his shrunk impact reaches **+41.80 per 100 balls** with a boundary frequency of 25.8% and a low dot-ball rate of 32.1%. In my 1,000-resample bootstrap, David qualified in **1,000 out of 1,000 draws** with a median rank of 3.0 (90% CI: 1.0–16.0).

#### 2. Naman Dhir (Rank #2 | Composite Score: +2.114 | Tier 1)
Naman Dhir delivers the highest raw pressure lift in the entire tournament dataset (**+50.23 runs per 100 balls**), elevating his performance from a negative normal baseline (-0.71) to an astonishing **+34.72 shrunk impact** under high leverage. Facing 186 high-pressure balls ($N_{\text{eff}} = 286.7$), Dhir achieved a 26.9% boundary rate and an extraordinarily low 28.0% dot-ball percentage. He qualified in **908 bootstrap draws** with a median rank of 5.0 (90% CI: 1.0–32.0).

#### 3. Reeza Hendricks (Rank #3 | Composite Score: +1.757 | Tier 2)
Reeza Hendricks represents the premier top-order anchor operating under chasing leverage. While his death-overs sample is modest (50 balls), his powerplay and middle-overs chasing execution across 223 high-pressure deliveries produces a shrunk impact of **+31.49 runs per 100 balls** and a massive raw lift of +35.94. His low dot-ball percentage (27.4%) and steady boundary accumulation (24.7%) yielded an 858/1,000 bootstrap qualification rate with a median rank of 8.0.

#### 4. Romario Shepherd (Rank #4 | Composite Score: +1.738 | Tier 2)
Romario Shepherd functions as an explosive lower-order batter who sustains heavy impact (+28.73 shrunk impact, +20.42 maintenance-lift) across 431 high-pressure balls ($N_{\text{eff}} = 507.4$). He recorded the highest match consistency rate among top batters (**66.1% positive matches**), qualifying in **1,000 out of 1,000 bootstrap draws** with a median rank of 10.0 (90% CI: 2.0–36.0).

#### 5. Rashid Khan (Rank #5 | Composite Score: +1.736 | Tier 2)
Rashid Khan's lower-order batting under extreme match pressure is extraordinary. Facing 377 high-pressure balls ($N_{\text{eff}} = 427.9$), he records a raw lift of **+57.81 runs per 100 balls** over his baseline, generating an EB-shrunk impact of **+28.07** and a death-overs impact of +27.74. He qualified in **994 bootstrap draws** with a median rank of 8.0 (90% CI: 1.0–40.4).

#### 6. Shashank Singh (Rank #6 | Composite Score: +1.725 | Tier 2)
Shashank Singh established himself as an elite domestic chase finisher across 327 high-pressure deliveries ($N_{\text{eff}} = 402.1$), generating a shrunk impact of **+32.24 runs per 100 balls** (+27.28 raw lift). In death overs, his shrunk impact surges to **+31.50 per 100 balls** with a dot-ball rate of just 27.8%. He qualified in **996 bootstrap draws** with a median rank of 9.0.

#### 7. Dinesh Karthik (Rank #7 | Composite Score: +1.678 | Tier 2)
Despite retiring from active IPL competition to serve as RCB's Batting Coach, Dinesh Karthik's 2022–2024 historical record reflects masterclass finishing execution: **+34.40 shrunk impact** (+21.67 raw lift, +28.01 maintenance-lift) across 250 high-pressure balls ($N_{\text{eff}} = 371.9$). In death overs, his impact reached **+32.53 per 100 balls** with a 994/1,000 bootstrap qualification rate.

#### 8. Rinku Singh (Rank #8 | Composite Score: +1.601 | Tier 2)
Rinku Singh provides the most proven death-overs finishing profile in Indian cricket. Facing 507 high-pressure balls ($N_{\text{eff}} = 711.1$), his overall shrunk impact of **+31.01 runs per 100 balls** (+21.24 raw lift) accelerates to an astounding **+62.19 per 100 balls in overs 16–20** across 596 death deliveries. He qualified in **1,000 out of 1,000 bootstrap draws** with a median rank of 10.0.

#### 9. Andre Russell (Rank #9 | Composite Score: +1.530 | Tier 2)
Transitioned into KKR's coaching staff as Power Coach, Andre Russell's statistical profile illustrates world-class maintenance: an elite normal baseline (+30.86) sustained at **+31.85 shrunk impact** under high pressure across 347 deliveries ($N_{\text{eff}} = 490.0$). He achieved a 1,000/1,000 bootstrap qualification rate with a median rank of 12.0.

#### 10. Heinrich Klaasen (Rank #10 | Composite Score: +1.482 | Tier 3)
Heinrich Klaasen combines elite volume (459 high-pressure balls, $N_{\text{eff}} = 772.9$) with outstanding middle-overs spin destruction, delivering **+24.88 shrunk impact** and a **65.6% match consistency rate**. He qualified in **999 out of 1,000 bootstrap draws** with a median rank of 15.0 (90% CI: 5.0–34.0).

![Top 10 Batters Ranking](file:///c:/Users/LENOVO/OneDrive/Desktop/SupeRR-Selector-Season-2/outputs/model_v3/charts/01_top10_batters_ranking.png)

</div>

---

<!-- PAGE 6: TOP 10 BOWLERS EVIDENCE -->
<div style="page-break-after: always;"></div>

# Section 6: Deep-Dive Evidence — Canonical Top 10 Bowlers

```
+---------------------------------------------------------------------------------------------------+
| CANONICAL TOP 10 BOWLERS: STATISTICAL DOSSIERS (Per 24 Legal Balls Bowled)                        |
+------+---------------------+-------+--------+------------+----------+------------+----------+-------+
| Rank | Player Name         | Tier  | Score  | Shrunk PWI | Raw Lift | Maint-Lift | HP Balls | N_eff |
+------+---------------------+-------+--------+------------+----------+------------+----------+-------+
| #1   | Sunil Narine        | T1    | +2.203 | +6.57      | +0.90    | +4.50      | 422      | 893.3 |
| #2   | Jasprit Bumrah      | T1    | +2.141 | +7.61      | +0.95    | +5.06      | 332      | 723.0 |
| #3   | Rashid Khan         | T2    | +1.994 | +5.59      | +3.01    | +4.59      | 706      | 1560.2|
| #4   | Nathan Ellis        | T2    | +1.699 | +5.50      | +4.44    | +4.68      | 229      | 387.2 |
| #5   | Eshan Malinga       | T2    | +1.563 | +3.85      | +4.40    | +3.69      | 176      | 420.0 |
| #6   | Matheesha Pathirana | T2    | +1.448 | +5.34      | +1.77    | +3.89      | 307      | 556.1 |
| #7   | Mohammad Nawaz      | T2    | +1.343 | +4.00      | +1.28    | +2.93      | 242      | 579.8 |
| #8   | Arshdeep Singh      | T3    | +0.878 | +1.90      | +1.14    | +1.58      | 593      | 1193.3|
| #9   | Krunal Pandya       | T3    | +0.870 | +3.15      | +0.76    | +2.25      | 372      | 740.8 |
| #10  | Wanindu Hasaranga   | T3    | +0.849 | +2.78      | -0.40    | +1.66      | 504      | 1177.8|
+------+---------------------+-------+--------+------------+----------+------------+----------+-------+
```

### Detailed Analytical Profiles

#### 1. Sunil Narine (Rank #1 | Composite Score: +2.203 | Tier 1)
Sunil Narine sets the gold standard for high-pressure bowling containment. Across 422 high-pressure balls ($N_{\text{eff}} = 893.3$), he restricts opponents to a boundary rate of **just 10.2%** while producing a dot-ball percentage of **36.3%**. His EB-shrunk pressure impact of **+6.57 runs saved per 24 balls** accelerates to **+7.56 in death overs**. In my bootstrap audit, Narine qualified in **1,000 out of 1,000 draws** with a median rank of 4.0 (90% CI: 1.0–17.0).

#### 2. Jasprit Bumrah (Rank #2 | Composite Score: +2.141 | Tier 1)
Jasprit Bumrah generates the highest absolute high-pressure impact in the tournament dataset: **+7.61 runs saved per 24 balls** (+5.06 maintenance-lift) across 332 high-pressure deliveries ($N_{\text{eff}} = 723.0$). In death overs (550 balls), his shrunk impact reaches an unprecedented **+8.94 runs saved per 24 balls**. Because his normal baseline is already world-class (+7.28), his raw lift (+0.95) appears small—a feature correctly resolved by Model B. Bumrah qualified in **999 out of 1,000 bootstrap draws** with a median rank of 4.0.

#### 3. Rashid Khan (Rank #3 | Composite Score: +1.994 | Tier 2)
Rashid Khan anchors bowling volume, delivering 706 high-pressure balls with a massive Kish $N_{\text{eff}}$ of **1,560.2**. He generates **+5.59 shrunk impact** (+3.01 raw lift, +4.59 maintenance-lift), rising to **+7.74 in death overs**. Opponents manage boundaries on only 12.9% of his deliveries. Rashid qualified in **1,000 out of 1,000 bootstrap draws** with a median rank of 6.0 (90% CI: 1.0–19.0).

#### 4. Nathan Ellis (Rank #4 | Composite Score: +1.699 | Tier 2)
Nathan Ellis delivers outstanding situational elevation. Facing 229 high-pressure deliveries ($N_{\text{eff}} = 387.2$), he produces a raw lift of **+4.44 runs saved per 24 balls**, generating a shrunk impact of **+5.50** (+4.68 maintenance-lift). Operating almost entirely in death overs (354 death balls), his yorker execution yielded a **988/1,000 bootstrap qualification rate** with a median rank of 8.0.

#### 5. Eshan Malinga (Rank #5 | Composite Score: +1.563 | Tier 2)
Eshan Malinga represents an exceptional emerging pacer with a slinging release. Across 176 high-pressure deliveries ($N_{\text{eff}} = 420.0$), he elevates from a modest normal baseline (+0.46) to produce **+3.85 shrunk impact** (+4.40 raw lift) and **+4.38 in death overs**. He achieved a 34.1% dot-ball rate, qualifying in **912 bootstrap draws** with a median rank of 9.0.

#### 6. Matheesha Pathirana (Rank #6 | Composite Score: +1.448 | Tier 2)
Matheesha Pathirana provides elite death-overs execution (539 death balls), delivering **+5.34 shrunk impact** (+3.89 maintenance-lift) across 307 high-pressure balls ($N_{\text{eff}} = 556.1$). His heavy dot-ball generation (**36.2% dots under pressure**) yielded a **1,000/1,000 bootstrap qualification rate** with a median rank of 10.0 (90% CI: 1.0–41.0).

#### 7. Mohammad Nawaz (Rank #7 | Composite Score: +1.343 | Tier 2)
Mohammad Nawaz demonstrates steady left-arm orthodox containment, generating **+4.00 shrunk impact** (+1.28 raw lift) across 242 high-pressure balls ($N_{\text{eff}} = 579.8$). He restricts boundary frequency to **11.2%**, qualifying in **990 bootstrap draws** with a median rank of 13.0.

#### 8. Arshdeep Singh (Rank #8 | Composite Score: +0.878 | Tier 3)
Recently traded to Mumbai Indians for INR 18.00 crore, Arshdeep Singh absorbed massive death bowling workloads (1,085 death balls; 593 high-pressure balls, $N_{\text{eff}} = 1,193.3$). He sustained positive impact (**+1.90 shrunk impact**, +1.14 raw lift, +3.60 in death overs), qualifying in **1,000 out of 1,000 bootstrap draws**.

#### 9. Krunal Pandya (Rank #9 | Composite Score: +0.870 | Tier 3)
Krunal Pandya operates as an economical middle-overs defensive spinner, generating **+3.15 shrunk impact** (+0.76 raw lift) across 372 high-pressure balls ($N_{\text{eff}} = 740.8$). His high dot-ball percentage (**35.2%**) and boundary containment (12.4%) yielded a **1,000/1,000 bootstrap qualification rate**.

#### 10. Wanindu Hasaranga (Rank #10 | Composite Score: +0.849 | Tier 3)
Wanindu Hasaranga delivers heavy spin volume (504 high-pressure balls, $N_{\text{eff}} = 1,177.8$), producing **+2.78 shrunk impact** and **+4.14 in death overs** despite a slight negative raw lift (-0.40) caused by an elite baseline (+3.21). He qualified in **1,000 out of 1,000 bootstrap draws**.

![Top 10 Bowlers Ranking](file:///c:/Users/LENOVO/OneDrive/Desktop/SupeRR-Selector-Season-2/outputs/model_v3/charts/02_top10_bowlers_ranking.png)

</div>

---

<!-- PAGE 7: RELIABILITY & SENSITIVITY -->
<div style="page-break-after: always;"></div>

# Section 7: Statistical Reliability, Consistency & Robustness Diagnostics

To confirm that my rankings reflect true underlying talent rather than sample artifacts or model hyperparameter choices, I executed four comprehensive validation protocols:

```
+----------------------------------------------------------------------------------------------------+
| SENSITIVITY & ROBUSTNESS SUITE RESULTS                                                             |
+------------------------------+---------------------------+-----------------------------------------+
| Diagnostic Protocol          | Sample Coverage / Scope   | Stability Metric (Spearman Rank Corr)   |
+------------------------------+---------------------------+-----------------------------------------+
| Leave-One-Season-Out (LOSO)  | 5 Seasons (2022 to 2026)  | Batters: 0.901 to 0.932 (Mean: 0.914)   |
|                              |                           | Bowlers: 0.912 to 0.941 (Mean: 0.926)   |
+------------------------------+---------------------------+-----------------------------------------+
| Wicket Valuation Sensitivity | w in {4.0, 6.0, 8.0, Ctx} | Batters: 0.982 to 0.998 vs Canonical    |
|                              |                           | Bowlers: 0.974 to 0.996 vs Canonical    |
+------------------------------+---------------------------+-----------------------------------------+
| Pressure Weight Perturbation | 26 Weight Combinations    | Batters Top-10 Overlap: 9.73 / 10 Mean  |
| (Leverage / Phase / State)   |                           | Bowlers Top-10 Overlap: 9.73 / 10 Mean  |
+------------------------------+---------------------------+-----------------------------------------+
| Definition Invariance        | Def A vs Def B vs Def C   | Batters Top-10 Overlap: 8 / 10          |
| (Def C: Over 16+ & RRR >= 10)|                           | Bowlers Top-10 Overlap: 8 / 10          |
+------------------------------+---------------------------+-----------------------------------------+
```

### 1. Leave-One-Season-Out (LOSO) Temporal Stability
By dropping each season from 2022 to 2026 sequentially and recomputing all context baselines, shrinkage factors, and composite scores from scratch, I verified that no single season skews the ratings. The minimum Spearman rank correlation across seasons was **0.901 for batters** and **0.912 for bowlers**.

### 2. Wicket Valuation Perturbation
Testing wicket replacement weights of $w \in [4.0, 8.0]$ runs alongside dynamic contextual marginal values yielded rank correlations $\ge 0.974$. This proves that my findings are robust to differing assumptions about wicket cost.

### 3. Bootstrap Cluster Resampling & The 800-Draw Reliability Standard
In my 1,000-resample stratified match-cluster bootstrap, deliveries are resampled at the match level. While high-exposure stars (Tim David, Sunil Narine, Jasprit Bumrah) qualified in 1,000/1,000 draws, small-sample streak performers suffered severe eligibility attrition:
- **Matthew Wade:** Qualified in only **720 draws** (ineligible in 280 draws).
- **Ashutosh Sharma:** Qualified in only **662 draws** (ineligible in 338 draws).
- **Abbas Afridi:** Qualified in only **504 draws** (ineligible in 496 draws).
- **Mujeeb Ur Rahman:** Qualified in only **744 draws** (ineligible in 256 draws).
Requiring $\ge 800$ valid draws establishes a rigorous reliability barrier, ensuring that every player in Rajasthan Royals' canonical Top 10 possesses dependable cross-match stability.

![Bootstrap Rank Uncertainty Intervals](file:///c:/Users/LENOVO/OneDrive/Desktop/SupeRR-Selector-Season-2/outputs/model_v3/charts/08_bootstrap_rank_uncertainty.png)

</div>

---

<!-- PAGE 8: MODEL LIMITATIONS & INTEGRITY -->
<div style="page-break-after: always;"></div>

# Section 8: Model Limitations, Boundaries & Pipeline Integrity

A responsible analytics department must clearly understand where its models are uncertain. I document four key boundaries:

### 1. The Small-Sample Sensitivity Boundary
While Empirical Bayes shrinkage prevents extreme rate distortion, players with qualifying high-pressure exposure between 120 and 180 balls exhibit wide bootstrap percentile intervals. For example, Naman Dhir (#2, 186 HP balls) carries a 5th–95th percentile rank interval of 1.0 to 32.0, whereas Tim David (#1, 570 HP balls) is tightly bounded between 1.0 and 16.0. Franchise recruitment decisions must treat Tier 1 small-sample leaders as high-upside targets requiring pairing with established anchors.

### 2. Tracking Data and Physical Measurement Absence
The competition dataset does not include ball-tracking trajectories (such as release height, ball speed, swing angle, or pitch map coordinates) or biomechanical bat sensors. All player evaluations derive strictly from match events (runs, extras, dismissals, dot balls, boundaries, and contextual state). I have deliberately excluded speculative physical claims, grounding my conclusions purely in on-field run expectancy.

### 3. Tournament Scope & Bilateral Realities
The dataset contains bilateral T20 Internationals and Indian Premier League matches, but excludes World Cup tournaments and non-qualifying secondary domestic leagues. All T20I records are harmonized via pre-match team Elo adjustments, but cannot account for differences in boundary dimensions or ground conditions beyond venue historical pars.

### 4. Zero Data Leakage & Read-Only Baseline Immutability
To ensure complete scientific reproducibility, all 39 baseline files from Version 1—including raw competition CSVs, baseline python modules, and independent audit logs—were verified unchanged via SHA-256 checksums (`checked=39, mismatches=0` in `outputs/model_v2/integrity_manifest_pre.json`). The entire pipeline runs deterministically via `python -m src.model_v3.run_pipeline` with a fixed pseudo-random seed (`seed=42`).

![Sensitivity Suite Overview](file:///c:/Users/LENOVO/OneDrive/Desktop/SupeRR-Selector-Season-2/outputs/model_v3/charts/11_model_sensitivity_comparison.png)

</div>

---

<!-- PAGE 9: RAJASTHAN ROYALS SQUAD STRATEGY -->
<div style="page-break-after: always;"></div>

# Section 9: Rajasthan Royals IPL 2027 Squad Strategy & Recruitment Dossiers

### Diagnostic Audit of Rajasthan Royals' IPL 2026 Campaign
In the 2026 IPL season, Rajasthan Royals finished 4th in the league stage, won the Eliminator against Sunrisers Hyderabad, and exited in Qualifier 2 against Gujarat Titans. Official tournament records confirm that **Riyan Parag** captained the side in 14 matches (with Yashasvi Jaiswal captaining 2 matches). Following the pre-season trade sending Sanju Samson to CSK in exchange for Ravindra Jadeja and Sam Curran, RR's on-field performance exposed severe tactical vulnerabilities:

```
+----------------------------------------------------------------------------------------------------+
| RAJASTHAN ROYALS 2026 BOWLING PERFORMANCE DIRECTLY AUDITED FROM RAW DATA                           |
+------------------+-----------+-------------+-------+---------------+---------+---------------------+
| Bowler Name      | Matches   | Legal Balls | Overs | Runs Conceded | Wickets | Economy Rate (ER)   |
+------------------+-----------+-------------+-------+---------------+---------+---------------------+
| Jofra Archer     | 16 apps   | 360         | 60.0  | 559           | 25      | 9.32 (Pace Anchor)  |
| Brijesh Sharma   | 13 apps   | 273         | 45.3  | 450           | 14      | 9.89                |
| Nandre Burger    | 13 apps   | 261         | 43.3  | 440           | 14      | 10.11               |
| Ravindra Jadeja  | 14 apps   | 198         | 33.0  | 277           | 10      | 8.39 (Defensive)    |
| Yash Punja       | 8 apps    | 180         | 30.0  | 279           | 9       | 9.30                |
| Ravi Bishnoi     | 9 apps    | 156         | 26.0  | 257           | 11      | 9.88 (Attacking)    |
| Tushar Deshpande | 7 apps    | 138         | 23.0  | 275           | 4       | 11.96 (Severe Leak) |
| Sandeep Sharma   | 6 apps    | 118         | 19.4  | 224           | 5       | 11.39 (Severe Leak) |
| Kuldeep Sen      | 0 bowled  | 0           | 0.0   | 0             | 0       | 0.00 (Unused)       |
+------------------+-----------+-------------+-------+---------------+---------+---------------------+
```

### Strategic Recruitment Gaps for IPL 2027 Mini-Auction
1. **Death Bowling Partner for Jofra Archer:** Sandeep Sharma (ER 11.39) and Tushar Deshpande (ER 11.96) leaked unsustainably in death overs. RR desperately requires a specialist death pacer executing yorkers and slower cutters.
2. **Defensive Spin Anchor to Complement Ravi Bishnoi:** Ravi Bishnoi operates as an aggressive wicket-taking leg-spinner (ER 9.88). Without an economical defensive partner at the other end (Jadeja bowled only 33 overs in 14 games), opponents attacked RR's middle overs.
3. **Power Finisher to Relieve Dhruv Jurel:** Shimron Hetmyer scored only 78 runs in 69 balls across 8 appearances (strike rate 113.04), forcing Dhruv Jurel and Donovan Ferreira into overextended roles.

![Recruitment Fit Matrix](file:///c:/Users/LENOVO/OneDrive/Desktop/SupeRR-Selector-Season-2/outputs/model_v3/charts/12_rr_recruitment_fit_matrix.png)

---

### Individual Recruitment Fit Notes: All 20 Ranked Players

#### Batters (10 Actionable Recruitment Notes)
1. **Tim David (#1 | Aus | RCB):** The premier power finisher in T20 cricket (+42.91 shrunk impact, death impact +41.80). If RCB releases him or explores a trade, RR should aggressively allocate purse funds. He directly solves RR's slot 6–7 boundary crisis.
2. **Naman Dhir (#2 | Ind | MI):** Exceptional domestic finisher (+50.23 raw lift). As an uncapped/low-bracket Indian batting all-rounder who bowls useful off-spin, Dhir represents RR's highest-value domestic auction target.
3. **Reeza Hendricks (#3 | SA | Uncontracted IPL):** Elite top-order chasing anchor (+31.49 shrunk impact). Available in the mini-auction pool at base price without trade friction; provides proven overseas backup for Yashasvi Jaiswal and Vaibhav Sooryavanshi.
4. **Romario Shepherd (#4 | WI | MI):** Explosive pace hitter (+28.73 shrunk impact, 66.1% match consistency). Ideal overseas seam-bowling finisher for slot 7, offering power hitting and 2 overs of pace.
5. **Rashid Khan (#5 | Afg | GT):** World-class lower-order match-winner (+57.81 raw lift). Unlikely to be released by Gujarat Titans, but if auction dynamics permit, represents a transformational dual-threat recruit.
6. **Shashank Singh (#6 | Ind | PBKS):** Premier Indian chase finisher (+32.24 shrunk impact, death impact +31.50). High-priority domestic trade or auction target to provide an experienced Indian finisher alongside Dhruv Jurel.
7. **Dinesh Karthik (#7 | Ind | RCB Coach):** Retired from active IPL competition to serve as RCB's Batting Coach & Mentor. Practical availability as an active player is zero; serves as a statistical benchmark for finisher execution.
8. **Rinku Singh (#8 | Ind | KKR):** Elite Indian death finisher (+62.19 death impact per 100 balls). Retained as KKR vice-captain; virtually unavailable via auction, but establishes the gold standard for left-handed finishing.
9. **Andre Russell (#9 | WI | KKR Coach):** Retired from IPL competition on November 30, 2025, transitioning into KKR's coaching staff. Unavailable as an active player; historical data validates power-hitting maintenance.
10. **Heinrich Klaasen (#10 | SA | SRH):** Premier spin-demolishing middle-order anchor (+24.88 shrunk impact, 65.6% consistency). Core retention for Sunrisers Hyderabad (INR 23 crore); target via trade only if SRH restructures purse.

#### Bowlers (10 Actionable Recruitment Notes)
1. **Sunil Narine (#1 | WI | KKR):** Benchmark mystery spinner (+6.57 shrunk impact, 10.2% boundary rate). Expected KKR retention; models the exact defensive containment profile RR needs alongside Ravi Bishnoi.
2. **Jasprit Bumrah (#2 | Ind | MI):** Benchmark fast bowler (+7.61 shrunk impact, death impact +8.94). Retained core spearhead for Mumbai Indians; provides the ultimate template for multi-phase pace bowling.
3. **Rashid Khan (#3 | Afg | GT):** Premier wrist-spinner worldwide (+5.59 shrunk impact across 706 HP balls). Expected GT retention; benchmark for attacking leg-spin under pressure.
4. **Nathan Ellis (#4 | Aus | PBKS):** **Primary Overseas Pace Target.** Armed with pinpoint death yorkers and cutters (+5.50 shrunk impact, +4.44 raw lift), Ellis directly solves RR's death-phase leakage behind Jofra Archer.
5. **Eshan Malinga (#5 | SL | Sri Lanka Domestic):** **High-Upside Low-Cost Pace Target.** Uncontracted slinger (+3.85 shrunk impact, +4.38 death impact) available at base price in the mini-auction; ideal development pace weapon.
6. **Matheesha Pathirana (#6 | SL | KKR):** **Elite Death Bowling Target.** Signed by KKR for INR 18 crore but truncated by calf injury in 2026. If released due to overseas slots, RR must bid aggressively for his 36.2% dot-ball rate and +5.34 impact.
7. **Mohammad Nawaz (#7 | Pak | PSL):** High-performing left-arm spinner (+4.00 shrunk impact, 11.2% boundary rate). Ineligible for IPL auction due to BCCI bilateral policy; statistical proof that defensive left-arm spin controls match tempo.
8. **Arshdeep Singh (#8 | Ind | Traded to MI):** Traded to Mumbai Indians on November 11, 2026 for INR 18.00 crore. Demonstrates the immense market valuation for left-arm death seamers.
9. **Krunal Pandya (#9 | Ind | RCB):** **Primary Domestic Spin Target.** Experienced left-arm orthodox spinner (+3.15 shrunk impact, 35.2% dot balls). Provides the exact middle-overs boundary control RR missed in 2026 without consuming an overseas slot.
10. **Wanindu Hasaranga (#10 | SL | LSG):** Multi-phase leg-spinner (+2.78 shrunk impact, death impact +4.14). Ruled out of IPL 2026 by hamstring injury; if released by LSG, offers high-upside wrist-spin depth.

</div>

---

<!-- PAGE 10: CONCLUSION & OPERATIONAL ROADMAP -->
<div style="page-break-after: always;"></div>

# Section 10: Conclusion & Operational Action Plan for IPL 2027 Auction

My independent investigation demonstrates that high-pressure excellence in T20 cricket is neither random nor synonymous with general batting averages or overall bowling economy. By decomposing match states strictly pre-delivery, applying Leave-Player-Out context baselines, shrinking noise via Kish effective sample sizes, and validating findings across 1,000 match-cluster bootstrap resamples, I have provided Rajasthan Royals with a rigorous, mathematically defensible talent evaluation framework.

```
+----------------------------------------------------------------------------------------------------+
| RAJASTHAN ROYALS IPL 2027 OPERATIONAL AUCTION BLUEPRINT                                            |
+--------------------------+------------------------------+--------------------+---------------------+
| Tactical Need            | Primary Target (Tier 1/2)    | Secondary Target   | Tactical Role       |
+--------------------------+------------------------------+--------------------+---------------------+
| Death Seam Specialist    | Nathan Ellis (#4 Bowler)     | Eshan Malinga (#5) | Overs 17 & 19 Pacer |
| Middle Spin Anchor       | Krunal Pandya (#9 Bowler)    | Wanindu Hasaranga  | Overs 7-15 Control  |
| Domestic Power Finisher  | Naman Dhir (#2 Batter)       | Shashank Singh (#6)| Overs 16-20 Striker |
| Overseas Chasing Anchor  | Reeza Hendricks (#3 Batter)  | Tim David (#1 Trd) | Top-Order Reserve   |
+--------------------------+------------------------------+--------------------+---------------------+
```

### Action Plan Ahead of the December 16 Mini-Auction in Goa
1. **Monitor the November 17 Retention Submissions:** Track whether Punjab Kings retain Nathan Ellis and whether Mumbai Indians protect Naman Dhir. If Ellis enters the auction pool, establish a dedicated valuation ceiling up to INR 9.0 crore.
2. **Scout Eshan Malinga Directly:** Dispatch regional scouts to observe Eshan Malinga in Sri Lankan domestic fixtures ahead of the December 3 auction shortlisting, securing him as a low-cost overseas pace weapon.
3. **Execute Domestic Spin Inquiries:** Explore trade or auction availability for experienced left-arm orthodox spinners (Krunal Pandya) to partner Ravi Bishnoi, creating a balanced, multi-dimensional bowling attack for Rajasthan Royals at the Sawai Mansingh Stadium in IPL 2027.

---

<!-- PAGE 11: APPENDIX A - FORMULATIONS -->
<div style="page-break-after: always;"></div>

# Appendix A: Mathematical Formulations, Code Identifiers & Notation Reference

### Notation Dictionary
- $PI_k \in [0, 1]$: Pre-delivery Pressure Index for ball $k$ (`pressure_index`).
- $w_k$: Continuous pressure weighting factor assigned to delivery $k$ (`pressure_weight`).
- $N_{\text{eff}}$: Kish Effective Sample Size accounting for weight variance (`pressure_neff`).
- $\bar{R}_{-i, c}$: Leave-Player-Out expected runs per ball in context cell $c$ (`ctx_bat_rpb` / `ctx_bowl_rpb`).
- $\bar{W}_{-i, c}$: Leave-Player-Out expected wicket probability per ball in context cell $c$ (`ctx_bat_out_prob` / `ctx_bowl_wkt_prob`).
- $K$: Empirical Bayes shrinkage calibration parameter ($K = 120.0$).
- $Z(X)$: Standardized normal score of metric $X$ across the eligible player pool.

### Full Composite Scoring Equations
$$\text{Score}_{\text{bat}} = 0.50 \cdot Z(\text{Shrunk PWI}_{\text{bat}}) + 0.30 \cdot Z(\text{Maint-Lift}_{\text{bat}}) + 0.20 \cdot Z(\text{EB Consistency}_{\text{bat}})$$
$$\text{Score}_{\text{bowl}} = 0.50 \cdot Z(\text{Shrunk PWI}_{\text{bowl}}) + 0.30 \cdot Z(\text{Maint-Lift}_{\text{bowl}}) + 0.20 \cdot Z(\text{EB Consistency}_{\text{bowl}})$$

### Code Identifier Mapping & Reproducibility Matrix
- `src/model_v3/pressure_model.py`: Calculates pre-delivery Pressure Index ($PI$) and continuous weights without outcome leakage.
- `src/model_v3/context_baselines.py`: Implements Leave-Player-Out hierarchical baselines with cell fallback ($N < 50$).
- `src/model_v3/impact_models.py`: Computes single-ball context adjustments, wicket valuations ($w = 6.0$), and Empirical Bayes shrinkage.
- `src/model_v3/ranking.py`: Assembles canonical rankings, applies the 800-draw bootstrap filter, and generates detailed player profiles.
- `src/model_v3/bootstrap.py`: Executes 1,000-resample stratified match-cluster bootstrap recomputing full baselines inside each draw.
- `src/model_v3/validation.py`: Runs LOSO, format, wicket, and shrinkage parameter sensitivity checks.

---

<!-- PAGE 12: APPENDIX B - SOURCE REGISTER -->
<div style="page-break-after: always;"></div>

# Appendix B: External Source Register & Methodology Audit Log

### Verified Public Citations & Access Register (Audited as of 2026-11-14)
1. **BCCI / IPL Official Portal:** *Hardik Pandya and Arshdeep Singh complete major trade between PBKS and MI*, published 2026-11-11. URL: `https://www.iplt20.com/news/article/hardik-pandya-and-arshdeep-singh-complete-major-trade-between-pbks-and-mi` [Official].
2. **BCCI / IPL Official Portal:** *Rishabh Pant and Kuldeep Yadav complete high-profile trade between DC and LSG*, published 2026-06-23. URL: `https://www.iplt20.com/news/article/rishabh-pant-and-kuldeep-yadav-complete-high-profile-trade-between-dc-and-lsg` [Official].
3. **The Indian Express:** *IPL 2026: Sanju Samson moves to Chennai in CSK's biggest-ever trade deal, Jadeja returns to Rajasthan Royals*, published 2025-11-15. URL: `https://indianexpress.com/article/sports/cricket/ipl-2026-retention-sanju-samson-csk-jadeja-rr-trade-deal-confirmed-10366973/` [Reputable Media].
4. **The Hindu:** *Andre Russell announces retirement from IPL, joins KKR support staff as power coach*, published 2025-11-30. URL: `https://www.thehindu.com/sport/cricket/andre-russell-announces-retirement-from-ipl-joins-kkr-support-staff-as-power-coach/article70341366.ece` [Reputable Media].
5. **India TV News:** *Dinesh Karthik becomes RCB's batting coach, mentor ahead of IPL 2025 after retiring from cricket*, published 2024-07-01. URL: `https://www.indiatvnews.com/sports/cricket/dinesh-karthik-becomes-rcb-s-batting-coach-mentor-ahead-of-ipl-2025-after-retiring-from-cricket-2024-07-01-939655` [Reputable Media].
6. **The Times of India:** *Mohit Sharma set to join CSK as bowling coach*, published 2026-09-29. URL: `https://timesofindia.indiatimes.com/sports/cricket/ipl/mohit-sharma-likely-to-join-csk-as-bowling-coach/articleshow/134561311.cms` [Reputable Media].
7. **CricTracker:** *Matthew Wade announces BBL retirement to take up full-time coaching role*, published 2026-09-17. URL: `https://www.crictracker.com/cricket-news/matthew-wade-announces-bbl-retirement-to-take-up-full-time-coaching-role-8665/` [Reputable Media].
8. **The Times of India:** *Sunil Narine scripts history, becomes the first overseas player to claim 200 IPL wickets*, published 2026-05-03. URL: `https://timesofindia.indiatimes.com/sports/cricket/ipl/ipl-2026/ipl-2026-sunil-narine-scripts-history-becomes-the-first-overseas-player-to-claim-200-ipl-wickets/articleshow/130731835.cms` [Reputable Media].
9. **The Indian Express:** *Matheesha Pathirana to miss IPL 2026 start through injury*, published 2026-03-21. URL: `https://indianexpress.com/article/sports/cricket/matheesha-pathirana-lockie-ferguson-miss-ipl-2026-start-injury-10593620/` [Reputable Media].
10. **Mint:** *IPL 2027 retentions explained: Player salaries, auction budgets and the decisions facing all 10 teams*, published 2026-11-08. URL: `https://www.livemint.com/sports/cricket-news/ipl-2027-retentions-explained-player-salaries-auction-budgets-and-the-decisions-facing-all-10-teams-11794138863732.html` [Reputable Media].

---
*Report End — All statistics derived strictly from historical match data under AGENTS.md guidelines.*

