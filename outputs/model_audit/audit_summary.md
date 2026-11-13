# Phase 0.5 — Independent Statistical Audit Summary

**Audit Scope:** Forensic recalculation and validation of the SupeRR Selector Season 2 Round 1 statistical pipeline (`src/`) and the four existing visualization outputs (`outputs/charts/*.png`) directly from `data/raw/*.csv`.  
**Preservation Guarantee:** Zero raw files, existing `src/` scripts, existing ranking CSVs, charts, or `docs/` files were modified or deleted. All audit artifacts reside in `outputs/model_audit/`.

---

## 1. Mathematical Reproducibility of Existing Charts & Rankings
- **Verdict: 100% MATHEMATICALLY REPRODUCIBLE.**
- Independent pure-pandas recalculation from `data/raw/*.csv` (`outputs/model_audit/independent_audit.py`) matched every score and metric in `outputs/top10_batters.csv` and `outputs/top10_bowlers.csv` to floating-point precision (`score_max_abs_err <= 4.44e-16`; verified in `batting_impact_validation.csv` and `bowling_impact_validation.csv`).
- All 9 independent cricket-accounting unit tests (`test_audit_rules.py`) passed (`9/9 OK` in 3.96s), confirming legal-ball rules, wide/no-ball (`Overstep`/`other`) handling, bye/legbye exclusion from bowler conceded runs, non-striker run-out tracking, Super Over (38 balls) and `Other_T20` (30 matches, 6,985 deliveries) exclusions, zero look-ahead state reconstruction, and `player_id` homonym preservation (`Abdul Samad` 7446 vs 6922; `Rashid Khan` 4722 vs 20172; `Haider Ali` 7338 vs 28756).

---

## 2. Critical & Moderate Methodological Findings (Why Rankings Behave as They Do)

| Severity | Finding | Evidence / Impact |
|---|---|---|
| **CRITICAL** | **Specialist Finisher Disqualification (`lp_balls >= 60` gate)** | **Ashutosh Sharma** (`8101`) faced 334 total balls and **273 HP balls** (`81.7%` of his career!) across 22 HP matches (`hp_impact_100 = +16.55`, `lp_impact_100 = -2.44`, raw lift `+18.99`), yet was **silently excluded** solely because `lp_balls = 42 < 60`. Requiring a finisher to accumulate 60 *low-pressure* balls penalizes players who almost exclusively bat under pressure. |
| **CRITICAL** | **Unshrunk Cross-Match Consistency (`m_balls >= 6`)** | `consistency_rate` receives 20% of the total score without Empirical Bayes shrinkage. Players with only **6–8 qualifying HP matches** (`Shai Hope` 6, `Reeza Hendricks` 7, `Mohammad Rizwan` 7, `Sai Kishore` 7, `Shubman Gill` 8) receive extreme z-scores (`+3.31 SD` for Sai Kishore's 7/7 = 100%; `+2.45 SD` for Hendricks/Rizwan's 6/7 = 85.7%) and display wide bootstrap rank CIs (`p95 = 21–59`). |
| **MODERATE** | **Elite-Baseline Penalty (`HP − LP` Delta Confounding)** | Players who dominate in *all* situations have high `LP` baselines, compressing their `HP − LP` delta: **Jasprit Bumrah** (`hp_impact_24 = +12.26`, `lp_impact_24 = +5.65`, delta `+6.60`) ranks **#8** behind **Mohit Sharma** (`hp = +9.37`, `lp = -8.02`, delta `+17.38`) and **Sai Kishore** (`hp = +17.26`, `lp = -4.37`, delta `+21.63`). Similarly, **Suryakumar Yadav** (`hp = +27.43`, `lp = +37.85`, rank **#16**) and **Tim David** (`hp = +42.27`, `lp = +47.22`, rank **#4**) incur negative deltas against exceptional normal baselines. |
| **MODERATE** | **No Batting-Order or Fine-Grained Opponent-Strength Adjustment** | Context cells (`comp_tier × season_year × phase`) treat all `T20I_Full` teams identically (e.g., Zimbabwe/Ireland/Bangladesh vs India/Australia) and do not adjust for `batting_order` (openers vs finishers). Zero-IPL T20I specialists (`Reeza Hendricks`, `Sufiyan Muqeem`, `Mohammad Nawaz`, `Abrar Ahmed`, `Mohammad Rizwan`) benefit from bilateral T20I volume. |
| **MODERATE** | **Bootstrap Simplifications** | Existing bootstrap (`n_boot = 300`, `seed = 42`) does not stratify by `IPL` vs `T20I`, freezes `pressure_index`, `ctx_*` baselines, and full-sample eligibility, and omits `absent` players if `hp_balls=0` or `lp_balls=0` (though `absent_iters_n500 = 0` for all 20 Top-10 players). Stratified `n_boot = 500` yields closely aligned medians (`bootstrap_reconciliation.csv`). |
| **MINOR** | **Intermediate Pressure Gap (`0.35 <= PI < 0.50`)** | Excludes `26,870` deliveries (`13.85%` of `193,988` primary balls) from both HP and LP pools (e.g., 408 balls for Suryakumar Yadav). Also `plot_bootstrap_ci` inverts the x-axis (`Rank 1` on right) and labels `prob_top10` without clarifying it is *bootstrap resample frequency*, not future match probability. |

