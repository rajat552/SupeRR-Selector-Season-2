# 04 — V2 Analytical Methodology

This document specifies the complete statistical and cricket-engineering methodology of the remediated **Model V2** pipeline (`src/model_v2/`), resolving all **seven methodological issues** identified during the Phase 0.5 audit of V1 (`src/`).

---

## 1. Primary Dataset Scope & Cricket Accounting (`data_loader.py`, `cricket_accounting.py`)

Starting from the raw competition tables (`200,999` deliveries across `883` scheduled matches from `2022-01-22` to `2026-11-01`):

- **Primary Scope Exclusions:**
  1. Excluded `16` abandoned matches with `0` deliveries in `ball_by_ball.csv`.
  2. Excluded `30` non-IPL `T20` A-team matches (`comp_id` `2670`, `3289`; `6,985` deliveries).
  3. Excluded `38` Super Over deliveries (`innings` $\in \{3, 4\}$ across `6` matches).
  - **Primary Analysis Dataset:** **837 matches** (`367` IPL, `470` T20I), **193,988 deliveries**, **185,692 legal balls**, and **186,516 batter balls faced**.
- **Player Identity:** Every join, baseline, shrinkage step, and aggregation keys strictly on `player_id` (`striker_id`, `bowler_id`), preserving homonyms (`Abdul Samad` `7446` vs `6922`; `Rashid Khan` `4722` vs `20172`; `Haider Ali` `7338` vs `28756`). `playing_eleven.csv` (`28,381` rows) is deduplicated on `(match_id, team_id, player_id)` keeping `is_played == True` first (`40` key duplicates resolved).
- **Exact Cricket Accounting Rules:**
  - `is_wide = (extras_type == 'wide')`; `is_noball = extras_type.isin(['Overstep', 'other'])`.
  - `is_legal_ball = ~(is_wide | is_noball)`; `is_batter_ball_faced = ~is_wide`.
  - `total_runs = runs + extras1_runs + extras_2_runs`.
  - `bowler_runs_conceded = runs + extras1_runs` if `(is_wide | is_noball)` else `runs` (`byes`, `legbyes`, and `Penalty` excluded).
  - `dismissal_type` typo `Obstracting the field` is normalized to `Obstructing the field`; `is_bowler_wicket = is_wicket & dismissal_type.isin({'Caught', 'Bowled', 'LBW', 'Stump', 'Hit Wicket'})`; `is_striker_dismissed = is_wicket & (dismissed_player_id == striker_id)`.

---

## 2. Zero-Look-Ahead Match State & Chronological Opponent Elo (`state_builder.py`, `opponent_strength.py`)

### 2.1 Pre-Delivery State
Deliveries are sorted chronologically within `(match_id, innings, overid, over_ball_num)`. For delivery $t$:
- `inn_max_balls` uses `first_inn_revised_overs` / `second_inn_revised_overs` **directly as balls** when non-null (default `120.0`).
- `pre_runs`, `pre_wickets`, and `pre_legal_balls` are computed via exclusive cumulative sums (`cumsum - current`).
- `pre_balls_remaining = max(1.0, inn_max_balls - pre_legal_balls)`.
- `pre_crr = 6.0 * pre_runs / pre_legal_balls` (or `0.0` if `pre_legal_balls == 0`).
- `target` (innings 2) uses `revised_target` when non-null, else `inn1_total_runs + 1.0`.
- `pre_rrr = min(36.0, 6.0 * max(0.0, target - pre_runs) / pre_balls_remaining)`.
- `phase`: `Powerplay` (`overid <= 6`), `Middle` (`7 <= overid <= 15`), `Death` (`overid >= 16`).

