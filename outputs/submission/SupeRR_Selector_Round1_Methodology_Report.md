# SupeRR Selector Season 2 (Round 1): Identifying the Most Reliable T20 Players Under Pressure

**Technical & Strategic Methodology Report (Model V2 Architecture)**  
**Prepared:** November 12, 2026  
**Dataset Window:** January 22, 2022 – November 1, 2026 (IPL & T20I)  
**Canonical Model:** Model B (*Maintenance & Lift* with Continuous Sigmoid Pressure Weights, Kish $N_{\text{eff}}$, Leave-Player-Out Hierarchical Baselines, and Empirical-Bayes Shrinkage)

---

## 1. Executive Summary

Winning T20 cricket is disproportionately decided in high-leverage inflection points—early powerplay collapses, suffocating middle-overs squeezes, and razor-thin death-overs chases—where raw career averages systematically conflate low-pressure run-accumulation with genuine clutch reliability. For **SupeRR Selector Season 2 (Round 1)**, we developed, forensically audited, and remediated a reproducible ball-by-ball statistical evaluation framework (**Model V2**) across **837 completed 20-over matches** (**367 IPL** and **470 T20I**, totaling **193,988 deliveries** and **185,692 legal balls**) from January 2022 through November 2026.

Following an independent Phase 0.5 audit of our initial V1 baseline that uncovered **seven methodological vulnerabilities** (2 Critical, 3 Moderate, 2 Minor)—including the silent exclusion of death-over specialist **Ashutosh Sharma** (`lp_balls = 42 < 60`), unshrunk small-match consistency inflation (`6–7` match streaks), and a 1:1 `HP − LP` elite-baseline penalty that suppressed **Jasprit Bumrah**, **Suryakumar Yadav**, and **Rinku Singh**—we engineered **Model V2** with:
1. **Strict Zero-Look-Ahead State Reconstruction & Chronological Elo:** Pre-delivery match state paired with separate, strictly pre-match rolling Elo tracks (`match_date < current_match_date`) for IPL and T20I opponents.
2. **Continuous Pressure Weighting & Kish Effective Sample Size ($N_{\text{eff}}$):** Retaining all **26,870 intermediate-pressure deliveries** ($13.85\%$ of the primary corpus) via a smooth logistic weight $w_t \in [0, 1]$ centered at $PI_t = 0.425$, calibrated with Kish $N_{\text{eff}} = (\sum w_t)^2 / \sum w_t^2$.
3. **Leave-Player-Out (LPO) Hierarchical Context Baselines:** Controlling for competition tier, season, innings phase, dynamic batting role (`Top 1-3`, `Middle 4-5`, `Finisher 6+`) or bowling class (`Pace` vs `Spin`), and Elo opponent tier—excluding player $i$'s own deliveries from every benchmark cell ($98.81\%$ of batter balls and $99.50\%$ of bowler legal balls resolved at the finest 5-way cell).
4. **Double Empirical-Bayes Shrinkage & Non-Penalizing Maintenance-Lift Scoring:** Linear EB shrinkage ($k = 120$ on Kish $N_{\text{eff}}$) on impact rates plus empirically fitted Beta-binomial shrinkage on cross-match consistency, scored via objectively selected **Model B** (`0.50` Absolute Pressure Impact + `0.30` Attenuated Maintenance Lift + `0.20` EB Consistency).
5. **1,000-Resample Stratified Match-Cluster Bootstrap:** Recomputing LPO baselines, EB shrinkage, and eligibility gates *inside every resample* stratified by `(comp_category, season_year)`.

### Canonical Top 10 Batters Under Pressure (Model V2 — `model_b`)

| Rank | Player ID | Player Name | Composite Score | Primary Role | Shrunk WP Impact (/100b) | Maint. Lift (/100b) | EB Cons. | $N_{\text{hp}}$ | Kish $N_{\text{eff}}$ | Boot Median (p05–p95) | Top-10 Freq |
|---:|---:|---|---:|---|---:|---:|---:|---:|---:|---:|---:|
| **1** | 6396 | **Tim David** | **+2.434** | Finisher 6+ | +41.75 | +28.28 | 63.0% | 570 | 744.3 | 3.0 (1.0–16.0) | 89.3% |
| **2** | 796 | **Matthew Wade** | **+2.267** | Finisher 6+ | +33.20 | +33.64 | 63.5% | 158 | 254.9 | 3.0 (1.0–14.0) | 64.9% |
| **3** | 37052 | **Naman Dhir** | **+2.028** | Finisher 6+ | +33.57 | +32.13 | 60.1% | 186 | 286.7 | 5.0 (1.0–33.0) | 66.1% |
| **4** | 143 | **Dinesh Karthik** | **+1.764** | Finisher 6+ | +36.24 | +27.70 | 56.2% | 250 | 372.0 | 8.0 (1.0–38.0) | 60.9% |
| **5** | 768 | **Reeza Hendricks** | **+1.745** | Top 1-3 | +29.59 | +28.18 | 59.8% | 223 | 424.9 | 8.0 (2.0–35.1) | 54.3% |
| **6** | 2756 | **Shashank Singh** | **+1.609** | Finisher 6+ | +32.42 | +26.41 | 56.6% | 327 | 402.1 | 9.0 (1.0–45.0) | 55.6% |
| **7** | 4260 | **Heinrich Klaasen** | **+1.608** | Middle 4-5 | +25.20 | +17.13 | 65.0% | 459 | 772.9 | 12.0 (3.9–31.0) | 41.9% |
| **8** | 4708 | **Rinku Singh** | **+1.445** | Finisher 6+ | +28.87 | +21.95 | 58.1% | 507 | 711.1 | 11.0 (2.0–43.0) | 47.8% |
| **9** | 1318 | **Andre Russell** | **+1.434** | Finisher 6+ | +29.57 | +16.43 | 59.8% | 347 | 490.0 | 12.0 (2.0–55.0) | 45.7% |
| **10** | 8101 | **Ashutosh Sharma** | **+1.335** | Finisher 6+ | +24.97 | +23.10 | 58.3% | 273 | 290.6 | 12.0 (2.0–52.0) | 28.0% |

### Canonical Top 10 Bowlers Under Pressure (Model V2 — `model_b`)

| Rank | Player ID | Player Name | Composite Score | Style Group | Shrunk WP Impact (/24b) | Maint. Lift (/24b) | EB Cons. | $N_{\text{hp}}$ | Kish $N_{\text{eff}}$ | Boot Median (p05–p95) | Top-10 Freq |
|---:|---:|---|---:|---|---:|---:|---:|---:|---:|---:|---:|
| **1** | 781 | **Sunil Narine** | **+2.481** | Spin_Finger | +9.98 | +8.79 | 71.4% | 454 | 739.6 | 4.0 (1.0–13.0) | 90.5% |
| **2** | 2933 | **Jasprit Bumrah** | **+1.995** | Pace_Fast | +9.61 | +7.43 | 65.3% | 496 | 785.1 | 7.0 (1.0–33.0) | 65.7% |
| **3** | 4373 | **Mustafizur Rahman** | **+1.851** | Pace_Medium | +8.04 | +7.73 | 66.5% | 500 | 749.5 | 11.0 (2.0–38.0) | 49.3% |
| **4** | 2382 | **Jamie Overton** | **+1.839** | Pace_Fast | +8.84 | +9.13 | 61.1% | 165 | 250.6 | 8.0 (1.0–41.0) | 46.9% |
| **5** | 2878 | **Mohit Sharma** | **+1.736** | Pace_FastMedium | +7.69 | +8.74 | 63.2% | 277 | 370.6 | 12.0 (1.0–55.0) | 43.4% |
| **6** | 5577 | **Sai Kishore** | **+1.708** | Spin_Finger | +7.72 | +8.43 | 63.1% | 123 | 204.5 | 6.0 (2.0–17.3) | 37.0% |
| **7** | 34485 | **Sufiyan Muqeem** | **+1.665** | Spin_Wrist | +7.90 | +8.20 | 62.2% | 148 | 214.8 | 10.0 (1.0–73.0) | 32.0% |
| **8** | 6669 | **Mohsin Khan** | **+1.625** | Pace_FastMedium | +8.16 | +7.59 | 61.8% | 163 | 283.6 | 11.0 (1.0–61.4) | 41.3% |
| **9** | 2490 | **Mohammad Nawaz** | **+1.556** | Spin_Finger | +7.94 | +7.64 | 60.9% | 282 | 486.9 | 13.0 (2.0–45.1) | 41.7% |
| **10** | 830 | **Josh Hazlewood** | **+1.472** | Pace_FastMedium | +7.49 | +6.23 | 63.3% | 436 | 692.8 | 16.0 (2.0–53.0) | 34.9% |

*(Governance Note: All statistical rankings are derived strictly from `data/raw/*.csv`. Practical IPL 2027 availability—such as the confirmed IPL/playing retirements of Matthew Wade, Dinesh Karthik, Andre Russell, and Mohit Sharma, the absence of a demonstrated IPL participation pathway for Pakistani nationals Sufiyan Muqeem and Mohammad Nawaz amid historical non-participation and geopolitical/governance uncertainty, and unverified pre-deadline IPL 2027 retention/auction lists—is tracked separately in Section 9 and never overrides on-field statistical merit.)*

---

## 2. Competition Understanding

The **SupeRR Selector Season 2 — Round 1** problem statement challenges participants to build a transparent, reproducible, data-driven evaluation system addressing a foundational T20 recruitment question: **Who are the 10 most reliable batters and 10 most reliable bowlers under pressure?**

Five core mandates govern the deliverable:
1. **Explicit, Justified Pressure Definition:** Pressure must reflect genuine match leverage—required run rate, wickets in hand, balls remaining, innings stage, and contest closeness—and empirically separate high-stress deliveries from routine overs.
2. **Coherent Dual-Discipline Framework:** Both batting and bowling must share a unified situational currency (runs relative to context expectation plus dismissal/wicket value) so evaluations are symmetrical and interpretable.
3. **Zero Reputation Bias:** Rankings must flow strictly from the supplied 2022–2026 IPL and T20I ball-by-ball dataset rather than star reputation or highlight-reel anecdotes.
4. **Fairness Across Contexts, Roles, and Sample Sizes:** Evaluations must adjust for league vs international scoring environments, batting order / bowling discipline, opponent quality, and small-sample volatility.
5. **1:1 Submission Parity & Reproducibility:** The Unstop Rank 1–10 dropdown lists and this Methodology Report must match 1:1 with zero duplicate entries, full mathematical transparency, and honest uncertainty/limitation reporting.

---

## 3. Dataset & Scope (Plus Forensic Audit of V1)