---

## 3. Specific Player Investigation Answers
- **Why Suryakumar Yadav is #16 (not Top 10):** Eligible (`657` HP balls, `48` matches, `hp_impact_100 = +27.43`, `consistency = 65.7%`), but his normal-pressure baseline is extraordinary (`lp_impact_100 = +37.85`, `lp_sr = 170.5`), producing `shrunk_delta = -8.82`.
- **Why Rinku Singh is #24 (not Top 10):** Eligible (`507` HP balls, `37` matches, `hp_impact_100 = +19.20`), but `lp_impact_100 = +25.27`, giving `shrunk_delta = -4.91`.
- **Why Ashutosh Sharma is excluded:** Ineligible due to `lp_balls = 42 < 60` despite `273` HP balls (`+16.55` HP impact vs `-2.44` LP impact).
- **Why Phil Salt & Nitish Reddy are excluded:** `Phil Salt` (`hp_balls = 112 < 120`, `hp_matches = 9 < 10`; `hp_impact_100 = +37.75`); `Nitish Reddy` (`hp_impact_100 = -11.14 <= 0`).
- **Why Sai Kishore (#2) & Sufiyan Muqeem (#1) rank so high:** Both pair strong HP impact (`+17.26`, `+19.70`) with negative LP baselines (`-4.37`, `-1.20`) and high unshrunk consistency (`7/7 = 100%`, `9/11 = 81.8%`) over modest samples (`123` and `148` HP balls).
- **Why Sunil Narine (#3) vs Jasprit Bumrah (#8):** Both have near-identical `shrunk_hp_impact` (`+9.84` vs `+9.87`), but Narine has a lower LP baseline (`+3.46` vs `+5.65`, giving larger shrunk delta `+7.10` vs `+5.32`) and higher consistency (`93.1%` vs `76.9%`).
- **Why Matthew Wade (#2 batter):** Low LP baseline (`-9.33`), only 3 dismissals in `158` HP balls (`hp_surv_100 = +5.29`, boosting `hp_impact_100` to `+40.57`), and last played `2024-04-10`.
- **Why Tim David (#4 batter despite negative delta):** His `z_abs_hp = +3.05` (`hp_impact_100 = +42.27` across `570` HP balls) and `z_cons = +1.38` (`74.2%`) outweigh `z_delta = -0.60` (`shrunk_delta = -4.09`).

---

## 4. Reconciliation with Earlier Reference Candidates
- **Batters Overlap (2/10):** `Naman Dhir`, `Tim David`.
  - *Only in Current:* `Reeza Hendricks`, `Matthew Wade`, `Sanju Samson`, `Shubman Gill`, `Mark Chapman`, `Glenn Maxwell`, `Shai Hope`, `Mohammad Rizwan`.
  - *Only in Earlier Ref:* `Suryakumar Yadav` (#16), `Rinku Singh` (#24), `Shreyas Iyer` (#15), `Glenn Phillips` (#45), `Tristan Stubbs` (#48), `Phil Salt` (ineligible `112` HP balls), `Ashutosh Sharma` (ineligible `42` LP balls), `Nitish Reddy` (ineligible `hp_impact <= 0`).
- **Bowlers Overlap (4/10):** `Sunil Narine`, `Mustafizur Rahman`, `Kuldeep Yadav`, `Jasprit Bumrah`.
  - *Only in Current:* `Sufiyan Muqeem`, `Sai Kishore`, `Mohammad Nawaz`, `Mohit Sharma`, `Mitchell Santner`, `Abrar Ahmed`.
  - *Only in Earlier Ref:* `Varun Chakravarthy` (#11, narrowly missed), `Jamie Overton` (#13), `Gerald Coetzee` (#14), `Jofra Archer` (#26), `Matheesha Pathirana` (#49), `Hasan Mahmud` (#87).
- **Exact Earlier Model Formulas:** **UNVERIFIED** (no prior model code exists in this repository).

---

## 5. Separate Practical IPL 2027 Feasibility Flags (`eligibility_flags.csv`)
Without altering statistical eligibility, practical auction verification flags apply to:
- **Zero IPL exposure in 2022–2026 (`hp_balls_ipl = 0`):** `Reeza Hendricks`, `Mark Chapman`, `Shai Hope`, `Mohammad Rizwan`, `Sufiyan Muqeem`, `Mohammad Nawaz`, `Abrar Ahmed`.
- **Inactive / retired check (`last_match_date < 2026-01-01`):** `Matthew Wade` (`2024-04-10`), `Mohammad Rizwan` (`2024-12-13`), `Mohit Sharma` (`2025-05-24`), `Glenn Maxwell` (`2025-11-06`), `Reeza Hendricks` (`2025-12-19`).
- **BCCI/IPL participation restriction (Pakistan nationals):** `Mohammad Rizwan`, `Sufiyan Muqeem`, `Mohammad Nawaz`, `Abrar Ahmed`.

---

## 6. What Must Be Corrected Before Final Canonical Rankings (Recommendations)
1. **Replace `lp_balls >= 60` with `tot_balls >= 300` (or `non_hp_balls >= 40` / player overall career baseline fallback)** so specialist high-pressure finishers like `Ashutosh Sharma` are not penalized for facing high-pressure balls.
2. **Shrink `consistency_rate` toward `0.50` via Empirical Bayes** ($k_{\text{matches}} = 10$): $\text{cons}_{\text{shrunk}} = \frac{m \cdot \text{rate} + 10 \cdot 0.50}{m + 10}$, and require `hp_qual_matches >= 10` (or `>= 150` HP balls) so 6–7 match streaks cannot dominate.
3. **Eliminate the Elite-Baseline Penalty:** Compare high-pressure performance against **either** the player's shrunk normal baseline **or** a phase-adjusted *overall* baseline using a continuous Pressure-Weighted Residual, and/or evaluate **Maintenance + Lift** ($\text{HP Impact} - \alpha \cdot \text{LP Impact}$ with $\alpha \in [0.35, 0.50]$ rather than $1.0$, or cap LP penalty) so players who *maintain* elite performance (`Bumrah`, `Suryakumar`, `Tim David`) aren't outranked solely by players with terrible normal baselines.
4. **Add Batting-Order & Opponent-Strength Controls:** Center batting residuals within `(comp_tier, season_year, phase, batting_role)` (`Top 1-3`, `Middle 4-5`, `Finisher 6+`), and separate `T20I_Top` (e.g. top-8/10 ICC full members) from lower-tier bilaterals or test IPL-only / IPL-weighted sensitivity.
5. **Fix Bootstrap:** Use **stratified** (`IPL` vs `T20I`) resampling (`n_boot >= 1000`), recompute baselines/shrinkage inside each resample, clarify `top10_inclusion_frequency` terminology, and un-invert the x-axis (Rank 1 on the left).

---

## 7. Complete Audit File Inventory (`outputs/model_audit/`)
- `audit_summary.md` (this report)
- `model_formula_audit.md` (exact code-level formula reconstruction)
- `audit_test_results.md` (9/9 passing unit tests)
- `independent_audit.py` & `test_audit_rules.py` (standalone audit code)
- `data_scope_comparison.csv`
- `batting_impact_validation.csv` & `bowling_impact_validation.csv`
- `batting_candidate_reconciliation.csv` & `bowling_candidate_reconciliation.csv`
- `bootstrap_reconciliation.csv`
- `sample_size_validation.csv`
- `eligibility_flags.csv`