### 2.2 Strictly Chronological Pre-Match Opponent Elo
To control for opponent quality across `IPL` and `T20I` without any data leakage or bootstrap recomputation bias:
- **Separate Tracks:** `IPL` and `T20I` Elo ratings are maintained independently (`base_elo = 1500.0`, `k_factor = 24.0`, logistic scale `400.0`).
- **Date-Batched Updates:** Matches are sorted by `(comp_category, match_date, match_number, match_id)`. All matches on date $D$ read team ratings produced **strictly from `match_date < D`**; updates from date $D$ are buffered and applied only after every match on date $D$ has recorded its pre-match Elos. `No Result` and `Match Abandoned` leave ratings unchanged; ties without `win_team_id` score `0.5`.
- **Deterministic Opponent Tiers (`opp_tier_bat`, `opp_tier_bowl`):**
  - `Low`: $\text{Elo} < 1480.0$ (`61,911` batter / `61,812` bowler deliveries)
  - `Mid`: $1480.0 \le \text{Elo} < 1525.0$ (`73,603` batter / `74,264` bowler deliveries)
  - `High`: $\text{Elo} \ge 1525.0$ (`58,474` batter / `57,912` bowler deliveries)
- Pre-match Elo is attached to every delivery prior to resampling so bootstrap draws never leak future match results.

---

## 3. Continuous Pressure Weighting & Kish Effective Sample Size (`pressure_model.py`)

V2 retains the V1 Pressure Index $PI_t \in [0, 1]$ (`52,002` HP balls at $PI_t \ge 0.50$ [`26.81%`], `115,116` LP balls at $PI_t < 0.35$ [`59.34%`], `26,870` intermediate balls at $0.35 \le PI_t < 0.50$ [`13.85%`]) for interpretability and regime gating, while eliminating the `13.85%` data-discard gap via smooth continuous weights over **all 193,988 deliveries**:

$$w_t = \sigma\left(\frac{PI_t - 0.425}{0.08}\right) = \frac{1}{1 + \exp\left(-\frac{PI_t - 0.425}{0.08}\right)}, \qquad w_t^{\text{norm}} = 1 - w_t$$

- Center `0.425` sits at the midpoint between V1's `0.35` and `0.50` thresholds (`mean w_t = 0.3512`, range `[0.0049, 0.9992]`).
- **Kish Effective Sample Size ($N_{\text{eff}}$):** Because continuous weights vary across deliveries, raw exposure $\sum w_t$ overstates precision. V2 quantifies effective pressure and normal-pressure sample sizes via Kish's formula:

$$N_{\text{eff}, i} = \frac{\left(\sum_{t \in \mathcal{D}_i} w_t\right)^2}{\sum_{t \in \mathcal{D}_i} w_t^2}$$

---

## 4. Dynamic Roles & Leave-Player-Out (LPO) Context Baselines (`batting_features.py`, `bowling_features.py`, `context_baselines.py`)

- **Dynamic Batting Roles:** Mapped from delivery `batting_order` (falling back to deduplicated `playing_eleven.batting_order`) into `Top 1-3` (`96,514` deliveries), `Middle 4-5` (`52,148`), and `Finisher 6+` (`45,326`), flagging `255` role mismatches and `358` uncertain-role deliveries.
- **Bowling Features:** Standardizes `pace_or_spin`, `bowling_arm`, `bowling_style_group` (`Pace_Fast`, `Pace_FastMedium`, `Pace_Medium`, `Spin_Wrist`, `Spin_Finger`), and zero-look-ahead `bowler_pre_legal_balls_in_inn`.
- **Leakage-Safe Leave-Player-Out (LPO) Hierarchical Baselines:** For every player $i$ and finest cell $c$, player $i$'s own deliveries are subtracted ($n_{-i, c} = n_c - n_{i, c}$). Whenever $n_{-i, c} < 50$ (`DEFAULT_MIN_CELL_N = 50`), the lookup walks up the hierarchy until $n_{-i, c_L} \ge 50$:
  - **Batting Hierarchy (6 levels):** `(comp_tier, season_year, phase, batting_role, opp_tier_bat)` $\to$ drop `opp_tier_bat` $\to$ drop `batting_role` $\to$ `(comp_tier, phase)` $\to$ `(phase)` $\to$ global LPO. (`191,674` / `98.81%` of deliveries resolve at finest Level 0; `1,815` at Level 1; `499` at Level 2.)
  - **Bowling Hierarchy (6 levels):** `(comp_tier, season_year, phase, pace_or_spin, opp_tier_bowl)` $\to$ drop `opp_tier_bowl` $\to$ drop `pace_or_spin` $\to$ `(comp_tier, phase)` $\to$ `(phase)` $\to$ global LPO. (`193,027` / `99.50%` resolve at Level 0; `813` at Level 1; `148` at Level 2.)

