# AGENTS.md — Workspace Governance & Engineering Rules

This repository houses the **SupeRR Selector Season 2 (Round 1)** analytics workspace (`Python 3.13`), preserving the audited **V1** baseline pipeline alongside the remediated **V2** statistical architecture.

---

## 1. Repository Layout: V1 vs V2

### Immutable V1 Baseline & Audit Artifacts (READ-ONLY)
- `data/raw/` — Official competition PDF and 6 raw CSV files (`competitions.csv`, `teams.csv`, `matches.csv`, `playing_eleven.csv`, `competition_team_player_mapping.csv`, `ball_by_ball.csv`).
- `src/*.py` — Original V1 pipeline modules (`data_loader.py`, `state_builder.py`, `pressure.py`, `baselines.py`, `batting_model.py`, `bowling_model.py`, `validation_tests.py`, `run_pipeline.py`).
- `outputs/*.csv`, `outputs/sensitivity_summary.json`, `outputs/charts/*.png`, `outputs/METHODOLOGY_REPORT.md` — Original V1 ranking outputs, charts, and report.
- `outputs/model_audit/` — Independent Phase 0.5 statistical audit (`audit_summary.md`, `model_formula_audit.md`, `audit_test_results.md`, `independent_audit.py`, `test_audit_rules.py`, and reconciliation CSVs).
- `docs/03_DATA_AUDIT.md`, `docs/04_ANALYTICAL_STRATEGY.md`, `docs/05_PROJECT_ROADMAP.md` — Original Phase 0 discovery documents.

### V2 Remediated Pipeline & Submission Workspace
- `src/model_v2/` — Modular V2 package resolving the 7 V1 methodological issues (`data_loader.py`, `cricket_accounting.py`, `state_builder.py`, `opponent_strength.py`, `pressure_model.py`, `batting_features.py`, `bowling_features.py`, `context_baselines.py`, plus modeling/bootstrap/pipeline modules).
- `tests/model_v2/` — Unit and statistical validation suite (`pytest`).
- `outputs/model_v2/` — V2 intermediate tables, rankings, diagnostics, `integrity_manifest_pre.json`, and `external_player_research.csv`.
- `outputs/submission/` — Final competition deliverables (`source_register.md`, final methodology report, charts, Unstop dropdown verification).
- `docs/00_COMPETITION_OVERVIEW.md`, `docs/01_PROBLEM_DEFINITION.md`, `docs/02_DATA_DICTIONARY.md` — Restored foundational governance and specification docs.

---

## 2. Strict Immutability & Preservation Rules

**NEVER modify, overwrite, or delete any of the following:**
- `data/raw/*`
- `src/*.py` (V1 modules at `src/` root)
- `outputs/model_audit/*`
- `outputs/*.csv`, `outputs/sensitivity_summary.json`, `outputs/charts/*`, `outputs/METHODOLOGY_REPORT.md`
- `docs/03_DATA_AUDIT.md`, `docs/04_ANALYTICAL_STRATEGY.md`, `docs/05_PROJECT_ROADMAP.md`
- `outputs/model_v2/integrity_manifest_pre.json`

All V1 checksums are recorded in `outputs/model_v2/integrity_manifest_pre.json` and must verify unchanged.

---

## 3. Data Confidentiality & External Research Rules

1. **No Raw Data Leakage:** Never copy, paste, upload, or include proprietary `data/raw/*.csv` rows, internal player/match IDs, or dataset-derived aggregates in external web search queries or third-party prompts.
2. **Public Facts Only Online:** External web research is strictly limited to public cricket knowledge (player career/retirement status, current franchise, BCCI/IPL rules, squad context) with every claim backed by an explicit URL, publication date, access date, and evidence classification (`Official`, `Reputable Media`, or `Unverified`) in `outputs/submission/source_register.md`.
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
# Run full V2 pipeline
python -m src.model_v2.run_pipeline

# Run V2 test suite
pytest tests/model_v2/ -v

# Re-run V1 independent audit unit tests (read-only verification)
python outputs/model_audit/test_audit_rules.py
```
