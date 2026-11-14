"""
Final Publication Generator for SupeRR Selector Season 2 Submission Report.
Compiles SupeRR_Final_Report.pdf (exactly 14 pages) directly from the verified
methodology, data tables, and SupeRR_Final_Report.md content.
"""

from pathlib import Path
import subprocess
import pypdf
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
OUT_DIR = ROOT / "outputs" / "submission_final"
MODEL_V4_DIR = ROOT / "outputs" / "model_v4"
CHART_DIR = MODEL_V4_DIR / "charts"
OUT_PDF = OUT_DIR / "SupeRR_Final_Report.pdf"
OUT_MD = OUT_DIR / "SupeRR_Final_Report.md"
TEMP_HTML = OUT_DIR / "report_temp.html"

OUT_DIR.mkdir(parents=True, exist_ok=True)

# Load data tables
top10_bat = pd.read_csv(MODEL_V4_DIR / "final_top10_batters.csv")
top10_bowl = pd.read_csv(MODEL_V4_DIR / "final_top10_bowlers.csv")
boot_bat = pd.read_csv(MODEL_V4_DIR / "bootstrap_canonical_batters.csv").set_index("striker_id")
boot_bowl = pd.read_csv(MODEL_V4_DIR / "bootstrap_canonical_bowlers.csv").set_index("bowler_id")

def uri_audit_chart(filename: str) -> str:
    return (ROOT / "outputs" / "data_audit" / "charts" / filename).as_uri()

def uri_chart(filename: str) -> str:
    return (CHART_DIR / filename).as_uri()

def make_page1_table_bat():
    bat_recs = {
        "Shashank Singh": "Priority if available",
        "Tim David": "Watchlist",
        "Naman Dhir": "Priority if available",
        "Dinesh Karthik": "Historical benchmark – retired player; RCB Coach",
        "Heinrich Klaasen": "Watchlist",
        "Suryakumar Yadav": "Watchlist",
        "Rinku Singh": "Priority if available",
        "Romario Shepherd": "Watchlist",
        "Andre Russell": "Historical benchmark – retired from IPL; KKR Coach",
        "Rashid Khan": "Priority if available"
    }
    rows = []
    for _, r in top10_bat.iterrows():
        tier_short = "Tier 1" if "Tier 1" in r["tier"] else ("Tier 2" if "Tier 2" in r["tier"] else "Tier 3")
        rec_text = bat_recs.get(r['player_name'], "Watchlist")
        rows.append(f"""
        <tr>
          <td><strong>{r['final_rank']}</strong></td>
          <td style="text-align:left;"><strong>{r['player_name']}</strong> ({int(r['player_id'])})</td>
          <td><span class="badge badge-{tier_short.lower().replace(' ', '')}">{tier_short}</span></td>
          <td>{r['elig_share']:.1%}</td>
          <td>{r['top10_freq']:.1%}</td>
          <td>{r['median_rank']:.0f} [{r['iqr_rank']:.0f}]</td>
          <td>{r['model_b_score']:.2f}</td>
          <td>{r['shrunk_wp_impact']:+.1f}</td>
          <td>{r['raw_lift']:+.1f}</td>
          <td>{int(r['hp_balls'])}</td>
          <td>{int(r['eligible_draws'])}/1000</td>
          <td style="font-size:5.8pt; text-align:left; font-weight:600; color:#1E3A8A;">{rec_text}</td>
        </tr>
        """)
    return "\n".join(rows)

def make_page1_table_bowl():
    bowl_recs = {
        "Sunil Narine": "Watchlist",
        "Jasprit Bumrah": "Watchlist",
        "Rashid Khan": "Priority if available",
        "Matheesha Pathirana": "Watchlist",
        "Eshan Malinga": "Priority if available",
        "Nathan Ellis": "Priority if available (traded CSK -> SRH)",
        "Noor Ahmad": "Priority if available",
        "Arshdeep Singh": "Watchlist (traded PBKS -> MI)",
        "Prasidh Krishna": "Watchlist",
        "Bhuvneshwar Kumar": "Watchlist"
    }
    rows = []
    for _, r in top10_bowl.iterrows():
        tier_short = "Tier 1" if "Tier 1" in r["tier"] else ("Tier 2" if "Tier 2" in r["tier"] else "Tier 3")
        rec_text = bowl_recs.get(r['player_name'], "Watchlist")
        rows.append(f"""
        <tr>
          <td><strong>{r['final_rank']}</strong></td>
          <td style="text-align:left;"><strong>{r['player_name']}</strong> ({int(r['player_id'])})</td>
          <td><span class="badge badge-{tier_short.lower().replace(' ', '')}">{tier_short}</span></td>
          <td>{r['elig_share']:.1%}</td>
          <td>{r['top10_freq']:.1%}</td>
          <td>{r['median_rank']:.0f} [{r['iqr_rank']:.0f}]</td>
          <td>{r['model_b_score']:.2f}</td>
          <td>{r['shrunk_wp_impact']:+.2f}</td>
          <td>{r['raw_lift']:+.2f}</td>
          <td>{int(r['hp_balls'])}</td>
          <td>{int(r['eligible_draws'])}/1000</td>
          <td style="font-size:5.8pt; text-align:left; font-weight:600; color:#1E3A8A;">{rec_text}</td>
        </tr>
        """)
    return "\n".join(rows)

def make_table2a_rows():
    rows = []
    for _, r in top10_bat.iterrows():
        pid = int(r['player_id'])
        b = boot_bat.loc[pid]
        p05 = int(b['boot_p05_rank'])
        p95 = int(b['boot_p95_rank'])
        share = r['rises_under_pressure_share']
        cls = "Rises under pressure" if share >= 0.60 else ("Elite all the time" if share < 0.40 else "Balanced / Context-dep")
        rows.append(f"""
        <tr>
          <td><strong>{r['final_rank']}</strong></td>
          <td style="text-align:left;"><strong>{r['player_name']}</strong> ({pid})</td>
          <td>{r['tier'].split()[0]}</td>
          <td>{r['shrunk_wp_impact']:+.1f}</td>
          <td>{r['shrunk_norm_impact']:+.1f}</td>
          <td><strong>{r['raw_lift']:+.1f}</strong></td>
          <td>{r['maint_lift']:+.1f}</td>
          <td>{int(r['hp_balls'])}</td>
          <td>{r['elig_share']:.1%}</td>
          <td>{r['top10_freq']:.1%}</td>
          <td>{r['median_rank']:.0f} [{r['iqr_rank']:.0f}]</td>
          <td>[{p05}, {p95}]</td>
          <td>{share:.1%}</td>
          <td style="font-size:6.5pt;">{cls}</td>
        </tr>
        """)
    return "\n".join(rows)

def make_table2b_rows():
    rows = []
    for _, r in top10_bowl.iterrows():
        pid = int(r['player_id'])
        b = boot_bowl.loc[pid]
        p05 = int(b['boot_p05_rank'])
        p95 = int(b['boot_p95_rank'])
        share = r['rises_under_pressure_share']
        cls = "Rises under pressure" if share >= 0.60 else ("Elite all the time" if share < 0.40 else "Balanced / Context-dep")
        rows.append(f"""
        <tr>
          <td><strong>{r['final_rank']}</strong></td>
          <td style="text-align:left;"><strong>{r['player_name']}</strong> ({pid})</td>
          <td>{r['tier'].split()[0]}</td>
          <td>{r['shrunk_wp_impact']:+.2f}</td>
          <td>{r['shrunk_norm_impact']:+.2f}</td>
          <td><strong>{r['raw_lift']:+.2f}</strong></td>
          <td>{r['maint_lift']:+.2f}</td>
          <td>{int(r['hp_balls'])}</td>
          <td>{r['elig_share']:.1%}</td>
          <td>{r['top10_freq']:.1%}</td>
          <td>{r['median_rank']:.0f} [{r['iqr_rank']:.0f}]</td>
          <td>[{p05}, {p95}]</td>
          <td>{share:.1%}</td>
          <td style="font-size:6.5pt;">{cls}</td>
        </tr>
        """)
    return "\n".join(rows)

# Build HTML template with exact 14 pages
html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>SupeRR Selector Season 2 — Round 1 Intelligence Submission</title>
<style>
  @page {{
    size: A4 portrait;
    margin: 1.05cm 1.05cm 1.05cm 1.05cm;
    @bottom-right {{
      content: "Page " counter(page) " of 15";
      font-size: 7pt;
      color: #718096;
      font-weight: 600;
    }}
  }}
  *, *:before, *:after {{
    box-sizing: border-box;
  }}
  body {{
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    color: #1A202C;
    background-color: #FFFFFF;
    line-height: 1.30;
    font-size: 8.0pt;
    margin: 0;
    padding: 0;
  }}
  .page {{
    page-break-after: always;
    break-after: page;
    height: 100%;
    display: flex;
    flex-direction: column;
    justify-content: flex-start;
  }}
  .page:last-child {{
    page-break-after: avoid;
    break-after: avoid;
  }}
  .header-bar {{
    border-bottom: 2px solid #E61E64;
    padding-bottom: 3px;
    margin-bottom: 5px;
    display: flex;
    justify-content: space-between;
    align-items: flex-end;
  }}
  .header-title {{
    font-size: 9.2pt;
    font-weight: 800;
    color: #1D3557;
    text-transform: uppercase;
    letter-spacing: 0.5px;
  }}
  .header-sub {{
    font-size: 7.0pt;
    color: #718096;
    font-weight: 600;
  }}
  .doc-title {{
    font-size: 14.5pt;
    font-weight: 900;
    color: #1D3557;
    line-height: 1.15;
    margin: 0 0 2px 0;
  }}
  .doc-subtitle {{
    font-size: 8.5pt;
    font-weight: 600;
    color: #E61E64;
    margin: 0 0 5px 0;
  }}
  .callout-box {{
    background-color: #F8FAFC;
    border-left: 3.5px solid #E61E64;
    padding: 4px 7px;
    margin-bottom: 5px;
    border-radius: 0 4px 4px 0;
  }}
  .callout-title {{
    font-weight: 800;
    color: #1D3557;
    font-size: 8.0pt;
    margin-bottom: 2px;
  }}
  .section-heading {{
    font-size: 10.0pt;
    font-weight: 800;
    color: #1D3557;
    border-bottom: 1px solid #E2E8F0;
    padding-bottom: 2px;
    margin: 7px 0 4px 0;
    text-transform: uppercase;
    letter-spacing: 0.3px;
  }}
  .sub-heading {{
    font-size: 8.5pt;
    font-weight: 700;
    color: #E61E64;
    margin: 4px 0 2px 0;
  }}
  p {{
    margin: 0 0 4px 0;
    text-align: justify;
  }}
  table {{
    width: 100%;
    border-collapse: collapse;
    margin: 2px 0 5px 0;
    font-size: 7.0pt;
  }}
  th, td {{
    padding: 2.5px 3.5px;
    border: 1px solid #CBD5E0;
    text-align: center;
  }}
  th {{
    background-color: #1D3557;
    color: #FFFFFF;
    font-weight: 700;
  }}
  tr:nth-child(even) {{
    background-color: #F7FAFC;
  }}
  .badge {{
    display: inline-block;
    padding: 1px 3.5px;
    border-radius: 3px;
    font-size: 6.0pt;
    font-weight: 800;
    text-transform: uppercase;
  }}
  .badge-tier1 {{
    background-color: #DEF7EC;
    color: #03543F;
    border: 1px solid #84E1BC;
  }}
  .badge-tier2 {{
    background-color: #E1EFFE;
    color: #1E429F;
    border: 1px solid #A4CAFE;
  }}
  .badge-tier3 {{
    background-color: #FEF08A;
    color: #713F12;
    border: 1px solid #FDE047;
  }}
  .rec-box {{
    width: 60px;
    background-color: #FFFFFF;
    border: 1px dashed #A0AEC0;
  }}
  .chart-img {{
    width: 100%;
    max-height: 220px;
    object-fit: contain;
    margin: 3px 0;
    border: 1px solid #E2E8F0;
    border-radius: 4px;
  }}
  .math-box {{
    background-color: #F8FAFC;
    border: 1px solid #CBD5E1;
    border-radius: 4px;
    padding: 3px 6px;
    margin: 3px 0;
    text-align: center;
    font-family: 'Cambria Math', 'Times New Roman', serif;
    font-size: 8.0pt;
    font-weight: 500;
    color: #0F172A;
  }}
  .grid-2 {{
    display: flex;
    gap: 8px;
    margin-bottom: 4px;
  }}
  .grid-2 > div {{
    flex: 1;
  }}
  .page-1-table th {{
    font-size: 6.6pt;
    padding: 2.0px 3px;
  }}
  .page-1-table td {{
    font-size: 6.8pt;
    padding: 1.6px 3px;
  }}
  .footer-note {{
    font-size: 6.4pt;
    color: #718096;
    margin-top: auto;
    border-top: 1px solid #E2E8F0;
    padding-top: 2px;
    display: flex;
    justify-content: space-between;
  }}
