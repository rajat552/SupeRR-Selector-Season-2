# SupeRR Selector Season 2 — Repository Cleanup Plan (Dry Run)

**Date:** 2026-11-14  
**Author:** Senior Software Engineer / Senior Cricket Data Scientist  
**Scope:** Conservative cleanup of `SupeRR-Selector-Season-2` workspace  
**Status:** PHASE 1 DRY RUN COMPLETE — AWAITING WRITTEN APPROVAL BEFORE EXECUTION

---

## Phase 0: Backup Verification

As mandated, a full backup of the workspace was created prior to inspecting or proposing any cleanup actions. The project contains no internal git repository, making this archive the single source of recovery.

- **Archive Path:** `../SupeRR_backup_20261114.zip` (resolved: `C:\Users\LENOVO\OneDrive\Desktop\SupeRR_backup_20261114.zip`)
- **Archive Size:** 16,290,008 bytes (15.54 MB)
- **Archive Contents:** Complete repository directory tree, excluding ephemeral cache folders (`__pycache__` and `.pytest_cache`).
- **Backup Verification Status:** Verified created and readable.

---

## Protected Assets (Strictly Preserved — Never Deleted, Moved, Renamed, or Edited)

In accordance with `AGENTS.md` and repository governance rules, the following directories and files are strictly protected and excluded from any deletion or modification:

1. `data/raw/*` — All official competition raw data and documentation, including `data/raw/.DS_Store`.
2. `src/*.py` — Audited V1 baseline modules (`baselines.py`, `batting_model.py`, `bowling_model.py`, `data_loader.py`, `pressure.py`, `run_pipeline.py`, `state_builder.py`, `validation_tests.py`).
3. `src/model_v2/*` — Full V2 production modeling package.
4. `src/model_v3/*` — Full V3 production modeling package.
5. `tests/*` — All unit and integration test suites (`tests/model_v2/`, `tests/model_v3/`).
6. `notebooks/*` — All 5 exploratory and analytical notebooks (`01` through `05`).
7. `outputs/*.csv`, `outputs/*.json`, `outputs/charts/*`, `outputs/METHODOLOGY_REPORT.md` — Original V1 baseline rankings, audit files, and charts.
8. `outputs/model_audit/*` — Independent Phase 0.5 statistical audit code, logs, and reconciliation artifacts.
9. `outputs/model_v2/*` — V2 model rankings, bootstrap distributions, validation metrics, and pre-integrity manifest.
10. `outputs/model_v3/*` — V3 model rankings, bootstrap distributions, diagnostics, and definition robustness tables.
11. `outputs/submission/*` — Official competition deliverables (methodology report, source register, squad fit, charts).
12. `outputs/submission_v3/*` — V3 submission deliverables.
13. `docs/*` — Foundational discovery, governance, data dictionary, and methodology specifications.
14. `README.md`, `AGENTS.md`, `requirements.txt`, `.gitignore` — Core workspace governance and configuration.
15. Integrity manifests: `outputs/model_v2/integrity_manifest_pre.json`.

---

## Phase 1: Proposed Cleanup Actions

### (a) Disposable Caches (Proposed for Deletion)

These files and directories are generated automatically during Python compilation and test execution. They contain no source code, configuration, or unique artifacts.

#### Cache Directories (8 directories)
1. `.pytest_cache/`
2. `outputs/model_audit/__pycache__/`
3. `scratch/__pycache__/`
4. `src/__pycache__/`
5. `src/model_v2/__pycache__/`
6. `src/model_v3/__pycache__/`
7. `tests/model_v2/__pycache__/`
8. `tests/model_v3/__pycache__/`

