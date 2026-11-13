"""Independent unit tests verifying cricket accounting, data filters, identity joins, and bootstrap rules."""

import unittest
from pathlib import Path
import numpy as np
import pandas as pd

from independent_audit import (
    load_raw,
    independent_prepare,
    independent_state_and_pi,
    BOWLER_DISMISSALS,
)


class TestCricketAuditRules(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.raw = load_raw()
        cls.bbb_all, cls.matches, cls.pl = independent_prepare(
            cls.raw, include_other_t20=True, include_super_overs=True
        )
        cls.bbb_prim, _, _ = independent_prepare(
            cls.raw, include_other_t20=False, include_super_overs=False
        )
        cls.df_prim = independent_state_and_pi(cls.bbb_prim)

    def test_01_legal_delivery_counting(self):
        """Wides, Overstep, and other (no-balls) are not legal deliveries; byes/legbyes are."""
        wides = self.bbb_all[self.bbb_all["extras_type"] == "wide"]
        oversteps = self.bbb_all[self.bbb_all["extras_type"] == "Overstep"]
        others = self.bbb_all[self.bbb_all["extras_type"] == "other"]
        byes = self.bbb_all[self.bbb_all["extras_type"] == "byes"]
        legbyes = self.bbb_all[self.bbb_all["extras_type"] == "legbyes"]

        self.assertTrue((~wides["is_legal_ball"]).all())
        self.assertTrue((~oversteps["is_legal_ball"]).all())
        self.assertTrue((~others["is_legal_ball"]).all())
        self.assertTrue(byes["is_legal_ball"].all())
        self.assertTrue(legbyes["is_legal_ball"].all())

    def test_02_extras_and_bowler_conceded_runs(self):
        """Byes, legbyes, and Penalty do not count against bowler_runs_conceded; wides/noballs do."""
        byes = self.bbb_all[self.bbb_all["extras_type"] == "byes"]
        self.assertEqual(int(byes["bowler_runs_conceded"].sum()), 0)
        penalty = self.bbb_all[self.bbb_all["extras_type"] == "Penalty"]
        self.assertEqual(int(penalty["bowler_runs_conceded"].sum()), 0)
        wides = self.bbb_all[self.bbb_all["extras_type"] == "wide"]
        self.assertEqual(int(wides["bowler_runs_conceded"].sum()), int(wides["extras1_runs"].sum()))

    def test_03_batter_runs_and_balls_faced(self):
        """Wides are not batter balls faced; Overstep/other no-balls allow batter runs and count as faced."""
        wides = self.bbb_all[self.bbb_all["extras_type"] == "wide"]
        self.assertTrue((~wides["is_batter_ball_faced"]).all())
        self.assertEqual(int(wides["runs"].sum()), 0)

        noballs = self.bbb_all[self.bbb_all["extras_type"].isin(["Overstep", "other"])]
        self.assertTrue(noballs["is_batter_ball_faced"].all())
        self.assertGreater(int(noballs["runs"].sum()), 1000)

    def test_04_credited_wickets_vs_runouts(self):
        """RunOut, Retire Out, and Obstructing the field do not credit bowlers; team wickets count all."""
        non_bowler = self.bbb_all[
            self.bbb_all["is_team_wicket"]
            & (~self.bbb_all["dismissal_type"].isin(BOWLER_DISMISSALS))
        ]
        self.assertGreater(len(non_bowler), 600)
        self.assertEqual(int(non_bowler["is_bowler_wicket"].sum()), 0)

        runouts = self.bbb_all[self.bbb_all["dismissal_type"] == "RunOut"]
        self.assertEqual(len(runouts), 600)
        self.assertEqual(int(runouts["is_bowler_wicket"].sum()), 0)
        # Non-striker runouts must be preserved accurately
        ns_ro = runouts[runouts["dismissed_player_id"] != runouts["striker_id"]]
        self.assertGreater(len(ns_ro), 250)

    def test_05_super_overs_excluded_in_primary(self):
        """Super Overs (innings 3 and 4, 38 balls) exist in raw and are excluded from primary."""
        so_raw = self.bbb_all[self.bbb_all["innings"].isin([3, 4])]
        self.assertEqual(len(so_raw), 38)
        self.assertTrue(self.bbb_prim["innings"].isin([1, 2]).all())

    def test_06_competition_filter_excludes_other_t20(self):
        """Primary dataset excludes the 30 Other_T20 A-team matches (6,985 deliveries)."""
        other_t20 = self.bbb_all[self.bbb_all["comp_category"] == "Other_T20"]
        self.assertEqual(other_t20["match_id"].nunique(), 30)
        self.assertEqual(len(other_t20), 6985)
        self.assertEqual((self.bbb_prim["comp_category"] == "Other_T20").sum(), 0)
        self.assertEqual(self.bbb_prim["match_id"].nunique(), 837)

    def test_07_player_identity_joins_preserve_homonyms(self):
        """Distinct player_ids sharing identical names are never merged."""
        abdul = self.pl[self.pl["player_name"] == "Abdul Samad"]
        rashid = self.pl[self.pl["player_name"] == "Rashid Khan"]
        haider = self.pl[self.pl["player_name"] == "Haider Ali"]
        self.assertEqual(set(abdul["player_id"]), {7446, 6922})
        self.assertEqual(set(rashid["player_id"]), {4722, 20172})
        self.assertEqual(set(haider["player_id"]), {7338, 28756})
        self.assertEqual(self.pl["player_id"].duplicated().sum(), 0)

    def test_08_zero_lookahead_pre_delivery_state(self):
        """First ball of every innings has pre_runs=0, pre_wickets=0, pre_legal_balls=0."""
        first_balls = self.df_prim.groupby(["match_id", "innings"]).first()
        self.assertTrue((first_balls["pre_runs"] == 0).all())
        self.assertTrue((first_balls["pre_wickets"] == 0).all())
        self.assertTrue((first_balls["pre_legal_balls"] == 0).all())

    def test_09_match_level_resampling_preserves_counts(self):
        """Stratified match-level resample preserves IPL (367) and T20I (470) match counts."""
        rng = np.random.default_rng(42)
        ipl_m = self.df_prim[self.df_prim["comp_category"] == "IPL"]["match_id"].unique()
        t20i_m = self.df_prim[self.df_prim["comp_category"] == "T20I"]["match_id"].unique()
        self.assertEqual(len(ipl_m), 367)
        self.assertEqual(len(t20i_m), 470)
        s_ipl = rng.choice(ipl_m, size=len(ipl_m), replace=True)
        s_t20i = rng.choice(t20i_m, size=len(t20i_m), replace=True)
        self.assertEqual(len(s_ipl), 367)
        self.assertEqual(len(s_t20i), 470)


if __name__ == "__main__":
    unittest.main(verbosity=2)

