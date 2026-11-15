"""
SupeRR Selector Season 2 — Interactive Intelligence Dashboard
V4 Multiverse Analysis & Rajasthan Royals Recruitment Intelligence
"""

import os
import json
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="SupeRR Selector Season 2 — Rajasthan Royals Analytics",
    page_icon="🏏",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- CUSTOM CSS: RAJASTHAN ROYALS HIGH-PERFORMANCE DESIGN SYSTEM ---
st.markdown("""
<style>
    /* 1. Global Typography & Font Architecture */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;600&display=swap');
    
    html, body {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        -webkit-font-smoothing: antialiased;
        background-color: #070D1B !important;
        color: #F8FAFC !important;
    }

    .stMarkdown, .stMarkdown p, .stText, label, .stSelectbox label, .stMultiSelect label, .stRadio label {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
        -webkit-font-smoothing: antialiased;
    }

    /* Explicitly protect Streamlit Material Symbols & Icons from font-family overrides */
    [data-testid="stIconMaterial"],
    [data-testid*="Icon"],
    [data-testid="stSidebarCollapseButton"] *,
    [data-testid="stSidebarExpandButton"] *,
    .material-symbols-rounded,
    .material-symbols-outlined,
    .material-symbols-sharp,
    [class*="material-symbols"],
    [class*="material-icons"] {
        font-family: 'Material Symbols Rounded', 'Material Symbols Outlined', 'Material Icons' !important;
        font-weight: normal !important;
        font-style: normal !important;
        letter-spacing: normal !important;
        text-transform: none !important;
        display: inline-block !important;
        white-space: nowrap !important;
        word-wrap: normal !important;
        direction: ltr !important;
        -webkit-font-feature-settings: 'liga' 1 !important;
        font-feature-settings: 'liga' 1 !important;
    }
    
    code, pre {
        font-family: 'JetBrains Mono', monospace !important;
    }

    /* 2. Elevated Header Typography */
    .main-title {
        font-size: 2.25rem !important;
        font-weight: 800 !important;
        letter-spacing: -0.03em !important;
        background: linear-gradient(135deg, #FFFFFF 0%, #E2E8F0 60%, #EA1A80 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.35rem !important;
        line-height: 1.2 !important;
    }
    
    .sub-title {
        font-size: 1.05rem !important;
        font-weight: 400 !important;
        color: #94A3B8 !important;
        letter-spacing: -0.01em !important;
        margin-bottom: 1.5rem !important;
        line-height: 1.5 !important;
    }

    h1, h2, h3, h4 {
        font-family: 'Inter', sans-serif !important;
        letter-spacing: -0.02em !important;
        color: #F8FAFC !important;
        font-weight: 700 !important;
    }
    
    h1 { font-size: 1.95rem !important; }
    h2 { font-size: 1.45rem !important; }
    h3 { font-size: 1.20rem !important; }

    /* 3. Rajasthan Royals High-Performance Metric Cards */
    .metric-card {
        background: linear-gradient(145deg, #131F37 0%, #0C1527 100%) !important;
        border: 1px solid rgba(234, 26, 128, 0.22) !important;
        border-radius: 12px !important;
        padding: 16px 18px !important;
        margin-bottom: 12px !important;
        box-shadow: 0 4px 20px -2px rgba(0, 0, 0, 0.5), inset 0 1px 0 rgba(255, 255, 255, 0.05) !important;
        transition: transform 0.15s ease, border-color 0.15s ease !important;
    }
    
    .metric-card:hover {
        border-color: rgba(234, 26, 128, 0.5) !important;
        transform: translateY(-2px) !important;
    }
    
    .metric-label {
        font-size: 0.72rem !important;
        text-transform: uppercase !important;
        color: #94A3B8 !important;
        font-weight: 700 !important;
        letter-spacing: 0.08em !important;
        margin-bottom: 5px !important;
    }
    
    .metric-value {
        font-size: 1.85rem !important;
        font-weight: 800 !important;
        letter-spacing: -0.03em !important;
        color: #FFFFFF !important;
        line-height: 1.1 !important;
    }
    
    .metric-delta {
        font-size: 0.80rem !important;
        font-weight: 600 !important;
        margin-top: 5px !important;
        display: flex !important;
        align-items: center !important;
        gap: 4px !important;
    }
    
    .delta-pos { color: #34D399 !important; }
    .delta-neg { color: #F87171 !important; }
    .delta-neutral { color: #94A3B8 !important; }

    /* 4. Rajasthan Royals Glassmorphism Callout Box */
    .callout-box {
        background: rgba(14, 27, 54, 0.82) !important;
        border: 1px solid rgba(234, 26, 128, 0.35) !important;
        border-left: 4px solid #EA1A80 !important;
        padding: 14px 18px !important;
        border-radius: 8px !important;
        margin-bottom: 1.25rem !important;
        color: #E2E8F0 !important;
        font-size: 0.92rem !important;
        line-height: 1.6 !important;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3) !important;
    }
    
    .callout-box strong {
        color: #FFFFFF !important;
    }

    .disclaimer-banner {
        background: rgba(30, 41, 59, 0.7) !important;
        border: 1px solid rgba(148, 163, 184, 0.25) !important;
        border-left: 4px solid #3B82F6 !important;
        padding: 12px 16px !important;
        border-radius: 8px !important;
        margin-bottom: 1.25rem !important;
        color: #CBD5E1 !important;
        font-size: 0.86rem !important;
        line-height: 1.5 !important;
    }

    /* 5. Status Badges & Pills */
    .badge {
        display: inline-flex !important;
        align-items: center !important;
        padding: 4px 10px !important;
        border-radius: 9999px !important;
        font-size: 0.72rem !important;
        font-weight: 700 !important;
        letter-spacing: 0.05em !important;
        text-transform: uppercase !important;
        margin-right: 6px !important;
    }
    
    .badge-confirmed { background: rgba(59, 130, 246, 0.20) !important; color: #60A5FA !important; border: 1px solid rgba(96, 165, 250, 0.4) !important; }
    .badge-reported { background: rgba(245, 158, 11, 0.20) !important; color: #FBBF24 !important; border: 1px solid rgba(251, 191, 36, 0.4) !important; }
    .badge-unverified { background: rgba(148, 163, 184, 0.20) !important; color: #CBD5E1 !important; border: 1px solid rgba(203, 213, 225, 0.4) !important; }
    .badge-retired { background: rgba(239, 68, 68, 0.20) !important; color: #F87171 !important; border: 1px solid rgba(248, 113, 113, 0.4) !important; }

    /* 6. Sidebar Refinement */
    [data-testid="stSidebar"] {
        background-color: #070D1B !important;
        border-right: 1px solid rgba(255, 255, 255, 0.06) !important;
    }
    
    [data-testid="stSidebar"] [role="radiogroup"] label[data-checked="true"] {
        background: rgba(234, 26, 128, 0.12) !important;
        border-radius: 8px !important;
        border-left: 3px solid #EA1A80 !important;
    }

    /* 7. Tables & DataFrames */
    .stDataFrame {
        border-radius: 10px !important;
        overflow: hidden !important;
        border: 1px solid rgba(255, 255, 255, 0.10) !important;
        background: #0C1527 !important;
    }

    div[data-testid="stDataFrame"] {
        width: 100% !important;
    }
</style>
""", unsafe_allow_html=True)

# --- PATH & DATA LOADING HELPERS ---
BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "data"