</style>
</head>
<body>

<!-- PAGE 1: EXECUTIVE SUMMARY & DUAL TOP-10 CONSENSUS LISTS -->
<div class="page" id="p1">
  <div class="header-bar">
    <div class="header-title">SupeRR Selector Season 2 — Round 1 Intelligence Submission</div>
    <div class="header-sub">Pre-Registered Multiverse Analysis (3.19M Evaluations)</div>
  </div>

  <h1 class="doc-title">Evaluating Cricket Performance Under Pressure: Multiverse Analysis & Rajasthan Royals Recruitment Strategy</h1>
  <div class="doc-subtitle">Submission by Rajat Aggarwal | Participant — SupeRR Selector Season 2 (Round 1)</div>

  <div class="callout-box">
    <div class="callout-title">One-Line Pressure Definition</div>
    <div>A delivery is classified as High-Pressure when the defending-side or batting-side pre-delivery leverage index reaches or exceeds 0.50 (evaluated via logistic sigmoid centered at 0.425 with slope k = 12.5 / scale 0.08), capturing tight run chases, early top-order collapses, and death-overs defense strictly before ball release.</div>
  </div>

  <div class="callout-box" style="border-left-color: #1D3557; margin-bottom:4px;">
    <div class="callout-title">Pre-Registered Ranking Rule & Metric Definitions</div>
    <div style="font-size:7.2pt;"><strong>Ranking Rule:</strong> Ordered by multiverse top-10 frequency; ties broken by lower median rank; candidate must pass &ge;50% eligibility across valid specifications and &ge;800/1,000 bootstrap draws (all 20 selections satisfy both).<br>
    <strong>Elig %:</strong> Candidate specification eligibility share across 15,150 specifications. &bull; <strong>Top-10 %:</strong> Share of valid specifications where player finishes inside the Top 10 (e.g., Rashid Khan: 77.8% eligible, 47.9% Top-10 inclusion, 61.6% retention when eligible).</div>
  </div>

  <div class="callout-box" style="border-left-color: #2B6CB0; margin-bottom:4px;">
    <div class="callout-title">Three Core Empirical Findings</div>
    <ul style="margin: 0; padding-left: 14px; font-size: 7.2pt;">
      <li><strong>Multiverse Specification Sensitivity & Empirical Main Effects:</strong> Evaluating 15,150 specifications per role (3,196,444 player-specification evaluations) demonstrates that empirical player_id main effects account for 76.58% (batting) and 65.73% (bowling) of percentile rank variance in a Sequential Type I ANOVA summing to exactly 100.00%. Methodological sensitivity operates through player &times; specification interactions (21.44% batting, 32.79% bowling), while direct dimension main effects sum to under 2%. Reporting multiverse consensus is vastly more robust than relying on any single specification.</li>
      <li><strong>Pre-Registered Bootstrap Filter Removes Volatile Assets:</strong> Applying the 1,000-draw stability hurdle (&ge;800 draws) eliminated sample-dependent fringe candidates (Matthew Wade [ID: 796] qualified in only 720/1,000 draws; Mujeeb Ur Rahman [ID: 6450] in 744/1,000; Naveen ul Haq [ID: 5809] in 513/1,000), promoting resilient contributors (Rashid Khan, Noor Ahmad, Prasidh Krishna).</li>
      <li><strong>Rajasthan Royals 2026 Phase Audit:</strong> Phase-level auditing from raw data reveals that while RR's death bowling was league-average overall (ER 10.60 vs league 10.67), Sandeep Sharma (ER 13.70) and Tushar Deshpande (ER 12.38) were expensive individuals. In the middle overs, spin economy lagged league par (Jadeja 8.39, Bishnoi 10.11 vs league 8.97). At the death, Donovan Ferreira (SR 221.7) lacked an explosive second death hitter (Hetmyer SR 121.1). The consensus targets offer direct tactical options, if available at auction.</li>
    </ul>
  </div>

  <div class="sub-heading" style="margin-top:1px;">Consensus Top-10 Batters (Ranked by Multiverse Frequency, Shrunk PWI & Lift)</div>
  <table class="page-1-table">
    <thead>
      <tr>
        <th>#</th>
        <th style="text-align:left;">Player (ID)</th>
        <th>Tier</th>
        <th>Elig %</th>
        <th>Top-10 %</th>
        <th>Med [IQR]</th>
        <th>Canon</th>
        <th>PWI</th>
        <th>Lift</th>
        <th>HP Balls</th>
        <th>Boot</th>
        <th>Participant Rec</th>
      </tr>
    </thead>
    <tbody>
      {make_page1_table_bat()}
    </tbody>
  </table>

  <div class="sub-heading" style="margin-top:1px;">Consensus Top-10 Bowlers (Ranked by Multiverse Frequency, Defending Shrunk Impact & Lift)</div>
  <table class="page-1-table">
    <thead>
      <tr>
        <th>#</th>
        <th style="text-align:left;">Player (ID)</th>
        <th>Tier</th>
        <th>Elig %</th>
        <th>Top-10 %</th>
        <th>Med [IQR]</th>
        <th>Canon</th>
        <th>PWI</th>
        <th>Lift</th>
        <th>HP Balls</th>
        <th>Boot</th>
        <th>Participant Rec</th>
      </tr>
    </thead>
    <tbody>
      {make_page1_table_bowl()}
    </tbody>
  </table>

  <div class="footer-note">
    <span>Rajat Aggarwal | Participant — SupeRR Selector Season 2</span>
    <span>Page 1 of 15</span>
  </div>
</div>

<!-- PAGE 2: PROBLEM UNDERSTANDING & CRICKET ACCOUNTING -->
<div class="page" id="p2">
  <div class="header-bar">
    <div class="header-title">Problem Understanding & Data Architecture</div>
    <div class="header-sub">SupeRR Selector Season 2</div>
  </div>

  <div class="section-heading">1. Problem Understanding & Operational Framing</div>
  <p>In high-stakes franchise cricket, evaluating players based on raw aggregate runs, strike rates, or economy rates introduces severe survivor bias. Standard metrics treat a boundary scored in a low-leverage blowout identically to a boundary struck when requiring 12 runs off 4 balls against disciplined execution. My mandate in Round 1 of the SupeRR Selector Season 2 competition is to build a mathematically grounded, leakage-safe, and empirically reproducible framework that ranks players by performance in high-pressure situations <em>compared with their normal performance</em>, while directly informing Rajasthan Royals' auction strategy for IPL 2027.</p>
  
  <p>To eliminate post-hoc narrative fitting and researcher degrees of freedom, I developed a complete multiverse (specification-curve) pipeline governed by an immutable pre-registration protocol (outputs/model_v4/PREREGISTRATION.md). Rather than presenting a single isolated model whose rankings could hinge on arbitrary parameter cutoffs, I evaluated 15,150 specifications per role (3,196,444 player-specification evaluations) across eight orthogonal analytical dimensions. Every statistical rank reported in this submission is derived strictly from historical match data; public external facts (player availability, retention rules, and franchise context) are maintained strictly as practical operational flags.</p>

  <div class="section-heading">2. Data Scope, Cleaning & Cricket Accounting</div>
  <p>My analytical scope encompasses the complete primary historical dataset spanning January 2022 to November 2026. Following strict competition standards, I excluded secondary A-team / emerging representative tournaments (Mens T20 Emerging Teams Asia Cup 2024 [comp ID 2670] and Asia Cup Rising Stars 2025 [comp ID 3289], comprising 30 matches and 6,985 deliveries, which include 12 Super Over balls), the remaining 26 Super Over deliveries in IPL/T20I fixtures (out of 38 total raw Super Over deliveries across all competitions), and 16 abandoned matches with zero deliveries bowled. The primary audit universe contains exactly <strong>837 matches</strong> (367 Indian Premier League and 470 T20 Internationals), <strong>193,988 total deliveries</strong>, and <strong>185,692 legal balls</strong>.</p>

  <p>Rigorous cricket accounting was implemented at the delivery level to prevent distorted player ratings:</p>
  <ul>
    <li><strong>Player Identity Disambiguation:</strong> Every join, feature calculation, and aggregation is keyed strictly on unique numeric player_id. Name-string joins were strictly forbidden to resolve homonyms in the raw data, such as Abdul Samad (IDs 7446 vs. 6922) and Rashid Khan (IDs 4722 vs. 20172).</li>
    <li><strong>Fair Bowling & Extras Attribution:</strong> Bowler runs conceded strictly exclude byes and leg-byes (which represent fielding or wicketkeeping variances). Non-legal deliveries (wides, oversteps, and other no-balls) are credited to the batting team's extras while charging the bowler's runs conceded. Wides are treated as non-legal balls that do not increment the batter's balls faced. Oversteps and other no-balls increment batter balls faced.</li>
    <li><strong>Wicket Attribution:</strong> Bowler wickets strictly exclude run outs, retired out, and obstructing the field (normalizing raw typos such as 'Obstracting the field').</li>
    <li><strong>Revised Overs Accounting:</strong> In rain-affected matches, columns first_inn_revised_overs and second_inn_revised_overs in matches.csv store balls (e.g., 114.0 balls = 19.0 overs), not decimal overs.</li>
  </ul>

  <div class="footer-note">
    <span>Verified against SHA-256 integrity manifest (39/39 files unchanged).</span>
    <span>Page 2 of 15</span>
  </div>
</div>


