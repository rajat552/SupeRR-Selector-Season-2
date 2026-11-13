# 05 — Model Comparison & Canonical Selection

To avoid arbitrary model choice, V2 evaluates three candidate scoring architectures side-by-side (`src/model_v2/model_comparison.py`) across out-of-sample predictive accuracy, temporal stability, bootstrap precision, domain fairness, and transparency. All empirical results below come directly from [model_comparison.csv](file:///c:/Users/LENOVO/OneDrive/Desktop/SupeRR-Selector-Season-2/outputs/model_v2/model_comparison.csv) and [model_c_oos_validation.csv](file:///c:/Users/LENOVO/OneDrive/Desktop/SupeRR-Selector-Season-2/outputs/model_v2/model_c_oos_validation.csv).

---

## 1. Candidate Model Specifications (`src/model_v2/impact_models.py`)

All three models operate on the identical V2 eligible pools (**99 batters**, **128 bowlers**) using LPO context-adjusted expectations, continuous pressure weights $w_t$, Kish $N_{\text{eff}}$, and Empirical Bayes Beta-binomial consistency:

1. **Model A — Absolute Continuous Pressure Impact:**
   $$\text{Score}_A = 0.50\,z(\text{Shrunk\_WP\_Impact}) + 0.30\,z(\text{Shrunk\_HP\_Impact}) + 0.20\,z(\text{EB\_Consistency})$$
   Focuses purely on pressure performance (continuous weighted + discrete HP) without any normal-pressure baseline subtraction.

2. **Model B — Maintenance & Lift (Selected Canonical Model):**
   $$\text{Norm\_Floored} = \max(\text{Shrunk\_Norm\_Impact},\; \text{lp\_floor}), \qquad \text{MaintLift} = \text{Shrunk\_WP\_Impact} - 0.35 \cdot \text{Norm\_Floored}$$
   $$\text{Score}_B = 0.50\,z(\text{Shrunk\_WP\_Impact}) + 0.30\,z(\text{MaintLift}) + 0.20\,z(\text{EB\_Consistency})$$
   where $\text{lp\_floor} = -5.0$ (batters) and $-3.0$ (bowlers). By attenuating the baseline coefficient ($\alpha = 0.35$ vs V1's $1.00$), flooring weak normal-pressure baselines, and using EB-shrunk continuous normal weights (`normal_neff`), Model B rewards both **elite maintenance under pressure** and **genuine pressure lift** without penalizing stars like Jasprit Bumrah or Tim David for dominating normal overs.

3. **Model C — Regularized Ridge + Logistic Interaction Model:**
   Fits delivery-level `Ridge(alpha=150.0)` on runs and `LogisticRegression(C=0.5)` on dismissals/wickets over sparse context (`comp_tier`, `phase`, `batting_role`/`pace_or_spin`, `opp_tier`, `innings`, standardized pre-match `opp_elo`), continuous `pressure_weight`, player main effects ($\alpha_i$), and `player x pressure_weight` interactions ($\beta_i$). Evaluated at $w = 0.85$:
   $$\text{Score}_C = 0.55\,z(\text{ModelC\_HP\_Impact}) + 0.25\,z(\text{ModelC\_Lift}) + 0.20\,z(\text{EB\_Consistency})$$

---

## 2. Empirical Model Comparison (`outputs/model_v2/model_comparison.csv`)

Evaluated using:
- **OOS Player-Level Correlation (`2022–2024 -> 2025–2026`):** Training score vs future `shrunk_wp_impact` (`70` common batters, `88` common bowlers).
- **Leave-One-Season-Out (LOSO):** Mean Spearman $\rho$ and Top-10 overlap across all 5 dropped seasons (`2022`–`2026`).
- **200-Iter Stratified Bootstrap:** Median CI width and mean Top-10 inclusion frequency for each model's Top 10 (Models A & B).
- **Model C Calibration Check:** OOS logistic calibration slope and Brier delta vs `Context_Pressure_Player` (`2022–2024 -> 2025–2026`).
- **Objective Composite Selection Score:** `0.35 * oos_spearman + 0.35 * loso_spearman + 0.30 * interpretability_score + domain_bonus - cal_penalty`.

### Batters (`n_eligible = 99`)
| Model | OOS Spearman | OOS Pearson | LOSO Mean $\rho$ | LOSO Top-10 Overlap | Boot CI Width (Med) | Boot Top-10 Freq | Benchmark Star Rank (`SKY`) | Ashutosh Retained | Selection Score | Selected |
|---|---:|---:|---:|---:|---:|---:|---:|---|---:|---|
| **Model A** | `-0.0222` | `+0.1041` | `0.9041` | `7.4` | `39.33` | `57.4%` | `#12` | `True` | `0.5787` | False |
| **Model B** | `-0.0542` | `+0.0717` | **`0.9047`** | `7.0` | **`36.58`** | `57.0%` | `#12` | `True` | **`0.6327`** | **True** |
| **Model C** | `-0.0463` | `+0.0757` | `0.9042` | `7.2` | — | — | `#10` | `True` | `0.2803` | False |

### Bowlers (`n_eligible = 128`)
| Model | OOS Spearman | OOS Pearson | LOSO Mean $\rho$ | LOSO Top-10 Overlap | Boot CI Width (Med) | Boot Top-10 Freq | Benchmark Star Rank (`Bumrah`) | Selection Score | Selected |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| **Model A** | **`+0.1580`** | **`+0.1415`** | `0.9348` | `6.8` | `46.95` | **`47.7%`** | `#2` | `0.6525` | False |
| **Model B** | `+0.1516` | `+0.1348` | **`0.9368`** | `6.4` | **`44.00`** | `47.5%` | **`#2`** | **`0.7159`** | **True** |
| **Model C** | `+0.1431` | `+0.1356` | `0.9312` | `6.4` | — | — | `#4` | `0.3560` | False |

---

## 3. Why Model C Was Not Selected (`outputs/model_v2/model_c_oos_validation.csv`)

Walk-forward delivery-level out-of-sample tests across four temporal splits (`2022-2024->2025-2026`, `2022-2023->2024`, `2022-2024->2025`, `2022-2025->2026`) demonstrate why adding `player x pressure_weight` interactions in a parametric GLM does not improve out-of-sample event prediction:

| Role | Split | Spec | Runs RMSE | Runs $R^2$ | Event Brier | Event Log-Loss | Cal Slope | Max Decile Cal Err |
|---|---|---|---:|---:|---:|---:|---:|---:|
| Batter | `2022-2024 -> 2025-2026` | `Context_Pressure_Only` | `1.7813` | `0.0063` | **`0.051938`** | **`0.211454`** | **`0.9742`** | **`0.0035`** |
| Batter | `2022-2024 -> 2025-2026` | `Context_Pressure_Player` | `1.7790` | `0.0089` | `0.052057` | `0.211824` | `0.7162` | `0.0248` |
| Batter | `2022-2024 -> 2025-2026` | `Model_C_Full_Interaction` | **`1.7789`** | **`0.0090`** | `0.052158` | `0.212322` | `0.6527` | `0.0321` |
| Bowler | `2022-2024 -> 2025-2026` | `Context_Pressure_Only` | `1.7814` | `0.0059` | **`0.050810`** | **`0.208115`** | **`1.0017`** | **`0.0048`** |
| Bowler | `2022-2024 -> 2025-2026` | `Context_Pressure_Player` | **`1.7808`** | **`0.0067`** | `0.050918` | `0.209094` | `0.6583` | `0.0130` |
| Bowler | `2022-2024 -> 2025-2026` | `Model_C_Full_Interaction` | `1.7809` | `0.0066` | `0.050944` | `0.209325` | `0.6040` | `0.0142` |

Across all four splits, `Model_C_Full_Interaction` yields calibration slopes of `0.6149–0.6837` (batters) and `0.5432–0.6570` (bowlers)—indicating systematic over-dispersion in predicted dismissal/wicket logits relative to `Context_Pressure_Only` (`0.8868–1.0783`)—and slightly worse Brier and log-loss than `Context_Pressure_Player`.

---

## 4. Canonical Selection Decision

**Model B (`Maintenance & Lift`)** is selected objectively (`objective_selection_score`: `0.6327` batters, `0.7159` bowlers; highest LOSO stability `0.9047` / `0.9368`; tightest bootstrap CI widths `36.58` / `44.00`; retains `Ashutosh Sharma` at `#10`, places `Jasprit Bumrah` at `#2`, and directly answers the Round 1 prompt comparing high-pressure delivery against usual baselines without penalizing elite all-weather performers).