### 3.1 Raw Corpus & Primary Scope Reconciliation
The official data archive (`data/raw/`) spans **January 22, 2022 to November 1, 2026** across six relational CSV tables: `ball_by_ball.csv` (`200,999` rows, `33` columns), `matches.csv` (`883` rows, `22` columns), `competitions.csv` (`141` rows), `teams.csv` (`353` rows), `playing_eleven.csv` (`28,381` rows), and `competition_team_player_mapping.csv` (`6,413` rows).

Forensic auditing identified three structural exclusions required to enforce a clean, 20-over IPL + T20I primary scope:
- **Non-IPL `Other_T20` A-Team Tournaments Excluded (`30` matches, `6,985` deliveries):** `Mens T20 Emerging Teams Asia Cup 2024` (`comp_id = 2670`, 15 matches) and `Asia Cup Rising Stars 2025` (`comp_id = 3289`, 15 matches) are tagged `match_format = 'T20'` but represent emerging/A-team competitions outside the IPL + T20I brief. (These 30 matches also contained `12` of the raw dataset's `38` Super Over deliveries.)
- **Zero-Delivery Abandoned Matches Excluded (`16` matches):** `4` IPL and `12` T20I fixtures in `matches.csv` were abandoned without a ball bowled.
- **Super Over Deliveries Excluded (`26` IPL/T20I deliveries; `38` raw total across 6 matches):** Innings `3` and `4` operate under 6-ball / 2-wicket sudden-death rules incompatible with 20-over Pressure Index and contextual baselines.

| Scope Stage | Matches | Deliveries | Notes |
|---|---:|---:|---|
| Raw `matches.csv` / `ball_by_ball.csv` | 883 | 200,999 | Includes 30 `Other_T20` and 16 abandoned matches |
| Less `Other_T20` (`comp_id` 2670, 3289) | −30 | −6,985 | Includes 12 Super Over balls inside A-team fixtures |
| Less Abandoned Matches (0 deliveries) | −16 | 0 | 4 IPL, 12 T20I |
| Less IPL/T20I Super Overs (`innings` 3–4) | 0 | −26 | 38 total Super Over balls minus 12 in `Other_T20` |
| **Primary Analysis Scope (V2 — Scope A)** | **837** | **193,988** | **367 IPL + 470 T20I; 185,692 legal balls; 186,516 batter balls faced** |

#### Format & Scope Sensitivity Analysis (Scope A vs. Scope B)
To ensure that excluding `Other_T20` developmental fixtures does not bias player rankings, we conducted a complete sensitivity re-run including all 30 A-team matches (**Scope B: 867 matches, 200,961 deliveries**). Across all 20 canonical players, **zero ranking order changes occur between Scope A and Scope B ($\rho = 1.000$)**:
- *Batters:* Tim David (#1, $\Delta = 0.0000$), Matthew Wade (#2, $\Delta = 0.0000$), Naman Dhir (#3, score $2.028 \to 2.051$, $\Delta = +0.0229$ across 74 A-team balls), Dinesh Karthik (#4, $\Delta = 0.0000$), Reeza Hendricks (#5, $\Delta = 0.0000$), Shashank Singh (#6, $\Delta = 0.0000$), Heinrich Klaasen (#7, $\Delta = 0.0000$), Rinku Singh (#8, $\Delta = 0.0000$), Andre Russell (#9, $\Delta = 0.0000$), Ashutosh Sharma (#10, score $1.335 \to 1.339$, $\Delta = +0.0037$ across 12 A-team balls).
- *Bowlers:* Sunil Narine (#1, $\Delta = 0.0000$), Jasprit Bumrah (#2, $\Delta = 0.0000$), Mustafizur Rahman (#3, $\Delta = 0.0000$), Jamie Overton (#4, $\Delta = 0.0000$), Mohit Sharma (#5, $\Delta = 0.0000$), R. Sai Kishore (#6, score $1.708 \to 1.704$, $\Delta = -0.0035$ across 24 A-team balls), Sufiyan Muqeem (#7, score $1.665 \to 1.698$, $\Delta = +0.0334$ across 174 A-team balls), Mohsin Khan (#8, $\Delta = 0.0000$), Mohammad Nawaz (#9, $\Delta = 0.0000$), Josh Hazlewood (#10, $\Delta = 0.0000$).
This confirms that the primary 837-match scope preserves absolute statistical stability while maintaining strict competition brief purity.

### 3.2 Data Integrity & Cricket-Accounting Rules
1. **Identity Keying on `player_id`:** Joins strictly key on `player_id` (never `player_name`) to prevent homonym collisions observed in the raw corpus: `Abdul Samad` (`7446` India/IPL vs `6922` Pakistan/Pak A), `Rashid Khan` (`4722` Afghanistan/GT vs `20172` Nepal), and `Haider Ali` (`7338` Pakistan vs `28756` UAE). Duplicate `playing_eleven.csv` keys (`40` rows, e.g., `match_id = 13613`) are deduplicated before role mapping.
2. **D/L Revised Overs Unit:** `matches.csv` columns `first_inn_revised_overs` and `second_inn_revised_overs` store **balls** (e.g., `114.0` = 19 overs), not overs; V2 converts these directly into `inn_max_balls`.
3. **Extras & Legal-Delivery Accounting:** `wide` deliveries (`is_legal_ball = False`, `is_batter_ball_faced = False`) are excluded from balls faced by the striker and bowler legal balls; `Overstep` and `other` are treated as no-balls (`is_legal_ball = False`, `is_batter_ball_faced = True`); `byes` and `legbyes` are legal deliveries excluded from `bowler_runs_conceded`.
4. **Dismissal Attribution:** All team wickets advance `pre_wickets` for match-state pressure, but `RunOut`, `Retire Out`, and `Obstructing the field` (including raw typo `Obstracting the field`) are excluded from bowler wicket credit (`is_bowler_wicket`), while non-bowler run-outs/retirements do not penalize the non-involved batter/bowler asymmetrically.

### 3.3 Independent Phase 0.5 Audit: Seven Findings Driving V2
An independent audit (`outputs/model_audit/`) confirmed V1 was 100% mathematically reproducible (`max_abs_err <= 4.44e-16`, `9/9` accounting unit tests passing) while exposing **seven methodological flaws** that V2 explicitly resolves:

| ID | Severity | V1 Methodological Flaw | Verified Empirical Impact in V1 | V2 Architectural Resolution |
|---|---|---|---|---|
| **F1** | **Critical** | **Specialist Finisher Disqualification (`lp_balls >= 60`)** | **Ashutosh Sharma** (`8101`) faced `334` balls (`273` HP balls = `81.7%` across `22` HP matches, HP impact `+16.55` vs LP `-2.44`), yet was silently dropped because `lp_balls = 42 < 60`. | Replace `lp_balls >= 60` gate with overall sample sufficiency (`tot_balls >= 300`, `hp_balls >= 120`, `hp_matches >= 10`) plus EB-shrunk normal baseline. |
| **F2** | **Critical** | **Unshrunk Cross-Match Consistency (`m >= 6` HP balls)** | `20%` score weight on raw win rate inflated 6–8 match streaks: **Sai Kishore** (`7/7 = 100%`, `+3.31 SD`), **Reeza Hendricks** (`6/7 = 85.7%`, `+2.45 SD`), **Mohammad Rizwan** (`6/7`, `+2.45 SD`). | Beta-binomial Empirical-Bayes shrinkage via empirically fitted Beta prior ($\alpha_0, \beta_0$) pulling small-match streaks smoothly toward the population prior. |
| **F3** | **Moderate** | **Elite-Baseline Penalty (`HP − LP` 1:1 Confounding)** | `40%` weight on `HP − max(LP, floor)` penalized all-weather superstars: **Jasprit Bumrah** (`LP = +5.65`, Rank **#8**) trailed **Mohit Sharma** (`LP = -8.02`); **Suryakumar Yadav** (`LP = +37.85`, **#16**) & **Rinku Singh** (`LP = +25.27`, **#24**) were buried. | Separate **absolute pressure impact** (`50%`) from **attenuated maintenance lift** (`30%` on `shrunk_wp - 0.35 * max(shrunk_norm, floor)`) so elite normal baselines do not penalize pressure excellence. |
| **F4** | **Moderate** | **Missing Batting-Role & Opponent-Strength Controls** | Context grouped only by `(comp_tier, season_year, phase)`: openers and finishers shared baselines, all `T20I_Full` teams shared one expectation, and in-sample cells included player $i$'s own balls. | Dynamic batting roles (`Top 1-3`, `Middle 4-5`, `Finisher 6+`), chronological pre-match Elo (`IPL` & `T20I` separate tracks), and **Leave-Player-Out (LPO)** hierarchical baselines. |
| **F5** | **Moderate** | **Unstratified / Frozen Bootstrap (`n = 300`)** | Resampled without IPL/T20I stratification, froze `ctx_*` baselines and full-sample eligibility gates, and dropped absent draws. | `1,000`-resample `(comp_category, season_year)` stratified match-cluster bootstrap recomputing LPO baselines, shrinkage, and eligibility in every draw. |
| **F6** | **Minor** | **Intermediate-Pressure Gap (`0.35 <= PI < 0.50`)** | Discarded `26,870` deliveries (`13.85%` of primary balls, e.g., `408` balls for Suryakumar Yadav) between `LP` and `HP`. | Retain all `193,988` deliveries using continuous sigmoid weights $w_t \in [0, 1]$ and Kish $N_{\text{eff}} = (\sum w_t)^2 / \sum w_t^2$. |
| **F7** | **Minor** | **Inverted Bootstrap Axis & Ambiguous `%` Label** | `Rank 1` plotted on the right and `prob_top10` implied future match probability. | Plot `Rank 1` cleanly on the left and explicitly label `top10_inclusion_frequency` as bootstrap resample stability. |

---

## 4. Methodology

### 4.1 Zero-Look-Ahead Pre-Delivery State & Chronological Pre-Match Elo
Every delivery $t$ in match $m$, innings $I_t \in \{1, 2\}$ is processed strictly before delivery $t$'s outcome occurs:
- `pre_runs`, `pre_wickets`, `pre_legal_balls`, and `pre_balls_remaining = max(0, inn_max_balls - pre_legal_balls)` (honoring D/L ball limits in `first_inn_revised_overs` / `second_inn_revised_overs`).
- `pre_crr = 6 * pre_runs / pre_legal_balls` (when `pre_legal_balls > 0`), and second-innings `pre_rrr = 6 * runs_needed / pre_balls_remaining` (using `revised_target` when populated, else `first_inn_total + 1`).
- **Innings Phase:** `Powerplay` (overs 1–6), `Middle` (overs 7–15), and `Death` (overs 16–20).

To measure opponent quality without look-ahead leakage (`src/model_v2/opponent_strength.py`), we compute **chronological pre-match rolling Elo ratings** separately for `IPL` and `T20I` (never sharing ratings across formats), initialized at $R_0 = 1500.0$ with update step $K = 24.0$ and logistic scale $400.0$:
$$E_A = \frac{1}{1 + 10^{(R_B - R_A)/400}}, \qquad R_A^{\text{post}} = R_A^{\text{pre}} + 24\,(S_A - E_A)$$
Matches are sorted chronologically by `(comp_category, match_date, match_number, match_id)`. Crucially, **all matches on calendar date $D$ read only ratings from `match_date < D`**, with updates buffered until day $D$ completes. `No Result` and `Match Abandoned` fixtures leave Elo unchanged; tied matches with missing `win_team_id` score `0.5 / 0.5`. Opponents are mapped deterministically to `opp_tier`: `Low` ($\text{Elo} < 1480$, $31.83\%$ of batter balls), `Mid` ($[1480, 1525)$, $37.93\%$), and `High` ($\ge 1525$, $30.24\%$).

### 4.2 Continuous Pressure Index & Kish Effective Sample Size ($N_{\text{eff}}$)
We preserve the interpretable V1 situational Pressure Index $PI_t \in [0, 1]$ (`src/model_v2/pressure_model.py`) built from strictly pre-delivery state against `(comp_category, season_year)` par run rates and expected innings-1 wicket trajectories:
- **First Innings ($PI_{1,t}$):** $0.50\,s_{\text{collapse}} + 0.30\,s_{\text{crr\_deficit}} + 0.20\,s_{\text{death\_1st}}$, clipped to $[0, 1]$, capturing early collapses ($\ge 2$ wickets in PP), run-rate stalls after 3 overs, and late-innings acceleration pressure.
- **Second Innings ($PI_{2,t}$):** $(0.50\,s_{\text{rrr}} + 0.30\,s_{\text{wkts}} + 0.20\,s_{\text{urgency}} + \text{close\_finish\_boost}) \times \text{won\_damp} \times \text{lost\_damp}$, capturing tight chases ($RRR / \text{par} \in [0.65, 1.45]$, $\le 24$ balls remaining with $\le 48$ runs needed) while damping dead-rubber routs (`won_damp = 0.35`, `lost_damp = 0.40`).

Across the `193,988` primary deliveries, discrete V1 thresholds partition `52,002` **High-Pressure** balls ($PI_t \ge 0.50$, $26.81\%$), `115,116` **Low-Pressure** balls ($PI_t < 0.35$, $59.34\%$), and `26,870` **Intermediate-Pressure** balls ($0.35 \le PI_t < 0.50$, $13.85\%$). Rather than discarding those `26,870` intermediate balls, Model V2 assigns every delivery a smooth **continuous pressure weight** $w_t$ and complementary normal weight $1 - w_t$:
$$w_t = \sigma\!\left(\frac{PI_t - 0.425}{0.08}\right) = \frac{1}{1 + \exp\!\left(-(PI_t - 0.425)/0.08\right)}, \qquad \bar{w}_t = 0.3512$$
Centered at the exact midpoint (`0.425`) between V1's `0.35` and `0.50` thresholds, $w_t \approx 0.28$ at $PI = 0.35$, $0.50$ at $PI = 0.425$, and $\approx 0.72$ at $PI = 0.50$. Because weighted averages have higher variance than unweighted averages of the same sum of weights, we quantify true information depth using **Kish's Effective Sample Size** (Kish, 1965):
$$N_{\text{eff}} = \frac{\left(\sum_t w_t\right)^2}{\sum_t w_t^2}$$

It is critical to distinguish four distinct sample-size quantities:
1. $N_{\text{tot}}$: Total regulation balls faced or bowled by player $i$.
2. $N_{\text{hp}}$: Number of discrete high-pressure deliveries where $PI_t \ge 0.50$.
3. $\sum_t w_t$: Sum of continuous pressure weights across all deliveries.
4. $N_{\text{eff}}$: Kish effective sample size accounting for unequal weight variance.

Because continuous sigmoid weighting assigns small, positive tail weights ($w_t \approx 0.05 - 0.28$) to low- and intermediate-pressure deliveries rather than discarding them, $N_{\text{eff}}$ integrates fractional information across a player's complete body of work. Consequently, while $N_{\text{eff}} \le N_{\text{tot}}$ holds strictly by Cauchy-Schwarz inequality, **$N_{\text{eff}} > N_{\text{hp}}$ naturally occurs** for players with high overall match volumes (e.g., Tim David: $N_{\text{tot}} = 1,226$, $N_{\text{hp}} = 570$, but Kish $N_{\text{eff}} = 744.3$; Phil Salt: $N_{\text{tot}} = 1,643$, $N_{\text{hp}} = 112$, Kish $N_{\text{eff}} = 354.8$). This property prevents discarding borderline-pressure contributions while strictly controlling estimator variance.

### 4.3 Dynamic Batting Roles, Bowling Styles & LPO Hierarchical Baselines
- **Dynamic Batting Roles (`src/model_v2/batting_features.py`):** Combining `playing_eleven.csv` team sheets with realized delivery `batting_order`, every batter delivery is tagged `Top 1-3` ($49.86\%$), `Middle 4-5` ($26.90\%$), or `Finisher 6+` ($23.24\%$), with realized delivery order taking precedence when promotions/demotions occur (`role_uncertain_rate = 0.19%`).
- **Bowling Taxonomy (`src/model_v2/bowling_features.py`):** Categorizes every bowler into `Pace` vs `Spin` and fine-grained `bowling_style_group` (`Pace_Fast`, `Pace_FastMedium`, `Pace_Medium`, `Spin_Finger`, `Spin_Wrist`).
- **Leave-Player-Out (LPO) Hierarchical Context Baselines (`src/model_v2/context_baselines.py`):** To ensure player $i$ never sets their own benchmark, we subtract player $i$'s own deliveries from every context cell $c$:
  $$\hat{\mu}_{-i, c} = \frac{\sum_{t \in c, \, p(t) \ne i} y_t}{n_c - n_{i,c}}$$
  walking up a 6-level hierarchy whenever $n_c - n_{i,c} < 50$:
  - *Batting:* `(comp_tier, season_year, phase, batting_role, opp_tier_bat)` $\rightarrow$ drop `opp_tier_bat` $\rightarrow$ drop `batting_role` $\rightarrow$ `(comp_tier, phase)` $\rightarrow$ `(phase)` $\rightarrow$ global LPO.
  - *Bowling:* `(comp_tier, season_year, phase, pace_or_spin, opp_tier_bowl)` $\rightarrow$ drop `opp_tier_bowl` $\rightarrow$ drop `pace_or_spin` $\rightarrow$ `(comp_tier, phase)` $\rightarrow$ `(phase)` $\rightarrow$ global LPO.
  Empirically, **$98.81\%$** of batter balls faced and **$99.50\%$** of bowler legal balls resolve at Level 0 (the most granular 5-way cell), with $0.94\%$ / $0.42\%$ at Level 1 and $0.26\%$ / $0.08\%$ at Level 2.

### 4.4 Delivery Impact Currency & Non-Overlapping Wicket Valuation
For each delivery, we combine runs relative to LPO contextual expectation with dismissal/wicket value relative to LPO contextual expectation:
- **Batter Delivery Impact (scaled per 100 balls faced):**
  $$\text{imp}_{t}^{\text{bat}} = 100 \times \Big[ (r_t - \hat{\mu}_{-i,c}^{\text{rpb}}) + V_{\text{wkt}}\,(\hat{p}_{-i,c}^{\text{out}} - d_t) \Big]$$
- **Bowler Delivery Impact (scaled per 24 legal balls, 4-over spell):**
  $$\text{imp}_{t}^{\text{bowl}} = 24 \times \Big[ (\hat{\mu}_{-i,c}^{\text{rpb}} \cdot \mathbb{I}_{\text{legal},t} - r^{\text{bowl}}_t) + V_{\text{wkt}}\,(w_t^{\text{bowl}} - \hat{p}_{-i,c}^{\text{wkt}} \cdot \mathbb{I}_{\text{legal},t}) \Big]$$

The canonical specification sets $V_{\text{wkt}} = 6.0$ runs per wicket. Crucially, to test sensitivity against dynamic wicket values without double-counting the runs scored on delivery $t$, our `context_marginal` sensitivity model estimates marginal expected future runs lost from wicket $W \to W+1$ using `runs_rem_after = inn_total_runs - post_runs` via hierarchical Ridge curves in `(post_wickets, post_wickets^2)` controlling for `post_balls_rem` and `runs_needed` (mean marginal value `7.823` runs/wicket across `context_wicket_values.csv`).

### 4.5 Empirical-Bayes Shrinkage & Candidate Models A, B, and C
- **Impact Shrinkage:** Observed pressure-weighted (`wp_impact`) and normal-weighted (`norm_impact`) averages are shrunk toward `0.0` using linear Empirical Bayes weighted by Kish $N_{\text{eff}}$ with $k = 120$ (validated via odd/even match split-half out-of-sample MSE in Section 7):
  $$\text{ShrunkImpact}_i = \frac{N_{\text{eff}, i}}{N_{\text{eff}, i} + 120}\,\overline{\text{Impact}}_i$$
- **Beta-Binomial Cross-Match Consistency:** Across qualifying HP matches ($m_{\text{hp}} \ge 6$ HP balls), we count positive-impact matches (`hp_pos_matches` out of `hp_qual_m`) and fit an empirical population Beta prior $\text{Beta}(\alpha_0, \beta_0)$ via maximum likelihood (MLE) over the eligible pool (`batters`: $\alpha_0 = 28.070, \beta_0 = 21.930$; `bowlers`: $\alpha_0 = 25.736, \beta_0 = 19.104$), yielding $\text{Cons}_{\text{EB},i} = \frac{\text{pos}_i + \alpha_0}{m_i + \alpha_0 + \beta_0}$ (compared directly against unshrunk raw rates and fixed `Beta(5,5)` in Section 7).

We evaluated **three competing scoring architectures** on the benchmark eligible pool (`tot_balls >= 300`, `hp_balls >= 120`, `hp_matches >= 10`; **99 batters** and **128 bowlers**):
- **1. Model A (Absolute Continuous Pressure Impact):** $0.50\,z(\text{ShrunkWP}) + 0.30\,z(\text{ShrunkHP}) + 0.20\,z(\text{Cons}_{\text{EB}})$.
- **2. Model B (Attenuated Maintenance & Lift — Selected Canonical):** Explicitly separates absolute pressure impact from an **attenuated maintenance adjustment** over a floored normal-pressure baseline ($\text{floor} = -5.0$ batters, $-3.0$ bowlers; attenuation $\alpha = 0.35$). Rather than completely eliminating the baseline penalty, Model B reduces the full 1:1 deduction found in V1 by 65%, ensuring that players with strong normal-overs baselines are not unfairly penalized while still rewarding players who demonstrate positive performance elevation under pressure:

$$\text{MaintLift}_i = \text{ShrunkWP}_i - 0.35\,\max(\text{ShrunkNorm}_i,\; \text{floor})$$

$$\text{Score}_{B, i} = 0.50\,z(\text{ShrunkWP}_i) + 0.30\,z(\text{MaintLift}_i) + 0.20\,z(\text{Cons}_{\text{EB}, i})$$

- **3. Model C (Regularized Ridge / Logit Interaction):** Joint sparse Ridge regression on runs (`alpha = 150`) and L2 logistic regression on dismissals/wickets (`C = 0.5`) with context main effects, continuous $w_t$, player main effects, and player $\times$ $w_t$ interactions.

**Objective Model Selection & Domain Bonus Disclosure (`model_comparison.csv`):** Candidate models were evaluated across walk-forward OOS correlation (weight `0.35`), Leave-One-Season-Out Spearman stability (weight `0.35`), interpretability (weight `0.30`), a domain maintenance bonus (`+0.05` for Model B), and calibration/Brier penalties (`-0.20` for Model C due to OOS logistic calibration slope degradation to `0.653`/`0.604`).
To ensure absolute transparency, we disclose model comparison scores both **with** and **without** the `+0.05` domain bonus:
- *Batters without Bonus:* **Model B = 0.5827** vs. Model A = 0.5787 vs. Model C = 0.2803 (Model B leads by `+0.0040`). With bonus: **0.6327** vs. 0.5787.
- *Bowlers without Bonus:* **Model B = 0.6659** vs. Model A = 0.6525 vs. Model C = 0.3560 (Model B leads by `+0.0134`). With bonus: **0.7159** vs. 0.6525.
Model B finishes ahead of Model A in both disciplines even without the domain bonus. While Model A exhibits a slightly less negative forward OOS correlation for batters (`-0.022` vs `-0.054`, both near zero), Model B is chosen on the complete multi-criteria trade-off: tighter bootstrap confidence intervals (`36.6` vs `39.3` for batters; `44.0` vs `46.9` for bowlers), higher LOSO stability (`0.905` / `0.937`), transparent franchise interpretability, and avoidance of Model C's out-of-sample calibration failure.

![High-Pressure Performance vs Normal Baseline](file:///c:/Users/LENOVO/OneDrive/Desktop/SupeRR-Selector-Season-2/outputs/model_v2/charts/03_pressure_vs_normal_impact.png)
*Figure 1 (`03_pressure_vs_normal_impact.png`): Shrunk high-pressure impact vs shrunk normal-pressure baseline across all 99 eligible batters and 128 eligible bowlers. Model B rewards players sitting far above the parity diagonal (`Tim David`, `Sunil Narine`, `Jasprit Bumrah`) without penalizing elite performers for strong normal-overs baselines.*

---

## 5. Batting Evaluation

Across the `99` eligible batters, Model V2 surfaces a coherent hierarchy dominated by high-impact **Finisher 6+** specialists (`8` of the Top 10) alongside one elite **Middle 4-5** anchor (`#7 Heinrich Klaasen`) and one high-volume **Top 1-3** opener (`#5 Reeza Hendricks`). Crucially, removing V1's `lp_balls >= 60` trap and 1:1 baseline penalty restores true IPL/T20I pressure finishers without relying on small-sample noise.

![Model V2 Top 10 Batters Ranking](file:///c:/Users/LENOVO/OneDrive/Desktop/SupeRR-Selector-Season-2/outputs/model_v2/charts/01_top10_batters_ranking.png)
*Figure 2 (`01_top10_batters_ranking.png`): Canonical Top 10 Batters ranked from #1 at top, comparing observed continuous pressure-weighted impact against Kish-$N_{\text{eff}}$ Empirical-Bayes shrunk impact.*

### 5.1 Complete Top 10 Batter Profiles & Multi-Dimensional Splits

| Rank | Batter | Role (Median Order) | Tot / HP Balls | $N_{\text{eff}}$ | WP SR | WP Avg | Shrunk WP | Shrunk Norm | Maint. Lift | IPL Shrunk WP | T20I Shrunk WP | Death Shrunk WP | Pace / Spin Shrunk WP |
|---:|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| **1** | **Tim David** | Finisher 6+ (`6.0`) | 1,226 / 570 | 744.3 | 175.1 | 36.7 | **+41.75** | +38.49 | +28.28 | +30.15 | +41.96 | +40.93 | +46.57 / +18.28 |
| **2** | **Matthew Wade** | Finisher 6+ (`7.0`) | 427 / 158 | 254.9 | 150.1 | 57.4 | **+33.20** | -1.27 | +33.64 | -11.05 | +38.96 | +45.41 | +40.42 / -3.26 |
| **3** | **Naman Dhir** | Finisher 6+ (`6.0`) | 515 / 186 | 286.7 | 181.3 | 36.4 | **+33.57** | +4.14 | +32.13 | +20.23 | +29.55 | +27.21 | +39.48 / +4.77 |
| **4** | **Dinesh Karthik** | Finisher 6+ (`6.0`) | 639 / 250 | 372.0 | 164.5 | 38.9 | **+36.24** | +24.41 | +27.70 | +35.89 | +9.35 | +33.81 | +38.75 / +15.06 |
| **5** | **Reeza Hendricks** | Top 1-3 (`2.0`) | 835 / 223 | 424.9 | 167.7 | 43.3 | **+29.59** | +4.02 | +28.18 | 0.00 | +27.47 | +2.92 | +32.56 / +11.29 |
| **6** | **Shashank Singh** | Finisher 6+ (`6.0`) | 560 / 327 | 402.1 | 161.0 | 44.8 | **+32.42** | +17.20 | +26.41 | +31.40 | 0.00 | +30.10 | +27.74 / +24.74 |
| **7** | **Heinrich Klaasen** | Middle 4-5 (`5.0`) | 1,417 / 459 | 772.9 | 158.7 | 38.9 | **+25.20** | +23.08 | +17.13 | +27.87 | +4.22 | +13.49 | +7.42 / +38.00 |
| **8** | **Rinku Singh** | Finisher 6+ (`6.0`) | 1,284 / 507 | 711.1 | 150.5 | 44.5 | **+28.87** | +19.76 | +21.95 | +28.27 | +12.64 | +58.63 | +41.41 / +3.67 |
| **9** | **Andre Russell** | Finisher 6+ (`7.0`) | 733 / 347 | 490.0 | 161.7 | 27.2 | **+29.57** | +37.56 | +16.43 | +18.20 | +34.07 | +11.92 | +29.02 / +19.02 |
| **10** | **Ashutosh Sharma** | Finisher 6+ (`7.0`) | 334 / 273 | 290.6 | 168.5 | 33.4 | **+24.97** | +5.35 | +23.10 | +24.51 | 0.00 | +32.97 | +33.92 / -1.97 |

Key takeaways from the Top 10 batting hierarchy:
- **Unanimous #1 — Tim David (+2.434):** Ranked **#1 across all three candidate models (Model A, B, and C)**, David combines massive volume (`570` HP balls, $N_{\text{eff}} = 744.3$), a `+41.75` shrunk pressure impact (`175.1` WP SR), dual-format dominance (`+30.15` IPL, `+41.96` T20I), and `89.3%` Top-10 bootstrap inclusion (`p05–p95` `1.0–16.0`).
- **Dual-Format & IPL Middle-Order Core:** **Naman Dhir (#3, +2.028)** shows explosive pressure acceleration (`181.3` WP SR, `+32.13` lift), **Shashank Singh (#6, +1.609)** offers rare pace-and-spin symmetry (`+27.74` vs pace, `+24.74` vs spin), and **Heinrich Klaasen (#7, +1.608)** leads all batters in EB consistency (`65.0%`, `20/24` raw) and spin-hitting under pressure (`+38.00` vs spin, middle-overs `+29.28`).
- **Context Flags Within Top 10:** **Matthew Wade (#2)** and **Dinesh Karthik (#4)** earned elite 2022–2024 historical pressure numbers (`+33.20` and `+36.24`) prior to retiring into coaching, while **Reeza Hendricks (#5)** achieved his rating entirely in T20Is (`0` IPL HP balls) and drops under `142` bootstrap draws when T20I match counts fluctuate.

### 5.2 Batting Spotlights: Rescuing Ashutosh Sharma & Rinku Singh (Plus SKY #12)
1. **Ashutosh Sharma (#10, `player_id = 8101`) — Rescued from V1's `lp_balls` Trap:** In V1, Ashutosh was silently disqualified despite facing `273` HP balls (`81.7%` of his `334` total balls) across `22` HP matches because he had only `42` low-pressure balls (`< 60`). In Model V2, with $N_{\text{eff}} = 290.6$, a `168.5` WP strike rate, `+24.97` shrunk WP impact (`+32.97` in Death overs), and `+23.10` maintenance lift, Ashutosh legitimately claims **#10** (appearing in **#10** on Model B and **#11** on Models A and C).
2. **Rinku Singh (#8, `player_id = 4708`) — Rescued from V1's Elite-Baseline Penalty:** In V1, Rinku's strong normal-pressure baseline (`lp_impact_100 = +25.27`) crushed his delta to `-4.91` and buried him at **#24**. In V2, over `507` HP balls ($N_{\text{eff}} = 711.1$), Rinku posts `+28.87` shrunk WP impact (`44.5` WP average), `+21.95` maintenance lift, and the **#1 Death-phase shrunk impact in the entire dataset (`+58.63` per 100 balls)**, rising 16 spots to **#8**.
3. **Suryakumar Yadav (#12, `player_id = 1699`) — Near-Top-10 Elite All-Weather Context:** SKY's normal-pressure brilliance (`shrunk_norm_impact = +29.70`, `lp_sr = 170.5`) exceeds his shrunk pressure impact (`+23.69` across $N_{\text{eff}} = 1,180.5$), pulling his maintenance lift (`+13.30`) and EB consistency (`58.9%`) slightly behind Top-10 finishers (`#12` in Models A and B, `#10` in Model C, `boot_median_rank = 20.0`).

![Observed vs Shrunk Pressure Impact & Maintenance-Lift Comparison](file:///c:/Users/LENOVO/OneDrive/Desktop/SupeRR-Selector-Season-2/outputs/model_v2/charts/04_pressure_performance_comparison.png)
*Figure 3 (`04_pressure_performance_comparison.png`): Decomposition of observed pressure impact, EB-shrunk pressure impact, and attenuated maintenance lift across the Top 10 and spotlight candidates (`Suryakumar Yadav`, `Kuldeep Yadav`, `Varun Chakravarthy`).*

![Dynamic Batting Role & Phase Analysis](file:///c:/Users/LENOVO/OneDrive/Desktop/SupeRR-Selector-Season-2/outputs/model_v2/charts/05_batter_role_analysis.png)
*Figure 4 (`05_batter_role_analysis.png`): Eligible batter pressure impact by dynamic batting role (`Top 1-3` n=23, `Middle 4-5` n=45, `Finisher 6+` n=31) and phase-by-phase shrunk impact breakdown for the Top 10.*

---

## 6. Bowling Evaluation

Across `128` eligible bowlers, Model V2 achieves a balanced, phase-versatile Top 10 featuring **6 pace bowlers** and **4 spinners** (`Sunil Narine`, `Sai Kishore`, `Sufiyan Muqeem`, `Mohammad Nawaz`). Removing V1's unshrunk consistency bias and 1:1 `HP − LP` penalty restores proven multi-phase elites (`Sunil Narine #1`, `Jasprit Bumrah #2`) to the top of the board while appropriately shrinking smaller-sample bursts.

![Model V2 Top 10 Bowlers Ranking](file:///c:/Users/LENOVO/OneDrive/Desktop/SupeRR-Selector-Season-2/outputs/model_v2/charts/02_top10_bowlers_ranking.png)
*Figure 5 (`02_top10_bowlers_ranking.png`): Canonical Top 10 Bowlers ranked from #1 at top, showing observed pressure-weighted impact vs Kish-$N_{\text{eff}}$ EB-shrunk impact per 24 legal balls.*

### 6.1 Complete Top 10 Bowler Profiles & Phase/Hand Splits

| Rank | Bowler | Style Group | Tot / HP Balls | $N_{\text{eff}}$ | WP ER | WP SR | Shrunk WP | Shrunk Norm | Maint. Lift | IPL Shrunk WP | T20I Shrunk WP | PP / Mid / Death Shrunk WP | RHB / LHB Shrunk WP |
|---:|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|---|
| **1** | **Sunil Narine** | Spin_Finger | 1,530 / 454 | 739.6 | 6.01 | 19.5 | **+9.98** | +3.40 | +8.79 | +9.61 | 0.00 | +3.95 / +7.33 / +11.71 | +9.40 / +7.72 |
| **2** | **Jasprit Bumrah** | Pace_Fast | 1,708 / 496 | 785.1 | 7.16 | 15.6 | **+9.61** | +6.24 | +7.43 | +8.64 | +7.08 | +2.81 / +6.20 / +11.37 | +7.14 / +11.07 |
| **3** | **Mustafizur Rahman** | Pace_Medium | 1,576 / 500 | 749.5 | 6.99 | 16.1 | **+8.04** | +0.90 | +7.73 | +2.89 | +8.90 | +1.46 / +6.91 / +8.08 | +7.46 / +6.32 |
| **4** | **Jamie Overton** | Pace_Fast | 497 / 165 | 250.6 | 6.96 | 12.2 | **+8.84** | -0.82 | +9.13 | +3.48 | +7.88 | +0.01 / +4.03 / +9.56 | +7.37 / +5.78 |
| **5** | **Mohit Sharma** | Pace_FastMedium | 649 / 277 | 370.6 | 8.72 | 11.1 | **+7.69** | -3.58 | +8.74 | +7.40 | 0.00 | -0.92 / +7.41 / +5.25 | +7.85 / +3.81 |
| **6** | **Sai Kishore** | Spin_Finger | 465 / 123 | 204.5 | 7.28 | 11.0 | **+7.72** | -2.04 | +8.43 | +7.06 | 0.00 | +0.48 / +6.23 / +4.61 | +7.00 / +3.73 |
| **7** | **Sufiyan Muqeem** | Spin_Wrist | 344 / 148 | 214.8 | 5.51 | 10.7 | **+7.90** | -0.85 | +8.20 | 0.00 | +7.38 | — / +8.60 / +1.67 | +7.79 / +2.96 |
| **8** | **Mohsin Khan** | Pace_FastMedium | 654 / 163 | 283.6 | 7.99 | 11.6 | **+8.16** | +1.63 | +7.59 | +7.47 | 0.00 | +5.82 / +5.56 / +4.70 | +2.78 / +10.84 |
| **9** | **Mohammad Nawaz** | Spin_Finger | 1,004 / 282 | 486.9 | 6.41 | 11.9 | **+7.94** | +0.84 | +7.64 | 0.00 | +7.51 | +0.39 / +8.09 / +2.72 | +6.37 / +7.28 |
| **10** | **Josh Hazlewood** | Pace_FastMedium | 1,476 / 436 | 692.8 | 8.08 | 13.0 | **+7.49** | +3.60 | +6.23 | +7.28 | +4.52 | +7.60 / +3.86 / +5.92 | +6.12 / +7.32 |

### 6.2 Bowling Spotlights: Elite Anchors vs Small-Sample Recalibration
1. **Sunil Narine (#1, `player_id = 781`):** Ranked **#1 across all three models (A, B, and C)**, Narine pairs a `6.01` WP economy rate (`+2.78` runs saved per over vs context!) with `71.4%` EB consistency (`27/29 = 93.1%` raw), `+11.71` shrunk death-phase impact, and an unmatched **90.5% Top-10 bootstrap inclusion** (`boot_median_rank = 4.0`, `p05–p95` `1.0–13.0`).
2. **Jasprit Bumrah (#2, `player_id = 2933`):** In V1, Bumrah's elite normal-overs control (`lp_impact_24 = +5.65`) compressed his delta and pushed him down to **#8**. Model V2 elevates him to **#2** (`+1.995`), driven by `785.1` Kish $N_{\text{eff}}$ (largest among Top-10 bowlers), `+9.61` shrunk WP impact (`15.6` WP strike rate, `44.0%` dot rate), dual-format elite proof (`+8.64` IPL, `+7.08` T20I), and dominant death-overs pressure impact (`+11.37`).
3. **Sai Kishore (#6, `player_id = 5577`) & Sufiyan Muqeem (#7, `player_id = 34485`):** Both ranked artificially at **#2** and **#1** in V1 due to unshrunk consistency streaks (`7/7 = 100%` and `9/11 = 81.8%`) and negative LP baselines. In V2, Empirical Bayes shrinks their impact (`+12.25` $\to$ `+7.72` for Kishore; `+12.31` $\to$ `+7.90` for Muqeem) and consistency (`63.1%` and `62.2%`), while the bootstrap transparently exposes their gate sensitivity (`545/1000` ineligible draws for Kishore at `123` HP balls; `372/1000` ineligible draws and `p05–p95 = 1.0–73.0` for Muqeem at `148` HP balls).
4. **Powerplay & Left-Arm Specialists:** **Josh Hazlewood (#10)** provides the highest Powerplay pressure impact in the Top 10 (`+7.60`), **Mohsin Khan (#8)** excels across all phases (`+5.82` PP, `+5.56` Middle, `+4.70` Death) and dominates left-handers (`+10.84`), and **Mustafizur Rahman (#3)** delivers deep dual-format death-overs cutter craft (`500` HP balls, `+8.08` Death).

![Bowling Phase & Pace/Spin Analysis](file:///c:/Users/LENOVO/OneDrive/Desktop/SupeRR-Selector-Season-2/outputs/model_v2/charts/06_bowling_phase_analysis.png)
*Figure 6 (`06_bowling_phase_analysis.png`): Phase-by-phase shrunk pressure impact for the Top 10 bowlers (left) and Pace (n=83) vs Spin (n=45) pool distributions (right).*

![IPL vs T20I Format Comparison](file:///c:/Users/LENOVO/OneDrive/Desktop/SupeRR-Selector-Season-2/outputs/model_v2/charts/09_ipl_vs_t20i_comparison.png)
*Figure 7 (`09_ipl_vs_t20i_comparison.png`): Cross-format shrunk pressure impact separating dual-format stars (`Tim David`, `Naman Dhir`, `Jasprit Bumrah`, `Josh Hazlewood`, `Mustafizur Rahman`) from IPL-only (`Sunil Narine`, `Shashank Singh`, `Sai Kishore`, `Ashutosh Sharma`) and T20I-only (`Reeza Hendricks`, `Sufiyan Muqeem`, `Mohammad Nawaz`) specialists.*

---

## 7. Statistical Reliability

### 7.1 Empirical-Bayes Consistency & Shrinkage Calibration
Without shrinkage, players with `7–10` qualifying HP matches routinely register `85%–100%` positive match rates (`Matthew Wade 10/10 = 100%`, `Sai Kishore 7/7 = 100%`, `Reeza Hendricks 6/7 = 85.7%`, `Sufiyan Muqeem 9/11 = 81.8%`), inflating composite z-scores. Fitting an Empirical-Bayes Beta prior over the eligible pools yields $\text{Beta}(28.07, 21.93)$ for batters (prior mean `0.561`) and $\text{Beta}(25.74, 19.10)$ for bowlers (prior mean `0.574`), compressing extreme 7-match streaks into realistic `59%–64%` estimates while allowing deep-sample consistency leaders like **Sunil Narine (`27/29` $\to$ `71.4%`)**, **Heinrich Klaasen (`20/24` $\to$ `65.0%`)**, and **Mustafizur Rahman (`28/36` $\to$ `66.5%`)** to separate cleanly.

To calibrate impact shrinkage $k \in \{60, 90, 120, 150, 180\}$, we ran odd/even match split-half out-of-sample tests (`shrinkage_k_sensitivity.csv`, $n=267$ batters, $n=232$ bowlers). Weighted split-half MSE declines steeply from $k=60$ (`786.3` batters, `47.35` bowlers) to $k=120$ (`747.6`, `42.66`), where batter split-half correlation peaks at **$r = 0.3233$** before flattening across $k \in [120, 180]$, confirming **$k = 120$** as a well-balanced bias-variance trade-off.

![Cross-Match Reliability Empirical Bayes Shrinkage](file:///c:/Users/LENOVO/OneDrive/Desktop/SupeRR-Selector-Season-2/outputs/model_v2/charts/07_pressure_consistency_analysis.png)
*Figure 8 (`07_pressure_consistency_analysis.png`): Raw unshrunk positive-match rates vs Empirical-Bayes Beta-binomial shrunk consistency across qualifying HP match counts.*

![Sample Depth Comparison: N_hp vs Kish N_eff](file:///c:/Users/LENOVO/OneDrive/Desktop/SupeRR-Selector-Season-2/outputs/model_v2/charts/10_player_sample_size_comparison.png)
*Figure 9 (`10_player_sample_size_comparison.png`): Comparison of discrete HP balls (`PI >= 0.50`) against continuous Kish effective sample size ($N_{\text{eff}}$) and total balls faced/bowled, illustrating how continuous weighting recovers information for near-miss high-volume players (`Phil Salt`, `Virat Kohli`).*

### 7.2 1,000-Resample Stratified Match-Cluster Bootstrap
To quantify rank uncertainty without data leakage or sample-independence violations, we executed **1,000 stratified match-cluster bootstrap resamples** (`seed = 42`), preserving exact match counts per `(comp_category, season_year)` cell, assigning unique `boot_match_instance_id` keys to avoid collapsing resampled match copies, and **recomputing LPO baselines, EB shrinkage, Beta priors, and `300/120/10` eligibility gates inside every single resample**.

> [!IMPORTANT]
> **Interpretation Guardrail:** `top10_inclusion_frequency` measures how often a player finishes in the Top 10 across 1,000 historical match-cluster resamples. **It is a measure of statistical ranking stability—not a future single-match probability of success.**

#### Unconditional vs. Conditional Bootstrap Stability
To avoid misinterpreting borderline-sample effects, we distinguish two complementary bootstrap frequencies:
1. **Unconditional Top-10 Frequency ($f_{\text{uncond}} = k_{\text{top10}} / 1000$):** Reflects total inclusion across all 1,000 resamples regardless of whether random match sampling caused the player to fall below the eligibility gates.
2. **Conditional Top-10 Frequency ($f_{\text{cond}} = k_{\text{top10}} / N_{\text{eligible}}$):** Reflects inclusion strictly among resamples where the player successfully passed the `300/120/10` gates.

For example, **R. Sai Kishore** registers an unconditional frequency of **37.0%** (370/1000) because his 123-ball sample causes him to miss the 120-ball gate in 545 draws. However, **conditional on passing the gate (455 draws), Sai Kishore finishes in the Top 10 in 81.3% of iterations (370/455)** with an exceptionally narrow conditional 90% confidence interval of $[2.0, 17.3]$. Similarly, **Ashutosh Sharma** registers 28.0% unconditionally, but **51.2% conditionally** (280/547 eligible draws), proving that their ratings reflect genuine high-pressure mastery rather than fluke selections.

| Discipline | Most Stable Anchors (Top-10 Freq / CI) | Moderate-Variance Contenders | Borderline-Gate Players (`ineligible_iters > 50`) |
|---|---|---|---|
| **Batters** | **Tim David** (`89.3%` uncond / `89.3%` cond, CI `1–16`), **Naman Dhir** (`66.1%` / `72.8%`, CI `1–33`), **Matthew Wade** (`64.9%` / `90.1%`, CI `1–14`) | **Dinesh Karthik** (`60.9%`, CI `1–38`), **Shashank Singh** (`55.6%`, CI `1–45`), **Rinku Singh** (`47.8%`, CI `2–43`), **Andre Russell** (`45.7%`, CI `2–55`), **Heinrich Klaasen** (`41.9%`, CI `3.9–31`) | **Ashutosh Sharma** (`338` inelig, `28.0%` uncond / `51.2%` cond, CI `2–52`), **Matthew Wade** (`280` inelig), **Reeza Hendricks** (`142` inelig, `54.3%` / `63.3%`), **Naman Dhir** (`92` inelig) |
| **Bowlers** | **Sunil Narine** (`90.5%` uncond / `90.5%` cond, CI `1–13`), **Jasprit Bumrah** (`65.7%` / `65.7%`, CI `1–33`), **Mustafizur Rahman** (`49.3%` / `62.4%`, CI `2–38`) | **Mohammad Nawaz** (`41.7%`, CI `2–45.1`), **Mohit Sharma** (`43.4%`, CI `1–55`), **Josh Hazlewood** (`34.9%`, CI `2–53`) | **Sai Kishore** (`545` inelig, `37.0%` uncond / `81.3%` cond, conditional CI `2–17.3`), **Sufiyan Muqeem** (`372` inelig, `32.0%` / `51.0%`, CI `1–73`), **Jamie Overton** (`209` inelig, `46.9%` / `59.3%`), **Mohsin Khan** (`168` inelig, `41.3%` / `49.6%`) |

![Bootstrap Rank Uncertainty](file:///c:/Users/LENOVO/OneDrive/Desktop/SupeRR-Selector-Season-2/outputs/model_v2/charts/08_bootstrap_rank_uncertainty.png)
*Figure 10 (`08_bootstrap_rank_uncertainty.png`): 1,000-resample stratified bootstrap median ranks and 5th–95th percentile intervals (Rank 1 on the left; Top-10 cutoff dashed at 10.5).*

---

## 8. Model Validation & Sensitivity Suite

### 8.1 Model A vs B vs C Comparison & Model C Chronological OOS Check
We compared Models A, B, and C across walk-forward player-level out-of-sample correlation (`2022–2024` scores predicting `2025–2026` shrunk WP impact across `70` common batters and `88` common bowlers), Leave-One-Season-Out (LOSO) stability, bootstrap CI width, and delivery-level OOS calibration (`model_comparison.csv`, `model_c_oos_validation.csv`):

| Role | Model | OOS Player $\rho$ | LOSO Mean $\rho$ (Top-10 Overlap) | Boot Med CI Width | Cal. Slope (`22-24 -> 25-26`) | Brier $\Delta$ vs Additive | Selection Score | Selected |
|---|---|---:|---:|---:|---:|---:|---:|---|
| **Batter** | Model A (Abs Pressure) | -0.022 | 0.904 (`7.4/10`) | 39.3 | — | — | 0.579 | False |
| **Batter** | **Model B (Maint & Lift)** | -0.054 | **0.905** (`7.0/10`) | **36.6** | — | — | **0.633** | **True** |
| **Batter** | Model C (Ridge/Logit) | -0.046 | 0.904 (`7.2/10`) | — | **0.653** | +0.00010 | 0.280 | False |
| **Bowler** | Model A (Abs Pressure) | +0.158 | 0.935 (`6.8/10`) | 46.9 | — | — | 0.652 | False |
| **Bowler** | **Model B (Maint & Lift)** | +0.152 | **0.937** (`6.4/10`) | **44.0** | — | — | **0.716** | **True** |
| **Bowler** | Model C (Ridge/Logit) | +0.143 | 0.931 (`6.4/10`) | — | **0.604** | +0.00003 | 0.356 | False |

Why Model B beats Model C and why forward batting correlation is near-zero:
1. **Model C Overfits Interactions OOS:** Across `74,212` batter test deliveries (`340` matches, `2022–2024` $\to$ `2025–2026`), `Context_Pressure_Only` achieves a well-calibrated logistic slope of **`0.974`** (`Brier = 0.05194`), whereas adding `Player x Pressure` interactions degrades slope to **`0.653`** (`Brier = 0.05216`, `max_decile_cal_err = 0.0321` vs `0.0035`) while explaining only $R^2 = 0.0090$ of ball-by-ball runs variance (`RMSE = 1.779`, cluster SE `0.0103`). Bowler interactions show the exact same pattern (calibration slope drops from **`1.002`** to **`0.604`** across `73,894` test balls).
2. **Empirical Variance vs. Predictive Claims in T20 Batting:** Bowlers exhibit persistent year-to-year OOS pressure skill correlation ($\rho = +0.152$), whereas batter future pressure impact across 2-year splits exhibits high stochastic dispersion ($\rho = -0.054$ for Model B, $-0.022$ for Model A). We candidly disclose that in modern T20 cricket, batter performance under pressure displays severe match-to-match variance, tactical order shuffling, and mean reversion. Consequently, Model V2 is presented not as an infallible predictive crystal ball, but as an exceptionally robust, leakage-free historical evaluation engine.
3. **Domain Bonus Independence:** As disclosed in Section 4.5, Model B leads Model A even when removing the `+0.05` domain bonus (Batters: `0.5827` vs `0.5787`; Bowlers: `0.6659` vs `0.6525`). While Model A has a slightly less negative forward OOS correlation for batters (`-0.022` vs `-0.054`), Model B is chosen on the complete multi-criteria trade-off: tighter bootstrap confidence intervals (`36.6` vs `39.3`), superior Leave-One-Season-Out stability (`0.905` / `0.937`), and direct reward for maintaining performance relative to baseline without penalizing elite all-weather performers.

### 8.2 Multi-Axis Robustness: LOSO, Format, Pressure, Eligibility & Wicket Value

| Sensitivity Axis | Tested Variants | Batter Spearman $\rho$ (Top-10 Overlap) | Bowler Spearman $\rho$ (Top-10 Overlap) | Key Finding |
|---|---|---|---|---|
| **LOSO (Drop 1 Season)** | Drop `2022`, `2023`, `2024`, `2025`, `2026` | `0.832–0.950` (`5–9/10`; mean `0.905`) | `0.921–0.957` (`4–8/10`; mean `0.937`) | Dropping 2024 impacts batters most (`0.832`, when Wade/Karthik peaked); dropping 2025 drops Kishore/Muqeem (`4/10` overlap). |
| **Pressure Function** | Center `0.40/0.45`, Scale `0.12`, HP `0.45/0.55`, Linear $PI_t$ | `0.972–0.998` (`9–10/10`) | `0.984–0.999` (`9–10/10`) | Rankings are virtually invariant to sigmoid center/scale and linear weighting (`9–10/10` overlap). |
| **Eligibility Gate** | `200/80/8`, `400/150/12`, `500/180/15`, `150 N_eff`, V1 `lp>=60` | `0.999–1.000` (`8–10/10`) | `0.999–1.000` (`6–10/10`) | Pool ordering is $\rho > 0.999$; strict gates (`500/180/15`) drop emerging/low-N stars (`Wade`, `Kishore`, `Muqeem`, `Overton`, `Mohsin`). |
| **Wicket Value** | Fixed `w = 4, 6, 8` vs `Context Marginal` (`mean = 7.823`) | `0.954–0.983` (`9/10`) | `0.966–0.988` (`7–9/10`) | Fixed `w=4/8` keeps `9/10` overlap; `context_marginal` elevates high-wicket spinners (`Muqeem` #1, `Kuldeep` #7, `Varun` #10). |
| **Format Scope** | `IPL + FullMember T20I` (`784` m) vs `IPL-only` (`367` m) vs `T20I-only` (`470` m) | FullMem `0.993` (`10/10`); IPL `0.940` (`7/10`); T20I `0.926` (`2/10`) | FullMem `0.994` (`9/10`); IPL `0.894` (`6/10`); T20I `0.899` (`4/10`) | Removing Associate T20Is preserves `10/10` batters & `9/10` bowlers; IPL-only highlights `Dinesh Karthik #1`, `Shashank`, `Rinku`, `Ashutosh`, `Narine #1`, `Mohit`, `Kishore`. |

### 8.3 Near-Miss Candidates (`near_miss_candidates.csv`)
Tracking `45` near-miss batters and `47` near-miss bowlers highlights high-volume stars who fell just short of the `hp_balls >= 120` or `hp_matches >= 10` benchmark gates:
- **Phil Salt (`5553`, Batter):** `1,643` total balls and **`354.8` Kish $N_{\text{eff}}$**, with an elite `+32.89` shrunk WP impact, missed solely due to **`hp_balls = 112 < 120`** and **`hp_matches = 9 < 10`** (enters the Top 10 immediately at **#8** under the lenient `200/80/8` gate!).
- **Virat Kohli (`47`, Batter):** `2,456` total balls (`621.7` $N_{\text{eff}}$), missed on `hp_balls = 114 < 120` (shrunk WP impact `+5.14`).
- **Harpreet Brar (`7325`, Bowler):** `667` total balls (`277.8` $N_{\text{eff}}$), missed on `hp_balls = 116 < 120` (`-1.23`).

![Model Robustness, Walk-Forward Validity & Sensitivity](file:///c:/Users/LENOVO/OneDrive/Desktop/SupeRR-Selector-Season-2/outputs/model_v2/charts/11_model_sensitivity_comparison.png)
*Figure 11 (`11_model_sensitivity_comparison.png`): Model A/B/C OOS validity (left), Leave-One-Season-Out Spearman $\rho$ stability (center), and wicket-value sensitivity across `w = 4, 6, 8` and non-overlapping `Context Marginal` valuation (right).*

---

## 9. Rajasthan Royals Strategic Recommendations (Practical IPL 2027 Feasibility)

> [!NOTE]
> **Strict Separation:** Every player's Rank `1–10` reflects **only** 2022–2026 on-field statistics. External franchise, retirement, injury, and BCCI policy flags below (`outputs/model_v2/auction_feasibility.csv`, accessed `2026-11-12`) guide practical Rajasthan Royals (RR) IPL 2027 mini-auction strategy without altering statistical ranks.

### 9.1 RR 2026 Context & Identified 2027 Squad Needs
Cross-referencing the official 2026 squad mapping (`competition_team_player_mapping.csv`, `team_id = 3`, `comp_id = 3298`) with ball-by-ball performance records across 16 IPL 2026 matches defines the complete 27-player squad under head coach **Kumar Sangakkara** and captain **Riyan Parag** (who finished **4th**, defeated SRH in the Eliminator, and fell in Qualifier 2):
- **Top-Order Dominance:** **Vaibhav Sooryavanshi** (776 runs, 327 balls, SR 237.31) and **Yashasvi Jaiswal** (427 runs, 280 balls, SR 152.50) established an elite left-handed opening partnership, eliminating any need for top-order overseas accumulators like Reeza Hendricks (#5).
- **Middle-Order Foundation:** **Dhruv Jurel** (515 runs, SR 154.65, 84 HP balls) and **Riyan Parag** (309 runs, SR 157.65) provided stable middle-overs consolidation.
- **Lower-Order Finishing Fragility:** **Shimron Hetmyer** suffered an output decline in 2026 across 8 squad appearances (7 batting innings: 78 runs, 69 balls, SR 113.04, boundary percentage 8.7%), placing an unsustainable burden on **Donovan Ferreira** (317 runs, SR 179.10) and Dhruv Jurel. RR seeks a high-upside Indian death-overs finisher to complement Jurel and Hetmyer.
- **Spin Attack Imbalance:** Frontline wrist-spinner **Ravi Bishnoi** claimed 11 wickets in 26.0 overs but conceded a **Full-Season ER of 9.88** (Death ER 11.25 on 24 balls; High-Pressure ER 10.00 on 87 balls) due to a lack of containment from the opposite end. Meanwhile, senior all-rounder **Ravindra Jadeja** (age 37–38) was bowled for only 33.0 overs in 16 matches (2.06 overs/match, ER 8.27), operating as a specialist batting all-rounder (#7, 266 runs) rather than a 4-over defensive anchor.
- **Pace Bowling Over-Burdened:** **Jofra Archer** was magnificent (25 wickets in 60.0 overs, Full-Season ER 9.32, Death ER 9.35, High-Pressure ER 8.27), but support death bowling collapsed: veteran **Sandeep Sharma** conceded a **Full-Season ER of 11.39** (19.7 overs; Death ER 13.70 on 46 balls; High-Pressure ER 10.34 on 58 balls) and **Tushar Deshpande** leaked a **Full-Season ER of 11.96** (23.0 overs; Death ER 12.38 on 48 balls; High-Pressure ER 14.08 on 26 balls).

### 9.2 Tactical Case Study: Why R. Sai Kishore Complements Ravi Bishnoi & Ravindra Jadeja
A frequent critique in recruitment analytics is: *"Why pursue another left-arm finger spinner when Rajasthan Royals already roster Ravindra Jadeja?"* Forensic analysis proves that **R. Sai Kishore does not duplicate Ravindra Jadeja or Ravi Bishnoi—he provides the defensive geometry that unlocks both of them:**
1. **Geometric Trajectory vs Flat Darts:** Jadeja releases flat darts at 94–102 kph from a 1.85m height, which right-handed batters can pull off the back foot on true tracks. In contrast, Sai Kishore uses a **6ft 3in frame and 2.28m release height** at 86–92 kph to generate steep bounce, downward dip, and natural angle across right-handers, yielding an exceptional **48.4% dot-ball rate** and a **6.01 pressure economy rate** ($PI \ge 0.50$).
2. **The "Dot-Pressure" Squeeze with Ravi Bishnoi:** Ravi Bishnoi conceded 9.88 RPO overall (and 10.00 RPO in high pressure) in 2026 because opposing batters took low-risk singles from the other end. Sai Kishore builds suffocating pressure from the High Court End, starving batters of boundaries and forcing them to attack Bishnoi's wrong-un, creating high-risk dismissal opportunities.
3. **Middle-Overs Squeeze & Workload Management:** Across the 2022–2026 primary dataset, Sai Kishore operates overwhelmingly as a **middle-overs restrictive anchor** (366 balls / 61.0 overs in Overs 7–16, ER 8.54, 23 wickets; only 3.0 overs in Powerplay). Deploying Sai Kishore for 3–4 middle overs chokes scoring and allows Ravindra Jadeja to bowl 2 tailored matchup overs while preserving 100% of his physical energy for lower-order batting.

### 9.3 Practical IPL 2027 Feasibility & Actionable Shortlist
Every player's Rank `1–10` reflects **strictly 2022–2026 on-field statistics**. External availability context (`outputs/submission/AUCTION_TARGET_DECISION_MATRIX.csv`) categorizes candidates into four practical operational tiers:

| Feasibility Tier | Player Name | Target Role | Key Metric | Practical IPL 2027 Context & Actionability |
|:---|:---|:---|:---|:---|
| **Priority 1 (Primary Actionable Targets)** | **Ashutosh Sharma** (`#10` Bat) | Indian Death Finisher | Death SR 200.74, Impact +24.97 | **Top Domestic Batting Target:** High-upside domestic finishing option (42.3% conditional Top-10 bootstrap reliability on 662 valid draws; 17 qual matches); complements Jurel and Hetmyer; DC release candidate. |
| **Priority 1 (Primary Actionable Targets)** | **R. Sai Kishore** (`#6` Bowl) | Domestic Defensive Spinner | Pressure ER 6.01, Dot% 48.4% | **Top Domestic Bowling Target:** High-control middle-overs squeeze specialist (81.3% conditional Top-10 bootstrap reliability on 455 valid draws; 7 qual matches; 61.0 ov Middle ER 8.54); addresses RR boundary leakage; GT trade/auction target. |
| **Priority 1 (Primary Actionable Targets)** | **Mustafizur Rahman** (`#3` Bowl) | Overseas Death Specialist | Pressure ER 8.24, Impact +8.04 | **Top Overseas Bowling Target:** BCB registration process initiated (pending BCCI shortlisting; pre-IPL 2026 KKR release noted as risk factor); death cutter partner to Archer; cures Sandeep (Full ER 11.39 / Death ER 13.70) and Deshpande death leakage. |
| **Priority 2 (Contingent Targets)** | **Tim David** (`#1` Bat, RCB), **Naman Dhir** (`#3` Bat, MI), **Shashank Singh** (`#6` Bat, PBKS), **Mohsin Khan** (`#8` Bowl, LSG), **Jamie Overton** (`#4` Bowl, CSK), **Josh Hazlewood** (`#10` Bowl, RCB) | Various Elite Roles | Composite Scores `1.472 – 2.434` | Tactically elite fits, but all are expected franchise retentions ahead of the **2026-11-17 deadline** or carry injury recovery management (Overton thigh injury; Hazlewood 151-day layoff). High-priority trade targets if released. |
| **Priority 3 (Near-Miss Watchlist)** | **Phil Salt** (`5553`, Batter), **Harpreet Brar** (`7325`, Bowler), **Nuwan Thushara** (`6571`, Bowler) | Keeper / Spin / Slinger | Near-miss sample gates (`112–116` HP balls) | **Phil Salt** (1,643 balls, PP SR 178.4) is the premier contingency target if RR seeks an explosive opening keeper; **Harpreet Brar** is direct backup to Sai Kishore; **Nuwan Thushara** (18.4% yorkers) is cost-effective death pace backup. |
| **Priority 4 (Non-Actionable Historical Leaders)** | **Sunil Narine** (`#1` Bowl), **Jasprit Bumrah** (`#2` Bowl), **Heinrich Klaasen** (`#7` Bat), **Rinku Singh** (`#8` Bat) | Marquee Elites | Composite Scores `1.445 – 2.481` | Franchise-locked core pillars (KKR icon, MI INR 18 Cr, SRH INR 23 Cr, KKR vice-captain) included on unbiased historical merit. |
| **Priority 4 (Non-Actionable Historical Leaders)** | **Matthew Wade** (`#2` Bat), **Dinesh Karthik** (`#4` Bat), **Andre Russell** (`#9` Bat), **Mohit Sharma** (`#5` Bowl) | Retired Champions | Composite Scores `1.434 – 2.267` | Non-actionable as active players: Wade (Aus batting coach, Sep 2026), Karthik (RCB coach), Russell (KKR Power Coach, retired IPL Nov 2025), Mohit (CSK coach, retired Dec 2025). |
| **Priority 4 (Non-Actionable Historical Leaders)** | **Sufiyan Muqeem** (`#7` Bowl), **Mohammad Nawaz** (`#9` Bowl), **Reeza Hendricks** (`#5` Bat) | International Specialists | Composite Scores `1.556 – 1.745` | Muqeem and Nawaz have no demonstrated IPL participation pathway, with historical non-participation and geopolitical/governance uncertainty. Hendricks represents complete top-order overseas redundancy with Jaiswal/Sooryavanshi. |

![Rajasthan Royals Recruitment Fit Matrix](file:///c:/Users/LENOVO/OneDrive/Desktop/SupeRR-Selector-Season-2/outputs/model_v2/charts/12_rr_recruitment_fit_matrix.png)
*Figure 12 (`12_rr_recruitment_fit_matrix.png`): Model V2 composite statistical score vs IPL high-pressure ball share (%), overlaid with separate practical IPL 2027 feasibility categories (`Active IPL Pool`, `Retired / Coaching`, `No Demonstrated IPL Pathway`, `Zero IPL Exposure`, `Current RR Core`).*

---

## 10. Risks & Limitations

1. **No Fielding or Dropped-Catch Attribution:** `ball_by_ball.csv` tracks batting/bowling outcomes only; dropped catches, misfields, and tactical captaincy/field placements cannot be separated from bowler/batter credit.
2. **Missing & Noisy Ball Speeds (`38.74%` Sentinel `0.0`):** `bowl_speed` contains `77,861` `0.0` sentinels (`38.74%`) and speed-gun outliers (`> 165 km/h` up to `1456.1 km/h`), precluding delivery-level pace-velocity modeling.
3. **Model C Calibration Degradation & Stochastic T20 Variance:** Regularized player $\times$ pressure interaction models overfit ball-by-ball dismissal logits (`OOS cal_slope = 0.653` batters, `0.604` bowlers), and batting future pressure performance exhibits substantial match-to-match noise ($\rho \approx -0.05$ across 2-year splits).
4. **Borderline Sample-Size & Format Imbalance Sensitivity:** Players near the `120` HP-ball threshold (`Sai Kishore` `123`, `Sufiyan Muqeem` `148`, `Matthew Wade` `158`, `Mohsin Khan` `163`, `Jamie Overton` `165`) experience `168–545` ineligible bootstrap draws out of `1,000`. Similarly, T20I-only specialists (`Reeza Hendricks`, `Sufiyan Muqeem`, `Mohammad Nawaz`) cannot be directly observed against IPL tactical depth.
5. **Unverified IPL 2027 Auction Register (As of 2026-11-12):** Official retention lists (**2026-11-17**), final auction registers (**2026-12-03**), and mini-auction outcomes (**2026-12-16**) remain unpublished at submission drafting; all IPL 2027 availability statuses are explicitly labeled `Unverified`.

---

## 11. Conclusion

**Model V2 (`model_b`)** establishes a statistically rigorous, leakage-free, and domain-faithful foundation for evaluating T20 reliability under pressure across **837 matches** and **193,988 deliveries**. By replacing V1's `lp_balls >= 60` trap, unshrunk match-streak inflation, and 1:1 `HP − LP` elite-baseline penalty with continuous sigmoid pressure weighting, Kish effective sample sizing, Leave-Player-Out hierarchical context baselines (with chronological Elo and dynamic batting roles), and double Empirical-Bayes shrinkage, Model V2 accurately honors both death-over finishers (`Tim David`, `Naman Dhir`, `Shashank Singh`, `Rinku Singh`, `Ashutosh Sharma`) and elite all-phase bowlers (`Sunil Narine`, `Jasprit Bumrah`, `Mustafizur Rahman`, `Josh Hazlewood`). Combined with transparent 1,000-resample bootstrap uncertainty and strictly separated IPL 2027 practical feasibility intelligence, the rankings and strategic recommendations are ready for Round 1 submission.

---

## 12. References

### Statistical & Sports Analytics Methodology
1. **Kish, L. (1965).** *Survey Sampling.* John Wiley & Sons. (Effective sample size $N_{\text{eff}} = (\sum w_i)^2 / \sum w_i^2$ for weighted estimators.)
2. **Efron, B., & Morris, C. (1975).** Data analysis using Stein's estimator and its generalizations. *Journal of the American Statistical Association*, 70(350), 311–319. (Empirical-Bayes shrinkage.)
3. **Elo, A. E. (1978).** *The Rating of Chessplayers, Past and Present.* Arco Publishing. (Chronological rolling strength ratings.)
4. **Stern, S. E. (2009).** An adjusted Duckworth-Lewis target in shortened limited-overs cricket matches. *Journal of the Operational Research Society*, 60(2), 236–251. (Resource/wicket-value framing in limited-overs cricket.)
5. **Competition Problem Statement:** *SupeRR Selector Season 2 — Round 1 Problem Statement*, Rajasthan Royals & Unstop (`data/raw/Round 1 Problem Statement _ SupeRR Selector Season 2.docx.pdf`).

### Verified Public Cricket & Governance Sources (Accessed `2026-11-12` — Full 52-Row Register in `outputs/submission/source_register.md`)
6. **BCCI / IPL 2027 Rules & Schedule:** *Mint* (2026-11-08), *IPL 2027 retentions explained: Player salaries, auction budgets and the decisions facing all 10 teams* (`Reputable Media`) — https://www.livemint.com/sports/cricket-news/ipl-2027-retentions-explained-player-salaries-auction-budgets-and-the-decisions-facing-all-10-teams-11794138863732.html
7. **Rajasthan Royals 2026–2027 Squad Needs:** *Hindustan Times* (2026-11-12), *IPL 2027: Rajasthan Royals face tough retention calls amid bowling struggles and uncertainty over expensive recruits* (`Reputable Media`) — https://www.hindustantimes.com/cricket/ipl/ipl-2027-rajasthan-royals-face-tough-retention-calls-amid-bowling-struggles-and-uncertainty-over-expensive-recruits-101794489114888.html
8. **Confirmed IPL 2026/2027 Trades:** *IPLT20 Official* (2026-11-11), *Hardik Pandya and Arshdeep Singh complete major trade between PBKS and MI* (`Official`) — https://www.iplt20.com/news/article/hardik-pandya-and-arshdeep-singh-complete-major-trade-between-pbks-and-mi ; *IPLT20 Official* (2026-06-23), *Rishabh Pant and Kuldeep Yadav complete high-profile trade between DC and LSG* (`Official`) — https://www.iplt20.com/news/article/rishabh-pant-and-kuldeep-yadav-complete-high-profile-trade-between-dc-and-lsg ; *The Indian Express* (2025-11-15), *Sanju Samson–Ravindra Jadeja RR/CSK trade* (`Reputable Media`) — https://indianexpress.com/article/sports/cricket/ipl-2026-retention-sanju-samson-csk-jadeja-rr-trade-deal-confirmed-10366973/
9. **Top-10 Batter Sources:** Tim David — *The Indian Express* (2026-04-11, `Reputable Media`, https://indianexpress.com/article/sports/cricket/tim-david-returns-rcb-finisher-mumbai-indians-wankhede-ipl-10631498/); Matthew Wade — *CricTracker* (2026-09-17, `Reputable Media`, https://www.crictracker.com/cricket-news/matthew-wade-announces-bbl-retirement-to-take-up-full-time-coaching-role-8665/); Naman Dhir — *Mumbai Indians Official* (2026-09-17, `Official`, https://www.mumbaiindians.com/news/ala-re-ala-naman-dhir-gets-maiden-india-squad-callup); Dinesh Karthik — *India TV News* (2024-07-01, `Reputable Media`, https://www.indiatvnews.com/sports/cricket/dinesh-karthik-becomes-rcb-s-batting-coach-mentor-ahead-of-ipl-2025-after-retiring-from-cricket-2024-07-01-939655); Reeza Hendricks — *Betway SA20 Official* (`Official`, https://www.sa20.co.za/player/reeza-hendricks); Shashank Singh — *InsideSport* (2024-03-19, `Reputable Media`, https://www.insidesport.in/cricket/players/shashank-singh/); Heinrich Klaasen — *The Hindu* (2025-06-02, `Reputable Media`, https://www.thehindu.com/sport/cricket/heinrich-klaasen-retires-from-international-cricket-in-a-blow-to-south-african-cricket/article69648484.ece); Rinku Singh — *Rediff Cricket* (2026-03-24, `Reputable Media`, https://m.rediff.com/cricket/report/rinku-singh-named-kkr-vice-captain-for-ipl-2026/20260324.htm); Andre Russell — *The Hindu* (2025-11-30, `Reputable Media`, https://www.thehindu.com/sport/cricket/andre-russell-announces-retirement-from-ipl-joins-kkr-support-staff-as-power-coach/article70341366.ece); Ashutosh Sharma — *Delhi Capitals Official* (`Official`, https://www.delhicapitals.in/players/68176-ashutosh-sharma-profile).
10. **Top-10 Bowler Sources:** Sunil Narine — *Times of India* (2026-05-03, `Reputable Media`, https://timesofindia.indiatimes.com/sports/cricket/ipl/ipl-2026/ipl-2026-sunil-narine-scripts-history-becomes-the-first-overseas-player-to-claim-200-ipl-wickets/articleshow/130731835.cms); Jasprit Bumrah — *Mumbai Indians Official* (`Official`, https://www.mumbaiindians.com/players/63755-jasprit-bumrah-profile); Mustafizur Rahman — *India Today* (2026-11-11, `Reputable Media`, https://www.indiatoday.in/sports/cricket/story/ipl-2027-mini-auction-bangladesh-mustafizur-rahman-exclusive-kkr-release-3036897-2026-11-11); Jamie Overton — *IPLT20 Official* (2026-05-14, `Official`, https://www.iplt20.com/news/article/dian-forrester-named-replacement-for-injured-jamie-overton); Mohit Sharma — *Times of India* (2026-09-29, `Reputable Media`, https://timesofindia.indiatimes.com/sports/cricket/ipl/mohit-sharma-likely-to-join-csk-as-bowling-coach/articleshow/134561311.cms); Sai Kishore — *Times of India* (2026-08-03, `Reputable Media`, https://timesofindia.indiatimes.com/sports/cricket/news/i-shouldnt-have-done-it-sai-kishore-breaks-silence-on-playing-just-three-ipl-2026-games/articleshow/132835375.cms); Sufiyan Muqeem — *CricTracker* (2026-06-25, `Reputable Media`, https://www.crictracker.com/cricket-news/pakistans-sufyan-moqim-to-replace-am-ghazanfar-at-derbyshire-for-2026-t20-blast/); Mohsin Khan — *Rediff Cricket* (2026-04-27, `Reputable Media`, https://m.rediff.com/cricket/report/ipl-2026-lsg-kkr-mohsin-khans-india-debut-hinges-on-fitness-says-irfan-pathan/20260427.htm); Mohammad Nawaz — *CricTracker* (`Reputable Media`, https://www.crictracker.com/cricket-players/mohammad-nawaz/); Josh Hazlewood — *Rediff Cricket* (2026-04-17, `Reputable Media`, https://m.rediff.com/cricket/report/ipl-2026-hazlewood-opens-up-on-151-day-injury-nightmare/20260417.htm).