<!-- PAGE 2B: DATA QUALITY & EMPIRICAL PRESSURE VALIDATION -->
<div class="page" id="p_audit">
  <div class="header-bar">
    <div class="header-title">Data Quality Audit & Empirical Pressure Validation</div>
    <div class="header-sub">SupeRR Selector Season 2 &bull; Pre-Modelling Audit</div>
  </div>

  <div class="section-heading">1. Scope Reconciliation & Referential Integrity (Step 0)</div>
  <p>To eliminate selection bias, the primary analytical scope was rigorously reconciled from the unfiltered raw database down to exactly <strong>837 matches</strong>, <strong>193,988 deliveries</strong>, and <strong>185,692 legal balls</strong> (367 IPL, 470 T20I matches, 2022–2026). Specifically: 200,999 raw deliveries (-) 6,985 emerging-tournament deliveries (comp IDs 2670 and 3289, 30 matches, which contain 12 Super Over deliveries) (-) 26 remaining IPL/T20I Super Over deliveries (out of 38 total raw Super Over deliveries across the entire dataset) (-) 16 abandoned zero-delivery fixtures = <strong>193,988 primary deliveries</strong> (185,692 legal deliveries; 7,472 wides, 824 no-balls; 186,516 batter balls faced).</p>

  <table style="font-size:7.2pt; margin-bottom:5px;">
    <thead>
      <tr>
        <th style="text-align:left;">Analytical Stage / Scope Step</th>
        <th>Matches</th>
        <th>Deliveries</th>
        <th>Legal Balls</th>
        <th style="text-align:left;">Accounting Rationale & Verification</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td style="text-align:left;">Total Raw Database Provided</td>
        <td>883</td>
        <td>200,999</td>
        <td>192,445</td>
        <td style="text-align:left;">Unfiltered repository dump (matches.csv, ball_by_ball.csv).</td>
      </tr>
      <tr>
        <td style="text-align:left;">(-) Abandoned / Zero-Delivery Fixtures</td>
        <td>-16</td>
        <td>0</td>
        <td>0</td>
        <td style="text-align:left;">Rain/abandonments with no play; verified 0 balls bowled.</td>
      </tr>
      <tr>
        <td style="text-align:left;">(-) Emerging Tournaments (Comp IDs 2670, 3289)</td>
        <td>-30</td>
        <td>-6,985</td>
        <td>-6,730</td>
        <td style="text-align:left;">Emerging/A-team tournaments (includes 12 Super Over deliveries, 10 legal); non-primary scope.</td>
      </tr>
      <tr>
        <td style="text-align:left;">(-) Remaining IPL/T20I Super Overs (Innings 3 & 4)</td>
        <td>0</td>
        <td>-26</td>
        <td>-23</td>
        <td style="text-align:left;">Remaining tie-breaker deliveries in IPL/T20I (out of 38 total raw Super Over deliveries, 33 legal).</td>
      </tr>
      <tr style="background-color:#F1F5F9; font-weight:bold;">
        <td style="text-align:left;">FINAL PRIMARY ANALYTICAL SCOPE</td>
        <td>837</td>
        <td>193,988</td>
        <td>185,692</td>
        <td style="text-align:left;">Exact target scope: 367 IPL + 470 T20I matches (2022–2026).</td>
      </tr>
    </tbody>
  </table>

  <div class="section-heading">2. Empirical Pressure Separation: High Pressure vs. Normal Outcomes</div>
  <p>To confirm that the pressure definition separates distinct match environments, outcome rates were independently computed across verified deliveries comparing raw High Pressure (PI &ge; 0.50) against Normal Pressure (PI &lt; 0.35). The intermediate band (0.35 &le; PI &lt; 0.50) is excluded only from this binary descriptive comparison, while retained in continuous modelling. Denominators strictly follow cricket accounting: batting metrics use batter balls faced (excluding wides); bowling metrics use bowler legal deliveries (excluding byes/leg-byes):</p>

  <div class="grid-2" style="align-items:center;">
    <div style="flex:1.25;">
      <table style="font-size:6.7pt;">
        <thead>
          <tr>
            <th style="text-align:left;">Role &amp; Metric</th>
            <th>High Pressure (PI &ge; 0.50)</th>
            <th>Normal (PI &lt; 0.35)</th>
            <th>Difference [95% CI]</th>
            <th>p-value</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td style="text-align:left;"><strong>Batting: Strike Rate</strong></td>
            <td><strong>133.9</strong></td>
            <td>144.2</td>
            <td>-10.3 [-12.7, -8.0]</td>
            <td>p &lt; 0.001</td>
          </tr>
          <tr>
            <td style="text-align:left;"><strong>Batting: Dismissal Rate</strong></td>
            <td><strong>6.66%</strong></td>
            <td>5.02%</td>
            <td>+1.64% [+1.40%, +1.87%]</td>
            <td>p &lt; 0.001</td>
          </tr>
          <tr>
            <td style="text-align:left;"><strong>Batting: Boundary Rate</strong></td>
            <td><strong>16.9%</strong></td>
            <td>20.0%</td>
            <td>-3.1% [-3.6%, -2.6%]</td>
            <td>p &lt; 0.001</td>
          </tr>
          <tr>
            <td style="text-align:left;"><strong>Batting: Dot-Ball Rate</strong></td>
            <td><strong>37.6%</strong></td>
            <td>36.6%</td>
            <td>+1.0% [+0.2%, +1.8%]</td>
            <td>p = 0.0096</td>
          </tr>
          <tr>
            <td style="text-align:left;"><strong>Bowling: Economy Rate</strong></td>
            <td><strong>9.36</strong></td>
            <td>8.15</td>
            <td>+1.21 [+1.04, +1.38]</td>
            <td>p &lt; 0.001</td>
          </tr>
          <tr>
            <td style="text-align:left;"><strong>Bowling: Dot-Ball Rate</strong></td>
            <td><strong>28.5%</strong></td>
            <td>41.2%</td>
            <td>-12.7% [-13.5%, -12.0%]</td>
            <td>p &lt; 0.001</td>
          </tr>
          <tr>
            <td style="text-align:left;"><strong>Bowling: Boundary Rate</strong></td>
            <td><strong>19.9%</strong></td>
            <td>19.1%</td>
            <td>+0.75% [+0.14%, +1.37%]</td>
            <td>p = 0.0167</td>
          </tr>
          <tr>
            <td style="text-align:left;"><strong>Bowling: Bowler Wicket Rate</strong></td>
            <td><strong>5.64%</strong></td>
            <td>5.58%</td>
            <td>+0.06% [-0.19%, +0.30%]</td>
            <td>p = 0.658 (n.s.)</td>
          </tr>
        </tbody>
      </table>
    </div>
    <div style="flex:1.05; text-align:center;">
      <img src="{uri_audit_chart('hp_vs_normal_outcomes.png')}" style="width:100%; max-height:185px; object-fit:contain; border:1px solid #CBD5E1; border-radius:4px;">
    </div>
  </div>

  <div class="callout-box" style="margin-top:3px;">
    <strong>Key Validation Takeaway:</strong> Under high pressure, batting strike rate drops by 10.3 points (133.9 vs 144.2, p &lt; 0.001) and boundary rate drops by 3.1% (16.9% vs 20.0%, p &lt; 0.001), while dismissal risk rises from 5.02% to 6.66% (+1.64%, p &lt; 0.001). Conversely, bowling economy escalates from 8.15 to 9.36 (+1.21 RPO, p &lt; 0.001) as dot balls drop sharply (28.5% vs 41.2%, p &lt; 0.001). Crucially, bowler-credited wicket rate is virtually identical (5.64% vs 5.58%, difference +0.06%, 95% CI [-0.19%, +0.30%], match-clustered p = 0.658, non-significant). This demonstrates that high pressure forces batters to take boundary-hitting risks against defensive bowling lines, producing runs and dismissals simultaneously, but bowler-credited strike ability remains constant. These descriptive differences between high-pressure and normal-pressure states must be distinguished from causal effects. This confirms that the continuous sigmoid formulation separates distinct, realistic match environments.
  </div>

  <div class="footer-note">
    <span>Pre-modelling data audit executed strictly from raw CSV tables (outputs/data_audit/).</span>
    <span>Page 3 of 15</span>
  </div>
</div>


<!-- PAGE 3: PRESSURE DEFINITIONS & REAL DELIVERIES -->
<div class="page" id="p3">
  <div class="header-bar">
    <div class="header-title">Defining Pressure in T20 Cricket</div>
    <div class="header-sub">Situational Mechanics & Mathematical Formulations</div>
  </div>

  <div class="section-heading">3. Batter-Side vs. Bowler-Side Pressure Formulations</div>
  <p>Pressure is inherently asymmetric between batters and bowlers. In a run chase where the batting team is 70/8 needing 110 runs from 30 balls, the batting team faces extreme collapse pressure, but the defending team is in commanding control and faces near-zero defending pressure. A single unified pressure index conflates these dynamics.</p>

  <div class="grid-2">
    <div>
      <div class="sub-heading">Batting Pressure Formulation</div>
      <p style="font-size:7.4pt;">In the first innings, pressure reflects resource depletion and collapse:
      <div class="math-box">PI<sub>bat, 1</sub> = 0.50 &middot; S<sub>collapse</sub> + 0.30 &middot; S<sub>crr</sub> + 0.20 &middot; S<sub>death</sub></div>
      where S<sub>collapse</sub> measures wickets lost relative to par. In the second innings, chase urgency and boundary deficits govern leverage:
      <div class="math-box">PI<sub>bat, 2</sub> = 0.50 &middot; S<sub>rrr</sub> + 0.30 &middot; S<sub>wkts</sub> + 0.20 &middot; S<sub>urgency</sub> + Boost<sub>close</sub></div>
      Continuous delivery weights are evaluated via logistic sigmoid centered at x<sub>0</sub> = 0.425 with slope k = 12.5 (scale s = 0.08):
      <div class="math-box">w<sub>k</sub> = 1 / [1 + e<sup>-12.5 &middot; (PI<sub>k</sub> - 0.425)</sup>] = 1 / [1 + e<sup>-(PI<sub>k</sub> - 0.425) / 0.08</sup>]</div>
    </div>
    <div>
      <div class="sub-heading">Defending Bowler Formulation</div>
      <p style="font-size:7.4pt;">In the first innings, pressure evaluates batting onslaughts (CRR &gt; par with &le;3 wickets down) and death overs (16–20 with &le;5 wickets down). A collapse damper down-weights deliveries when the batting team has lost &ge;6 wickets:
      <div class="math-box">PI<sub>bowl, 1</sub> = max(S<sub>death</sub>, S<sub>top</sub>) &times; Damp<sub>collapse</sub></div>
      In the second innings, leverage peaks during live, balanced chases (RRR ratio 0.7–1.5 with chasing side having &ge;4 wickets in hand). When the chasing side has lost &ge;7 wickets, tail-damping reduces leverage to 0.20.</p>
    </div>
  </div>

  <div class="sub-heading">Worked Delivery Examples from Raw Match Data (ball_by_ball.csv)</div>
  <p style="font-size:7.0pt; color:#4A5568; margin-top:-2px;"><em>Note: In raw data accounting, both events occurred on ball 15.5 (state shown is evaluated after 14.4 completed overs).</em></p>
  <div class="callout-box" style="margin-bottom:5px;">
    <strong>Worked Example 1 — Batter High Pressure (Match ID 14148, IPL 2022, Innings 2, Over 15, Ball 5 [Ball 15.5; state shown after 14.4 overs]):</strong><br>
    Chasing 193, the batting team is 104/5 in 14.4 overs needing 89 runs from 32 balls (pre_rrr = 16.69). Batter Shashank Singh (ID 2756) faces Wanindu Hasaranga (ID 4900). Continuous pressure index PI<sub>bat</sub> = 0.8648. Sigmoid weight w<sub>k</sub> = 0.9959. Shashank strikes a 6. LPO context baseline: expected runs 1.1087, expected dismissal 0.0396. Net impact: +4.8913 runs above expected + 0.2379 dismissal avoidance (V = 6.0) = <strong>+5.1292 runs</strong>, weighted at 0.9959 into his high-pressure sample.
  </div>
  <div class="callout-box" style="margin-bottom:5px; border-left-color: #1D3557;">
    <strong>Worked Example 2 — Defending Bowler High Pressure (Match ID 40749, IPL 2025, Innings 2, Over 15, Ball 5 [Ball 15.5; state shown after 14.4 overs]):</strong><br>
    Rain-affected DLS match with a revised target of 147 in 19 overs (114 balls). Chasing team is 113/2 in 14.4 overs needing 34 runs from 26 balls (pre_rrr = 7.85). Bowler Jasprit Bumrah (ID 2933) bowls to Shubman Gill (ID 6288). Defending pressure index PI<sub>bowl</sub> = 0.7958, sigmoid weight w<sub>k</sub> = 0.9904. Bumrah dismisses Gill <strong>Bowled</strong>, conceding 0 runs. LPO baseline: expected runs conceded 1.6681, expected wicket 0.0489. Net impact: +1.6681 runs saved + 5.7064 wicket value (V = 6.0) = <strong>+7.3745 runs</strong> created/saved, weighted at 0.9904 into Bumrah's defending ledger.
  </div>

  <div class="footer-note">
    <span>Zero look-ahead: all state variables evaluated strictly at t - 1 pre-ball release.</span>
    <span>Page 4 of 15</span>
  </div>
