# 02 — Data Dictionary (`data/raw/*.csv`)

All column names, data types, null counts, unique counts, and domain values below were verified directly against the unmodified raw CSV files in `data/raw/`.

---

## 1. Table Inventory & Primary Relationships

| File | Rows | Columns | Primary Key / Grain | Joins To |
|---|---:|---:|---|---|
| `competitions.csv` | 141 | 4 | `comp_id` | `matches.comp_id`, `teams.comp_id`, `competition_team_player_mapping.comp_id` |
| `teams.csv` | 353 | 3 | `(comp_id, team_id)` | `matches`, `playing_eleven`, `ball_by_ball` |
| `matches.csv` | 883 | 22 | `match_id` | `competitions.comp_id`, `ball_by_ball.match_id`, `playing_eleven.match_id` |
| `playing_eleven.csv` | 28,381 | 9 | `(match_id, team_id, player_id)` *(40 key dups)* | `matches.match_id`, `teams.team_id` |
| `competition_team_player_mapping.csv` | 6,413 | 6 | `(comp_id, team_id, player_id)` | `competitions.comp_id`, `teams.team_id` |
| `ball_by_ball.csv` | 200,999 | 33 | `(match_id, innings, overid, over_ball_num)` | `matches.match_id`, `teams.team_id`, `player_id`s |

---

## 2. `competitions.csv` (141 rows, 4 columns)

| Column | Dtype | Nulls | Unique | Description & Observed Values |
|---|---|---:|---:|---|
| `comp_id` | `int64` | 0 | 141 | Unique competition identifier (3 comps `2940`, `3405`, `3473` have 0 matches in `matches.csv`). |
| `comp_name` | `str` | 0 | 141 | Official tournament/series name (e.g., `South Africa in New Zealand T20I Series 2026`, `IPL 2022`). |
| `match_format` | `str` | 0 | 2 | `T20I` (134 rows) or `T20` (7 rows: 5 IPL seasons + 2 A-team tournaments `comp_id` `2670`, `3289`). |
| `season` | `str` | 0 | 8 | Season label (`2022`–`2026`, plus `2022/23`, `2023/24`, `2024/25`). |

---

## 3. `teams.csv` (353 rows, 3 columns)

| Column | Dtype | Nulls | Unique | Description & Observed Values |
|---|---|---:|---:|---|
| `comp_id` | `int64` | 0 | 141 | Foreign key to `competitions.comp_id`. |
| `team_id` | `int64` | 0 | 38 | Unique team identifier across all IPL franchises and national/A sides. |
| `team_name` | `str` | 0 | 38 | Team display name (e.g., `England`, `Rajasthan Royals`). |

---

## 4. `matches.csv` (883 rows, 22 columns)

Date range: `2022-01-22` to `2026-11-01`. Includes `16` abandoned matches absent from `ball_by_ball.csv` (`3` also absent from `playing_eleven.csv`).

| Column | Dtype | Nulls | Unique | Description & Observed Values |
|---|---|---:|---:|---|
| `match_id` | `int64` | 0 | 883 | Unique match identifier. |
| `comp_id` | `int64` | 0 | 138 | Foreign key to `competitions.comp_id`. |
| `match_number` | `int64` | 0 | 75 | Match sequence number within the competition. |
| `match_date` | `str` | 0 | 686 | ISO date (`YYYY-MM-DD`, `2022-01-22` to `2026-11-01`). |
| `stage` | `str` | 0 | 7 | `League` (620), `Others` (226), `Final` (12), `Qualifier` (10), `Super 4` (6), `Eliminator` (5), `Semi Final` (4). |
| `venue_id` | `int64` | 0 | 98 | Numeric venue identifier. |
| `venue_country` | `str` | 0 | 17 | Host country name (e.g., `India`, `West Indies`). |
| `home_team_id` | `int64` | 0 | 36 | Home team `team_id`. |
| `home_team` | `str` | 0 | 36 | Home team name. |
| `away_team_id` | `int64` | 0 | 36 | Away team `team_id`. |
| `away_team` | `str` | 0 | 36 | Away team name. |
| `home_team_captain_id` | `float64` | 44 | 89 | `player_id` of home captain (nullable). |
| `away_team_captain_id` | `float64` | 45 | 98 | `player_id` of away captain (nullable). |
| `toss_win_team_id` | `float64` | 15 | 37 | `team_id` winning the toss (null on abandoned matches without toss). |
| `toss_opted` | `str` | 15 | 2 | `Fielding` (639), `Batting` (229), or null (15). |
| `man_of_the_match` | `int64` | 0 | 293 | `player_id` of Player of the Match (`0` sentinel in 119 rows). |
| `first_inn_revised_overs` | `float64` | 858 | 13 | **IMPORTANT — Stored in BALLS, not overs** (e.g., `114.0` = 19 overs). Populated only for 25 rain-reduced matches; default `120` balls when null. |
| `second_inn_revised_overs` | `float64` | 858 | 12 | **IMPORTANT — Stored in BALLS, not overs.** Populated only for 25 rain-reduced matches; default `120` balls when null. |
| `revised_target` | `float64` | 860 | 23 | D/L revised 2nd-innings target runs (populated for 23 D/L chases; else `inn1_total_runs + 1`). |
| `knock_out` | `int64` | 0 | 2 | Binary knockout flag: `0` (852 matches), `1` (31 matches). |
| `win_team_id` | `float64` | 41 | 36 | Winning `team_id` (41 nulls: 21 No Result, 19 Match Abandoned, 1 Match Tied). |
| `result` | `str` | 0 | 670 | Human-readable result string (e.g., `West Indies Won by 9 Wickets`). |

