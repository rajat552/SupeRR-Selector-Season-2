# SupeRR Selector Season 2 — Round 1 Methodology Report
**Identifying the Most Reliable Batters and Bowlers Under Pressure (IPL & T20I, 2022–2026)**

---

## 1. Executive Summary & Final Rankings

Using 193,988 delivery-level records across 837 completed IPL (367) and T20I (470) matches from January 2022 to November 2026, we built a zero-look-ahead **Pressure Index ($PI_t \in [0, 1]$)** and evaluated every player's **context-adjusted performance under high pressure ($PI_t \ge 0.50$)** against their own **normal/low-pressure baseline ($PI_t < 0.35$)**, stabilized via **Empirical Bayes shrinkage** ($k = 120$ balls) and weighted by **cross-match consistency**.

### Top 10 Batters Under Pressure (Unstop Rank Order)
| Rank | Player ID | Player Name | Tot Balls | HP Balls | HP Matches | HP SR | LP SR | HP Impact / 100 | LP Impact / 100 | Shrunk $\Delta$ | Consistency | Pressure Score |
|---:|---:|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| **1** | 768 | **Reeza Hendricks** | 835 | 223 | 15 | 170.9 | 129.9 | +47.3 | +6.3 | +26.7 | 85.7% | **2.30** |
| **2** | 796 | **Matthew Wade** | 427 | 158 | 12 | 158.2 | 127.7 | +40.6 | -9.3 | +28.4 | 70.0% | **1.67** |
| **3** | 37052 | **Naman Dhir** | 515 | 186 | 18 | 179.0 | 159.8 | +29.6 | -8.1 | +22.9 | 73.3% | **1.30** |
| **4** | 6396 | **Tim David** | 1226 | 570 | 48 | 180.2 | 187.4 | +42.3 | +47.2 | -4.1 | 74.2% | **1.26** |
| **5** | 2258 | **Sanju Samson** | 2232 | 178 | 15 | 179.8 | 151.8 | +32.9 | +13.1 | +11.8 | 70.0% | **0.95** |
| **6** | 6288 | **Shubman Gill** | 2711 | 133 | 12 | 169.2 | 147.0 | +39.8 | +14.4 | +13.4 | 62.5% | **0.92** |
| **7** | 3374 | **Mark Chapman** | 873 | 334 | 21 | 144.9 | 149.5 | +27.9 | +14.0 | +10.3 | 68.8% | **0.91** |
| **8** | 838 | **Glenn Maxwell** | 958 | 260 | 24 | 168.8 | 155.0 | +27.2 | +6.3 | +14.3 | 57.1% | **0.74** |
| **9** | 4369 | **Shai Hope** | 1105 | 128 | 12 | 169.5 | 142.2 | +33.2 | +16.5 | +8.6 | 66.7% | **0.65** |
| **10** | 3024 | **Mohammad Rizwan** | 1152 | 147 | 11 | 153.7 | 122.2 | +19.7 | +13.7 | +3.3 | 85.7% | **0.51** |

### Top 10 Bowlers Under Pressure (Unstop Rank Order)
| Rank | Player ID | Player Name | Tot Balls | HP Balls | HP Matches | HP ER | LP ER | HP WAP / 24 | HP Impact / 24 | LP Impact / 24 | Shrunk $\Delta$ | Consistency | Pressure Score |
|---:|---:|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| **1** | 34485 | **Sufiyan Muqeem** | 344 | 148 | 12 | 5.11 | 8.03 | +1.09 | +19.7 | -1.2 | +11.5 | 81.8% | **2.35** |
| **2** | 5577 | **Sai Kishore** | 465 | 123 | 11 | 6.98 | 10.34 | +1.18 | +17.3 | -4.4 | +10.9 | 100.0% | **2.26** |
| **3** | 781 | **Sunil Narine** | 1530 | 454 | 35 | 5.88 | 7.48 | -0.05 | +12.4 | +3.5 | +7.1 | 93.1% | **1.82** |
| **4** | 2490 | **Mohammad Nawaz** | 1004 | 282 | 26 | 6.38 | 7.82 | +0.91 | +12.9 | +0.2 | +9.0 | 72.7% | **1.58** |
| **5** | 2878 | **Mohit Sharma** | 649 | 277 | 21 | 8.64 | 11.00 | +0.83 | +9.4 | -8.0 | +12.1 | 66.7% | **1.48** |
| **6** | 4373 | **Mustafizur Rahman** | 1576 | 500 | 40 | 6.72 | 8.54 | +0.00 | +9.8 | -1.6 | +9.2 | 69.4% | **1.36** |
| **7** | 3644 | **Kuldeep Yadav** | 1914 | 642 | 50 | 7.22 | 8.79 | +0.51 | +9.7 | -0.3 | +8.4 | 71.4% | **1.34** |
| **8** | 2933 | **Jasprit Bumrah** | 1708 | 496 | 43 | 6.76 | 7.32 | +0.24 | +12.3 | +5.7 | +5.3 | 76.9% | **1.31** |
| **9** | 4101 | **Mitchell Santner** | 1737 | 515 | 37 | 6.79 | 8.19 | +0.33 | +9.0 | -0.7 | +7.9 | 78.8% | **1.28** |
| **10** | 5979 | **Abrar Ahmed** | 764 | 309 | 24 | 5.30 | 8.03 | -0.06 | +11.9 | +1.3 | +7.6 | 66.7% | **1.21** |

---