</div>

<!-- PAGE 4: PERFORMANCE MEASUREMENT & BASELINES -->
<div class="page" id="p4">
  <div class="header-bar">
    <div class="header-title">Performance Measurement Framework</div>
    <div class="header-sub">LPO Hierarchical Baselines & Regularization</div>
  </div>

  <div class="section-heading">4. Performance Measurement: Metrics, Baselines & Scoring Logic</div>
  <p>To measure performance above expectation fairly, every delivery must be compared against a realistic baseline expectation. Using raw league averages conflates player skill with favorable usage (e.g., batting during the field-restricted powerplay versus batting against spin in the middle overs). I implemented a leakage-safe <strong>Leave-Player-Out (LPO) Hierarchical Context Baseline</strong> that computes expected runs, dismissals, dot balls, and boundaries across multi-dimensional match cells.</p>

  <p>For player i on delivery k in match state cell c, player i's own historical contributions are strictly subtracted to eliminate self-leakage:
      <div class="math-box">&mu;&#770;<sub>-i, c</sub> = (&sum;<sub>j &ne; i, j &isin; c</sub> y<sub>j</sub>) / (&sum;<sub>j &ne; i, j &isin; c</sub> n<sub>j</sub>)</div>
  Whenever a cell has fewer than 50 observations after subtracting player iii, the algorithm automatically backs up the hierarchical tree (from format &times; season &times; phase &times; wickets bucket &times; role &times; opposition strength, up to phase and league level), ensuring robust estimates for rare game situations.</p>

  <div class="grid-2">
    <div>
      <div class="sub-heading">Wicket Valuation: Fixed Choice vs. Marginal Sensitivity</div>
      <p style="font-size:7.4pt;">In composite impact scoring, assigning an arbitrary run value to a wicket (e.g., 20 runs) double-counts deliveries and distorts ratings. I set wicket value to <strong>6.0 runs</strong> as a fixed analytical choice, avoiding double-counting the runs conceded on delivery iki. The non-overlapping context-marginal empirical estimate (7.82 runs) is evaluated across the multiverse as a sensitivity variant.</p>
    </div>
    <div>
      <div class="sub-heading">Empirical Bayes Shrinkage (iK=120i)</div>
      <p style="font-size:7.4pt;">Small samples in high-pressure subsets risk extreme noisy ratings. I applied Empirical Bayes shrinkage toward zero based on Kish's effective sample size N<sub>eff</sub> = (&sum; w<sub>k</sub>)<sup>2</sup> / &sum; w<sub>k</sub><sup>2</sup>:
      <div class="math-box">PWI<sub>shrunk</sub> = [N<sub>eff</sub> / (N<sub>eff</sub> + 120)] &middot; PWI<sub>raw</sub></div>
      This shrinks a player with only 20 HP balls heavily toward the prior, while preserving the true signal of established performers with 400+ HP balls.</p>
    </div>
  </div>

  <div class="sub-heading">Model Selection: Model A vs. Model B</div>
  <p>On empirical predictive criteria, Model A (absolute high-pressure output) is slightly ahead of Model B for batters. However, Model B is selected as the primary scoring framework because the competition brief explicitly requires ranking players by their performance under pressure <em>compared with their usual performance</em>:
      <div class="math-box">Score<sub>Model B</sub> = 0.50 &middot; z(PWI<sub>shrunk</sub>) + 0.30 &middot; z(MaintLift<sub>shrunk</sub>) + 0.20 &middot; z(Consistency<sub>EB</sub>)</div>
  where MaintLift = PWI<sub>shrunk</sub> - 0.35 &middot; max(Normal<sub>shrunk</sub>, Floor). This properly balances absolute capability with baseline resilience.</p>

  <div class="footer-note">
    <span>Labels: Shrunk PWI represents shrinkage-adjusted impact; Raw Lift represents unshrunk delta.</span>
    <span>Page 5 of 15</span>
  </div>
</div>

<!-- PAGE 5: FAIR COMPARISONS & MULTIVERSE GRID -->
<div class="page" id="p5">
  <div class="header-bar">
    <div class="header-title">Fair Comparisons & Multiverse Grid</div>
    <div class="header-sub">Sample Gates & 8-Dimensional Specification Architecture</div>
  </div>

  <div class="section-heading">5. Ensuring Fair Comparisons Across Contexts</div>
  <p>To ensure rankings reflect genuine skill rather than statistical noise, my framework enforces three rigorous governance layers:</p>
  <ul>
    <li><strong>Multi-Tier Eligibility Gates:</strong> Lenient (&ge;200 total balls, &ge;80 HP balls, &ge;8 HP matches); Standard Benchmark (&ge;300 total balls, &ge;120 HP balls, &ge;10 HP matches); Strict (&ge;400 total balls, &ge;150 HP balls, &ge;12 HP matches). In the multiverse selection rule, a player must qualify in &ge;50% of valid specifications.</li>
    <li><strong>Competition & Format Governance:</strong> The multiverse grid evaluates three format scopes: (F1) IPL + All T20I, (F2) IPL + Full-Member T20I, and (F3) IPL Only. Every candidate's HP volume and impact are partitioned across IPL and T20I tracks.</li>
    <li><strong>Cluster-Robust Match-Level Sampling:</strong> Deliveries within the same match share unobserved correlations. All standard errors, variance components, and bootstrap resamples are clustered at the match level.</li>
  </ul>

  <div class="section-heading">6. Multiverse Specification Grid (15,150 Specifications per Role)</div>
  <p>The multiverse grid evaluates <strong>15,150 specifications per role</strong> (3,196,444 player-specification evaluations across both roles):
      <div class="math-box">Total Specifications = 30 (P &times; W &times; F) &times; [504 (Model A/B specs) + 1 (Model C spec)] = 15,150</div>
  The 3,196,444 evaluation rows sum the eligible players evaluated in each specification (32–136 batters, 46–184 bowlers), including 3,030 bowler P0 reference specifications that are retained for audit diagnostics but excluded from candidate selection.</p>
  
  <table style="font-size:6.8pt;">
    <thead>
      <tr><th>Dimension</th><th>Levels Evaluated</th><th>Analytical Role & Parameters</th></tr>
    </thead>
    <tbody>
      <tr><td><strong>P (Pressure Definition)</strong></td><td>5 variants (P1-P5)</td><td>Continuous sigmoids (centers 0.40, 0.425, 0.45; scale 0.08, k=12.5), discrete threshold, Definition C collapse.</td></tr>
      <tr><td><strong>W (Wickets in Baseline)</strong></td><td>2 levels (W0, W1)</td><td>Conditioning match state baselines on wickets in hand (0-2, 3-5, 6+ wickets down).</td></tr>
      <tr><td><strong>M (Scoring Model)</strong></td><td>3 formulations (A, B, C)</td><td>Model A (absolute), Model B (maintenance & lift), Model C (interaction ridge regression).</td></tr>
      <tr><td><strong>V (Wicket Value)</strong></td><td>4 valuations</td><td>Fixed values (4.0, 6.0, 8.0 runs) and context-marginal dynamic estimate (7.82 runs).</td></tr>
      <tr><td><strong>K (Shrinkage Strength)</strong></td><td>3 penalties</td><td>Empirical Bayes shrinkage constants K = 60, 120 (canonical), 180.</td></tr>
      <tr><td><strong>F (Format Scope)</strong></td><td>3 scopes (F1, F2, F3)</td><td>IPL + All T20I (837 matches), IPL + Full-Member T20I (784 matches), IPL Only (367 matches).</td></tr>
      <tr><td><strong>G (Eligibility Gate)</strong></td><td>3 volume thresholds</td><td>Lenient (200/80/8), Standard (300/120/10), Strict (400/150/12), scaled for Definition C.</td></tr>
      <tr><td><strong>S (Composite Weights)</strong></td><td>7 weight vectors</td><td>Base (0.50, 0.30, 0.20) plus 6 local &plusmn;0.10 perturbations renormalised.</td></tr>
    </tbody>
  </table>

  <div class="footer-note">
    <span>Pre-registered protocol locked at outputs/model_v4/PREREGISTRATION.md.</span>
    <span>Page 6 of 15</span>
  </div>
</div>

<!-- PAGE 6: MULTIVERSE SPECIFICATION CURVE & ANOVA -->
<div class="page" id="p6">
  <div class="header-bar">
    <div class="header-title">Multiverse Specification Curve & Variance Decomposition</div>
    <div class="header-sub">Sensitivity Analysis Across 3.19M Evaluations</div>
  </div>

  <div class="section-heading">7. Specification Curve Findings & Sequential Type I ANOVA</div>
  <p>Across 15,150 specifications per role, top-ranked candidates consistently demonstrate high inclusion frequency. To understand ranking variance rigorously, I conducted a sequential (Type I) ANOVA on percentile ranks (y<sub>i,s</sub> = rank<sub>i,s</sub> / n<sub>eligible,s</sub>). Sequential (Type I) decomposition is order-dependent; the percentages reflect hierarchical explanatory contributions summing to exactly 100.00%, rather than uniquely isolated causal intrinsic-talent shares. Note: In raw ranks (which vary with specification candidate size n<sub>eligible,s</sub>), the player main effect is 60.17% (batting) and 62.08% (bowling); normalizing to percentile ranks yields 76.58% and 65.73%.</p>

  <div class="sub-heading">Sequential (Type I) ANOVA Variance Decomposition on Percentile Ranks</div>
  <table style="font-size:6.8pt;">
    <thead>
      <tr><th>Dimension / Source of Variance</th><th>Batters SS</th><th>Batters Share (%)</th><th>Bowlers SS</th><th>Bowlers Share (%)</th><th>Interpretation</th></tr>
    </thead>
    <tbody>
      <tr><td><strong>Player Identifier Main Effect (player_id)</strong></td><td><strong>40,196.12</strong></td><td><strong>76.58%</strong></td><td><strong>50,725.94</strong></td><td><strong>65.73%</strong></td><td>Empirical panel variance attributable to individual player mean ranks (non-causal).</td></tr>
      <tr><td>Eligibility Gate (g_gate)</td><td>426.87</td><td>0.81%</td><td>357.13</td><td>0.46%</td><td>Volume thresholds shift qualification of specialist finishers.</td></tr>
      <tr><td>Pressure Definition (p_def)</td><td>323.09</td><td>0.62%</td><td>521.97</td><td>0.68%</td><td>Continuous sigmoids vs discrete cuts vs Def C reorder borderline players.</td></tr>
      <tr><td>Format Scope (f_scope)</td><td>262.63</td><td>0.50%</td><td>240.83</td><td>0.31%</td><td>Domestic IPL vs international depth shifts player sample volumes.</td></tr>
      <tr><td>Wickets in Baseline (w_def)</td><td>18.13</td><td>0.03%</td><td>2.12</td><td>0.00%</td><td>Conditioning match state baselines on wickets in hand.</td></tr>
      <tr><td>Wicket Value (v_val)</td><td>5.31</td><td>0.01%</td><td>17.74</td><td>0.02%</td><td>Fixed 4.0/6.0/8.0 vs context-marginal 7.82 runs valuation.</td></tr>
      <tr><td>Scoring Model Formulation (m_model)</td><td>1.76</td><td>0.00%</td><td>1.26</td><td>0.00%</td><td>Model A (absolute) vs Model B (lift) formulation shift.</td></tr>
      <tr><td>Shrinkage Strength (k_shrink)</td><td>0.99</td><td>0.00%</td><td>1.12</td><td>0.00%</td><td>Regularization penalty strength (K=60, 120, 180).</td></tr>
      <tr><td>Metric Component Weights (s_weights)</td><td>0.37</td><td>0.00%</td><td>0.13</td><td>0.00%</td><td>Local perturbations of run/wicket/boundary weights.</td></tr>
      <tr><td><strong>Player &times; Specification Interaction</strong></td><td><strong>11,251.00</strong></td><td><strong>21.44%</strong></td><td><strong>25,308.16</strong></td><td><strong>32.79%</strong></td><td><strong>Measures individual player sensitivity across specifications.</strong></td></tr>
      <tr><td><strong>Total Sum of Squares</strong></td><td><strong>52,486.26</strong></td><td><strong>100.00%</strong></td><td><strong>77,176.40</strong></td><td><strong>100.00%</strong></td><td><strong>Sequential decomposition sums to exactly 100.00%.</strong></td></tr>
    </tbody>
  </table>

  <p style="font-size:7.2pt; margin-top:2px;">Because percentile ranks within every specification have mean 0.50 by construction, main effects of specification dimensions sum to under 2%. The meaningful methodological sensitivity lies in the <strong>Player &times; Specification Interaction</strong> (21.44% for batters, 32.79% for bowlers). This confirms that individual player rankings shift across choices, demonstrating why reporting consensus frequencies across the multiverse is vastly more reliable than relying on any single specification.</p>

  <img class="chart-img" style="max-height:160px;" src="{(ROOT / 'outputs' / 'submission_final' / 'charts' / 'fig1_variance_decomposition_aligned.png').as_uri()}" alt="Sequential Type I ANOVA Variance Decomposition">

  <div class="footer-note">
    <span>ANOVA computed on balanced panel of qualifying players across specifications.</span>
    <span>Page 7 of 15</span>
  </div>
