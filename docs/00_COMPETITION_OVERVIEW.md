# 00 — Competition Overview

**Event:** SupeRR Selector Season 2 — Round 1  
**Theme:** *Identify the Most Reliable Players Under Pressure*  
**Primary Source:** [Round 1 Problem Statement _ SupeRR Selector Season 2.docx.pdf](file:///c:/Users/LENOVO/OneDrive/Desktop/SupeRR-Selector-Season-2/data/raw/Round%201%20Problem%20Statement%20_%20SupeRR%20Selector%20Season%202.docx.pdf)

---

## 1. Challenge Objective

Build a transparent, reproducible, data-driven system that measures how batters and bowlers perform in **high-pressure match situations** relative to their **usual performance levels**, and use it to identify and rank the **10 most reliable batters** and **10 most reliable bowlers** under pressure.

Key challenge mandates from the official Round 1 Problem Statement:
- **Define Pressure Explicitly:** Pressure may incorporate required run rate, wickets in hand, balls remaining, innings stage, contest closeness, and other relevant match-context signals. The chosen definition must be justified and shown to separate genuine pressure situations from ordinary ones.
- **Dual-Discipline Coverage:** The methodology must work coherently for both **batting** and **bowling**.
- **Data-Backed Selection (No Reputation Bias):** Rankings must be supported by rigorous analysis of the supplied historical IPL and T20I dataset (2022–2026), not reputation alone.
- **Full Transparency & Reproducibility:** Documentation must be clear enough for an independent reviewer to understand and reproduce the methodology.

---

## 2. Official Dataset Provided (`data/raw/`)

Historical IPL and T20 International (T20I) records from **2022-01-22 to 2026-11-01** across 6 CSV files:
1. `ball_by_ball.csv` (`200,999` rows, `33` columns) — Delivery-level match events.
2. `matches.csv` (`883` rows, `22` columns) — Match metadata, venues, dates, captains, toss, D/L revisions, and results.
3. `competitions.csv` (`141` rows, `4` columns) — Competition IDs, names, formats (`T20`, `T20I`), and seasons.
4. `teams.csv` (`353` rows, `3` columns) — Competition-to-team mappings (`38` unique teams).
5. `playing_eleven.csv` (`28,381` rows, `9` columns) — Playing XIs, substitutes/impact players, captain/keeper flags, and batting order.
6. `competition_team_player_mapping.csv` (`6,413` rows, `6` columns) — Roster mappings (`1,217` unique `player_id`s).

*(See [02_DATA_DICTIONARY.md](file:///c:/Users/LENOVO/OneDrive/Desktop/SupeRR-Selector-Season-2/docs/02_DATA_DICTIONARY.md) and [03_DATA_AUDIT.md](file:///c:/Users/LENOVO/OneDrive/Desktop/SupeRR-Selector-Season-2/docs/03_DATA_AUDIT.md) for full schemas and verified audit counts. Note that `competitions.csv` also contains 2 non-IPL `T20` A-team competitions totaling 30 matches / 6,985 deliveries, which are excluded from the primary 837-match IPL+T20I scope.)*

---

## 3. Required Submission Deliverables

The official Round 1 submission consists of **two mandatory components** (plus one optional community component):

### 01 — Player Rankings (Unstop Dropdowns)
- Two ordered Top-10 lists selected via the Unstop submission dropdowns:
  - **Top 10 Batters under pressure** (Rank 1 through Rank 10, where Rank 1 is highest-rated).
  - **Top 10 Bowlers under pressure** (Rank 1 through Rank 10, where Rank 1 is highest-rated).
- **Constraints:** No repeated players within a Top-10 list; dropdown selections and ordering must match the Methodology Report 1:1.

### 02 — Methodology Report (Document Upload)
A comprehensive report explaining how pressure was defined, ratings were constructed, data was analysed, and final rankings were produced. Required sections:
1. **Pressure Definition:** Match situations and indicators used, and why they capture pressure.
2. **Performance Measurement:** Batting and bowling metrics, player baselines, and rating/scoring logic.
3. **Fair Comparisons:** Sample-size treatment, player eligibility, match-context adjustments, and handling of IPL vs T20I data.
4. **Evidence for Top 10:** Quantitative results, comparisons, tables, and charts supporting selections and rank ordering.
5. **Reliability and Limitations:** Cross-match consistency checks, uncertainty quantification, and where the model is less certain.

### Optional — Share Your Journey
- Optional photos, screenshots, or a 30–60s video describing the approach and an interesting insight (does not affect evaluation).

---

## 4. Data Governance & Analytical Integrity Principles

1. **Raw Data Immutability & Confidentiality:** Files under `data/raw/` are strictly read-only and never shared in external queries.
2. **Identity Disambiguation:** All player joins and aggregations key on `player_id` rather than `player_name` to prevent homonym collisions (`Abdul Samad`, `Rashid Khan`, `Haider Ali`).
3. **Zero Look-Ahead:** Every pressure indicator, match-state feature, and opponent-strength rating is computed strictly from information available *before* the delivery or match occurs.
4. **Separation of Statistical Merit vs Franchise Constraints:** Statistical rankings reflect 2022–2026 on-field data; external IPL 2027 availability, retirement, or BCCI participation context is tracked separately with verifiable public citations in `outputs/submission/source_register.md`.
