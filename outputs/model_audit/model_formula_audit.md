# Model Formula Audit — Exact Reconstruction from Source Code

All formulas below were reconstructed directly from the existing source files (`src/data_loader.py`, `src/state_builder.py`, `src/pressure.py`, `src/baselines.py`, `src/batting_model.py`, `src/bowling_model.py`, `src/validation_tests.py`, `src/run_pipeline.py`).

---

## 1. Source Files & Data Scope (`src/data_loader.py`)
- **Inputs:** All 6 CSVs in `data/raw/` (`competitions.csv`, `teams.csv`, `matches.csv`, `playing_eleven.csv`, `competition_team_player_mapping.csv`, `ball_by_ball.csv`).
- **Competition Filter:**
  - `IPL`: `match_format == 'T20'` AND `'IPL' in comp_name` (367 matches, 87,673 non-super-over deliveries).
  - `T20I`: `match_format == 'T20I'` (470 matches, 106,315 non-super-over deliveries).
  - `Other_T20` (`comp_id` 2670 & 3289, 30 matches, 6,985 deliveries) **excluded**.
  - Super Overs (`innings in {3, 4}`, 38 deliveries across 6 matches) **excluded**.
  - **Primary Scope:** 837 matches, 193,988 deliveries (185,692 legal balls).
- **Delivery & Cricket Accounting:**
  - `is_wide = (extras_type == 'wide')`
  - `is_noball = extras_type.isin(['Overstep', 'other'])`
  - `is_legal_ball = ~(is_wide | is_noball)`
  - `is_batter_ball_faced = ~is_wide` (no-balls count as balls faced; wides do not).
  - `total_runs = runs + extras1_runs + extras_2_runs`
  - `bowler_runs_conceded = runs + extras1_runs` (when `is_wide | is_noball`) else `runs` (byes, legbyes, Penalty excluded from bowler runs).
  - `is_team_wicket = bool(is_wicket)`
  - `is_bowler_wicket = is_team_wicket & dismissal_type.isin({'Caught', 'Bowled', 'LBW', 'Stump', 'Hit Wicket'})`.
- **Player Identity:** Keyed strictly on `player_id` (`striker_id` / `bowler_id`), avoiding homonym collisions (`Abdul Samad` `7446` vs `6922`; `Rashid Khan` `4722` vs `20172`; `Haider Ali` `7338` vs `28756`).

---

## 2. Pre-Delivery Match State (`src/state_builder.py`)
Sorted by `(match_id, innings, overid, over_ball_num)`. For delivery $t$:
- `inn_max_balls` = `first_inn_revised_overs` (already stored in balls) for inn 1, `second_inn_revised_overs` for inn 2, defaulting to `120.0`.
- `pre_runs = cumsum(total_runs) - total_runs`
- `pre_wickets = cumsum(is_team_wicket) - int(is_team_wicket)`
- `pre_legal_balls = cumsum(is_legal_ball) - int(is_legal_ball)`
- `pre_balls_remaining = max(1.0, inn_max_balls - pre_legal_balls)`
- `pre_crr = 6.0 * pre_runs / pre_legal_balls` (if `pre_legal_balls > 0` else `0.0`)
- `target` (innings 2) = `revised_target` if non-null else `inn1_total_runs + 1.0`
- `pre_rrr = min(36.0, 6.0 * max(0.0, target - pre_runs) / pre_balls_remaining)`
- `phase`: `Powerplay` (`overid <= 6`), `Middle` (`7 <= overid <= 15`), `Death` (`overid >= 16`).

---