</div>

<!-- PAGE 7: BATTING CONSENSUS RANKINGS & PROFILES (1-5) -->
<div class="page" id="p7">
  <div class="header-bar">
    <div class="header-title">Consensus Batting Rankings & Profiles</div>
    <div class="header-sub">Multiverse Results & Empirical Evidence (Ranks 1 to 5)</div>
  </div>

  <div class="section-heading">8A. Top-10 Batters: Comprehensive Performance Table</div>
  <table>
    <thead>
      <tr>
        <th>#</th>
        <th style="text-align:left;">Player (ID)</th>
        <th>Tier</th>
        <th>Shrunk PWI</th>
        <th>Normal</th>
        <th>Raw Lift</th>
        <th>Maint Lift</th>
        <th>HP Balls</th>
        <th>Elig %</th>
        <th>Top-10 %</th>
        <th>Med [IQR]</th>
        <th>Boot 90% CI</th>
        <th>Rises %</th>
        <th>Classification</th>
      </tr>
    </thead>
    <tbody>
      {make_table2a_rows()}
    </tbody>
  </table>

  <div class="sub-heading">Detailed Empirical Evidence: Batters 1 to 5</div>
  <p><strong>1. Shashank Singh (ID: 2756) — Tier 1 | Classification: Rises under pressure:</strong> Shashank finishes inside the Top 10 across <strong>94.9%</strong> of valid multiverse specifications with a median rank of 5.0 (IQR 3.0). Across 327 high-pressure balls, he generates a shrunk PWI of <strong>+32.2</strong> runs/100b with a raw lift of <strong>+22.2</strong> over normal situations. Rises under pressure in <strong>100.0%</strong> of specifications. In 1,000 bootstrap draws, he achieves 996 eligible finishes with a 90% rank interval of <strong>[1, 44]</strong>. IPL 2026 Team (raw data): Punjab Kings. Availability for IPL 2027: UNVERIFIED. Tactical Fit: Strong candidate, if available at auction, to partner Donovan Ferreira in death-overs hitting.</p>

  <p><strong>2. Tim David (ID: 6396) — Tier 1 | Classification: Rises under pressure:</strong> Tim David posts the single highest shrunk high-pressure impact in the competition database at <strong>+42.9</strong> runs/100b. He achieves top-10 inclusion in <strong>92.1%</strong> of specifications with a median rank of 1.0 (IQR 2.0). Supported by 570 high-pressure balls and 1,000/1,000 bootstrap draws, his raw lift is +9.0 runs/100b with a 90% bootstrap interval of <strong>[1, 16]</strong>. Rises under pressure in <strong>78.1%</strong> of specifications. IPL 2026 Team (raw data): Royal Challengers Bengaluru. Availability: UNVERIFIED. Tactical Fit: High-impact boundary asset, if available at auction, to provide overseas death-overs boundary power.</p>

  <p><strong>3. Naman Dhir (ID: 37052) — Tier 1 | Classification: Rises under pressure:</strong> Dhir demonstrates a raw pressure lift of <strong>+35.4</strong> runs/100b (shrunk PWI +34.7 vs. normal -0.7). He finishes top-10 in <strong>88.6%</strong> of specifications with a median rank of 4.0. Eligible in 908/1,000 bootstrap draws with a 90% interval of <strong>[1, 32]</strong>. Rises under pressure in <strong>100.0%</strong> of specifications. IPL 2026 Team (raw data): Mumbai Indians. Availability: UNVERIFIED. Tactical Fit: High-lift Indian middle-order option, if available at auction, providing versatile acceleration.</p>

  <p><strong>4. Dinesh Karthik (ID: 143) — Tier 2 | Classification: Rises under pressure:</strong> Karthik achieves candidate eligibility in <strong>100.0%</strong> and Top-10 inclusion in <strong>78.3%</strong> of multiverse specifications across 250 HP balls, generating a shrunk PWI of +34.4 with a raw lift of +16.1. Eligible in 994/1,000 bootstrap draws with median rank 5.0 and 90% interval of <strong>[1, 44]</strong>. Rises under pressure in <strong>80.0%</strong> of specifications. Status: Historical benchmark — retired from active IPL play after the 2024 season; active Royal Challengers Bengaluru Batting Coach & Mentor (2025–2026). Retained as an empirical performance benchmark rather than an actionable recruitment target.</p>

  <p><strong>5. Heinrich Klaasen (ID: 4260) — Tier 2 | Classification: Rises under pressure:</strong> Klaasen secures a <strong>74.4%</strong> top-10 frequency across 459 HP balls with shrunk PWI +24.9 and raw lift +3.4. Median rank is 7.0, supported by 999/1,000 bootstrap draws with 90% interval of <strong>[5, 34]</strong>. Rises under pressure in <strong>80.0%</strong> of specifications. IPL 2026 Team (raw data): Sunrisers Hyderabad. Availability: UNVERIFIED. Tactical Fit: Premier middle-overs boundary engine, if available at auction, maintaining high baseline output.</p>

  <div class="footer-note">
    <span>Metrics evaluated per 100 balls above context baseline. Shrunk via Empirical Bayes (K=120).</span>
    <span>Page 8 of 15</span>
  </div>
</div>

<!-- PAGE 8: BATTING PROFILES CONTINUED (6-10) & CHART -->
<div class="page" id="p8">
  <div class="header-bar">
    <div class="header-title">Batting Profiles Continued & Resilience Landscape</div>
    <div class="header-sub">Evidence for Batters 6 to 10</div>
  </div>

  <div class="sub-heading">Detailed Empirical Evidence: Batters 6 to 10</div>
  <p><strong>6. Suryakumar Yadav (ID: 1699) — Tier 2 | Classification: Elite all the time:</strong> Suryakumar features in the Top 10 across <strong>73.1%</strong> of specifications with a median rank of 8.0 (IQR 6.0) across 657 high-pressure balls. Shrunk PWI is +25.4 runs/100b. His raw lift is -4.6 (reflecting a baseline of +30.0 runs/100b). Rises under pressure in <strong>23.3%</strong> of specifications. Eligible in 1,000/1,000 bootstrap draws with 90% interval of <strong>[6, 44]</strong>. IPL 2026 Team (raw data): Mumbai Indians. Availability: UNVERIFIED. Tactical Fit: Dominant middle-overs boundary creator, if available at auction, whose high output holds against defensive fields.</p>

  <p><strong>7. Rinku Singh (ID: 4708) — Tier 2 | Classification: Rises under pressure:</strong> Rinku achieves a <strong>63.1%</strong> multiverse frequency across 507 HP balls, recording a shrunk PWI of +31.0 and a raw lift of +17.9 runs/100b. Eligible in 1,000/1,000 bootstrap draws with median rank 9.0 and 90% interval of <strong>[2, 39]</strong>. Rises under pressure in <strong>80.0%</strong> of specifications. IPL 2026 Team (raw data): Kolkata Knight Riders. Availability: UNVERIFIED. Tactical Fit: High-performing left-handed chase finisher, if available at auction, with consistent execution.</p>

  <p><strong>8. Romario Shepherd (ID: 6726) — Tier 2 | Classification: Balanced / Context-dependent:</strong> Shepherd records a <strong>55.5%</strong> top-10 frequency with median rank 6.0 across 431 HP balls. Shrunk PWI is +28.7 runs/100b with +5.0 raw lift. Eligible in 1,000/1,000 bootstrap draws with 90% interval of <strong>[2, 36]</strong>. Rises under pressure in <strong>49.1%</strong> of specifications. IPL 2026 Team (raw data): Royal Challengers Bengaluru. Availability: UNVERIFIED. Tactical Fit: Explosive lower-order hitter, if available at auction, adding depth to death-overs batting.</p>

  <p><strong>9. Andre Russell (ID: 1318) — Tier 2 | Classification: Elite all the time:</strong> Russell achieves candidate eligibility in <strong>100.0%</strong> and Top-10 inclusion in <strong>54.2%</strong> of multiverse specifications across 347 HP balls with shrunk PWI +31.8 and +1.0 raw lift. Eligible in 1,000/1,000 bootstrap draws with median rank 10.0 and 90% interval of <strong>[2, 54]</strong>. Elite across all match states in <strong>82.2%</strong> of specifications (normal baseline +30.9). Status: Historical benchmark — retired from IPL on 30 Nov 2025; active Kolkata Knight Riders Power Coach for IPL 2026 while continuing in select non-IPL leagues. Serves as a prime baseline for elite late-innings power-hitting.</p>

  <p><strong>10. Rashid Khan (ID: 4722) — Tier 3 | Classification: Rises under pressure:</strong> Rashid achieves candidate eligibility in <strong>77.8%</strong> of multiverse specifications and finishes inside the Top 10 in <strong>47.9%</strong> of specifications (retaining a top-10 position in <strong>61.6%</strong> of specifications where eligible), across 377 HP balls with shrunk PWI +28.1 and raw lift of <strong>+40.3</strong> runs/100b (normal baseline -12.2). Supported by 994/1,000 bootstrap draws with median rank 8.0 and 90% interval of <strong>[1, 40]</strong>. Rises under pressure in <strong>99.3%</strong> of specifications. IPL 2026 Team (raw data): Gujarat Titans. Availability: UNVERIFIED. Tactical Fit: Dual-threat asset, if available at auction, providing lower-order batting lift alongside frontline bowling.</p>

  <img class="chart-img" style="max-height:175px;" src="{uri_chart('fig2_maintenance_vs_lift_batters.png')}" alt="Batting Maintenance vs Lift Landscape">

  <div class="footer-note">
    <span>Matthew Wade (multiverse frequency 52.96%) removed due to 720/1,000 bootstrap stability failure.</span>
    <span>Page 9 of 15</span>
  </div>
</div>

