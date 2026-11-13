# SupeRR Selector Season 2 — Round 1

Data-driven identification and ranking of the **Top 10 Batters** and **Top 10 Bowlers** who perform most reliably under high-pressure T20 match situations across **IPL** and **T20 International (T20I)** cricket (2022–2026).

---

## Project Structure (V1 Baseline vs V2 Remediated Pipeline)

```text
SupeRR-Selector-Season-2/
│
├── .gitignore                        # Defensive ignores for raw data & Python caches
├── AGENTS.md                         # Workspace governance, immutability & integrity rules
├── README.md                         # Project overview & canonical run commands
├── requirements.txt                  # Exact Python 3.13 environment dependencies
│
├── data/
│   └── raw/                          # Read-only competition PDF & 6 raw CSV tables
│       ├── Round 1 Problem Statement _ SupeRR Selector Season 2.docx.pdf
│       ├── ball_by_ball.csv
│       ├── competition_team_player_mapping.csv
│       ├── competitions.csv
│       ├── matches.csv
│       ├── playing_eleven.csv
│       └── teams.csv
│
├── docs/                             # Competition overview, problem definition, data dictionary & audits
│   ├── 00_COMPETITION_OVERVIEW.md
│   ├── 01_PROBLEM_DEFINITION.md
│   ├── 02_DATA_DICTIONARY.md
│   ├── 03_DATA_AUDIT.md
│   ├── 04_ANALYTICAL_STRATEGY.md
│   └── 05_PROJECT_ROADMAP.md
│
├── src/                              # V1 baseline scripts (preserved read-only)
│   ├── *.py                          # V1 modules (data_loader, state_builder, pressure, baselines, models, run_pipeline)
│   └── model_v2/                     # V2 remediated pipeline package
│
├── tests/
│   └── model_v2/                     # V2 pytest suite (cricket accounting, zero leakage, shrinkage, bootstrap)
│
├── notebooks/                        # Exploratory & diagnostic notebooks
│
└── outputs/
    ├── *.csv, charts/, METHODOLOGY_REPORT.md  # Preserved V1 outputs
    ├── model_audit/                  # Independent Phase 0.5 forensic audit of V1
    ├── model_v2/                     # V2 rankings, diagnostics, integrity manifest, external player research
    └── submission/                   # Final submission report, charts & verified source register
```

---

## Setup & Canonical Commands

Tested on **Python 3.13** with dependencies pinned in [requirements.txt](file:///c:/Users/LENOVO/OneDrive/Desktop/SupeRR-Selector-Season-2/requirements.txt).

```powershell
# Install dependencies (if setting up a fresh environment)
pip install -r requirements.txt

# Run the canonical V2 end-to-end pipeline
python -m src.model_v2.run_pipeline

# Run the V2 unit & statistical integrity test suite
pytest tests/model_v2/ -v

# Run the read-only V1 independent audit verification tests
python outputs/model_audit/test_audit_rules.py
```

---

## Documentation Index

- [00_COMPETITION_OVERVIEW.md](file:///c:/Users/LENOVO/OneDrive/Desktop/SupeRR-Selector-Season-2/docs/00_COMPETITION_OVERVIEW.md) — Challenge brief, submission deliverables, evaluation criteria, and governance rules.
- [01_PROBLEM_DEFINITION.md](file:///c:/Users/LENOVO/OneDrive/Desktop/SupeRR-Selector-Season-2/docs/01_PROBLEM_DEFINITION.md) — Mathematical problem framing, V1 audit synthesis (7 identified methodological issues), and V2 remediation specifications.
- [02_DATA_DICTIONARY.md](file:///c:/Users/LENOVO/OneDrive/Desktop/SupeRR-Selector-Season-2/docs/02_DATA_DICTIONARY.md) — Complete schema, data types, null counts, and edge-case conventions for all 6 raw CSVs.
- [03_DATA_AUDIT.md](file:///c:/Users/LENOVO/OneDrive/Desktop/SupeRR-Selector-Season-2/docs/03_DATA_AUDIT.md) — Empirical dataset audit, anomalies, and exclusions.
- [04_ANALYTICAL_STRATEGY.md](file:///c:/Users/LENOVO/OneDrive/Desktop/SupeRR-Selector-Season-2/docs/04_ANALYTICAL_STRATEGY.md) — Phase 0 analytical design notes.
- [05_PROJECT_ROADMAP.md](file:///c:/Users/LENOVO/OneDrive/Desktop/SupeRR-Selector-Season-2/docs/05_PROJECT_ROADMAP.md) — Phase-by-phase execution roadmap.
- [audit_summary.md](file:///c:/Users/LENOVO/OneDrive/Desktop/SupeRR-Selector-Season-2/outputs/model_audit/audit_summary.md) & [model_formula_audit.md](file:///c:/Users/LENOVO/OneDrive/Desktop/SupeRR-Selector-Season-2/outputs/model_audit/model_formula_audit.md) — Independent forensic audit of the V1 pipeline.
