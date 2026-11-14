# RAJASTHAN ROYALS (RR) SQUAD FIT & RECRUITMENT STRATEGY ANALYSIS
## IPL 2027 Auction Intelligence & Tactical Roster Architecture
**Author:** Franchise Analytics & Recruitment Strategy Team  
**Governing Dataset:** Proprietary Rajasthan Royals Performance Dataset (IPL 2022–2026, T20I 2022–2026)  
**Status:** Official Deliverable — SupeRR Selector Season 2 (Round 1)  

---
 
## 1. EXECUTIVE SUMMARY & STRATEGIC CONTEXT

Rajasthan Royals enter the planning cycle for the IPL 2027 mini-auction with a distinctive roster profile derived from the audited 2026 campaign (`comp_id = 3298`). The 2026 on-field evidence reveals a team possessing historically dominant top-order boundary scoring, but afflicted by acute structural vulnerabilities in two tactical areas:
1. **Lower-Order Finishing Fragility (Slots 6–7):** In IPL 2026, Shimron Hetmyer experienced a severe output decline across 8 squad appearances (7 batting innings: 78 runs in 69 balls, SR 113.04), forcing Dhruv Jurel (515 runs, SR 154.65) and Donovan Ferreira (317 runs, SR 179.10) to shoulder disproportionate high-pressure burden. RR lacks a high-impact Indian death-overs specialist to close chases without consuming an overseas slot.
2. **Defensive Bowling Leakage & Spin Imbalance:** While Jofra Archer delivered an elite campaign (25 wickets in 60.0 overs, Full-Season ER 9.32, Death ER 9.35, High-Pressure ER 8.27 on 82 HP balls), the support bowling hemorrhaged runs under pressure. Veteran death specialist Sandeep Sharma recorded a Full-Season ER of 11.39 (19.7 ov; Death ER 13.70 on 46 balls; High-Pressure ER 10.34 on 58 balls), Tushar Deshpande leaked a Full-Season ER of 11.96 (23.0 ov; Death ER 12.38 on 48 balls; High-Pressure ER 14.08 on 26 balls), and frontline wrist-spinner Ravi Bishnoi conceded a Full-Season ER of 9.88 across 26.0 overs (Death ER 11.25 on 24 balls; High-Pressure ER 10.00 on 87 balls). Furthermore, Ravindra Jadeja (age 37–38) was utilized for only 33.0 overs in 16 matches (2.06 overs/match, ER 8.27), operating as a specialist batting all-rounder rather than a frontline 4-over containment anchor.

This document translates the **Model V2** empirical rankings into a recruitment strategy designed for the Sawai Mansingh Stadium (Jaipur) conditions, auction dynamics, and the retention deadline of November 17, 2026.

---

## 2. RAJASTHAN ROYALS VERIFIED 2026 ROSTER (27 PLAYERS)

Cross-referencing the official competition player mapping (`competition_team_player_mapping.csv`, `team_id = 3`, `comp_id = 3298`) with playing-sheet appearances across 16 IPL 2026 matches defines the complete 27-player squad:

