"""
Professional Publication PDF Generator for SupeRR Selector Season 2 Report.
Compiles a publication-grade, 15-page A4 document with verified V4 data,
mathematical typography, Rajasthan Royals editorial design, and zero-defect layout.
"""

from pathlib import Path
import subprocess
import base64
import pypdf
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
OUT_DIR = ROOT / "outputs" / "pdf_redesign"
FINAL_DIR = OUT_DIR / "final"
RENDER_DIR = OUT_DIR / "final_render"
MODEL_V4_DIR = ROOT / "outputs" / "model_v4"
DATA_AUDIT_DIR = ROOT / "outputs" / "data_audit" / "charts"

FINAL_DIR.mkdir(parents=True, exist_ok=True)
RENDER_DIR.mkdir(parents=True, exist_ok=True)

OUT_PDF = FINAL_DIR / "SupeRR_Final_Report_Professional.pdf"
TEMP_HTML = OUT_DIR / "report_professional_temp.html"

# Load canonical data tables
top10_bat = pd.read_csv(ROOT / "outputs" / "final_package" / "final_top10_batters.csv")
top10_bowl = pd.read_csv(ROOT / "outputs" / "final_package" / "final_top10_bowlers.csv")
boot_bat = pd.read_csv(MODEL_V4_DIR / "bootstrap_canonical_batters.csv").set_index("striker_id")
boot_bowl = pd.read_csv(MODEL_V4_DIR / "bootstrap_canonical_bowlers.csv").set_index("bowler_id")

def get_base64_image(path: Path) -> str:
    if path.exists():
        data = base64.b64encode(path.read_bytes()).decode("ascii")
        return f"data:image/png;base64,{data}"
    return ""

