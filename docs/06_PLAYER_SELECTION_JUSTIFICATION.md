# 06 — Canonical Player Selection Justification & Practical Context

All statistical rankings below derive strictly from **Model B (Maintenance & Lift)** over the `837`-match (`193,988`-delivery) 2022–2026 IPL + T20I dataset ([final_top10_batters.csv](file:///c:/Users/LENOVO/OneDrive/Desktop/SupeRR-Selector-Season-2/outputs/model_v2/final_top10_batters.csv), [final_top10_bowlers.csv](file:///c:/Users/LENOVO/OneDrive/Desktop/SupeRR-Selector-Season-2/outputs/model_v2/final_top10_bowlers.csv)). Practical IPL 2027 availability and Rajasthan Royals squad-fit notes are kept **strictly separate** in §5 ([auction_feasibility.csv](file:///c:/Users/LENOVO/OneDrive/Desktop/SupeRR-Selector-Season-2/outputs/model_v2/auction_feasibility.csv), [source_register.md](file:///c:/Users/LENOVO/OneDrive/Desktop/SupeRR-Selector-Season-2/outputs/submission/source_register.md)).

---

## 1. Canonical Top 10 Batters Under Pressure

| Rank | ID | Player Name | Primary Role | `N_tot` | `N_hp` | `N_eff` | Shrunk WP Impact | Shrunk Norm Impact | Maint Lift | EB Cons (Raw) | Pressure Score | Boot Med (p05–p95) | Top-10 Freq |
|---:|---:|---|---|---:|---:|---:|---:|---:|---:|---|---|---:|---:|---:|
| **1** | `6396` | **Tim David** | Finisher 6+ | 1,226 | 570 | 744.3 | +41.75 | +38.49 | +28.28 | 63.0% (74.2%) | **+2.434** | 3.0 (1.0–16.0) | 89.3% |
| **2** | `796` | **Matthew Wade** | Finisher 6+ | 427 | 158 | 254.9 | +33.20 | -1.27 | +33.64 | 63.5% (100.0%) | **+2.267** | 3.0 (1.0–14.0) | 64.9% |
| **3** | `37052` | **Naman Dhir** | Finisher 6+ | 515 | 186 | 286.7 | +33.57 | +4.14 | +32.13 | 60.1% (73.3%) | **+2.028** | 5.0 (1.0–33.0) | 66.1% |
| **4** | `143` | **Dinesh Karthik** | Finisher 6+ | 639 | 250 | 372.0 | +36.24 | +24.41 | +27.70 | 56.2% (56.2%) | **+1.764** | 8.0 (1.0–38.0) | 60.9% |
| **5** | `768` | **Reeza Hendricks** | Top 1-3 | 835 | 223 | 424.9 | +29.59 | +4.02 | +28.18 | 59.8% (85.7%) | **+1.745** | 8.0 (2.0–35.2) | 54.3% |
| **6** | `2756` | **Shashank Singh** | Finisher 6+ | 560 | 327 | 402.1 | +32.42 | +17.20 | +26.41 | 56.6% (57.9%) | **+1.609** | 9.0 (1.0–45.0) | 55.6% |
| **7** | `4260` | **Heinrich Klaasen** | Middle 4-5 | 1,417 | 459 | 772.9 | +25.20 | +23.08 | +17.13 | 65.0% (83.3%) | **+1.608** | 12.0 (3.9–31.0) | 41.9% |
| **8** | `4708` | **Rinku Singh** | Finisher 6+ | 1,284 | 507 | 711.1 | +28.87 | +19.76 | +21.95 | 58.1% (61.3%) | **+1.445** | 11.0 (2.0–43.0) | 47.8% |
| **9** | `1318` | **Andre Russell** | Finisher 6+ | 733 | 347 | 490.0 | +29.57 | +37.56 | +16.43 | 59.8% (68.2%) | **+1.434** | 12.0 (2.0–55.0) | 45.7% |
| **10** | `8101` | **Ashutosh Sharma** | Finisher 6+ | 334 | 273 | 290.6 | +24.97 | +5.35 | +23.10 | 58.3% (64.7%) | **+1.335** | 12.0 (2.0–52.0) | 28.0% |

### Batter Selection Justification
1. **Tim David (#1):** Leads the entire `99`-batter pool in shrunk pressure impact (`+41.75 / 100`), maintains elite production across both normal (`+38.49`) and pressure overs, excels in Death (`+40.93`) and vs Pace (`+46.57`), and delivers across both IPL (`362` HP balls, `+30.15` shrunk) and T20I (`208` HP balls, `+41.96` shrunk) with `89.3%` bootstrap Top-10 inclusion. Best HP match: `41507` (`2025-07-25`, T20I, `18` HP balls, `+47.81` impact).
2. **Matthew Wade (#2):** Highest Maintenance & Lift (`+33.64`) and strong Death (`+45.41`) / vs Pace (`+40.42`) T20I impact (`+38.96` shrunk T20I, `155` of `158` HP balls in T20Is), though `280/1000` bootstrap draws fall below the `120` HP-ball / `10`-match gate and last match was `2024-04-10`.
3. **Naman Dhir (#3):** High-impact young Indian finisher (`+33.57` shrunk WP impact, `+39.48` vs Pace) who translates across IPL (`142` HP balls, `+20.23` shrunk) and T20I (`44` HP balls, `+29.55` shrunk) through `2026-11-01`.
4. **Dinesh Karthik (#4):** Driven by elite IPL death-overs finishing (`207` IPL HP balls, `+35.89` shrunk IPL impact; `+33.81` Death, `+38.75` vs Pace) with `994/1000` eligible bootstrap draws.
5. **Reeza Hendricks (#5):** The lone `Top 1-3` batter in the V2 Top 10; moves from V1 `#1` to `#5` once his `6/7` (`85.7%`) consistency streak is shrunk to `59.8%` EB consistency, though his `223` HP balls (`N_eff = 424.9`) are `100%` T20I (`0` IPL balls).
6. **Shashank Singh (#6):** Pure IPL middle/death finisher (`327` IPL HP balls, `N_eff = 402.1`, `+31.40` shrunk IPL impact; balanced `+27.74` vs Pace and `+24.74` vs Spin).
7. **Heinrich Klaasen (#7):** Elite `Middle 4-5` pressure anchor (`N_eff = 772.9`, highest EB consistency in Top 10 at `65.0%` from `20/24` qualifying HP matches; unmatched `+38.00` vs Spin).
8. **Rinku Singh (#8):** Rescued from V1's `#24` elite-baseline penalty (`+28.87` shrunk WP impact vs `+19.76` normal; `#1` among Top 10 in Death phase at `+58.63`, `1,000/1,000` eligible bootstrap draws).
9. **Andre Russell (#9):** High-impact finisher (`347` HP balls, `+37.56` normal baseline, `+34.28` Middle phase; `1,000/1,000` eligible draws) who entered Top 10 once the 1:1 `HP - LP` penalty was replaced by Maintenance & Lift.
10. **Ashutosh Sharma (#10):** **Directly rescued from V1's `lp_balls >= 60` disqualification** (`81.7%` of his `334` career balls were HP; `273` IPL HP balls, `+32.97` Death, `+33.92` vs Pace). Wide CI (`p05=2.0–p95=52.0`, `338` ineligible bootstrap draws) reflects his `334`-ball boundary proximity.

---

## 2. Canonical Top 10 Bowlers Under Pressure

| Rank | ID | Player Name | Style | `N_tot` | `N_hp` | `N_eff` | Shrunk WP Impact | Shrunk Norm Impact | Maint Lift | EB Cons (Raw) | Pressure Score | Boot Med (p05–p95) | Top-10 Freq |
|---:|---:|---|---|---:|---:|---:|---:|---:|---:|---|---|---:|---:|---:|
| **1** | `781` | **Sunil Narine** | Spin (OB) | 1,530 | 454 | 739.6 | +9.98 | +3.40 | +8.79 | 71.4% (93.1%) | **+2.481** | 4.0 (1.0–13.0) | 90.5% |
| **2** | `2933` | **Jasprit Bumrah** | Pace (RF) | 1,708 | 496 | 785.1 | +9.61 | +6.24 | +7.43 | 65.3% (74.4%) | **+1.995** | 7.0 (1.0–33.0) | 65.7% |
| **3** | `4373` | **Mustafizur Rahman** | Pace (LM) | 1,576 | 500 | 749.5 | +8.04 | +0.90 | +7.73 | 66.5% (77.8%) | **+1.851** | 11.0 (2.0–38.0) | 49.3% |
| **4** | `2382` | **Jamie Overton** | Pace (RF) | 497 | 165 | 250.6 | +8.84 | -0.82 | +9.13 | 61.1% (75.0%) | **+1.839** | 8.0 (1.0–41.0) | 46.9% |
| **5** | `2878` | **Mohit Sharma** | Pace (RMF) | 649 | 277 | 370.6 | +7.69 | -3.58 | +8.74 | 63.2% (77.8%) | **+1.736** | 12.0 (1.0–55.0) | 43.4% |
| **6** | `5577` | **Sai Kishore** | Spin (SLA) | 465 | 123 | 204.5 | +7.72 | -2.04 | +8.43 | 63.1% (100.0%) | **+1.708** | 6.0 (2.0–17.3) | 37.0% |
| **7** | `34485` | **Sufiyan Muqeem** | Spin (LWC) | 344 | 148 | 214.8 | +7.90 | -0.85 | +8.20 | 62.2% (81.8%) | **+1.665** | 10.0 (1.0–73.0) | 32.0% |
| **8** | `6669` | **Mohsin Khan** | Pace (LMF) | 654 | 163 | 283.6 | +8.16 | +1.63 | +7.59 | 61.8% (76.9%) | **+1.625** | 11.0 (1.0–61.4) | 41.3% |
| **9** | `2490` | **Mohammad Nawaz** | Spin (SLA) | 1,004 | 282 | 486.9 | +7.94 | +0.84 | +7.64 | 60.9% (68.2%) | **+1.556** | 13.0 (2.0–45.1) | 41.7% |
| **10** | `830` | **Josh Hazlewood** | Pace (RFM) | 1,476 | 436 | 692.8 | +7.49 | +3.60 | +6.23 | 63.3% (70.0%) | **+1.472** | 16.0 (2.0–53.0) | 34.9% |

### Bowler Selection Justification
1. **Sunil Narine (#1):** Dominates the `128`-bowler pool in both shrunk pressure impact (`+9.98 / 24`) and EB consistency (`71.4%`, `27/29` qualifying HP matches), with `90.5%` bootstrap Top-10 inclusion and Death-phase shrunk impact `+11.71`.
2. **Jasprit Bumrah (#2):** Rises from V1 `#8` to V2 `#2` once the elite-baseline penalty on his `+6.24` normal baseline is removed; highest `N_eff` (`785.1`) in the Top 10, elite in both IPL (`+8.64`) and T20I (`+7.08`), and `+11.37` in Death overs.
3. **Mustafizur Rahman (#3):** High-volume left-arm pace/cutter specialist (`500` HP balls, `N_eff = 749.5`, `66.5%` EB consistency, `+8.08` Death impact) anchored by strong T20I numbers (`+8.90` shrunk T20I vs `+2.89` IPL).
4. **Jamie Overton (#4):** High-impact fast bowler (`+8.84` shrunk WP impact, `+9.56` Death) performing in both T20I (`+7.88`) and IPL (`+3.48`), though modest `N_eff` (`250.6`) causes `209/1000` ineligible draws.
5. **Mohit Sharma (#5):** Pure IPL death/middle-overs specialist (`277` IPL HP balls, `+7.41` Middle, `+5.25` Death) retaining `#5` with `995/1000` eligible bootstrap draws.
6. **Sai Kishore (#6):** Drops from V1 `#2` to `#6` as `7/7` (`100%`) raw consistency shrinks to `63.1%` EB consistency; remains vulnerable to volume gate (`545/1000` ineligible draws at `123` HP balls).
7. **Sufiyan Muqeem (#7):** Drops from V1 `#1` to `#7` under opponent-Elo and Beta-binomial shrinkage (`148` T20I HP balls, `N_eff = 214.8`, wide CI `1.0–73.0`).
8. **Mohsin Khan (#8):** Strong all-phase IPL left-arm pacer (`+5.82` Powerplay, `+5.56` Middle, `+4.70` Death; `163` IPL HP balls, `+7.47` shrunk IPL impact).
9. **Mohammad Nawaz (#9):** T20I left-arm spinner (`282` T20I HP balls, `N_eff = 486.9`, `+8.09` Middle overs; `999/1000` eligible bootstrap draws).
10. **Josh Hazlewood (#10):** All-format powerplay & death ace (`436` HP balls, `N_eff = 692.8`, `+7.60` Powerplay, `+5.92` Death; `1,000/1,000` eligible draws) who enters V2 Top 10 ahead of V1's `#9` Mitchell Santner (`#15`) and `#7` Kuldeep Yadav (`#16`).

---

## 3. V1-to-V2 Shifts & Near-Miss Contenders

- **Reversal of V1 Top-Order / Bilateral Inflation:** Controlling for `batting_role` (`Top 1-3` vs `Finisher 6+`), chronological `opp_tier` Elo, and Beta-binomial consistency dampens V1's top-order and bilateral T20I inflation: `Sanju Samson` moves `#5 -> #31`, `Shubman Gill` `#6 -> #35`, `Mark Chapman` `#7 -> #22`, `Shai Hope` `#9 -> #44`, and `Mohammad Rizwan` `#10 -> #59`.
- **Strongest Contenders Just Outside Top 10:**
  - *Batters:* `Romario Shepherd` (`#11`, score `+1.241`), `Suryakumar Yadav` (`#12`, `+1.061`, `N_eff = 1,180.5`, `#10` under Model C), `Rovman Powell` (`#13`, `+1.052`).
  - *Bowlers:* `Abrar Ahmed` (`#11`, `+1.433`), `Jofra Archer` (`#12`, `+1.417`), `Gerald Coetzee` (`#13`, `+1.394`), `Rashid Khan` (`#14`, `+1.320`, `N_eff = 1,479.2`), `Mitchell Santner` (`#15`, `+1.283`), `Kuldeep Yadav` (`#16`, `+1.275`), `Varun Chakravarthy` (`#17`, `+1.220`).
- **Notable Gate Near-Misses (`near_miss_candidates.csv`):** `Phil Salt` (`1,643` total balls, `N_eff = 354.8`, missed on `hp_balls = 112 < 120` and `hp_matches = 9 < 10`) and `Virat Kohli` (`2,456` total balls, `15` HP matches, `N_eff = 621.7`, missed on `hp_balls = 114 < 120`).

---

## 4. Separation of Statistical Ranking vs. Practical IPL 2027 Feasibility

Per governance rules, statistical rankings never incorporate manual availability overrides. As of **2026-11-12**, official IPL 2027 retention lists (due `2026-11-17`) and the final mini-auction register (due `2026-12-03` for the `2026-12-16` Goa auction) are unpublished, so every player's `ipl_2027_availability_status` is explicitly **`Unverified`**. Practical context flags for the Top 20 (`auction_feasibility.csv`) highlight:
- **Retired from IPL / Playing Formats (Not Feasible as Players):** `Matthew Wade` (BBL/domestic retired Sep 2026; Australia batting coach), `Dinesh Karthik` (IPL retired 2024; RCB Batting Coach & Mentor), `Andre Russell` (IPL retired Nov 2025; KKR Power Coach), `Mohit Sharma` (retired Dec 2025; CSK bowling coach).
- **BCCI Policy Ineligible / Zero IPL Exposure:** `Sufiyan Muqeem` and `Mohammad Nawaz` (Pakistan nationals, zero IPL eligibility under BCCI policy); `Reeza Hendricks` (zero IPL contracts).
- **Active IPL Core / Likely Retained:** `Tim David` (RCB), `Naman Dhir` (MI), `Shashank Singh` (PBKS), `Heinrich Klaasen` (SRH), `Rinku Singh` (KKR vice-captain), `Ashutosh Sharma` (DC), `Sunil Narine` (KKR), `Jasprit Bumrah` (MI), `Jamie Overton` (CSK, May 2026 thigh injury), `Sai Kishore` (GT, 3 games in 2026 post-finger surgery), `Mohsin Khan` (LSG), `Josh Hazlewood` (RCB).
- **Confirmed Auction Entrant Context:** `Mustafizur Rahman` (released by KKR pre-IPL 2026; BCB confirmed registration for IPL 2027 mini-auction as of `2026-11-11`).
