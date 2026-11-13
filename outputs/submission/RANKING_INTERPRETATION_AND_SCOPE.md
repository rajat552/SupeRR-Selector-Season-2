# RANKING INTERPRETATION, COMPETITION SCOPE & UNSTOP SUBMISSION GUIDE
## Comprehensive Governance Briefing on Competition Problem Statement, Dataset Scope & Dual-List Framework
**Competition:** SupeRR Selector Season 2 (Round 1) — Rajasthan Royals  
**Document Classification:** Official Submission Strategy & Governance Protocol  
**Author:** Franchise Analytics & Statistical Model Governance Team  

---

## 1. OFFICIAL COMPETITION PROBLEM STATEMENT DECONSTRUCTION

To establish absolute compliance with competition rules, the official Round 1 problem statement (`Round 1 Problem Statement _ SupeRR Selector Season 2.docx.pdf`) and the Unstop portal specifications have been independently audited.

### 1.1 The "Uncapped Player" Question: Marketing vs. Official Specification
A critical point of clarity concerns whether Round 1 is strictly restricted to "uncapped" players.
- **The Finding:** The **official Round 1 problem statement document does NOT mandate or restrict rankings to uncapped players.**
- **Exact Document Language:** The problem statement explicitly instructs participants to evaluate player performance under high-pressure match situations across the provided proprietary 2022–2026 dataset (encompassing all IPL and international T20 matches) and submit two ranked lists:
  1. **Top-10 Batters Under Pressure**
  2. **Top-10 Bowlers Under Pressure**