---

## 5. `playing_eleven.csv` (28,381 rows, 9 columns)

Covers `880` matches and `1,082` unique `player_id`s. Contains **40 duplicate `(match_id, team_id, player_id)` rows**; deduplicate prioritizing `is_played == True`.

| Column | Dtype | Nulls | Unique | Description & Observed Values |
|---|---|---:|---:|---|
| `match_id` | `int64` | 0 | 880 | Foreign key to `matches.match_id`. |
| `team_id` | `int64` | 0 | 38 | Foreign key to `teams.team_id`. |
| `player_id` | `int64` | 0 | 1,082 | Unique player identifier. |
| `batting_order` | `float64` | 8,678 | 13 | Listed batting position (`1`–`13`; null for `8,667` unused squad/bench rows + `11` rows with `is_played == True`). |
| `is_played` | `bool` | 0 | 2 | `True` if player took part in match, `False` for unused squad/substitutes. |
| `is_captain` | `object` | 8,667 | 2 | Boolean captain indicator (`True`/`False`; null when `is_played == False`). |
| `is_wk` | `object` | 8,667 | 2 | Boolean wicketkeeper indicator (`True`/`False`; null when `is_played == False`). |
| `is_impact` | `int64` | 0 | 2 | `1` if subbed in as IPL Impact Player, else `0`. |
| `is_impact_off` | `int64` | 0 | 2 | `1` if subbed off for IPL Impact Player, else `0`. |

---

## 6. `competition_team_player_mapping.csv` (6,413 rows, 6 columns)

| Column | Dtype | Nulls | Unique | Description & Observed Values |
|---|---|---:|---:|---|
| `comp_id` | `int64` | 0 | 140 | Foreign key to `competitions.comp_id`. |
| `comp_name` | `str` | 0 | 140 | Competition name. |
| `team_id` | `int64` | 0 | 38 | Team identifier. |
| `team_name` | `str` | 0 | 38 | Team name. |
| `player_id` | `int64` | 0 | 1,217 | Unique player identifier (1,217 IDs vs 1,210 names — always key on `player_id`). |
| `player_name` | `str` | 0 | 1,210 | Player display name. |

---

## 7. `ball_by_ball.csv` (200,999 rows, 33 columns)

Covers `867` matches (`367` IPL = `87,687` rows; `470` T20I = `106,327` rows; `30` `Other_T20` = `6,985` rows). Removing `Other_T20` and `38` Super Over rows (`innings` 3–4) leaves **837 matches** and **193,988 deliveries** (**185,692 legal balls**).