#### Compiled Bytecode Files (60 `.pyc` files)
- `outputs\model_audit\__pycache__\independent_audit.cpython-313.pyc`
- `scratch\__pycache__\check_composition.cpython-313.pyc`
- `scratch\__pycache__\print_cross_table.cpython-313.pyc`
- `scratch\__pycache__\print_top15.cpython-313.pyc`
- `scratch\__pycache__\scan_dependencies.cpython-313.pyc`
- `scratch\__pycache__\test_definition_c.cpython-313.pyc`
- `scratch\__pycache__\test_pressure_formulation.cpython-313.pyc`
- `src\__pycache__\baselines.cpython-313.pyc`
- `src\__pycache__\batting_model.cpython-313.pyc`
- `src\__pycache__\bowling_model.cpython-313.pyc`
- `src\__pycache__\data_loader.cpython-313.pyc`
- `src\__pycache__\pressure.cpython-313.pyc`
- `src\__pycache__\state_builder.cpython-313.pyc`
- `src\__pycache__\validation_tests.cpython-313.pyc`
- `src\model_v2\__pycache__\__init__.cpython-313.pyc`
- `src\model_v2\__pycache__\batting_features.cpython-313.pyc`
- `src\model_v2\__pycache__\bootstrap.cpython-313.pyc`
- `src\model_v2\__pycache__\bowling_features.cpython-313.pyc`
- `src\model_v2\__pycache__\context_baselines.cpython-313.pyc`
- `src\model_v2\__pycache__\cricket_accounting.cpython-313.pyc`
- `src\model_v2\__pycache__\data_loader.cpython-313.pyc`
- `src\model_v2\__pycache__\eligibility.cpython-313.pyc`
- `src\model_v2\__pycache__\impact_models.cpython-313.pyc`
- `src\model_v2\__pycache__\model_comparison.cpython-313.pyc`
- `src\model_v2\__pycache__\opponent_strength.cpython-313.pyc`
- `src\model_v2\__pycache__\pressure_model.cpython-313.pyc`
- `src\model_v2\__pycache__\ranking.cpython-313.pyc`
- `src\model_v2\__pycache__\run_pipeline.cpython-313.pyc`
- `src\model_v2\__pycache__\shrinkage.cpython-313.pyc`
- `src\model_v2\__pycache__\state_builder.cpython-313.pyc`
- `src\model_v2\__pycache__\validation.cpython-313.pyc`
- `src\model_v2\__pycache__\visualization.cpython-313.pyc`
- `src\model_v3\__pycache__\__init__.cpython-313.pyc`
- `src\model_v3\__pycache__\batting_features.cpython-313.pyc`
- `src\model_v3\__pycache__\bootstrap.cpython-313.pyc`
- `src\model_v3\__pycache__\bowling_features.cpython-313.pyc`
- `src\model_v3\__pycache__\context_baselines.cpython-313.pyc`
- `src\model_v3\__pycache__\cricket_accounting.cpython-313.pyc`
- `src\model_v3\__pycache__\data_loader.cpython-313.pyc`
- `src\model_v3\__pycache__\definition_robustness.cpython-313.pyc`
- `src\model_v3\__pycache__\eligibility.cpython-313.pyc`
- `src\model_v3\__pycache__\impact_models.cpython-313.pyc`
- `src\model_v3\__pycache__\model_comparison.cpython-313.pyc`
- `src\model_v3\__pycache__\opponent_strength.cpython-313.pyc`
- `src\model_v3\__pycache__\pressure_model.cpython-313.pyc`
- `src\model_v3\__pycache__\ranking.cpython-313.pyc`
- `src\model_v3\__pycache__\run_pipeline.cpython-313.pyc`
- `src\model_v3\__pycache__\shrinkage.cpython-313.pyc`
- `src\model_v3\__pycache__\state_builder.cpython-313.pyc`
- `src\model_v3\__pycache__\validation.cpython-313.pyc`
- `src\model_v3\__pycache__\visualization.cpython-313.pyc`
- `tests\model_v2\__pycache__\__init__.cpython-313.pyc`
- `tests\model_v2\__pycache__\test_cricket_accounting.cpython-313-pytest-9.0.3.pyc`
- `tests\model_v2\__pycache__\test_models_and_bootstrap.cpython-313-pytest-9.0.3.pyc`
- `tests\model_v2\__pycache__\test_state_and_leakage.cpython-313-pytest-9.0.3.pyc`
- `tests\model_v3\__pycache__\__init__.cpython-313.pyc`
- `tests\model_v3\__pycache__\test_bowler_pressure.cpython-313-pytest-9.0.3.pyc`
- `tests\model_v3\__pycache__\test_cricket_accounting.cpython-313-pytest-9.0.3.pyc`
- `tests\model_v3\__pycache__\test_models_and_bootstrap.cpython-313-pytest-9.0.3.pyc`
- `tests\model_v3\__pycache__\test_state_and_leakage.cpython-313-pytest-9.0.3.pyc`