<!-- PAGE 9: BOWLING CONSENSUS RANKINGS & PROFILES (1-5) -->
<div class="page" id="p9">
  <div class="header-bar">
    <div class="header-title">Consensus Bowling Rankings & Profiles</div>
    <div class="header-sub">Defending-Side Evaluation & Empirical Evidence (Ranks 1 to 5)</div>
  </div>

  <div class="section-heading">8B. Top-10 Bowlers: Comprehensive Performance Table</div>
  <table>
    <thead>
      <tr>
        <th>#</th>
        <th style="text-align:left;">Player (ID)</th>
        <th>Tier</th>
        <th>Shrunk PWI</th>
        <th>Normal</th>
        <th>Raw Lift</th>
        <th>Maint Lift</th>
        <th>HP Balls</th>
        <th>Elig %</th>
        <th>Top-10 %</th>
        <th>Med [IQR]</th>
        <th>Boot 90% CI</th>
        <th>Rises %</th>
        <th>Classification</th>
      </tr>
    </thead>
    <tbody>
      {make_table2b_rows()}
    </tbody>
  </table>

  <div class="sub-heading">Detailed Empirical Evidence: Bowlers 1 to 5</div>
  <p><strong>1. Sunil Narine (ID: 781) — Tier 1 | Classification: Balanced / Context-dependent:</strong> Narine finishes inside the Top 10 in <strong>100.0%</strong> (99.97%) of valid multiverse specifications with a median rank of 3.0 (IQR 1.0). Across 422 high-pressure balls, his defending shrunk impact is <strong>+6.57</strong> runs saved/24b with raw lift of +0.64. In 1,000 bootstrap draws, he achieves 1,000 eligible finishes with a 90% rank interval of <strong>[1, 17]</strong>. Rises under pressure in <strong>52.5%</strong> of specifications. IPL 2026 Team (raw data): Kolkata Knight Riders. Availability for IPL 2027: UNVERIFIED. Tactical Fit: Defensive spin controller, if available at auction, to restrict middle-overs run rates.</p>

  <p><strong>2. Jasprit Bumrah (ID: 2933) — Tier 1 | Classification: Elite all the time:</strong> Bumrah records defending shrunk impact of <strong>+7.61</strong> runs saved/24b. He finishes inside the Top 10 across <strong>99.2%</strong> of specifications with median rank 2.0 (IQR 2.0). Supported by 332 HP balls and 999/1,000 bootstrap draws with 90% interval of <strong>[1, 23]</strong>. Raw lift is +0.33; rises under pressure in <strong>7.2%</strong> of specifications (normal baseline +7.28). IPL 2026 Team (raw data): Mumbai Indians. Availability: UNVERIFIED. Tactical Fit: Frontline pace anchor across all match phases, if available at auction.</p>

  <p><strong>3. Rashid Khan (ID: 4722) — Tier 1 | Classification: Rises under pressure:</strong> Rashid achieves a <strong>93.5%</strong> multiverse frequency across 706 HP balls. Defending shrunk impact is <strong>+5.59</strong> runs saved/24b with raw lift of <strong>+2.75</strong>. Supported by 1,000/1,000 bootstrap draws with median rank 5.0 and 90% interval of <strong>[1, 19]</strong>. Rises under pressure in <strong>99.2%</strong> of specifications. IPL 2026 Team (raw data): Gujarat Titans. Availability: UNVERIFIED. Tactical Fit: Attacking wrist-spin option, if available at auction, addressing middle-overs economy deficits.</p>

  <p><strong>4. Matheesha Pathirana (ID: 8661) — Tier 1 | Classification: Elite all the time:</strong> Pathirana achieves candidate eligibility in <strong>100.0%</strong> and Top-10 inclusion in <strong>83.4%</strong> of multiverse specifications across 307 HP balls, recording defending shrunk impact of +5.34 runs saved/24b and +1.21 raw lift. Supported by 1,000/1,000 bootstrap draws with median rank 3.0 and 90% interval of <strong>[1, 41]</strong>. Elite across all match states in <strong>77.8%</strong> of specifications. IPL 2026 Team (raw data): Kolkata Knight Riders (mapped in competition_team_player_mapping.csv). Availability: UNVERIFIED. Note: Sustained confirmed hamstring injury on 16 May 2026 (replaced by Luvnith Sisodia for remainder of season); actively rehabilitating; do not assume 2027 unavailability. Tactical Fit: Specialist death bowler, if available at auction, providing strong run restriction (+5.34 runs saved/24b).</p>

  <p><strong>5. Eshan Malinga (ID: 39657) — Tier 2 | Classification: Rises under pressure:</strong> Malinga posts a <strong>71.9%</strong> top-10 frequency across 176 HP balls with defending impact +3.85 runs saved/24b and raw lift of +3.39. Qualified in 912/1,000 bootstrap draws with median rank 6.0 and 90% interval of <strong>[1, 38]</strong>. Rises under pressure in <strong>74.4%</strong> of specifications. IPL 2026 Team (raw data): Sunrisers Hyderabad (mapped in competition_team_player_mapping.csv). Availability: UNVERIFIED. Tactical Fit: Emerging pace option, if available at auction, demonstrating significant lift (+3.39) under leverage.</p>

  <div class="footer-note">
    <span>Bowling metrics evaluated per 24 legal balls. Bowler P0 single-index excluded from selection.</span>
    <span>Page 10 of 15</span>
  </div>
</div>

<!-- PAGE 10: BOWLING PROFILES CONTINUED (6-10) & CHART -->
<div class="page" id="p10">
  <div class="header-bar">
    <div class="header-title">Bowling Profiles Continued & Resilience Landscape</div>
    <div class="header-sub">Evidence for Bowlers 6 to 10</div>
  </div>

  <div class="sub-heading">Detailed Empirical Evidence: Bowlers 6 to 10</div>
  <p><strong>6. Nathan Ellis (ID: 7920) — Tier 2 | Classification: Rises under pressure:</strong> Ellis achieves candidate eligibility in <strong>75.5%</strong> and Top-10 inclusion in <strong>54.8%</strong> of multiverse specifications (retaining top 10 in <strong>72.5%</strong> when eligible) across 229 HP balls with defending shrunk impact +5.50 runs saved/24b and raw lift +3.15. Supported by 988/1,000 bootstrap draws with median rank 7.0 and 90% interval of <strong>[1, 36]</strong>. Rises under pressure in <strong>65.9%</strong> of specifications. IPL 2026 Team (raw data): Chennai Super Kings (mapped in competition_team_player_mapping.csv; subsequently traded CSK &rarr; SRH on 5 Nov 2026 for INR 2.00 Cr all-cash [Official SRH/IPL confirmation]). Availability: UNVERIFIED (contingent on SRH retention/trade decisions). Tactical Fit: Tactical death-overs target, if available at auction, to replace high-economy supporting overs.</p>

  <p><strong>7. Noor Ahmad (ID: 7967) — Tier 3 | Classification: Balanced / Context-dependent:</strong> Noor finishes top-10 in <strong>40.1%</strong> of specifications across 351 HP balls with defending impact +2.54 runs saved/24b. Eligible in 1,000/1,000 bootstrap draws with median rank 12.0 and 90% interval of <strong>[6, 62]</strong>. Rises under pressure in <strong>54.5%</strong> of specifications. IPL 2026 Team (raw data): Chennai Super Kings (mapped in competition_team_player_mapping.csv). Availability: UNVERIFIED. Tactical Fit: Left-arm wrist-spinner, if available at auction, providing middle-overs control.</p>

  <p><strong>8. Arshdeep Singh (ID: 6464) — Tier 3 | Classification: Balanced / Context-dependent:</strong> Arshdeep achieves candidate eligibility in <strong>100.0%</strong> and Top-10 inclusion in <strong>35.1%</strong> of multiverse specifications across 593 HP balls with defending impact +1.90 runs saved/24b and raw lift +0.99. Supported by 1,000/1,000 bootstrap draws with 90% interval of <strong>[9, 55]</strong>. Rises under pressure in <strong>55.8%</strong> of specifications. IPL 2026 Team (raw data): Punjab Kings (mapped in competition_team_player_mapping.csv; traded PBKS &rarr; MI on 11 Nov 2026 in player-swap for Hardik Pandya [Official IPL announcement]). Availability: UNVERIFIED (contingent on MI retention). Tactical Fit: Indian left-arm seam option across powerplay and death overs, if available at auction.</p>

  <p><strong>9. Prasidh Krishna (ID: 4489) — Tier 3 | Classification: Rises under pressure:</strong> Prasidh achieves a <strong>31.7%</strong> top-10 frequency across 234 HP balls with defending impact +2.96 runs saved/24b and raw lift +2.67. Supported by 994/1,000 bootstrap draws with median rank 13.0 and 90% interval of <strong>[5, 63]</strong>. Rises under pressure in <strong>68.3%</strong> of specifications. IPL 2026 Team (raw data): Gujarat Titans (mapped in competition_team_player_mapping.csv). Availability: UNVERIFIED. Tactical Fit: Hit-the-deck pace bowler with strong raw lift (+2.67), if available at auction.</p>

  <p><strong>10. Bhuvneshwar Kumar (ID: 360) — Tier 3 | Classification: Elite all the time:</strong> Bhuvneshwar finishes top-10 in <strong>27.2%</strong> of specifications across 361 HP balls with defending impact +3.25 runs saved/24b. Supported by 1,000/1,000 bootstrap draws with 90% interval of <strong>[7, 56]</strong>. Rises under pressure in <strong>1.9%</strong> of specifications (normal baseline +4.56). IPL 2026 Team (raw data): Royal Challengers Bengaluru (mapped in competition_team_player_mapping.csv). Availability: UNVERIFIED. Tactical Fit: Experienced new-ball swing bowler with disciplined control, if available at auction.</p>

  <img class="chart-img" style="max-height:175px;" src="{uri_chart('fig3_maintenance_vs_lift_bowlers.png')}" alt="Bowling Maintenance vs Lift Landscape">

  <div class="footer-note">
    <span>Mujeeb (draws: 744) and Naveen (draws: 513) removed due to bootstrap stability failure.</span>
    <span>Page 11 of 15</span>
  </div>
</div>