## 3. Pressure Index & Thresholds (`src/pressure.py`)
- **Par Run Rate (`par_rpo`):** `6.0 * sum(total_runs) / sum(is_legal_ball)` per `(comp_category, season_year)`.
- **Expected Wickets (`exp_wickets`):** Mean `pre_wickets` in innings 1 per `(comp_category, overid)`.
- **1st Innings ($PI_1$):**
  $$S_{\text{collapse}} = \text{clip}\left(\frac{\max(0, W_{\text{pre}} - E[W])}{2.2} + 0.25 \cdot \mathbb{I}[\text{over} \le 6 \land W_{\text{pre}} \ge 2], 0, 1\right)$$
  $$S_{\text{deficit}} = \mathbb{I}[B_{\text{pre}} \ge 18] \cdot \text{clip}\left(\frac{\text{ParRPO} - CRR_{\text{pre}}}{3.0}, 0, 1\right)$$
  $$S_{\text{death1}} = 0.75\cdot\mathbb{I}[\text{over}\ge 16 \land W_{\text{pre}}\le 6] + 0.45\cdot\mathbb{I}[\text{over}\ge 16 \land W_{\text{pre}}>6] + 0.25\cdot\mathbb{I}[12\le \text{over}\le 15]$$
  $$PI_1 = \text{clip}(0.50 S_{\text{collapse}} + 0.30 S_{\text{deficit}} + 0.20 S_{\text{death1}}, 0, 1)$$
- **2nd Innings ($PI_2$):**
  $$\text{ratio} = \frac{RRR_{\text{pre}}}{\max(6.0, \text{ParRPO})}, \quad S_{\text{RRR}} = \text{clip}\left(\frac{\text{ratio} - 0.65}{0.80}, 0, 1\right)$$
  $$S_{\text{wkts2}} = \mathbb{I}[\text{RunsNeeded} > 10] \cdot \text{clip}\left(\frac{W_{\text{pre}} - 1}{5.5}, 0, 1\right), \quad S_{\text{urg2}} = \text{clip}\left(\frac{\text{MaxBalls} - B_{\text{rem}}}{\max(60, \text{MaxBalls})}, 0, 1\right)$$
  $$\text{CFBoost} = 0.20 \cdot \mathbb{I}[B_{\text{rem}}\le 24 \land 0<\text{RunsNeeded}\le 48 \land 0.75\le \text{ratio}\le 2.20]$$
  $$\text{WonDamp} = 0.35\text{ if }(\text{ratio}<0.55 \land W_{\text{hand}}\ge 5)\text{ else }1.0; \quad \text{LostDamp} = 0.40\text{ if }(\text{ratio}>2.20 \land B_{\text{rem}}>18)\text{ else }1.0$$
  $$PI_2 = \text{clip}\left((0.50 S_{\text{RRR}} + 0.30 S_{\text{wkts2}} + 0.20 S_{\text{urg2}} + \text{CFBoost}) \cdot \text{WonDamp} \cdot \text{LostDamp}, 0, 1\right)$$
- **Thresholds:**
  - High Pressure: $PI_t \ge 0.50$ (`52,002` deliveries, `26.81%`).
  - Normal / Low Pressure: $PI_t < 0.35$ (`115,116` deliveries, `59.34%`).
  - Intermediate Gap (excluded from both HP and LP): $0.35 \le PI_t < 0.50$ (`26,870` deliveries, `13.85%`).

---

## 4. Context Baselines (`src/baselines.py`)
Context cells: `comp_tier` (`IPL`, `T20I_Full`, `T20I_Assoc`) × `season_year` × `phase`:
- `ctx_bat_rpb`: mean `runs` per batter ball faced.
- `ctx_bat_out_prob`: mean striker dismissal probability per ball faced (`dismissed_player_id == striker_id`).
- `ctx_bowl_rpb`: `sum(bowler_runs_conceded) / sum(is_legal_ball)`.
- `ctx_bowl_wkt_prob`: `sum(is_bowler_wicket) / sum(is_legal_ball)`.

---

