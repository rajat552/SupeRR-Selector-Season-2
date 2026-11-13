# 03 — Data Audit

All counts and diagnostics below were computed directly from the unmodified raw files in `data/raw/`.

## 1. File Inventory & Dimensions

| File | Size (bytes) | Rows | Columns | Exact Duplicate Rows |
|---|---:|---:|---:|---:|
| `competitions.csv` | 7,624 | 141 | 4 | 0 |
| `teams.csv` | 6,922 | 353 | 3 | 0 |
| `matches.csv` | 123,864 | 883 | 22 | 0 |
| `playing_eleven.csv` | 966,287 | 28,381 | 9 | 0 *(40 key dups)* |
| `competition_team_player_mapping.csv` | 462,969 | 6,413 | 6 | 0 |
| `ball_by_ball.csv` | 41,071,837 | 200,999 | 33 | 0 |
| `Round 1 Problem Statement _ SupeRR Selector Season 2.docx.pdf` | 254,082 | 2 pages | — | — |

## 2. Competition, Season & Format Coverage

- **Date range (`matches.csv`):** `2022-01-22` to `2026-11-01` (883 matches across 138 competitions; 3 competitions in `competitions.csv`—`comp_id` `2940`, `3405`, `3473`—have 0 matches).
- **Format breakdown in `matches.csv` vs `ball_by_ball.csv`:**
  - **IPL (`match_format = 'T20'` and `'IPL'` in `comp_name`):** 371 matches in `matches.csv` (seasons 2022–2026) → **367 matches** / **87,687 deliveries** in `ball_by_ball.csv` (4 abandoned).
  - **T20I (`match_format = 'T20I'`):** 482 matches in `matches.csv` → **470 matches** / **106,327 deliveries** in `ball_by_ball.csv` (12 abandoned).
  - **Non-IPL `T20` (`Other_T20`):** **30 matches** / **6,985 deliveries** across 2 A-team tournaments:
    - `Mens T20 Emerging Teams Asia Cup 2024` (`comp_id = 2670`, 15 matches)
    - `Asia Cup Rising Stars 2025` (`comp_id = 3289`, 15 matches)
- **Unique Teams:** 38 unique `team_id`s across `teams.csv` and `ball_by_ball.csv` (36 in `matches.csv` home/away).
- **Unique Players:**
  - `competition_team_player_mapping.csv`: 1,217 unique `player_id`s (1,210 unique `player_name`s).
  - `playing_eleven.csv`: 1,082 unique `player_id`s.
  - `ball_by_ball.csv`: 888 unique `striker_id`s (885 names), 867 unique `non_striker_id`s (864 names), 647 unique `bowler_id`s (646 names).

## 3. Missing Values Summary

- **`competitions.csv`, `teams.csv`, `competition_team_player_mapping.csv`:** 0 nulls across all columns.
- **`matches.csv`:**
  - `home_team_captain_id`: 44 nulls (4.98%)
  - `away_team_captain_id`: 45 nulls (5.10%)
  - `toss_win_team_id` / `toss_opted`: 15 nulls (1.70%)
  - `win_team_id`: 41 nulls (4.64% — 21 No Result, 19 Match Abandoned, 1 Match Tied)
  - `first_inn_revised_overs` / `second_inn_revised_overs`: 858 nulls (97.17% — populated only for 25 rain-affected matches)
  - `revised_target`: 860 nulls (97.40% — populated only for 23 D/L chases)
  - `man_of_the_match`: 0 nulls, but `0` sentinel in 119 rows.
- **`playing_eleven.csv`:**
  - `batting_order`: 8,678 nulls (30.58% — 8,667 where `is_played == False`, plus 11 where `is_played == True`).
  - `is_captain`, `is_wk`: 8,667 nulls each (30.54% — all where `is_played == False`).
- **`ball_by_ball.csv`:**
  - `dismissal_type_id`, `dismissal_type`: 190,118 nulls (94.59%, non-null only on wickets).
  - `dismissed_player_id`: 190,107 nulls (94.58% — 11-row mismatch with `is_wicket`, see §4).
  - `extras_type`: 189,167 nulls (94.11%, non-null only on extras).
  - `stroke`: 6,158 nulls (3.06%).
  - `delivery_style`: 391 nulls (0.19%).
  - `over_or_around`: 407 nulls (0.20%).
  - `bowl_speed`: 0 nulls, but **`0.0` sentinel in 77,861 rows (38.74%)**.

