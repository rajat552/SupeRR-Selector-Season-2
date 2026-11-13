"""Phase 1 (P0 Foundation) feature and baseline modules for Model V2."""

from .cricket_accounting import (
    BOWLER_WICKET_TYPES,
    NON_BOWLER_WICKET_TYPES,
    DISMISSAL_TYPO_MAP,
    NOBALL_EXTRAS_TYPES,
    apply_cricket_accounting,
    normalize_dismissal_types,
)
from .data_loader import (
    RAW_DIR,
    FULL_MEMBER_TEAMS,
    load_raw_tables,
    classify_competition,
    assign_comp_tier,
    deduplicate_playing_eleven,
    build_player_lookup,
    load_clean_dataset,
)
from .state_builder import assign_phase, build_match_state
from .opponent_strength import (
    DEFAULT_BASE_ELO,
    DEFAULT_K_FACTOR,
    DEFAULT_LOW_TIER_CUTOFF,
    DEFAULT_HIGH_TIER_CUTOFF,
    classify_elo_tier,
    compute_pre_match_elo,
    attach_opponent_elo,
)
from .pressure_model import (
    compute_v1_pressure_index,
    compute_pressure_weights,
    kish_effective_sample_size,
    grouped_kish_neff,
    compute_pressure_features,
)
from .batting_features import (
    ROLE_TOP,
    ROLE_MIDDLE,
    ROLE_FINISHER,
    ROLE_UNKNOWN,
    order_to_batting_role,
    add_batting_features,
    summarize_batter_roles,
)
from .bowling_features import (
    BOWLING_STYLE_GROUP_MAP,
    add_bowling_features,
    summarize_bowler_styles,
)
from .context_baselines import (
    DEFAULT_MIN_CELL_N,
    BAT_HIERARCHY,
    BOWL_HIERARCHY,
    add_lpo_context_baselines,
)


def build_foundation_dataset(
    include_other_t20: bool = False,
    include_super_overs: bool = False,
    min_cell_n: int = DEFAULT_MIN_CELL_N,
):
    """Convenience end-to-end Phase 1 builder returning (df, matches, pe, player_lookup, match_elo)."""
    bbb, matches, pe, player_lookup = load_clean_dataset(
        include_other_t20=include_other_t20,
        include_super_overs=include_super_overs,
    )
    df = build_match_state(bbb)
    df, match_elo = attach_opponent_elo(df, matches=matches)
    df = compute_pressure_features(df)
    df = add_batting_features(df, pe)
    df = add_bowling_features(df)
    df = add_lpo_context_baselines(df, min_cell_n=min_cell_n)
    return df, matches, pe, player_lookup, match_elo
