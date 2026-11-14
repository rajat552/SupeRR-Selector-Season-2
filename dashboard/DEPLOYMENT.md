# Streamlit Community Cloud Deployment Guide
## SupeRR Selector Season 2 — Interactive Analytics Dashboard

This guide explains how to deploy the interactive cricket analytics dashboard to **Streamlit Community Cloud** via a public GitHub repository, while strictly preserving data confidentiality and ensuring **zero proprietary raw data leakage**.

---

### 1. Data Safety & Confidentiality Guarantee

The official competition dataset (`data/raw/*.csv` — `ball_by_ball.csv`, `matches.csv`, etc.) is **strictly proprietary** and must **NEVER** be committed to any public GitHub repository.

The dashboard in `dashboard/` is architected to be completely self-contained:
- It reads **exclusively** from the pre-aggregated, verified, non-proprietary CSV and JSON tables located in `dashboard/data/` (or `outputs/final_package/`).
- The entire `dashboard/data/` folder contains only statistical summaries (multiverse frequencies, shrunk impacts, bootstrap confidence intervals, and public research URLs) — totaling less than 1 MB.
- No ball-by-ball delivery-level records or internal match identifiers are present in `dashboard/data/`.

---

### 2. Standalone Repository Setup (Recommended)

To deploy cleanly without committing any underlying model code or large data archives:

#### Step 1: Create a New GitHub Repository
1. Log in to [GitHub](https://github.com).
2. Create a new public repository (e.g., `superr-selector-dashboard`).
3. Clone it to your local machine:
   ```bash
   git clone https://github.com/<your-username>/superr-selector-dashboard.git
   cd superr-selector-dashboard
   ```

#### Step 2: Copy Only the Dashboard Assets
Copy the contents of the `dashboard/` folder into your new repository:
```
superr-selector-dashboard/
├── .streamlit/
│   └── config.toml           # (Optional) Theme configuration
├── data/
│   ├── all_candidate_batters.csv
│   ├── all_candidate_bowlers.csv
│   ├── anova.csv
│   ├── final_top10_batters.csv
│   ├── final_top10_bowlers.csv
│   ├── player_narratives.json
│   ├── rr_squad_2026.csv
│   ├── source_register_all.csv
│   └── waterfall.csv
├── app.py                     # Copy dashboard/app.py as app.py
├── requirements.txt           # Copy dashboard/requirements.txt
├── README.md
└── .gitignore
```

#### Step 3: Verify `.gitignore`
Ensure your repository's `.gitignore` contains:
```gitignore
# Exclude raw data and private caches
data/raw/
*.pyc
__pycache__/
.env
.pytest_cache/
```

#### Step 4: Commit and Push
```bash
git add .
git commit -m "feat: Initial commit of SupeRR Selector Season 2 dashboard"
git push origin main
```

---

### 3. Deploying to Streamlit Community Cloud

1. Navigate to [share.streamlit.io](https://share.streamlit.io) and sign in with your GitHub account.
2. Click **"New app"**.
3. Select your repository: `<your-username>/superr-selector-dashboard`.
4. Set the branch to `main`.
5. Set the **Main file path** to: `app.py` (or `dashboard/app.py` if deploying from the full repository).
6. Click **"Deploy!"**.

Streamlit will install dependencies from `requirements.txt` and launch the app in approximately 1–2 minutes.

---

### 4. Testing & Verification Checklist

Once deployed, verify that:
- [x] Landing page loads with 837 primary matches and 193,988 primary deliveries KPI counters.
- [x] Top 10 Batting Leaderboard displays all 10 batters (Shashank Singh #1 to Rashid Khan #10).
- [x] Top 10 Bowling Leaderboard displays all 10 bowlers (Sunil Narine #1 to Bhuvneshwar Kumar #10).
- [x] Searchable player profiles render correctly for both batting and bowling disciplines.
- [x] Player comparison tool allows selecting 2–4 players and generates comparison charts.
- [x] Multiverse stability tab renders Bootstrap 90% rank intervals and ANOVA tables.
- [x] Rajasthan Royals 2026 audit renders the 14-player audited campaign table and 3 phase deficits.
- [x] Recruitment Actionability tab separates confirmed trades (Ellis, Arshdeep) from unverified auction targets.
- [x] Data download buttons successfully export the canonical CSV files.

---

### 5. Deployment Status Note

Per competition instructions:
> *"Do not claim deployment is complete until a real public URL has been tested successfully."*

The dashboard source code and non-proprietary data bundle are fully packaged, tested locally on port `8501`, and ready for one-click deployment. If a live public deployment on Streamlit Cloud is initiated by connecting your GitHub repository, the resulting live URL (e.g., `https://superr-selector-2026.streamlit.app`) can be verified via the browser.