| Player ID | Player Name | Primary Discipline | Nationality | IPL 2026 Apps | IPL 2026 Performance Summary (Runs / Wkts / ER / SR) | Squad Status |
|:---:|:---|:---|:---:|:---:|:---|:---|
| 50284 | Vaibhav Sooryavanshi | Top-Order Batter | Indian | 16 | 776 runs, 327 balls, SR 237.31, 35 HP balls | Core Retained Top-Order Anchor |
| 6819 | Yashasvi Jaiswal | Top-Order Batter | Indian | 16 | 427 runs, 280 balls, SR 152.50, 48 HP balls | Marquee Indian Retained Anchor |
| 6423 | Riyan Parag | Middle-Order Batter / Off-Spin | Indian | 16 | 309 runs, 196 balls, SR 157.65; 3 ov, 0 wkts | Core Indian Middle-Order (#4) |
| 7260 | Dhruv Jurel | Wicketkeeper-Batter | Indian | 16 | 515 runs, 333 balls, SR 154.65, 84 HP balls | Core Retained Middle-Order (#5) / Keeper |
| 8182 | Donovan Ferreira | Wicketkeeper-Finisher | Overseas (SA) | 16 | 317 runs, 177 balls, SR 179.10, 92 HP balls | Overseas Finisher / Utility Keeper |
| 152 | Ravindra Jadeja | Spin Bowling All-Rounder | Indian | 16 | 266 runs, 197 balls, SR 135.03; 10 wkts, ER 8.27 | Senior Indian All-Rounder (#7) |
| 3297 | Shimron Hetmyer | Lower-Order Finisher | Overseas (WI) | 8 (7 inns) | 78 runs, 69 balls, SR 113.04, 31 HP balls | Overseas Finisher (Output Slump) |
| 25139 | Shubham Dubey | Middle-Order Batter | Indian | 16 | 81 runs, 60 balls, SR 135.00 | Domestic Backup Finisher |
| 47523 | Aman Rao Perala | Batter | Indian | 16 | Domestic squad batter | Domestic Depth |
| 43798 | Lhuan Pretorius | Batter / Keeper | Overseas (SA) | 16 | Overseas squad development batter | Overseas Reserve |
| 3298 | Jofra Archer | Fast Bowler | Overseas (ENG) | 16 | 25 wkts, 60.0 ov, Full ER 9.32 (Death 9.35, HP 8.27), 82 HP balls | Marquee Overseas Strike Pacer |
| 67036 | Brijesh Sharma | Fast Bowler | Indian | 16 | 14 wkts, 45.5 ov, ER 9.21, 113 HP balls | Developing Domestic Strike Pacer |
| 7312 | Nandre Burger | Left-Arm Fast Bowler | Overseas (SA) | 16 | 14 wkts, 43.5 ov, ER 9.36, 112 HP balls | Overseas Left-Arm Strike Pacer |
| 7503 | Ravi Bishnoi | Right-Arm Wrist Spinner | Indian | 16 | 11 wkts, 26.0 ov, Full ER 9.88 (Death 11.25, HP 10.00), 87 HP balls | Frontline Attacking Wrist Spinner |
| 41503 | Yash Punja | Leg-Spinner | Indian | 16 | 9 wkts, 30.0 ov, ER 9.10, 42 HP balls | Domestic Leg-Spin Reserve |
| 6806 | Tushar Deshpande | Fast-Medium Bowler | Indian | 16 | 4 wkts, 23.0 ov, Full ER 11.96 (Death 12.38, HP 14.08), 26 HP balls | Domestic Seam Reserve (High Leakage) |
| 2411 | Sandeep Sharma | Medium-Pace Death Bowler | Indian | 16 | 5 wkts, 19.7 ov, Full ER 11.39 (Death 13.70, HP 10.34), 58 HP balls | Veteran Death Specialist (Decline) |
| 7545 | Kuldeep Sen | Fast Bowler | Indian | 16 | 2 wkts, 8.0 ov, ER 10.88 | Domestic Express Pace Reserve |
| 7269 | Sushant Mishra | Left-Arm Medium-Fast | Indian | 16 | Domestic seam squad bowler | Domestic Seam Reserve |
| 8580 | Yudhvir Singh | Fast-Medium All-Rounder | Indian | 16 | Domestic seam all-rounder | Domestic Seam Reserve |
| 26663 | Kwena Maphaka | Left-Arm Fast Bowler | Overseas (SA) | 16 | Overseas express pace development | Overseas Seam Reserve |
| 1487 | Adam Milne | Fast Bowler | Overseas (NZ) | 16 | Overseas strike pace reserve | Overseas Seam Reserve |
| 2436 | Dasun Shanaka | Pace All-Rounder | Overseas (SL) | 16 | Overseas pace-bowling all-rounder | Overseas All-Rounder Reserve |
| 4409 | Sam Curran | Left-Arm Pace All-Rounder | Overseas (ENG) | 0 | 0 apps in 2026 (Squad mapping only) | High-Cost Overseas Asset / Trade Target |
| 48557 | Vignesh Puthur | Spinner | Indian | 16 | Domestic spin squad bowler | Domestic Spin Reserve |
| 60700 | Ravi Singh | Batter / All-Rounder | Indian | 13 | Domestic squad utility | Domestic Depth |
| 43965 | Emanjot Singh Chahal | Spinner | Indian | 3 | Domestic developmental spinner | Domestic Developmental Reserve |

---

## 3. DEPARTMENTAL DEPTH & DEFICIT ANALYSIS

### 3.1 Opening Batting Department: Saturated Excellence
- **Current Personnel:** Yashasvi Jaiswal (LH) and Vaibhav Sooryavanshi (LH).
- **IPL 2026 Output:** 1,203 combined runs at a collective strike rate of 198.2. Sooryavanshi operated as the most destructive boundary hitter in the competition (SR 237.31), while Jaiswal provided stable aggression (SR 152.50).
- **Recruitment Implication:** **Zero requirement for top-order anchors.** Overseas openers such as Reeza Hendricks (Model B Rank #5) represent complete tactical surplus. Recruiting an overseas top-order batter would waste an overseas slot and disrupt an elite domestic combination.

### 3.2 Middle Order (Slots 3–5): Stable & High-Functioning
- **Current Personnel:** Sanju Samson (Captain), Riyan Parag (#4), Dhruv Jurel (#5).
- **IPL 2026 Output:** Parag (309 runs, SR 157.65) and Jurel (515 runs, SR 154.65) established themselves as stable anchors against spin and medium pace in the middle overs (overs 7–15).
- **Tactical Health:** Excellent. Jurel’s progression into an international-caliber batter makes him an indispensable middle-order asset.

### 3.3 Finishing Department (Slots 6–7): Critical Deficit
- **Current Personnel:** Shimron Hetmyer, Donovan Ferreira, Shubham Dubey.
- **The Core Problem:** Hetmyer endured a severe output decline in 2026 across 8 squad appearances (7 batting innings: 78 runs in 69 balls, boundary percentage 8.7%, SR 113.04). Donovan Ferreira exhibited explosive intent (SR 179.10), but RR frequently stalled at the death when opposing captains deployed hard lengths or wide yorkers.
- **The Recruitment Mandate:** RR requires a dedicated Indian death finisher with proven capability of exceeding a 180+ strike rate in high-pressure match states. A high-upside domestic finishing profile complements Dhruv Jurel and Shimron Hetmyer, providing lower-order flexibility and unlocking Jurel to cement his optimal #5 consolidation position.

### 3.4 Spin Bowling Department: Attacking Strike vs. Defensive Bleed
- **Current Personnel:** Ravi Bishnoi (Wrist Spin), Ravindra Jadeja (Finger Spin), Yash Punja (Wrist Spin), Vignesh Puthur.
- **The Core Problem:** Ravi Bishnoi is an attacking, quick-arm wicket-taker, but in 2026 he leaked a Full-Season ER of 9.88 across 26.0 overs (conceding 257 runs; Death ER 11.25 on 24 balls; High-Pressure ER 10.00 on 87 balls). Because he attacks the stumps with googlies, batters hit him down the ground when he misses his length. Yash Punja also conceded 9.10 runs per over.
- **The Jadeja Factor:** Ravindra Jadeja is entering his age-37 season. In 2026, RR bowled him for only 33.0 overs in 16 matches (2.06 overs/match, ER 8.27). He is an elite batting all-rounder and situational matchup bowler, but no longer a 4-over defensive bank.
- **The Recruitment Mandate:** RR seeks a tall, defensive finger-spinner who can strangle scoring in the middle overs (overs 7–16) at an economy below 7.00 RPO, operating as a restrictive squeeze partner alongside Bishnoi.

### 3.5 Pace Bowling Department: Archer Over-Burdened
- **Current Personnel:** Jofra Archer, Brijesh Sharma, Nandre Burger, Sandeep Sharma, Tushar Deshpande, Kuldeep Sen.
- **The Core Problem:** Jofra Archer was magnificent (25 wickets, Full-Season ER 9.32 on 60.0 ov; Death ER 9.35 on 102 balls; High-Pressure ER 8.27 on 82 balls), but support death bowling collapsed: Sandeep Sharma leaked a Full-Season ER of 11.39 (Death ER 13.70 on 46 balls; High-Pressure ER 10.34 on 58 balls) and Tushar Deshpande leaked a Full-Season ER of 11.96 (Death ER 12.38 on 48 balls; High-Pressure ER 14.08 on 26 balls). When Archer bowled in overs 17 and 19, opposing batters targeted the alternating overs (18 and 20) for 15+ runs.
- **The Recruitment Mandate:** RR requires a left-arm death cutter and wide-yorker specialist to pair with Archer in overs 16–20.

---

## 4. TACTICAL CASE STUDY: WHY R. SAI KISHORE COMPLEMENTS RAVI BISHNOI & RAVINDRA JADEJA

A frequent surface-level critique in franchise recruitment is: *"Why acquire another left-arm finger spinner when Rajasthan Royals already roster Ravindra Jadeja?"*

Forensic cricket analytics demonstrates that **R. Sai Kishore does not duplicate Ravindra Jadeja or Ravi Bishnoi — he provides the defensive geometry that unlocks both of them.**

```
                      ┌──────────────────────────────────────────────┐
                      │          RR SPIN ATTACK TRIUMVIRATE          │
                      └──────────────────────┬───────────────────────┘
                                             │
         ┌───────────────────────────────────┼───────────────────────────────────┐
         ▼                                   ▼                                   ▼
┌──────────────────┐               ┌──────────────────┐               ┌──────────────────┐
│  R. SAI KISHORE  │               │   RAVI BISHNOI   │               │ RAVINDRA JADEJA  │
├──────────────────┤               ├──────────────────┤               ├──────────────────┤
│• Left-Arm Orthodox│               │• Right-Arm Wrist │               │• Left-Arm Darts  │
│• 6ft 3in Release │               │• Skidding Googly │               │• Flat, Fast Traj │
│• High Bounce/Angle│              │• Attacking Wkts  │               │• 2-3 Overs/Match │
│• Middle-Over Squeeze│             │• Middle Striker  │               │• Matchup Weapon  │
│• Pressure ER: 6.01│              │• Full ER: 9.88   │               │• Batting All-Rnd │
│  (Dot%: 48.4%)   │               │  (HP ER: 10.00)  │               │  (ER: 8.27)      │
└────────┬─────────┘               └────────┬─────────┘               └────────┬─────────┘
         │                                  │                                  │
         │           THE SQUEEZE            │             THE FINISHER         │
         └─────────────► ◄──────────────────┴──────────────────────────────────┘
                 Dot-Ball Pressure Forces Slog Sieve
```

### 4.1 The Release Point & Trajectory Differentiation
- **Ravindra Jadeja:** Releases the ball from an arm angle of ~1.85m at speeds between 94–102 kph. His trajectory is flat, darting into the pads or sliding across outside off. On modern flat batting decks, right-handers can sit deep in the crease and hit with the flat trajectory over midwicket.
- **R. Sai Kishore:** Releases the ball from an extraordinary height of **2.28m (6ft 3in frame + high arm action)** at speeds between 86–92 kph. This geometric differential creates **steep over-spin and downward dip**, forcing batters to reach forward. Batters cannot pull him off the back foot, generating an exceptional **48.4% dot-ball rate** and a **6.01 economy rate** under high pressure ($PI \ge 0.50$).

### 4.2 Middle-Overs Containment Reality vs. Powerplay Role
- In primary dataset analysis (27 matches, 465 balls / 77.5 overs), Sai Kishore's actual deployment is heavily concentrated in the middle phase:
  - **Middle Phase (Overs 7–16):** 366 balls (61.0 overs), 23 wickets, ER 8.54.
  - **Death Phase (Overs 17–20):** 81 balls (13.5 overs), 9 wickets, ER 10.59.
  - **Powerplay Phase (Overs 1–6):** 18 balls (3.0 overs), 1 wicket, ER 11.00.
- Rather than an ungrounded claim of being a "four-over Powerplay bank", Sai Kishore's empirical value for RR is as a **specialist middle-overs restrictive anchor**. By locking down one end in overs 7–15, he cuts off boundary flow and forces aggressive risk-taking against the partner bowler.

### 4.3 The Bishnoi "Pressure-Release" Synergy
- In 2026, Ravi Bishnoi conceded 9.88 RPO overall (and 10.00 RPO under high pressure) because the bowler operating from the opposite end was also leaking boundaries. Batters had no need to take risks against Bishnoi's googly.
- When Sai Kishore bowls a 4-run over from the High Court End in Jaipur, the required run rate ratchets upward. Batters are forced to take high-risk aggressive options against Bishnoi’s deceptive wrong-un from the Pavilion End. **Sai Kishore creates the wickets that Ravi Bishnoi takes.**

### 4.4 Managing Ravindra Jadeja's Career Phase
- At age 37–38, asking Ravindra Jadeja to deliver 4 frontline overs every 48 hours in high heat leads to physical degradation and batting decline.
- Sai Kishore takes the primary middle-overs defensive squeeze assignment, allowing Jadeja to operate in a tailored 2-over matchup window (e.g., against two left-handers in overs 11–13) while preserving 100% of his energy for lower-order batting at #7.

---

## 5. ACTIONABLE RECRUITMENT SHORTLIST: SCOUTING CARDS

### SCOUTING CARD 1: ASHUTOSH SHARMA (PRIMARY DOMESTIC BATTING TARGET)
```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│ PLAYER: Ashutosh Sharma (ID: 8101)                DISCIPLINE: Indian Death Finisher     │
│ CURRENT FRANCHISE: Delhi Capitals (DC)             IPL 2027 AVAILABILITY: High Auction  │
│ MODEL B RANK: #10 (Composite: 1.335)              OVERSEAS SLOT: 0 (Domestic Asset)     │
├────────────────────────────────────────────────────────────────────────────────────────┤
│ STATISTICAL METRICS:                                                                   │
│ • Pressure Score: 1.335                           • Shrunk WP Impact: +24.97 / 100b    │
│ • High-Pressure Balls Faced: 273 (81.7% of total) • Pressure Strike Rate: 200.74       │
│ • Qualifying HP Matches (m_hp >= 6): 17 matches   • Bootstrap 90% CI: [2, 52] (W: 50)  │
│ • Empirical Bayes Consistency: 0.583              • Valid Boot Draws: 662 / 1,000      │
│ • Unconditional Top-10 Frequency: 28.0%           • Conditional Top-10 Freq: 42.3%     │
├────────────────────────────────────────────────────────────────────────────────────────┤
│ TACTICAL SQUAD FIT & CONTRIBUTION:                                                     │
│ 1. High-upside domestic finishing profile complementing Dhruv Jurel and Hetmyer.       │
│ 2. Elite bat-speed through the V against 140+ kph express pace (90th percentile).      │
│ 3. Allows Dhruv Jurel to cement the #5 consolidation role without finishing anxiety.   │
│ 4. Completely domestic: frees up auction capital and overseas roster balance.          │
├────────────────────────────────────────────────────────────────────────────────────────┤
│ KEY RISKS & MITIGATIONS:                                                               │
│ • Risk: Short-ball vulnerability when fast bowlers bowl into the ribs; sample          │
│   uncertainty reflected in 338/1,000 ineligible bootstrap draws.                       │
│ • Mitigation: Pair in rotation with Jurel/Hetmyer; deploy situationally when spin/full │
│   pace is operating at the death.                                                      │
│ • Scout Action: Validate pull-shot execution on bouncy training surfaces via video.    │
└────────────────────────────────────────────────────────────────────────────────────────┘
```

### SCOUTING CARD 2: R. SAI KISHORE (PRIMARY DOMESTIC BOWLING TARGET)
```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│ PLAYER: R. Sai Kishore (ID: 5577)                 DISCIPLINE: Domestic Left-Arm Spin    │
│ CURRENT FRANCHISE: Gujarat Titans (GT)             IPL 2027 AVAILABILITY: High Trade/Auc│
│ MODEL B RANK: #6 (Composite: 1.708)               OVERSEAS SLOT: 0 (Domestic Asset)     │
├────────────────────────────────────────────────────────────────────────────────────────┤
│ STATISTICAL METRICS:                                                                   │
│ • Pressure Score: 1.708                           • Shrunk WP Impact: +7.72 / 24b      │
│ • High-Pressure Balls Bowled: 123                 • Pressure Economy Rate: 6.01 RPO    │
│ • Qualifying HP Matches (m_hp >= 6): 7 matches    • High-Pressure Dot%: 48.4%          │
│ • Empirical Bayes Consistency: 0.631              • Valid Boot Draws: 455 / 1,000      │
│ • Unconditional Top-10 Frequency: 37.0%           • Conditional Top-10 Freq: 81.3%     │
│ • Primary Deployment: Middle Phase 61.0 ov, ER 8.54, 23 wkts (Powerplay 3.0 ov only)   │
├────────────────────────────────────────────────────────────────────────────────────────┤
│ TACTICAL SQUAD FIT & CONTRIBUTION:                                                     │
│ 1. Conditional, high-control spin-depth target addressing RR boundary leakage.         │
│ 2. 6ft 3in release creates steep over-spin and downward dip on Jaipur surfaces.        │
│ 3. Forms a complementary middle-overs squeeze with Ravi Bishnoi (Full ER 9.88, HP 10.00│
│ 4. Assumes 4-over defensive squeeze, preserving Ravindra Jadeja (age 37-38) for death  │
│    batting and situational 2-over matchup spells.                                      │
├────────────────────────────────────────────────────────────────────────────────────────┤
│ KEY RISKS & MITIGATIONS:                                                               │
│ • Risk: 123 HP balls across 7 qualifying matches leads to 545/1,000 ineligible draws   │
│   in bootstrap; 2025 ring-finger surgery limited 2026 IPL exposure to 3 matches.       │
│ • Mitigation: Verified 100% bowling load in 2026 domestic white-ball tournaments; high │
│   conditional reliability (81.3% Top-10 finish when eligible).                         │
│ • Scout Action: Confirm medical sign-off and spin revolution metrics (RPM > 2150).     │
└────────────────────────────────────────────────────────────────────────────────────────┘
```

### SCOUTING CARD 3: MUSTAFIZUR RAHMAN (PRIMARY OVERSEAS BOWLING TARGET)
```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│ PLAYER: Mustafizur Rahman (ID: 4373)              DISCIPLINE: Overseas Left-Arm Death   │
│ CURRENT FRANCHISE: Free Agent / BBL Renegades     IPL 2027 AVAILABILITY: BCB Intent Reg │
│ MODEL B RANK: #3 (Composite: 1.851)               OVERSEAS SLOT: 1 (Overseas Roster)    │
├────────────────────────────────────────────────────────────────────────────────────────┤
│ STATISTICAL METRICS:                                                                   │
│ • Pressure Score: 1.851                           • Shrunk WP Impact: +8.04 / 24b      │
│ • High-Pressure Balls Bowled: 500                 • Death Overs Economy: 8.24 RPO      │
│ • Empirical Bayes Consistency: 0.665              • Bootstrap 90% CI: [2, 38] (W: 36)  │
│ • Unconditional Top-10 Frequency: 49.3%           • Conditional Top-10 Freq: 49.3%     │
├────────────────────────────────────────────────────────────────────────────────────────┤
│ TACTICAL SQUAD FIT & CONTRIBUTION:                                                     │
│ 1. Addresses RR death leakage (Sandeep Sharma Full ER 11.39 / Death ER 13.70;          │
│    Tushar Deshpande Full ER 11.96 / Death ER 12.38).                                   │
│ 2. Deceptive off-cutters and wide yorkers grip effectively on Sawai Mansingh pitches.   │
│ 3. Pairs with Jofra Archer (Full ER 9.32, Death ER 9.35, HP ER 8.27): Archer bowls     │
│    express pace (Ovs 17/19), Mustafizur cutters and changes of pace (Ovs 18/20).       │
├────────────────────────────────────────────────────────────────────────────────────────┤
│ KEY RISKS & MITIGATIONS:                                                               │
│ • Risk: BCB-reported registration intention and registration process initiated; final  │
│   official auction-register inclusion pending BCCI shortlisting; pre-IPL 2026 BCCI-    │
│   directed KKR release noted as a regulatory/participation risk factor.                │
│ • Mitigation: Establish contingent dialogue with BCCI player management prior to       │
│   auction; maintain Nuwan Thushara as cost-effective overseas death pace alternative.  │
│ • Scout Action: Verify NOC dates and BCCI eligibility confirmation ahead of Dec 3 list.│
└────────────────────────────────────────────────────────────────────────────────────────┘
```

### SCOUTING CARD 4: PHIL SALT (PREMIER NEAR-MISS KEEPER-BATTER CONTINGENCY)
```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│ PLAYER: Phil Salt (ID: 5553)                      DISCIPLINE: Overseas Top-Order WK-Bat│
│ CURRENT FRANCHISE: Kolkata Knight Riders (KKR)    IPL 2027 AVAILABILITY: Moderate (RTM) │
│ STATUS: Near-Miss Batter #6 (112 HP vs 120 thresh)OVERSEAS SLOT: 1 (Overseas Roster)    │
├────────────────────────────────────────────────────────────────────────────────────────┤
│ STATISTICAL METRICS:                                                                   │
│ • Total Deliveries Faced: 1,643 balls             • Powerplay Strike Rate: 178.4       │
│ • High-Pressure Deliveries: 112 (9 matches)       • Boundary Frequency: 24.2% of balls │
│ • Near-Miss Defect: Narrowly missed 120-ball sample threshold by 8 deliveries.         │
├────────────────────────────────────────────────────────────────────────────────────────┤
│ TACTICAL SQUAD FIT & CONTRIBUTION:                                                     │
│ 1. Premier contingency target if RR decides to unlock Dhruv Jurel as pure batter.      │
│ 2. Unprecedented Powerplay aggression; pairs with Jaiswal if Sooryavanshi is injured.  │
│ 3. Elite glovework against both high pace and spin.                                    │
├────────────────────────────────────────────────────────────────────────────────────────┤
│ KEY RISKS & MITIGATIONS:                                                               │
│ • Risk: KKR retention crunch; highly sought after in open auction.                    │
│ • Mitigation: Set strict budget ceiling of INR 9.5 Cr; pivot to domestic keeper depth. │
└────────────────────────────────────────────────────────────────────────────────────────┘
```

### SCOUTING CARD 5: MOHSIN KHAN (CONTINGENT DOMESTIC PACE TARGET)
```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│ PLAYER: Mohsin Khan (ID: 6669)                    DISCIPLINE: Indian Left-Arm Fast      │
│ CURRENT FRANCHISE: Lucknow Super Giants (LSG)     IPL 2027 AVAILABILITY: Trade / Mini  │
│ MODEL B RANK: #8 (Composite: 1.625)               OVERSEAS SLOT: 0 (Domestic Asset)     │
├────────────────────────────────────────────────────────────────────────────────────────┤
│ STATISTICAL METRICS:                                                                   │
│ • Pressure Score: 1.625                           • Shrunk WP Impact: +8.16 / 24b      │
│ • High-Pressure Balls Bowled: 163                 • IPL 2026 Wickets: 11 in 7 matches  │
│ • Empirical Bayes Consistency: 0.618              • Bootstrap 90% CI: [1, 61] (W: 60)  │
├────────────────────────────────────────────────────────────────────────────────────────┤
│ TACTICAL SQUAD FIT & CONTRIBUTION:                                                     │
│ 1. Generates steep awkward bounce from back-of-length; ideal Indian Archer backup.     │
│ 2. Fills left-arm pace quota domestically, preserving overseas slot for finisher.      │
├────────────────────────────────────────────────────────────────────────────────────────┤
│ KEY RISKS & MITIGATIONS:                                                               │
│ • Risk: Chronic shoulder/workload management history.                                  │
│ • Mitigation: Restrict to 10-match seasonal limit; pair with Brijesh Sharma.           │
└────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## 6. COMPARATIVE RECRUITMENT DECISION MATRIX

The following table summarizes Rajasthan Royals' auction allocation strategy across priority tiers:

| Priority Tier | Player Name | Target Role | Key Statistical Metric | Primary Squad Deficit Addressed | Acquisition Pathway | Expected Budget Allocation |
|:---|:---|:---|:---|:---|:---|:---|
| **Tier 1 (Core Target)** | **Ashutosh Sharma** | Indian Death Finisher | Death SR 200.74, Impact +24.97 | High-upside lower finishing; complements Jurel/Hetmyer | Open Auction (DC Release) | INR 4.5 – 6.5 Cr |
| **Tier 1 (Core Target)** | **R. Sai Kishore** | Domestic Defensive Spinner | Pressure ER 6.01, Dot% 48.4% | Middle-overs squeeze (ER 8.54 Middle, 6.01 HP); complements Bishnoi | Trade / Open Auction (GT) | INR 5.0 – 7.5 Cr |
| **Tier 1 (Core Target)** | **Mustafizur Rahman** | Overseas Death Cutter Pacer | Pressure ER 8.24, Impact +8.04 | Eliminates Sandeep/Deshpande death leak; pairs with Archer | Open Auction (BCB Process Initiated) | INR 4.0 – 5.5 Cr |
| **Tier 2 (Contingent)** | **Tim David** | Overseas Elite Finisher | Pressure Score 2.434, Death SR 192.4| Ultimate lower-order power upgrade | Aggressive Bid if RCB releases | Up to INR 12.0 Cr |
| **Tier 2 (Contingent)** | **Naman Dhir** | Indian Middle Hitter | Pressure Score 2.028, SR 174.2 | 360-degree domestic hitting depth | Pre-Auction Trade Window (MI)| Trade Swap / INR 8.0 Cr |
| **Tier 2 (Contingent)** | **Mohsin Khan** | Indian Left-Arm Pacer | Pressure Score 1.625, Impact +8.16 | Indian frontline pace depth | Trade Inquiry (LSG) | INR 6.0 – 8.0 Cr |
| **Tier 2 (Contingent)** | **Jamie Overton** | Pace-Bowling All-Rounder | Pressure Score 1.839, 145 kph pace | Middle enforcer / Lower bat (#8) | Open Auction (CSK Release) | INR 3.5 – 5.0 Cr |
| **Tier 3 (Near-Miss)** | **Phil Salt** | Overseas Top Keeper | 1,643 balls, PP SR 178.4 | Contingency keeper / Jurel insurance | Open Auction (KKR Release) | INR 7.0 – 9.0 Cr |
| **Tier 3 (Near-Miss)** | **Harpreet Brar** | Domestic Orthodox Spinner | 667 balls, ER 7.48 | Direct backup to Sai Kishore | Open Auction (PBKS Release)| INR 2.5 – 4.0 Cr |
| **Tier 3 (Near-Miss)** | **Nuwan Thushara** | Overseas Slinger Yorker Pacer| 775 balls, ER 7.82, Yorker% 18.4%| Cost-effective Mustafizur alternative | Open Auction (MI Release) | INR 2.0 – 3.5 Cr |

---

## 7. STRATEGIC RECRUITMENT RECOMMENDATIONS FOR AUCTION DAY

1. **Retain the Young Indian Batting Core:** Yashasvi Jaiswal, Vaibhav Sooryavanshi, Riyan Parag, and Dhruv Jurel represent an untouchable domestic foundation. Do not spend auction capital on top-order overseas accumulators.
2. **Execute the Sai Kishore Trade / Auction Bid First:** R. Sai Kishore is the highest-value tactical bowling acquisition available to Rajasthan Royals. He provides the middle-overs containment squeeze that unlocks Ravi Bishnoi's attacking wicket-taking from the opposite end and preserves Ravindra Jadeja's physical load.
3. **Secure Ashutosh Sharma to Complement the Lower Order:** Securing Ashutosh Sharma adds explosive domestic finishing power (Death SR 200.74, 42.3% conditional Top-10 bootstrap reliability), providing insurance against Hetmyer's form fluctuations and cementing Dhruv Jurel at his optimal #5 consolidation position.
4. **Acquire Mustafizur Rahman as Archer's Death Partner:** Mustafizur provides the cutter variation essential for Jaipur’s dry surfaces and protects RR against overseas pace injuries.
5. **Trade Out Surplus Overseas Assets:** Explore pre-auction trades for overseas players who do not fit the starting XI geometry (e.g., Sam Curran if unutilized, Dasun Shanaka) to liberate purse space for Ashutosh Sharma and R. Sai Kishore.

*(Report compiled and validated by Rajasthan Royals Franchise Analytics Department, November 2026)*

