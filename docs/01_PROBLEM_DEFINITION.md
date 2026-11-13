# 01 — Problem Definition & V1-to-V2 Remediation Specification

This document translates the Round 1 challenge into a formal statistical estimation problem, summarizes the **seven methodological issues** uncovered by the independent Phase 0.5 audit of the V1 pipeline (`src/`), and defines the V2 remediation targets (`src/model_v2/`).

---

## 1. Formal Problem Framing

Given delivery-level records $t \in \{1, \dots, N\}$ across completed 20-over IPL and T20I matches ($837$ matches, $193{,}988$ deliveries, $185{,}692$ legal balls after excluding $30$ `Other_T20` A-team matches, $16$ zero-delivery abandoned matches, and $38$ Super Over deliveries):

1. **Pre-Delivery State ($S_t$):** Reconstruct the exact match state strictly prior to delivery $t$ (`pre_runs`, `pre_wickets`, `pre_legal_balls`, `pre_balls_remaining`, `pre_crr`, `pre_rrr`, `phase`), honoring D/L revised ball limits (`first_inn_revised_overs` / `second_inn_revised_overs`, stored in balls) and `revised_target`.
2. **Pressure Function ($PI_t \in [0, 1]$):** Map pre-delivery state $S_t$ to a continuous pressure score distinguishing high-leverage match states (collapse recovery, tight chases, late-innings pressure) from routine or already-decided states.
3. **Context-Adjusted Performance Residual ($y_{t} - \hat{\mu}_{c(t)}$):** Measure each delivery's outcome (runs scored/conceded, dismissal/wicket) against a leakage-safe contextual expectation for `(comp_tier, season_year, phase, role/pace_spin, opp_tier)`.
4. **Player Reliability Under Pressure:** Aggregate delivery residuals into:
   - **Absolute Pressure Impact** (performance when $PI_t$ is high),
   - **Pressure Lift / Maintenance** (performance under pressure relative to the player's own baseline without penalizing elite all-weather players),
   - **Shrunk Cross-Match Consistency** (match-to-match repeatability stabilized via Empirical Bayes shrinkage), and
   - **Bootstrap Rank Uncertainty** (stratified match-level resampling intervals).

---

## 2. Independent Audit of V1 (`outputs/model_audit/`)

An independent forensic audit ([audit_summary.md](file:///c:/Users/LENOVO/OneDrive/Desktop/SupeRR-Selector-Season-2/outputs/model_audit/audit_summary.md), [model_formula_audit.md](file:///c:/Users/LENOVO/OneDrive/Desktop/SupeRR-Selector-Season-2/outputs/model_audit/model_formula_audit.md)) verified that the V1 code (`src/*.py`) is **100% mathematically reproducible** (`score_max_abs_err <= 4.44e-16`; `9/9` cricket-accounting unit tests passing), while identifying **seven methodological issues** across three severity tiers:

### Critical Issues (2)

1. **Specialist Finisher Disqualification (`lp_balls >= 60` exclusion)**
   - *V1 Behavior:* Eligibility requires `lp_balls >= 60` ($PI_t < 0.35$).
   - *Verified Impact:* Specialist death-over finishers who predominantly bat under pressure are silently dropped. For example, **Ashutosh Sharma** (`player_id = 8101`) faced `334` total balls and `273` HP balls (`81.7%` of his sample) across `22` HP matches (`hp_impact_100 = +16.55`, `lp_impact_100 = -2.44`, raw lift `+18.99`), yet was excluded solely because `lp_balls = 42 < 60`.
   - *V2 Fix:* Replace the `lp_balls >= 60` gate with overall sample sufficiency (`tot_balls >= 300`, `hp_balls >= 120`, `hp_matches >= 10`) plus a shrunk non-HP / career baseline fallback so high-pressure specialists are retained.

2. **Unshrunk Cross-Match Consistency (`m_balls >= 6`)**
   - *V1 Behavior:* `consistency_rate` (fraction of HP matches with `m_balls >= 6` and `m_impact > 0`) receives a `20%` weight in the final composite z-score with zero Empirical Bayes shrinkage.
   - *Verified Impact:* Players with only `6–8` qualifying HP matches receive extreme z-scores—e.g., **Sai Kishore** (`7/7 = 100%`, `+3.31 SD`), **Reeza Hendricks** (`6/7 = 85.7%`, `+2.45 SD`), **Mohammad Rizwan** (`6/7 = 85.7%`, `+2.45 SD`), alongside `Shai Hope` (`6`) and `Shubman Gill` (`8`)—and exhibit wide bootstrap rank CIs (`p95 = 21–59`).
   - *V2 Fix:* Apply Beta-binomial / Empirical Bayes shrinkage toward `0.50` (and require sufficient effective HP match/ball depth), downweighting small-match streaks smoothly.

### Moderate Issues (3)

3. **Elite-Baseline Penalty (`HP - LP` Delta Confounding)**
   - *V1 Behavior:* Gives `40%` score weight to $\Delta = \text{HP\_Impact} - \max(\text{LP\_Impact}, \text{floor})$, treating a unit of LP excellence as a full 1:1 penalty on delta.
   - *Verified Impact:* Elite all-situation performers have high `LP` baselines that compress or invert their deltas:
     - **Jasprit Bumrah** (`hp_impact_24 = +12.26`, `lp_impact_24 = +5.65`, `shrunk_delta = +5.32`) ranks **#8** behind **Mohit Sharma** (`hp = +9.37`, `lp = -8.02`, raw delta `+17.38`) and **Sai Kishore** (`hp = +17.26`, `lp = -4.37`, raw delta `+21.63`).
     - **Suryakumar Yadav** (`hp_impact_100 = +27.43`, `lp_impact_100 = +37.85`, `shrunk_delta = -8.82`) ranks **#16**; **Rinku Singh** (`hp = +19.20`, `lp = +25.27`, `shrunk_delta = -4.91`) ranks **#24**; **Tim David** (`hp = +42.27`, `lp = +47.22`, `shrunk_delta = -4.09`) ranks **#4**.
   - *V2 Fix:* Separate **maintenance under pressure** from **weak-baseline inflation** using shrunk pressure-weighted modeling / attenuated baseline comparison so elite performers are not penalized for dominating low-pressure overs.

4. **Missing Batting-Role & Opponent-Strength Controls**
   - *V1 Behavior:* Context baselines group only by `(comp_tier, season_year, phase)` (`IPL`, `T20I_Full`, `T20I_Assoc`).
   - *Verified Impact:* Batting expectations do not distinguish `batting_order` roles (`Top 1-3` vs `Middle 4-5` vs `Finisher 6+`), and all `T20I_Full` opponents (e.g., Zimbabwe/Ireland/Bangladesh vs India/Australia) share a single baseline, inflating metrics for bilateral T20I specialists with zero IPL exposure (`Reeza Hendricks`, `Sufiyan Muqeem`, `Mohammad Nawaz`, `Abrar Ahmed`, `Mohammad Rizwan`). Also in-sample baselines include player `i`'s own balls.
   - *V2 Fix:*
     - Compute dynamic batting roles (`Top 1-3`, `Middle 4-5`, `Finisher 6+`) from `playing_eleven.csv` + `ball_by_ball.batting_order`.
     - Compute strictly chronological pre-match rolling **Elo ratings** (`match_date < current_match_date`, separate tracks for `IPL` and `T20I`) to derive `opp_tier`.
     - Compute **Leave-Player-Out (LPO)** hierarchical context baselines across `(comp_tier, season_year, phase, role/pace_spin, opp_tier)` with parent fallback when `(n_cell - n_{i,cell}) < 50`.

5. **Unstratified / Frozen Bootstrap (`n_boot = 300`, `seed = 42`)**
   - *V1 Behavior:* Resamples `837` unique `match_id`s without `IPL`/`T20I` stratification, freezes `pressure_index`, `ctx_*` baselines, and full-sample eligibility gates from the full dataset, and drops `absent` players when `hp_balls == 0` or `lp_balls == 0` in a draw.
   - *V2 Fix:* Use `(comp_category, season_year)` stratified match-level resampling with unique match-instance IDs (`n_boot >= 1000`), recompute baselines/shrinkage inside each resample (while keeping pre-computed pre-match `opp_elo` fixed), and handle borderline/absent draws explicitly.

### Minor Issues (2)

6. **Intermediate-Pressure Gap (`0.35 <= PI_t < 0.50`)**
   - *V1 Behavior:* Discards `26,870` deliveries (`13.85%` of `193,988` primary deliveries—e.g., `408` balls for Suryakumar Yadav) that fall between `LP` (`PI < 0.35`) and `HP` (`PI >= 0.50`).
   - *V2 Fix:* Retain all `193,988` primary deliveries using a continuous pressure weight $w_t \in [0, 1]$ alongside discrete regime reporting and Kish effective sample size $N_{\text{eff}} = (\sum w_t)^2 / \sum w_t^2$.

7. **Inverted Bootstrap Chart Axis & Ambiguous `%` Label**
   - *V1 Behavior:* `plot_bootstrap_ci` inverts the x-axis (placing Rank 1 on the right) and labels `prob_top10` without distinguishing *bootstrap resample inclusion frequency* from future match probability.
   - *V2 Fix:* Plot Rank 1 cleanly on the left and explicitly label bootstrap metrics as `top10_inclusion_frequency` (bootstrap resample inclusion rate).