@st.cache_data
def load_data():
    b10 = pd.read_csv(DATA_DIR / "final_top10_batters.csv")
    w10 = pd.read_csv(DATA_DIR / "final_top10_bowlers.csv")
    all_b = pd.read_csv(DATA_DIR / "all_candidate_batters.csv")
    all_w = pd.read_csv(DATA_DIR / "all_candidate_bowlers.csv")
    rr = pd.read_csv(DATA_DIR / "rr_squad_2026.csv")
    sources = pd.read_csv(DATA_DIR / "source_register_all.csv")
    waterfall = pd.read_csv(DATA_DIR / "waterfall.csv")
    anova = pd.read_csv(DATA_DIR / "anova.csv")
    
    with open(DATA_DIR / "player_narratives.json", "r", encoding="utf-8") as f:
        narratives = json.load(f)
        
    for df in [all_b, all_w]:
        if 'shrunk_wp_impact' not in df.columns and 'mean_shrunk_pwi' in df.columns:
            df['shrunk_wp_impact'] = df['mean_shrunk_pwi']
        if 'raw_pressure_lift' not in df.columns and 'mean_raw_lift' in df.columns:
            df['raw_pressure_lift'] = df['mean_raw_lift']
        if 'hp_balls' not in df.columns and 'mean_hp_balls' in df.columns:
            df['hp_balls'] = df['mean_hp_balls']

    # Attach standardized IPL 2027 status to b10 and w10
    b10['ipl_2027_status'] = b10['player_id'].astype(str).map(
        lambda pid: narratives.get('batters', {}).get(pid, {}).get('ipl_2027_status', 'Unverified')
    )
    w10['ipl_2027_status'] = w10['player_id'].astype(str).map(
        lambda pid: narratives.get('bowlers', {}).get(pid, {}).get('ipl_2027_status', 'Unverified')
    )
    b10['status_label'] = b10['player_id'].astype(str).map(
        lambda pid: narratives.get('batters', {}).get(pid, {}).get('status_label', 'UNVERIFIED')
    )
    w10['status_label'] = w10['player_id'].astype(str).map(
        lambda pid: narratives.get('bowlers', {}).get(pid, {}).get('status_label', 'UNVERIFIED')
    )

    # Standardize source register status categories (Confirmed, Reported, Unverified, Retired / Historical only)
    def map_src_status(row):
        stat = str(row.get('ipl_2027_availability_status', '')).lower()
        act = str(row.get('active_status', '')).lower()
        if 'retired' in act or 'retired' in stat or 'coaching' in act or 'coach' in act:
            return 'Retired / Historical only'
        if 'traded' in act or 'traded' in stat or 'trade' in stat:
            return 'Confirmed'
        if 'injured' in act or 'injury' in stat or 'rehab' in act or 'rehab' in stat:
            return 'Reported'
        return 'Unverified'

    sources['ipl_2027_status_category'] = sources.apply(map_src_status, axis=1)

    return b10, w10, all_b, all_w, rr, sources, waterfall, anova, narratives

b10, w10, all_b, all_w, rr, sources, waterfall, anova, narratives = load_data()

# --- STANDARDIZED PLOTLY RAJASTHAN ROYALS THEME HELPER ---
def apply_rr_plotly_theme(fig, title=None, height=390):
    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(12, 21, 39, 0)",
        plot_bgcolor="rgba(12, 21, 39, 0.45)",
        font=dict(family="Inter, -apple-system, sans-serif", size=12, color="#94A3B8"),
        title=dict(
            text=f"<b>{title}</b>" if title else "",
            font=dict(size=14, color="#F8FAFC", family="Inter, sans-serif"),
            x=0.0,
            xanchor="left"
        ) if title else None,
        margin=dict(l=20, r=20, t=40 if title else 20, b=30),
        height=height,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
            font=dict(size=11, color="#CBD5E1")
        ),
        xaxis=dict(gridcolor="rgba(255, 255, 255, 0.06)", zerolinecolor="rgba(255, 255, 255, 0.1)"),
        yaxis=dict(gridcolor="rgba(255, 255, 255, 0.06)", zerolinecolor="rgba(255, 255, 255, 0.1)")
    )
    return fig

# --- LEADERBOARD FORMATTING & COLUMN CONFIG HELPERS ---
def get_leaderboard_column_config(role="batter"):
    impact_title = "Shrunk Impact (r/100b)" if role == "batter" else "Defending Impact (r/24b)"
    impact_help = (
        "Empirical Bayes regularized impact: runs scored per 100 balls above context expectation"
        if role == "batter" else
        "Empirical Bayes regularized impact: runs saved per 24 balls below context expectation"
    )
    raw_lift_help = (
        "Unshrunk difference between high-pressure strike rate and normal baseline strike rate"
        if role == "batter" else
        "Unshrunk difference between normal baseline economy rate and high-pressure economy rate (runs saved/24b)"
    )
    
    cfg = {
        "Rank": st.column_config.NumberColumn(
            "Rank",
            help="Consensus V4 Multiverse Rank across 15,150 specifications",
            format="#%d"
        ),
        "Player Name": st.column_config.TextColumn(
            "Player Name",
            help="Audited player name (identity strictly keyed on player_id)"
        ),
        "Player ID": st.column_config.NumberColumn(
            "Player ID",
            help="Canonical player_id resolving homonyms (e.g. Abdul Samad, Rashid Khan)",
            format="%d"
        ),
        "Tier": st.column_config.TextColumn(
            "Tier",
            help="Model V4 Robustness Tier (Tier 1 Core Consensus, Tier 2 Strong Contender, Tier 3 Context-Dependent)"
        ),
        "Top-10 Inclusion %": st.column_config.TextColumn(
            "Top-10 Inclusion %",
            help="Percentage of valid model specifications (out of 15,150) in which the player finished inside the top 10. (Descriptive historical frequency across model choices, NOT a future-success probability)"
        ),
        "Candidate Eligibility %": st.column_config.TextColumn(
            "Candidate Eligibility %",
            help="Percentage of specifications in which the player met minimum sample volume thresholds to be evaluated (distinct from top-10 inclusion)"
        ),
        impact_title: st.column_config.TextColumn(
            impact_title,
            help=impact_help
        ),
        "Raw Pressure Lift": st.column_config.TextColumn(
            "Raw Pressure Lift",
            help=raw_lift_help
        ),
        "HP Balls": st.column_config.NumberColumn(
            "HP Balls",
            help="Total deliveries faced or bowled under high-pressure leverage conditions in the primary dataset",
            format="%d"
        ),
        "Bootstrap Valid Draws": st.column_config.TextColumn(
            "Bootstrap Valid Draws",
            help="Number of resample iterations (out of 1,000 stratified match bootstrap draws) where the player was eligible"
        ),
        "Bootstrap 90% CI": st.column_config.TextColumn(
            "Bootstrap 90% CI",
            help="90% bootstrap rank confidence interval [5th percentile, 95th percentile] across 1,000 resamples"
        ),
        "IPL 2027 Status": st.column_config.TextColumn(
            "IPL 2027 Status",
            help="Real-world external market status: Confirmed (official trade), Reported (medical/rehab), Unverified (pending formal BCCI list), or Retired / Historical only"
        )
    }
    return cfg

def prepare_display_batters(df):
    d = pd.DataFrame()
    d['Rank'] = df['final_rank'].astype(int)
    d['Player Name'] = df['player_name']
    d['Player ID'] = df['player_id'].astype(int)
    d['Tier'] = df['tier']
    d['Top-10 Inclusion %'] = (df['top10_freq'] * 100).round(1).astype(str) + "%"
    d['Candidate Eligibility %'] = (df['elig_share'] * 100).round(1).astype(str) + "%"
    d['Shrunk Impact (r/100b)'] = df['shrunk_wp_impact'].apply(lambda x: f"+{x:.1f}")
    d['Raw Pressure Lift'] = df['raw_lift'].apply(lambda x: f"+{x:.1f}" if x >= 0 else f"{x:.1f}")
    d['HP Balls'] = df['hp_balls'].astype(int)
    d['Bootstrap Valid Draws'] = df['valid_eligible_iters'].astype(int).astype(str) + " / 1,000"
    d['Bootstrap 90% CI'] = "[" + df['boot_p05_rank'].astype(int).astype(str) + ", " + df['boot_p95_rank'].astype(int).astype(str) + "]"
    d['IPL 2027 Status'] = df['ipl_2027_status']
    return d

def prepare_display_bowlers(df):
    d = pd.DataFrame()
    d['Rank'] = df['final_rank'].astype(int)
    d['Player Name'] = df['player_name']
    d['Player ID'] = df['player_id'].astype(int)
    d['Tier'] = df['tier']
    d['Top-10 Inclusion %'] = (df['top10_freq'] * 100).round(1).astype(str) + "%"
    d['Candidate Eligibility %'] = (df['elig_share'] * 100).round(1).astype(str) + "%"
    d['Defending Impact (r/24b)'] = df['shrunk_wp_impact'].apply(lambda x: f"+{x:.2f}")
    d['Raw Pressure Lift'] = df['raw_lift'].apply(lambda x: f"+{x:.2f}" if x >= 0 else f"{x:.2f}")
    d['HP Balls'] = df['hp_balls'].astype(int)
    d['Bootstrap Valid Draws'] = df['valid_eligible_iters'].astype(int).astype(str) + " / 1,000"
    d['Bootstrap 90% CI'] = "[" + df['boot_p05_rank'].astype(int).astype(str) + ", " + df['boot_p95_rank'].astype(int).astype(str) + "]"
    d['IPL 2027 Status'] = df['ipl_2027_status']
    return d

# --- SIDEBAR NAVIGATION ---
st.sidebar.image("https://img.icons8.com/color/96/cricket.png", width=64)
st.sidebar.title("SupeRR Selector")
st.sidebar.caption("Season 2 | V4 Multiverse Analysis")