#### Other Caches
- `.ipynb_checkpoints/`: None found (0 files).
- `Thumbs.db`: None found (0 files).

---

### (b) Possibly Redundant Files (Proposed for Deletion upon Review)

The following 6 files exist in the `scratch/` directory. All 6 were temporary diagnostic or exploratory scripts created during model development and verification passes. None are imported or referenced anywhere in production code, tests, notebooks, or governance documentation.

| File Path | Size | Referenced By | Redundancy Evidence & Superseding Implementation |
| :--- | :---: | :--- | :--- |
| `scratch/check_composition.py` | 1,794 B | None | Temporary test script used to inspect bowler high-pressure delivery composition. Superseded by formal pipeline outputs (`outputs/model_v3/bowler_pressure_definition_comparison.csv`) and `tests/model_v3/test_bowler_pressure.py`. |
| `scratch/print_cross_table.py` | 1,478 B | None | Temporary script used to print formatted cross-definition tables to terminal. Superseded by `src/model_v3/definition_robustness.py`. |
| `scratch/print_top15.py` | 1,755 B | None | Temporary script used to format and preview top 15 ranking lists to terminal. Superseded by official ranking tables in `outputs/model_v3/` and `outputs/submission_v3/`. |
| `scratch/scan_dependencies.py` | 2,683 B | None | Temporary diagnostic script written to audit package imports across all files for this cleanup plan. Superseded by the dependency report in Section (d) below. |
| `scratch/test_definition_c.py` | 6,019 B | None | Research prototype for Definition C bowler pressure formulation. Fully integrated and superseded by `src/model_v3/definition_robustness.py` and `tests/model_v3/test_bowler_pressure.py`. |
| `scratch/test_pressure_formulation.py` | 3,023 B | None | Research prototype for bowler pressure thresholds and formula testing. Fully integrated and superseded by `src/model_v3/pressure_model.py`. |

*(Note: If all 6 files in `scratch/` are approved for deletion, the `scratch/` folder will be empty and can be cleanly removed).*

---

### (c) Duplicate Documentation (Reporting Only — Zero Edits, Merges, or Deletions)

In strict compliance with instructions, documentation files are **NOT modified, merged, or deleted**. The repository contains 6 identified pairs of documents reflecting the chronological evolution of the project from Phase 0/V1 baseline through Phase 4.2/V2 submission and V3 implementation:

1. **`docs/04_ANALYTICAL_STRATEGY.md` (5,757 bytes) vs `docs/04_ANALYTICAL_METHODOLOGY.md` (9,456 bytes)**
   - *Context:* `04_ANALYTICAL_STRATEGY.md` is the original Phase 0 strategy document framing the initial V1 analytical roadmap. `04_ANALYTICAL_METHODOLOGY.md` is the comprehensive V2 specification detailing mathematical formulations, match-state features, and contextual baselines.
2. **`docs/05_PROJECT_ROADMAP.md` (3,681 bytes) vs `docs/05_MODEL_SELECTION.md` (6,871 bytes)**
   - *Context:* `05_PROJECT_ROADMAP.md` is the initial Phase 0 milestone plan. `05_MODEL_SELECTION.md` is the formal V2 model selection document comparing baseline, additive, shrinkage, and regression models.
3. **`docs/08_SUBMISSION_CHECKLIST.md` (5,169 bytes) vs `outputs/submission/FINAL_SUBMISSION_CHECKLIST.md` (5,542 bytes)**
   - *Context:* `08_SUBMISSION_CHECKLIST.md` is the initial project setup checklist. `outputs/submission/FINAL_SUBMISSION_CHECKLIST.md` is the final Phase 4.2 pre-submission verification checklist.
4. **`outputs/submission/user_review_required.md` (9,497 bytes) vs `outputs/submission/FINAL_HUMAN_REVIEW.md` (13,631 bytes)**
   - *Context:* `user_review_required.md` was the initial questionnaire prepared during early V2 validation. `FINAL_HUMAN_REVIEW.md` is the comprehensive, final consolidated review dossier addressing Unstop submission format, auction context, and player evaluations.
