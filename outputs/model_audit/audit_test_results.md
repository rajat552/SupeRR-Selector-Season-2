# Audit Unit Test Results

Executed independently via:
```powershell
python outputs/model_audit/test_audit_rules.py
```

## Summary
- **Result:** **9 / 9 tests PASSED** in 3.956s (`OK`).
- **Source tested:** Standalone independent recalculation functions reading directly from `data/raw/*.csv` (`outputs/model_audit/independent_audit.py`).

## Test Coverage Breakdown
1. `test_01_legal_delivery_counting`: Verified `wide`, `Overstep`, and `other` are excluded from legal deliveries while `byes` and `legbyes` count as legal deliveries.
2. `test_02_extras_and_bowler_conceded_runs`: Verified `byes`, `legbyes`, and `Penalty` are excluded from `bowler_runs_conceded`, while `wide` and `Overstep`/`other` extras are charged to the bowler.
3. `test_03_batter_runs_and_balls_faced`: Verified `wide` deliveries have `0` batter runs and are excluded from batter balls faced, whereas `Overstep`/`other` no-balls allow batter runs and count as balls faced.
4. `test_04_credited_wickets_vs_runouts`: Verified `RunOut` (600 dismissals, including >250 non-striker run-outs), `Retire Out`, and `Obstructing the field` are counted as team wickets without crediting the bowler.
5. `test_05_super_overs_excluded_in_primary`: Verified 38 Super Over deliveries (`innings` 3 & 4) exist in raw data and are excluded from the primary 20-over dataset.
6. `test_06_competition_filter_excludes_other_t20`: Verified the 30 `Other_T20` A-team matches (6,985 deliveries) are excluded from the primary 837-match dataset.
7. `test_07_player_identity_joins_preserve_homonyms`: Verified `player_id` keying preserves distinct players sharing identical names (`Abdul Samad` 7446 vs 6922, `Rashid Khan` 4722 vs 20172, `Haider Ali` 7338 vs 28756).
8. `test_08_zero_lookahead_pre_delivery_state`: Verified the first delivery of every innings has `pre_runs = 0`, `pre_wickets = 0`, and `pre_legal_balls = 0`.
9. `test_09_match_level_resampling_preserves_counts`: Verified stratified match-level bootstrap resampling preserves exact IPL (367) and T20I (470) match counts.

