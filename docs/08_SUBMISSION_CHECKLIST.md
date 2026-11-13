# 08 — Submission Verification Checklist

Final pre-submission checklist for **SupeRR Selector Season 2 — Round 1** (V2 Remediated Pipeline).

---

## 1. Unstop Dropdown Selections (Must Match 1:1 with Report)

- **Top 10 Batters (`outputs/model_v2/final_top10_batters.csv`):**
  1. `Tim David` (`striker_id = 6396`, Score `+2.434`)
  2. `Matthew Wade` (`striker_id = 796`, Score `+2.267`)
  3. `Naman Dhir` (`striker_id = 37052`, Score `+2.028`)
  4. `Dinesh Karthik` (`striker_id = 143`, Score `+1.764`)
  5. `Reeza Hendricks` (`striker_id = 768`, Score `+1.745`)
  6. `Shashank Singh` (`striker_id = 2756`, Score `+1.609`)
  7. `Heinrich Klaasen` (`striker_id = 4260`, Score `+1.608`)
  8. `Rinku Singh` (`striker_id = 4708`, Score `+1.445`)
  9. `Andre Russell` (`striker_id = 1318`, Score `+1.434`)
  10. `Ashutosh Sharma` (`striker_id = 8101`, Score `+1.335`)

- **Top 10 Bowlers (`outputs/model_v2/final_top10_bowlers.csv`):**
  1. `Sunil Narine` (`bowler_id = 781`, Score `+2.481`)
  2. `Jasprit Bumrah` (`bowler_id = 2933`, Score `+1.995`)
  3. `Mustafizur Rahman` (`bowler_id = 4373`, Score `+1.851`)
  4. `Jamie Overton` (`bowler_id = 2382`, Score `+1.839`)
  5. `Mohit Sharma` (`bowler_id = 2878`, Score `+1.736`)
  6. `Sai Kishore` (`bowler_id = 5577`, Score `+1.708`)
  7. `Sufiyan Muqeem` (`bowler_id = 34485`, Score `+1.665`)
  8. `Mohsin Khan` (`bowler_id = 6669`, Score `+1.625`)
  9. `Mohammad Nawaz` (`bowler_id = 2490`, Score `+1.556`)
  10. `Josh Hazlewood` (`bowler_id = 830`, Score `+1.472`)

- **Dropdown Integrity:** Zero repeated players within either list; all 20 names cross-checked on `player_id` to prevent homonym confusion (`Abdul Samad`, `Rashid Khan`, `Haider Ali`).

---

## 2. Methodology Report Rubric Alignment

| Required PDF Section | Verified Coverage | Primary Reference Docs |
|---|---|---|
| **Pressure Definition** | Zero-look-ahead pre-delivery state, V1 $PI_t \in [0,1]$, V2 continuous sigmoid weights $w_t$ across all `193,988` deliveries (eliminating `13.85%` gap), Kish $N_{\text{eff}}$ | [04_ANALYTICAL_METHODOLOGY.md](file:///c:/Users/LENOVO/OneDrive/Desktop/SupeRR-Selector-Season-2/docs/04_ANALYTICAL_METHODOLOGY.md) |
| **Performance Measurement** | LPO hierarchical context residuals, RAE/RSO + wicket value ($V_w=6.0$ + non-overlapping marginal check), EB shrinkage ($k=120$), Beta-binomial consistency, Model A/B/C selection (`Model B`) | [05_MODEL_SELECTION.md](file:///c:/Users/LENOVO/OneDrive/Desktop/SupeRR-Selector-Season-2/docs/05_MODEL_SELECTION.md) |
| **Fair Comparisons** | Separate IPL/T20I chronological pre-match Elo, dynamic `batting_role` / `pace_or_spin` controls, `300/120/10` gate rescuing `Ashutosh Sharma`, format/gate sensitivity | [04_ANALYTICAL_METHODOLOGY.md](file:///c:/Users/LENOVO/OneDrive/Desktop/SupeRR-Selector-Season-2/docs/04_ANALYTICAL_METHODOLOGY.md), [07_VALIDATION_AND_LIMITATIONS.md](file:///c:/Users/LENOVO/OneDrive/Desktop/SupeRR-Selector-Season-2/docs/07_VALIDATION_AND_LIMITATIONS.md) |
| **Evidence for Top 10** | Full metrics, phase/format/matchup splits, standout match dates, 12 publication-ready charts in `outputs/model_v2/charts/` | [06_PLAYER_SELECTION_JUSTIFICATION.md](file:///c:/Users/LENOVO/OneDrive/Desktop/SupeRR-Selector-Season-2/docs/06_PLAYER_SELECTION_JUSTIFICATION.md) |
| **Reliability & Limitations** | `1,000`-iter stratified bootstrap CIs, OOS walk-forward checks, LOSO, pressure/wicket/shrinkage-$k$ sensitivity, explicit limitations & separated IPL 2027 practical flags | [07_VALIDATION_AND_LIMITATIONS.md](file:///c:/Users/LENOVO/OneDrive/Desktop/SupeRR-Selector-Season-2/docs/07_VALIDATION_AND_LIMITATIONS.md) |

---

## 3. Code, Data Governance & Deliverable Verification

- [x] **V1 / Raw Immutability:** `outputs/model_v2/integrity_manifest_pre.json` verified `39/39` files unchanged (`0` mismatches). `docs/03_DATA_AUDIT.md`, `docs/04_ANALYTICAL_STRATEGY.md`, and `docs/05_PROJECT_ROADMAP.md` untouched.
- [x] **Reproducible Pipeline & Tests:** Canonical run `python -m src.model_v2.run_pipeline` (`206.49s` runtime recorded in [execution_log.md](file:///c:/Users/LENOVO/OneDrive/Desktop/SupeRR-Selector-Season-2/outputs/model_v2/execution_log.md)), `bowler_player_profiles.csv` RHB/LHB splits + 12 charts regenerated (#30), and `pytest tests/model_v2/ -v` (`15 passed in 102.19s`).
- [x] **External Source & Confidentiality Hygiene:** `52` verified records in [external_player_research.csv](file:///c:/Users/LENOVO/OneDrive/Desktop/SupeRR-Selector-Season-2/outputs/model_v2/external_player_research.csv), `20` Top-20 feasibility records in [auction_feasibility.csv](file:///c:/Users/LENOVO/OneDrive/Desktop/SupeRR-Selector-Season-2/outputs/model_v2/auction_feasibility.csv), and [source_register.md](file:///c:/Users/LENOVO/OneDrive/Desktop/SupeRR-Selector-Season-2/outputs/submission/source_register.md) with `access_date = 2026-11-12` and explicit `Unverified` IPL 2027 status.
- [ ] **Final Submission Package (`outputs/submission/`):** Final rankings CSVs, `player_recommendations.csv`, `user_review_required.md`, `SupeRR_Selector_Round1_Methodology_Report.md/.pdf`, and final Unstop dropdown check (in progress by `@reporter`).
