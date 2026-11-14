# Execution Run Log & System Audit Register
**SupeRR Selector Season 2 — Round 1 Analytics Deliverable**
**Submission Author:** Rajat Aggarwal (Senior Cricket Data Scientist)
**Run Date:** 2026-11-14 | **Repository Status:** Fully Audited, Verified & Reproducible

---

## 1. System Runtime & Package Environment

- **Operating System:** Windows (AMD64)
- **Python Version:** `3.13.1` (tags/v3.13.1:0671451, Dec 3 2024, 19:06:28) [MSC v.1942 64 bit]
- **Installed Core Package Versions:**
  - `pandas`: 3.0.3
  - `numpy`: 2.4.4
  - `scipy`: 1.17.1
  - `scikit-learn`: 1.8.0
  - `statsmodels`: 0.14.6
  - `matplotlib`: 3.10.8
  - `seaborn`: 0.13.2
  - `pytest`: 9.0.3
  - `pypdf`: 6.20.0
  - `jupyter`: available
  - `nbconvert`: 7.17.2

---

## 2. Integrity Verification (39/39 Checksums)

- **Verification Command:** `python -c "from src.model_v4.run_multiverse_pipeline import verify_v1_checksums; print(verify_v1_checksums())"`
- **Result:** `{'checked': 39, 'mismatches': 0}` (**PASS**)
- **Target Manifest:** `outputs/model_v2/integrity_manifest_pre.json`

---

## 3. Multiverse Pipeline Stage Runtimes (`archive/reproducibility_run/model_v4_rerun/`)

- **Execution Command:** `python run_rerun_v4.py`
- **Total Pipeline Runtime:** **295.34 seconds (4.92 minutes)**
- **Stage Breakdown:**
  1. *Checksum Verification:* 0.08s
  2. *Data Load & Foundation Build:* 4.34s
  3. *Multiverse Grid Evaluation (15,150 specs):* 206.14s (3.44 min)
  4. *Multiverse Summary Aggregation:* 16.61s
  5. *ANOVA Variance Decomposition (Sequential Type I):* 4.75s
  6. *Stratified Bootstrap Canonical Evaluation (1,000 draws):* 51.55s
  7. *Pre-Registered Selection Rule Application & Tiering:* 0.08s
  8. *Specification Curves Generation:* 5.76s
  9. *Walk-Forward Temporal Stability Evaluation:* 6.03s

---

## 4. Test Suite & Notebooks Execution

- **Test Suite Command:** `pytest tests/model_v2 tests/model_v3 tests/model_v4 -q`
  - **Result:** `54 passed in 303.74s (0:05:03)` (**100% PASS**)
- **Notebooks Execution Command:** `jupyter nbconvert --to notebook --execute notebooks/01-05`
  - `01_data_exploration.ipynb`: **Executed Successfully**
  - `02_pressure_analysis.ipynb`: **Executed Successfully**
  - `03_batting_analysis.ipynb`: **Executed Successfully**
  - `04_bowling_analysis.ipynb`: **Executed Successfully**
  - `05_model_validation.ipynb`: **Executed Successfully**
  - Destination: `outputs/final_package/notebooks_executed/`

---

## 5. Deliverable Inventory (`outputs/final_package/`)

1. `SupeRR_Final_Report.pdf` (Final compiled PDF, 15 pages, 1.95 MB)
2. `SupeRR_Final_Report.md` (Complete editable source of the report)
3. `REQUIREMENTS_MATRIX.md` (Requirements traceability mapping)
4. `VERIFICATION.md` (Automated data checks & fidelity audits)
5. `REPRODUCIBILITY.md` (Exact bitwise rerun comparison table)
6. `source_register.md` (External fact and citation registry)
7. `final_top10_batters.csv` (Verified top-10 batters)
8. `final_top10_bowlers.csv` (Verified top-10 bowlers)
9. `PREREGISTRATION.md` (Locked pre-registration protocol)
10. `DEVIATIONS.md` (Documentation of zero methodology deviations)
11. `RUN_LOG.md` (This document)
12. `data_audit/` (Step 0 raw data audit profiles, CSVs, and charts)
13. `notebooks_executed/` (Executed copies of all 5 research notebooks)
