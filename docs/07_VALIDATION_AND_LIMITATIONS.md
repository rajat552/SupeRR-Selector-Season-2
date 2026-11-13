# 07 — Validation, Robustness & Limitations

All validation results below are verified directly against [execution_log.md](file:///c:/Users/LENOVO/OneDrive/Desktop/SupeRR-Selector-Season-2/outputs/model_v2/execution_log.md), the V2 sensitivity CSVs in `outputs/model_v2/`, and the test suite (`tests/model_v2/`).

---

## 1. Automated Verification & Immutability

- **V1 Integrity Manifest (`outputs/model_v2/integrity_manifest_pre.json`):** `39/39` raw, V1 source, and Phase 0.5 audit files verified unchanged (`0` SHA-256 mismatches).
- **V2 Automated Test Suite (`pytest tests/model_v2/ -v`):** Covers cricket accounting rules, zero look-ahead match state, strict chronological date-batched Elo, LPO self-exclusion, Kish $N_{\text{eff}}$, Beta-binomial shrinkage, non-overlapping wicket valuation, and stratified bootstrap equivalence against direct delivery-level resampling (`< 1e-10` numerical tolerance).
- **V1 Audit Rule Tests (`python outputs/model_audit/test_audit_rules.py`):** `9/9` passing (`OK`).

---

## 2. Stratified Bootstrap Uncertainty (`1,000` Resamples, `seed = 42`)

Stratifying by `(comp_category, season_year)` and recomputing full LPO baselines, Beta-binomial priors, shrinkage, and eligibility inside every resample (`19.63s` total for both roles):
- **Precision Scales with Effective Sample Size:** Rank CI width correlates negatively with Kish $N_{\text{eff}}$ across the full eligible pool (`Spearman(pressure_neff, boot_ci_width) = -0.2320` across `99` batters; `-0.3213` across `128` bowlers).
- **Established Core vs. Gate-Boundary Volatility:**
  - High-$N_{\text{eff}}$ anchors exhibit strong Top-10 inclusion and `0` ineligible resamples: `Sunil Narine` (`90.5%`, median `4.0`, `p05–p95 = 1–13`, `0` ineligible), `Tim David` (`89.3%`, median `3.0`, `1–16`, `0` ineligible), `Jasprit Bumrah` (`65.7%`, median `7.0`, `1–33`, `0` ineligible).
  - Players near the `300 / 120 / 10` gate boundaries experience frequent resampling drop-offs (`ineligible_iters`): `Sai Kishore` (`545/1000` ineligible, `hp_balls=123`), `Sufiyan Muqeem` (`372/1000`, `tot_balls=344`), `Ashutosh Sharma` (`338/1000`, `tot_balls=334`), `Matthew Wade` (`280/1000`, `hp_balls=158`), `Jamie Overton` (`209/1000`, `hp_balls=165`). Zero top-10 players have `absent_iters > 0`.

---

## 3. Multi-Dimensional Sensitivity Suite

| Sensitivity Axis | Source CSV | Key Empirical Findings |
|---|---|---|
| **Competition Format** | [format_sensitivity.csv](file:///c:/Users/LENOVO/OneDrive/Desktop/SupeRR-Selector-Season-2/outputs/model_v2/format_sensitivity.csv) | **IPL + Full-Member T20I (`784` matches):** `10/10` batters overlap ($\rho = 0.9930$), `9/10` bowlers overlap ($\rho = 0.9944$, `Jofra Archer` enters Top 10 replacing `Mohammad Nawaz`). **IPL-only (`367` matches, benchmark gate):** `7/10` batters ($\rho = 0.9404$), `6/10` bowlers ($\rho = 0.8940$). **T20I-only (`470` matches):** `2/10` batters ($\rho = 0.9259$), `4/10` bowlers ($\rho = 0.8990$) — confirming T20I-only and IPL-only specialists diverge sharply when separated. |
| **Pressure Threshold & Weighting** | [pressure_sensitivity.csv](file:///c:/Users/LENOVO/OneDrive/Desktop/SupeRR-Selector-Season-2/outputs/model_v2/pressure_sensitivity.csv) | Across `hp_thresh = 0.45` (`10/10` overlap, $\rho = 0.9903$/`0.9936`) and `0.55` (`9/10` overlap, $\rho = 0.9919$/`0.9955`), sigmoid centers `{0.40, 0.425, 0.45}`, and scale `0.12`, Top-10 overlap is `9–10/10` with $\rho \ge 0.990$. Even switching to linear $w_t = PI_t$ yields `10/10` batters ($\rho = 0.9718$) and `9/10` bowlers ($\rho = 0.9835$). |
| **Eligibility Gates** | [eligibility_sensitivity.csv](file:///c:/Users/LENOVO/OneDrive/Desktop/SupeRR-Selector-Season-2/outputs/model_v2/eligibility_sensitivity.csv) | Sweeping `lenient (200/80/8)` to `very_strict (500/180/15)` yields $\rho \ge 0.9991$ across common players (`140 -> 61` batters; `161 -> 84` bowlers). Pure Kish $N_{\text{eff}} \ge 150$ (`111` batters, `147` bowlers) preserves `10/10` batters and `9/10` bowlers. Re-enabling V1's `lp_balls >= 60` counterfactual drops `Ashutosh Sharma` (`99 -> 98` batters). |
| **Wicket Valuation** | [wicket_sensitivity.csv](file:///c:/Users/LENOVO/OneDrive/Desktop/SupeRR-Selector-Season-2/outputs/model_v2/wicket_sensitivity.csv) | Fixed $V_w \in \{4.0, 6.0, 8.0\}$ preserves `9–10/10` overlap ($\rho \ge 0.9820$). Non-overlapping context-marginal wicket value (`mean = 7.82`, range `1.0–15.0`, [context_wicket_values.csv](file:///c:/Users/LENOVO/OneDrive/Desktop/SupeRR-Selector-Season-2/outputs/model_v2/context_wicket_values.csv)) achieves $\rho = 0.9539$ (`9/10` overlap) for batters and $\rho = 0.9656$ (`7/10` overlap, lifting spinners `Kuldeep Yadav`, `Varun Chakravarthy`, `Abrar Ahmed`) for bowlers. |
| **Shrinkage $k$** | [shrinkage_k_sensitivity.csv](file:///c:/Users/LENOVO/OneDrive/Desktop/SupeRR-Selector-Season-2/outputs/model_v2/shrinkage_k_sensitivity.csv) | Odd/even match-split weighted MSE (`n = 267` batters, `n = 232` bowlers) drops sharply from `k = 60` (`786.30` / `47.35`) to `k = 120` (`747.60` / `42.66`) and flattens beyond `120–150`, confirming `k = 120` avoids under-shrinking noisy small samples. |
| **Leave-One-Season-Out (LOSO)** | [loso_sensitivity.csv](file:///c:/Users/LENOVO/OneDrive/Desktop/SupeRR-Selector-Season-2/outputs/model_v2/loso_sensitivity.csv) | Dropping any single season (`2022`–`2026`) yields $\rho \in [0.8320, 0.9505]$ (`5–9/10` overlap) for batters and $\rho \in [0.9207, 0.9566]$ (`4–8/10` overlap) for bowlers; `2024` (batters) and `2025` (bowlers) cause the largest single-year shifts due to concentrated IPL/T20 WC volume. |

---

## 4. Key Limitations

1. **Format Heterogeneity (IPL vs. T20I):** Although V2 controls for `comp_tier` and pre-match `opp_elo`, zero-IPL T20I specialists (`Reeza Hendricks`, `Sufiyan Muqeem`, `Mohammad Nawaz`) cannot be tested directly against IPL batting/bowling depth within the supplied dataset.
2. **Missing Ball-Tracking & Fielding Telemetry:** `bowl_speed` has a `0.0` sentinel on `38.74%` (`77,861`) of raw deliveries and extreme outliers (`>165 km/h`), so pace velocity was excluded; dropped catches, misfields, and pitch/dew conditions are absent from the raw schema.
3. **Sample-Size Gate Sensitivity:** Players just above the `300/120/10` thresholds (`Ashutosh Sharma`, `Sai Kishore`, `Sufiyan Muqeem`, `Matthew Wade`, `Jamie Overton`) exhibit wide bootstrap rank intervals (`40–72` ranks) and `209–545` ineligible resamples.
4. **Role Uncertainty & Team-Sheet Discrepancies:** `358` deliveries carry `is_role_uncertain == True` (`255` mismatches between `playing_eleven.batting_order` and realized `ball_by_ball.batting_order`).
5. **Temporal Lag in Player Career Status:** Statistical scores aggregate 2022–2026 historical deliveries equally without age-curve decay or post-data retirement filtering; `Matthew Wade`, `Dinesh Karthik`, `Andre Russell`, and `Mohit Sharma` have since retired from IPL/playing roles, and all IPL 2027 availability remains `Unverified` prior to the `2026-11-17` retention and `2026-12-03` auction register deadlines.