## 4. Data-Integrity Issues & Anomalies Discovered

1. **Non-IPL `T20` Tournaments (30 matches):** `Mens T20 Emerging Teams Asia Cup 2024` and `Asia Cup Rising Stars 2025` are tagged `match_format = 'T20'` (A-team/emerging fixtures), whereas the official brief specifies IPL and T20I data.
2. **Player Name Collisions & Duplicate Player IDs:**
   - **True homonyms (different people, same name):** `Abdul Samad` (`7446` India/IPL vs `6922` Pakistan/Pak A), `Rashid Khan` (`4722` Afghanistan/GT vs `20172` Nepal), `Haider Ali` (`7338` Pakistan vs `28756` UAE).
   - **Potential duplicate IDs for same player:** `Basil Hameed` (`8638` & `39444`, both UAE), `Muhammad Farooq` (`27373` & `28978`, both UAE), `Bashir Ahmad` (`39479` Afg A & `29833` Afg), `Mohammad Ali` (`3083` & `20229`, both Pak).
3. **`playing_eleven.csv` Key Duplicates:** 40 duplicate `(match_id, team_id, player_id)` rows (e.g., `match_id = 13613` lists players twice with different batting orders).
4. **Abandoned Matches Without Deliveries:** 16 matches in `matches.csv` are absent from `ball_by_ball.csv` (all `Match Abandoned`); 3 of these (`48513`, `36210`, `41503`) are also absent from `playing_eleven.csv`.
5. **Super Overs:** 6 matches (`34429`, `40725`, `45512`, `48027`, `48029`, `50359`) contain `innings` `3` and `4` (38 deliveries total).
6. **Extras & Legal-Delivery Conventions:**
   - `wide` (7,714): not a legal delivery; not a ball faced by batter.
   - `Overstep` (576) and `other` (264): both are **no-balls** (`extras1_runs = 1`, plus batter `runs` and `extras_2_runs`); not a legal delivery for bowler overs, but batter can score runs off the bat.
   - `byes` (529), `legbyes` (2,748): legal deliveries, no batter runs (except 1 anomalous `legbyes` row with `runs=1`).
   - `Penalty` (1 row, 5 runs).
   - 2 rows have `extras_type = NaN` yet `extras1_runs > 0` or `extras_2_runs > 0` (`match_id` `17555`, `36097`).
7. **Wicket & Dismissal Anomalies:**
   - 12 rows have `is_wicket = False` and `dismissal_type = NaN` yet `dismissed_player_id` is populated (likely Retired Hurt).
   - 1 row (`match_id = 40709`, inn 2) has `is_wicket = True` and `dismissed_player_id = NaN`.
   - 275 dismissals have `dismissed_player_id != striker_id` (271 `RunOut`, 3 `Retire Out`, 1 `Obstracting the field`).
   - Typo in `dismissal_type`: `Obstracting the field` (2 rows) vs `Obstructing the field` (1 row).
8. **Misleading Column Name (`*_revised_overs`):** `first_inn_revised_overs` and `second_inn_revised_overs` store **balls** (e.g., `114.0` = 19 overs), not overs.
9. **Speed-Gun Outliers (`bowl_speed`):** 38.74% are `0.0`; 20 rows exceed `165 km/h` (up to `1456.1 km/h`), and 22 rows are between `0` and `50 km/h`.

## 5. Initial Exclusion & Cleaning Recommendations (Pending Approval)
- **Exclude from primary dataset (or flag):**
  1. The 16 abandoned matches with 0 deliveries.
  2. Super Over deliveries (`innings in {3, 4}`, 38 balls) from standard 20-over Pressure Index & baseline calculations (analyse separately if needed).
  3. **Decision needed:** Exclude the 30 `Other_T20` (A-team) matches so the primary pool strictly reflects IPL + T20I as stated in the official PDF (keep as a sensitivity check if desired).
  4. Exclude `Retire Out` / `Retired Hurt` from bowler wicket credit; credit only bowler-attributable dismissals (`Caught`, `Bowled`, `LBW`, `Stump`, `Hit Wicket`) to bowlers, while counting all team wickets fallen for match-state tracking.
- **Deduplicate** `playing_eleven.csv` on `(match_id, team_id, player_id)`.
- **Key all player stats on `player_id`**, never `player_name`.