nav_choice = st.sidebar.radio(
    "Navigation Menu",
    [
        "🏠 Overview & Executive Summary",
        "🏏 Top 10 Batting Leaderboard",
        "🎯 Top 10 Bowling Leaderboard",
        "🔍 Searchable Player Profiles",
        "⚖️ Player Comparison Tool",
        "📊 Multiverse & Bootstrap Stability",
        "🛡️ Rajasthan Royals 2026 Audit",
        "💼 IPL 2027 Recruitment Actionability",
        "🔬 Methodology & Governance",
        "📥 Downloads & Data Export"
    ]
)

st.sidebar.markdown("---")
st.sidebar.markdown("""
**Data Governance:**
- Baseline: **Model V4 Multiverse**
- Specs: **15,150 per role**
- Matches: **837 (367 IPL, 470 T20I)**
- Deliveries: **193,988 primary**
- Checksums: **39/39 Verified**
""")

st.sidebar.info("⚠️ **Disclaimer:** This is an independent participant research project based on historical cricket data. It is not an official Rajasthan Royals product or recruitment decision.")
st.sidebar.caption("Rajasthan Royals Analytical Recruitment Suite")

# ==============================================================================
# 1. OVERVIEW & EXECUTIVE SUMMARY
# ==============================================================================
if nav_choice == "🏠 Overview & Executive Summary":
    st.markdown('<div class="main-title">SupeRR Selector Season 2: Cricket Intelligence</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-title">Evaluating T20 Performance Under Pressure: Multiverse Specification-Curve Analysis &amp; Rajasthan Royals Recruitment Architecture</div>', unsafe_allow_html=True)
    
    # Disclaimer Banner
    st.markdown("""
    <div class="disclaimer-banner">
        <strong>Academic &amp; Participant Research Disclaimer:</strong> This is an independent participant research project based on historical cricket data. It is not an official Rajasthan Royals product or recruitment decision.
    </div>
    """, unsafe_allow_html=True)

    # KPI Row
    kpi1, kpi2, kpi3, kpi4, kpi5 = st.columns(5)
    with kpi1:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-label">Primary Matches</div>
            <div class="metric-value">837</div>
            <div class="metric-delta delta-neutral">367 IPL + 470 T20I</div>
        </div>
        """, unsafe_allow_html=True)
    with kpi2:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-label">Primary Deliveries</div>
            <div class="metric-value">193,988</div>
            <div class="metric-delta delta-neutral">185,692 Legal Balls</div>
        </div>
        """, unsafe_allow_html=True)
    with kpi3:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-label">Multiverse Specs</div>
            <div class="metric-value">15,150</div>
            <div class="metric-delta delta-pos">Per Discipline Grid</div>
        </div>
        """, unsafe_allow_html=True)
    with kpi4:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-label">Bootstrap Draws</div>
            <div class="metric-value">1,000</div>
            <div class="metric-delta delta-pos">Stratified Match Clustered</div>
        </div>
        """, unsafe_allow_html=True)
    with kpi5:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-label">Selected Leaders</div>
            <div class="metric-value">10 + 10</div>
            <div class="metric-delta delta-neutral">Batters &amp; Bowlers</div>
        </div>
        """, unsafe_allow_html=True)
        
    st.markdown("""
    <div class="callout-box">
        <strong>Executive Operational Mandate:</strong> This intelligence platform provides an audited, reproducible, and scientifically rigorous evaluation of player performance under high leverage in T20 cricket. Built exclusively on the verified <strong>Model V4 Multiverse</strong> architecture, it assesses ranking sensitivity across analytical specifications across 15,150 model specifications and leave-player-out empirical Bayes baselines.
    </div>
    """, unsafe_allow_html=True)
    
    # Leaderboard Presentation Selection
    st.markdown("---")
    st.markdown("### 🏆 V4 Multiverse Consensus Leaderboards Under Pressure")
    st.markdown("""
    *Statistical Definition:* **Top-10 Inclusion %** is the percentage of valid model specifications (out of 15,150) in which the player ranked in the top 10. It measures historical ranking robustness across researcher assumptions, **not a future-success probability**. **Candidate Eligibility %** reflects meeting minimum volume thresholds.
    """)

    view_layout = st.radio(
        "Leaderboard View Layout",
        ["Stacked Full-Width Tables (Recommended for Desktop)", "Tabbed View (Accessible Tab Switching)"],
        horizontal=True,
        label_visibility="collapsed"
    )

    disp_b = prepare_display_batters(b10)
    disp_w = prepare_display_bowlers(w10)

    if view_layout.startswith("Stacked"):
        # Stacked Full-Width Section 1: Batters
        st.markdown("#### 🏏 Top 10 Batters (V4 Multiverse Consensus)")
        st.caption("Pre-registered decision threshold: Multiverse Top-10 Inclusion Frequency ≥ 45% across 15,150 specifications.")
        st.dataframe(
            disp_b,
            hide_index=True,
            use_container_width=True,
            column_config=get_leaderboard_column_config("batter")
        )
        
        st.markdown("<br>", unsafe_allow_html=True)

        # Stacked Full-Width Section 2: Bowlers
        st.markdown("#### 🎯 Top 10 Bowlers (V4 Multiverse Consensus)")
        st.caption("Pre-registered decision threshold: Multiverse Top-10 Inclusion Frequency ≥ 25% across 15,150 specifications.")
        st.dataframe(
            disp_w,
            hide_index=True,
            use_container_width=True,
            column_config=get_leaderboard_column_config("bowler")
        )
    else:
        tab_b, tab_w = st.tabs(["🏏 Top 10 Batters (Multiverse Consensus)", "🎯 Top 10 Bowlers (Multiverse Consensus)"])
        with tab_b:
            st.caption("Pre-registered decision threshold: Multiverse Top-10 Inclusion Frequency ≥ 45% across 15,150 specifications.")
            st.dataframe(
                disp_b,
                hide_index=True,
                use_container_width=True,
                column_config=get_leaderboard_column_config("batter")
            )
        with tab_w:
            st.caption("Pre-registered decision threshold: Multiverse Top-10 Inclusion Frequency ≥ 25% across 15,150 specifications.")
            st.dataframe(
                disp_w,
                hide_index=True,
                use_container_width=True,
                column_config=get_leaderboard_column_config("bowler")
            )
        
    st.markdown("---")
    
    # Core Findings
    st.subheader("📌 Three Core Empirical Discoveries")
    f1, f2, f3 = st.columns(3)
    with f1:
        st.markdown("""
        **1. Finite Sample Size vs True Skill**  
        Raw strike-rate or economy splits under pressure are heavily polluted by small sample noise. Empirical Bayes shrinkage and leave-player-out baselines reduce ranking variance by over **60%**, pulling volatile small-sample outliers toward cell priors.
        """)
    with f2:
        st.markdown("""
        **2. Asymmetry of Pressure Lift**  
        Pressure impact is highly asymmetric. Bowlers generally find run-prevention easier as batters take desperation risks (+0.5 to +3.0 runs saved/24b). Batters who genuinely elevate under high required run rates (Shashank Singh, Naman Dhir) are exceptionally rare market commodities.
        """)
    with f3:
        st.markdown("""
        **3. Descriptive vs Predictive Reality**  
        Walk-forward temporal testing (2022–2024 $\to$ 2025–2026) demonstrates that batting pressure splits are **descriptive, not predictive** ($r = 0.05$). Bowler rankings show moderate stability ($r = 0.26$). Rankings document historical execution, not guaranteed future outcomes.
        """)
        
    # Delivery Waterfall Reconciliation
    with st.expander("🔍 Audited Primary Scope Delivery Waterfall (Exact Cricket Accounting)"):
        wf_display = waterfall.copy()
        for col in ['Matches', 'Deliveries', 'Legal_Balls']:
            if col in wf_display.columns:
                wf_display[col] = wf_display[col].apply(lambda x: f"{x:+,}" if x < 0 else f"{x:,}")
        st.dataframe(wf_display, hide_index=True, use_container_width=True)
        st.caption("Net arithmetic: 200,999 raw - 6,985 emerging - 26 remaining IPL/T20I Super Overs = 193,988 primary deliveries (185,692 legal balls).")

# ==============================================================================
# 2. TOP 10 BATTING LEADERBOARD
# ==============================================================================
elif nav_choice == "🏏 Top 10 Batting Leaderboard":
    st.markdown('<div class="main-title">Top 10 Batting Leaderboard Under Pressure</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-title">Pre-Registered Decision Rule: Multiverse Top-10 Frequency ≥ 45% | Shrunk Win-Probability Impact &amp; Lift</div>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="callout-box">
        <strong>Statistical Definition Standard:</strong>
        <ul>
            <li><strong>Top-10 Inclusion %:</strong> Percentage of valid specifications (out of 15,150) in which the batter ranked in the top 10. This is an analytical sensitivity metric reflecting specification stability, <em>not a future-success probability</em>.</li>
            <li><strong>Candidate Eligibility %:</strong> Share of specifications where the player met minimum ball volume cutoffs.</li>
            <li><strong>Historical Benchmark vs Actionability:</strong> Inactive or retired players (e.g. Dinesh Karthik, Andre Russell) are preserved as historical analytical benchmarks.</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

    # Filter controls
    col_f1, col_f2 = st.columns([1, 3])
    with col_f1:
        selected_tier = st.multiselect(
            "Filter by Tier",
            options=b10['tier'].unique().tolist(),
            default=b10['tier'].unique().tolist()
        )
    
    df_filtered_b = b10[b10['tier'].isin(selected_tier)].copy()
    disp_filtered_b = prepare_display_batters(df_filtered_b)
    
    # Detailed Table
    st.dataframe(
        disp_filtered_b,
        hide_index=True,
        use_container_width=True,
        column_config=get_leaderboard_column_config("batter")
    )
    
    st.markdown("<br>", unsafe_allow_html=True)

    # Interactive Visualizations
    col_chart1, col_chart2 = st.columns(2)
    with col_chart1:
        fig1 = px.scatter(
            b10,
            x='shrunk_wp_impact',
            y='top10_freq',
            size='hp_balls',
            color='tier',
            color_discrete_map={
                'Tier 1 (Core Consensus)': '#F59E0B',
                'Tier 2 (Strong Contender)': '#EA1A80',
                'Tier 3 (Context-Dependent)': '#94A3B8'
            },
            hover_name='player_name',
            hover_data={'player_id': True, 'final_rank': True, 'hp_sr': ':.1f', 'raw_lift': ':.1f'},
            labels={
                'shrunk_wp_impact': 'Shrunk High-Pressure Impact (runs/100b)',
                'top10_freq': 'Multiverse Top-10 Frequency',
                'tier': 'Tier'
            }
        )
        fig1.update_layout(yaxis_tickformat='.0%')
        apply_rr_plotly_theme(fig1, title="Multiverse Top-10 Consensus vs Impact (Size = HP Balls)")
        st.plotly_chart(fig1, use_container_width=True)
        
    with col_chart2:
        fig2 = go.Figure()
        fig2.add_trace(go.Bar(
            y=b10['player_name'],
            x=b10['shrunk_norm_impact'],
            name='Normal Baseline Impact',
            orientation='h',
            marker_color='#334E68'
        ))
        fig2.add_trace(go.Bar(
            y=b10['player_name'],
            x=b10['shrunk_wp_impact'],
            name='High-Pressure Impact',
            orientation='h',
            marker_color='#EA1A80'
        ))
        fig2.update_layout(
            barmode='group',
            yaxis=dict(autorange="reversed"),
            xaxis_title="Impact Metric (runs/100 balls above context)"
        )
        apply_rr_plotly_theme(fig2, title="Performance Lift: HP Impact vs Normal Baseline")
        st.plotly_chart(fig2, use_container_width=True)

# ==============================================================================
# 3. TOP 10 BOWLING LEADERBOARD
# ==============================================================================
elif nav_choice == "🎯 Top 10 Bowling Leaderboard":
    st.markdown('<div class="main-title">Top 10 Bowling Leaderboard Under Pressure</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-title">Pre-Registered Decision Rule: Multiverse Top-10 Frequency ≥ 25% | Defending Shrunk Impact &amp; Dot/Wicket Suppression</div>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="callout-box">
        <strong>Statistical Definition Standard:</strong>
        <ul>
            <li><strong>Top-10 Inclusion %:</strong> Percentage of valid specifications (out of 15,150) in which the bowler ranked in the top 10. Reflects robustness across model specifications, <em>not future predictability</em>.</li>
            <li><strong>Defending Impact:</strong> Empirical Bayes runs saved per 24 balls against match-context baseline expectation.</li>
            <li><strong>Market Status:</strong> Nathan Ellis and Arshdeep Singh represent Confirmed Trades; Pathirana is under Reported Rehabilitation; Bhuvneshwar Kumar is a Retired Benchmark.</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

    # Filter controls
    col_f1, col_f2 = st.columns([1, 3])
    with col_f1:
        selected_tier_w = st.multiselect(
            "Filter by Tier",
            options=w10['tier'].unique().tolist(),
            default=w10['tier'].unique().tolist()
        )
    
    df_filtered_w = w10[w10['tier'].isin(selected_tier_w)].copy()
    disp_filtered_w = prepare_display_bowlers(df_filtered_w)
    
    # Detailed Table
    st.dataframe(
        disp_filtered_w,
        hide_index=True,
        use_container_width=True,
        column_config=get_leaderboard_column_config("bowler")
    )
    
    st.markdown("<br>", unsafe_allow_html=True)

    # Interactive Visualizations
    col_chart1, col_chart2 = st.columns(2)
    with col_chart1:
        fig1_w = px.scatter(
            w10,
            x='shrunk_wp_impact',
            y='top10_freq',
            size='hp_balls',
            color='tier',
            color_discrete_map={
                'Tier 1 (Core Consensus)': '#F59E0B',
                'Tier 2 (Strong Contender)': '#EA1A80',
                'Tier 3 (Context-Dependent)': '#94A3B8'
            },
            hover_name='player_name',
            hover_data={'player_id': True, 'final_rank': True, 'hp_er': ':.2f', 'raw_lift': ':.2f'},
            labels={
                'shrunk_wp_impact': 'Defending Shrunk Impact (runs saved/24b)',
                'top10_freq': 'Multiverse Top-10 Frequency',
                'tier': 'Tier'
            }
        )
        fig1_w.update_layout(yaxis_tickformat='.0%')
        apply_rr_plotly_theme(fig1_w, title="Multiverse Consensus vs Defending Impact (Size = HP Balls)")
        st.plotly_chart(fig1_w, use_container_width=True)
        
    with col_chart2:
        fig2_w = go.Figure()
        fig2_w.add_trace(go.Bar(
            y=w10['player_name'],
            x=w10['shrunk_norm_impact'],
            name='Normal Baseline Saved/24b',
            orientation='h',
            marker_color='#334E68'
        ))
        fig2_w.add_trace(go.Bar(
            y=w10['player_name'],
            x=w10['shrunk_wp_impact'],
            name='High-Pressure Saved/24b',
            orientation='h',
            marker_color='#10B981'
        ))
        fig2_w.update_layout(
            barmode='group',
            yaxis=dict(autorange="reversed"),
            xaxis_title="Runs Saved per 24 balls against cell expectation"
        )
        apply_rr_plotly_theme(fig2_w, title="Defensive Suppression: HP Impact vs Normal Baseline")
        st.plotly_chart(fig2_w, use_container_width=True)

# ==============================================================================
# 4. SEARCHABLE PLAYER PROFILES
# ==============================================================================
elif nav_choice == "🔍 Searchable Player Profiles":
    st.markdown('<div class="main-title">Interactive Player Intelligence Dossier</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-title">Detailed Performance Breakdown, Empirical Baselines &amp; Tactical Scouting Context</div>', unsafe_allow_html=True)
    
    col_p1, col_p2 = st.columns([1, 2])
    with col_p1:
        discipline = st.radio("Select Discipline", ["Batting", "Bowling"], horizontal=True)
        
    with col_p2:
        if discipline == "Batting":
            player_list = b10['player_name'].tolist() + [p for p in all_b['player_name'].dropna().unique() if p not in b10['player_name'].tolist()]
            selected_player_name = st.selectbox("Search or Select Player", player_list[:50])
            player_data = all_b[all_b['player_name'] == selected_player_name].iloc[0]
            is_top10 = selected_player_name in b10['player_name'].tolist()
            if is_top10:
                top10_meta = b10[b10['player_name'] == selected_player_name].iloc[0]
        else:
            player_list = w10['player_name'].tolist() + [p for p in all_w['player_name'].dropna().unique() if p not in w10['player_name'].tolist()]
            selected_player_name = st.selectbox("Search or Select Player", player_list[:50])
            player_data = all_w[all_w['player_name'] == selected_player_name].iloc[0]
            is_top10 = selected_player_name in w10['player_name'].tolist()
            if is_top10:
                top10_meta = w10[w10['player_name'] == selected_player_name].iloc[0]

    st.markdown("---")
    
    # Player Header Banner
    pid = int(player_data['player_id'])
    role_key = 'batters' if discipline == "Batting" else 'bowlers'
    narrative = narratives.get(role_key, {}).get(str(pid), narratives.get(role_key, {}).get(pid, {}))
    
    status_cat = narrative.get('ipl_2027_status', 'Unverified')
    badge_class = {
        'Confirmed': 'badge-confirmed',
        'Reported': 'badge-reported',
        'Unverified': 'badge-unverified',
        'Retired / Historical only': 'badge-retired'
    }.get(status_cat, 'badge-unverified')

    col_hdr1, col_hdr2 = st.columns([2, 1])
    with col_hdr1:
        st.markdown(f"### {selected_player_name} (`player_id`: {pid})")
        st.markdown(f"**Classification:** `{narrative.get('classification', 'Audited T20 Candidate')}` | **Role:** {narrative.get('tactical_role', 'Specialist')}")
        st.markdown(f"**IPL 2026 Team:** {narrative.get('ipl_2026_team', 'Audited Pool')} | **IPL 2027 Market Status:** <span class='badge {badge_class}'>{status_cat.upper()}</span>", unsafe_allow_html=True)
    with col_hdr2:
        if is_top10:
            st.metric("Consensus V4 Rank", f"#{int(top10_meta['final_rank'])}", delta=f"{top10_meta['top10_freq']*100:.1f}% Top-10 Inclusion")
        else:
            st.metric("Multiverse Rank", f"#{int(player_data.get('median_rank', 999))}", delta="Outside Top 10")
            
    # Metrics Row 1: Primary Leverage Metrics
    if discipline == "Batting":
        m1, m2, m3, m4, m5 = st.columns(5)
        with m1:
            st.metric("Consensus Rank", f"#{int(top10_meta['final_rank'])}" if is_top10 else f"#{int(player_data.get('median_rank', 999))}")
        with m2:
            st.metric("Robustness Tier", str(player_data.get('tier', 'Candidate Pool')))
        with m3:
            st.metric("Top-10 Inclusion %", f"{player_data['top10_freq']*100:.1f}%", help="Percentage of valid model specifications where player ranked in top 10 (historical specification frequency, NOT future probability)")
        with m4:
            st.metric("Candidate Elig %", f"{player_data['elig_share']*100:.1f}%", help="Percentage of specifications meeting volume criteria")
        with m5:
            st.metric("HP Balls Faced", f"{int(player_data['hp_balls'])} b", help="Total deliveries faced under high leverage")
            
        m6, m7, m8, m9, m10 = st.columns(5)
        with m6:
            st.metric("Shrunk Impact", f"+{player_data['shrunk_wp_impact']:.1f} r/100b")
        with m7:
            st.metric("Raw Pressure Lift", f"{player_data['raw_pressure_lift']:+.1f} r/100b")
        with m8:
            st.metric("HP Strike Rate", f"{player_data['hp_sr']:.1f}", delta=f"{player_data['hp_sr'] - player_data['norm_sr']:.1f} vs Normal")
        with m9:
            valid_draws = int(player_data.get('valid_eligible_iters', 1000)) if pd.notna(player_data.get('valid_eligible_iters')) else 1000
            st.metric("Bootstrap Valid Draws", f"{valid_draws} / 1,000")
        with m10:
            if is_top10:
                st.metric("Bootstrap 90% CI", f"[{int(top10_meta['boot_p05_rank'])}, {int(top10_meta['boot_p95_rank'])}]")
            else:
                st.metric("Bootstrap 90% CI", "Evaluated")
    else:
        m1, m2, m3, m4, m5 = st.columns(5)
        with m1:
            st.metric("Consensus Rank", f"#{int(top10_meta['final_rank'])}" if is_top10 else f"#{int(player_data.get('median_rank', 999))}")
        with m2:
            st.metric("Robustness Tier", str(player_data.get('tier', 'Candidate Pool')))
        with m3:
            st.metric("Top-10 Inclusion %", f"{player_data['top10_freq']*100:.1f}%", help="Percentage of valid specifications where bowler ranked in top 10 (descriptive historical frequency, NOT future probability)")
        with m4:
            st.metric("Candidate Elig %", f"{player_data['elig_share']*100:.1f}%", help="Percentage of specifications meeting volume criteria")
        with m5:
            st.metric("HP Balls Bowled", f"{int(player_data['hp_balls'])} b", help="Total deliveries bowled under high leverage")
            
        m6, m7, m8, m9, m10 = st.columns(5)
        with m6:
            st.metric("Defending Impact", f"+{player_data['shrunk_wp_impact']:.2f} r/24b")
        with m7:
            st.metric("Raw Pressure Lift", f"{player_data['raw_pressure_lift']:+.2f} r/24b")
        with m8:
            st.metric("HP Economy Rate", f"{player_data['hp_er']:.2f}", delta=f"{player_data['norm_er'] - player_data['hp_er']:+.2f} vs Normal", delta_color="inverse")
        with m9:
            valid_draws = int(player_data.get('valid_eligible_iters', 1000)) if pd.notna(player_data.get('valid_eligible_iters')) else 1000
            st.metric("Bootstrap Valid Draws", f"{valid_draws} / 1,000")
        with m10:
            if is_top10:
                st.metric("Bootstrap 90% CI", f"[{int(top10_meta['boot_p05_rank'])}, {int(top10_meta['boot_p95_rank'])}]")
            else:
                st.metric("Bootstrap 90% CI", "Evaluated")
                
    st.markdown("---")
    
    # Qualitative & Tactical Narrative
    col_txt1, col_txt2 = st.columns(2)
    with col_txt1:
        st.subheader("📋 Empirical Profile & Performance Summary")
        st.write(narrative.get('profile_summary', 'Detailed statistical profile compiled from Model V4 Multiverse specification-curve evaluations.'))
    with col_txt2:
        st.subheader("🛡️ Rajasthan Royals Tactical Recruitment Fit")
        st.write(narrative.get('rr_fit', 'Evaluated against Rajasthan Royals 2026 phase deficits and squad balance.'))

# ==============================================================================
# 5. PLAYER COMPARISON TOOL
# ==============================================================================
elif nav_choice == "⚖️ Player Comparison Tool":
    st.markdown('<div class="main-title">Head-to-Head Player Comparison</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-title">Compare 2 to 4 Players Side-by-Side Across Core Pressure Metrics</div>', unsafe_allow_html=True)
    
    disc_comp = st.radio("Discipline for Comparison", ["Batting", "Bowling"], horizontal=True)
    
    if disc_comp == "Batting":
        options = b10['player_name'].tolist() + [p for p in all_b['player_name'].dropna().unique() if p not in b10['player_name'].tolist()]
        default_picks = ["Shashank Singh", "Tim David", "Naman Dhir"]
        selected_players = st.multiselect("Select 2 to 4 Players", options, default=default_picks, max_selections=4)
        comp_df = all_b[all_b['player_name'].isin(selected_players)].copy()
        
        if len(selected_players) >= 2:
            st.subheader("Direct Metrics Comparison Matrix")
            metrics_table = comp_df[[
                'player_name', 'player_id', 'tier', 'final_rank', 'hp_sr', 'norm_sr', 'hp_avg', 'shrunk_wp_impact', 
                'raw_pressure_lift', 'hp_balls', 'top10_freq', 'elig_share', 'valid_eligible_iters'
            ]].copy()
            metrics_table['final_rank'] = metrics_table['final_rank'].apply(lambda x: f"#{int(x)}" if pd.notna(x) else "Pool")
            metrics_table['top10_freq'] = (metrics_table['top10_freq'] * 100).round(1).astype(str) + "%"
            metrics_table['elig_share'] = (metrics_table['elig_share'] * 100).round(1).astype(str) + "%"
            metrics_table['shrunk_wp_impact'] = metrics_table['shrunk_wp_impact'].apply(lambda x: f"+{x:.1f} r/100b")
            metrics_table['raw_pressure_lift'] = metrics_table['raw_pressure_lift'].apply(lambda x: f"{x:+.1f} r/100b")
            metrics_table['hp_sr'] = metrics_table['hp_sr'].round(1).astype(str)
            metrics_table['norm_sr'] = metrics_table['norm_sr'].round(1).astype(str)
            metrics_table['hp_avg'] = metrics_table['hp_avg'].round(1).astype(str)
            metrics_table['hp_balls'] = metrics_table['hp_balls'].round(0).astype(int).astype(str) + " b"
            metrics_table['valid_eligible_iters'] = metrics_table['valid_eligible_iters'].fillna(1000).astype(int).astype(str) + " / 1,000"
            
            # Map IPL status
            metrics_table['IPL 2027 Status'] = metrics_table['player_id'].astype(str).map(
                lambda pid: narratives.get('batters', {}).get(pid, {}).get('ipl_2027_status', 'Unverified')
            )

            metrics_table.columns = [
                'Player Name', 'Player ID', 'Robustness Tier', 'Consensus Rank', 'HP Strike Rate', 'Normal SR', 'HP Avg', 
                'Shrunk Impact', 'Raw Lift', 'HP Balls', 'Top-10 Inclusion %', 'Candidate Eligibility %', 'Bootstrap Valid Draws', 'IPL 2027 Status'
            ]
            
            comp_display = metrics_table.set_index('Player Name').T
            comp_display.columns.name = "Metric"
            st.dataframe(comp_display, use_container_width=True)
            
            # Grouped Bar Comparison
            fig_comp = go.Figure()
            colors = ['#EA1A80', '#3B82F6', '#F59E0B', '#10B981']
            for i, p in enumerate(selected_players):
                p_row = comp_df[comp_df['player_name'] == p].iloc[0]
                fig_comp.add_trace(go.Bar(
                    name=p,
                    x=['HP Strike Rate', 'Normal SR', 'Shrunk Impact (r/100b)', 'Raw Lift (r/100b)'],
                    y=[p_row['hp_sr'], p_row['norm_sr'], p_row['shrunk_wp_impact'], p_row['raw_pressure_lift']],
                    marker_color=colors[i % len(colors)]
                ))
            fig_comp.update_layout(barmode='group')
            apply_rr_plotly_theme(fig_comp, title="Key Rate & Impact Metrics Comparison")
            st.plotly_chart(fig_comp, use_container_width=True)
        else:
            st.warning("Please select at least 2 players to compare.")
    else:
        options_w = w10['player_name'].tolist() + [p for p in all_w['player_name'].dropna().unique() if p not in w10['player_name'].tolist()]
        default_picks_w = ["Sunil Narine", "Jasprit Bumrah", "Nathan Ellis"]
        selected_players_w = st.multiselect("Select 2 to 4 Players", options_w, default=default_picks_w, max_selections=4)
        comp_df_w = all_w[all_w['player_name'].isin(selected_players_w)].copy()
        
        if len(selected_players_w) >= 2:
            st.subheader("Direct Metrics Comparison Matrix")
            metrics_table_w = comp_df_w[[
                'player_name', 'player_id', 'tier', 'final_rank', 'hp_er', 'norm_er', 'hp_dot_pct', 'shrunk_wp_impact', 
                'raw_pressure_lift', 'hp_balls', 'top10_freq', 'elig_share', 'valid_eligible_iters'
            ]].copy()
            metrics_table_w['final_rank'] = metrics_table_w['final_rank'].apply(lambda x: f"#{int(x)}" if pd.notna(x) else "Pool")
            metrics_table_w['top10_freq'] = (metrics_table_w['top10_freq'] * 100).round(1).astype(str) + "%"
            metrics_table_w['elig_share'] = (metrics_table_w['elig_share'] * 100).round(1).astype(str) + "%"
            metrics_table_w['shrunk_wp_impact'] = metrics_table_w['shrunk_wp_impact'].apply(lambda x: f"+{x:.2f} r/24b")
            metrics_table_w['raw_pressure_lift'] = metrics_table_w['raw_pressure_lift'].apply(lambda x: f"{x:+.2f} r/24b")
            metrics_table_w['hp_er'] = metrics_table_w['hp_er'].round(2).astype(str)
            metrics_table_w['norm_er'] = metrics_table_w['norm_er'].round(2).astype(str)
            metrics_table_w['hp_dot_pct'] = metrics_table_w['hp_dot_pct'].round(1).astype(str) + "%"
            metrics_table_w['hp_balls'] = metrics_table_w['hp_balls'].round(0).astype(int).astype(str) + " b"
            metrics_table_w['valid_eligible_iters'] = metrics_table_w['valid_eligible_iters'].fillna(1000).astype(int).astype(str) + " / 1,000"
            
            # Map IPL status
            metrics_table_w['IPL 2027 Status'] = metrics_table_w['player_id'].astype(str).map(
                lambda pid: narratives.get('bowlers', {}).get(pid, {}).get('ipl_2027_status', 'Unverified')
            )

            metrics_table_w.columns = [
                'Player Name', 'Player ID', 'Robustness Tier', 'Consensus Rank', 'HP Economy', 'Normal ER', 'HP Dot %', 
                'Defending Impact', 'Raw Lift', 'HP Balls', 'Top-10 Inclusion %', 'Candidate Eligibility %', 'Bootstrap Valid Draws', 'IPL 2027 Status'
            ]
            
            comp_display_w = metrics_table_w.set_index('Player Name').T
            comp_display_w.columns.name = "Metric"
            st.dataframe(comp_display_w, use_container_width=True)
            
            # Grouped Bar Comparison
            fig_comp_w = go.Figure()
            colors = ['#EA1A80', '#3B82F6', '#F59E0B', '#10B981']
            for i, p in enumerate(selected_players_w):
                p_row_w = comp_df_w[comp_df_w['player_name'] == p].iloc[0]
                fig_comp_w.add_trace(go.Bar(
                    name=p,
                    x=['HP Economy Rate', 'Normal ER', 'Defending Impact (r/24b)', 'Raw Lift (r/24b)'],
                    y=[p_row_w['hp_er'], p_row_w['norm_er'], p_row_w['shrunk_wp_impact'], p_row_w['raw_pressure_lift']],
                    marker_color=colors[i % len(colors)]
                ))
            fig_comp_w.update_layout(barmode='group')
            apply_rr_plotly_theme(fig_comp_w, title="Key Economy & Run Suppression Metrics Comparison")
            st.plotly_chart(fig_comp_w, use_container_width=True)
        else:
            st.warning("Please select at least 2 players to compare.")

# ==============================================================================
# 6. MULTIVERSE & BOOTSTRAP STABILITY
# ==============================================================================
elif nav_choice == "📊 Multiverse & Bootstrap Stability":
    st.markdown('<div class="main-title">Multiverse &amp; Bootstrap Robustness Audit</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-title">15,150 Specifications Evaluated per Role | 1,000-Draw Stratified Match Bootstrap</div>', unsafe_allow_html=True)
    
    col_b1, col_b2 = st.columns(2)
    with col_b1:
        fig_ci_b = go.Figure()
        fig_ci_b.add_trace(go.Scatter(
            x=b10['median_rank'],
            y=b10['player_name'],
            mode='markers',
            marker=dict(color='#EA1A80', size=11, line=dict(color='#FFFFFF', width=1)),
            error_x=dict(
                type='data',
                symmetric=False,
                array=b10['boot_p95_rank'] - b10['median_rank'],
                arrayminus=b10['median_rank'] - b10['boot_p05_rank'],
                color='#F472B6',
                thickness=2.5,
                width=6
            ),
            hovertext="Median: " + b10['median_rank'].astype(str) + " [CI: " + b10['boot_p05_rank'].astype(int).astype(str) + ", " + b10['boot_p95_rank'].astype(int).astype(str) + "]"
        ))
        fig_ci_b.update_layout(
            yaxis=dict(autorange="reversed"),
            xaxis_title="Bootstrap Rank (Lower = Better)"
        )
        apply_rr_plotly_theme(fig_ci_b, title="🏏 Batters 90% Rank Confidence Intervals across 1,000 Resamples")
        st.plotly_chart(fig_ci_b, use_container_width=True)
        
    with col_b2:
        fig_ci_w = go.Figure()
        fig_ci_w.add_trace(go.Scatter(
            x=w10['median_rank'],
            y=w10['player_name'],
            mode='markers',
            marker=dict(color='#10B981', size=11, line=dict(color='#FFFFFF', width=1)),
            error_x=dict(
                type='data',
                symmetric=False,
                array=w10['boot_p95_rank'] - w10['median_rank'],
                arrayminus=w10['median_rank'] - w10['boot_p05_rank'],
                color='#6EE7B7',
                thickness=2.5,
                width=6
            ),
            hovertext="Median: " + w10['median_rank'].astype(str) + " [CI: " + w10['boot_p05_rank'].astype(int).astype(str) + ", " + w10['boot_p95_rank'].astype(int).astype(str) + "]"
        ))
        fig_ci_w.update_layout(
            yaxis=dict(autorange="reversed"),
            xaxis_title="Bootstrap Rank (Lower = Better)"
        )
        apply_rr_plotly_theme(fig_ci_w, title="🎯 Bowlers 90% Rank Confidence Intervals across 1,000 Resamples")
        st.plotly_chart(fig_ci_w, use_container_width=True)
        
    st.markdown("---")
    
    # Candidate Eligibility vs Top 10 Inclusion
    st.subheader("Candidate Eligibility % vs Top-10 Inclusion Frequency")
    st.markdown("""
    **Core Governance Principle:** **Candidate Eligibility %** reflects whether a player met minimum sample volume cutoffs in a specification. **Top-10 Inclusion %** indicates how often their performance placed them in the top 10. These metrics are strictly separate.
    """)
    
    col_el1, col_el2 = st.columns(2)
    with col_el1:
        b10_chart = b10.rename(columns={'elig_share': 'Specification Eligibility %', 'top10_freq': 'Top-10 Consensus %'})
        fig_el_b = px.bar(
            b10_chart,
            x='player_name',
            y=['Specification Eligibility %', 'Top-10 Consensus %'],
            barmode='group',
            color_discrete_sequence=['#334E68', '#EA1A80'],
            labels={'value': 'Share of Specifications', 'variable': 'Metric', 'player_name': 'Player'}
        )
        fig_el_b.update_layout(yaxis_tickformat='.0%')
        apply_rr_plotly_theme(fig_el_b, title="Batters: Specification Eligibility vs Top-10 Consensus")
        st.plotly_chart(fig_el_b, use_container_width=True)
        
    with col_el2:
        w10_chart = w10.rename(columns={'elig_share': 'Specification Eligibility %', 'top10_freq': 'Top-10 Consensus %'})
        fig_el_w = px.bar(
            w10_chart,
            x='player_name',
            y=['Specification Eligibility %', 'Top-10 Consensus %'],
            barmode='group',
            color_discrete_sequence=['#334E68', '#10B981'],
            labels={'value': 'Share of Specifications', 'variable': 'Metric', 'player_name': 'Player'}
        )
        fig_el_w.update_layout(yaxis_tickformat='.0%')
        apply_rr_plotly_theme(fig_el_w, title="Bowlers: Specification Eligibility vs Top-10 Consensus")
        st.plotly_chart(fig_el_w, use_container_width=True)
        
    # ANOVA Variance Decomposition
    st.subheader("Sequential Type I ANOVA on Percentile Ranks (100.00% Variance Decomposition)")
    st.dataframe(anova, hide_index=True, use_container_width=True)
    st.caption("Epistemic note: Type I sequential sums of squares measure empirical variance across researcher model choices, not an unbiased structural estimate of true player talent.")

# ==============================================================================
# 7. RAJASTHAN ROYALS 2026 AUDIT & SQUAD-GAP ANALYSIS
# ==============================================================================
elif nav_choice == "🛡️ Rajasthan Royals 2026 Audit":
    st.markdown('<div class="main-title">Rajasthan Royals 2026 Campaign Audit</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-title">Phase-by-Phase Empirical Audit from Raw Match Data &amp; Concrete Recruitment Solutions</div>', unsafe_allow_html=True)
    
    # RR Summary KPIs
    r1, r2, r3, r4 = st.columns(4)
    with r1:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-label">Tournament Record</div>
            <div class="metric-value">16 M</div>
            <div class="metric-delta delta-neutral">8 Wins, 8 Losses (3rd Place)</div>
        </div>
        """, unsafe_allow_html=True)
    with r2:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-label">Playoff Finish</div>
            <div class="metric-value">Qualifier 2</div>
            <div class="metric-delta delta-pos">Podium Finish</div>
        </div>
        """, unsafe_allow_html=True)
    with r3:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-label">Team Death ER</div>
            <div class="metric-value">10.60</div>
            <div class="metric-delta delta-pos">-0.07 vs League Avg (10.67)</div>
        </div>
        """, unsafe_allow_html=True)
    with r4:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-label">Middle Spin ER</div>
            <div class="metric-value">9.29</div>
            <div class="metric-delta delta-neg">+0.32 vs League Avg (8.97)</div>
        </div>
        """, unsafe_allow_html=True)
        
    st.markdown("---")
    
    # RR Squad Performance Table
    st.subheader("📋 Audited RR 2026 Player Performance Table (from `matches.csv` & `ball_by_ball.csv`)")
    st.dataframe(rr, hide_index=True, use_container_width=True)
    
    st.markdown("---")
    
    # Tactical Phase Deficits
    st.subheader("🔍 Three Tactical Recruitment Focal Areas for Rajasthan Royals")
    
    rr_col1, rr_col2, rr_col3 = st.columns(3)
    with rr_col1:
        st.markdown("""
        #### 1. Death-Overs Bowling Leaks
        - **Audited Empirical Finding:** RR's overall team death ER was **10.60** (league avg 10.67), but individual variance was extreme.
        - **The Deficit:** Jofra Archer (9.35 ER) and Nandre Burger (9.33 ER) performed well, but **Sandeep Sharma conceded 13.70 rpo** (46 balls) and **Tushar Deshpande conceded 12.38 rpo** (48 balls).
        - **Recruitment Solution:** Inquire regarding targeted death seamers like **Nathan Ellis** (+5.50 runs saved/24b) or monitor **Eshan Malinga** (+3.39 raw lift) to stabilize expensive death spells.
        """)
    with rr_col2:
        st.markdown("""
        #### 2. Middle-Overs Spin Economy
        - **Audited Empirical Finding:** RR spinners conceded **9.29 rpo** in overs 7–15 compared to the tournament average of **8.97 rpo**.
        - **The Deficit:** Ravindra Jadeja held an 8.39 ER, but secondary spin leaked heavily: Yash Punja posted **9.54 ER** and Ravi Bishnoi conceded **10.11 ER** with only 21.9% dots.
        - **Recruitment Solution:** Add an attacking, controlling wrist-spinner like **Noor Ahmad** (+2.54 impact, 34.8% dots) or monitor trade options to choke middle overs.
        """)
    with rr_col3:
        st.markdown("""
        #### 3. Death-Overs Batting Support
        - **Audited Empirical Finding:** Donovan Ferreira produced an exceptional **221.7 SR** across 83 death balls (league avg 169.4).
        - **The Deficit:** Secondary finishers lacked boundary output: Jadeja scored at **140.5 SR**, Shubham Dubey at **146.3 SR**, and Shimron Hetmyer managed only **121.1 SR**.
        - **Recruitment Solution:** Target a domestic finisher to partner Ferreira if contractually released. Top analytical profiles: **Shashank Singh** (+22.2 raw lift) or **Naman Dhir** (+35.4 raw lift).
        """)

# ==============================================================================
# 8. IPL 2027 RECRUITMENT ACTIONABILITY
# ==============================================================================
elif nav_choice == "💼 IPL 2027 Recruitment Actionability":
    st.markdown('<div class="main-title">IPL 2027 Recruitment Actionability Register</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-title">Strict Governance: Historical Statistical Ranking Separated from Real-World Auction Feasibility</div>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="callout-box">
        <strong>Strict Governance Rule:</strong> Statistical models reflect what happened historically in the dataset. Real-world IPL recruitment requires verifying contracts, BCCI retention rules, confirmed trades, and injury statuses via dated public reporting.<br><br>
        <strong>Classification Categories:</strong>
        <ul>
            <li><strong>Confirmed:</strong> Official, executed trades or contract actions published by BCCI / franchises.</li>
            <li><strong>Reported:</strong> Verified media or franchise reports (e.g. medical rehabilitation, reported retentions).</li>
            <li><strong>Unverified:</strong> Active players awaiting formal BCCI retention list publication. <em>Never labeled auction-available.</em></li>
            <li><strong>Retired / Historical only:</strong> Players retired from IPL competition, serving as analytical benchmarks.</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    # Status KPI Row
    n_conf = (sources['ipl_2027_status_category'] == 'Confirmed').sum()
    n_rep = (sources['ipl_2027_status_category'] == 'Reported').sum()
    n_ret = (sources['ipl_2027_status_category'] == 'Retired / Historical only').sum()
    n_unv = (sources['ipl_2027_status_category'] == 'Unverified').sum()

    s1, s2, s3, s4 = st.columns(4)
    with s1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Confirmed Trades</div>
            <div class="metric-value">{n_conf}</div>
            <div class="metric-delta delta-pos">Official BCCI Actions</div>
        </div>
        """, unsafe_allow_html=True)
    with s2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Reported Medical/Rehab</div>
            <div class="metric-value">{n_rep}</div>
            <div class="metric-delta delta-neutral">Active Rehabilitation</div>
        </div>
        """, unsafe_allow_html=True)
    with s3:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Retired Benchmarks</div>
            <div class="metric-value">{n_ret}</div>
            <div class="metric-delta delta-neg">Coaching / Inactive</div>
        </div>
        """, unsafe_allow_html=True)
    with s4:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Unverified Active</div>
            <div class="metric-value">{n_unv}</div>
            <div class="metric-delta delta-neutral">Awaiting Formal List</div>
        </div>
        """, unsafe_allow_html=True)

    # Filter controls
    col_s1, col_s2, col_s3 = st.columns([1, 1, 2])
    with col_s1:
        status_filter = st.selectbox(
            "Filter Status Category",
            ["All", "Confirmed", "Reported", "Unverified", "Retired / Historical only"]
        )
    with col_s2:
        disc_filter = st.selectbox("Filter Discipline", ["All", "Batter", "Bowler"])
    with col_s3:
        search_kw = st.text_input("Search Player or Franchise", "")
        
    df_src = sources.copy()
    if status_filter != "All":
        df_src = df_src[df_src['ipl_2027_status_category'] == status_filter]
    if disc_filter != "All":
        df_src = df_src[df_src['discipline'] == disc_filter]
    if search_kw:
        df_src = df_src[
            df_src['player_name'].str.contains(search_kw, case=False, na=False) |
            df_src['latest_verified_franchise'].str.contains(search_kw, case=False, na=False)
        ]
        
    st.dataframe(
        df_src[['player_name', 'discipline', 'role', 'latest_verified_franchise', 'ipl_2027_status_category', 'active_status', 'ipl_2027_availability_status', 'evidence_classification', 'source_url']],
        hide_index=True,
        use_container_width=True,
        column_config={
            "player_name": "Player Name",
            "discipline": "Discipline",
            "role": "Role",
            "latest_verified_franchise": "Franchise",
            "ipl_2027_status_category": "Standardized Status",
            "active_status": "Active Status & Context",
            "ipl_2027_availability_status": "Availability Details",
            "evidence_classification": "Evidence Tier",
            "source_url": st.column_config.LinkColumn("Source URL")
        }
    )
    
    st.markdown("---")
    st.subheader("🔍 Key Verified Real-World Fact Register")
    
    st.markdown("""
    - **Nathan Ellis (`player_id`: 7920):** Officially traded from **Chennai Super Kings (CSK) to Sunrisers Hyderabad (SRH) on 5 November 2026** for INR 2.00 Cr. Overseas competition at SRH creates an active secondary trade/monitoring opportunity.
    - **Arshdeep Singh (`player_id`: 6464):** Officially traded from **Punjab Kings (PBKS) to Mumbai Indians (MI) on 11 November 2026** in an all-cash INR 18.00 Cr deal. Unviable for near-term transfer.
    - **Matheesha Pathirana (`player_id`: 8661):** Sustained a confirmed grade-2 hamstring strain on **16 May 2026** vs GT; currently undergoing rehabilitation; do not assume 2027 unavailability without updated medical clearance.
    - **Dinesh Karthik, Andre Russell & Bhuvneshwar Kumar:** Classified as retired IPL players / coaches (DK: RCB Batting Coach & Mentor; Russell: KKR Power Coach; Bhuvi: transitioned to coaching). Retained as analytical benchmarks.
    - **Matthew Wade (`player_id`: 796):** Retired from international cricket (Oct 2024) and BBL (Feb 2025). Excluded by bootstrap hurdle (720/1,000 draws).
    - **Pakistani Players (e.g. Haris Rauf):** Documented non-participation in IPL auctions since 2008 as real-world context for near-miss candidates.
    """)

# ==============================================================================
# 9. METHODOLOGY & GOVERNANCE
# ==============================================================================
elif nav_choice == "🔬 Methodology & Governance":
    st.markdown('<div class="main-title">Methodological Architecture &amp; Scientific Governance</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-title">Leave-Player-Out Baselines, Empirical Bayes Regularization &amp; Multiverse Specification Curves</div>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="disclaimer-banner">
        <strong>Academic &amp; Participant Research Disclaimer:</strong> This is an independent participant research project based on historical cricket data. It is not an official Rajasthan Royals product or recruitment decision.
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    ### 1. Situational Pressure Definition
    Pressure is formulated as a pre-delivery leverage index:
    - **Chasing (2nd Innings):** Driven by Required Run Rate (RRR) relative to Current Run Rate (CRR), balls remaining, and wickets in hand.
    - **Setting (1st Innings):** Driven by match phase, pre-delivery wickets lost, and leverage relative to historical par score.
    - **Zero Look-Ahead Guarantee:** All features (`pre_runs`, `pre_wickets`, `pre_balls_remaining`, `pre_rrr`) are calculated strictly prior to delivery execution.
    """)
    
    st.markdown("### 2. Leave-Player-Out (LPO) Hierarchical Baselines")
    st.markdown(r"To avoid self-contamination, context baselines subtract player $i$'s own deliveries from cell $c$:")
    st.latex(r"\mu_{c,-i} = \frac{\sum_{j \ne i} \text{runs}_{j,c}}{\sum_{j \ne i} \text{balls}_{j,c}}")
    st.markdown("When the cell sample size falls below 50 balls, the baseline hierarchically falls back to phase and competition parent priors.")
    
    st.markdown("### 3. Empirical Bayes Shrinkage")
    st.markdown(r"Observed player performance $\hat{\theta}_i$ is shrunk toward prior mean $\mu_0$ based on effective sample size $n_i$:")
    st.latex(r"\theta_i^{\text{EB}} = w_i \hat{\theta}_i + (1 - w_i) \mu_0, \quad w_i = \frac{n_i}{n_i + K}")
    st.markdown("Where $K$ is estimated via marginal maximum likelihood, preventing small-sample noise from dominating leaderboard rankings.")
    
    st.markdown(r"""
    ### 4. Multiverse Grid Architecture (15,150 Specifications)
    The specification curve tests:
    - **Pressure Definitions:** 3 formulations (P1, P2, P3).
    - **Wicket Valuation Modes:** 5 modes (W0 to W4).
    - **Scoring Models:** 4 models (Model A, B, C, D).
    - **Shrinkage Constants:** 5 values ($K \in [60, 200]$).
    - **Volume Thresholds:** 5 levels ($V \in [4, 12]$ matches).
    - **Match Filters:** 3 splits (All, IPL Only, T20I Only).
    - **Competition Weights:** Standard vs Recency-Weighted.
    
    Total Grid = $3 \times 5 \times 4 \times 5 \times 5 \times 3 \times 2 = \mathbf{15{,}150 \text{ specifications}}$.
    
    ### 5. Scientific Limitations & Epistemic Humility
    1. **Non-Causal Interpretability:** ANOVA variance decomposition reflects researcher model choices, not intrinsic player talent.
    2. **Role Confounding:** Finishers naturally face higher leverage than openers; baselines control for context but role specialization remains.
    3. **Survivor Bias:** Players who fail repeatedly under pressure lose their spot in the playing XI, leaving only resilient survivors in long-horizon samples.
    4. **Descriptive vs Predictive:** Walk-forward split tests demonstrate that pressure splits are descriptive documentation of past execution, not guaranteed future performance.
    """)