| Column | Dtype | Nulls | Unique | Description & Observed Values |
|---|---|---:|---:|---|
| `match_id` | `int64` | 0 | 867 | Foreign key to `matches.match_id`. |
| `innings` | `int64` | 0 | 4 | `1`, `2` (regulation), `3`, `4` (Super Overs — 38 rows across 6 matches). |
| `overid` | `int64` | 0 | 20 | 1-indexed over number (`1`–`20`). |
| `over_ball_num` | `int64` | 0 | 13 | Sequential delivery index within the over (`1`–`13`, includes wides/no-balls). |
| `innings_ball_num` | `int64` | 0 | 136 | Sequential delivery index within the innings (`1`–`136`). |
| `batting_team_id` | `int64` | 0 | 38 | Batting team `team_id`. |
| `bowling_team_id` | `int64` | 0 | 38 | Bowling team `team_id`. |
| `striker_id` | `int64` | 0 | 888 | Batter on strike (`player_id`). |
| `striker_name` | `str` | 0 | 885 | Striker name (885 names for 888 IDs due to homonyms). |
| `non_striker_id` | `int64` | 0 | 867 | Non-striker (`player_id`). |
| `non_striker_name` | `str` | 0 | 864 | Non-striker name. |
| `bowler_id` | `int64` | 0 | 647 | Bowler (`player_id`). |
| `bowler_name` | `str` | 0 | 646 | Bowler name. |
| `batting_type` | `str` | 0 | 2 | `RHB` (131,006), `LHB` (69,993). |
| `bowling_type` | `str` | 0 | 12 | Detailed style (e.g., `Right-arm Leg-Break`, `Right-arm Fast`, `Slow left-arm orthodox`, etc.). |
| `batting_order` | `int64` | 0 | 13 | Striker's batting entry position (`1`–`13`). |
| `runs` | `int64` | 0 | 7 | Runs scored off the bat (`0`–`6`). |
| `is_four` | `bool` | 0 | 2 | `True` if boundary 4 (`runs == 4` / boundary). |
| `is_six` | `bool` | 0 | 2 | `True` if boundary 6 (`runs == 6`). |
| `is_wicket` | `bool` | 0 | 2 | `True` if a team wicket fell on this delivery. |
| `dismissal_type_id` | `float64` | 190,118 | 8 | Numeric dismissal code (non-null only when `dismissal_type` is populated). |
| `dismissal_type` | `str` | 190,118 | 9 | `Caught` (7,557), `Bowled` (1,775), `LBW` (709), `RunOut` (600), `Stump` (214), `Hit Wicket` (17), `Retire Out` (6), `Obstracting the field` (2 — typo), `Obstructing the field` (1). |
| `dismissed_player_id` | `float64` | 190,107 | 814 | `player_id` dismissed (12 rows have `is_wicket=False` with `dismissed_player_id` populated [Retired Hurt]; 1 row has `is_wicket=True` with null `dismissed_player_id`). |
| `extras_type` | `str` | 189,167 | 6 | `wide` (7,714), `legbyes` (2,748), `Overstep` (576, no-ball), `byes` (529), `other` (264, no-ball), `Penalty` (1). |
| `extras1_runs` | `int64` | 0 | 6 | Primary extra runs (e.g., `1` for no-ball/wide, plus wide runs). |
| `extras_2_runs` | `int64` | 0 | 3 | Secondary extra runs. |
| `pace_or_spin` | `str` | 0 | 2 | `Pace` (123,886) or `Spin` (77,113). |
| `bowl_speed` | `float64` | 0 | 1,033 | Delivery speed in km/h (`0.0` sentinel on `77,861` rows = `38.74%`; extreme outliers up to `1456.1`). |
| `stroke` | `str` | 6,158 | 30 | Batter shot classification (e.g., `Cover Drive`). |
| `delivery_style` | `str` | 391 | 34 | Delivery variation (e.g., `Inswing`). |
| `over_or_around` | `str` | 407 | 2 | `Over` (154,670), `Around` (45,922), or null (407). |
| `on_or_off` | `str` | 0 | 2 | `Off-side` (104,875), `On-side` (96,124). |
| `delivery_ist_time` | `str` | 0 | 200,826 | Timestamp string (e.g., `2022-01-23 00:00:00 UTC`). |

*(Exact column name for secondary extras in `ball_by_ball.csv` is `extras_2_runs`.)*

---

## 8. Critical Cricket Accounting Rules

- **Legal delivery:** `~(extras_type.isin(['wide', 'Overstep', 'other']))` (`byes` and `legbyes` are legal).
- **Batter ball faced:** `~(extras_type == 'wide')` (no-balls `Overstep` and `other` count as balls faced and allow bat runs).
- **Total team runs:** `runs + extras1_runs + extras_2_runs`.
- **Bowler runs conceded:** `runs + extras1_runs` when `extras_type` is `wide`, `Overstep`, or `other`; otherwise `runs` (byes, legbyes, and Penalty are excluded).
- **Bowler-credited wicket:** `is_wicket & dismissal_type.isin({'Caught', 'Bowled', 'LBW', 'Stump', 'Hit Wicket'})`. All team wickets (`is_wicket == True`) advance match-state `pre_wickets`.
