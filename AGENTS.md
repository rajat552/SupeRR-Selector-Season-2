# AGENTS.md — Workspace Governance & Engineering Rules

This repository houses the **SupeRR Selector Season 2 (Round 1)** analytics workspace (`Python 3.13`), preserving the audited **V1** baseline pipeline alongside the remediated **V2**, **V3**, and final **V4 Multiverse** analytical architectures.

---

## 1. Repository Layout: Iterative Versions & Submission Architecture

### Immutable V1 Baseline & Audit Artifacts (READ-ONLY)
- `data/raw/` — Official competition PDF and 6 raw CSV files (`competitions.csv`, `teams.csv`, `matches.csv`, `playing_eleven.csv`, `competition_team_player_mapping.csv`, `ball_by_ball.csv`).
- `src/*.py` — Original V1 pipeline modules (`data_loader.py`, `state_builder.py`, `pressure.py`, `baselines.py`, `batting_model.py`, `bowling_model.py`, `validation_tests.py`, `run_pipeline.py`).
- `outputs/*.csv`, `outputs/sensitivity_summary.json`, `outputs/charts/*.png`, `outputs/METHODOLOGY_REPORT.md` — Original V1 ranking outputs, charts, and report.
- `outputs/model_audit/` — Independent Phase 0.5 statistical audit (`audit_summary.md`, `model_formula_audit.md`, `audit_test_results.md`, `independent_audit.py`, `test_audit_rules.py`, and reconciliation CSVs).
- `docs/03_DATA_AUDIT.md`, `docs/04_ANALYTICAL_STRATEGY.md`, `docs/05_PROJECT_ROADMAP.md` — Original Phase 0 discovery documents.

### V2 & V3 Analytical Pipelines & Intermediate Diagnostics
- `src/model_v2/`, `src/model_v3/` — Remediated model architectures and feature extraction engines.
- `tests/model_v2/`, `tests/model_v3/` — Unit and statistical validation suites (`pytest`).
- `outputs/model_v2/` — V2 intermediate tables, rankings, diagnostics, and `integrity_manifest_pre.json`.
- `outputs/model_v3/` — V3 sensitivity feature tables and rankings.

### Final V4 Multiverse Model & Submission Deliverables
- `src/model_v4/` — Final specification-curve pipeline evaluating 15,150 specifications per role.
- `tests/model_v4/` — Validation suite for V4 components.
- `outputs/model_v4/` — Final multiverse specification records, summary matrices, bootstrap distributions, and charts.
- `outputs/data_audit/` — Step 0 raw data audit schema profiles, referential checks, cricket accounting, and pressure separation validation.
- `outputs/submission_final/` — Final submission compilation scripts and editable Markdown report source.
- `outputs/final_package/` — **OFFICIAL SUBMISSION DELIVERABLE BUNDLE** (`SupeRR_Final_Report.pdf`, data files, verification matrices, executed notebooks, and run logs).
- `archive/` — Historical submission drafts (`old_reports/`), reproducibility run comparison baselines (`reproducibility_run/`), and duplicates.

---

## 2. Strict Immutability & Preservation Rules

**NEVER modify, overwrite, or delete any of the following:**
- `data/raw/*` (including `data/raw/.DS_Store`)
- `src/*.py` (V1 modules at `src/` root)
- `src/model_v2/`, `src/model_v3/`, `src/model_v4/`
- `tests/` (all subdirectories)
- `notebooks/` (all notebooks)
- `outputs/model_audit/*`
- `outputs/*.csv`, `outputs/sensitivity_summary.json`, `outputs/charts/*`, `outputs/METHODOLOGY_REPORT.md`
- `outputs/model_v2/*` (including `outputs/model_v2/integrity_manifest_pre.json`)
- `outputs/model_v3/*`
- `outputs/model_v4/*`
- `outputs/data_audit/*`
- `outputs/submission_final/*`
- `outputs/final_package/*`
- `archive/*`
- `docs/03_DATA_AUDIT.md`, `docs/04_ANALYTICAL_STRATEGY.md`, `docs/05_PROJECT_ROADMAP.md`

All V1 checksums are recorded in `outputs/model_v2/integrity_manifest_pre.json` and must verify unchanged.

---

## 3. Data Confidentiality & External Research Rules

1. **No Raw Data Leakage:** Never copy, paste, upload, or include proprietary `data/raw/*.csv` rows, internal player/match IDs, or dataset-derived aggregates in external web search queries or third-party prompts.
2. **Public Facts Only Online:** External web research is strictly limited to public cricket knowledge (player career/retirement status, current franchise, BCCI/IPL rules, squad context) with every claim backed by an explicit URL, publication date, access date, and evidence classification (`Official`, `Reputable Media`, or `Unverified`) in `outputs/final_package/source_register.md`.
3. **Separate Statistical Ranking from Practical Feasibility:** Statistical rankings must be computed strictly from `data/raw/*.csv` without manual overrides; IPL 2027 availability/auction/eligibility notes must remain clearly separated as practical context flags.

---

## 4. Non-Negotiable Cricket & Statistical Integrity Standards

- **Player Identity:** Always key joins and aggregations on `player_id`, never `player_name` (homonyms exist: `Abdul Samad` `7446` vs `6922`; `Rashid Khan` `4722` vs `20172`; `Haider Ali` `7338` vs `28756`).
- **Primary Scope:** Exclude `Other_T20` (`comp_id` `2670`, `3289` — 30 matches, 6,985 deliveries), Super Overs (`innings` 3–4 — 38 deliveries), and the 16 abandoned matches with 0 deliveries -> **837 matches** (367 IPL, 470 T20I), **193,988 deliveries** (**185,692 legal balls**).
- **Zero Look-Ahead:** All match-state features (`pre_runs`, `pre_wickets`, `pre_legal_balls`, `pre_balls_remaining`, `pre_crr`, `pre_rrr`, `phase`) and pre-match Elo ratings (`match_date < current_match_date`, separate IPL and T20I tracks) must be strictly pre-delivery / pre-match.
- **Revised Overs Column Unit:** `matches.csv` columns `first_inn_revised_overs` and `second_inn_revised_overs` store **balls** (e.g., `114.0` = 19 overs), not overs.
- **Cricket Accounting:** `wide` is non-legal and not a batter ball faced; `Overstep` and `other` are no-balls (non-legal for bowler, batter ball faced = True); `byes`/`legbyes` are legal and excluded from `bowler_runs_conceded`; bowler wickets exclude `RunOut`, `Retire Out`, and `Obstructing the field` (normalize typo `Obstracting the field`).
- **Leave-Player-Out (LPO) Baselines:** Context baselines must subtract player `i`'s own deliveries from cell `c` before scoring player `i`, with hierarchical parent fallback when `n_cell - n_{i,cell} < 50`.

---

## 5. Canonical Commands

```powershell
# 1. Verify V1 File Immutability Checksums (39/39)
python -c "from src.model_v4.run_multiverse_pipeline import verify_v1_checksums; print(verify_v1_checksums())"

# 2. Run full V4 Multiverse Pipeline (Final Model: 15,150 specifications)
python -m src.model_v4.run_multiverse_pipeline

# 3. Run complete test suite (54 unit and statistical tests)
pytest tests/model_v2 tests/model_v3 tests/model_v4 -q

# 4. Compile final submission report (15 pages, outputs/submission_final/SupeRR_Final_Report.pdf)
python outputs/submission_final/compile_final_report.py

# 5. Run automated PDF and player verification audit
python outputs/submission_final/build_verification.py
```