# ==============================================================================
# 10. DOWNLOADS & DATA EXPORT
# ==============================================================================
elif nav_choice == "📥 Downloads & Data Export":
    st.markdown('<div class="main-title">Data Export &amp; Verification Downloads</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-title">Download Canonical, Audited CSV Outputs from the Verified V4 Submission Package</div>', unsafe_allow_html=True)
    
    col_d1, col_d2 = st.columns(2)
    with col_d1:
        st.subheader("🏏 Final Top 10 Batters CSV")
        st.write("Canonical 30-column verified CSV containing Multiverse frequencies, shrunk impact, raw lift, and bootstrap statistics.")
        b10_csv = b10.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Download final_top10_batters.csv",
            data=b10_csv,
            file_name="final_top10_batters.csv",
            mime="text/csv"
        )
        
    with col_d2:
        st.subheader("🎯 Final Top 10 Bowlers CSV")
        st.write("Canonical 30-column verified CSV containing Multiverse frequencies, defending shrunk impact, raw lift, and bootstrap statistics.")
        w10_csv = w10.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Download final_top10_bowlers.csv",
            data=w10_csv,
            file_name="final_top10_bowlers.csv",
            mime="text/csv"
        )
        
    st.markdown("---")
    
    col_d3, col_d4 = st.columns(2)
    with col_d3:
        st.subheader("🛡️ Rajasthan Royals 2026 Audit CSV")
        st.write("Audited player performance metrics from RR 2026 IPL campaign.")
        rr_csv = rr.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Download rr_squad_2026.csv",
            data=rr_csv,
            file_name="rr_squad_2026.csv",
            mime="text/csv"
        )
        
    with col_d4:
        st.subheader("📋 Verified External Source Register CSV")
        st.write("Complete 51-player dated research register with standardized status categories and evidence classifications.")
        src_csv = sources.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Download source_register_all.csv",
            data=src_csv,
            file_name="source_register_all.csv",
            mime="text/csv"
        )

# --- FOOTER ---
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #64748B; font-size: 0.85rem; padding: 14px 0;">
    SupeRR Selector Season 2 — Round 1 Analytics Submission | V4 Multiverse Analysis<br>
    <em>Disclaimer: This is an independent participant research project based on historical cricket data. It is not an official Rajasthan Royals product or recruitment decision.</em><br>
    Strictly Read-Only | Verified &amp; Audited | No Proprietary Ball-by-Ball Data Exposed
</div>
""", unsafe_allow_html=True)
