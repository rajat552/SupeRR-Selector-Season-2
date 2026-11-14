# FINAL HUMAN REVIEW & SUBMISSION DOSSIER
## SupeRR Selector Season 2 (Round 1) — Rajasthan Royals IPL 2027 Auction Strategy
**Date:** 2026-11-13  
**Status:** READY FOR PARTICIPANT REVIEW (Phase 4.2 Factual Reconciliation Completed)  
**Governing Dataset:** Proprietary Rajasthan Royals Performance Dataset (IPL 2022–2026, T20I 2022–2026)  
**Lead Architecture:** Model V2 (`model_b` — Attenuated Maintenance & Lift Engine)  

---

## 1. EXECUTIVE SUBMISSION SUMMARY

All analytical modelling, statistical validation, visual de-overlapping, and recruitment strategy refinement for Round 1 of the SupeRR Selector Season 2 competition are complete. 

This project delivers a **dual-framework architecture** that satisfies both the scientific evaluation rubrics of sports data science and the practical operational requirements of Rajasthan Royals' recruitment department:
1. **View 1: The 20 Historical Statistical Leaders (Canonical Selections):**  
   The objective, mathematically uncompromised output of Model V2 evaluating 2022–2026 performance under pressure across 837 matches and 193,988 deliveries. **These 20 players represent the canonical ranking submitted if player dropdowns are present, and form the core analytical foundation of the report.**
2. **View 2: The Actionable Rajasthan Royals Recruitment Shortlist:**  
   The real-world franchise operational strategy that filters statistical excellence through contract realities, player retirements, bilateral governance realities, overseas slot limits, and RR's specific 2026 squad deficits. **This strategy centers on Ashutosh Sharma, R. Sai Kishore, and Mustafizur Rahman as primary targets.**