<!-- PAGE 11: RAJASTHAN ROYALS SQUAD AUDIT & PHASE EVIDENCE -->
<div class="page" id="p11">
  <div class="header-bar">
    <div class="header-title">Rajasthan Royals Tactical Recruitment Dossier</div>
    <div class="header-sub">IPL 2026 Phase-Level Audit from Raw Data</div>
  </div>

  <div class="section-heading">9. Rajasthan Royals 2026 Performance Audit & Tactical Planning</div>
  <p>To ensure recruitment recommendations are actionable for Rajasthan Royals, I audited RR's actual 2026 IPL campaign directly from raw match records (matches.csv, ball_by_ball.csv, and playing_eleven.csv). RR played 16 matches in 2026, captained primarily by Riyan Parag (14 matches) with Yashasvi Jaiswal leading in 2 matches (Sanju Samson represented Chennai Super Kings in 2026).</p>

  <div class="sub-heading">Audited Rajasthan Royals 2026 Squad Performance (from raw data)</div>
  <table>
    <thead>
      <tr>
        <th style="text-align:left;">Player Name (ID)</th>
        <th>Actual Apps</th>
        <th>Runs</th>
        <th>Balls</th>
        <th>Bat SR</th>
        <th>Overs</th>
        <th>Runs Conc</th>
        <th>Wkts</th>
        <th>Bowl ER</th>
      </tr>
    </thead>
    <tbody>
      <tr><td style="text-align:left;">Vaibhav Sooryavanshi (50284)</td><td>16</td><td>776</td><td>327</td><td><strong>237.31</strong></td><td>0.0</td><td>0</td><td>0</td><td>&mdash;</td></tr>
      <tr><td style="text-align:left;">Dhruv Jurel (7260)</td><td>16</td><td>515</td><td>333</td><td>154.65</td><td>0.0</td><td>0</td><td>0</td><td>&mdash;</td></tr>
      <tr><td style="text-align:left;">Yashasvi Jaiswal (6819)</td><td>16</td><td>427</td><td>280</td><td>152.50</td><td>0.0</td><td>0</td><td>0</td><td>&mdash;</td></tr>
      <tr><td style="text-align:left;">Jofra Archer (3298)</td><td>16</td><td>64</td><td>47</td><td>136.17</td><td><strong>60.0</strong></td><td>559</td><td><strong>25</strong></td><td>9.32</td></tr>
      <tr><td style="text-align:left;">Donovan Ferreira (8182)</td><td>15</td><td>317</td><td>177</td><td>179.10</td><td>3.0</td><td>41</td><td>1</td><td>13.67</td></tr>
      <tr><td style="text-align:left;">Riyan Parag (6423) [Captain]</td><td>14</td><td>309</td><td>196</td><td>157.65</td><td>4.0</td><td>38</td><td>2</td><td>9.50</td></tr>
      <tr><td style="text-align:left;">Ravindra Jadeja (152)</td><td>14</td><td>266</td><td>197</td><td>135.03</td><td>33.0</td><td>277</td><td>10</td><td>8.39</td></tr>
      <tr><td style="text-align:left;">Nandre Burger (7312)</td><td>13</td><td>14</td><td>9</td><td>155.56</td><td>43.5</td><td>440</td><td>14</td><td><strong>10.11</strong></td></tr>
      <tr><td style="text-align:left;">Brijesh Sharma (67036)</td><td>13</td><td>2</td><td>4</td><td>50.00</td><td>45.5</td><td>450</td><td>14</td><td><strong>9.89</strong></td></tr>
      <tr><td style="text-align:left;">Ravi Bishnoi (7503)</td><td>9</td><td>0</td><td>3</td><td>0.00</td><td>26.0</td><td>257</td><td>11</td><td>9.88</td></tr>
      <tr><td style="text-align:left;">Shimron Hetmyer (3297)</td><td>8</td><td>78</td><td>69</td><td><strong>113.04</strong></td><td>0.0</td><td>0</td><td>0</td><td>&mdash;</td></tr>
      <tr><td style="text-align:left;">Tushar Deshpande (6806)</td><td>7</td><td>26</td><td>14</td><td>185.71</td><td>23.0</td><td>275</td><td>4</td><td><strong>11.96</strong></td></tr>
      <tr><td style="text-align:left;">Sandeep Sharma (2411)</td><td>6</td><td>0</td><td>0</td><td>&mdash;</td><td><strong>19.4</strong></td><td>224</td><td>5</td><td><strong>11.39</strong></td></tr>
      <tr><td style="text-align:left;">Kuldeep Sen (7545)</td><td>0</td><td>0</td><td>0</td><td>&mdash;</td><td>0.0</td><td>0</td><td>0</td><td>&mdash;</td></tr>
    </tbody>
  </table>

  <div class="sub-heading">Phase-Level Evidence & Strategic Recruitment Opportunities</div>
  <p>Auditing deliveries by match phase from data/raw identifies three tactical focal areas for Rajasthan Royals:</p>
  <ul>
    <li><strong>1. Death-Overs Bowling Execution (Overs 16–20):</strong> RR's team economy rate at the death was <strong>10.60</strong>, closely matching the league death average of <strong>10.67</strong> (indicating league-average team performance overall). However, individual variance was severe: Jofra Archer (ER 9.35) and Nandre Burger (ER 9.33) bowled well, whereas Sandeep Sharma conceded <strong>13.70</strong> runs/over across 46 death balls and Tushar Deshpande conceded <strong>12.38</strong> across 48 death balls. <em>Recruitment Opportunity:</em> If available at auction, targeted death seamers like Nathan Ellis (+5.50 shrunk impact) or Eshan Malinga (+3.39 raw lift) provide options to replace expensive supporting death overs.</li>
    <li><strong>2. Middle-Overs Spin Economy (Overs 7–15):</strong> In the middle overs, RR's spin group conceded <strong>9.29</strong> runs/over across all spinners (9.19 for Jadeja, Punja, and Bishnoi) compared to the league spin average of <strong>8.97</strong> (a visible control gap). While Ravindra Jadeja maintained a solid economy of <strong>8.39</strong>, secondary spinners conceded higher rates: Yash Punja (41503) posted ER <strong>9.54</strong> and Ravi Bishnoi posted ER <strong>10.11</strong> (with a dot ball rate of only 21.9%). <em>Recruitment Opportunity:</em> If available at auction, adding a controlling wrist-spinner like Noor Ahmad or Rashid Khan would help bridge the middle-overs spin economy gap.</li>
    <li><strong>3. Death-Overs Batting Support (Overs 16–20):</strong> At the death, Donovan Ferreira produced a strike rate of <strong>221.7</strong> across 83 death balls (well above the league death average of 169.4). However, secondary death hitters lacked comparable boundary production: Ravindra Jadeja recorded SR <strong>140.5</strong>, Shubham Dubey recorded SR <strong>146.3</strong>, and Shimron Hetmyer scored at SR <strong>121.1</strong> (78 runs off 69 balls overall). <em>Recruitment Opportunity:</em> RR requires a second, preferably Indian, death hitter. If available at auction, Shashank Singh (+22.2 raw lift) or Naman Dhir (+35.4 raw lift) would effectively complement Ferreira.</li>
  </ul>

  <div class="footer-note">
    <span>Audited strictly from raw tables. Actual appearances verified via playing_eleven.is_played == 1.</span>
    <span>Page 12 of 15</span>
  </div>
</div>