---

## 5. Delivery Impact, Empirical Bayes Shrinkage & Eligibility (`shrinkage.py`, `eligibility.py`, `impact_models.py`)

- **Delivery Impact Residuals:**
  - **Batting (per 100 balls faced):** $I_{t}^{\text{bat}} = (r_t - \text{ctx\_bat\_rpb}_t) + V_w \cdot (\text{ctx\_bat\_out\_prob}_t - \text{out}_t)$, scaled by $100 / \sum w_t$.
  - **Bowling (per 24 legal balls):** $I_{t}^{\text{bowl}} = (\text{ctx\_bowl\_rpb}_t \cdot \ell_t - c_t) + V_w \cdot (\text{wkt}_t - \text{ctx\_bowl\_wkt\_prob}_t \cdot \ell_t)$, scaled by $24 / \sum w_t \ell_t$.
  - Canonical wicket value $V_w = 6.0$, cross-checked against a non-overlapping Ridge-based context-marginal wicket value model (`mean = 7.82` across `240` `(comp_tier, innings, over_bucket, pre_wickets)` cells, predicting strictly remaining post-delivery runs `inn_total_runs - post_runs` to guarantee zero double-counting).
- **Empirical Bayes Impact Shrinkage ($k = 120.0$):** Shrunk toward prior `0.0` using Kish $N_{\text{eff}}$:

$$\hat{\theta}_{i, \text{shrunk}} = \frac{N_{\text{eff}, i}}{N_{\text{eff}, i} + 120.0}\,\hat{\theta}_{i, \text{obs}}$$

- **Beta-Binomial Match Consistency:** Qualifying HP matches (`>= 6` HP balls in a match) with positive HP impact (`hp_pos_matches` out of `hp_qual_m`) are shrunk using an empirical population Beta prior $\text{Beta}(\alpha_0, \beta_0)$ fitted via Beta-Binomial MLE over players with $\ge 3$ qualifying matches:
  - Batters fitted prior: $\alpha_0 = 28.0701,\; \beta_0 = 21.9299$ (prior mean `0.561`, effective prior strength `50.0` matches).
  - Bowlers fitted prior: $\alpha_0 = 25.7405,\; \beta_0 = 19.1077$ (prior mean `0.574`, effective prior strength `44.8` matches).
  - Posterior consistency: $\text{EB\_Cons}_i = \frac{\text{pos}_i + \alpha_0}{m_i + \alpha_0 + \beta_0}$.
- **Eligibility Gate (Benchmark `300 / 120 / 10`, NO `lp_balls >= 60` Trap):**
  - `tot_balls >= 300`, `hp_balls >= 120`, and `hp_matches >= 10`.
  - Yields **99 eligible batters** (up from `54` in V1) and **128 eligible bowlers** (up from `92` in V1), rescuing specialist finishers such as `Ashutosh Sharma` (`lp_balls = 42`).

---

## 6. Stratified Match-Cluster Bootstrap (`bootstrap.py`)

Uncertainty is quantified over **1,000 resamples** (`seed = 42`) stratified strictly by `(comp_category, season_year)`, preserving exact seasonal match counts across IPL (`367`) and T20I (`470`). Inside every iteration, duplicated matches receive unique `boot_match_instance_id`s and **all** LPO baselines, Empirical Bayes shrinkage, empirical Beta-binomial priors, eligibility gates, and z-score standardizations are recomputed from scratch while holding pre-match `opp_elo` fixed.