## 5. Batting & Bowling Impact, Eligibility & Ranking (`src/batting_model.py`, `src/bowling_model.py`)
- **Wicket Value:** Fixed `wicket_weight = 6.0` runs per wicket saved (batting) or taken (bowling).
- **Batting Impact per 100 Balls:**
  $$\text{Impact}_{100} = 100 \cdot \frac{\sum (r_t - \text{ctx\_bat\_rpb}_t)}{n_{\text{balls}}} + 6.0 \cdot 100 \cdot \frac{\sum (\text{ctx\_bat\_out\_prob}_t - \text{out}_t)}{n_{\text{balls}}}$$
- **Bowling Impact per 24 Balls:**
  $$\text{Impact}_{24} = 4.0 \cdot \left(6.0 \cdot \frac{\sum (\text{ctx\_bowl\_rpb}_t\cdot\text{legal}_t - \text{conceded}_t)}{n_{\text{legal}}}\right) + 6.0 \cdot \left(24.0 \cdot \frac{\sum (\text{wkt}_t - \text{ctx\_bowl\_wkt\_prob}_t\cdot\text{legal}_t)}{n_{\text{legal}}}\right)$$
- **Eligibility Criteria:** `tot_balls >= 300`, `hp_balls >= 120`, `hp_balls_elite >= 80` (`IPL` + `T20I_Full`), `hp_matches >= 10`, `lp_balls >= 60`, AND `hp_impact > 0`.
- **Delta & Shrinkage:**
  - Batting: $\Delta = \text{HP\_Impact}_{100} - \max(\text{LP\_Impact}_{100}, -15.0)$
  - Bowling: $\Delta = \text{HP\_Impact}_{24} - \max(\text{LP\_Impact}_{24}, -10.0)$
  - Shrinkage weight: $w = n_{\text{HP}} / (n_{\text{HP}} + 120.0)$; $\Delta_{\text{shrunk}} = w\Delta$, $\text{HP\_shrunk} = w \cdot \text{HP\_Impact}$.
- **Cross-Match Consistency (`consistency_rate`):** Share of HP matches with `m_balls >= 6` where `m_impact > 0` (**unshrunk**; imputed `0.5` if 0 qualifying matches).
- **Final Score:**
  $$\text{PressureScore} = 0.40\,z(\Delta_{\text{shrunk}}) + 0.40\,z(\text{HP\_shrunk}) + 0.20\,z(\text{consistency\_rate})$$

---

## 6. Bootstrap Implementation (`src/validation_tests.py` & `src/run_pipeline.py`)
- **Random Seed:** `seed = 42` (`np.random.default_rng(42)`).
- **Resamples:** `n_boot = 300`.
- **Resampling Unit:** Entire matches (`df["match_id"].unique()`, `n = 837`) sampled with replacement **without stratification** across IPL vs T20I.
- **In-Sample Simplifications Found:**
  1. Context baselines (`ctx_bat_rpb`, `ctx_bowl_rpb`) and `pressure_index` are **frozen** from the full sample rather than recomputed per resample.
  2. Eligibility gates are **not** re-applied inside bootstrap iterations; only the 54/92 full-sample eligible players are ranked.
  3. Players with `hp_balls == 0` or `lp_balls == 0` in a resample are dropped from that iteration (verified `0` absent iterations for all 20 Top-10 players, though possible for borderline candidates).
  4. All 54 batters / 92 bowlers are ranked in each resample (not truncated at Top 10), so median rank and 5th–95th percentile intervals reflect ranks across the full eligible pool (`1..54` / `1..92`).

---

## 7. Earlier Provisional Reference Model
- **Status: UNVERIFIED (Not Present in Repository).** No earlier model scripts or parameter files exist in this workspace prior to the current `src/` implementation; therefore, its exact formulas cannot be reconstructed from code and are marked **unverified**. Reconciliation in `batting_candidate_reconciliation.csv` and `bowling_candidate_reconciliation.csv` instead compares those 20 named candidates using independently recalculated raw and context-adjusted metrics from `data/raw/`.