3. **Contingency View: Uncapped Indian Player Rankings:**  
   In case the live submission portal or evaluators specifically assess uncapped domestic players, an explicit contingency ranking is provided in [RANKING_INTERPRETATION_AND_SCOPE.md](file:///c:/Users/LENOVO/OneDrive/Desktop/SupeRR-Selector-Season-2/outputs/submission/RANKING_INTERPRETATION_AND_SCOPE.md) (Top 10 Batters led by Shashank Singh and Ashutosh Sharma; Top 7 Bowlers led by Mohsin Khan and Yash Dayal).

---

## 2. THE 20 OFFICIAL UNSTOP SELECTIONS (CANONICAL RANKING)

If player selection dropdown menus are present on the Unstop submission form, enter the 20 selections below in exact numerical order:

### Top 10 Batters Under Pressure (Model B Canonical)
| Rank | Exact Dropdown Name / Transliteration | `player_id` | Composite Score | Role | Practical Context Flag |
|:---:|:---|:---:|:---:|:---|:---|
| **1** | **Tim David** | 6396 | **+2.434** | Finisher 6+ | Active (RCB IPL 2026); Core power-finishing benchmark |
| **2** | **Matthew Wade** | 796 | **+2.267** | Finisher 6+ | **Retired / Coaching Staff** (Australia batting coach Sep 2026) |
| **3** | **Naman Dhir** | 37052 | **+2.028** | Finisher 6+ | Active (MI IPL 2026 & India white-ball squad call-up) |
| **4** | **Dinesh Karthik** | 143 | **+1.764** | Finisher 6+ | **Retired / Coaching Staff** (RCB Batting Coach & Mentor) |
| **5** | **Reeza Hendricks** | 768 | **+1.745** | Top 1-3 | **Zero IPL Exposure** (SA20 / South Africa T20I only) |
| **6** | **Shashank Singh** | 2756 | **+1.609** | Finisher 6+ | Active (PBKS IPL 2026 core finisher; INR 5.5 Cr anchor) |
| **7** | **Heinrich Klaasen** | 4260 | **+1.608** | Middle 4-5 | Active Franchise T20 (SRH IPL 2026 INR 23 Cr retention) |
| **8** | **Rinku Singh** | 4708 | **+1.445** | Finisher 6+ | Active (KKR vice-captain IPL 2026 core retention) |
| **9** | **Andre Russell** | 1318 | **+1.434** | Finisher 6+ | **Retired from IPL / Support Staff** (KKR Power Coach IPL 2026) |
| **10** | **Ashutosh Sharma** | 8101 | **+1.335** | Finisher 6+ | Active (DC IPL 2026); Rescued from V1 `lp_balls < 60` defect |

### Top 10 Bowlers Under Pressure (Model B Canonical)
| Rank | Exact Dropdown Name / Transliteration | `player_id` | Composite Score | Role / Style | Practical Context Flag |
|:---:|:---|:---:|:---:|:---|:---|
| **1** | **Sunil Narine** | 781 | **+2.481** | Spin_Finger | Active Franchise T20 (KKR icon; first overseas to 200 IPL wkts) |
| **2** | **Jasprit Bumrah** | 2933 | **+1.995** | Pace_Fast | Active (MI IPL 2026 INR 18 Cr marquee retention) |
| **3** | **Mustafizur Rahman** | 4373 | **+1.851** | Pace_Medium | Active; BCB registration process initiated (pending BCCI final register Dec 3) |
| **4** | **Jamie Overton** | 2382 | **+1.839** | Pace_Fast | Active (CSK IPL 2026; May 2026 thigh injury recovery) |
| **5** | **Mohit Sharma** | 2878 | **+1.736** | Pace_FastMedium | **Retired / Coaching Staff** (CSK bowling coach; retired Dec 2025) |
| **6** | **Sai Kishore** *(Ravisrinivasan Sai Kishore)* | 5577 | **+1.708** | Spin_Finger | Active (GT IPL 2026); Pressure ER 6.01; middle-overs squeeze specialist |
| **7** | **Sufiyan Muqeem** *(Sufyan Moqim)* | 34485 | **+1.665** | Spin_Wrist | **No Demonstrated IPL Pathway** (geopolitical/governance uncertainty) |
| **8** | **Mohsin Khan** | 6669 | **+1.625** | Pace_FastMedium | Active (LSG IPL 2026; 11 wkts in 7 games; injury management) |
| **9** | **Mohammad Nawaz** | 2490 | **+1.556** | Spin_Finger | **No Demonstrated IPL Pathway** (geopolitical/governance uncertainty) |
| **10** | **Josh Hazlewood** | 830 | **+1.472** | Pace_FastMedium | Active (RCB IPL 2026 INR 12.5 Cr retention; 151-day layoff) |

---

## 3. THE ACTIONABLE RR RECRUITMENT SHORTLIST (IPL 2027)

Derived from the forensic audit of Rajasthan Royals' 2026 roster (27 players) and detailed in [RR_SQUAD_FIT_ANALYSIS.md](file:///c:/Users/LENOVO/OneDrive/Desktop/SupeRR-Selector-Season-2/outputs/submission/RR_SQUAD_FIT_ANALYSIS.md):

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                        RAJASTHAN ROYALS ACTIONABLE SHORTLIST                           │
├────────────────────────────────────────────────────────────────────────────────────────┤
│ 1. ASHUTOSH SHARMA (Domestic Death Finisher, Rank #10):                                │
│    • Death Strike Rate: 200.74 | Shrunk Impact: +24.97 / 100b                          │
│    • High-upside domestic finishing profile (42.3% conditional Top-10 bootstrap freq). │
│    • Complements Dhruv Jurel (#5) and Hetmyer; provides crucial lower-order depth.     │
│                                                                                        │
│ 2. R. SAI KISHORE (Domestic Defensive Spinner, Rank #6):                               │
│    • Pressure Economy Rate: 6.01 RPO | Dot-Ball Rate: 48.4%                            │
│    • 6ft 3in release creates steep bounce & over-spin; middle-overs restrictive anchor │
│      (61.0 ov in Middle phase at ER 8.54, 23 wkts; 3.0 ov in PP).                      │
│    • Complements Ravi Bishnoi (Full-Season ER 9.88, HP ER 10.00) via dot-ball squeeze.│
│    • Takes 4-over defensive bank, allowing Ravindra Jadeja (age 37-38) to bowl 2       │
│      situational overs and preserve batting energy. Zero overseas slot cost.           │
│                                                                                        │
│ 3. MUSTAFIZUR RAHMAN (Overseas Left-Arm Death Cutter Pacer, Rank #3):                  │
│    • Death Economy Rate: 8.24 RPO | Shrunk Impact: +8.04 / 24b                         │
│    • BCB registration process initiated (pending BCCI shortlisting; 2026 KKR release   │
│      noted as a regulatory/participation risk factor).                                 │
│    • Addresses Sandeep Sharma (Full ER 11.39 / Death ER 13.70) & Deshpande (Full ER   │
│      11.96 / Death ER 12.38) death leakage in tandem with Jofra Archer (Full ER 9.32). │
│                                                                                        │
│ 4. KEY CONTINGENCY TARGETS:                                                            │
│    • Phil Salt (Near-Miss #6 WK-Batter; 1,643 balls, PP SR 178.4; top keeper target).  │
│    • Mohsin Khan (LSG Indian left-arm strike pacer; high-value trade target).          │
│    • Jamie Overton (CSK pace-bowling all-rounder; 145 kph enforcer / #8 batter).       │
│    • Naman Dhir & Shashank Singh (Contingent domestic middle-order finishers).         │
└────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## 4. COMPLETE SUBMISSION DELIVERABLES DOSSIER

All files in `outputs/submission/` are synchronized, mathematically verified, and formatted to the highest professional franchise standard:

| File Name | Format | Primary Contents & Strategic Function |
|:---|:---:|:---|
| [SupeRR_Selector_Round1_Methodology_Report.pdf](file:///c:/Users/LENOVO/OneDrive/Desktop/SupeRR-Selector-Season-2/outputs/submission/SupeRR_Selector_Round1_Methodology_Report.pdf) | PDF (21 Pages) | **Primary Competition Deliverable:** Complete methodology report featuring executive summary, Phase 0.5 audit findings, mathematical architecture, batting/bowling analyses, statistical reliability, sensitivity suite, RR 2026 squad audit, Sai Kishore case study, scouting cards, and all 12 de-overlapped charts. |
| [final_batting_rankings.csv](file:///c:/Users/LENOVO/OneDrive/Desktop/SupeRR-Selector-Season-2/outputs/submission/final_batting_rankings.csv) | CSV | Complete statistical ranking and profile features for all 99 eligible batters. |
| [final_bowling_rankings.csv](file:///c:/Users/LENOVO/OneDrive/Desktop/SupeRR-Selector-Season-2/outputs/submission/final_bowling_rankings.csv) | CSV | Complete statistical ranking and profile features for all 128 eligible bowlers. |
| [AUCTION_TARGET_DECISION_MATRIX.csv](file:///c:/Users/LENOVO/OneDrive/Desktop/SupeRR-Selector-Season-2/outputs/submission/AUCTION_TARGET_DECISION_MATRIX.csv) | CSV | Comprehensive 10-dimension franchise decision matrix evaluating all 20 canonical players and key near-miss contenders across 4 actionability tiers. |
| [RR_SQUAD_FIT_ANALYSIS.md](file:///c:/Users/LENOVO/OneDrive/Desktop/SupeRR-Selector-Season-2/outputs/submission/RR_SQUAD_FIT_ANALYSIS.md) | Markdown | 27-player RR 2026 roster audit, departmental depth/deficit breakdowns, Sai Kishore complementary case study, and 5 structured scouting cards. |
| [RANKING_INTERPRETATION_AND_SCOPE.md](file:///c:/Users/LENOVO/OneDrive/Desktop/SupeRR-Selector-Season-2/outputs/submission/RANKING_INTERPRETATION_AND_SCOPE.md) | Markdown | Governance analysis of the competition problem statement, uncapped player scope reconciliation, Uncapped Indian Contingency Rankings, and dual-list framework. |
| [source_register.md](file:///c:/Users/LENOVO/OneDrive/Desktop/SupeRR-Selector-Season-2/outputs/submission/source_register.md) | Markdown | 52 verified external cricket research records with full URLs, publication dates, and evidence classifications (`Official` or `Reputable Media`). |
| [user_review_required.md](file:///c:/Users/LENOVO/OneDrive/Desktop/SupeRR-Selector-Season-2/outputs/submission/user_review_required.md) | Markdown | Pre-submission human review checklist and dropdown transliteration reference. |
| [FINAL_QUALITY_AUDIT.md](file:///c:/Users/LENOVO/OneDrive/Desktop/SupeRR-Selector-Season-2/outputs/submission/FINAL_QUALITY_AUDIT.md) | Markdown | Forensic independent audit certifying 100% numerical parity, zero look-ahead leakage, and verified submission readiness. |

---

## 5. FINAL INSTRUCTIONS FOR THE USER (PORTAL SUBMISSION)

When ready to submit on Unstop:
1. **Open the Unstop Competition Portal** for *SupeRR Selector Season 2 (Round 1)*.
2. **Determine the Live Form Interface:**
   - **Scenario A (Dropdown Menus Present):** Enter the 20 Canonical Leaders in Section 2 above into the respective dropdown fields. If the form specifically restricts options to uncapped domestic players, select from the Uncapped Indian Contingency Rankings in [RANKING_INTERPRETATION_AND_SCOPE.md](file:///c:/Users/LENOVO/OneDrive/Desktop/SupeRR-Selector-Season-2/outputs/submission/RANKING_INTERPRETATION_AND_SCOPE.md) (Shashank Singh #1, Ashutosh Sharma #2, Ayush Badoni #3 / Mohsin Khan #1, Yash Dayal #2, Rasikh Salam #3). Note transliterations: `Sai Kishore` may appear as `Ravisrinivasan Sai Kishore`; `Sufiyan Muqeem` as `Sufyan Moqim`.
   - **Scenario B (Document Upload Only):** If the portal features a file-upload interface only (e.g., single PDF/deck upload as per the public overview), upload [SupeRR_Selector_Round1_Methodology_Report.pdf](file:///c:/Users/LENOVO/OneDrive/Desktop/SupeRR-Selector-Season-2/outputs/submission/SupeRR_Selector_Round1_Methodology_Report.pdf). All 20 canonical selections, actionable targets, and uncapped contingency rankings are comprehensively presented inside the report.
3. **Attach Supplementary Files / Links:** If additional attachment or text/URL fields exist, provide links or files for `final_batting_rankings.csv`, `final_bowling_rankings.csv`, `AUCTION_TARGET_DECISION_MATRIX.csv`, and `RR_SQUAD_FIT_ANALYSIS.md`.
4. **Final Review & Submission:** Review all inputs and click **Submit**.