## 2. Data Scope, Cleaning & Integrity Controls
1. **Competition Filtering:** Excluded 30 non-IPL `T20` A-team matches (`Mens T20 Emerging Teams Asia Cup 2024` and `Asia Cup Rising Stars 2025`), 16 abandoned matches with 0 deliveries, and 38 Super Over balls (`innings` 3–4), leaving **837 matches** (367 IPL, 470 T20I) and **193,988 deliveries**.
2. **Player Identity Disambiguation:** All joins and aggregations key strictly on `player_id`, preventing homonym collisions (e.g., Indian IPL batter `Abdul Samad` `7446` vs Pakistani `Abdul Samad` `6922`; Afghanistan/GT `Rashid Khan` `4722` vs Nepal `Rashid Khan` `20172`).
3. **Extras, Legal Balls & Wickets:**
   - `wide` (7,714): non-legal, excluded from batter balls faced and bowler legal balls.
   - `Overstep` (576) & `other` (264): no-balls (non-legal for bowler overs, batter runs counted).
   - Bowler runs conceded = `runs` + `wide`/`noball` extras (excluding byes/legbyes/penalty).
   - Bowler wickets = `Caught`, `Bowled`, `LBW`, `Stump`, `Hit Wicket` only (team wickets include all dismissals for match state).
   - `first_inn_revised_overs` / `second_inn_revised_overs` (stored in balls) are used directly as `inn_max_balls` for D/L-reduced games.

---

## 3. Pressure Definition ($PI_t \in [0, 1]$)
Every delivery $t$ is scored using **strictly pre-delivery state** (runs, wickets, legal balls remaining before ball $t$):
- **2nd Innings (Chases):** Combines Required Run Rate ratio ($RRR_t / \text{ParRPO}$), wickets lost when $>10$ runs remain, and late-innings urgency, with **dead-chase damping** when a game is already won ($RRR/\text{Par} < 0.55$, $\ge 5$ wkts in hand) or effectively lost ($RRR/\text{Par} > 2.20$, $>18$ balls left).
- **1st Innings (Setting a Target):** Combines **collapse pressure** (wickets lost above expected wickets at that over, plus early Powerplay collapse boost), **scoring-rate deficit** ($\text{ParRPO} - CRR_t$ after over 3), and **death-over execution**.
- **Calibration:** At $PI_t \ge 0.50$, **26.8%** of deliveries are high-pressure (17.2% of 1st-innings balls, 37.5% of 2nd-innings balls; only 44.4% of death overs qualify, separating genuine tension from routine death overs). Low-pressure baseline is $PI_t < 0.35$ (59.3% of balls).

---

## 4. Performance Measurement, Baselines & Fair Comparisons
1. **Context-Adjusted Residuals:** Every delivery is centered against the exact `(comp_tier, season_year, phase)` par (`IPL`, `T20I_Full`, `T20I_Assoc` × `2022–2026` × `Powerplay/Middle/Death`), neutralizing IPL vs T20I scoring gaps and 2022–2026 run inflation.
2. **Batting Impact per 100 Balls:** $\text{Impact}_{100} = \text{RAE}_{100} + 6.0 \times \text{SurvAbovePar}_{100}$.
3. **Bowling Impact per 24 Balls:** $\text{Impact}_{24} = 4.0 \times \text{RSO} + 6.0 \times \text{WAP}_{24}$.
4. **Eligibility Gates:** $\ge 300$ total balls, $\ge 120$ high-pressure balls ($\ge 80$ in IPL/Full-Member T20I), $\ge 10$ high-pressure matches, $\ge 60$ low-pressure balls, and positive absolute high-pressure impact (yields **54 eligible batters** and **92 eligible bowlers**).
5. **Composite Score:**
   $$\text{Score} = 0.40\,z(\Delta_{\text{shrunk}}) + 0.40\,z(\text{HP Impact}_{\text{shrunk}}) + 0.20\,z(\text{Consistency Rate})$$
   where $w = n_{\text{HP}} / (n_{\text{HP}} + 120)$ shrinks small-sample extremes and low-pressure baselines are floored to prevent negative-baseline distortion.

---

## 5. Visual Evidence & Validation Results
- Charts generated in `outputs/charts/`:
  - `top10_batters_impact.png` & `top10_bowlers_impact.png`
  - `top10_batters_bootstrap.png` & `top10_bowlers_bootstrap.png`
- **Competition-Scope Sensitivity (`IPL + Full-Member T20I only` vs `All`):**
  - Batters: **10/10** Top-10 overlap, Spearman $\rho = 0.9925$.
  - Bowlers: **9/10** Top-10 overlap, Spearman $\rho = 0.9841$.
- **Threshold Sensitivity (`0.45`, `0.50`, `0.55`):**
  - Batters Spearman $\rho = 0.878$ (`0.45`) and $0.851$ (`0.55`).
  - Bowlers Spearman $\rho = 0.916$ (`0.45`) and $0.919$ (`0.55`).
- **Match-Level Bootstrap (300 Resamples):** Top-ranked players such as Reeza Hendricks (81.3% P(Top 10), median rank 3), Matthew Wade (71.3%, median 5), Sai Kishore (81.3%, median 5), Sufiyan Muqeem (67.0%, median 4), and Sunil Narine (64.7%, median 8) show strong rank stability.

---

## 6. Limitations & Separate Recruitment Context
- **Limitations:** `bowl_speed` is `0.0` on 38.74% of balls and was excluded from the core score; fielding/dropped catches are not in the data; bootstrap CIs widen for players near Ranks 8–10 with 120–150 HP balls.
- **Recruitment Note (Separate from Statistical Ranking):** Uncapped/emerging IPL targets like **Naman Dhir** (#3 batter) and **Sai Kishore** (#2 bowler), alongside proven IPL match-winners **Tim David**, **Sanju Samson**, **Shubman Gill**, **Sunil Narine**, **Kuldeep Yadav**, and **Jasprit Bumrah**, stand out statistically; actual IPL 2027 auction availability/retention status is an external franchise constraint separate from this statistical ranking.