5. **`outputs/METHODOLOGY_REPORT.md` (8,612 bytes) vs `outputs/submission/SupeRR_Selector_Round1_Methodology_Report.md` (70,448 bytes)**
   - *Context:* `outputs/METHODOLOGY_REPORT.md` is the immutable V1 baseline report (retained under audit preservation rules). `outputs/submission/SupeRR_Selector_Round1_Methodology_Report.md` is the complete, professional 18-page V2 submission report.
6. **`outputs/model_v2/execution_log.md` (3,761 bytes) vs `outputs/model_v3/execution_log.md` (3,753 bytes)**
   - *Context:* Separate chronological execution logs documenting execution runs for Model V2 and Model V3 pipelines respectively.

---

### (d) Dependencies Audit (Reporting Only — `requirements.txt` Unmodified)

Every package listed in `requirements.txt` was scanned across all files in `src/`, `tests/`, and `notebooks/`. Results are reported below:

| Package | `requirements.txt` Spec | `src/` Imports (Files) | `tests/` Imports (Files) | `notebooks/` Imports (Files) | Active Pipeline Role & Usage Status |
| :--- | :--- | :---: | :---: | :---: | :--- |
| **pandas** | `pandas>=2.0.0` | 43 files | 7 files | 5 files | **Core:** Fundamental data structure for ball-by-ball processing, match state, aggregations, and tabular outputs across all pipeline versions. |
| **numpy** | `numpy>=1.24.0` | 37 files | 7 files | 5 files | **Core:** Vectorized arithmetic, array operations, pressure index math, bootstrap resampling indices, and numerical transformations. |
| **scipy** | `scipy>=1.10.0` | 12 files | 0 files | 0 files | **Core:** Used in `bootstrap.py` (percentile calculations), `impact_models.py` (`scipy.sparse`), `shrinkage.py` (`scipy.stats.beta`), and `opponent_strength.py` (`scipy.optimize.minimize`). |
| **scikit-learn** | `scikit-learn>=1.2.0` | 2 files | 0 files | 0 files | **Active:** Used in `src/model_v2/impact_models.py` and `src/model_v3/impact_models.py` (`sklearn.linear_model.Ridge`, `LogisticRegression`) for Model D regression benchmarks. |
| **statsmodels** | `statsmodels>=0.14.0` | 0 files | 0 files | 0 files | **Unused:** Not imported anywhere in `src/`, `tests/`, or `notebooks/`. Listed in requirements as a statistical dependency but unreferenced in code. |
| **matplotlib** | `matplotlib>=3.7.0` | 3 files | 0 files | 5 files | **Active:** Used in `src/run_pipeline.py`, `src/model_v2/visualization.py`, `src/model_v3/visualization.py`, and all 5 exploratory notebooks to generate competition charts. |
| **seaborn** | `seaborn>=0.12.0` | 0 files | 0 files | 5 files | **Exploratory:** Imported and used in all 5 exploratory analysis notebooks (`01` through `05`) for distribution and correlation plots; not imported in `src/`. |
| **pytest** | `pytest>=7.0.0` | 0 files | 7 files | 0 files | **Active Test Framework:** Powers both `tests/model_v2/` and `tests/model_v3/` automated test suites. |
| **pypdf** | `pypdf>=3.0.0` | 0 files | 0 files | 0 files | **Utility:** Used during ad-hoc verification of PDF submission streams; not imported in production pipeline code. |
| **jupyter** | `jupyter>=1.0.0` | 0 files | 0 files | 0 files | **Runtime Environment:** Interactive notebook execution environment for `.ipynb` files. |

*(Note: Per instructions, `requirements.txt` is protected and will not be edited).*

---

## Action Items Proposed for User Approval

To execute Phase 2 (Execution), please provide written approval for the following deletion scope:

1. **Approve Group (a):** Delete all 8 cache directories and 60 compiled `.pyc` files listed in Section (a).
2. **Approve Group (b):** Delete the 6 temporary exploratory scripts in `scratch/` listed in Section (b), along with the empty `scratch/` directory.

No files from `data/`, `docs/`, `notebooks/`, `outputs/`, `src/`, `tests/`, or workspace root will be deleted, moved, or altered.

