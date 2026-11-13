# Pre-Submission Human Review & Governance Checklist — SupeRR Selector Season 2 (Round 1)

**Prepared:** 2026-11-13  
**Canonical Model:** Model V2 (`model_b` — Attenuated Maintenance & Lift with Continuous Pressure Weights, Kish $N_{\text{eff}}$, LPO Hierarchical Baselines, and Empirical-Bayes Shrinkage)  
**Deliverables Status:** Ready for participant verification prior to Unstop portal upload.  

---

## 1. THE DUAL-LIST ARCHITECTURE: EXACT UNSTOP SUBMISSIONS VS. ACTIONABLE SHORTLIST

To ensure complete clarity and academic/professional distinction, the submission package contains two complementary views:

### View 1: The 20 Historical Statistical Leaders (To Select in the Unstop Portal Form)
These 20 selections represent the strict, unbiased mathematical output of Model V2 across 2022–2026 performance under pressure. They directly answer the literal competition problem statement without arbitrary human filters or subjective deletions.

#### Top 10 Batters Under Pressure (Model B)
| Rank | Exact Dropdown Name / Transliteration | `player_id` | Composite Score | Historical Merit & Practical Context Flag |
|---:|---|---:|---:|---|
| 1 | **Tim David** | 6396 | +2.434 | Active (RCB IPL 2026); Core power-finishing benchmark |
| 2 | **Matthew Wade** | 796 | +2.267 | **Retired / Coaching Flag** (Australia white-ball batting coach Sep 2026; last IPL 2024) |
| 3 | **Naman Dhir** | 37052 | +2.028 | Active (MI IPL 2026 & India white-ball call-up); 360-degree power hitter |
| 4 | **Dinesh Karthik** | 143 | +1.764 | **Retired / Coaching Flag** (RCB Batting Coach & Mentor; retired IPL 2024) |
| 5 | **Reeza Hendricks** | 768 | +1.745 | **Zero IPL Exposure** (SA20 / T20I only); top-order accumulator |
| 6 | **Shashank Singh** | 2756 | +1.609 | Active (PBKS IPL 2026 core finisher); clutch crisis chaser |
| 7 | **Heinrich Klaasen** | 4260 | +1.608 | Active franchise T20 (SRH IPL 2026 INR 23 Cr retention; int'l retired Jun 2025) |
| 8 | **Rinku Singh** | 4708 | +1.445 | Active (KKR vice-captain IPL 2026 core retention); premier death finisher |
| 9 | **Andre Russell** | 1318 | +1.434 | **Retired / Coaching Flag** (KKR Power Coach IPL 2026; retired IPL Nov 2025) |
| 10 | **Ashutosh Sharma** | 8101 | +1.335 | Active (DC IPL 2026); Death SR 200.74; rescued from V1 `lp_balls < 60` defect |

#### Top 10 Bowlers Under Pressure (Model B)
| Rank | Exact Dropdown Name / Transliteration | `player_id` | Composite Score | Historical Merit & Practical Context Flag |
|---:|---|---:|---:|---|
| 1 | **Sunil Narine** | 781 | +2.481 | Active franchise T20 (KKR IPL 2026 core icon; int'l retired Nov 2023) |
| 2 | **Jasprit Bumrah** | 2933 | +1.995 | Active (MI IPL 2026 INR 18 Cr marquee retention); world pace benchmark |
| 3 | **Mustafizur Rahman** | 4373 | +1.851 | Active; BCB registration process initiated (pending BCCI final register Dec 3) |
| 4 | **Jamie Overton** | 2382 | +1.839 | Active (CSK IPL 2026; May 2026 thigh injury recovery); express pace all-rounder |
| 5 | **Mohit Sharma** | 2878 | +1.736 | **Retired / Coaching Flag** (CSK bowling coach; retired all cricket Dec 2025) |
| 6 | **Sai Kishore** *(Ravisrinivasan Sai Kishore)* | 5577 | +1.708 | Active (GT IPL 2026); Pressure ER 6.01; middle-overs squeeze specialist |
| 7 | **Sufiyan Muqeem** *(Sufyan Moqim)* | 34485 | +1.665 | **No Demonstrated IPL Pathway** (geopolitical/governance uncertainty) |
| 8 | **Mohsin Khan** | 6669 | +1.625 | Active (LSG IPL 2026); Indian left-arm pace weapon; prior injury management |
| 9 | **Mohammad Nawaz** | 2490 | +1.556 | **No Demonstrated IPL Pathway** (geopolitical/governance uncertainty) |
| 10 | **Josh Hazlewood** | 830 | +1.472 | Active (RCB IPL 2026 INR 12.5 Cr retention); high-control pace spearhead |

---

### View 2: The Actionable Rajasthan Royals Recruitment Shortlist (For Methodology Report & Defence)
Detailed in [RR_SQUAD_FIT_ANALYSIS.md](file:///c:/Users/LENOVO/OneDrive/Desktop/SupeRR-Selector-Season-2/outputs/submission/RR_SQUAD_FIT_ANALYSIS.md) and [AUCTION_TARGET_DECISION_MATRIX.csv](file:///c:/Users/LENOVO/OneDrive/Desktop/SupeRR-Selector-Season-2/outputs/submission/AUCTION_TARGET_DECISION_MATRIX.csv):
1. **Ashutosh Sharma (Domestic Death Finisher, Rank #10):** High-upside lower-order finishing profile (Death SR 200.74, 42.3% conditional Top-10 bootstrap reliability); complements Dhruv Jurel and Shimron Hetmyer; domestic asset.
2. **R. Sai Kishore (Domestic Defensive Spinner, Rank #6):** Specialist middle-overs restrictive squeeze anchor (6.01 High-Pressure ER, 48.4% dot-ball rate, 61.0 ov in Middle phase at ER 8.54, 81.3% conditional Top-10 bootstrap reliability); complements Ravi Bishnoi (Full-Season ER 9.88, High-Pressure ER 10.00) and preserves Ravindra Jadeja (age 37–38); domestic asset.
3. **Mustafizur Rahman (Overseas Death Specialist, Rank #3):** BCB registration process initiated; addresses death leakage (Sandeep Sharma Full-Season ER 11.39 / Death ER 13.70; Tushar Deshpande Full-Season ER 11.96 / Death ER 12.38); pairs with Jofra Archer (Full-Season ER 9.32, Death ER 9.35).
4. **Scouting Watchlist / Contingency Targets:** Phil Salt (Near-Miss #6 WK-Batter), Mohsin Khan (LSG Trade), Jamie Overton (CSK Release), Naman Dhir (MI Contingent), Shashank Singh (PBKS Contingent).

---

## 2. MANDATORY PRE-SUBMISSION CHECKS FOR THE PARTICIPANT

1. **Unstop Submission Interface Duality & Form Input:**
   - **Scenario A (Dropdowns Present):** If the portal features dropdown menus for player selection (as described in the problem statement document), select the 20 Canonical Leaders. If restricted to uncapped domestic players, select from the Uncapped Indian Contingency Rankings in [RANKING_INTERPRETATION_AND_SCOPE.md](file:///c:/Users/LENOVO/OneDrive/Desktop/SupeRR-Selector-Season-2/outputs/submission/RANKING_INTERPRETATION_AND_SCOPE.md) (Shashank Singh #1, Ashutosh Sharma #2, Ayush Badoni #3 / Mohsin Khan #1, Yash Dayal #2, Rasikh Salam #3). Note transliterations: `Sai Kishore` may appear as `Ravisrinivasan Sai Kishore`; `Sufiyan Muqeem` as `Sufyan Moqim`.
   - **Scenario B (Document Upload Only):** If the portal provides a document-upload interface only (e.g., single PDF/deck upload as per the public overview), upload [SupeRR_Selector_Round1_Methodology_Report.pdf](file:///c:/Users/LENOVO/OneDrive/Desktop/SupeRR-Selector-Season-2/outputs/submission/SupeRR_Selector_Round1_Methodology_Report.pdf). All 20 canonical selections, actionable targets, and uncapped contingency rankings are comprehensively presented inside the report.

2. **`Unverified` IPL 2027 Auction Timeline (Key Governance Dates):**
   - **2026-11-17:** Official BCCI IPL 2027 retention/release list submission deadline.
   - **2026-11-23:** Player auction registration deadline.
   - **2026-12-03:** Official BCCI auction register and sets published.
   - **2026-12-16:** IPL 2027 Mini-Auction in Goa.
   - *Guidance:* If submitting or presenting after November 17, consult the official retention press release on `iplt20.com` to confirm any late trade or release announcements.

3. **Verbal / Written Defence Strategy:**
   - If evaluators ask why retired players (Wade, Karthik, Mohit Sharma, Russell) or franchise icons (Bumrah, Narine) appear in your Top 10:
     > *"We maintain strict scientific governance by separating statistical performance measurement from operational auction feasibility. The 20 selections submitted represent the objective, mathematically proven leaders under pressure across the 2022–2026 dataset as mandated by the Round 1 prompt. In our report’s Section 9 and dedicated RR Squad Fit Analysis, we apply franchise operational filters to deliver an actionable recruitment roadmap targeting Ashutosh Sharma, R. Sai Kishore, and Mustafizur Rahman."*

---

## 3. FINAL DELIVERABLE RECONCILIATION

Ensure all deliverables in `outputs/submission/` are packaged and ready:
1. [SupeRR_Selector_Round1_Methodology_Report.pdf](file:///c:/Users/LENOVO/OneDrive/Desktop/SupeRR-Selector-Season-2/outputs/submission/SupeRR_Selector_Round1_Methodology_Report.pdf) (Primary PDF deliverable, compiled with 12 clean, de-overlapped visual charts)
2. [final_batting_rankings.csv](file:///c:/Users/LENOVO/OneDrive/Desktop/SupeRR-Selector-Season-2/outputs/submission/final_batting_rankings.csv) (Complete statistical ranking of all batters)
3. [final_bowling_rankings.csv](file:///c:/Users/LENOVO/OneDrive/Desktop/SupeRR-Selector-Season-2/outputs/submission/final_bowling_rankings.csv) (Complete statistical ranking of all bowlers)
4. [AUCTION_TARGET_DECISION_MATRIX.csv](file:///c:/Users/LENOVO/OneDrive/Desktop/SupeRR-Selector-Season-2/outputs/submission/AUCTION_TARGET_DECISION_MATRIX.csv) (10-dimension franchise evaluation matrix)
5. [RR_SQUAD_FIT_ANALYSIS.md](file:///c:/Users/LENOVO/OneDrive/Desktop/SupeRR-Selector-Season-2/outputs/submission/RR_SQUAD_FIT_ANALYSIS.md) (27-player squad audit, Sai Kishore case study & scouting cards)
6. [RANKING_INTERPRETATION_AND_SCOPE.md](file:///c:/Users/LENOVO/OneDrive/Desktop/SupeRR-Selector-Season-2/outputs/submission/RANKING_INTERPRETATION_AND_SCOPE.md) (Problem statement scope & dual-list governance briefing)
7. [source_register.md](file:///c:/Users/LENOVO/OneDrive/Desktop/SupeRR-Selector-Season-2/outputs/submission/source_register.md) (External cricket research & evidence classifications)
8. [user_review_required.md](file:///c:/Users/LENOVO/OneDrive/Desktop/SupeRR-Selector-Season-2/outputs/submission/user_review_required.md) (This governance checklist)