<!-- PAGE 12: EMPIRICAL VALIDATION & WALK-FORWARD -->
<div class="page" id="p12">
  <div class="header-bar">
    <div class="header-title">Model Reliability, Limitations & Walk-Forward Validation</div>
    <div class="header-sub">Out-of-Sample Performance & Stability Checks</div>
  </div>

  <div class="section-heading">10. Walk-Forward Temporal Validation (2022–2024 to 2025–2026)</div>
  <p>To evaluate out-of-sample predictive validity honestly, models trained on 2022–2024 data were tested against out-of-sample 2025–2026 performance on the canonical specification:</p>
  <ul>
    <li><strong>Canonical Batting Stability:</strong> Spearman r = 0.0508 (p = 0.7864, uninformative out-of-sample across 31 common players).</li>
    <li><strong>Canonical Bowling Stability:</strong> Spearman r = 0.2646 (p = 0.0721, modest positive correlation across 47 common players).</li>
  </ul>
  <p><strong>Methodological Finding:</strong> Batting pressure rankings are <strong>descriptive, not predictive</strong>. High-pressure batting over a single season or two-season window contains substantial noise, situational variance, and role volatility. Historical pressure metrics describe what occurred under specific match conditions rather than guaranteeing future replication. Bowling pressure performance demonstrates modest stability (r = 0.26), but still contains significant season-to-season variation.</p>

  <div class="sub-heading">Bootstrap Stability Hurdle: Excluded Candidates</div>
  <p>Applying the 1,000-draw stratified match bootstrap hurdle (&ge;800 valid eligible resamples) removed volatile fringe players:</p>
  <ul>
    <li><strong>Matthew Wade (ID: 796):</strong> Achieved 52.96% multiverse top-10 frequency across eligible specifications, but only qualified in <strong>720 / 1,000</strong> bootstrap resamples, failing the pre-registered &ge;800 stability hurdle. Status: Retired from international cricket (Oct 2024) and Australian domestic cricket (BBL / state cricket in Sep 2026 to take up coaching duties); has not participated in recent IPL auctions. His exclusion strictly on bootstrap stability grounds promoted Rashid Khan (#10) into the final batting list.</li>
    <li><strong>Mujeeb Ur Rahman (ID: 6450):</strong> Achieved 49.14% multiverse top-10 frequency, but qualified in only <strong>744 / 1,000</strong> bootstrap resamples.</li>
    <li><strong>Naveen ul Haq (ID: 5809):</strong> Achieved 48.74% multiverse top-10 frequency, but qualified in only <strong>513 / 1,000</strong> bootstrap resamples.</li>
    <li>Their removal promoted Prasidh Krishna (#9) and Bhuvneshwar Kumar (#10) into the final bowling list.</li>
  </ul>

  <div class="grid-2">
    <div>
      <img class="chart-img" style="max-height:170px;" src="{uri_chart('fig4_bootstrap_stability_batters.png')}" alt="Batting Bootstrap Stability">
    </div>
    <div>
      <img class="chart-img" style="max-height:170px;" src="{uri_chart('fig5_bootstrap_stability_bowlers.png')}" alt="Bowling Bootstrap Stability">
    </div>
  </div>

  <div class="footer-note">
    <span>Walk-forward evaluated on unpenalized Spearman rank correlation between time periods.</span>
    <span>Page 13 of 15</span>
  </div>
</div>

<!-- PAGE 13: PLAYERS NEXT IN LINE & STRATEGIC ALTERNATIVES -->
<div class="page" id="p13">
  <div class="header-bar">
    <div class="header-title">Players Next in Line (Ranks 11–15) & Strategic Alternatives</div>
    <div class="header-sub">Depth Charts & Contingency Targets</div>
  </div>

  <div class="section-heading">11. Batters Next in Line (Ranks 11 to 15)</div>
  <table style="font-size:7pt;">
    <thead>
      <tr><th>#</th><th style="text-align:left;">Player Name (ID)</th><th>Multi Top-10 %</th><th>Med [IQR]</th><th>Boot Draws</th><th style="text-align:left;">Strategic Role & Tactical Context</th></tr>
    </thead>
    <tbody>
      <tr><td>11</td><td style="text-align:left;">Ashutosh Sharma (8101)</td><td>38.20%</td><td>9.0 [11.0]</td><td>662 / 1000</td><td style="text-align:left;">Lower-order finisher (+29.7 raw lift); sample volatility in bootstrap resamples.</td></tr>
      <tr><td>12</td><td style="text-align:left;">Shreyas Iyer (3647)</td><td>32.62%</td><td>14.0 [12.0]</td><td>999 / 1000</td><td style="text-align:left;">Middle-order spin anchor; solid baseline but moderate pressure lift (+4.2).</td></tr>
      <tr><td>13</td><td style="text-align:left;">Mahendra Singh Dhoni (8)</td><td>23.79%</td><td>14.0 [12.0]</td><td>978 / 1000</td><td style="text-align:left;">Veteran death finisher (+14.8 raw lift); lower volume in international format scope.</td></tr>
      <tr><td>14</td><td style="text-align:left;">Nicholas Pooran (3125)</td><td>12.61%</td><td>22.0 [14.0]</td><td>1000 / 1000</td><td style="text-align:left;">High baseline overseas middle-order hitter; qualifies across all specifications.</td></tr>
      <tr><td>15</td><td style="text-align:left;">Namboori Tilak Varma (7897)</td><td>11.50%</td><td>24.0 [15.0]</td><td>1000 / 1000</td><td style="text-align:left;">Versatile Indian top/middle-order batter with solid cross-format baseline.</td></tr>
    </tbody>
  </table>
  <p style="font-size:6.8pt; color:#4A5568; margin-top:-2px;"><em>(Note: Reeza Hendricks achieved 26.37% top-10 frequency across specifications where he qualified, but was excluded from the candidate pool because his overall eligibility was 35.59%, below the pre-registered 50% candidate gate).</em></p>

  <div class="section-heading">12. Bowlers Next in Line (Ranks 11 to 15)</div>
  <table style="font-size:7pt;">
    <thead>
      <tr><th>#</th><th style="text-align:left;">Player Name (ID)</th><th>Multi Top-10 %</th><th>Med [IQR]</th><th>Boot Draws</th><th style="text-align:left;">Strategic Role & Tactical Context</th></tr>
    </thead>
    <tbody>
      <tr><td>11</td><td style="text-align:left;">Krunal Pandya (4219)</td><td>26.17%</td><td>14.0 [12.0]</td><td>1000 / 1000</td><td style="text-align:left;">Defensive left-arm orthodox spinner (+2.41 raw lift); excellent economy discipline.</td></tr>
      <tr><td>12</td><td style="text-align:left;">Alzarri Joseph (3275)</td><td>26.14%</td><td>24.0 [15.0]</td><td>1000 / 1000</td><td style="text-align:left;">Overseas pace strike option; effective in short high-leverage bursts.</td></tr>
      <tr><td>13</td><td style="text-align:left;">Mohammad Nawaz (2490)</td><td>24.85%</td><td>11.0 [10.0]</td><td>990 / 1000</td><td style="text-align:left;">Left-arm spinner (+2.15 raw lift); derived strictly from international T20I matches.</td></tr>
      <tr><td>14</td><td style="text-align:left;">T Natarajan (4265)</td><td>22.40%</td><td>18.0 [11.0]</td><td>1000 / 1000</td><td style="text-align:left;">Specialized Indian death bowler; strong consistency under pressure.</td></tr>
      <tr><td>15</td><td style="text-align:left;">Ravi Bishnoi (7503)</td><td>21.80%</td><td>19.0 [12.0]</td><td>1000 / 1000</td><td style="text-align:left;">Attacking Indian leg-spinner; currently on RR roster (ER 9.88 in 2026).</td></tr>
    </tbody>
  </table>
  <p style="font-size:6.8pt; color:#4A5568; margin-top:-2px;"><em>(Note: Abbas Afridi achieved 27.83% top-10 frequency across lenient specifications, but qualified in only 40.03% of specifications, failing the 50% candidate gate. Pakistani players have historically not participated in the IPL player auction since 2008 and 2027 auction registration/eligibility remains unconfirmed; their metrics derive strictly from international T20Is).</em></p>

  <div class="sub-heading">Strategic Recruitment Summary for Rajasthan Royals</div>
  <p style="font-size:7.4pt;">Auction dynamics dictate that elite Tier 1 assets (Bumrah, Narine, Klaasen) are franchise cornerstones who will likely to be retained. RR's practical recruitment focus must concentrate on actionable high-ceiling players who could address these needs, if available at auction: Shashank Singh and Naman Dhir to partner Ferreira in death batting, and Nathan Ellis and Eshan Malinga to provide dependable death overs.</p>

  <div class="footer-note">
    <span>Depth charts evaluated across all 15,150 multiverse specifications.</span>
    <span>Page 14 of 15</span>
  </div>
</div>

<!-- PAGE 14: APPENDIX & METHODOLOGICAL REPRODUCIBILITY -->
<div class="page" id="p14">
  <div class="header-bar">
    <div class="header-title">Appendix: Baseline Lists & Reproducibility</div>
    <div class="header-sub">Governance, Mathematical Formulas & Audit Log</div>
  </div>

  <div class="section-heading">Appendix A: Unfiltered Canonical Baseline Top-10 Lists</div>
  <div class="grid-2">
    <div>
      <div class="sub-heading">Canonical Batters (Specification P2-W1-Model B)</div>
      <table style="font-size:7pt;">
        <thead>
          <tr><th>#</th><th style="text-align:left;">Player</th><th>PWI</th><th>Raw Lift</th></tr>
        </thead>
        <tbody>
          <tr><td>1</td><td style="text-align:left;">Tim David (6396)</td><td>+42.9</td><td>+9.0</td></tr>
          <tr><td>2</td><td style="text-align:left;">Naman Dhir (37052)</td><td>+34.7</td><td>+35.4</td></tr>
          <tr><td>3</td><td style="text-align:left;">Matthew Wade* (796)</td><td>+31.7</td><td>+35.7</td></tr>
          <tr><td>4</td><td style="text-align:left;">Romario Shepherd (6726)</td><td>+28.7</td><td>+5.0</td></tr>
          <tr><td>5</td><td style="text-align:left;">Rashid Khan (4722)</td><td>+28.1</td><td>+40.3</td></tr>
          <tr><td>6</td><td style="text-align:left;">Reeza Hendricks^ (768)</td><td>+31.5</td><td>+27.8</td></tr>
          <tr><td>7</td><td style="text-align:left;">Shashank Singh (2756)</td><td>+32.2</td><td>+22.2</td></tr>
          <tr><td>8</td><td style="text-align:left;">Heinrich Klaasen (4260)</td><td>+24.9</td><td>+3.4</td></tr>
          <tr><td>9</td><td style="text-align:left;">Ashutosh Sharma (8101)</td><td>+31.6</td><td>+29.7</td></tr>
          <tr><td>10</td><td style="text-align:left;">Dinesh Karthik (143)</td><td>+34.4</td><td>+16.1</td></tr>
        </tbody>
      </table>
    </div>
    <div>
      <div class="sub-heading">Canonical Bowlers (Specification P2-W1-Model B)</div>
      <table style="font-size:7pt;">
        <thead>
          <tr><th>#</th><th style="text-align:left;">Player</th><th>PWI</th><th>Raw Lift</th></tr>
        </thead>
        <tbody>
          <tr><td>1</td><td style="text-align:left;">Sunil Narine (781)</td><td>+6.57</td><td>+0.64</td></tr>
          <tr><td>2</td><td style="text-align:left;">Jasprit Bumrah (2933)</td><td>+7.61</td><td>+0.33</td></tr>
          <tr><td>3</td><td style="text-align:left;">Rashid Khan (4722)</td><td>+5.59</td><td>+2.75</td></tr>
          <tr><td>4</td><td style="text-align:left;">Nathan Ellis (7920)</td><td>+5.50</td><td>+3.15</td></tr>
          <tr><td>5</td><td style="text-align:left;">Eshan Malinga (39657)</td><td>+3.85</td><td>+3.39</td></tr>
          <tr><td>6</td><td style="text-align:left;">Matheesha Pathirana (8661)</td><td>+5.34</td><td>+1.21</td></tr>
          <tr><td>7</td><td style="text-align:left;">Mujeeb Ur Rahman* (6450)</td><td>+5.06</td><td>+3.48</td></tr>
          <tr><td>8</td><td style="text-align:left;">Naveen ul Haq* (5809)</td><td>+3.20</td><td>+2.24</td></tr>
          <tr><td>9</td><td style="text-align:left;">Bhuvneshwar Kumar (360)</td><td>+3.25</td><td>-1.31</td></tr>
          <tr><td>10</td><td style="text-align:left;">Krunal Pandya (4219)</td><td>+3.22</td><td>+2.41</td></tr>
        </tbody>
      </table>
    </div>
  </div>
  <p style="font-size:6.8pt; color:#4A5568; margin-top:-2px;"><em>*Removed by bootstrap stability hurdle (<800 draws). ^Excluded by 50% candidate eligibility gate.</em></p>

  <div class="section-heading">Appendix B: Exact Pipeline Reproduction Commands</div>
  <p style="font-size:7.2pt; font-family:monospace; background-color:#F8FAFC; padding:4px; border:1px solid #E2E8F0;">
    # 1. Run Complete Multiverse Pipeline (15,150 specs / role; 3,196,444 evaluations):<br>
    python -m src.model_v4.run_multiverse_pipeline<br><br>
    # 2. Run Comprehensive Unit & Statistical Test Suite (54 passed):<br>
    python -m pytest tests/model_v2 tests/model_v3 tests/model_v4 -q<br><br>
    # 3. Verify Player IDs, Checksums & Sequential Variance Decomposition:<br>
    python outputs/submission_final/build_verification.py
  </p>

  <div class="section-heading">Appendix C: External Verification Citations & IPL 2026 Teams</div>
  <ul style="font-size:6.8pt; margin: 0; padding-left: 14px;">
    <li><strong>data/raw/competition_team_player_mapping.csv:</strong> Verified IPL 2026 teams: Pathirana (KKR), Prasidh (GT), Malinga (SRH), Ellis (CSK), Noor (CSK), Bhuvneshwar (RCB), Shepherd (RCB), David (RCB), Shashank (PBKS), Naman Dhir (MI), Klaasen (SRH), Suryakumar (MI), Rinku (KKR), Rashid (GT), Narine (KKR), Bumrah (MI).</li>
    <li><strong>Nathan Ellis (Sunrisers Hyderabad / IPL Official, 2026-11-05; accessed 2026-11-14):</strong> Mapped to CSK in IPL 2026 raw data; traded CSK &rarr; SRH on 5 Nov 2026 in an all-cash INR 2.00 Cr transaction. [Official]</li>
    <li><strong>Arshdeep Singh (iplt20.com, 2026-11-11; accessed 2026-11-14):</strong> Mapped to PBKS in IPL 2026 raw data; traded PBKS &rarr; MI on 11 Nov 2026 in swap deal for Hardik Pandya. [Official]</li>
    <li><strong>Matheesha Pathirana (KKR / ESPNcricinfo, 2026-05-18; accessed 2026-11-14):</strong> Suffered confirmed hamstring injury on 16 May 2026 and replaced by Luvnith Sisodia for remainder of season; actively rehabilitating; do not assume 2027 unavailability. [Official / Reputable Media]</li>
    <li><strong>Andre Russell (The Hindu, 2025-11-30; accessed 2026-11-12):</strong> Retired from IPL on 30 Nov 2025; appointed KKR Power Coach for IPL 2026 while continuing in select non-IPL leagues. [Reputable Media]</li>
    <li><strong>Dinesh Karthik (India TV News, 2024-07-01; accessed 2026-11-12):</strong> Retired after IPL 2024; active RCB Batting Coach & Mentor (2025-2026). [Reputable Media]</li>
    <li><strong>Matthew Wade (cricket.com.au, 2024-10-29 & 2026-09-17; accessed 2026-11-14):</strong> Retired from international cricket and Australian domestic cricket (BBL / state) to take up coaching duties. [Official]</li>
    <li><strong>Pakistani Players (BCCI / IPL Historical Record 2008–2026):</strong> Have historically not participated in the IPL player auction since 2008; 2027 auction registration/eligibility remains unconfirmed. [Historical Record]</li>
    <li><strong>All Other IPL 2027 Auction Statuses:</strong> Strictly marked <strong>UNVERIFIED</strong> as official BCCI auction lists remain unpublished.</li>
  </ul>

  <div class="footer-note">
    <span>Rajat Aggarwal | Participant — SupeRR Selector Season 2</span>
    <span>Page 15 of 15</span>
  </div>
</div>

</body>
</html>
"""

TEMP_HTML.write_text(html_content, encoding="utf-8")
print(f"Generated HTML template at {TEMP_HTML}")

# Compile PDF using Headless Chrome / Edge
chrome_path = r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"
if not Path(chrome_path).exists():
    chrome_path = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"

cmd = [
    chrome_path,
    "--headless",
    "--disable-gpu",
    "--run-all-compositor-stages-before-draw",
    "--print-to-pdf-no-header",
    f"--print-to-pdf={OUT_PDF.resolve()}",
    str(TEMP_HTML.resolve())
]

res = subprocess.run(cmd, capture_output=True, text=True)
print("PDF compilation exit code:", res.returncode)

if OUT_PDF.exists():
    reader = pypdf.PdfReader(OUT_PDF)
    num_pages = len(reader.pages)
    file_size_kb = OUT_PDF.stat().st_size / 1024
    print(f"SUCCESS: Generated {OUT_PDF.name} ({num_pages} pages, {file_size_kb:.1f} KB)")
else:
    print("FAILED: Output PDF not created.")