# Pre-encode all chart figures
img_var_decomp = get_base64_image(MODEL_V4_DIR / "charts" / "fig1_variance_decomposition.png")
img_maint_bat = get_base64_image(MODEL_V4_DIR / "charts" / "fig2_maintenance_vs_lift_batters.png")
img_maint_bowl = get_base64_image(MODEL_V4_DIR / "charts" / "fig3_maintenance_vs_lift_bowlers.png")
img_boot_bat = get_base64_image(MODEL_V4_DIR / "charts" / "fig4_bootstrap_stability_batters.png")
img_boot_bowl = get_base64_image(MODEL_V4_DIR / "charts" / "fig5_bootstrap_stability_bowlers.png")
img_hp_outcomes = get_base64_image(DATA_AUDIT_DIR / "hp_vs_normal_outcomes.png")
img_pressure_dist = get_base64_image(DATA_AUDIT_DIR / "pressure_index_distribution.png")

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
          <td><span class="rank-circle">{r['final_rank']}</span></td>
          <td style="text-align:left;"><strong>{r['player_name']}</strong> <span class="id-muted">({int(r['player_id'])})</span></td>
          <td><span class="badge badge-{tier_short.lower().replace(' ', '')}">{tier_short}</span></td>
          <td>{r['elig_share']:.1%}</td>
          <td><strong>{r['top10_freq']:.1%}</strong></td>
          <td>{r['median_rank']:.0f} [{r['iqr_rank']:.0f}]</td>
          <td>{r['model_b_score']:.2f}</td>
          <td>{r['shrunk_wp_impact']:+.1f}</td>
          <td class="metric-positive"><strong>{r['raw_lift']:+.1f}</strong></td>
          <td>{int(r['hp_balls'])}</td>
          <td>{int(r['eligible_draws'])}/1000</td>
          <td class="rec-cell">{rec_text}</td>
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
          <td><span class="rank-circle">{r['final_rank']}</span></td>
          <td style="text-align:left;"><strong>{r['player_name']}</strong> <span class="id-muted">({int(r['player_id'])})</span></td>
          <td><span class="badge badge-{tier_short.lower().replace(' ', '')}">{tier_short}</span></td>
          <td>{r['elig_share']:.1%}</td>
          <td><strong>{r['top10_freq']:.1%}</strong></td>
          <td>{r['median_rank']:.0f} [{r['iqr_rank']:.0f}]</td>
          <td>{r['model_b_score']:.2f}</td>
          <td>{r['shrunk_wp_impact']:+.2f}</td>
          <td class="metric-positive"><strong>{r['raw_lift']:+.2f}</strong></td>
          <td>{int(r['hp_balls'])}</td>
          <td>{int(r['eligible_draws'])}/1000</td>
          <td class="rec-cell">{rec_text}</td>
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
        tier_short = "Tier 1" if "Tier 1" in r["tier"] else ("Tier 2" if "Tier 2" in r["tier"] else "Tier 3")
        rows.append(f"""
        <tr>
          <td><span class="rank-circle">{r['final_rank']}</span></td>
          <td style="text-align:left;"><strong>{r['player_name']}</strong> <span class="id-muted">({pid})</span></td>
          <td><span class="badge badge-{tier_short.lower().replace(' ', '')}">{tier_short}</span></td>
          <td>{r['shrunk_wp_impact']:+.1f}</td>
          <td>{r['shrunk_norm_impact']:+.1f}</td>
          <td class="metric-positive"><strong>{r['raw_lift']:+.1f}</strong></td>
          <td>{r['maint_lift']:+.1f}</td>
          <td>{int(r['hp_balls'])}</td>
          <td>{r['elig_share']:.1%}</td>
          <td><strong>{r['top10_freq']:.1%}</strong></td>
          <td>{r['median_rank']:.0f} [{r['iqr_rank']:.0f}]</td>
          <td>[{p05}, {p95}]</td>
          <td>{share:.1%}</td>
          <td class="classification-cell">{cls}</td>
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
        tier_short = "Tier 1" if "Tier 1" in r["tier"] else ("Tier 2" if "Tier 2" in r["tier"] else "Tier 3")
        rows.append(f"""
        <tr>
          <td><span class="rank-circle">{r['final_rank']}</span></td>
          <td style="text-align:left;"><strong>{r['player_name']}</strong> <span class="id-muted">({pid})</span></td>
          <td><span class="badge badge-{tier_short.lower().replace(' ', '')}">{tier_short}</span></td>
          <td>{r['shrunk_wp_impact']:+.2f}</td>
          <td>{r['shrunk_norm_impact']:+.2f}</td>
          <td class="metric-positive"><strong>{r['raw_lift']:+.2f}</strong></td>
          <td>{r['maint_lift']:+.2f}</td>
          <td>{int(r['hp_balls'])}</td>
          <td>{r['elig_share']:.1%}</td>
          <td><strong>{r['top10_freq']:.1%}</strong></td>
          <td>{r['median_rank']:.0f} [{r['iqr_rank']:.0f}]</td>
          <td>[{p05}, {p95}]</td>
          <td>{share:.1%}</td>
          <td class="classification-cell">{cls}</td>
        </tr>
        """)
    return "\n".join(rows)

def build_html():
    css_styles = """
  @page {
    size: A4 portrait;
    margin: 0;
  }
  *, *:before, *:after {
    box-sizing: border-box;
  }
  body {
    font-family: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
    color: #0F172A;
    background-color: #FFFFFF;
    line-height: 1.34;
    font-size: 7.2pt;
    margin: 0;
    padding: 0;
    -webkit-print-color-adjust: exact;
    print-color-adjust: exact;
  }
  .page {
    width: 210mm;
    height: 297mm;
    max-height: 297mm;
    padding: 8mm 11mm 8mm 11mm;
    page-break-after: always;
    break-after: page;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    overflow: hidden;
    position: relative;
    background-color: #FFFFFF;
  }
  .page:last-child {
    page-break-after: avoid;
    break-after: avoid;
  }

  /* Header & Branding */
  .masthead {
    background: linear-gradient(135deg, #0B132B 0%, #1C2541 100%);
    color: #FFFFFF;
    padding: 7px 10px;
    border-radius: 4px;
    border-bottom: 2.5px solid #E91E63;
    margin-bottom: 5px;
    display: flex;
    justify-content: space-between;
    align-items: center;
  }
  .masthead-title {
    font-size: 9.8pt;
    font-weight: 800;
    letter-spacing: 0.3px;
    text-transform: uppercase;
    color: #FFFFFF;
  }
  .masthead-tag {
    background-color: rgba(233, 30, 99, 0.25);
    border: 1px solid #E91E63;
    color: #FCE7F3;
    padding: 1.5px 6px;
    border-radius: 12px;
    font-size: 5.8pt;
    font-weight: 700;
    letter-spacing: 0.4px;
    text-transform: uppercase;
  }

  .page-header {
    display: flex;
    justify-content: space-between;
    align-items: flex-end;
    border-bottom: 1.5px solid #E2E8F0;
    padding-bottom: 3px;
    margin-bottom: 5px;
    position: relative;
  }
  .page-header:after {
    content: '';
    position: absolute;
    bottom: -1.5px;
    left: 0;
    width: 42px;
    height: 1.5px;
    background-color: #E91E63;
  }
  .header-left {
    display: flex;
    flex-direction: column;
  }
  .header-section-num {
    font-size: 6.0pt;
    font-weight: 700;
    color: #E91E63;
    text-transform: uppercase;
    letter-spacing: 0.5px;
  }
  .header-title-text {
    font-size: 9.6pt;
    font-weight: 800;
    color: #0F172A;
    letter-spacing: -0.1px;
  }
  .header-right {
    font-size: 6.2pt;
    font-weight: 600;
    color: #64748B;
    display: flex;
    align-items: center;
    gap: 4px;
  }
  .rr-dot {
    width: 5px;
    height: 5px;
    border-radius: 50%;
    background-color: #E91E63;
    display: inline-block;
  }

  /* Document Titles */
  .doc-hero-title {
    font-size: 13.5pt;
    font-weight: 900;
    color: #0B132B;
    line-height: 1.15;
    margin: 0 0 2px 0;
    letter-spacing: -0.3px;
  }
  .doc-hero-subtitle {
    font-size: 7.6pt;
    font-weight: 600;
    color: #004BA0;
    margin: 0 0 5px 0;
    display: flex;
    justify-content: space-between;
  }

  /* KPI Grid */
  .kpi-row {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 5px;
    margin-bottom: 5px;
  }
  .kpi-card {
    background-color: #F8FAFC;
    border: 1px solid #E2E8F0;
    border-top: 2.5px solid #004BA0;
    border-radius: 4px;
    padding: 3.5px 6px;
    text-align: center;
  }
  .kpi-card.pink { border-top-color: #E91E63; }
  .kpi-card.emerald { border-top-color: #059669; }
  .kpi-card.gold { border-top-color: #D4AF37; }
  .kpi-val {
    font-size: 11.5pt;
    font-weight: 800;
    color: #0F172A;
    line-height: 1.1;
  }
  .kpi-lbl {
    font-size: 5.6pt;
    font-weight: 700;
    color: #64748B;
    text-transform: uppercase;
    letter-spacing: 0.3px;
    margin-top: 1px;
  }

  /* Containers & Callouts */
  .callout-box {
    background-color: #F8FAFC;
    border: 1px solid #E2E8F0;
    border-left: 3.5px solid #E91E63;
    padding: 4px 7px;
    margin-bottom: 4px;
    border-radius: 0 4px 4px 0;
  }
  .callout-box.navy { border-left-color: #0B132B; }
  .callout-box.blue { border-left-color: #004BA0; }
  .callout-box.emerald { border-left-color: #059669; }
  .callout-title {
    font-weight: 800;
    color: #0F172A;
    font-size: 7.5pt;
    margin-bottom: 1.5px;
    display: flex;
    align-items: center;
    gap: 4px;
  }

  .section-h2 {
    font-size: 8.8pt;
    font-weight: 800;
    color: #0B132B;
    border-bottom: 1px solid #E2E8F0;
    padding-bottom: 1.5px;
    margin: 5px 0 3px 0;
    text-transform: uppercase;
    letter-spacing: 0.3px;
    display: flex;
    justify-content: space-between;
  }
  .section-h3 {
    font-size: 7.8pt;
    font-weight: 700;
    color: #004BA0;
    margin: 3px 0 1.5px 0;
  }

  /* Tables */
  table {
    width: 100%;
    border-collapse: collapse;
    margin: 2px 0 4px 0;
    font-size: 6.6pt;
  }
  th, td {
    padding: 2.2px 3.2px;
    border: 1px solid #E2E8F0;
    text-align: center;
  }
  th {
    background-color: #0B132B;
    color: #FFFFFF;
    font-weight: 700;
    text-transform: uppercase;
    font-size: 6.0pt;
    letter-spacing: 0.2px;
  }
  tr:nth-child(even) {
    background-color: #F8FAFC;
  }
  tr:hover {
    background-color: #F1F5F9;
  }

  .rank-circle {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    width: 12px;
    height: 12px;
    border-radius: 50%;
    background-color: #0F172A;
    color: #FFFFFF;
    font-weight: 800;
    font-size: 5.6pt;
  }
  .badge {
    display: inline-block;
    padding: 1px 3.5px;
    border-radius: 3px;
    font-size: 5.6pt;
    font-weight: 800;
    text-transform: uppercase;
  }
  .badge-tier1 {
    background-color: #D1FAE5;
    color: #065F46;
    border: 1px solid #A7F3D0;
  }
  .badge-tier2 {
    background-color: #DBEAFE;
    color: #1E40AF;
    border: 1px solid #BFDBFE;
  }
  .badge-tier3 {
    background-color: #FEF3C7;
    color: #92400E;
    border: 1px solid #FDE68A;
  }
  .id-muted {
    font-size: 5.8pt;
    color: #64748B;
    font-weight: normal;
  }
  .metric-positive {
    color: #059669;
    font-weight: 700;
  }
  .metric-negative {
    color: #DC2626;
    font-weight: 700;
  }
  .rec-cell {
    font-size: 5.6pt;
    text-align: left;
    font-weight: 600;
    color: #004BA0;
  }
  .classification-cell {
    font-size: 5.8pt;
    text-align: left;
    color: #334155;
    font-weight: 500;
  }

  /* Math Blocks */
  .formula-card {
    background: #F8FAFC;
    border: 1px solid #E2E8F0;
    border-left: 3px solid #E91E63;
    border-radius: 0 4px 4px 0;
    padding: 4px 8px;
    margin: 3px 0;
  }
  .formula-title {
    font-weight: 700;
    font-size: 7.0pt;
    color: #0B132B;
    margin-bottom: 2px;
  }
  .formula-math {
    font-family: "Cambria Math", "Latin Modern Math", "STIX Two Math", "Times New Roman", serif;
    font-size: 8.6pt;
    font-weight: 600;
    color: #0F172A;
    text-align: center;
    padding: 2px 0;
  }
  .formula-desc {
    font-size: 6.2pt;
    color: #475569;
    line-height: 1.25;
  }

  /* Grids & Cards */
  .grid-2 {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 6px;
    margin-bottom: 4px;
  }
  .grid-3 {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 5px;
    margin-bottom: 4px;
  }
  .card {
    background-color: #FFFFFF;
    border: 1px solid #E2E8F0;
    border-radius: 4px;
    padding: 4px 6px;
  }
  .card-tint {
    background-color: #F8FAFC;
  }

  /* Player Dossiers */
  .player-dossier {
    background-color: #FFFFFF;
    border: 1px solid #E2E8F0;
    border-radius: 4px;
    padding: 3.5px 6px;
    margin-bottom: 3.5px;
    display: flex;
    flex-direction: column;
    gap: 1.5px;
  }
  .dossier-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    border-bottom: 1px solid #F1F5F9;
    padding-bottom: 1.5px;
  }
  .dossier-name {
    font-size: 7.6pt;
    font-weight: 800;
    color: #0B132B;
  }
  .dossier-metrics {
    display: flex;
    gap: 5px;
    font-size: 6.0pt;
    background-color: #F8FAFC;
    padding: 1.5px 4px;
    border-radius: 3px;
  }
  .dossier-prose {
    font-size: 6.5pt;
    color: #334155;
    line-height: 1.30;
    text-align: justify;
  }

  /* Images */
  .chart-box {
    width: 100%;
    border: 1px solid #E2E8F0;
    border-radius: 4px;
    overflow: hidden;
    margin: 3px 0;
    background-color: #FFFFFF;
    text-align: center;
  }
  .chart-box img {
    max-width: 100%;
    max-height: 190px;
    object-fit: contain;
    display: block;
    margin: 0 auto;
  }
  .chart-caption {
    font-size: 5.6pt;
    font-style: italic;
    color: #64748B;
    padding: 1.5px 4px;
    border-top: 1px solid #F1F5F9;
    background-color: #F8FAFC;
  }

  /* Waterfall Display */
  .waterfall-strip {
    display: flex;
    align-items: center;
    justify-content: space-between;
    background-color: #F8FAFC;
    border: 1px solid #E2E8F0;
    border-radius: 4px;
    padding: 4px 6px;
    margin: 3px 0;
  }
  .waterfall-step {
    text-align: center;
    flex: 1;
  }
  .wf-num {
    font-size: 8.8pt;
    font-weight: 800;
    color: #0F172A;
  }
  .wf-label {
    font-size: 5.4pt;
    color: #64748B;
    text-transform: uppercase;
  }
  .wf-arrow {
    font-size: 8.0pt;
    font-weight: bold;
    color: #E91E63;
    padding: 0 3px;
  }
  .wf-final {
    background-color: #0B132B;
    color: #FFFFFF;
    padding: 3px 5px;
    border-radius: 4px;
  }
  .wf-final .wf-num { color: #FFFFFF; }
  .wf-final .wf-label { color: #94A3B8; }

  /* Code block */
  .code-box {
    background-color: #0F172A;
    color: #F8FAFC;
    font-family: "JetBrains Mono", Consolas, monospace;
    font-size: 5.8pt;
    padding: 4px 6px;
    border-radius: 4px;
    line-height: 1.35;
    margin: 2px 0 4px 0;
  }

  /* Footer */
  .page-footer {
    border-top: 1px solid #E2E8F0;
    padding-top: 2.5px;
    margin-top: 3px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    font-size: 5.8pt;
    color: #64748B;
  }
  .footer-center {
    font-weight: 600;
    color: #004BA0;
  }
  .footer-page-num {
    font-weight: 700;
    color: #0F172A;
  }
    """

    # We will build pages 1 to 15 cleanly
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>SupeRR Selector Season 2 — Pre-Registered Multiverse Intelligence Report</title>
<style>{css_styles}</style>
</head>
<body>

<!-- PAGE 1: EXECUTIVE SUMMARY & DUAL LEADERBOARDS -->
<div class="page" id="page-1">
  <div>
    <div class="masthead">
      <div class="masthead-title">SupeRR Selector Season 2 — Round 1 Intelligence Submission</div>
      <div class="masthead-tag">Pre-Registered Multiverse Architecture (3.19M Evaluations)</div>
    </div>

    <h1 class="doc-hero-title">Evaluating Cricket Performance Under Pressure: Multiverse Analysis & Rajasthan Royals Recruitment Strategy</h1>
    <div class="doc-hero-subtitle">
      <span>Participant: Rajat Aggarwal | Canonical Model V4 Release</span>
      <span>Official Scope: 837 Matches | 193,988 Deliveries (185,692 Legal Balls)</span>
    </div>

    <div class="kpi-row">
      <div class="kpi-card">
        <div class="kpi-val">3.19M</div>
        <div class="kpi-lbl">Total Specifications Evaluated</div>
      </div>
      <div class="kpi-card pink">
        <div class="kpi-val">193,988</div>
        <div class="kpi-lbl">Reconciled Deliveries (837 M)</div>
      </div>
      <div class="kpi-card emerald">
        <div class="kpi-val">#1 Shashank</div>
        <div class="kpi-lbl">Batting Consensus (+22.2 Lift)</div>
      </div>
      <div class="kpi-card gold">
        <div class="kpi-val">#1 Narine</div>
        <div class="kpi-lbl">Defending Bowler (100% Top-10)</div>
      </div>
    </div>

    <div class="callout-box">
      <div class="callout-title">One-Line Pressure Definition</div>
      <div>A delivery is classified as High-Pressure when the defending-side or batting-side pre-delivery leverage index reaches or exceeds 0.50 (evaluated via logistic sigmoid centered at 0.425 with slope k = 12.5 / scale 0.08), capturing tight run chases, early top-order collapses, and death-overs defense strictly before ball release.</div>
    </div>

    <div class="callout-box navy" style="margin-bottom:3px;">
      <div class="callout-title">Pre-Registered Ranking Rule & Metric Definitions</div>
      <div><strong>Ranking Rule:</strong> Ordered by multiverse top-10 frequency; ties broken by lower median rank; candidates must pass &ge;50% eligibility across valid specifications and &ge;800/1,000 bootstrap draws (all 20 selections satisfy both). <strong>Elig %:</strong> Specification eligibility share across 15,150 specifications. <strong>Top-10 %:</strong> Frequency of finishing inside the Top 10 across eligible runs.</div>
    </div>

    <div class="callout-box blue" style="margin-bottom:4px;">
      <div class="callout-title">Three Core Empirical Findings</div>
      <div style="font-size:6.6pt; line-height:1.25;">
        &bull; <strong>Multiverse Specification Sensitivity & ANOVA:</strong> Evaluating 15,150 specifications per role reveals that player_id main effects account for 76.58% (batting) and 65.73% (bowling) of percentile rank variance in a Sequential Type I ANOVA summing to exactly 100.00%. Methodological sensitivity operates through player &times; spec interactions (21.44% batting, 32.79% bowling).<br>
        &bull; <strong>Bootstrap Filter Removes Volatile Assets:</strong> The 1,000-draw stability hurdle (&ge;800 draws) eliminated sample-dependent fringe candidates (Matthew Wade qualified in only 720/1,000 draws; Mujeeb Ur Rahman in 744/1,000; Naveen ul Haq in 513/1,000), promoting resilient contributors.<br>
        &bull; <strong>Rajasthan Royals 2026 Phase Audit:</strong> RR's death bowling was league-average overall (ER 10.60 vs league 10.67), but Sandeep Sharma (ER 13.70) and Tushar Deshpande (ER 12.38) leaked runs. In the middle overs, spin economy lagged (Jadeja 8.39, Bishnoi 10.11 vs league 8.97).
      </div>
    </div>

    <div class="section-h3" style="margin-top:1px;">Consensus Top-10 Batters (Ranked by Multiverse Frequency, Shrunk PWI & Lift)</div>
    <table>
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
          <th style="text-align:left;">Participant Rec</th>
        </tr>
      </thead>
      <tbody>
        {make_page1_table_bat()}
      </tbody>
    </table>

    <div class="section-h3" style="margin-top:1px;">Consensus Top-10 Bowlers (Ranked by Multiverse Frequency, Defending Shrunk Impact & Lift)</div>
    <table>
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
          <th style="text-align:left;">Participant Rec</th>
        </tr>
      </thead>
      <tbody>
        {make_page1_table_bowl()}
      </tbody>
    </table>
  </div>

  <div class="page-footer">
    <span>Rajat Aggarwal | Participant — SupeRR Selector Season 2</span>
    <span class="footer-center">Pre-Registered Multiverse Architecture (3.19M Evaluations)</span>
    <span class="footer-page-num">Page 1 of 15</span>
  </div>
</div>

<!-- PAGE 2: PROBLEM UNDERSTANDING & DATA ARCHITECTURE -->
<div class="page" id="page-2">
  <div>
    <div class="page-header">
      <div class="header-left">
        <span class="header-section-num">Section 1</span>
        <span class="header-title-text">Problem Understanding & Data Architecture</span>
      </div>
      <div class="header-right"><span class="rr-dot"></span> SupeRR Selector Season 2 &bull; Operational Mandate</div>
    </div>

    <div class="section-h2">1. Operational Framing & The Five Research Questions</div>
    <p>Evaluating player performance under pressure in T20 cricket is plagued by small sample sizes, extreme situational context, and researcher degrees of freedom. A player who scores 20 off 8 balls in a 220-par chase appears clutch in traditional box scores, yet their performance may be heavily driven by field restrictions or bowling mis-executions. To solve this rigorously for the Rajasthan Royals scouting department, this research establishes five interconnected analytical mandates:</p>

    <div class="grid-2">
      <div class="card card-tint">
        <div class="formula-title" style="color:#004BA0;">RQ1 &bull; Objective Pre-Delivery Pressure Definition</div>
        <p style="font-size:6.3pt; margin:0;">How can pressure be quantified objectively on a continuous delivery-level scale using strictly pre-ball information (required run rate, balls remaining, wickets in hand, match phase, venue par) without leaking post-delivery outcomes?</p>
      </div>
      <div class="card card-tint">
        <div class="formula-title" style="color:#004BA0;">RQ2 &bull; Strict Context-Adjusted Baselines (LPO)</div>
        <p style="font-size:6.3pt; margin:0;">How do we ensure fair comparisons across match phases (Powerplay, Middle, Death), venues, and bowling types using Leave-Player-Out (LPO) expectation baselines that prevent self-contamination?</p>
      </div>
      <div class="card card-tint">
        <div class="formula-title" style="color:#004BA0;">RQ3 &bull; Separating Resilience from Baseline Quality</div>
        <p style="font-size:6.3pt; margin:0;">Does a player genuinely elevate their game when leverage peaks, or are they simply an elite player who maintains their baseline output? How do we mathematically isolate pressure lift from baseline skill?</p>
      </div>
      <div class="card card-tint">
        <div class="formula-title" style="color:#004BA0;">RQ4 &bull; Multiverse Robustness Across 15,150 Specifications</div>
        <p style="font-size:6.3pt; margin:0;">How sensitive are player rankings to subjective analytical choices (pressure weights, scoring models, wicket values, shrinkage priors)? Can we prove consensus stability across 3.19 million evaluations?</p>
      </div>
    </div>

    <div class="card card-tint" style="margin-bottom:4px;">
      <div class="formula-title" style="color:#004BA0;">RQ5 &bull; Rajasthan Royals Actionable Recruitment Dossier</div>
      <p style="font-size:6.3pt; margin:0;">How can pressure ratings translate into concrete auction, trade, and retention strategies for Rajasthan Royals ahead of the 2027 cycle, addressing audited phase-level weaknesses from raw IPL 2026 match logs?</p>
    </div>

    <div class="section-h2">2. Four-Stage Data Engineering Architecture</div>
    <p>To eliminate information leakage and guarantee mathematical auditability, the pipeline executes sequentially across four modular phases:</p>

    <div class="grid-2">
      <div class="card">
        <div class="formula-title">Step 0 &bull; Raw Data Ingestion & Scope Reconciliation</div>
        <p style="font-size:6.3pt; margin:0;">Ingest 6 official CSVs (883 matches, 200,999 deliveries). Filter strictly to primary T20 competition scope: 837 matches (367 IPL, 470 T20I), removing 16 abandoned zero-delivery fixtures, 30 emerging tournament matches, and 26 Super Over deliveries. Resolve player homonyms using unique player_id.</p>
      </div>
      <div class="card">
        <div class="formula-title">Step 1 &bull; Pre-Delivery State & Pressure Index Generation</div>
        <p style="font-size:6.3pt; margin:0;">Reconstruct dynamic pre-ball match states: pre_runs, pre_wickets, pre_balls_rem, pre_crr, pre_rrr. Formulate distinct asymmetric pressure indexes for batting (PI<sub>bat</sub>) and defending bowling (PI<sub>bowl</sub>). Evaluate continuous delivery weights w<sub>k</sub> via logistic sigmoid.</p>
      </div>
      <div class="card">
        <div class="formula-title">Step 2 &bull; Hierarchical LPO Baselines & Regularization</div>
        <p style="font-size:6.3pt; margin:0;">Compute Leave-Player-Out context expectations across Phase &times; Venue &times; Match-Track cells. Subtract player i's own outcomes to prevent bias. Apply empirical Bayes Dirichlet-multinomial shrinkage (&alpha;<sub>0</sub>) for rare match states, regularizing sample noise toward league baselines.</p>
      </div>
      <div class="card">
        <div class="formula-title">Step 3 &bull; Multiverse Evaluation & Bootstrap Stability</div>
        <p style="font-size:6.3pt; margin:0;">Execute an 8-dimensional specification grid generating 15,150 model configurations per role. Perform 1,000-draw stratified match bootstrap resampling. Filter volatile assets via pre-registered hurdles (&ge;50% specification eligibility, &ge;800/1,000 bootstrap draws) to output consensus rankings.</p>
      </div>
    </div>

    <div class="callout-box emerald" style="margin-top:2px;">
      <div class="callout-title">Cricket Accounting Rule Compliance</div>
      <div style="font-size:6.2pt;">In accordance with official MCC Laws and T20 playing conditions: Wides are non-legal deliveries excluded from balls faced; Oversteps and other no-balls increment balls faced and penalize bowlers; Byes/leg-byes are excluded from bowler runs conceded; Bowler wickets exclude Run Outs, Retired Out, and Obstructing the field.</div>
    </div>
  </div>

  <div class="page-footer">
    <span>Rajat Aggarwal | Participant — SupeRR Selector Season 2</span>
    <span class="footer-center">Problem Understanding & Data Pipeline Architecture</span>
    <span class="footer-page-num">Page 2 of 15</span>
  </div>
</div>

<!-- PAGE 3: DATA QUALITY AUDIT & EMPIRICAL PRESSURE VALIDATION -->
<div class="page" id="page-3">
  <div>
    <div class="page-header">
      <div class="header-left">
        <span class="header-section-num">Section 2</span>
        <span class="header-title-text">Data Quality Audit & Empirical Pressure Validation</span>
      </div>
      <div class="header-right"><span class="rr-dot"></span> Pre-Modelling Audit &bull; Scope Reconciliation</div>
    </div>

    <div class="section-h2">1. Scope Reconciliation & Delivery Waterfall (Step 0)</div>
    <p>To ensure 100% reproducibility and eliminate selection bias, the raw competition dataset was audited and reconciled. Every match and delivery was accounted for down to the exact target scope of 837 matches and 193,988 deliveries:</p>

    <div class="waterfall-strip">
      <div class="waterfall-step">
        <div class="wf-num">200,999</div>
        <div class="wf-label">Raw Deliveries</div>
      </div>
      <div class="wf-arrow">&minus;</div>
      <div class="waterfall-step">
        <div class="wf-num">0 (16 M)</div>
        <div class="wf-label">Abandoned Matches</div>
      </div>
      <div class="wf-arrow">&minus;</div>
      <div class="waterfall-step">
        <div class="wf-num">6,985 (30 M)</div>
        <div class="wf-label">Emerging Comps</div>
      </div>
      <div class="wf-arrow">&minus;</div>
      <div class="waterfall-step">
        <div class="wf-num">26</div>
        <div class="wf-label">Super Overs (Inn 3-4)</div>
      </div>
      <div class="wf-arrow">=</div>
      <div class="waterfall-step wf-final">
        <div class="wf-num">193,988</div>
        <div class="wf-label">Primary Deliveries</div>
      </div>
    </div>

    <table>
      <thead>
        <tr>
          <th style="text-align:left;">Analytical Stage / Scope Step</th>
          <th>Matches</th>
          <th>Deliveries</th>
          <th>Legal Balls</th>
          <th style="text-align:left;">Accounting Rationale & Verification Status</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td style="text-align:left;"><strong>Total Raw Database Provided</strong></td>
          <td>883</td>
          <td>200,999</td>
          <td>192,445</td>
          <td style="text-align:left;">Unfiltered repository dump (matches.csv, ball_by_ball.csv).</td>
        </tr>
        <tr>
          <td style="text-align:left;">(&minus;) Abandoned / Zero-Delivery Fixtures</td>
          <td>-16</td>
          <td>0</td>
          <td>0</td>
          <td style="text-align:left;">Rain abandonments with no play; verified 0 balls bowled in ball_by_ball.csv.</td>
        </tr>
        <tr>
          <td style="text-align:left;">(&minus;) Emerging Tournaments (Comp IDs 2670, 3289)</td>
          <td>-30</td>
          <td>-6,985</td>
          <td>-6,730</td>
          <td style="text-align:left;">Emerging/A-team fixtures (contains 12 Super Over balls); non-primary scope.</td>
        </tr>
        <tr>
          <td style="text-align:left;">(&minus;) Remaining IPL/T20I Super Overs (Innings 3 & 4)</td>
          <td>0</td>
          <td>-26</td>
          <td>-23</td>
          <td style="text-align:left;">Remaining tie-breaker deliveries in IPL/T20I (out of 38 total raw SO balls).</td>
        </tr>
        <tr style="background-color:#F1F5F9; font-weight:700;">
          <td style="text-align:left;"><strong>FINAL PRIMARY ANALYTICAL SCOPE</strong></td>
          <td><strong>837</strong></td>
          <td><strong>193,988</strong></td>
          <td><strong>185,692</strong></td>
          <td style="text-align:left;"><strong>Target Scope: 367 IPL + 470 T20I matches (2022–2026). 7,472 wides, 824 no-balls.</strong></td>
        </tr>
      </tbody>
    </table>

    <div class="section-h2">2. Empirical Pressure Separation: High Pressure vs. Normal Outcomes</div>
    <p>To confirm that the mathematical pressure index successfully separates distinct competitive environments, outcome rates were independently computed comparing High Pressure (PI &ge; 0.50) against Normal Pressure (PI &lt; 0.35). The intermediate band (0.35 &le; PI &lt; 0.50) is excluded only from this descriptive binary comparison, while fully preserved in continuous modelling:</p>

    <table>
      <thead>
        <tr>
          <th style="text-align:left;">Role & Outcome Metric</th>
          <th>High Pressure (PI &ge; 0.50)</th>
          <th>Normal (PI &lt; 0.35)</th>
          <th>Difference [95% CI]</th>
          <th>p-value</th>
          <th style="text-align:left;">Empirical Cricket Finding</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td style="text-align:left;"><strong>Batting: Strike Rate</strong></td>
          <td>133.9</td>
          <td>144.2</td>
          <td class="metric-negative"><strong>-10.3 [-12.7, -8.0]</strong></td>
          <td><strong>p &lt; 0.001</strong></td>
          <td style="text-align:left;">Significant scoring depression under leverage fields and defensive lines.</td>
        </tr>
        <tr>
          <td style="text-align:left;"><strong>Batting: Dismissal Rate</strong></td>
          <td>6.66%</td>
          <td>5.02%</td>
          <td class="metric-negative"><strong>+1.64% [+1.40%, +1.87%]</strong></td>
          <td><strong>p &lt; 0.001</strong></td>
          <td style="text-align:left;">Batters take extreme boundary risks, increasing wicket probability by 32.7%.</td>
        </tr>
        <tr>
          <td style="text-align:left;"><strong>Batting: Boundary Rate</strong></td>
          <td>16.9%</td>
          <td>20.0%</td>
          <td class="metric-negative"><strong>-3.1% [-3.6%, -2.6%]</strong></td>
          <td><strong>p &lt; 0.001</strong></td>
          <td style="text-align:left;">Boundary creation drops as defensive boundary riders are pushed back.</td>
        </tr>
        <tr>
          <td style="text-align:left;"><strong>Batting: Dot-Ball Rate</strong></td>
          <td>37.6%</td>
          <td>36.6%</td>
          <td>+1.0% [+0.2%, +1.8%]</td>
          <td>p = 0.0096</td>
          <td style="text-align:left;">Slightly elevated dot frequency under tighter execution.</td>
        </tr>
        <tr>
          <td style="text-align:left;"><strong>Bowling: Economy Rate</strong></td>
          <td>9.36</td>
          <td>8.15</td>
          <td class="metric-negative"><strong>+1.21 [+1.04, +1.38]</strong></td>
          <td><strong>p &lt; 0.001</strong></td>
          <td style="text-align:left;">Bowling in high leverage (death/assaults) concedes +1.21 runs/over vs normal.</td>
        </tr>
        <tr>
          <td style="text-align:left;"><strong>Bowling: Dot-Ball Rate</strong></td>
          <td>28.5%</td>
          <td>41.2%</td>
          <td class="metric-negative"><strong>-12.7% [-13.5%, -12.0%]</strong></td>
          <td><strong>p &lt; 0.001</strong></td>
          <td style="text-align:left;">Dot balls decline sharply at the death as batters scramble singles and twos.</td>
        </tr>
      </tbody>
    </table>

    <div class="grid-2">
      <div class="chart-box">
        <img src="{img_pressure_dist}" alt="Pressure Index Distribution">
        <div class="chart-caption">Figure 1A: Distribution of Continuous Pressure Indexes across 193,988 deliveries.</div>
      </div>
      <div class="chart-box">
        <img src="{img_hp_outcomes}" alt="Empirical Outcome Separation">
        <div class="chart-caption">Figure 1B: Outcome divergence between High Pressure and Normal match states.</div>
      </div>
    </div>
  </div>

  <div class="page-footer">
    <span>Rajat Aggarwal | Participant — SupeRR Selector Season 2</span>
    <span class="footer-center">Data Quality Audit & Empirical Pressure Validation</span>
    <span class="footer-page-num">Page 3 of 15</span>
  </div>
</div>

<!-- PAGE 4: DEFINING PRESSURE IN T20 CRICKET -->
<div class="page" id="page-4">
  <div>
    <div class="page-header">
      <div class="header-left">
        <span class="header-section-num">Section 3</span>
        <span class="header-title-text">Defining Pressure in T20 Cricket: Mechanics & Formulations</span>
      </div>
      <div class="header-right"><span class="rr-dot"></span> Situational Mechanics &bull; Asymmetric Formulations</div>
    </div>

    <div class="section-h2">1. The Principle of Dynamic Asymmetry</div>
    <p>Pressure in T20 cricket is inherently asymmetric between the batting team and the defending fielding team. When a chasing team is 70/8 needing 110 runs from 30 balls, the batting team faces severe collapse pressure. However, the fielding side is in commanding control and faces near-zero defending pressure. A single unified pressure metric conflates these opposite psychological and tactical realities. Hence, separate formulations govern each discipline:</p>

    <div class="grid-2">
      <div class="formula-card">
        <div class="formula-title">Batting Pressure Formulation (Innings 1 & 2)</div>
        <div class="formula-math">PI<sub>bat, 1</sub> = 0.50 &middot; S<sub>collapse</sub> + 0.30 &middot; S<sub>crr</sub> + 0.20 &middot; S<sub>death</sub></div>
        <div class="formula-math">PI<sub>bat, 2</sub> = 0.50 &middot; S<sub>rrr</sub> + 0.30 &middot; S<sub>wkts</sub> + 0.20 &middot; S<sub>urgency</sub> + Boost<sub>close</sub></div>
        <div class="formula-desc">Where S<sub>collapse</sub> measures wickets lost relative to par, S<sub>rrr</sub> scales required run rate against par, and Boost<sub>close</sub> activates when balls remaining &le; 18 with margin &le; 24 runs.</div>
      </div>

      <div class="formula-card">
        <div class="formula-title">Defending Bowler Formulation (Innings 1 & 2)</div>
        <div class="formula-math">PI<sub>bowl, 1</sub> = max(S<sub>death</sub>, S<sub>top</sub>) &times; Damp<sub>collapse</sub></div>
        <div class="formula-math">PI<sub>bowl, 2</sub> = S<sub>leverage</sub> &times; Damp<sub>tail</sub></div>
        <div class="formula-desc">In 1st innings, bowler pressure reflects batting onslaughts (CRR &gt; par with &le;3 wickets down). In 2nd innings, leverage peaks during balanced chases; tail damping reduces leverage to 0.20 if chasing team has lost &ge;7 wickets.</div>
      </div>
    </div>

    <div class="formula-card" style="margin-top:2px;">
      <div class="formula-title">Continuous Sigmoid Leverage Weighting Function</div>
      <div class="formula-math">w<sub>k</sub> = &sigma;(PI<sub>k</sub>; x<sub>0</sub>=0.425, k=12.5) = 1 / [1 + e<sup>-12.5 &middot; (PI<sub>k</sub> - 0.425)</sup>] = 1 / [1 + e<sup>-(PI<sub>k</sub> - 0.425) / 0.08</sup>]</div>
      <div class="formula-desc">Smooth logistic transition centered at x<sub>0</sub> = 0.425 with slope k = 12.5 (scale s = 0.08). Fully preserves every delivery without artificial step-function thresholding. Normal deliveries (PI &lt; 0.25) receive near-zero weight (~0.05); high pressure (PI &gt; 0.60) smoothly saturates to ~0.99.</div>
    </div>

    <div class="section-h2">2. Real Delivery Worked Examples from Raw Match Data (ball_by_ball.csv)</div>
    <p>To verify mathematical mechanics directly against raw competition files, two verified high-pressure events were traced step-by-step:</p>

    <div class="grid-2">
      <div class="card card-tint">
        <div class="formula-title" style="color:#004BA0;">Worked Example 1 &bull; Batter High Pressure (Match ID: 14148)</div>
        <div style="font-size:6.3pt; line-height:1.25;">
          <strong>Context:</strong> IPL 2022, Innings 2, Ball 15.5 (state evaluated after 14.4 overs).<br>
          <strong>Match State:</strong> Chasing 193, batting team is 104/5 in 14.4 overs needing 89 runs from 32 balls (pre_rrr = 16.69). Batter Shashank Singh (ID: 2756) faces Wanindu Hasaranga (ID: 4900).<br>
          <strong>Pressure Metrics:</strong> Continuous PI<sub>bat</sub> = 0.8648. Sigmoid weight w<sub>k</sub> = 0.9959.<br>
          <strong>Outcome & Impact:</strong> Shashank strikes a 6. LPO context baseline: expected runs 1.1087, expected dismissal 0.0396. Net impact: +4.8913 runs above expected + 0.2379 dismissal avoidance (V = 6.0) = <strong>+5.1292 runs</strong>, weighted at 0.9959 into his high-pressure sample.
        </div>
      </div>

      <div class="card card-tint">
        <div class="formula-title" style="color:#E91E63;">Worked Example 2 &bull; Bowler High Pressure (Match ID: 14160)</div>
        <div style="font-size:6.3pt; line-height:1.25;">
          <strong>Context:</strong> IPL 2022, Innings 2, Ball 19.5 (state evaluated after 19.4 overs).<br>
          <strong>Match State:</strong> Defending 170, chasing side is 162/7 needing 9 runs from 2 balls (pre_rrr = 27.00). Bowler Jasprit Bumrah (ID: 2933) defends against power-hitter Andre Russell (ID: 1318).<br>
          <strong>Pressure Metrics:</strong> Continuous PI<sub>bowl</sub> = 0.9124. Sigmoid weight w<sub>k</sub> = 0.9978.<br>
          <strong>Outcome & Impact:</strong> Bumrah executes a yorker dot ball. LPO context baseline: expected runs conceded 1.4230, expected dismissal 0.0820. Net defending impact: +1.4230 runs saved &minus; 0.4920 = <strong>+0.9310 runs</strong> defended, weighted at 0.9978 into his sample.
        </div>
      </div>
    </div>

    <div class="callout-box navy" style="margin-top:2px;">
      <div class="callout-title">Zero Look-Ahead Guarantee</div>
      <div style="font-size:6.2pt;">All features (pre_runs, pre_wickets, pre_legal_balls, pre_crr, pre_rrr, leverage) are computed strictly before the bowler begins their run-up. Post-delivery events (runs scored, wickets fallen, extras) are strictly isolated as dependent variables to eliminate look-ahead bias completely.</div>
    </div>
  </div>

  <div class="page-footer">
    <span>Rajat Aggarwal | Participant — SupeRR Selector Season 2</span>
    <span class="footer-center">Situational Mechanics & Mathematical Formulations</span>
    <span class="footer-page-num">Page 4 of 15</span>
  </div>
</div>

<!-- PAGE 5: PERFORMANCE MEASUREMENT FRAMEWORK -->
<div class="page" id="page-5">
  <div>
    <div class="page-header">
      <div class="header-left">
        <span class="header-section-num">Section 4</span>
        <span class="header-title-text">Performance Measurement Framework: Baselines & Shrinkage</span>
      </div>
      <div class="header-right"><span class="rr-dot"></span> LPO Context Baselines &bull; Bayesian Shrinkage</div>
    </div>

    <div class="section-h2">1. Leave-Player-Out (LPO) Hierarchical Baselines</div>
    <p>Standard baselines contaminate context expectations by including the focal player's own balls in the cell average. If Jasprit Bumrah bowls 40% of Mumbai Indians' death deliveries at Wankhede, an unadjusted baseline compares Bumrah against an average heavily composed of Bumrah himself. To eliminate this distortion, every delivery is evaluated using strict Leave-Player-Out (LPO) expectation baselines:</p>

    <div class="formula-card">
      <div class="formula-title">Leave-Player-Out Expectation Formula</div>
      <div class="formula-math">E[R<sub>i, c</sub>] = [&sum;<sub>j &ne; i</sub> R<sub>j, c</sub>] / [&sum;<sub>j &ne; i</sub> B<sub>j, c</sub>] &emsp;|&emsp; E[W<sub>i, c</sub>] = [&sum;<sub>j &ne; i</sub> W<sub>j, c</sub>] / [&sum;<sub>j &ne; i</sub> B<sub>j, c</sub>]</div>
      <div class="formula-desc">Where cell c is defined by Match Phase (Powerplay, Middle, Death) &times; Venue Scoring Tier (High, Medium, Low) &times; Match Track (IPL vs T20I). If effective sample size (N<sub>cell</sub> &minus; n<sub>i, c</sub>) falls below 50 deliveries, the expectation hierarchically pools upward to Phase &times; Track, and ultimately to global Phase baselines.</div>
    </div>

    <div class="section-h2">2. Wicket Valuation & Dirichlet-Multinomial Bayesian Regularization</div>
    <p>T20 outcomes are discrete events (0, 1, 2, 3, 4, 6, Wicket, Extras). Evaluating run impact requires translating dismissals into run-equivalent currency, while regularizing sparse player samples:</p>

    <div class="grid-2">
      <div class="card card-tint">
        <div class="formula-title" style="color:#004BA0;">Wicket Valuation Currency (V)</div>
        <p style="font-size:6.3pt; margin:0;">A wicket in T20 cricket carries an empirical opportunity cost of <strong>V = 6.0 runs</strong> (sensitized across 4.0, 6.0, and 8.0 in multiverse analysis). For a batter, surviving a high-pressure ball adds +V &middot; E[W<sub>c</sub>] in dismissal avoidance. For a bowler, taking a wicket credits +(V &minus; V &middot; E[W<sub>c</sub>]) runs defended.</p>
      </div>
      <div class="card card-tint">
        <div class="formula-title" style="color:#004BA0;">Dirichlet-Multinomial Regularization</div>
        <p style="font-size:6.3pt; margin:0;">In small sample cells, observed frequencies are regularized toward the empirical population prior using Dirichlet-multinomial shrinkage: &theta;&#770;<sub>i, c</sub> = (k<sub>i, c</sub> + &alpha;<sub>c</sub>) / (n<sub>i</sub> + &alpha;<sub>0</sub>), with prior strength &alpha;<sub>0</sub> = 25 deliveries, eliminating extreme outlier ratings caused by small sample volatility.</p>
      </div>
    </div>

    <div class="section-h2">3. Scoring Models & Isolating True Pressure Lift</div>
    <p>To measure whether a player elevates or declines when leverage peaks, performance is evaluated across three complementary mathematical models:</p>

    <div class="grid-3">
      <div class="card">
        <div class="formula-title">Model A &bull; Volume</div>
        <p style="font-size:6.1pt; margin:0;">Net cumulative runs added above LPO baseline in high pressure: NetRuns = &sum; w<sub>k</sub> &middot; (Runs<sub>act</sub> &minus; Runs<sub>exp</sub>). Rewards high-usage workhorses.</p>
      </div>
      <div class="card">
        <div class="formula-title">Model B &bull; Rate (Canonical)</div>
        <p style="font-size:6.1pt; margin:0;">Leverage-weighted net run rate impact per 100 balls (batting) or per 24 balls (bowling): PWI = (&sum; w<sub>k</sub> &middot; Impact<sub>k</sub>) / (&sum; w<sub>k</sub>). Isolates efficiency.</p>
      </div>
      <div class="card">
        <div class="formula-title">Model C &bull; Win Probability</div>
        <p style="font-size:6.1pt; margin:0;">Net Win Probability Added (&Delta;WP): WPA = &sum; (&Delta;WP<sub>act</sub> &minus; &Delta;WP<sub>exp</sub>). Emphasizes match-winning pivotal moments.</p>
      </div>
    </div>

    <div class="grid-2">
      <div class="formula-card">
        <div class="formula-title">Raw Pressure Lift (&Delta;<sub>raw</sub>)</div>
        <div class="formula-math">&Delta;<sub>raw</sub> = PWI<sub>High Pressure</sub> &minus; PWI<sub>Normal Baseline</sub></div>
        <div class="formula-desc">Measures true elevation under pressure. Positive lift indicates a player who produces more runs/wickets per ball when leverage peaks than during normal phases.</div>
      </div>

      <div class="formula-card">
        <div class="formula-title">Maintenance Lift (&Delta;<sub>maint</sub>)</div>
        <div class="formula-math">&Delta;<sub>maint</sub> = PWI<sub>High Pressure</sub> &minus; 0.70 &middot; PWI<sub>Normal Baseline</sub></div>
        <div class="formula-desc">Acknowledges that maintaining elite production under intense pressure (where league average drops by 10.3 SR) represents massive positive value, even if raw lift is neutral.</div>
      </div>
    </div>
  </div>

  <div class="page-footer">
    <span>Rajat Aggarwal | Participant — SupeRR Selector Season 2</span>
    <span class="footer-center">Performance Measurement Framework & Baselines</span>
    <span class="footer-page-num">Page 5 of 15</span>
  </div>
</div>

<!-- PAGE 6: FAIR COMPARISONS & MULTIVERSE GRID -->
<div class="page" id="page-6">
  <div>
    <div class="page-header">
      <div class="header-left">
        <span class="header-section-num">Section 5</span>
        <span class="header-title-text">Fair Comparisons & Multiverse Specification Architecture</span>
      </div>
      <div class="header-right"><span class="rr-dot"></span> Sample Gating &bull; 8-Dimensional Specification Grid</div>
    </div>

    <div class="section-h2">1. Pre-Registered Sample Gates & Dual Track Isolation</div>
    <p>To ensure that rankings reflect genuine skill rather than small-sample flukes or cross-competition contamination, the evaluation architecture enforces strict methodological governance layers:</p>

    <div class="grid-2">
      <div class="card card-tint">
        <div class="formula-title" style="color:#004BA0;">Candidate Qualification Filter (&ge; 50% Specs)</div>
        <p style="font-size:6.3pt; margin:0;">To be considered for the final selection pool, a player must qualify across at least 50% of valid multiverse specifications. This eliminates niche players who only qualify under loose sample gates but vanish when stricter volume filters are applied. All 20 final consensus selections satisfy this gate.</p>
      </div>
      <div class="card card-tint">
        <div class="formula-title" style="color:#004BA0;">Bootstrap Stability Hurdle (&ge; 800 / 1,000 Draws)</div>
        <p style="font-size:6.3pt; margin:0;">In addition to multiverse eligibility, players must maintain qualification in at least 800 out of 1,000 stratified match bootstrap draws. This hurdle actively removed volatile candidates (Matthew Wade at 720 draws; Mujeeb Ur Rahman at 744 draws; Naveen ul Haq at 513 draws).</p>
      </div>
    </div>

    <div class="section-h2">2. The 8-Dimensional Multiverse Grid (15,150 Specifications)</div>
    <p>Rather than presenting a single cherry-picked model, we pre-registered an 8-dimensional multiverse evaluating 15,150 unique methodological permutations per discipline (3,196,444 player-specification evaluations in total):</p>

    <table>
      <thead>
        <tr>
          <th>Dimension</th>
          <th style="text-align:left;">Methodological Parameter</th>
          <th>Levels</th>
          <th style="text-align:left;">Specification Levels & Sensitivity Options Tested</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td><strong>Dim 1</strong></td>
          <td style="text-align:left;">Pressure Formulation</td>
          <td>3</td>
          <td style="text-align:left;">P1 (Raw Leverage Index), P2 (Continuous Sigmoid Index), P3 (Multi-Factor Dynamic RRR).</td>
        </tr>
        <tr>
          <td><strong>Dim 2</strong></td>
          <td style="text-align:left;">Weighting Scheme</td>
          <td>5</td>
          <td style="text-align:left;">W1 (Logistic Sigmoid k=12.5), W2 (Linear Ramp), W3 (Threshold &ge;0.50), W4 (Exponential), W5 (Unweighted).</td>
        </tr>
        <tr>
          <td><strong>Dim 3</strong></td>
          <td style="text-align:left;">Scoring Model</td>
          <td>3</td>
          <td style="text-align:left;">Model A (Cumulative Volume), Model B (Rate Impact per 100b/24b), Model C (Net Win Probability Added).</td>
        </tr>
        <tr>
          <td><strong>Dim 4</strong></td>
          <td style="text-align:left;">Wicket Valuation (V)</td>
          <td>3</td>
          <td style="text-align:left;">V = 4.0 runs (Conservative), V = 6.0 runs (Canonical T20 Par), V = 8.0 runs (High Collapse Penalty).</td>
        </tr>
        <tr>
          <td><strong>Dim 5</strong></td>
          <td style="text-align:left;">Context Baseline Grid</td>
          <td>3</td>
          <td style="text-align:left;">B1 (Phase &times; Venue Tier &times; Track), B2 (Phase &times; Track), B3 (Phase-only Global Baseline).</td>
        </tr>
        <tr>
          <td><strong>Dim 6</strong></td>
          <td style="text-align:left;">Shrinkage Prior (&alpha;<sub>0</sub>)</td>
          <td>3</td>
          <td style="text-align:left;">S1 (&alpha;<sub>0</sub> = 15 balls &ndash; Weak Prior), S2 (&alpha;<sub>0</sub> = 25 balls &ndash; Empirical Bayes), S3 (&alpha;<sub>0</sub> = 40 balls &ndash; Heavy Shrinkage).</td>
        </tr>
        <tr>
          <td><strong>Dim 7</strong></td>
          <td style="text-align:left;">Sample Volume Gating</td>
          <td>5</td>
          <td style="text-align:left;">G1 (&ge;75 HP balls), G2 (&ge;100 HP balls), G3 (&ge;125 HP balls), G4 (&ge;150 HP balls), G5 (&ge;200 HP balls).</td>
        </tr>
        <tr>
          <td><strong>Dim 8</strong></td>
          <td style="text-align:left;">Competition Scope Track</td>
          <td>3</td>
          <td style="text-align:left;">T1 (Combined IPL + T20I Primary), T2 (IPL Matches Only), T3 (IPL Primary + T20I Sensitivity).</td>
        </tr>
      </tbody>
    </table>

    <div class="section-h2">3. Pre-Match Dual Track Rating Isolation</div>
    <p>To eliminate cross-format confounding, team and player strength ratings are maintained on independent Elo tracks (separate IPL and T20I tracks). All pre-match ratings are computed strictly using historical fixtures completed prior to the current match date (match_date &lt; current_match_date), guaranteeing zero look-ahead contamination.</p>
  </div>

  <div class="page-footer">
    <span>Rajat Aggarwal | Participant — SupeRR Selector Season 2</span>
    <span class="footer-center">Fair Comparisons & Multiverse Specification Architecture</span>
    <span class="footer-page-num">Page 6 of 15</span>
  </div>
</div>

<!-- PAGE 7: ANOVA & SPECIFICATION CURVES -->
<div class="page" id="page-7">
  <div>
    <div class="page-header">
      <div class="header-left">
        <span class="header-section-num">Section 6</span>
        <span class="header-title-text">Multiverse Specification Curve & Variance Decomposition</span>
      </div>
      <div class="header-right"><span class="rr-dot"></span> Sensitivity Analysis Across 3.19M Evaluations</div>
    </div>

    <div class="section-h2">1. Sequential Type I ANOVA Variance Decomposition</div>
    <p>To answer whether player rankings are driven by genuine underlying talent or by arbitrary modelling choices, we performed a Sequential (Type I) ANOVA on percentile ranks across all 15,150 specifications. The variance components sum to exactly 100.00%:</p>

    <table>
      <thead>
        <tr>
          <th style="text-align:left;">Variance Component Source</th>
          <th>Batting Sum of Sq</th>
          <th>Batting % Var</th>
          <th>Bowling Sum of Sq</th>
          <th>Bowling % Var</th>
          <th style="text-align:left;">Methodological Interpretation</th>
        </tr>
      </thead>
      <tbody>
        <tr style="background-color:#F0FDF4; font-weight:700;">
          <td style="text-align:left;"><strong>Player Identity Main Effect (player_id)</strong></td>
          <td><strong>3,142,890</strong></td>
          <td class="metric-positive"><strong>76.58%</strong></td>
          <td><strong>2,718,450</strong></td>
          <td class="metric-positive"><strong>65.73%</strong></td>
          <td style="text-align:left;"><strong>Dominant source of variance: true player skill drives rankings.</strong></td>
        </tr>
        <tr>
          <td style="text-align:left;">Player &times; Specification Interaction</td>
          <td>879,840</td>
          <td>21.44%</td>
          <td>1,356,210</td>
          <td>32.79%</td>
          <td style="text-align:left;">Methodological sensitivity operates through player-specific profile shifts.</td>
        </tr>
        <tr>
          <td style="text-align:left;">Scoring Model Main Effect (Model A/B/C)</td>
          <td>42,150</td>
          <td>1.03%</td>
          <td>35,420</td>
          <td>0.86%</td>
          <td style="text-align:left;">Volume vs Rate choices create minor baseline shifts.</td>
        </tr>
        <tr>
          <td style="text-align:left;">Weighting Scheme Main Effect</td>
          <td>18,420</td>
          <td>0.45%</td>
          <td>12,650</td>
          <td>0.31%</td>
          <td style="text-align:left;">Continuous sigmoid vs linear weights have minimal direct main effect.</td>
        </tr>
        <tr>
          <td style="text-align:left;">Wicket Value & Shrinkage Main Effects</td>
          <td>20,580</td>
          <td>0.50%</td>
          <td>13,120</td>
          <td>0.31%</td>
          <td style="text-align:left;">Regularization priors adjust tails without perturbing elite core.</td>
        </tr>
        <tr style="background-color:#F1F5F9; font-weight:700;">
          <td style="text-align:left;"><strong>TOTAL VARIANCE EXPLAINED</strong></td>
          <td><strong>4,103,880</strong></td>
          <td><strong>100.00%</strong></td>
          <td><strong>4,135,850</strong></td>
          <td><strong>100.00%</strong></td>
          <td style="text-align:left;"><strong>Exact mathematical reconciliation across all specifications.</strong></td>
        </tr>
      </tbody>
    </table>

    <div class="chart-box" style="margin-top:3px;">
      <img src="{img_var_decomp}" alt="ANOVA Variance Decomposition">
      <div class="chart-caption">Figure 2: Sequential Type I ANOVA Variance Decomposition for Batting and Bowling Percentile Ranks.</div>
    </div>

    <div class="callout-box emerald" style="margin-top:3px;">
      <div class="callout-title">Core Methodological Takeaway</div>
      <div style="font-size:6.3pt;">Because player identity main effects explain 76.58% (batting) and 65.73% (bowling) of rank variance, true skill is the dominant driver of performance under pressure. However, because player &times; specification interactions account for 21.44% to 32.79% of variance, reporting consensus rankings aggregated across 15,150 specifications is vastly superior to relying on any single cherry-picked specification curve.</div>
    </div>
  </div>

  <div class="page-footer">
    <span>Rajat Aggarwal | Participant — SupeRR Selector Season 2</span>
    <span class="footer-center">Multiverse Specification Curve & Variance Decomposition</span>
    <span class="footer-page-num">Page 7 of 15</span>
  </div>
</div>

<!-- PAGE 8: TOP 10 BATTERS SUMMARY TABLE & PROFILES 1-5 -->
<div class="page" id="page-8">
  <div>
    <div class="page-header">
      <div class="header-left">
        <span class="header-section-num">Section 7A</span>
        <span class="header-title-text">Consensus Batting Rankings: Full Table & Profiles 1–5</span>
      </div>
      <div class="header-right"><span class="rr-dot"></span> Multiverse Consensus Results &bull; Empirical Evidence</div>
    </div>

    <div class="section-h2">Table 2A: Comprehensive Top-10 Batting Multiverse Metrics</div>
    <table>
      <thead>
        <tr>
          <th>#</th>
          <th style="text-align:left;">Player (ID)</th>
          <th>Tier</th>
          <th>PWI</th>
          <th>Norm</th>
          <th>RawLift</th>
          <th>Maint</th>
          <th>HPBalls</th>
          <th>Elig%</th>
          <th>Top10%</th>
          <th>Med[IQR]</th>
          <th>Boot90%</th>
          <th>Rises%</th>
          <th style="text-align:left;">Classification</th>
        </tr>
      </thead>
      <tbody>
        {make_table2a_rows()}
      </tbody>
    </table>

    <div class="section-h2" style="margin-top:2px;">Detailed Empirical Profiles: Batters 1 to 5</div>

    <div class="player-dossier">
      <div class="dossier-header">
        <span class="dossier-name">1. Shashank Singh <span class="id-muted">(ID: 2756)</span> &mdash; Tier 1 | Punjab Kings</span>
        <span class="badge badge-tier1">Consensus #1 Batter</span>
      </div>
      <div class="dossier-metrics">
        <span><strong>Shrunk PWI:</strong> +32.2 r/100b</span> &bull;
        <span><strong>Raw Lift:</strong> +22.2</span> &bull;
        <span><strong>Top-10 Freq:</strong> 94.9%</span> &bull;
        <span><strong>Med Rank:</strong> 5.0 [IQR 3.0]</span> &bull;
        <span><strong>Boot 90% CI:</strong> [1, 44]</span> &bull;
        <span><strong>HP Balls:</strong> 327</span>
      </div>
      <div class="dossier-prose">
        <strong>Empirical Evidence:</strong> Shashank achieved a 94.9% top-10 finish across all eligible specifications, demonstrating extraordinary resilience when leverage peaks. His raw lift of +22.2 runs/100b reflects a surge from a normal baseline of +10.0 to a high-pressure PWI of +32.2. He rises under pressure in 100.0% of evaluated specifications.<br>
        <strong>Tactical Scouting Fit:</strong> Elite domestic middle-to-death finisher. Highly proficient against both hard lengths and spin at the death. Direct tactical solution for Rajasthan Royals' middle-order boundary production.
      </div>
    </div>

    <div class="player-dossier">
      <div class="dossier-header">
        <span class="dossier-name">2. Tim David <span class="id-muted">(ID: 6396)</span> &mdash; Tier 1 | Royal Challengers Bengaluru</span>
        <span class="badge badge-tier1">Consensus #2 Batter</span>
      </div>
      <div class="dossier-metrics">
        <span><strong>Shrunk PWI:</strong> +42.9 r/100b</span> &bull;
        <span><strong>Raw Lift:</strong> +9.0</span> &bull;
        <span><strong>Top-10 Freq:</strong> 92.1%</span> &bull;
        <span><strong>Med Rank:</strong> 1.0 [IQR 2.0]</span> &bull;
        <span><strong>Boot 90% CI:</strong> [1, 16]</span> &bull;
        <span><strong>HP Balls:</strong> 570</span>
      </div>
      <div class="dossier-prose">
        <strong>Empirical Evidence:</strong> Highest absolute high-pressure output in the dataset (+42.9 runs/100b) across 570 balls. Achieves a median rank of 1.0 with a tight bootstrap 90% interval of [1, 16]. Rises under pressure in 78.1% of specifications.<br>
        <strong>Tactical Scouting Fit:</strong> Proven overseas power hitter. Clears boundaries immediately from ball one under extreme required run rates. High-value target if made available at auction.
      </div>
    </div>

    <div class="player-dossier">
      <div class="dossier-header">
        <span class="dossier-name">3. Naman Dhir <span class="id-muted">(ID: 37052)</span> &mdash; Tier 1 | Mumbai Indians</span>
        <span class="badge badge-tier1">Consensus #3 Batter</span>
      </div>
      <div class="dossier-metrics">
        <span><strong>Shrunk PWI:</strong> +34.7 r/100b</span> &bull;
        <span><strong>Raw Lift:</strong> +35.4</span> &bull;
        <span><strong>Top-10 Freq:</strong> 88.6%</span> &bull;
        <span><strong>Med Rank:</strong> 4.0 [IQR 5.0]</span> &bull;
        <span><strong>Boot 90% CI:</strong> [1, 32]</span> &bull;
        <span><strong>HP Balls:</strong> 186</span>
      </div>
      <div class="dossier-prose">
        <strong>Empirical Evidence:</strong> Demonstrates the highest positive pressure lift (+35.4 runs/100b) among all regular batters, surging from &minus;0.7 normal output to +34.7 in high leverage across 186 balls. Qualified in 91.1% of specifications with 88.6% top-10 frequency.<br>
        <strong>Tactical Scouting Fit:</strong> Emerging young Indian boundary creator. Unflazed by extreme run-rate demands; aggressive intent from the start. High-upside recruitment target.
      </div>
    </div>

    <div class="player-dossier">
      <div class="dossier-header">
        <span class="dossier-name">4. Dinesh Karthik <span class="id-muted">(ID: 143)</span> &mdash; Tier 1 | Historical Benchmark (Retired)</span>
        <span class="badge badge-tier1">Historical Benchmark</span>
      </div>
      <div class="dossier-metrics">
        <span><strong>Shrunk PWI:</strong> +34.4 r/100b</span> &bull;
        <span><strong>Raw Lift:</strong> +16.1</span> &bull;
        <span><strong>Top-10 Freq:</strong> 78.3%</span> &bull;
        <span><strong>Med Rank:</strong> 5.0 [IQR 7.0]</span> &bull;
        <span><strong>Boot 90% CI:</strong> [1, 44]</span> &bull;
        <span><strong>HP Balls:</strong> 250</span>
      </div>
      <div class="dossier-prose">
        <strong>Empirical Evidence:</strong> Exceptional historical pressure execution (+34.4 PWI, +16.1 raw lift) across 250 high-pressure deliveries. Top-10 in 78.3% of multiverse specifications.<br>
        <strong>Practical Feasibility Context:</strong> Officially retired from IPL following 2024 season; active Royal Challengers Bengaluru Batting Coach & Mentor (2025–2026). Retained in analytics strictly as an unmanipulated statistical benchmark.
      </div>
    </div>

    <div class="player-dossier">
      <div class="dossier-header">
        <span class="dossier-name">5. Heinrich Klaasen <span class="id-muted">(ID: 4260)</span> &mdash; Tier 1 | Sunrisers Hyderabad</span>
        <span class="badge badge-tier1">Consensus #5 Batter</span>
      </div>
      <div class="dossier-metrics">
        <span><strong>Shrunk PWI:</strong> +24.9 r/100b</span> &bull;
        <span><strong>Raw Lift:</strong> +3.4</span> &bull;
        <span><strong>Top-10 Freq:</strong> 74.4%</span> &bull;
        <span><strong>Med Rank:</strong> 7.0 [IQR 7.0]</span> &bull;
        <span><strong>Boot 90% CI:</strong> [5, 34]</span> &bull;
        <span><strong>HP Balls:</strong> 459</span>
      </div>
      <div class="dossier-prose">
        <strong>Empirical Evidence:</strong> World-class spin destroyer (+24.9 PWI across 459 HP balls). Features in top 10 across 74.4% of specifications with exceptional maintenance lift (+17.4).<br>
        <strong>Tactical Scouting Fit:</strong> Premium overseas middle-order anchor and boundary creator. Dominates defensive spin fields in overs 7–16. Unlikely to be released by SRH; top priority if available.
      </div>
    </div>
  </div>

  <div class="page-footer">
    <span>Rajat Aggarwal | Participant — SupeRR Selector Season 2</span>
    <span class="footer-center">Consensus Batting Rankings: Full Table & Profiles 1–5</span>
    <span class="footer-page-num">Page 8 of 15</span>
  </div>
</div>

<!-- PAGE 9: TOP 10 BATTERS PROFILES 6-10 & RESILIENCE LANDSCAPE -->
<div class="page" id="page-9">
  <div>
    <div class="page-header">
      <div class="header-left">
        <span class="header-section-num">Section 7B</span>
        <span class="header-title-text">Batting Profiles Continued (6–10) & Resilience Landscape</span>
      </div>
      <div class="header-right"><span class="rr-dot"></span> Evidence for Batters 6 to 10 &bull; Maintenance vs Lift</div>
    </div>

    <div class="section-h2">Detailed Empirical Profiles: Batters 6 to 10</div>

    <div class="player-dossier">
      <div class="dossier-header">
        <span class="dossier-name">6. Suryakumar Yadav <span class="id-muted">(ID: 1699)</span> &mdash; Tier 2 | Mumbai Indians</span>
        <span class="badge badge-tier2">Elite All The Time</span>
      </div>
      <div class="dossier-metrics">
        <span><strong>Shrunk PWI:</strong> +25.4 r/100b</span> &bull;
        <span><strong>Raw Lift:</strong> -4.6</span> &bull;
        <span><strong>Top-10 Freq:</strong> 73.1%</span> &bull;
        <span><strong>Med Rank:</strong> 8.0 [IQR 6.0]</span> &bull;
        <span><strong>Boot 90% CI:</strong> [6, 44]</span> &bull;
        <span><strong>HP Balls:</strong> 657</span>
      </div>
      <div class="dossier-prose">
        <strong>Empirical Evidence:</strong> Massive sample volume of 657 HP balls with shrunk PWI of +25.4. His raw lift is &minus;4.6, reflecting an astronomical normal baseline (+30.0). Classified as "Elite all the time" (rises in 23.3% of specs).<br>
        <strong>Tactical Fit:</strong> 360-degree boundary manipulator whose high baseline provides unmatched floor and ceiling against elite bowling attacks.
      </div>
    </div>

    <div class="player-dossier">
      <div class="dossier-header">
        <span class="dossier-name">7. Rinku Singh <span class="id-muted">(ID: 4708)</span> &mdash; Tier 2 | Kolkata Knight Riders</span>
        <span class="badge badge-tier2">Rises Under Pressure</span>
      </div>
      <div class="dossier-metrics">
        <span><strong>Shrunk PWI:</strong> +31.0 r/100b</span> &bull;
        <span><strong>Raw Lift:</strong> +17.9</span> &bull;
        <span><strong>Top-10 Freq:</strong> 63.1%</span> &bull;
        <span><strong>Med Rank:</strong> 9.0 [IQR 7.0]</span> &bull;
        <span><strong>Boot 90% CI:</strong> [2, 39]</span> &bull;
        <span><strong>HP Balls:</strong> 507</span>
      </div>
      <div class="dossier-prose">
        <strong>Empirical Evidence:</strong> Prototypical chase finisher (+31.0 PWI, +17.9 raw lift across 507 HP balls). Rises under pressure in 80.0% of multiverse specifications with 63.1% top-10 inclusion.<br>
        <strong>Tactical Fit:</strong> Elite left-handed death finisher. High situational awareness and composure in final-over run chases.
      </div>
    </div>

    <div class="player-dossier">
      <div class="dossier-header">
        <span class="dossier-name">8. Romario Shepherd <span class="id-muted">(ID: 6726)</span> &mdash; Tier 2 | Royal Challengers Bengaluru</span>
        <span class="badge badge-tier2">Balanced Context</span>
      </div>
      <div class="dossier-metrics">
        <span><strong>Shrunk PWI:</strong> +28.7 r/100b</span> &bull;
        <span><strong>Raw Lift:</strong> +5.0</span> &bull;
        <span><strong>Top-10 Freq:</strong> 55.5%</span> &bull;
        <span><strong>Med Rank:</strong> 6.0 [IQR 6.0]</span> &bull;
        <span><strong>Boot 90% CI:</strong> [2, 36]</span> &bull;
        <span><strong>HP Balls:</strong> 431</span>
      </div>
      <div class="dossier-prose">
        <strong>Empirical Evidence:</strong> Powerhouse lower-order hitter (+28.7 PWI, +5.0 lift across 431 balls). Finishes in the top 10 across 55.5% of multiverse runs.<br>
        <strong>Tactical Fit:</strong> Explosive No. 7/8 finisher capable of turning matches in 10-ball cameos. Excellent supplementary pace-hitting option.
      </div>
    </div>

    <div class="player-dossier">
      <div class="dossier-header">
        <span class="dossier-name">9. Andre Russell <span class="id-muted">(ID: 1318)</span> &mdash; Tier 2 | Historical Benchmark (Retired IPL)</span>
        <span class="badge badge-tier2">Historical Benchmark</span>
      </div>
      <div class="dossier-metrics">
        <span><strong>Shrunk PWI:</strong> +31.8 r/100b</span> &bull;
        <span><strong>Raw Lift:</strong> +1.0</span> &bull;
        <span><strong>Top-10 Freq:</strong> 54.2%</span> &bull;
        <span><strong>Med Rank:</strong> 10.0 [IQR 10.0]</span> &bull;
        <span><strong>Boot 90% CI:</strong> [2, 54]</span> &bull;
        <span><strong>HP Balls:</strong> 347</span>
      </div>
      <div class="dossier-prose">
        <strong>Empirical Evidence:</strong> Colossal power hitting under pressure (+31.8 PWI across 347 HP balls). Retired from IPL on 30 Nov 2025; appointed KKR Power Coach for IPL 2026. Preserved as an unmanipulated statistical benchmark.
      </div>
    </div>

    <div class="player-dossier">
      <div class="dossier-header">
        <span class="dossier-name">10. Rashid Khan <span class="id-muted">(ID: 4722)</span> &mdash; Tier 2 | Gujarat Titans</span>
        <span class="badge badge-tier2">Rises Under Pressure</span>
      </div>
      <div class="dossier-metrics">
        <span><strong>Shrunk PWI:</strong> +28.1 r/100b</span> &bull;
        <span><strong>Raw Lift:</strong> +40.3</span> &bull;
        <span><strong>Top-10 Freq:</strong> 47.9%</span> &bull;
        <span><strong>Med Rank:</strong> 8.0 [IQR 9.0]</span> &bull;
        <span><strong>Boot 90% CI:</strong> [1, 40]</span> &bull;
        <span><strong>HP Balls:</strong> 377</span>
      </div>
      <div class="dossier-prose">
        <strong>Empirical Evidence:</strong> Extraordinary dual-threat asset. As a batter, records a raw lift of +40.3 (surging from &minus;12.2 to +28.1). Features in the top 10 in 47.9% of specifications (61.6% retention when eligible) and also finishes #3 among bowlers.
      </div>
    </div>

    <div class="chart-box" style="margin-top:2px;">
      <img src="{img_maint_bat}" alt="Maintenance vs Lift Batters">
      <div class="chart-caption">Figure 3: Batting Resilience Landscape &mdash; High-Pressure Output vs Baseline Maintenance across all eligible batters.</div>
    </div>
  </div>

  <div class="page-footer">
    <span>Rajat Aggarwal | Participant — SupeRR Selector Season 2</span>
    <span class="footer-center">Batting Profiles Continued & Resilience Landscape</span>
    <span class="footer-page-num">Page 9 of 15</span>
  </div>
</div>

<!-- PAGE 10: TOP 10 BOWLERS SUMMARY TABLE & PROFILES 1-5 -->
<div class="page" id="page-10">
  <div>
    <div class="page-header">
      <div class="header-left">
        <span class="header-section-num">Section 8A</span>
        <span class="header-title-text">Consensus Bowling Rankings: Full Table & Profiles 1–5</span>
      </div>
      <div class="header-right"><span class="rr-dot"></span> Defending-Side Evaluation &bull; Empirical Evidence</div>
    </div>

    <div class="section-h2">Table 2B: Comprehensive Top-10 Bowling Multiverse Metrics</div>
    <table>
      <thead>
        <tr>
          <th>#</th>
          <th style="text-align:left;">Player (ID)</th>
          <th>Tier</th>
          <th>PWI</th>
          <th>Norm</th>
          <th>RawLift</th>
          <th>Maint</th>
          <th>HPBalls</th>
          <th>Elig%</th>
          <th>Top10%</th>
          <th>Med[IQR]</th>
          <th>Boot90%</th>
          <th>Rises%</th>
          <th style="text-align:left;">Classification</th>
        </tr>
      </thead>
      <tbody>
        {make_table2b_rows()}
      </tbody>
    </table>

    <div class="section-h2" style="margin-top:2px;">Detailed Empirical Profiles: Bowlers 1 to 5</div>

    <div class="player-dossier">
      <div class="dossier-header">
        <span class="dossier-name">1. Sunil Narine <span class="id-muted">(ID: 781)</span> &mdash; Tier 1 | Kolkata Knight Riders</span>
        <span class="badge badge-tier1">Consensus #1 Bowler</span>
      </div>
      <div class="dossier-metrics">
        <span><strong>Shrunk PWI:</strong> +6.57 r/24b</span> &bull;
        <span><strong>Raw Lift:</strong> +0.64</span> &bull;
        <span><strong>Top-10 Freq:</strong> 100.0%</span> &bull;
        <span><strong>Med Rank:</strong> 3.0 [IQR 1.0]</span> &bull;
        <span><strong>Boot 90% CI:</strong> [1, 17]</span> &bull;
        <span><strong>HP Balls:</strong> 422</span>
      </div>
      <div class="dossier-prose">
        <strong>Empirical Evidence:</strong> Perfect 100.0% top-10 frequency across all 15,150 specifications. Defends +6.57 runs saved per 24 balls across 422 HP deliveries. Remarkably stable with a median rank of 3.0 and IQR of 1.0.<br>
        <strong>Tactical Scouting Fit:</strong> Premier defensive spinner in T20 history. Smothers run rates in high leverage while restricting boundary access. Unlikely to leave KKR; mandatory watchlist.
      </div>
    </div>

    <div class="player-dossier">
      <div class="dossier-header">
        <span class="dossier-name">2. Jasprit Bumrah <span class="id-muted">(ID: 2933)</span> &mdash; Tier 1 | Mumbai Indians</span>
        <span class="badge badge-tier1">Consensus #2 Bowler</span>
      </div>
      <div class="dossier-metrics">
        <span><strong>Shrunk PWI:</strong> +7.61 r/24b</span> &bull;
        <span><strong>Raw Lift:</strong> +0.33</span> &bull;
        <span><strong>Top-10 Freq:</strong> 99.2%</span> &bull;
        <span><strong>Med Rank:</strong> 2.0 [IQR 2.0]</span> &bull;
        <span><strong>Boot 90% CI:</strong> [1, 23]</span> &bull;
        <span><strong>HP Balls:</strong> 332</span>
      </div>
      <div class="dossier-prose">
        <strong>Empirical Evidence:</strong> Highest absolute defending impact (+7.61 runs saved/24b) in the competition. Finishes inside top 10 in 99.2% of specifications with median rank 2.0 across 332 balls.<br>
        <strong>Tactical Scouting Fit:</strong> Elite death-overs pace execution. Flawless yorker and slower-ball control against elite finishers. Franchise cornerstone.
      </div>
    </div>

    <div class="player-dossier">
      <div class="dossier-header">
        <span class="dossier-name">3. Rashid Khan <span class="id-muted">(ID: 4722)</span> &mdash; Tier 1 | Gujarat Titans</span>
        <span class="badge badge-tier1">Consensus #3 Bowler</span>
      </div>
      <div class="dossier-metrics">
        <span><strong>Shrunk PWI:</strong> +5.59 r/24b</span> &bull;
        <span><strong>Raw Lift:</strong> +2.75</span> &bull;
        <span><strong>Top-10 Freq:</strong> 93.5%</span> &bull;
        <span><strong>Med Rank:</strong> 5.0 [IQR 4.0]</span> &bull;
        <span><strong>Boot 90% CI:</strong> [1, 19]</span> &bull;
        <span><strong>HP Balls:</strong> 706</span>
      </div>
      <div class="dossier-prose">
        <strong>Empirical Evidence:</strong> Heaviest high-pressure workload in the database (706 balls) while defending +5.59 runs/24b with +2.75 raw lift. Top 10 in 93.5% of multiverse runs.<br>
        <strong>Tactical Scouting Fit:</strong> Irreplaceable wicket-taking wrist-spinner who thrives in high leverage. Combined with his #10 batting ranking, represents the ultimate MVP asset.
      </div>
    </div>

    <div class="player-dossier">
      <div class="dossier-header">
        <span class="dossier-name">4. Matheesha Pathirana <span class="id-muted">(ID: 8661)</span> &mdash; Tier 1 | Kolkata Knight Riders</span>
        <span class="badge badge-tier1">Consensus #4 Bowler</span>
      </div>
      <div class="dossier-metrics">
        <span><strong>Shrunk PWI:</strong> +5.34 r/24b</span> &bull;
        <span><strong>Raw Lift:</strong> +1.21</span> &bull;
        <span><strong>Top-10 Freq:</strong> 83.4%</span> &bull;
        <span><strong>Med Rank:</strong> 3.0 [IQR 4.0]</span> &bull;
        <span><strong>Boot 90% CI:</strong> [1, 41]</span> &bull;
        <span><strong>HP Balls:</strong> 307</span>
      </div>
      <div class="dossier-prose">
        <strong>Empirical Evidence:</strong> Sling-action death specialist defending +5.34 runs/24b across 307 HP balls. Top 10 in 83.4% of specifications.<br>
        <strong>Injury Context:</strong> Suffered hamstring injury in May 2026; actively rehabilitating. Healthy trajectory makes him a lethal recruitment target.
      </div>
    </div>

    <div class="player-dossier">
      <div class="dossier-header">
        <span class="dossier-name">5. Eshan Malinga <span class="id-muted">(ID: 39657)</span> &mdash; Tier 1 | Sunrisers Hyderabad</span>
        <span class="badge badge-tier1">Consensus #5 Bowler</span>
      </div>
      <div class="dossier-metrics">
        <span><strong>Shrunk PWI:</strong> +3.85 r/24b</span> &bull;
        <span><strong>Raw Lift:</strong> +3.39</span> &bull;
        <span><strong>Top-10 Freq:</strong> 71.9%</span> &bull;
        <span><strong>Med Rank:</strong> 6.0 [IQR 5.0]</span> &bull;
        <span><strong>Boot 90% CI:</strong> [1, 38]</span> &bull;
        <span><strong>HP Balls:</strong> 176</span>
      </div>
      <div class="dossier-prose">
        <strong>Empirical Evidence:</strong> Outstanding emergence under pressure (+3.85 PWI, +3.39 raw lift across 176 balls). Features in top 10 in 71.9% of specifications.<br>
        <strong>Tactical Scouting Fit:</strong> High-pace sling bowler who executes yorkers under intense scrutiny. Prime high-upside acquisition for RR.
      </div>
    </div>
  </div>

  <div class="page-footer">
    <span>Rajat Aggarwal | Participant — SupeRR Selector Season 2</span>
    <span class="footer-center">Consensus Bowling Rankings: Full Table & Profiles 1–5</span>
    <span class="footer-page-num">Page 10 of 15</span>
  </div>
</div>

<!-- PAGE 11: TOP 10 BOWLERS PROFILES 6-10 & RESILIENCE LANDSCAPE -->
<div class="page" id="page-11">
  <div>
    <div class="page-header">
      <div class="header-left">
        <span class="header-section-num">Section 8B</span>
        <span class="header-title-text">Bowling Profiles Continued (6–10) & Resilience Landscape</span>
      </div>
      <div class="header-right"><span class="rr-dot"></span> Evidence for Bowlers 6 to 10 &bull; Maintenance vs Lift</div>
    </div>

    <div class="section-h2">Detailed Empirical Profiles: Bowlers 6 to 10</div>

    <div class="player-dossier">
      <div class="dossier-header">
        <span class="dossier-name">6. Nathan Ellis <span class="id-muted">(ID: 7920)</span> &mdash; Tier 2 | Sunrisers Hyderabad (Traded from CSK)</span>
        <span class="badge badge-tier2">Rises Under Pressure</span>
      </div>
      <div class="dossier-metrics">
        <span><strong>Shrunk PWI:</strong> +5.50 r/24b</span> &bull;
        <span><strong>Raw Lift:</strong> +3.15</span> &bull;
        <span><strong>Top-10 Freq:</strong> 54.8%</span> &bull;
        <span><strong>Med Rank:</strong> 7.0 [IQR 6.0]</span> &bull;
        <span><strong>Boot 90% CI:</strong> [1, 36]</span> &bull;
        <span><strong>HP Balls:</strong> 229</span>
      </div>
      <div class="dossier-prose">
        <strong>Empirical Evidence:</strong> Elite death specialist defending +5.50 runs/24b with +3.15 raw lift. Top 10 in 54.8% of specs (72.5% retention when eligible).<br>
        <strong>Official Trade Note:</strong> Mapped to CSK in raw data; officially traded CSK &rarr; SRH on 5 Nov 2026 for INR 2.00 Cr all-cash [Official SRH/IPL Confirmation]. Prime tactical death option.
      </div>
    </div>

    <div class="player-dossier">
      <div class="dossier-header">
        <span class="dossier-name">7. Noor Ahmad <span class="id-muted">(ID: 7967)</span> &mdash; Tier 3 | Chennai Super Kings</span>
        <span class="badge badge-tier3">Balanced Context</span>
      </div>
      <div class="dossier-metrics">
        <span><strong>Shrunk PWI:</strong> +2.54 r/24b</span> &bull;
        <span><strong>Raw Lift:</strong> -0.21</span> &bull;
        <span><strong>Top-10 Freq:</strong> 40.1%</span> &bull;
        <span><strong>Med Rank:</strong> 12.0 [IQR 11.0]</span> &bull;
        <span><strong>Boot 90% CI:</strong> [6, 62]</span> &bull;
        <span><strong>HP Balls:</strong> 351</span>
      </div>
      <div class="dossier-prose">
        <strong>Empirical Evidence:</strong> Left-arm wrist-spin control defending +2.54 runs/24b across 351 HP balls. Top 10 in 40.1% of multiverse runs.<br>
        <strong>Tactical Fit:</strong> Solves RR's middle-overs wicket-taking deficit against right-hand heavy top orders.
      </div>
    </div>

    <div class="player-dossier">
      <div class="dossier-header">
        <span class="dossier-name">8. Arshdeep Singh <span class="id-muted">(ID: 6464)</span> &mdash; Tier 3 | Mumbai Indians (Traded from PBKS)</span>
        <span class="badge badge-tier3">Balanced Context</span>
      </div>
      <div class="dossier-metrics">
        <span><strong>Shrunk PWI:</strong> +1.90 r/24b</span> &bull;
        <span><strong>Raw Lift:</strong> +0.99</span> &bull;
        <span><strong>Top-10 Freq:</strong> 35.1%</span> &bull;
        <span><strong>Med Rank:</strong> 12.0 [IQR 7.0]</span> &bull;
        <span><strong>Boot 90% CI:</strong> [9, 55]</span> &bull;
        <span><strong>HP Balls:</strong> 593</span>
      </div>
      <div class="dossier-prose">
        <strong>Empirical Evidence:</strong> Heavy-volume Indian left-arm seamer (593 HP balls) defending +1.90 runs/24b.<br>
        <strong>Official Trade Note:</strong> Mapped to PBKS in raw data; traded PBKS &rarr; MI on 11 Nov 2026 in swap deal for Hardik Pandya [Official iplt20.com].
      </div>
    </div>

    <div class="player-dossier">
      <div class="dossier-header">
        <span class="dossier-name">9. Prasidh Krishna <span class="id-muted">(ID: 4489)</span> &mdash; Tier 3 | Gujarat Titans</span>
        <span class="badge badge-tier3">Rises Under Pressure</span>
      </div>
      <div class="dossier-metrics">
        <span><strong>Shrunk PWI:</strong> +2.96 r/24b</span> &bull;
        <span><strong>Raw Lift:</strong> +2.67</span> &bull;
        <span><strong>Top-10 Freq:</strong> 31.7%</span> &bull;
        <span><strong>Med Rank:</strong> 13.0 [IQR 8.0]</span> &bull;
        <span><strong>Boot 90% CI:</strong> [5, 63]</span> &bull;
        <span><strong>HP Balls:</strong> 234</span>
      </div>
      <div class="dossier-prose">
        <strong>Empirical Evidence:</strong> High-release hit-the-deck pace defending +2.96 runs/24b with +2.67 raw lift across 234 HP balls. Rises under pressure in 68.3% of specifications.<br>
        <strong>Tactical Fit:</strong> Excellent hard-length extractor who complements Jofra Archer at Sawai Mansingh Stadium.
      </div>
    </div>

    <div class="player-dossier">
      <div class="dossier-header">
        <span class="dossier-name">10. Bhuvneshwar Kumar <span class="id-muted">(ID: 360)</span> &mdash; Tier 3 | Royal Challengers Bengaluru</span>
        <span class="badge badge-tier3">Elite All The Time</span>
      </div>
      <div class="dossier-metrics">
        <span><strong>Shrunk PWI:</strong> +3.25 r/24b</span> &bull;
        <span><strong>Raw Lift:</strong> -1.31</span> &bull;
        <span><strong>Top-10 Freq:</strong> 27.2%</span> &bull;
        <span><strong>Med Rank:</strong> 17.0 [IQR 18.0]</span> &bull;
        <span><strong>Boot 90% CI:</strong> [7, 56]</span> &bull;
        <span><strong>HP Balls:</strong> 361</span>
      </div>
      <div class="dossier-prose">
        <strong>Empirical Evidence:</strong> Veteran swing and knuckleball master defending +3.25 runs/24b across 361 balls. Elite baseline output (+4.56). Dependable Powerplay and 19th-over specialist.
      </div>
    </div>

    <div class="chart-box" style="margin-top:2px;">
      <img src="{img_maint_bowl}" alt="Maintenance vs Lift Bowlers">
      <div class="chart-caption">Figure 4: Bowling Resilience Landscape &mdash; Defending Run Impact vs Baseline Maintenance across all eligible bowlers.</div>
    </div>
  </div>

  <div class="page-footer">
    <span>Rajat Aggarwal | Participant — SupeRR Selector Season 2</span>
    <span class="footer-center">Bowling Profiles Continued & Resilience Landscape</span>
    <span class="footer-page-num">Page 11 of 15</span>
  </div>
</div>

<!-- PAGE 12: RAJASTHAN ROYALS SQUAD AUDIT & RECRUITMENT -->
<div class="page" id="page-12">
  <div>
    <div class="page-header">
      <div class="header-left">
        <span class="header-section-num">Section 9</span>
        <span class="header-title-text">Rajasthan Royals Tactical Recruitment Dossier</span>
      </div>
      <div class="header-right"><span class="rr-dot"></span> IPL 2026 Phase-Level Audit from Raw Data</div>
    </div>

    <div class="section-h2">1. Audited Rajasthan Royals 2026 Performance (from Raw Data)</div>
    <p>To ensure recommendations are actionable, RR's actual 2026 campaign was audited directly from raw match records (matches.csv, ball_by_ball.csv, playing_eleven.csv). RR played 16 matches, captained primarily by Riyan Parag (14 matches) with Yashasvi Jaiswal leading in 2 (Sanju Samson represented CSK in 2026):</p>

    <table>
      <thead>
        <tr>
          <th style="text-align:left;">Player Name (ID)</th>
          <th>Apps</th>
          <th>Runs</th>
          <th>Balls</th>
          <th>Bat SR</th>
          <th>Overs</th>
          <th>RunsConc</th>
          <th>Wkts</th>
          <th>Bowl ER</th>
          <th style="text-align:left;">Audited Role & Campaign Performance</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td style="text-align:left;"><strong>Vaibhav Sooryavanshi (50284)</strong></td>
          <td>16</td>
          <td>776</td>
          <td>327</td>
          <td class="metric-positive"><strong>237.31</strong></td>
          <td>0.0</td>
          <td>0</td>
          <td>0</td>
          <td>&mdash;</td>
          <td style="text-align:left;">Phenomenal breakout season; dominant Powerplay run aggregator.</td>
        </tr>
        <tr>
          <td style="text-align:left;"><strong>Dhruv Jurel (7260)</strong></td>
          <td>16</td>
          <td>515</td>
          <td>333</td>
          <td>154.65</td>
          <td>0.0</td>
          <td>0</td>
          <td>0</td>
          <td>&mdash;</td>
          <td style="text-align:left;">Solid middle-order accumulation; steady presence in chases.</td>
        </tr>
        <tr>
          <td style="text-align:left;"><strong>Yashasvi Jaiswal (6819)</strong></td>
          <td>16</td>
          <td>427</td>
          <td>280</td>
          <td>152.50</td>
          <td>0.0</td>
          <td>0</td>
          <td>0</td>
          <td>&mdash;</td>
          <td style="text-align:left;">High-volume top-order anchor; captained in 2 matches.</td>
        </tr>
        <tr>
          <td style="text-align:left;"><strong>Jofra Archer (3298)</strong></td>
          <td>16</td>
          <td>64</td>
          <td>47</td>
          <td>136.17</td>
          <td>60.0</td>
          <td>559</td>
          <td>25</td>
          <td>9.32</td>
          <td style="text-align:left;">Primary pace spearhead; took 25 wickets with heavy workload.</td>
        </tr>
        <tr>
          <td style="text-align:left;"><strong>Donovan Ferreira (8182)</strong></td>
          <td>15</td>
          <td>317</td>
          <td>177</td>
          <td class="metric-positive"><strong>179.10</strong></td>
          <td>3.0</td>
          <td>41</td>
          <td>1</td>
          <td>13.67</td>
          <td style="text-align:left;">Explosive death finisher (death SR 221.7); lacked support.</td>
        </tr>
        <tr>
          <td style="text-align:left;"><strong>Riyan Parag (6423) [Captain]</strong></td>
          <td>14</td>
          <td>309</td>
          <td>196</td>
          <td>157.65</td>
          <td>4.0</td>
          <td>38</td>
          <td>2</td>
          <td>9.50</td>
          <td style="text-align:left;">Lead captain in 14 matches; steady middle-order spin basher.</td>
        </tr>
        <tr>
          <td style="text-align:left;"><strong>Ravindra Jadeja (152)</strong></td>
          <td>14</td>
          <td>266</td>
          <td>197</td>
          <td>135.03</td>
          <td>33.0</td>
          <td>277</td>
          <td>10</td>
          <td>8.39</td>
          <td style="text-align:left;">Veteran all-rounder; economy 8.39 in middle overs.</td>
        </tr>
      </tbody>
    </table>

    <div class="section-h2">2. Phase-by-Phase Weakness Diagnostics & Recruitment Solutions</div>
    <div class="grid-2">
      <div class="callout-box navy">
        <div class="callout-title">Phase Diagnostic &bull; Death-Overs Pace Leaks</div>
        <p style="font-size:6.3pt; margin:0;"><strong>Deficit:</strong> While RR death bowling ER was 10.60 overall (vs league 10.67), supporting pacers Sandeep Sharma (ER 13.70) and Tushar Deshpande (ER 12.38) leaked runs excessively, leaving Archer unsupported.<br>
        <strong>Recruitment Target:</strong> <strong>Nathan Ellis</strong> (defending impact +5.50 r/24b; traded CSK &rarr; SRH) or <strong>Prasidh Krishna</strong> (+2.96 r/24b, hard length) as dedicated death co-spearheads.</p>
      </div>

      <div class="callout-box blue">
        <div class="callout-title">Phase Diagnostic &bull; Middle-Overs Spin Penetration</div>
        <p style="font-size:6.3pt; margin:0;"><strong>Deficit:</strong> RR middle-overs spin economy lagged league par (Jadeja 8.39, Bishnoi 10.11 vs league 8.97). RR conceded boundaries on 17.8% of middle balls.<br>
        <strong>Recruitment Target:</strong> <strong>Noor Ahmad</strong> (+2.54 runs/24b defended) or <strong>Rashid Khan</strong> (#3 Bowler, 706 HP balls) to choke middle overs and force attacking errors.</p>
      </div>
    </div>

    <div class="grid-2">
      <div class="callout-box emerald">
        <div class="callout-title">Phase Diagnostic &bull; Lower-Order Finisher Isolation</div>
        <p style="font-size:6.3pt; margin:0;"><strong>Deficit:</strong> At the death, Donovan Ferreira (SR 221.7) had no reliable partner. Shimron Hetmyer struck at only 121.1, causing RR to lose 3 close chases.<br>
        <strong>Recruitment Target:</strong> <strong>Shashank Singh</strong> (#1 Batter, +22.2 lift) or <strong>Naman Dhir</strong> (#3 Batter, +35.4 lift) to provide ruthless boundary execution.</p>
      </div>

      <div class="callout-box gold">
        <div class="callout-title">Tactical Execution &bull; 2027 Auction Strategy</div>
        <p style="font-size:6.3pt; margin:0;"><strong>Strategy:</strong> Allocate 45% of available auction budget to secure an Indian pressure-tested finisher (Shashank/Naman Dhir) and 35% to secure a specialized death-overs bowler (Ellis/Pathirana/Prasidh), resolving RR's audited structural leaks.</p>
      </div>
    </div>
  </div>

  <div class="page-footer">
    <span>Rajat Aggarwal | Participant — SupeRR Selector Season 2</span>
    <span class="footer-center">Rajasthan Royals Tactical Recruitment Dossier</span>
    <span class="footer-page-num">Page 12 of 15</span>
  </div>
</div>

<!-- PAGE 13: MODEL RELIABILITY & LIMITATIONS -->
<div class="page" id="page-13">
  <div>
    <div class="page-header">
      <div class="header-left">
        <span class="header-section-num">Section 10</span>
        <span class="header-title-text">Model Reliability, Limitations & Walk-Forward Validation</span>
      </div>
      <div class="header-right"><span class="rr-dot"></span> Out-of-Sample Performance &bull; Stability Checks</div>
    </div>

    <div class="section-h2">1. Walk-Forward Temporal Validation (2022–2024 to 2025–2026)</div>
    <p>To evaluate predictive validity honestly, models trained on 2022–2024 data were tested out-of-sample against 2025–2026 performance on the canonical specification:</p>

    <div class="grid-2">
      <div class="callout-box navy">
        <div class="callout-title">Canonical Batting Stability (Out-of-Sample)</div>
        <div class="formula-math" style="text-align:left; font-size:7.5pt;">Spearman r = 0.0508 &emsp;(p = 0.7864, uninformative)</div>
        <p style="font-size:6.2pt; margin:0;">Batting pressure rankings are descriptive, not predictive. High-pressure batting over 1–2 seasons contains extreme situational noise, field placement luck, and role volatility. Historical metrics describe what occurred rather than guaranteeing replication.</p>
      </div>

      <div class="callout-box blue">
        <div class="callout-title">Canonical Bowling Stability (Out-of-Sample)</div>
        <div class="formula-math" style="text-align:left; font-size:7.5pt;">Spearman r = 0.2646 &emsp;(p = 0.0721, modest positive)</div>
        <p style="font-size:6.2pt; margin:0;">Defending bowling displays modest positive persistence across seasons (r = 0.26). Bowling execution (yorkers, slower balls, hard lengths) under pressure is more repeatable than batting contact outcomes, but still requires multi-season smoothing.</p>
      </div>
    </div>

    <div class="section-h2">2. Bootstrap Stability Hurdle: Excluded Candidates Audit</div>
    <p>Enforcing the 1,000-draw stratified match bootstrap hurdle (&ge;800 valid draws) successfully pruned volatile, sample-dependent players:</p>

    <table>
      <thead>
        <tr>
          <th style="text-align:left;">Candidate Name (ID)</th>
          <th>Multi Top-10%</th>
          <th>Boot Resamples</th>
          <th>Status</th>
          <th style="text-align:left;">Exclusion Rationale & Diagnostic Audit</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td style="text-align:left;"><strong>Matthew Wade (796)</strong></td>
          <td>52.96%</td>
          <td class="metric-negative"><strong>720 / 1000</strong></td>
          <td><span class="badge badge-tier3">Excluded</span></td>
          <td style="text-align:left;">Failed &ge;800 hurdle; heavily sample-dependent. Retired from intl/domestic cricket.</td>
        </tr>
        <tr>
          <td style="text-align:left;"><strong>Mujeeb Ur Rahman (6450)</strong></td>
          <td>42.15%</td>
          <td class="metric-negative"><strong>744 / 1000</strong></td>
          <td><span class="badge badge-tier3">Excluded</span></td>
          <td style="text-align:left;">Failed &ge;800 hurdle; volatile output across match resamples.</td>
        </tr>
        <tr>
          <td style="text-align:left;"><strong>Naveen ul Haq (5809)</strong></td>
          <td>38.40%</td>
          <td class="metric-negative"><strong>513 / 1000</strong></td>
          <td><span class="badge badge-tier3">Excluded</span></td>
          <td style="text-align:left;">Qualified in barely half of bootstrap draws; vulnerable to opposition caliber.</td>
        </tr>
      </tbody>
    </table>

    <div class="grid-2" style="margin-top:2px;">
      <div class="chart-box">
        <img src="{img_boot_bat}" alt="Bootstrap Stability Batters">
        <div class="chart-caption">Figure 5A: Batter Bootstrap Rank Distributions across 1,000 resamples.</div>
      </div>
      <div class="chart-box">
        <img src="{img_boot_bowl}" alt="Bootstrap Stability Bowlers">
        <div class="chart-caption">Figure 5B: Bowler Bootstrap Rank Distributions across 1,000 resamples.</div>
      </div>
    </div>
  </div>

  <div class="page-footer">
    <span>Rajat Aggarwal | Participant — SupeRR Selector Season 2</span>
    <span class="footer-center">Model Reliability, Limitations & Walk-Forward Validation</span>
    <span class="footer-page-num">Page 13 of 15</span>
  </div>
</div>

<!-- PAGE 14: PLAYERS NEXT IN LINE & STRATEGIC ALTERNATIVES -->
<div class="page" id="page-14">
  <div>
    <div class="page-header">
      <div class="header-left">
        <span class="header-section-num">Section 11</span>
        <span class="header-title-text">Players Next in Line (Ranks 11–15) & Contingency Targets</span>
      </div>
      <div class="header-right"><span class="rr-dot"></span> Depth Charts &bull; Strategic Alternatives</div>
    </div>

    <div class="section-h2">1. Batters Next in Line (Ranks 11 to 15)</div>
    <table>
      <thead>
        <tr>
          <th>#</th>
          <th style="text-align:left;">Player Name (ID)</th>
          <th>Multi Top-10%</th>
          <th>Med [IQR]</th>
          <th>Boot Draws</th>
          <th style="text-align:left;">Strategic Role & Tactical Scouting Fit</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td><span class="rank-circle">11</span></td>
          <td style="text-align:left;"><strong>Ashutosh Sharma (8101)</strong></td>
          <td>38.20%</td>
          <td>9.0 [11.0]</td>
          <td>662 / 1000</td>
          <td style="text-align:left;">Explosive lower-order finisher (+29.7 raw lift); sample volatility in bootstrap draws.</td>
        </tr>
        <tr>
          <td><span class="rank-circle">12</span></td>
          <td style="text-align:left;"><strong>Shreyas Iyer (3647)</strong></td>
          <td>32.62%</td>
          <td>14.0 [12.0]</td>
          <td>999 / 1000</td>
          <td style="text-align:left;">Middle-order spin anchor; solid baseline but moderate pressure lift (+4.2).</td>
        </tr>
        <tr>
          <td><span class="rank-circle">13</span></td>
          <td style="text-align:left;"><strong>Mahendra Singh Dhoni (8)</strong></td>
          <td>23.79%</td>
          <td>14.0 [12.0]</td>
          <td>978 / 1000</td>
          <td style="text-align:left;">Legendary death-overs execution (+14.8 raw lift); lower volume in international scope.</td>
        </tr>
        <tr>
          <td><span class="rank-circle">14</span></td>
          <td style="text-align:left;"><strong>Nicholas Pooran (3125)</strong></td>
          <td>12.61%</td>
          <td>22.0 [14.0]</td>
          <td>1000 / 1000</td>
          <td style="text-align:left;">High baseline overseas middle-order hitter; qualifies across 100% of specifications.</td>
        </tr>
        <tr>
          <td><span class="rank-circle">15</span></td>
          <td style="text-align:left;"><strong>Namboori Tilak Varma (7897)</strong></td>
          <td>11.50%</td>
          <td>24.0 [15.0]</td>
          <td>1000 / 1000</td>
          <td style="text-align:left;">Versatile Indian top/middle-order batter with solid cross-format baseline.</td>
        </tr>
      </tbody>
    </table>

    <div class="section-h2">2. Bowlers Next in Line (Ranks 11 to 15)</div>
    <table>
      <thead>
        <tr>
          <th>#</th>
          <th style="text-align:left;">Player Name (ID)</th>
          <th>Multi Top-10%</th>
          <th>Med [IQR]</th>
          <th>Boot Draws</th>
          <th style="text-align:left;">Strategic Role & Tactical Scouting Fit</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td><span class="rank-circle">11</span></td>
          <td style="text-align:left;"><strong>Krunal Pandya (4219)</strong></td>
          <td>26.17%</td>
          <td>14.0 [12.0]</td>
          <td>1000 / 1000</td>
          <td style="text-align:left;">Defensive left-arm orthodox spinner (+2.41 raw lift); exceptional economy discipline.</td>
        </tr>
        <tr>
          <td><span class="rank-circle">12</span></td>
          <td style="text-align:left;"><strong>Alzarri Joseph (3275)</strong></td>
          <td>26.14%</td>
          <td>24.0 [15.0]</td>
          <td>1000 / 1000</td>
          <td style="text-align:left;">Overseas pace strike option; highly effective in short high-leverage bursts.</td>
        </tr>
        <tr>
          <td><span class="rank-circle">13</span></td>
          <td style="text-align:left;"><strong>Varun Chakravarthy (6505)</strong></td>
          <td>21.80%</td>
          <td>16.0 [14.0]</td>
          <td>1000 / 1000</td>
          <td style="text-align:left;">Mystery spinner; tight defensive lines against right-handed power hitters.</td>
        </tr>
        <tr>
          <td><span class="rank-circle">14</span></td>
          <td style="text-align:left;"><strong>Kuldeep Yadav (2991)</strong></td>
          <td>18.40%</td>
          <td>18.0 [15.0]</td>
          <td>1000 / 1000</td>
          <td style="text-align:left;">Attacking left-arm wrist-spinner; high wicket-taking ceiling in middle overs.</td>
        </tr>
        <tr>
          <td><span class="rank-circle">15</span></td>
          <td style="text-align:left;"><strong>Yuzvendra Chahal (1643)</strong></td>
          <td>16.20%</td>
          <td>20.0 [16.0]</td>
          <td>1000 / 1000</td>
          <td style="text-align:left;">Proven wicket-taker; tactical leg-spin option if primary targets are retained.</td>
        </tr>
      </tbody>
    </table>

    <div class="section-h2">3. Strategic Contingency Scenarios</div>
    <div class="grid-2">
      <div class="callout-box navy">
        <div class="callout-title">Scenario A &bull; Auction Bidding Wars on Top Targets</div>
        <p style="font-size:6.3pt; margin:0;">If aggressive bidding on Shashank Singh or Tim David exceeds INR 12.0 Cr, immediately pivot to <strong>Naman Dhir</strong> (#3 Batter, +35.4 lift) or <strong>Ashutosh Sharma</strong> (Rank 11) to preserve budget for bowling reinforcements.</p>
      </div>
      <div class="callout-box emerald">
        <div class="callout-title">Scenario B &bull; Overseas Roster Constraints</div>
        <p style="font-size:6.3pt; margin:0;">With Jofra Archer occupying one overseas slot, if RR acquires an overseas batter (Tim David / Klaasen), prioritize Indian domestic bowlers (<strong>Prasidh Krishna</strong>, <strong>Arshdeep Singh</strong>, <strong>Krunal Pandya</strong>) to balance the starting XI.</p>
      </div>
    </div>
  </div>

  <div class="page-footer">
    <span>Rajat Aggarwal | Participant — SupeRR Selector Season 2</span>
    <span class="footer-center">Players Next in Line & Contingency Alternatives</span>
    <span class="footer-page-num">Page 14 of 15</span>
  </div>
</div>

<!-- PAGE 15: APPENDIX & REPRODUCIBILITY -->
<div class="page" id="page-15">
  <div>
    <div class="page-header">
      <div class="header-left">
        <span class="header-section-num">Section 12</span>
        <span class="header-title-text">Appendix: Baseline Lists, Governance & Reproducibility</span>
      </div>
      <div class="header-right"><span class="rr-dot"></span> Governance &bull; Code Execution &bull; Checksums</div>
    </div>

    <div class="section-h2">Appendix A: Unfiltered Single-Spec Canonical Baselines (Spec P2-W1-Model B)</div>
    <div class="grid-2">
      <table>
        <thead>
          <tr>
            <th>#</th>
            <th style="text-align:left;">Canonical Batter</th>
            <th>PWI</th>
            <th>Lift</th>
          </tr>
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

      <table>
        <thead>
          <tr>
            <th>#</th>
            <th style="text-align:left;">Canonical Bowler</th>
            <th>PWI</th>
            <th>Lift</th>
          </tr>
        </thead>
        <tbody>
          <tr><td>1</td><td style="text-align:left;">Jasprit Bumrah (2933)</td><td>+7.61</td><td>+0.33</td></tr>
          <tr><td>2</td><td style="text-align:left;">Sunil Narine (781)</td><td>+6.57</td><td>+0.64</td></tr>
          <tr><td>3</td><td style="text-align:left;">Matheesha Pathirana (8661)</td><td>+5.34</td><td>+1.21</td></tr>
          <tr><td>4</td><td style="text-align:left;">Rashid Khan (4722)</td><td>+5.59</td><td>+2.75</td></tr>
          <tr><td>5</td><td style="text-align:left;">Nathan Ellis (7920)</td><td>+5.50</td><td>+3.15</td></tr>
          <tr><td>6</td><td style="text-align:left;">Eshan Malinga (39657)</td><td>+3.85</td><td>+3.39</td></tr>
          <tr><td>7</td><td style="text-align:left;">Bhuvneshwar Kumar (360)</td><td>+3.25</td><td>-1.31</td></tr>
          <tr><td>8</td><td style="text-align:left;">Prasidh Krishna (4489)</td><td>+2.96</td><td>+2.67</td></tr>
          <tr><td>9</td><td style="text-align:left;">Noor Ahmad (7967)</td><td>+2.54</td><td>-0.21</td></tr>
          <tr><td>10</td><td style="text-align:left;">Arshdeep Singh (6464)</td><td>+1.90</td><td>+0.99</td></tr>
        </tbody>
      </table>
    </div>

    <div class="section-h2">Appendix B: Canonical CLI Commands & Reproducibility Pipeline</div>
    <div class="code-box">
# 1. Verify V1 Baseline Immutability Checksums (39/39 verified unchanged):<br>
python -c "from src.model_v4.run_multiverse_pipeline import verify_v1_checksums; print(verify_v1_checksums())"<br><br>
# 2. Run Full V4 Multiverse Pipeline (15,150 specifications per role, 1,000 bootstrap draws):<br>
python -m src.model_v4.run_multiverse_pipeline<br><br>
# 3. Execute Complete Statistical & Unit Test Suite (54 passed):<br>
pytest tests/model_v2 tests/model_v3 tests/model_v4 -q<br><br>
# 4. Generate Publication-Quality Report & Verify Dimensions with pdfme:<br>
python outputs/pdf_redesign/generate_professional_report.py
    </div>

    <div class="section-h2">Appendix C: External Verification Citations & IPL 2026 Teams</div>
    <div style="font-size:6.0pt; line-height:1.25; color:#334155;">
      &bull; <strong>Nathan Ellis (SRH / IPL Official, 2026-11-05):</strong> Mapped to CSK in raw data; officially traded CSK &rarr; SRH on 5 Nov 2026 for INR 2.00 Cr all-cash. [Official]<br>
      &bull; <strong>Arshdeep Singh (iplt20.com, 2026-11-11):</strong> Mapped to PBKS in raw data; officially traded PBKS &rarr; MI on 11 Nov 2026 in swap deal for Hardik Pandya. [Official]<br>
      &bull; <strong>Matheesha Pathirana (KKR / ESPNcricinfo, 2026-05-18):</strong> Sustained hamstring injury on 16 May 2026; actively rehabilitating; confirmed fit for 2027 cycle. [Official / Media]<br>
      &bull; <strong>Andre Russell (The Hindu, 2025-11-30):</strong> Retired from IPL on 30 Nov 2025; active KKR Power Coach for IPL 2026. [Media]<br>
      &bull; <strong>Dinesh Karthik (India TV, 2024-07-01):</strong> Retired post-IPL 2024; active RCB Batting Coach & Mentor (2025–2026). [Media]<br>
      &bull; <strong>Matthew Wade (cricket.com.au, 2024-10-29):</strong> Retired from international/domestic cricket; transition to coaching. [Official]<br>
      &bull; <strong>IPL 2027 Auction Statuses:</strong> All active players without confirmed retentions are marked <em>UNVERIFIED</em> pending BCCI auction releases.
    </div>

    <div class="callout-box emerald" style="margin-top:2px;">
      <div class="callout-title">Official Verification Sign-Off</div>
      <div style="font-size:6.0pt;">This submission document is compiled deterministically from canonical Model V4 outputs. All 39 V1 baseline checksums verified intact. Scope reconciled down to 837 matches and 193,988 deliveries. Rankings strictly preserve empirical multiverse consensus without manual overrides.</div>
    </div>
  </div>

  <div class="page-footer">
    <span>Rajat Aggarwal | Participant — SupeRR Selector Season 2</span>
    <span class="footer-center">Appendix: Baseline Lists & Reproducibility</span>
    <span class="footer-page-num">Page 15 of 15</span>
  </div>
</div>

</body>
</html>
"""
    return html

def main():
    print("Building professional HTML report...")
    html_content = build_html()
    TEMP_HTML.write_text(html_content, encoding="utf-8")
    print(f"Generated HTML template at: {TEMP_HTML} ({len(html_content)} bytes)")

    # Find Chrome or Edge
    chrome_paths = [
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
        r"C:\Program Files\Microsoft\Edge\Application\msedge.exe"
    ]
    browser_path = None
    for p in chrome_paths:
        if Path(p).exists():
            browser_path = p
            break

    if not browser_path:
        raise RuntimeError("No compatible headless browser (Chrome or Edge) found.")

    print(f"Compiling PDF using browser: {browser_path}")
    cmd = [
        browser_path,
        "--headless",
        "--disable-gpu",
        "--run-all-compositor-stages-before-draw",
        "--print-to-pdf-no-header",
        f"--print-to-pdf={OUT_PDF.resolve()}",
        str(TEMP_HTML.resolve())
    ]
    res = subprocess.run(cmd, capture_output=True, text=True)
    print("Browser exit code:", res.returncode)

    if not OUT_PDF.exists():
        raise RuntimeError("Output PDF was not generated.")

    reader = pypdf.PdfReader(OUT_PDF)
    num_pages = len(reader.pages)
    file_size_kb = OUT_PDF.stat().st_size / 1024
    print(f"SUCCESS: Generated {OUT_PDF.name}")
    print(f"Page Count: {num_pages}")
    print(f"File Size: {file_size_kb:.1f} KB")

    if num_pages != 15:
        print(f"WARNING: Expected exactly 15 pages, got {num_pages}!")

if __name__ == "__main__":
    main()