- **Dataset Composition:** The dataset supplied by Rajasthan Royals contains complete ball-by-ball records from 367 IPL matches and 470 international T20Is (ICC Men's T20 World Cups, bilateral series, and qualifiers). This data structure inherently includes international superstars (e.g., Jasprit Bumrah, Sunil Narine, Heinrich Klaasen, Tim David) alongside domestic emerging players.
- **Portal Copy Reconciliation:** Certain marketing banners or introductory copy on Unstop use phrases like *"find the next breakout stars"* or *"unearth hidden gems"*. In professional franchise scouting, these promotional statements reflect the strategic *goal* of analytics (finding undervalued talent), whereas the technical assignment evaluates all players on an equal statistical footing.
- **Strategic Resolution:** Restricting the initial statistical model to uncapped players would introduce severe selection bias, discard 85% of high-pressure deliveries, and artificially distort the Bayesian shrinkage priors. Therefore, the **statistical rankings (Model V2) evaluate all eligible players in the dataset**, while the **RR Squad Fit & Recruitment Shortlist** specifically surfaces actionable, high-value emerging and domestic players (such as Ashutosh Sharma and R. Sai Kishore).

### 1.2 Uncapped Indian Player Contingency Ranking (Alternative Filter View)
To provide complete strategic coverage in the event that evaluators or a specific portal submission track evaluate participants strictly on uncapped Indian talent, Model V2 generates an explicit **Uncapped Indian Player Contingency Ranking** (filtered for Indian domestic players with zero senior international caps during the 2022–2026 dataset window):

#### Uncapped Indian Batters Under Pressure (Model B Contingency)
| Uncapped Rank | Overall Rank | Player ID | Player Name | Composite Score | Shrunk WP Impact (/100b) | HP Balls Faced | Notes & Practical Status |
|:---:|:---:|:---:|:---|:---:|:---:|:---:|:---|
| **1** | #6 | 2756 | **Shashank Singh** | +1.609 | +32.42 | 327 | PBKS core finisher; elite clutch chase execution |
| **2** | #10 | 8101 | **Ashutosh Sharma** | +1.335 | +24.97 | 273 | DC finisher; 200.74 Death SR; primary RR target |
| **3** | #27 | 7426 | **Ayush Badoni** | +0.941 | +15.82 | 268 | LSG middle-order crisis accumulator & finisher |
| **4** | #50 | 2734 | **Nitish Rana** | +0.528 | +8.45 | 185 | Experienced domestic anchor/hitter (KKR/domestic) |
| **5** | #63 | 6967 | **Rajat Patidar** | +0.334 | +5.12 | 212 | RCB middle-overs spin enforcer |
| **6** | #64 | 2792 | **Rahul Tewatia** | +0.327 | +4.98 | 240 | GT domestic death specialist |
| **7** | #72 | 7437 | **Sai Sudharsan** | +0.224 | +3.10 | 194 | GT top-order anchor |
| **8** | #74 | 7446 | **Abdul Samad** | +0.170 | +2.45 | 165 | SRH domestic lower-order hitter |
| **9** | #75 | 8136 | **Nehal Wadhera** | +0.165 | +2.20 | 142 | MI middle-order left-handed power hitter |
| **10** | #85 | 6827 | **M Shahrukh Khan** | -0.053 | -0.84 | 158 | GT domestic power finisher |

*(Note on **Naman Dhir** [`37052`, Overall #3, Composite +2.028]: Had 0 senior international caps during the 2022–2026 dataset period; earned maiden India white-ball squad call-up in September 2026. If classified as uncapped prior to official debut, he ranks **#1** among uncapped batters).*

#### Uncapped Indian Bowlers Under Pressure (Model B Contingency)
| Uncapped Rank | Overall Rank | Player ID | Player Name | Composite Score | Shrunk WP Impact (/24b) | HP Balls Bowled | Notes & Practical Status |
|:---:|:---:|:---:|:---|:---:|:---:|:---:|:---|
| **1** | #8 | 6669 | **Mohsin Khan** | +1.625 | +8.16 | 163 | LSG left-arm strike pacer; elite death execution |
| **2** | #36 | 7427 | **Yash Dayal** | +0.767 | +3.88 | 210 | RCB left-arm seamer; swing and death discipline |
| **3** | #38 | 5482 | **Rasikh Salam** | +0.742 | +3.65 | 178 | DC seam bowler; deceptive change of pace |
| **4** | #79 | 8138 | **Suyash Sharma** | +0.222 | +1.12 | 145 | KKR domestic leg-break/googly bowler |
| **5** | #108 | 6797 | **Kartik Tyagi** | -0.198 | -1.02 | 134 | Express pace seamer (145+ kph) |
| **6** | #114 | 27393 | **Digvesh Rathi** | -0.285 | -1.44 | 128 | Domestic seam bowler |
| **7** | #123 | 6818 | **Vaibhav Arora** | -0.478 | -2.35 | 152 | KKR swing bowler |

*(Note on **R. Sai Kishore** [`5577`, Overall #6, Composite +1.708]: Represented India in the 2023 Asian Games [3 T20I caps], making him technically capped in official ICC records, though uncapped in bilateral senior series; Sunil Narine and Mohit Sharma are capped internationals).*

---

## 2. DATASET BOUNDARIES & FORMAT SCOPE SENSITIVITY

### 2.1 Primary Analyzed Scope (Scope A: 837 Matches)
The proprietary dataset provided by Rajasthan Royals spans six competitions across the 2022–2026 cycle:

$$\text{Scope A (Primary Baseline)} = 837 \text{ Matches} \quad (367 \text{ IPL} + 470 \text{ T20I})$$

- **Total Deliveries:** 193,988 deliveries.
- **Legal Deliveries:** 185,692 balls (cricket accounting applied: wides and no-balls separated).
- **Excluded Categories:**
  1. **Abandoned / No-Result Fixtures:** 16 matches with zero deliveries bowled.
  2. **Super Overs:** 38 deliveries (Innings 3 and 4) excluded from regulation state-space models due to non-standard strategic incentives.
  3. **Other_T20 Developmental Fixtures:** 30 matches (6,985 balls) across `comp_id = 2670` and `comp_id = 3289`.

### 2.2 Sensitivity Analysis: Inclusion of `Other_T20` (Scope B: 867 Matches)
To prove that Model V2 rankings do not depend on the exclusion of `Other_T20` (emerging/developmental A-team tournaments), we executed a comprehensive sensitivity test across Scope B (200,961 total balls).

| Player Name | Role | Scope A Pressure Score (837 Matches) | Scope B Pressure Score (867 Matches) | Score Delta ($\Delta$) | Scope A Rank | Scope B Rank | Deliveries in Other_T20 |
|:---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **Tim David** | Batter | 2.4336 | 2.4336 | 0.0000 | #1 | #1 | 0 balls |
| **Matthew Wade** | Batter | 2.2669 | 2.2669 | 0.0000 | #2 | #2 | 0 balls |
| **Naman Dhir** | Batter | 2.0283 | 2.0512 | +0.0229 | #3 | #3 | 74 balls |
| **Dinesh Karthik** | Batter | 1.7640 | 1.7640 | 0.0000 | #4 | #4 | 0 balls |
| **Reeza Hendricks** | Batter | 1.7452 | 1.7452 | 0.0000 | #5 | #5 | 0 balls |
| **Shashank Singh** | Batter | 1.6086 | 1.6086 | 0.0000 | #6 | #6 | 0 balls |
| **Heinrich Klaasen** | Batter | 1.6082 | 1.6082 | 0.0000 | #7 | #7 | 0 balls |
| **Rinku Singh** | Batter | 1.4450 | 1.4450 | 0.0000 | #8 | #8 | 0 balls |
| **Andre Russell** | Batter | 1.4339 | 1.4339 | 0.0000 | #9 | #9 | 0 balls |
| **Ashutosh Sharma** | Batter | 1.3355 | 1.3392 | +0.0037 | #10 | #10 | 12 balls |
| **Sunil Narine** | Bowler | 2.4810 | 2.4810 | 0.0000 | #1 | #1 | 0 balls |
| **Jasprit Bumrah** | Bowler | 1.9954 | 1.9954 | 0.0000 | #2 | #2 | 0 balls |
| **Mustafizur Rahman** | Bowler | 1.8505 | 1.8505 | 0.0000 | #3 | #3 | 0 balls |
| **Jamie Overton** | Bowler | 1.8389 | 1.8389 | 0.0000 | #4 | #4 | 0 balls |
| **Mohit Sharma** | Bowler | 1.7363 | 1.7363 | 0.0000 | #5 | #5 | 0 balls |
| **R. Sai Kishore** | Bowler | 1.7076 | 1.7041 | -0.0035 | #6 | #6 | 24 balls |
| **Sufiyan Muqeem** | Bowler | 1.6648 | 1.6982 | +0.0334 | #7 | #7 | 174 balls |
| **Mohsin Khan** | Bowler | 1.6249 | 1.6249 | 0.0000 | #8 | #8 | 0 balls |
| **Mohammad Nawaz** | Bowler | 1.5557 | 1.5557 | 0.0000 | #9 | #9 | 0 balls |
| **Josh Hazlewood** | Bowler | 1.4719 | 1.4719 | 0.0000 | #10 | #10 | 0 balls |

> [!NOTE]
> **Audit Finding:** Across all 20 players, **zero ranking order changes occur between Scope A and Scope B.** The rank correlation is $\rho = 1.000$. The statistical architecture is completely invariant to this scope definition.

---

## 3. THE DUAL-LIST SELECTION FRAMEWORK

To meet both the rigorous academic requirements of Unstop evaluation and the practical operational standards of Rajasthan Royals' recruitment department, the project delivers two clear, distinct analytical lenses:

```
                                  PROPRIETARY DATASET (2022-2026)
                                                 │
                                                 ▼
                                     MODEL V2 EMPIRICAL ENGINE
                                 (Win Probability Impact + EB Lift)
                                                 │
                     ┌───────────────────────────┴───────────────────────────┐
                     ▼                                                       ▼
        VIEW 1: STATISTICAL LEADERS                             VIEW 2: ACTIONABLE RECRUITMENT
     (Canonical Mathematical Output)                         (Franchise Tactical Architecture)
                     │                                                       │
  • Pure quantitative ranking                               • Filtered by Auction Feasibility
  • 10 Batters & 10 Bowlers                                 • 2026 RR Squad Deficits Addressed
  • Unbiased historical merit                               • Contract / Retention Status
  • Formally submitted in Unstop Form                       • Core Targets: Ashutosh, Sai Kishore,
                                                              Mustafizur Rahman
```

### 3.1 View 1: Historical Statistical Leaders (The 20 Canonical Selections)
- **Definition:** The objective mathematical output of Model V2, ranking players by shrunken high-pressure win-probability impact and maintenance lift across 2022–2026.
- **Batting Top-10:**
  1. Tim David
  2. Matthew Wade
  3. Naman Dhir
  4. Dinesh Karthik
  5. Reeza Hendricks
  6. Shashank Singh
  7. Heinrich Klaasen
  8. Rinku Singh
  9. Andre Russell
  10. Ashutosh Sharma
- **Bowling Top-10:**
  1. Sunil Narine
  2. Jasprit Bumrah
  3. Mustafizur Rahman
  4. Jamie Overton
  5. Mohit Sharma
  6. R. Sai Kishore
  7. Sufiyan Muqeem
  8. Mohsin Khan
  9. Mohammad Nawaz
  10. Josh Hazlewood
- **Purpose:** Answers the direct, literal prompt: *"Who performed best under pressure in the dataset?"* It proves mathematical mastery, statistical robustness, and data engineering integrity.

### 3.2 View 2: Actionable RR Recruitment Shortlist (Auction Targets)
- **Definition:** The practical franchise recruitment strategy that translates statistical excellence into auction execution for the IPL 2027 auction (retention deadline Nov 17, 2026).
- **Core Actionable Targets:**
  1. **Ashutosh Sharma (Domestic Death Finisher):** High-upside lower-order finishing profile (Death SR 200.74, 42.3% conditional Top-10 bootstrap reliability); complements Dhruv Jurel and Shimron Hetmyer; domestic asset.
  2. **R. Sai Kishore (Domestic Defensive Spinner):** Specialist middle-overs restrictive squeeze anchor (6.01 High-Pressure ER, 48.4% dot-ball rate, 61.0 ov in Middle phase at ER 8.54, 81.3% conditional Top-10 bootstrap reliability); complements Ravi Bishnoi (Full-Season ER 9.88, High-Pressure ER 10.00) and preserves Ravindra Jadeja (age 37–38); domestic asset.
  3. **Mustafizur Rahman (Overseas Death Cutter Specialist):** BCB registration process initiated (pending BCCI shortlisting); addresses death leakage (Sandeep Sharma Full-Season ER 11.39 / Death ER 13.70; Tushar Deshpande Full-Season ER 11.96 / Death ER 12.38); pairs with Jofra Archer (Full-Season ER 9.32, Death ER 9.35, High-Pressure ER 8.27).
- **Contingent & Near-Miss Watchlist:** Phil Salt (Near-Miss #6 WK-Batter), Mohsin Khan (LSG Trade), Jamie Overton (CSK Release), Naman Dhir (MI Contingent), Shashank Singh (PBKS Contingent).

---

## 4. UNSTOP PORTAL SUBMISSION PROTOCOL & INTERFACE DUALITY

Depending on the specific submission form configuration presented on the live Unstop portal, participants should follow the appropriate submission path below:

### Scenario A: If Player Selection Dropdown Menus Are Present
If the live portal interface features explicit dropdown fields for player selection (as described in the competition problem statement document):
1. **Select the 20 Canonical Statistical Leaders (View 1):**
   - **Top 10 Batters:** Tim David, Matthew Wade, Naman Dhir, Dinesh Karthik, Reeza Hendricks, Shashank Singh, Heinrich Klaasen, Rinku Singh, Andre Russell, Ashutosh Sharma.
   - **Top 10 Bowlers:** Sunil Narine, Jasprit Bumrah, Mustafizur Rahman, Jamie Overton, Mohit Sharma, R. Sai Kishore *(or Ravisrinivasan Sai Kishore)*, Sufiyan Muqeem *(or Sufyan Moqim)*, Mohsin Khan, Mohammad Nawaz, Josh Hazlewood.
2. **Alternative Uncapped Selection:** If the portal interface explicitly restricts dropdown options to uncapped domestic players, select from the **Uncapped Indian Player Contingency Ranking** established in Section 1.2:
   - *Batters:* Shashank Singh (#1), Ashutosh Sharma (#2), Ayush Badoni (#3), Nitish Rana (#4), Rajat Patidar (#5), Rahul Tewatia (#6), Sai Sudharsan (#7), Abdul Samad (#8), Nehal Wadhera (#9), M Shahrukh Khan (#10). *(Include Naman Dhir if classified uncapped).*
   - *Bowlers:* Mohsin Khan (#1), Yash Dayal (#2), Rasikh Salam (#3), Suyash Sharma (#4), Kartik Tyagi (#5), Digvesh Rathi (#6), Vaibhav Arora (#7).

### Scenario B: If Document-Upload Only (PDF / PPT / Dashboard)
If the live portal interface consists of a standard document-upload field without individual player dropdowns (as indicated in the public Unstop competition overview):
1. **Upload the Primary PDF Deliverable:** Attach `outputs/submission/SupeRR_Selector_Round1_Methodology_Report.pdf`.
2. **Supplementary File / URL Fields:** If supplementary attachment or text/URL fields are provided, submit links or files for:
   - `outputs/submission/final_batting_rankings.csv`
   - `outputs/submission/final_bowling_rankings.csv`
   - `outputs/submission/AUCTION_TARGET_DECISION_MATRIX.csv`
   - `outputs/submission/RR_SQUAD_FIT_ANALYSIS.md`

### Defending the Framework in Evaluation / Q&A
If questioned by the evaluators regarding the presence of retired players (e.g., Matthew Wade, Dinesh Karthik, Mohit Sharma) or franchise-locked icons (Jasprit Bumrah, Sunil Narine):
> *"Our analytical architecture strictly adheres to scientific governance by keeping statistical measurement separate from operational feasibility. The Top-10 ranking represents the unbiased mathematical evaluation of 2022–2026 performance under pressure requested by the problem statement. In Section 9 of our methodology report and our dedicated RR Squad Fit Analysis, we translate these empirical insights into an actionable IPL 2027 recruitment plan, highlighting Ashutosh Sharma, R. Sai Kishore, and Mustafizur Rahman as the primary actionable targets, alongside a dedicated uncapped contingency ranking."*

This dual-framework structure provides an airtight defense that satisfies both academic data science rubrics and professional franchise front-office criteria.

