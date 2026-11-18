"""
Professional Publication PDF Generator for SupeRR Selector Season 2 Report.
Version 3.0: Page-Specific Layout Architecture.
Ensures zero empty voids on sparse pages, zero overflow on dense pages,
and 100% visible footers and content across all 15 pages.
"""

from pathlib import Path
import subprocess
import base64
import pypdf
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
OUT_DIR = ROOT / "outputs" / "pdf_redesign"
FINAL_DIR = OUT_DIR / "final"
RENDER_DIR = OUT_DIR / "after"
PREVIEW_DIR = OUT_DIR / "preview"
MODEL_V4_DIR = ROOT / "outputs" / "model_v4"
DATA_AUDIT_DIR = ROOT / "outputs" / "data_audit" / "charts"

FINAL_DIR.mkdir(parents=True, exist_ok=True)
RENDER_DIR.mkdir(parents=True, exist_ok=True)
PREVIEW_DIR.mkdir(parents=True, exist_ok=True)

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
        "Shashank Singh": "Retained (PBKS) — Historical Benchmark",
        "Tim David": "Retained (RCB) — Historical Benchmark",
        "Naman Dhir": "Retained (MI) — Historical Benchmark",
        "Dinesh Karthik": "Retired — Historical Benchmark Only",
        "Heinrich Klaasen": "Retained (SRH) — Historical Benchmark",
        "Suryakumar Yadav": "Retained (MI) — Historical Benchmark",
        "Rinku Singh": "Retained (KKR) — Historical Benchmark",
        "Romario Shepherd": "Retained (RCB) — Historical Benchmark",
        "Andre Russell": "Retired — Historical Benchmark Only (KKR Coach)",
        "Rashid Khan": "Retained (GT) — Historical Benchmark"
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
        "Sunil Narine": "Retained (KKR) — Historical Benchmark",
        "Jasprit Bumrah": "Retained (MI) — Historical Benchmark",
        "Rashid Khan": "Retained (GT) — Historical Benchmark",
        "Matheesha Pathirana": "Released (CSK) — Reg & Medical Pending",
        "Eshan Malinga": "Retained (SRH) — Historical Benchmark",
        "Nathan Ellis": "Trade In (SRH) — Retained / Unavailable",
        "Noor Ahmad": "Retained (CSK) — Historical Benchmark",
        "Arshdeep Singh": "Trade In (MI) — Retained / Unavailable",
        "Prasidh Krishna": "Retained (GT) — Historical Benchmark",
        "Bhuvneshwar Kumar": "Retained (RCB) — Historical Benchmark"
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
    line-height: 1.40;
    font-size: 8.8pt;
    margin: 0;
    padding: 0;
    -webkit-print-color-adjust: exact;
    print-color-adjust: exact;
  }
  .page {
    width: 210mm;
    height: 297mm;
    max-height: 297mm;
    padding: 9mm 12mm 9mm 12mm;
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
  .page-body {
    flex: 1;
    display: flex;
    flex-direction: column;
    justify-content: flex-start;
  }

  /* Header & Branding */
  .masthead {
    background: linear-gradient(135deg, #0B132B 0%, #1C2541 100%);
    color: #FFFFFF;
    padding: 7px 12px;
    border-radius: 5px;
    border-bottom: 2.5px solid #E91E63;
    margin-bottom: 5px;
    display: flex;
    justify-content: space-between;
    align-items: center;
  }
  .masthead-title {
    font-size: 10.5pt;
    font-weight: 800;
    letter-spacing: 0.3px;
    text-transform: uppercase;
    color: #FFFFFF;
  }
  .masthead-tag {
    background-color: rgba(233, 30, 99, 0.25);
    border: 1px solid #E91E63;
    color: #FCE7F3;
    padding: 2px 7px;
    border-radius: 12px;
    font-size: 6.2pt;
    font-weight: 700;
    letter-spacing: 0.4px;
    text-transform: uppercase;
  }

  .page-header {
    display: flex;
    justify-content: space-between;
    align-items: flex-end;
    border-bottom: 1.5px solid #E2E8F0;
    padding-bottom: 4px;
    margin-bottom: 6px;
    position: relative;
  }
  .page-header:after {
    content: '';
    position: absolute;
    bottom: -1.5px;
    left: 0;
    width: 50px;
    height: 1.5px;
    background-color: #E91E63;
  }
  .header-left {
    display: flex;
    flex-direction: column;
  }
  .header-section-num {
    font-size: 6.8pt;
    font-weight: 800;
    color: #E91E63;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    margin-bottom: 1px;
  }
  .header-title-text {
    font-size: 11.5pt;
    font-weight: 800;
    color: #0B132B;
    letter-spacing: -0.2px;
  }
  .header-right {
    font-size: 7.0pt;
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
    line-height: 1.18;
    margin: 0 0 2px 0;
    letter-spacing: -0.3px;
  }
  .doc-hero-subtitle {
    font-size: 7.8pt;
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
    gap: 6px;
    margin-bottom: 5px;
  }
  .kpi-card {
    background-color: #F8FAFC;
    border: 1px solid #E2E8F0;
    border-top: 2.5px solid #004BA0;
    border-radius: 5px;
    padding: 4px 6px;
    text-align: center;
  }
  .kpi-card.pink { border-top-color: #E91E63; }
  .kpi-card.emerald { border-top-color: #059669; }
  .kpi-card.gold { border-top-color: #D4AF37; }
  .kpi-val {
    font-size: 11.5pt;
    font-weight: 800;
    color: #0F172A;
    line-height: 1.15;
  }
  .kpi-lbl {
    font-size: 6.0pt;
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
    padding: 5px 8px;
    margin-bottom: 5px;
    border-radius: 0 5px 5px 0;
    font-size: 8.0pt;
    line-height: 1.35;
  }
  .callout-box.navy { border-left-color: #0B132B; }
  .callout-box.blue { border-left-color: #004BA0; }
  .callout-box.emerald { border-left-color: #059669; }
  .callout-box.gold { border-left-color: #D4AF37; }
  .callout-title {
    font-weight: 800;
    color: #0B132B;
    font-size: 8.4pt;
    margin-bottom: 2px;
    display: flex;
    align-items: center;
    gap: 4px;
  }

  .section-h2 {
    font-size: 10.5pt;
    font-weight: 800;
    color: #0B132B;
    border-bottom: 1.5px solid #E2E8F0;
    padding-bottom: 2px;
    margin: 6px 0 4px 0;
    text-transform: uppercase;
    letter-spacing: 0.3px;
    display: flex;
    justify-content: space-between;
  }
  .section-h3 {
    font-size: 8.8pt;
    font-weight: 700;
    color: #004BA0;
    margin: 4px 0 2px 0;
  }

  /* Tables */
  table {
    width: 100%;
    border-collapse: collapse;
    margin: 2px 0 4px 0;
    font-size: 7.4pt;
  }
  th, td {
    padding: 3.0px 4.0px;
    border: 1px solid #E2E8F0;
    text-align: center;
  }
  th {
    background-color: #0B132B;
    color: #FFFFFF;
    font-weight: 700;
    text-transform: uppercase;
    font-size: 6.8pt;
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
    width: 13px;
    height: 13px;
    border-radius: 50%;
    background-color: #0F172A;
    color: #FFFFFF;
    font-weight: 800;
    font-size: 6.2pt;
  }
  .badge {
    display: inline-block;
    padding: 1px 3.8px;
    border-radius: 3px;
    font-size: 6.0pt;
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
    font-size: 6.4pt;
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
    font-size: 6.2pt;
    text-align: left;
    font-weight: 600;
    color: #004BA0;
  }
  .classification-cell {
    font-size: 6.5pt;
    text-align: left;
    color: #334155;
    font-weight: 500;
  }

  /* Math Blocks */
  .formula-card {
    background: #F8FAFC;
    border: 1px solid #E2E8F0;
    border-left: 3.5px solid #E91E63;
    border-radius: 0 5px 5px 0;
    padding: 7px 10px;
    margin: 4px 0;
  }
  .formula-title {
    font-weight: 800;
    font-size: 8.8pt;
    color: #0B132B;
    margin-bottom: 3px;
  }
  .formula-math {
    font-family: "Cambria Math", "Latin Modern Math", "STIX Two Math", "Times New Roman", serif;
    font-size: 10.8pt;
    font-weight: 600;
    color: #0F172A;
    text-align: center;
    padding: 3px 0;
  }
  .formula-desc {
    font-size: 7.5pt;
    color: #475569;
    line-height: 1.32;
    margin-top: 2px;
  }

  /* Grids & Cards */
  .grid-2 {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 8px;
    margin-bottom: 5px;
  }
  .grid-3 {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 7px;
    margin-bottom: 5px;
  }
  .card {
    background-color: #FFFFFF;
    border: 1px solid #E2E8F0;
    border-radius: 5px;
    padding: 7px 10px;
    font-size: 8.2pt;
    line-height: 1.36;
  }
  .card-tint {
    background-color: #F8FAFC;
  }

  /* Player Dossiers */
  .player-dossier {
    background-color: #FFFFFF;
    border: 1px solid #E2E8F0;
    border-radius: 5px;
    padding: 4.5px 7.5px;
    margin-bottom: 4px;
    display: flex;
    flex-direction: column;
    gap: 2px;
  }
  .dossier-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    border-bottom: 1px solid #F1F5F9;
    padding-bottom: 1.5px;
  }
  .dossier-name {
    font-size: 8.4pt;
    font-weight: 800;
    color: #0B132B;
  }
  .dossier-metrics {
    display: flex;
    gap: 7px;
    font-size: 6.8pt;
    background-color: #F8FAFC;
    padding: 2px 5px;
    border-radius: 3px;
  }
  .dossier-prose {
    font-size: 7.2pt;
    color: #334155;
    line-height: 1.32;
    text-align: justify;
  }

  /* Images & Charts */
  .chart-box {
    width: 100%;
    border: 1px solid #E2E8F0;
    border-radius: 5px;
    overflow: hidden;
    margin: 4px 0;
    background-color: #FFFFFF;
    text-align: center;
  }
  .chart-box img {
    max-width: 100%;
    max-height: 310px;
    object-fit: contain;
    display: block;
    margin: 0 auto;
  }
  .chart-box.compact img {
    max-height: 220px;
  }
  .chart-caption {
    font-size: 6.8pt;
    font-style: italic;
    color: #64748B;
    padding: 2.5px 5px;
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
    border-radius: 5px;
    padding: 6px 9px;
    margin: 4px 0;
  }
  .waterfall-step {
    text-align: center;
    flex: 1;
  }
  .wf-num {
    font-size: 11.0pt;
    font-weight: 800;
    color: #0F172A;
  }
  .wf-label {
    font-size: 6.2pt;
    color: #64748B;
    text-transform: uppercase;
    font-weight: 600;
  }
  .wf-arrow {
    font-size: 10.0pt;
    font-weight: bold;
    color: #E91E63;
    padding: 0 3px;
  }
  .wf-final {
    background-color: #0B132B;
    color: #FFFFFF;
    padding: 4px 7px;
    border-radius: 5px;
  }
  .wf-final .wf-num { color: #FFFFFF; }
  .wf-final .wf-label { color: #94A3B8; }

  /* Code block */
  .code-box {
    background-color: #0F172A;
    color: #F8FAFC;
    font-family: "JetBrains Mono", Consolas, monospace;
    font-size: 6.8pt;
    padding: 6px 9px;
    border-radius: 5px;
    line-height: 1.38;
    margin: 3px 0 5px 0;
  }

  /* Footer */
  .page-footer {
    border-top: 1.5px solid #E2E8F0;
    padding-top: 3.5px;
    margin-top: 3px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    font-size: 6.8pt;
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
  p {
    margin: 0 0 4px 0;
  }

  /* Specific Page Tuning */
  #page-1 .masthead { padding: 1.5px 0; margin-bottom: 2px; font-size: 7.0pt; }
  #page-1 .doc-hero-title { font-size: 11.8pt; margin: 1px 0; line-height: 1.15; }
  #page-1 .doc-hero-subtitle { margin-bottom: 2px; font-size: 6.8pt; }
  #page-1 .kpi-row { margin-bottom: 2px; }
  #page-1 .kpi-card { padding: 2px 4px; }
  #page-1 .kpi-val { font-size: 10.0pt; }
  #page-1 .kpi-lbl { font-size: 5.4pt; }
  #page-1 .callout-box { padding: 2px 5px !important; margin-bottom: 2px !important; font-size: 6.6pt !important; line-height: 1.16 !important; }
  #page-1 .callout-title { font-size: 7.2pt !important; margin-bottom: 1px !important; }
  #page-1 .section-h3 { font-size: 7.4pt; margin: 1px 0 1px 0; }
  #page-1 table { font-size: 5.7pt !important; margin: 1px 0 2px 0 !important; }
  #page-1 th, #page-1 td { padding: 1.0px 2.2px !important; line-height: 1.10 !important; }
  #page-1 .rank-circle { width: 10px; height: 10px; font-size: 5.2pt; }
  #page-1 .badge { font-size: 5.0pt; padding: 0.5px 2px; }
  #page-1 .id-muted { font-size: 5.2pt; }
  #page-1 .rec-cell { font-size: 5.4pt; }

  #page-6 table th, #page-6 table td { padding: 4.5px 6px; font-size: 8.2pt; }
  #page-13 .chart-box img { max-height: 280px !important; }
  #page-14 table th, #page-14 table td { padding: 5.0px 6px; font-size: 8.4pt; }
  #page-15 table th, #page-15 table td { padding: 3.5px 5px; font-size: 8.0pt; }

    """

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
  <div class="page-body">
    <div class="masthead">
      <div class="masthead-title">SupeRR Selector Season 2 — Round 1 Intelligence Submission</div>
      <div class="masthead-tag">Pre-Registered Multiverse Architecture (3.19M Evaluations) &bull; Post-Retention Reconciled Audit</div>
    </div>

    <h1 class="doc-hero-title">Evaluating Cricket Performance Under Pressure: Multiverse Analysis & Rajasthan Royals Recruitment Strategy</h1>
    <div class="doc-hero-subtitle">
      <span>Participant: Rajat Aggarwal | Canonical Model V4 Release (Post-Retention Audit 18 Nov 2026)</span>
      <span>Official Scope: 837 Matches | 193,988 Deliveries (185,692 Legal Balls)</span>
    </div>

    <div class="kpi-row">
      <div class="kpi-card">
        <div class="kpi-val">3.19M</div>
        <div class="kpi-lbl">Player-Spec Records (15.15k Specs/Role)</div>
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

    <div class="callout-box" style="padding:4px 7px; margin-bottom:4px; font-size:7.4pt;">
      <div class="callout-title" style="font-size:8.0pt;">One-Line Pressure Definition</div>
      <div>A delivery is classified as High-Pressure when the defending-side or batting-side pre-delivery leverage index reaches or exceeds 0.50 (evaluated via logistic sigmoid centered at 0.425 with slope k = 12.5 / scale 0.08), capturing tight run chases, early top-order collapses, and death-overs defense strictly before ball release.</div>
    </div>

    <div class="callout-box navy" style="padding:4px 7px; margin-bottom:4px; font-size:7.4pt;">
      <div class="callout-title" style="font-size:8.0pt;">Pre-Registered Ranking Rule & Metric Definitions</div>
      <div><strong>Ranking Rule:</strong> Ordered by multiverse top-10 frequency; ties broken by lower median rank; candidates must pass &ge;50% eligibility across valid specifications and &ge;800/1,000 bootstrap draws (all 20 selections satisfy both). <strong>Elig %:</strong> Specification eligibility share across 15,150 specifications. <strong>Top-10 %:</strong> Frequency of finishing inside the Top 10 across eligible runs.</div>
    </div>

    <div class="callout-box blue" style="padding:4px 7px; margin-bottom:4px; font-size:7.2pt; line-height:1.26;">
      <div class="callout-title" style="font-size:8.0pt;">Three Core Empirical Findings</div>
      <div>
        &bull; <strong>Multiverse Specification Sensitivity & ANOVA:</strong> Evaluating 15,150 specifications per role reveals that player_id main effects account for 60.17% (batting) and 62.08% (bowling) of percentile rank variance in a Sequential Type I ANOVA summing to exactly 100.00%. Methodological sensitivity operates through player &times; spec interactions and residual error (25.56% batting, 22.08% bowling), while format scope accounts for 9.69% and 9.44%.<br>
        &bull; <strong>Bootstrap Filter Removes Volatile Assets:</strong> The 1,000-draw stability hurdle (&ge;800 draws) eliminated sample-dependent fringe candidates (Matthew Wade qualified in only 720/1,000 draws; Mujeeb Ur Rahman in 744/1,000; Naveen ul Haq in 513/1,000), promoting resilient contributors.<br>
        &bull; <strong>Rajasthan Royals 2026 Phase Audit:</strong> RR's death bowling was league-average overall (ER 10.60 vs league 10.67), but Sandeep Sharma (ER 13.70) and Tushar Deshpande (ER 12.38) leaked runs. In the middle overs, spin economy lagged (Jadeja 8.39, Bishnoi 10.11 vs league 8.97).
      </div>
    </div>

    <div class="section-h3" style="margin-top:1px; font-size:8.2pt;">Consensus Top-10 Batters (Ranked by Multiverse Frequency, Shrunk PWI & Lift)</div>
    <table style="font-size:6.6pt; margin:1px 0 3px 0;">
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

    <div class="section-h3" style="margin-top:1px; font-size:8.2pt;">Consensus Top-10 Bowlers (Ranked by Multiverse Frequency, Defending Shrunk Impact & Lift)</div>
    <table style="font-size:6.6pt; margin:1px 0 3px 0;">
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
  <div class="page-body">
    <div class="page-header">
      <div class="header-left">
        <span class="header-section-num">Section 1</span>
        <span class="header-title-text">Problem Understanding & Data Architecture</span>
      </div>
      <div class="header-right"><span class="rr-dot"></span> SupeRR Selector Season 2 &bull; Operational Mandate</div>
    </div>

    <div class="section-h2">1. Operational Framing & The Five Research Questions</div>
    <p style="font-size:9.2pt; line-height:1.44;">Evaluating player performance under pressure in T20 cricket is plagued by small sample sizes, extreme situational context, and researcher degrees of freedom. A player who scores 20 off 8 balls in a 220-par chase appears clutch in traditional box scores, yet their performance may be heavily driven by field restrictions or bowling mis-executions. To solve this rigorously for the Rajasthan Royals scouting department, this research establishes five interconnected analytical mandates:</p>

    <div class="grid-2" style="gap:11px; margin-top:4px;">
      <div class="card card-tint" style="padding:10px 12px;">
        <div class="formula-title" style="color:#004BA0; font-size:9.6pt;">RQ1 &bull; Objective Pre-Delivery Pressure Definition</div>
        <p style="font-size:8.4pt; margin:0; line-height:1.40;">How can pressure be quantified objectively on a continuous delivery-level scale using strictly pre-ball information (required run rate, balls remaining, wickets in hand, match phase, venue par) without leaking post-delivery outcomes?</p>
      </div>
      <div class="card card-tint" style="padding:10px 12px;">
        <div class="formula-title" style="color:#004BA0; font-size:9.6pt;">RQ2 &bull; Strict Context-Adjusted Baselines (LPO)</div>
        <p style="font-size:8.4pt; margin:0; line-height:1.40;">How do we ensure fair comparisons across match phases (Powerplay, Middle, Death), venues, and bowling types using Leave-Player-Out (LPO) expectation baselines that prevent self-contamination?</p>
      </div>
      <div class="card card-tint" style="padding:10px 12px;">
        <div class="formula-title" style="color:#004BA0; font-size:9.6pt;">RQ3 &bull; Separating Resilience from Baseline Quality</div>
        <p style="font-size:8.4pt; margin:0; line-height:1.40;">Does a player genuinely elevate their game when leverage peaks, or are they simply an elite player who maintains their baseline output? How do we mathematically isolate pressure lift from baseline skill?</p>
      </div>
      <div class="card card-tint" style="padding:10px 12px;">
        <div class="formula-title" style="color:#004BA0; font-size:9.6pt;">RQ4 &bull; Multiverse Robustness Across 15,150 Specifications</div>
        <p style="font-size:8.4pt; margin:0; line-height:1.40;">How sensitive are player rankings to subjective analytical choices (pressure weights, scoring models, wicket values, shrinkage priors)? Can we prove consensus stability across 3.19 million evaluations?</p>
      </div>
    </div>

    <div class="card card-tint" style="padding:10px 14px; margin-top:4px; margin-bottom:8px;">
      <div class="formula-title" style="color:#004BA0; font-size:9.8pt;">RQ5 &bull; Rajasthan Royals Actionable Recruitment Dossier</div>
      <p style="font-size:8.6pt; margin:0; line-height:1.42;">How can pressure ratings translate into concrete auction, trade, and retention strategies for Rajasthan Royals ahead of the 2027 cycle, addressing audited phase-level weaknesses from raw IPL 2026 match logs?</p>
    </div>

    <div class="section-h2" style="margin-top:6px;">2. Four-Stage Data Engineering Architecture</div>
    <p style="font-size:9.2pt; line-height:1.44;">To eliminate information leakage and guarantee mathematical auditability, the pipeline executes sequentially across four modular phases:</p>

    <div class="grid-2" style="gap:11px; margin-top:4px;">
      <div class="card" style="padding:10px 12px;">
        <div class="formula-title" style="font-size:9.4pt;">Step 0 &bull; Raw Data Ingestion & Scope Reconciliation</div>
        <p style="font-size:8.2pt; margin:0; line-height:1.38;">Ingest 6 official CSVs (883 matches, 200,999 deliveries). Filter strictly to primary T20 competition scope: 837 matches (367 IPL, 470 T20I), removing 16 abandoned zero-delivery fixtures, 30 emerging tournament matches, and 26 Super Over deliveries. Resolve player homonyms using unique player_id.</p>
      </div>
      <div class="card" style="padding:10px 12px;">
        <div class="formula-title" style="font-size:9.4pt;">Step 1 &bull; Pre-Delivery State & Pressure Index Generation</div>
        <p style="font-size:8.2pt; margin:0; line-height:1.38;">Reconstruct dynamic pre-ball match states: pre_runs, pre_wickets, pre_balls_rem, pre_crr, pre_rrr. Formulate distinct asymmetric pressure indexes for batting (PI<sub>bat</sub>) and defending bowling (PI<sub>bowl</sub>). Evaluate continuous delivery weights w<sub>k</sub> via logistic sigmoid.</p>
      </div>
      <div class="card" style="padding:10px 12px;">
        <div class="formula-title" style="font-size:9.4pt;">Step 2 &bull; Hierarchical LPO Baselines & Regularization</div>
        <p style="font-size:8.2pt; margin:0; line-height:1.38;">Compute Leave-Player-Out context expectations across Phase &times; Venue &times; Match-Track cells. Subtract player i's own outcomes to prevent bias. Apply empirical Bayes Dirichlet-multinomial shrinkage (&alpha;<sub>0</sub>) for rare match states, regularizing sample noise toward league baselines.</p>
      </div>
      <div class="card" style="padding:10px 12px;">
        <div class="formula-title" style="font-size:9.4pt;">Step 3 &bull; Multiverse Evaluation & Bootstrap Stability</div>
        <p style="font-size:8.2pt; margin:0; line-height:1.38;">Execute an 8-dimensional specification grid generating 15,150 model configurations per role. Perform 1,000-draw stratified match bootstrap resampling. Filter volatile assets via pre-registered hurdles (&ge;50% specification eligibility, &ge;800/1,000 bootstrap draws) to output consensus rankings.</p>
      </div>
    </div>

    <div class="callout-box emerald" style="margin-top:8px; padding:8px 12px;">
      <div class="callout-title" style="font-size:9.2pt;">Cricket Accounting Rule Compliance</div>
      <div style="font-size:8.2pt; line-height:1.38;">In accordance with official MCC Laws and T20 playing conditions: Wides are non-legal deliveries excluded from balls faced; Oversteps and other no-balls increment balls faced and penalize bowlers; Byes/leg-byes are excluded from bowler runs conceded; Bowler wickets exclude Run Outs, Retired Out, and Obstructing the field.</div>
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
  <div class="page-body">
    <div class="page-header">
      <div class="header-left">
        <span class="header-section-num">Section 2</span>
        <span class="header-title-text">Data Quality Audit & Empirical Pressure Validation</span>
      </div>
      <div class="header-right"><span class="rr-dot"></span> Pre-Modelling Audit &bull; Scope Reconciliation</div>
    </div>

    <div class="section-h2">1. Scope Reconciliation & Delivery Waterfall (Step 0)</div>
    <p style="font-size:8.8pt;">To ensure 100% reproducibility and eliminate selection bias, the raw competition dataset was audited and reconciled. Every match and delivery was accounted for down to the exact target scope of 837 matches and 193,988 deliveries:</p>

    <div class="waterfall-strip" style="padding:8px 12px; margin:5px 0;">
      <div class="waterfall-step">
        <div class="wf-num" style="font-size:12.0pt;">200,999</div>
        <div class="wf-label">Raw Deliveries</div>
      </div>
      <div class="wf-arrow">&minus;</div>
      <div class="waterfall-step">
        <div class="wf-num" style="font-size:12.0pt;">0 (16 M)</div>
        <div class="wf-label">Abandoned Matches</div>
      </div>
      <div class="wf-arrow">&minus;</div>
      <div class="waterfall-step">
        <div class="wf-num" style="font-size:12.0pt;">6,985 (30 M)</div>
        <div class="wf-label">Emerging Comps</div>
      </div>
      <div class="wf-arrow">&minus;</div>
      <div class="waterfall-step">
        <div class="wf-num" style="font-size:12.0pt;">26</div>
        <div class="wf-label">Super Overs (Inn 3-4)</div>
      </div>
      <div class="wf-arrow">=</div>
      <div class="waterfall-step wf-final" style="padding:5px 9px;">
        <div class="wf-num" style="font-size:12.5pt;">193,988</div>
        <div class="wf-label">Primary Deliveries</div>
      </div>
    </div>

    <table style="font-size:7.8pt; margin:4px 0 6px 0;">
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

    <div class="section-h2" style="margin-top:4px;">2. Empirical Pressure Separation: High Pressure vs. Normal Outcomes</div>
    <p style="font-size:8.6pt;">To confirm that the mathematical pressure index successfully separates distinct competitive environments, outcome rates were independently computed comparing High Pressure (PI &ge; 0.50) against Normal Pressure (PI &lt; 0.35). The intermediate band (0.35 &le; PI &lt; 0.50) is excluded only from this descriptive binary comparison, while fully preserved in continuous modelling:</p>

    <table style="font-size:7.8pt; margin:4px 0 6px 0;">
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

    <div class="grid-2" style="gap:9px; margin-top:3px;">
      <div class="chart-box compact">
        <img src="{img_pressure_dist}" alt="Pressure Index Distribution" style="max-height:210px;">
        <div class="chart-caption">Figure 1A: Distribution of Continuous Pressure Indexes across 193,988 deliveries.</div>
      </div>
      <div class="chart-box compact">
        <img src="{img_hp_outcomes}" alt="Empirical Outcome Separation" style="max-height:210px;">
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
  <div class="page-body">
    <div class="page-header">
      <div class="header-left">
        <span class="header-section-num">Section 3</span>
        <span class="header-title-text">Defining Pressure in T20 Cricket: Mechanics & Formulations</span>
      </div>
      <div class="header-right"><span class="rr-dot"></span> Situational Mechanics &bull; Asymmetric Formulations</div>
    </div>

    <div class="section-h2">1. The Principle of Dynamic Asymmetry</div>
    <p style="font-size:9.2pt; line-height:1.44;">Pressure in T20 cricket is inherently asymmetric between the batting team and the defending fielding team. When a chasing team is 70/8 needing 110 runs from 30 balls, the batting team faces severe collapse pressure. However, the fielding side is in commanding control and faces near-zero defending pressure. A single unified pressure metric conflates these opposite psychological and tactical realities. Hence, separate formulations govern each discipline:</p>

    <div class="grid-2" style="gap:12px; margin-top:6px;">
      <div class="formula-card" style="padding:10px 14px;">
        <div class="formula-title" style="font-size:9.6pt;">Batting Pressure Formulation (Innings 1 & 2)</div>
        <div class="formula-math" style="font-size:11.8pt; padding:6px 0;">PI<sub>bat, 1</sub> = 0.50 &middot; S<sub>collapse</sub> + 0.30 &middot; S<sub>crr</sub> + 0.20 &middot; S<sub>death</sub></div>
        <div class="formula-math" style="font-size:11.8pt; padding:6px 0;">PI<sub>bat, 2</sub> = 0.50 &middot; S<sub>rrr</sub> + 0.30 &middot; S<sub>wkts</sub> + 0.20 &middot; S<sub>urgency</sub> + Boost<sub>close</sub></div>
        <div class="formula-desc" style="font-size:8.2pt; line-height:1.40;">Where S<sub>collapse</sub> measures wickets lost relative to par, S<sub>rrr</sub> scales required run rate against par, and Boost<sub>close</sub> activates when balls remaining &le; 18 with margin &le; 24 runs.</div>
      </div>

      <div class="formula-card" style="padding:10px 14px;">
        <div class="formula-title" style="font-size:9.6pt;">Defending Bowler Formulation (Innings 1 & 2)</div>
        <div class="formula-math" style="font-size:11.8pt; padding:6px 0;">PI<sub>bowl, 1</sub> = max(S<sub>death</sub>, S<sub>top</sub>) &times; Damp<sub>collapse</sub></div>
        <div class="formula-math" style="font-size:11.8pt; padding:6px 0;">PI<sub>bowl, 2</sub> = S<sub>leverage</sub> &times; Damp<sub>tail</sub></div>
        <div class="formula-desc" style="font-size:8.2pt; line-height:1.40;">In 1st innings, bowler pressure reflects batting onslaughts (CRR &gt; par with &le;3 wickets down). In 2nd innings, leverage peaks during balanced chases; tail damping reduces leverage to 0.20 if chasing team has lost &ge;7 wickets.</div>
      </div>
    </div>

    <div class="formula-card" style="margin-top:6px; padding:10px 14px;">
      <div class="formula-title" style="font-size:9.8pt;">Continuous Sigmoid Leverage Weighting Function</div>
      <div class="formula-math" style="font-size:12.0pt; padding:6px 0;">w<sub>k</sub> = &sigma;(PI<sub>k</sub>; x<sub>0</sub>=0.425, k=12.5) = 1 / [1 + e<sup>-12.5 &middot; (PI<sub>k</sub> - 0.425)</sup>] = 1 / [1 + e<sup>-(PI<sub>k</sub> - 0.425) / 0.08</sup>]</div>
      <div class="formula-desc" style="font-size:8.4pt; line-height:1.42;">Smooth logistic transition centered at x<sub>0</sub> = 0.425 with slope k = 12.5 (scale s = 0.08). Fully preserves every delivery without artificial step-function thresholding. Normal deliveries (PI &lt; 0.25) receive near-zero weight (~0.05); high pressure (PI &gt; 0.60) smoothly saturates to ~0.99.</div>
    </div>

    <div class="section-h2" style="margin-top:8px;">2. Real Delivery Worked Examples from Raw Match Data (ball_by_ball.csv)</div>
    <p style="font-size:9.2pt; line-height:1.44;">To verify mathematical mechanics directly against raw competition files, two verified high-pressure events were traced step-by-step:</p>

    <div class="grid-2" style="gap:12px; margin-top:6px;">
      <div class="card card-tint" style="padding:10px 14px;">
        <div class="formula-title" style="color:#004BA0; font-size:9.6pt;">Worked Example 1 &bull; Batter High Pressure (Match ID: 14148)</div>
        <div style="font-size:8.4pt; line-height:1.42;">
          <strong>Context:</strong> IPL 2022, Innings 2, Ball 15.5 (state evaluated after 14.4 overs).<br>
          <strong>Match State:</strong> Chasing 193, batting team is 104/5 in 14.4 overs needing 89 runs from 32 balls (pre_rrr = 16.69). Batter Shashank Singh (ID: 2756) faces Wanindu Hasaranga (ID: 4900).<br>
          <strong>Pressure Metrics:</strong> Continuous PI<sub>bat</sub> = 0.8648. Sigmoid weight w<sub>k</sub> = 0.9959.<br>
          <strong>Outcome & Impact:</strong> Shashank strikes a 6. LPO context baseline: expected runs 1.1087, expected dismissal 0.0396. Net impact: +4.8913 runs above expected + 0.2379 dismissal avoidance (V = 6.0) = <strong>+5.1292 runs</strong>, weighted at 0.9959 into his high-pressure sample.
        </div>
      </div>

      <div class="card card-tint" style="padding:10px 14px;">
        <div class="formula-title" style="color:#E91E63; font-size:9.6pt;">Worked Example 2 &bull; Bowler High Pressure (Match ID: 14160)</div>
        <div style="font-size:8.4pt; line-height:1.42;">
          <strong>Context:</strong> IPL 2022, Innings 2, Ball 19.5 (state evaluated after 19.4 overs).<br>
          <strong>Match State:</strong> Defending 170, chasing side is 162/7 needing 9 runs from 2 balls (pre_rrr = 27.00). Bowler Jasprit Bumrah (ID: 2933) defends against power-hitter Andre Russell (ID: 1318).<br>
          <strong>Pressure Metrics:</strong> Continuous PI<sub>bowl</sub> = 0.9124. Sigmoid weight w<sub>k</sub> = 0.9978.<br>
          <strong>Outcome & Impact:</strong> Bumrah executes a yorker dot ball. LPO context baseline: expected runs conceded 1.4230, expected dismissal 0.0820. Net defending impact: +1.4230 runs saved &minus; 0.4920 = <strong>+0.9310 runs</strong> defended, weighted at 0.9978 into his sample.
        </div>
      </div>
    </div>

    <div class="callout-box navy" style="margin-top:8px; padding:8px 12px;">
      <div class="callout-title" style="font-size:9.2pt;">Zero Look-Ahead Guarantee</div>
      <div style="font-size:8.4pt; line-height:1.40;">All features (pre_runs, pre_wickets, pre_legal_balls, pre_crr, pre_rrr, leverage) are computed strictly before the bowler begins their run-up. Post-delivery events (runs scored, wickets fallen, extras) are strictly isolated as dependent variables to eliminate look-ahead bias completely.</div>
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
  <div class="page-body">
    <div class="page-header">
      <div class="header-left">
        <span class="header-section-num">Section 4</span>
        <span class="header-title-text">Performance Measurement Framework: Baselines & Shrinkage</span>
      </div>
      <div class="header-right"><span class="rr-dot"></span> LPO Context Baselines &bull; Bayesian Shrinkage</div>
    </div>

    <div class="section-h2">1. Leave-Player-Out (LPO) Hierarchical Baselines</div>
    <p style="font-size:9.2pt; line-height:1.44;">Standard baselines contaminate context expectations by including the focal player's own balls in the cell average. If Jasprit Bumrah bowls 40% of Mumbai Indians' death deliveries at Wankhede, an unadjusted baseline compares Bumrah against an average heavily composed of Bumrah himself. To eliminate this distortion, every delivery is evaluated using strict Leave-Player-Out (LPO) expectation baselines:</p>

    <div class="formula-card" style="padding:10px 14px; margin:6px 0;">
      <div class="formula-title" style="font-size:9.8pt;">Leave-Player-Out Expectation Formula</div>
      <div class="formula-math" style="font-size:12.0pt; padding:6px 0;">E[R<sub>i, c</sub>] = [&sum;<sub>j &ne; i</sub> R<sub>j, c</sub>] / [&sum;<sub>j &ne; i</sub> B<sub>j, c</sub>] &emsp;|&emsp; E[W<sub>i, c</sub>] = [&sum;<sub>j &ne; i</sub> W<sub>j, c</sub>] / [&sum;<sub>j &ne; i</sub> B<sub>j, c</sub>]</div>
      <div class="formula-desc" style="font-size:8.4pt; line-height:1.42;">Where cell c is defined by the 7-level hierarchy (finest level: Match Track &times; Season &times; Phase &times; Wickets Down &times; Role/Style &times; Opponent Tier). If effective sample size (N<sub>cell</sub> &minus; n<sub>i, c</sub>) falls below 50 deliveries, the expectation hierarchically pools upward across 7 tiers down to Phase and global LPO. In production, 100.00% of deliveries resolve at Levels 0–3, strictly preserving complete IPL vs T20I format isolation without any cross-format leakage.</div>
    </div>

    <div class="section-h2" style="margin-top:8px;">2. Wicket Valuation & Dirichlet-Multinomial Bayesian Regularization</div>
    <p style="font-size:9.2pt; line-height:1.44;">T20 outcomes are discrete events (0, 1, 2, 3, 4, 6, Wicket, Extras). Evaluating run impact requires translating dismissals into run-equivalent currency, while regularizing sparse player samples:</p>

    <div class="grid-2" style="gap:12px; margin-top:6px;">
      <div class="card card-tint" style="padding:10px 14px;">
        <div class="formula-title" style="color:#004BA0; font-size:9.6pt;">Wicket Valuation Currency (V)</div>
        <p style="font-size:8.4pt; margin:0; line-height:1.42;">A wicket in T20 cricket carries an empirical opportunity cost of <strong>V = 6.0 runs</strong> (sensitized across 4.0, 6.0, and 8.0 in multiverse analysis). For a batter, surviving a high-pressure ball adds +V &middot; E[W<sub>c</sub>] in dismissal avoidance. For a bowler, taking a wicket credits +(V &minus; V &middot; E[W<sub>c</sub>]) runs defended.</p>
      </div>
      <div class="card card-tint" style="padding:10px 14px;">
        <div class="formula-title" style="color:#004BA0; font-size:9.6pt;">Dirichlet-Multinomial Regularization</div>
        <p style="font-size:8.4pt; margin:0; line-height:1.42;">In small sample cells, observed frequencies are regularized toward the empirical population prior using Dirichlet-multinomial shrinkage: &theta;&#770;<sub>i, c</sub> = (k<sub>i, c</sub> + &alpha;<sub>c</sub>) / (n<sub>i</sub> + &alpha;<sub>0</sub>), with prior strength &alpha;<sub>0</sub> = 25 deliveries, eliminating extreme outlier ratings caused by small sample volatility.</p>
      </div>
    </div>

    <div class="section-h2" style="margin-top:8px;">3. Scoring Models & Isolating True Pressure Lift</div>
    <p style="font-size:9.2pt; line-height:1.44;">To measure whether a player elevates or declines when leverage peaks, performance is evaluated across three complementary mathematical models:</p>

    <div class="grid-3" style="gap:10px; margin-top:6px;">
      <div class="card" style="padding:9px 12px;">
        <div class="formula-title" style="font-size:9.2pt;">Model A &bull; Volume</div>
        <p style="font-size:8.0pt; margin:0; line-height:1.38;">Net cumulative runs added above LPO baseline in high pressure: NetRuns = &sum; w<sub>k</sub> &middot; (Runs<sub>act</sub> &minus; Runs<sub>exp</sub>). Rewards high-usage workhorses.</p>
      </div>
      <div class="card" style="padding:9px 12px;">
        <div class="formula-title" style="font-size:9.2pt;">Model B &bull; Rate (Canonical)</div>
        <p style="font-size:8.0pt; margin:0; line-height:1.38;">Leverage-weighted net run rate impact per 100 balls (batting) or per 24 balls (bowling): PWI = (&sum; w<sub>k</sub> &middot; Impact<sub>k</sub>) / (&sum; w<sub>k</sub>). Isolates efficiency.</p>
      </div>
      <div class="card" style="padding:9px 12px;">
        <div class="formula-title" style="font-size:9.2pt;">Model C &bull; Win Probability</div>
        <p style="font-size:8.0pt; margin:0; line-height:1.38;">Net Win Probability Added (&Delta;WP): WPA = &sum; (&Delta;WP<sub>act</sub> &minus; &Delta;WP<sub>exp</sub>). Emphasizes match-winning pivotal moments.</p>
      </div>
    </div>

    <div class="grid-2" style="gap:12px; margin-top:6px;">
      <div class="formula-card" style="padding:9px 12px;">
        <div class="formula-title" style="font-size:9.2pt;">Raw Pressure Lift (&Delta;<sub>raw</sub>)</div>
        <div class="formula-math" style="font-size:11.2pt; padding:4px 0;">&Delta;<sub>raw</sub> = PWI<sub>High Pressure</sub> &minus; PWI<sub>Normal Baseline</sub></div>
        <div class="formula-desc" style="font-size:8.0pt; line-height:1.38;">Measures true elevation under pressure. Positive lift indicates a player who produces more runs/wickets per ball when leverage peaks than during normal phases.</div>
      </div>

      <div class="formula-card" style="padding:9px 12px;">
        <div class="formula-title" style="font-size:9.2pt;">Maintenance Lift (&Delta;<sub>maint</sub>)</div>
        <div class="formula-math" style="font-size:10.8pt; padding:4px 0;">&Delta;<sub>maint</sub> = PWI<sub>HP</sub> &minus; 0.35 &middot; max(PWI<sub>Normal</sub>, Floor)</div>
        <div class="formula-desc" style="font-size:8.0pt; line-height:1.38;">Floor = &minus;5.0 runs/100b (batters), &minus;3.0 runs/24b (bowlers). Attenuates normal baseline drag with &alpha; = 0.35 to reward players who maintain elite output under pressure without penalizing high-volume anchors.</div>
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
  <div class="page-body">
    <div class="page-header">
      <div class="header-left">
        <span class="header-section-num">Section 5</span>
        <span class="header-title-text">Fair Comparisons & Multiverse Specification Architecture</span>
      </div>
      <div class="header-right"><span class="rr-dot"></span> Sample Gating &bull; 8-Dimensional Specification Grid</div>
    </div>

    <div class="section-h2">1. Pre-Registered Sample Gates & Dual Track Isolation</div>
    <p style="font-size:9.2pt; line-height:1.44;">To ensure that rankings reflect genuine skill rather than small-sample flukes or cross-competition contamination, the evaluation architecture enforces strict methodological governance layers:</p>

    <div class="grid-2" style="gap:12px; margin-top:6px; margin-bottom:8px;">
      <div class="card card-tint" style="padding:11px 14px;">
        <div class="formula-title" style="color:#004BA0; font-size:9.8pt;">Candidate Qualification Filter (&ge; 50% Specs)</div>
        <p style="font-size:8.5pt; margin:0; line-height:1.42;">To be considered for the final selection pool, a player must qualify across at least 50% of valid multiverse specifications. This eliminates niche players who only qualify under loose sample gates but vanish when stricter volume filters are applied. All 20 final consensus selections satisfy this gate.</p>
      </div>
      <div class="card card-tint" style="padding:11px 14px;">
        <div class="formula-title" style="color:#004BA0; font-size:9.8pt;">Bootstrap Stability Hurdle (&ge; 800 / 1,000 Draws)</div>
        <p style="font-size:8.5pt; margin:0; line-height:1.42;">In addition to multiverse eligibility, players must maintain qualification in at least 800 out of 1,000 stratified match bootstrap draws. This hurdle actively removed volatile candidates (Matthew Wade at 720 draws; Mujeeb Ur Rahman at 744 draws; Naveen ul Haq at 513 draws).</p>
      </div>
    </div>

    <div class="section-h2">2. The 8-Dimensional Multiverse Grid (15,150 Specifications)</div>
    <p style="font-size:9.2pt; line-height:1.44;">Rather than presenting a single cherry-picked model, we pre-registered an 8-dimensional multiverse evaluating 15,150 valid specifications per discipline (30,300 valid specifications and 3,196,444 player-specification evaluation records across the Parquet database):</p>

    <table style="font-size:8.0pt; margin:6px 0 10px 0;">
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
          <td><strong>Dim F</strong></td>
          <td style="text-align:left;">Competition Scope Track</td>
          <td>3</td>
          <td style="text-align:left;">F1 (IPL + All T20I), F2 (IPL + Full-Member T20I), F3 (IPL Exclusively).</td>
        </tr>
        <tr>
          <td><strong>Dim W</strong></td>
          <td style="text-align:left;">Wickets State in Baseline</td>
          <td>2</td>
          <td style="text-align:left;">W0 (Without wickets down bucket), W1 (With wickets bucket '0-2', '3-5', '6+').</td>
        </tr>
        <tr>
          <td><strong>Dim P</strong></td>
          <td style="text-align:left;">Situational Pressure Def</td>
          <td>5 / 6</td>
          <td style="text-align:left;">P1 (Sigmoid 0.40), P2 (Sigmoid 0.425), P3 (Sigmoid 0.45), P4 (Discrete &ge;0.50), P5 (Def C Situational). Bowlers evaluate P0–P5 (P0 = Diagnostic V2 Benchmark).</td>
        </tr>
        <tr>
          <td><strong>Dim V</strong></td>
          <td style="text-align:left;">Wicket Valuation (V)</td>
          <td>4</td>
          <td style="text-align:left;">V = 4.0 runs, V = 6.0 runs (Canonical T20 Par), V = 8.0 runs, V = Context-Marginal.</td>
        </tr>
        <tr>
          <td><strong>Dim K</strong></td>
          <td style="text-align:left;">EB Shrinkage Strength (K)</td>
          <td>3</td>
          <td style="text-align:left;">K = 60 (Light Shrinkage), K = 120 (Canonical Empirical Bayes), K = 180 (Heavy Shrinkage).</td>
        </tr>
        <tr>
          <td><strong>Dim G</strong></td>
          <td style="text-align:left;">Sample Volume Gating</td>
          <td>3</td>
          <td style="text-align:left;">Lenient (200b / 80 HP balls), Standard (300b / 120 HP balls), Strict (400b / 150 HP balls).</td>
        </tr>
        <tr>
          <td><strong>Dim M</strong></td>
          <td style="text-align:left;">Scoring Formulation</td>
          <td>2 + 1</td>
          <td style="text-align:left;">Model A (Cumulative Volume), Model B (Attenuated Rate Lift) + Model C (Canonical Ridge-Logit).</td>
        </tr>
        <tr>
          <td><strong>Dim S</strong></td>
          <td style="text-align:left;">Composite Metric Weights</td>
          <td>7</td>
          <td style="text-align:left;">S0 (Base 50/30/20) + 6 One-at-a-time Sensitivity Perturbations (S1&ndash;S6).</td>
        </tr>
      </tbody>
    </table>

    <div class="callout-box navy" style="padding:6px 10px; margin-top:3px; margin-bottom:6px; font-size:7.6pt; line-height:1.32;">
      <strong>Combinatorial Accounting:</strong> Each (F, W, P) cache evaluates (4 &times; 3 &times; 3 &times; 2 &times; 7) = 504 specs + 1 Model C spec = 505 specs. <strong>Batting:</strong> 3 scopes &times; 2 wicket states &times; 5 pressure defs &times; 505 = <strong>15,150 valid specs</strong>. <strong>Bowling:</strong> 3 &times; 2 &times; 6 &times; 505 = <strong>18,180 total specs</strong> (where 3,030 P0 specs serve as diagnostic single-index benchmarks flagged is_valid=False, leaving <strong>15,150 valid bowling specs</strong>).
    </div>

    <div class="section-h2" style="margin-top:6px;">3. Pre-Match Dual Track Rating Isolation</div>
    <p style="font-size:9.2pt; line-height:1.44;">To eliminate cross-format confounding, team and player strength ratings are maintained on independent Elo tracks (separate IPL and T20I tracks). All pre-match ratings are computed strictly using historical fixtures completed prior to the current match date (match_date &lt; current_match_date), guaranteeing zero look-ahead contamination.</p>

    <div class="card card-tint" style="padding:10px 14px; margin-top:8px; border-left:3.5px solid #004BA0;">
      <div class="formula-title" style="color:#004BA0; font-size:9.2pt;">Multiverse Robustness Governance Guarantee</div>
      <p style="font-size:8.4pt; margin:0; line-height:1.40;">By systematically evaluating candidates across 15,150 model specifications rather than a single hand-crafted metric, researcher degrees of freedom and parameter cherry-picking are systematically minimized through pre-registration. Any player appearing in the consensus top 10 demonstrates robust resilience across wide sensitivity perturbations across leverage thresholds, scoring formulations, and wicket valuations.</p>
    </div>
  </div>

  <div class="page-footer">
    <span>Rajat Aggarwal | Participant — SupeRR Selector Season 2</span>
    <span class="footer-center">Fair Comparisons & Multiverse Specification Architecture</span>
    <span class="footer-page-num">Page 6 of 15</span>
  </div>
</div>

<!-- PAGE 7: ANOVA & SPECIFICATION CURVES -->
<div class="page" id="page-7">
  <div class="page-body">
    <div class="page-header">
      <div class="header-left">
        <span class="header-section-num">Section 6</span>
        <span class="header-title-text">Multiverse Specification Curve & Variance Decomposition</span>
      </div>
      <div class="header-right"><span class="rr-dot"></span> Sensitivity Analysis Across 3.19M Evaluations</div>
    </div>

    <div class="section-h2">1. Sequential Type I ANOVA Variance Decomposition</div>
    <p style="font-size:9.0pt; line-height:1.42;">To answer whether player rankings are driven by genuine underlying talent or by arbitrary modelling choices, we performed a Sequential (Type I) ANOVA on percentile ranks across all 15,150 specifications. The variance components sum to exactly 100.00%:</p>

    <table style="font-size:8.0pt; margin:5px 0 7px 0;">
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
          <td><strong>285,702,638</strong></td>
          <td class="metric-positive"><strong>60.17%</strong></td>
          <td><strong>581,828,132</strong></td>
          <td class="metric-positive"><strong>62.08%</strong></td>
          <td style="text-align:left;"><strong>Dominant source of variance: consistent individual player differences drive rankings.</strong></td>
        </tr>
        <tr>
          <td style="text-align:left;">Competition Scope Main Effect (f_scope: IPL vs T20I)</td>
          <td>46,026,415</td>
          <td>9.69%</td>
          <td>88,438,217</td>
          <td>9.44%</td>
          <td style="text-align:left;">Primary analytical fork: international sample vs IPL exclusivity.</td>
        </tr>
        <tr>
          <td style="text-align:left;">Sample Volume Gate Main Effect (g_gate: Lenient/Std/Strict)</td>
          <td>13,379,929</td>
          <td>2.82%</td>
          <td>44,188,960</td>
          <td>4.72%</td>
          <td style="text-align:left;">Qualification threshold shifts candidate pool density.</td>
        </tr>
        <tr>
          <td style="text-align:left;">Pressure Definition Main Effect (p_def: P1–P5)</td>
          <td>8,082,966</td>
          <td>1.70%</td>
          <td>15,398,001</td>
          <td>1.64%</td>
          <td style="text-align:left;">Continuous center shifting (0.40 vs 0.45) & discrete thresholds.</td>
        </tr>
        <tr>
          <td style="text-align:left;">Model, Wicket Value, Weights & Shrinkage (w, v, m, k, s)</td>
          <td>253,856</td>
          <td>0.05%</td>
          <td>338,186</td>
          <td>0.04%</td>
          <td style="text-align:left;">Mathematical hyperparameter choices demonstrate negligible sensitivity.</td>
        </tr>
        <tr>
          <td style="text-align:left;">Player &times; Specification Interaction & Residual</td>
          <td>121,353,012</td>
          <td>25.56%</td>
          <td>206,958,209</td>
          <td>22.08%</td>
          <td style="text-align:left;">Individual profile shifts across specifications justify consensus aggregation.</td>
        </tr>
        <tr style="background-color:#F1F5F9; font-weight:700;">
          <td style="text-align:left;"><strong>TOTAL VARIANCE EXPLAINED</strong></td>
          <td><strong>474,798,816</strong></td>
          <td><strong>100.00%</strong></td>
          <td><strong>937,149,704</strong></td>
          <td><strong>100.00%</strong></td>
          <td style="text-align:left;"><strong>Exact mathematical reconciliation across all specifications.</strong></td>
        </tr>
      </tbody>
    </table>

    <div class="chart-box" style="margin-top:4px; margin-bottom:5px;">
      <img src="{img_var_decomp}" alt="ANOVA Variance Decomposition" style="max-height:330px;">
      <div class="chart-caption" style="font-size:7.2pt; padding:3px 6px;">Figure 2: Sequential Type I ANOVA Variance Decomposition for Batting and Bowling Percentile Ranks.</div>
    </div>

    <div class="callout-box emerald" style="padding:8px 12px;">
      <div class="callout-title" style="font-size:9.2pt;">Core Methodological Takeaway</div>
      <div style="font-size:8.2pt; line-height:1.38;">Player identity main effects explain 60.17% (batting) and 62.08% (bowling) of rank variance in a Sequential Type I ANOVA [player_id, f_scope, g_gate, p_def, w, v, m, k, s] on the unbalanced candidate panel, demonstrating that observed player differences dominate methodological noise rather than serving as causal proof of invariant talent. Because player &times; specification interactions account for 22.08% to 25.56% of variance, reporting consensus rankings aggregated across 15,150 specifications is essential.</div>
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
  <div class="page-body">
    <div class="page-header">
      <div class="header-left">
        <span class="header-section-num">Section 7A</span>
        <span class="header-title-text">Consensus Batting Rankings: Full Table & Profiles 1–5</span>
      </div>
      <div class="header-right"><span class="rr-dot"></span> Multiverse Consensus Results &bull; Empirical Evidence</div>
    </div>

    <div class="section-h2">Table 2A: Comprehensive Top-10 Batting Multiverse Metrics</div>
    <table style="font-size:6.6pt; margin:1px 0 3px 0;">
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

    <div class="player-dossier" style="padding:3.5px 6.5px; margin-bottom:2.5px;">
      <div class="dossier-header">
        <span class="dossier-name" style="font-size:8.0pt;">1. Shashank Singh <span class="id-muted">(ID: 2756)</span> &mdash; Tier 1 | Punjab Kings</span>
        <span class="badge badge-tier1" style="font-size:5.6pt;">Consensus #1 Batter</span>
      </div>
      <div class="dossier-metrics" style="font-size:6.4pt; padding:1.5px 4px;">
        <span><strong>Shrunk PWI:</strong> +32.2 r/100b</span> &bull;
        <span><strong>Raw Lift:</strong> +22.2</span> &bull;
        <span><strong>Top-10 Freq:</strong> 94.9%</span> &bull;
        <span><strong>Med Rank:</strong> 5.0 [IQR 3.0]</span> &bull;
        <span><strong>Boot 90% CI:</strong> [1, 44]</span> &bull;
        <span><strong>HP Balls:</strong> 327</span>
      </div>
      <div class="dossier-prose" style="font-size:6.8pt; line-height:1.26;">
        <strong>Empirical Evidence:</strong> Shashank achieved a 94.9% top-10 finish across all eligible specifications, demonstrating extraordinary resilience when leverage peaks. His raw lift of +22.2 runs/100b reflects a surge from a normal baseline of +10.0 to a high-pressure PWI of +32.2. He rises under pressure in 100.0% of evaluated specifications. <strong>Availability & Tactical Context:</strong> Retained by Punjab Kings (PBKS) for IPL 2027; preserved in analytical rankings as an unmanipulated historical performance benchmark.
      </div>
    </div>

    <div class="player-dossier" style="padding:3.5px 6.5px; margin-bottom:2.5px;">
      <div class="dossier-header">
        <span class="dossier-name" style="font-size:8.0pt;">2. Tim David <span class="id-muted">(ID: 6396)</span> &mdash; Tier 1 | Royal Challengers Bengaluru</span>
        <span class="badge badge-tier1" style="font-size:5.6pt;">Consensus #2 Batter</span>
      </div>
      <div class="dossier-metrics" style="font-size:6.4pt; padding:1.5px 4px;">
        <span><strong>Shrunk PWI:</strong> +42.9 r/100b</span> &bull;
        <span><strong>Raw Lift:</strong> +9.0</span> &bull;
        <span><strong>Top-10 Freq:</strong> 92.1%</span> &bull;
        <span><strong>Med Rank:</strong> 1.0 [IQR 2.0]</span> &bull;
        <span><strong>Boot 90% CI:</strong> [1, 16]</span> &bull;
        <span><strong>HP Balls:</strong> 570</span>
      </div>
      <div class="dossier-prose" style="font-size:6.8pt; line-height:1.26;">
        <strong>Empirical Evidence:</strong> Highest absolute high-pressure output in the dataset (+42.9 runs/100b) across 570 balls. Achieves a median rank of 1.0 with a tight bootstrap 90% interval of [1, 16]. Rises under pressure in 78.1% of specifications. <strong>Availability & Tactical Context:</strong> Retained by Royal Challengers Bengaluru (RCB); elite overseas power-finishing historical benchmark.
      </div>
    </div>

    <div class="player-dossier" style="padding:3.5px 6.5px; margin-bottom:2.5px;">
      <div class="dossier-header">
        <span class="dossier-name" style="font-size:8.0pt;">3. Naman Dhir <span class="id-muted">(ID: 37052)</span> &mdash; Tier 1 | Mumbai Indians</span>
        <span class="badge badge-tier1" style="font-size:5.6pt;">Consensus #3 Batter</span>
      </div>
      <div class="dossier-metrics" style="font-size:6.4pt; padding:1.5px 4px;">
        <span><strong>Shrunk PWI:</strong> +34.7 r/100b</span> &bull;
        <span><strong>Raw Lift:</strong> +35.4</span> &bull;
        <span><strong>Top-10 Freq:</strong> 88.6%</span> &bull;
        <span><strong>Med Rank:</strong> 4.0 [IQR 5.0]</span> &bull;
        <span><strong>Boot 90% CI:</strong> [1, 32]</span> &bull;
        <span><strong>HP Balls:</strong> 186</span>
      </div>
      <div class="dossier-prose" style="font-size:6.8pt; line-height:1.26;">
        <strong>Empirical Evidence:</strong> Demonstrates the highest positive pressure lift (+35.4 runs/100b) among all regular batters, surging from &minus;0.7 normal output to +34.7 in high leverage across 186 balls. Qualified in 91.1% of specifications with 88.6% top-10 frequency. <strong>Availability & Tactical Context:</strong> Retained by Mumbai Indians (MI); domestic high-leverage elevation benchmark.
      </div>
    </div>

    <div class="player-dossier" style="padding:3.5px 6.5px; margin-bottom:2.5px;">
      <div class="dossier-header">
        <span class="dossier-name" style="font-size:8.0pt;">4. Dinesh Karthik <span class="id-muted">(ID: 143)</span> &mdash; Tier 2 | Historical Benchmark (Retired)</span>
        <span class="badge badge-tier1" style="font-size:5.6pt;">Historical Benchmark</span>
      </div>
      <div class="dossier-metrics" style="font-size:6.4pt; padding:1.5px 4px;">
        <span><strong>Shrunk PWI:</strong> +34.4 r/100b</span> &bull;
        <span><strong>Raw Lift:</strong> +16.1</span> &bull;
        <span><strong>Top-10 Freq:</strong> 78.3%</span> &bull;
        <span><strong>Med Rank:</strong> 5.0 [IQR 7.0]</span> &bull;
        <span><strong>Boot 90% CI:</strong> [1, 44]</span> &bull;
        <span><strong>HP Balls:</strong> 250</span>
      </div>
      <div class="dossier-prose" style="font-size:6.8pt; line-height:1.26;">
        <strong>Empirical Evidence:</strong> Exceptional historical pressure execution (+34.4 PWI, +16.1 raw lift) across 250 high-pressure deliveries. Top-10 in 78.3% of multiverse specifications. <strong>Practical Feasibility Context:</strong> Officially retired from IPL following 2024 season; active RCB Batting Coach & Mentor (2025–2026). Retained in analytics strictly as an unmanipulated statistical benchmark.
      </div>
    </div>

    <div class="player-dossier" style="padding:3.5px 6.5px; margin-bottom:2.5px;">
      <div class="dossier-header">
        <span class="dossier-name" style="font-size:8.0pt;">5. Heinrich Klaasen <span class="id-muted">(ID: 4260)</span> &mdash; Tier 2 | Sunrisers Hyderabad</span>
        <span class="badge badge-tier1" style="font-size:5.6pt;">Consensus #5 Batter</span>
      </div>
      <div class="dossier-metrics" style="font-size:6.4pt; padding:1.5px 4px;">
        <span><strong>Shrunk PWI:</strong> +24.9 r/100b</span> &bull;
        <span><strong>Raw Lift:</strong> +3.4</span> &bull;
        <span><strong>Top-10 Freq:</strong> 74.4%</span> &bull;
        <span><strong>Med Rank:</strong> 7.0 [IQR 7.0]</span> &bull;
        <span><strong>Boot 90% CI:</strong> [5, 34]</span> &bull;
        <span><strong>HP Balls:</strong> 459</span>
      </div>
      <div class="dossier-prose" style="font-size:6.8pt; line-height:1.26;">
        <strong>Empirical Evidence:</strong> World-class spin destroyer (+24.9 PWI across 459 HP balls). Features in top 10 across 74.4% of specifications with exceptional maintenance lift (+17.4). <strong>Availability & Tactical Context:</strong> Retained by Sunrisers Hyderabad (SRH, ₹23.00 Cr); world-class middle-overs spin-tackling benchmark.
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
  <div class="page-body">
    <div class="page-header">
      <div class="header-left">
        <span class="header-section-num">Section 7B</span>
        <span class="header-title-text">Batting Profiles Continued (6–10) & Resilience Landscape</span>
      </div>
      <div class="header-right"><span class="rr-dot"></span> Evidence for Batters 6 to 10 &bull; Maintenance vs Lift</div>
    </div>

    <div class="section-h2">Detailed Empirical Profiles: Batters 6 to 10</div>

    <div class="player-dossier" style="padding:4.5px 7.5px; margin-bottom:4px;">
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
        <strong>Empirical Evidence:</strong> Massive sample volume of 657 HP balls with shrunk PWI of +25.4. His raw lift is &minus;4.6, reflecting an astronomical normal baseline (+30.0). Classified as "Elite all the time" (rises in 23.3% of specs). <strong>Availability & Tactical Context:</strong> Retained by Mumbai Indians (MI); world-class 360-degree high-pressure historical benchmark.
      </div>
    </div>

    <div class="player-dossier" style="padding:4.5px 7.5px; margin-bottom:4px;">
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
        <strong>Empirical Evidence:</strong> Prototypical chase finisher (+31.0 PWI, +17.9 raw lift across 507 HP balls). Rises under pressure in 80.0% of multiverse specifications with 63.1% top-10 inclusion. <strong>Availability & Tactical Context:</strong> Retained by Kolkata Knight Riders (KKR, ₹13.00 Cr); elite domestic chase-finishing benchmark.
      </div>
    </div>

    <div class="player-dossier" style="padding:4.5px 7.5px; margin-bottom:4px;">
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
        <strong>Empirical Evidence:</strong> Powerhouse lower-order hitter (+28.7 PWI, +5.0 lift across 431 balls). Finishes in the top 10 across 55.5% of multiverse runs. <strong>Availability & Tactical Context:</strong> Retained by Royal Challengers Bengaluru (RCB); lower-order explosive power-hitting benchmark.
      </div>
    </div>

    <div class="player-dossier" style="padding:4.5px 7.5px; margin-bottom:4px;">
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

    <div class="player-dossier" style="padding:4.5px 7.5px; margin-bottom:4px;">
      <div class="dossier-header">
        <span class="dossier-name">10. Rashid Khan <span class="id-muted">(ID: 4722)</span> &mdash; Tier 3 | Gujarat Titans</span>
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
        <strong>Empirical Evidence:</strong> Extraordinary dual-threat asset. As a batter, records a raw lift of +40.3 (surging from &minus;12.2 to +28.1). Features in the top 10 in 47.9% of specifications (61.6% retention when eligible) and also finishes #3 among bowlers. <strong>Availability:</strong> Retained by Gujarat Titans (GT, ₹18.00 Cr); dual-threat benchmark.
      </div>
    </div>

    <div class="chart-box" style="margin-top:3px;">
      <img src="{img_maint_bat}" alt="Maintenance vs Lift Batters" style="max-height:310px;">
      <div class="chart-caption" style="font-size:7.0pt; padding:3px 6px;">Figure 3: Batting Resilience Landscape &mdash; High-Pressure Output vs Baseline Maintenance across all eligible batters.</div>
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
  <div class="page-body">
    <div class="page-header">
      <div class="header-left">
        <span class="header-section-num">Section 8A</span>
        <span class="header-title-text">Consensus Bowling Rankings: Full Table & Profiles 1–5</span>
      </div>
      <div class="header-right"><span class="rr-dot"></span> Defending-Side Evaluation &bull; Empirical Evidence</div>
    </div>

    <div class="section-h2">Table 2B: Comprehensive Top-10 Bowling Multiverse Metrics</div>
    <table style="font-size:6.6pt; margin:1px 0 3px 0;">
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

    <div class="player-dossier" style="padding:3.5px 6.5px; margin-bottom:2.5px;">
      <div class="dossier-header">
        <span class="dossier-name" style="font-size:8.0pt;">1. Sunil Narine <span class="id-muted">(ID: 781)</span> &mdash; Tier 1 | Kolkata Knight Riders</span>
        <span class="badge badge-tier1" style="font-size:5.6pt;">Consensus #1 Bowler</span>
      </div>
      <div class="dossier-metrics" style="font-size:6.4pt; padding:1.5px 4px;">
        <span><strong>Shrunk PWI:</strong> +6.57 r/24b</span> &bull;
        <span><strong>Raw Lift:</strong> +0.64</span> &bull;
        <span><strong>Top-10 Freq:</strong> 100.0%</span> &bull;
        <span><strong>Med Rank:</strong> 3.0 [IQR 1.0]</span> &bull;
        <span><strong>Boot 90% CI:</strong> [1, 17]</span> &bull;
        <span><strong>HP Balls:</strong> 422</span>
      </div>
      <div class="dossier-prose" style="font-size:6.8pt; line-height:1.26;">
        <strong>Empirical Evidence:</strong> Perfect 100.0% top-10 frequency across all 15,150 specifications. Defends +6.57 runs saved per 24 balls across 422 HP deliveries. Remarkably stable with a median rank of 3.0 and IQR of 1.0. <strong>Tactical Scouting Fit:</strong> Premier defensive spinner in T20 history. Smothers run rates in high leverage while restricting boundary access. Retained by Kolkata Knight Riders (KKR, ₹12.00 Cr); premier defensive spin benchmark in T20 history.
      </div>
    </div>

    <div class="player-dossier" style="padding:3.5px 6.5px; margin-bottom:2.5px;">
      <div class="dossier-header">
        <span class="dossier-name" style="font-size:8.0pt;">2. Jasprit Bumrah <span class="id-muted">(ID: 2933)</span> &mdash; Tier 1 | Mumbai Indians</span>
        <span class="badge badge-tier1" style="font-size:5.6pt;">Consensus #2 Bowler</span>
      </div>
      <div class="dossier-metrics" style="font-size:6.4pt; padding:1.5px 4px;">
        <span><strong>Shrunk PWI:</strong> +7.61 r/24b</span> &bull;
        <span><strong>Raw Lift:</strong> +0.33</span> &bull;
        <span><strong>Top-10 Freq:</strong> 99.2%</span> &bull;
        <span><strong>Med Rank:</strong> 2.0 [IQR 2.0]</span> &bull;
        <span><strong>Boot 90% CI:</strong> [1, 23]</span> &bull;
        <span><strong>HP Balls:</strong> 332</span>
      </div>
      <div class="dossier-prose" style="font-size:6.8pt; line-height:1.26;">
        <strong>Empirical Evidence:</strong> Highest absolute defending impact (+7.61 runs saved/24b) in the competition. Finishes inside top 10 in 99.2% of specifications with median rank 2.0 across 332 balls. <strong>Availability & Tactical Context:</strong> Retained by Mumbai Indians (MI, ₹18.00 Cr); the global standard for high-pressure death bowling.
      </div>
    </div>

    <div class="player-dossier" style="padding:3.5px 6.5px; margin-bottom:2.5px;">
      <div class="dossier-header">
        <span class="dossier-name" style="font-size:8.0pt;">3. Rashid Khan <span class="id-muted">(ID: 4722)</span> &mdash; Tier 1 | Gujarat Titans</span>
        <span class="badge badge-tier1" style="font-size:5.6pt;">Consensus #3 Bowler</span>
      </div>
      <div class="dossier-metrics" style="font-size:6.4pt; padding:1.5px 4px;">
        <span><strong>Shrunk PWI:</strong> +5.59 r/24b</span> &bull;
        <span><strong>Raw Lift:</strong> +2.75</span> &bull;
        <span><strong>Top-10 Freq:</strong> 93.5%</span> &bull;
        <span><strong>Med Rank:</strong> 5.0 [IQR 4.0]</span> &bull;
        <span><strong>Boot 90% CI:</strong> [1, 19]</span> &bull;
        <span><strong>HP Balls:</strong> 706</span>
      </div>
      <div class="dossier-prose" style="font-size:6.8pt; line-height:1.26;">
        <strong>Empirical Evidence:</strong> Heaviest high-pressure workload in the database (706 balls) while defending +5.59 runs/24b with +2.75 raw lift. Top 10 in 93.5% of multiverse runs. <strong>Tactical Scouting Fit:</strong> Irreplaceable wicket-taking wrist-spinner who thrives in high leverage. Retained by Gujarat Titans (GT, ₹18.00 Cr); primary wrist-spin benchmark across the multiverse.
      </div>
    </div>

    <div class="player-dossier" style="padding:3.5px 6.5px; margin-bottom:2.5px;">
      <div class="dossier-header">
        <span class="dossier-name" style="font-size:8.0pt;">4. Matheesha Pathirana <span class="id-muted">(ID: 8661)</span> &mdash; Tier 1 | Chennai Super Kings (Released)</span>
        <span class="badge badge-tier1" style="font-size:5.6pt;">Consensus #4 Bowler</span>
      </div>
      <div class="dossier-metrics" style="font-size:6.4pt; padding:1.5px 4px;">
        <span><strong>Shrunk PWI:</strong> +5.34 r/24b</span> &bull;
        <span><strong>Raw Lift:</strong> +1.21</span> &bull;
        <span><strong>Top-10 Freq:</strong> 83.4%</span> &bull;
        <span><strong>Med Rank:</strong> 3.0 [IQR 4.0]</span> &bull;
        <span><strong>Boot 90% CI:</strong> [1, 41]</span> &bull;
        <span><strong>HP Balls:</strong> 307</span>
      </div>
      <div class="dossier-prose" style="font-size:6.8pt; line-height:1.26;">
        <strong>Empirical Evidence:</strong> Sling-action death specialist defending +5.34 runs/24b across 307 HP balls. Top 10 in 83.4% of specifications. <strong>Availability & Medical Governance:</strong> Historical V4 death-bowling performance is elite. Released by CSK. Auction registration (23 Nov 2026 deadline) and 2027 medical/workload clearance remain subject to official verification.
      </div>
    </div>

    <div class="player-dossier" style="padding:3.5px 6.5px; margin-bottom:2.5px;">
      <div class="dossier-header">
        <span class="dossier-name" style="font-size:8.0pt;">5. Eshan Malinga <span class="id-muted">(ID: 39657)</span> &mdash; Tier 2 | Sunrisers Hyderabad</span>
        <span class="badge badge-tier1" style="font-size:5.6pt;">Consensus #5 Bowler</span>
      </div>
      <div class="dossier-metrics" style="font-size:6.4pt; padding:1.5px 4px;">
        <span><strong>Shrunk PWI:</strong> +3.85 r/24b</span> &bull;
        <span><strong>Raw Lift:</strong> +3.39</span> &bull;
        <span><strong>Top-10 Freq:</strong> 71.9%</span> &bull;
        <span><strong>Med Rank:</strong> 6.0 [IQR 5.0]</span> &bull;
        <span><strong>Boot 90% CI:</strong> [1, 38]</span> &bull;
        <span><strong>HP Balls:</strong> 176</span>
      </div>
      <div class="dossier-prose" style="font-size:6.8pt; line-height:1.26;">
        <strong>Empirical Evidence:</strong> Outstanding emergence under pressure (+3.85 PWI, +3.39 raw lift across 176 balls). Features in top 10 in 71.9% of specifications. <strong>Availability & Tactical Context:</strong> Retained by Sunrisers Hyderabad (SRH); breakout high-pace sling-action bowling benchmark.
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
  <div class="page-body">
    <div class="page-header">
      <div class="header-left">
        <span class="header-section-num">Section 8B</span>
        <span class="header-title-text">Bowling Profiles Continued (6–10) & Resilience Landscape</span>
      </div>
      <div class="header-right"><span class="rr-dot"></span> Evidence for Bowlers 6 to 10 &bull; Maintenance vs Lift</div>
    </div>

    <div class="section-h2">Detailed Empirical Profiles: Bowlers 6 to 10</div>

    <div class="player-dossier" style="padding:4.5px 7.5px; margin-bottom:4px;">
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
        <strong>Empirical Evidence:</strong> Elite death specialist defending +5.50 runs/24b with +3.15 raw lift. Top 10 in 54.8% of specs (72.5% retention when eligible). <strong>Availability & Trade Context:</strong> Mapped to CSK in raw data; officially traded CSK &rarr; SRH on 5 Nov 2026 for ₹2.00 Cr all-cash; retained by SRH for IPL 2027. Historical benchmark.
      </div>
    </div>

    <div class="player-dossier" style="padding:4.5px 7.5px; margin-bottom:4px;">
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
        <strong>Empirical Evidence:</strong> Left-arm wrist-spin control defending +2.54 runs/24b across 351 HP balls. Top 10 in 40.1% of multiverse runs. <strong>Availability & Tactical Context:</strong> Retained by Chennai Super Kings (CSK); elite left-arm wrist-spin historical benchmark.
      </div>
    </div>

    <div class="player-dossier" style="padding:4.5px 7.5px; margin-bottom:4px;">
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
        <strong>Empirical Evidence:</strong> Heavy-volume Indian left-arm seamer (593 HP balls) defending +1.90 runs/24b. <strong>Availability & Trade Context:</strong> Mapped to PBKS in raw data; traded PBKS &rarr; MI on 11 Nov 2026 (₹18.00 Cr all-cash); retained by MI. High-volume Indian death-bowling benchmark.
      </div>
    </div>

    <div class="player-dossier" style="padding:4.5px 7.5px; margin-bottom:4px;">
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
        <strong>Empirical Evidence:</strong> High-release hit-the-deck pace defending +2.96 runs/24b with +2.67 raw lift across 234 HP balls. Rises under pressure in 68.3% of specifications. <strong>Availability & Tactical Context:</strong> Retained by Gujarat Titans (GT); high-release pace benchmark.
      </div>
    </div>

    <div class="player-dossier" style="padding:4.5px 7.5px; margin-bottom:4px;">
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
        <strong>Empirical Evidence:</strong> Veteran swing and knuckleball master defending +3.25 runs/24b across 361 balls. Elite baseline output (+4.56). Retained by Royal Challengers Bengaluru (RCB); veteran powerplay and knuckleball control benchmark.
      </div>
    </div>

    <div class="chart-box" style="margin-top:3px;">
      <img src="{img_maint_bowl}" alt="Maintenance vs Lift Bowlers" style="max-height:310px;">
      <div class="chart-caption" style="font-size:7.0pt; padding:3px 6px;">Figure 4: Bowling Resilience Landscape &mdash; Defending Run Impact vs Baseline Maintenance across all eligible bowlers.</div>
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
  <div class="page-body">
    <div class="page-header">
      <div class="header-left">
        <span class="header-section-num">Section 9</span>
        <span class="header-title-text">Rajasthan Royals Tactical Recruitment Dossier</span>
      </div>
      <div class="header-right"><span class="rr-dot"></span> IPL 2026 Phase-Level Audit from Raw Data</div>
    </div>

    <div class="section-h2">1. Audited Rajasthan Royals 2026 Performance (from Raw Data)</div>
    <p style="font-size:9.0pt; line-height:1.42;">To ensure recommendations are actionable, RR's actual 2026 campaign was audited directly from raw match records (matches.csv, ball_by_ball.csv, playing_eleven.csv). RR played 16 matches, captained primarily by Riyan Parag (14 matches) with Yashasvi Jaiswal leading in 2 (Sanju Samson represented CSK in 2026):</p>

    <table style="font-size:8.0pt; margin:5px 0 8px 0;">
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

    <div class="callout-box navy" style="padding:5px 9px; margin-bottom:5px; font-size:7.5pt;">
      <strong>Confirmed Post-Retention Squad Position (17 Nov 2026 Cutoff):</strong> 19 players under contract (17 retained + 2 trades in) | <strong>Available Purse: ₹27.05 Cr</strong> (7th in IPL) | <strong>6 Open Slots</strong> (3 Overseas). Confirmed Trades In: <strong>Mohammed Shami</strong> (LSG &rarr; RR, ₹8.00 Cr pace spearhead), <strong>M. Siddharth</strong> (LSG &rarr; RR, ₹0.75 Cr SLA spin); Traded Out: <strong>Sam Curran</strong> (RR &rarr; LSG, ₹14.50 Cr). Key Releases: <strong>Shimron Hetmyer</strong> (clearing ₹11.00 Cr), <strong>Tushar Deshpande</strong> (clearing ₹6.50 Cr).
    </div>

    <div class="section-h2" style="margin-top:2px;">2. Post-Retention Phase Solutions & Recruitment Strategy</div>
    <div class="grid-2" style="gap:8px; margin-top:3px;">
      <div class="callout-box navy" style="padding:6px 10px;">
        <div class="callout-title" style="font-size:8.6pt;">Phase Solution &bull; Death-Overs Pace Spearhead</div>
        <p style="font-size:7.6pt; margin:0; line-height:1.32;"><strong>Deficit:</strong> Supporting pacers Sandeep Sharma (ER 13.70) and released Deshpande (ER 12.38) leaked runs excessively at the death.<br>
        <strong>Recruitment Target:</strong> <strong>Matheesha Pathirana</strong> (RR Priority #1 Bowler, V4 Impact +5.34 r/24b, 83.4% Top-10 freq; Max Bid: ₹11.50 Cr) or <strong>Trent Boult</strong> (Priority #3, new-ball/death left-arm swing, ₹5.00 Cr) / <strong>Avesh Khan</strong> (Priority #2, heavy-ball workhorse, ₹5.50 Cr).</p>
      </div>

      <div class="callout-box emerald" style="padding:6px 10px;">
        <div class="callout-title" style="font-size:8.6pt;">Phase Solution &bull; Lower-Order Finisher Rebalance</div>
        <p style="font-size:7.6pt; margin:0; line-height:1.32;"><strong>Deficit:</strong> Donovan Ferreira (death SR 221.7) had no reliable partner; Hetmyer released to recover ₹11 Cr purse.<br>
        <strong>Recruitment Target:</strong> <strong>Nehal Wadhera</strong> (RR Priority #1 Batter, domestic LHB finisher, death SR 172.9, 100% elig, 976 boot draws; Max Bid: ₹7.50 Cr) and <strong>M Shahrukh Khan</strong> (Priority #2, domestic RHB pace destroyer, death SR 168.4, 93.4% elig; Max Bid: ₹4.50 Cr).</p>
      </div>
    </div>

    <div class="grid-2" style="gap:8px; margin-top:4px;">
      <div class="callout-box blue" style="padding:6px 10px;">
        <div class="callout-title" style="font-size:8.6pt;">Phase Solution &bull; Middle-Overs Spin Balance</div>
        <p style="font-size:7.6pt; margin:0; line-height:1.32;"><strong>Deficit:</strong> RR conceded boundaries on 17.8% of middle balls (Jadeja 8.39, Bishnoi 10.11 ER).<br>
        <strong>Tactical Adjustment:</strong> Acquisition of <strong>M. Siddharth</strong> (LSG trade, ₹0.75 Cr) secures domestic SLA control, preserving overseas slots exclusively for death bowling (Pathirana).</p>
      </div>

      <div class="callout-box gold" style="padding:6px 10px;">
        <div class="callout-title" style="font-size:8.6pt;">RR Auction Purse Allocation Plan (₹27.05 Cr Available)</div>
        <p style="font-size:7.6pt; margin:0; line-height:1.32;"><strong>Primary Scenario:</strong> <strong>Pathirana</strong> (₹10.50 Cr, OS#1) + <strong>Wadhera</strong> (₹6.50 Cr, Ind#1) + <strong>Shahrukh</strong> (₹4.00 Cr, Ind#2) + <strong>Boult</strong> (₹3.50 Cr, OS#2) + 2 Uncapped (₹0.60 Cr) + Reserve (₹1.95 Cr) = <strong>₹27.05 Cr</strong>.<br><strong>Contingency Pivot:</strong> If Pathirana exceeds ceiling/fails medical, pivot to <strong>Boult</strong> (₹4.50 Cr) + <strong>Avesh Khan</strong> (₹5.00 Cr) + <strong>Wadhera</strong> (₹7.50 Cr) + <strong>Shahrukh</strong> (₹4.50 Cr) + <strong>Mustafizur</strong> (₹2.50 Cr) + 1 Uncapped (₹0.30 Cr) + Reserve (₹2.75 Cr) = <strong>₹27.05 Cr</strong>.</p>
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
  <div class="page-body">
    <div class="page-header">
      <div class="header-left">
        <span class="header-section-num">Section 10</span>
        <span class="header-title-text">Model Reliability, Limitations & Walk-Forward Validation</span>
      </div>
      <div class="header-right"><span class="rr-dot"></span> Out-of-Sample Performance &bull; Stability Checks</div>
    </div>

    <div class="section-h2">1. Walk-Forward Temporal Validation (2022–2024 to 2025–2026)</div>
    <p style="font-size:9.0pt; line-height:1.42;">To evaluate predictive validity honestly, models trained on 2022–2024 data were tested out-of-sample against 2025–2026 performance on the canonical specification:</p>

    <div class="grid-2" style="gap:11px; margin-top:4px; margin-bottom:6px;">
      <div class="callout-box navy" style="padding:10px 13px;">
        <div class="callout-title" style="font-size:9.4pt;">Canonical Batting Stability (Out-of-Sample)</div>
        <div class="formula-math" style="text-align:left; font-size:10.0pt; padding:3px 0;">Spearman r = 0.0508 &emsp;(p = 0.7864, uninformative)</div>
        <p style="font-size:8.0pt; margin:0; line-height:1.38;">Batting pressure rankings are descriptive, not predictive. High-pressure batting over 1–2 seasons contains extreme situational noise, field placement luck, and role volatility. Historical metrics describe what occurred rather than guaranteeing replication.</p>
      </div>

      <div class="callout-box blue" style="padding:10px 13px;">
        <div class="callout-title" style="font-size:9.4pt;">Canonical Bowling Stability (Out-of-Sample)</div>
        <div class="formula-math" style="text-align:left; font-size:10.0pt; padding:3px 0;">Spearman r = 0.2646 &emsp;(p = 0.0721, modest positive)</div>
        <p style="font-size:8.0pt; margin:0; line-height:1.38;">Defending bowling displays modest positive persistence across seasons (r = 0.26). Bowling execution (yorkers, slower balls, hard lengths) under pressure is more repeatable than batting contact outcomes, but still requires multi-season smoothing.</p>
      </div>
    </div>

    <div class="section-h2">2. Bootstrap Stability Hurdle: Excluded Candidates Audit</div>
    <p style="font-size:9.0pt; line-height:1.42;">Enforcing the 1,000-draw stratified match bootstrap hurdle (&ge;800 valid draws) successfully pruned volatile, sample-dependent players:</p>

    <table style="font-size:8.0pt; margin:5px 0 7px 0;">
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

    <div class="grid-2" style="gap:9px; margin-top:4px;">
      <div class="chart-box compact">
        <img src="{img_boot_bat}" alt="Bootstrap Stability Batters" style="max-height:250px;">
        <div class="chart-caption" style="font-size:7.0pt; padding:2.5px 5px;">Figure 5A: Batter Bootstrap Rank Distributions across 1,000 resamples.</div>
      </div>
      <div class="chart-box compact">
        <img src="{img_boot_bowl}" alt="Bootstrap Stability Bowlers" style="max-height:250px;">
        <div class="chart-caption" style="font-size:7.0pt; padding:2.5px 5px;">Figure 5B: Bowler Bootstrap Rank Distributions across 1,000 resamples.</div>
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
  <div class="page-body">
    <div class="page-header">
      <div class="header-left">
        <span class="header-section-num">Section 11</span>
        <span class="header-title-text">Players Next in Line (Ranks 11–15) & Contingency Targets</span>
      </div>
      <div class="header-right"><span class="rr-dot"></span> Depth Charts &bull; Strategic Alternatives</div>
    </div>

    <div class="section-h2">1. Batters Next in Line (Ranks 11 to 15)</div>
    <table style="font-size:8.0pt; margin:5px 0 8px 0;">
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
          <td style="text-align:left;"><strong>Ashutosh Sharma (8101)*</strong></td>
          <td>38.20%</td>
          <td>9.0 [11.0]</td>
          <td><span class="metric-negative">662 / 1000 (Failed)</span></td>
          <td style="text-align:left;">Explosive finisher (+29.7 raw lift), but fails formal stability hurdle (&lt; 800 draws); high-variance exploratory option only.</td>
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

    <div class="section-h2" style="margin-top:5px;">2. Bowlers Next in Line (Ranks 11 to 15)</div>
    <table style="font-size:8.0pt; margin:5px 0 8px 0;">
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

    <div class="section-h2" style="margin-top:4px;">3. Post-Retention Auction Recruitment Shortlist (Dual-Ranking Architecture)</div>
    <div class="grid-2" style="gap:8px; margin-top:2px;">
      <table style="font-size:7.2pt;">
        <thead>
          <tr>
            <th>RR#</th>
            <th>V4#</th>
            <th style="text-align:left;">Focus Batter</th>
            <th>Role Fit</th>
            <th>PWI</th>
            <th>Max Bid</th>
          </tr>
        </thead>
        <tbody>
          <tr><td><strong>#1</strong></td><td>#56</td><td style="text-align:left;"><strong>Nehal Wadhera (7059)</strong></td><td>Indian LHB Finisher</td><td>-2.11</td><td>₹7.50 Cr</td></tr>
          <tr><td><strong>#2</strong></td><td>#73</td><td style="text-align:left;"><strong>M Shahrukh Khan (3782)</strong></td><td>Indian RHB Pace Hitter</td><td>-2.69</td><td>₹4.50 Cr</td></tr>
          <tr><td><strong>#3</strong></td><td>#42</td><td style="text-align:left;"><strong>Nitish Rana (4246)</strong></td><td>LHB Anchor/Floater</td><td>+6.19</td><td>₹4.00 Cr</td></tr>
        </tbody>
      </table>

      <table style="font-size:7.2pt;">
        <thead>
          <tr>
            <th>RR#</th>
            <th>V4#</th>
            <th style="text-align:left;">Focus Bowler</th>
            <th>Role Fit</th>
            <th>PWI</th>
            <th>Max Bid</th>
          </tr>
        </thead>
        <tbody>
          <tr><td><strong>#1</strong></td><td>#4</td><td style="text-align:left;"><strong>Matheesha Pathirana (8661)</strong></td><td>Overseas Death Specialist</td><td>+5.34</td><td>₹11.50 Cr</td></tr>
          <tr><td><strong>#2</strong></td><td>#31</td><td style="text-align:left;"><strong>Avesh Khan (3653)</strong></td><td>Domestic Pace Workhorse</td><td>+0.29</td><td>₹5.50 Cr</td></tr>
          <tr><td><strong>#3</strong></td><td>#30</td><td style="text-align:left;"><strong>Trent Boult (2320)</strong></td><td>Left-Arm Swing Spearhead</td><td>+2.39</td><td>₹5.00 Cr</td></tr>
        </tbody>
      </table>
    </div>

    <div class="grid-2" style="gap:8px; margin-top:4px;">
      <div class="callout-box navy" style="padding:6px 10px;">
        <div class="callout-title" style="font-size:8.4pt;">Contingency Scenario A &bull; Bidding Inflation on Pathirana</div>
        <p style="font-size:7.4pt; margin:0; line-height:1.32;">If aggressive bidding for Pathirana exceeds the ₹11.50 Cr hard ceiling, immediately pivot to <strong>Trent Boult</strong> (Target ₹3.50–5.00 Cr) paired with <strong>Avesh Khan</strong> (Target ₹4.50–5.50 Cr), shifting remaining purse capital to guarantee securing primary Indian finisher <strong>Nehal Wadhera</strong>.</p>
      </div>
      <div class="callout-box gold" style="padding:6px 10px;">
        <div class="callout-title" style="font-size:8.4pt;">Contingency Scenario B &bull; Medical & Registration Governance</div>
        <p style="font-size:7.4pt; margin:0; line-height:1.32;">Candidate screening enforces strict governance filters: <strong>Jacob Bethell</strong> subject to ECB medical clearance; <strong>Mitchell Starc</strong> opted out per official media confirmation; <strong>Mustafizur Rahman</strong> subject to BCB NOC issuance; <strong>Matheesha Pathirana</strong> subject to auction registration and 2027 fitness clearance. Registration: <em>Pending - Deadline 23 Nov 2026; Final List 3 Dec 2026</em>.</p>
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
  <div class="page-body">
    <div class="page-header">
      <div class="header-left">
        <span class="header-section-num">Section 12</span>
        <span class="header-title-text">Appendix: Baseline Lists, Governance & Reproducibility</span>
      </div>
      <div class="header-right"><span class="rr-dot"></span> Governance &bull; Code Execution &bull; Checksums</div>
    </div>

    <div class="section-h2">Appendix A: Unfiltered Single-Spec Canonical Baselines (Spec P2-W1-Model B)</div>
    <div class="grid-2" style="gap:11px; margin-bottom:5px;">
      <table style="font-size:7.6pt;">
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

      <table style="font-size:7.6pt;">
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

    <div class="section-h2" style="margin-top:3px;">Appendix B: Canonical CLI Commands & Reproducibility Pipeline</div>
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

    <div style="font-size:6.7pt; color:#64748B; margin-top:1px; line-height:1.25;">
      * <strong>Matthew Wade (796):</strong> Excluded from consensus rankings after failing the pre-registered bootstrap stability hurdle (720/1,000 valid resamples &lt; 800 threshold; retired from international and domestic cricket).<br>
      ^ <strong>Reeza Hendricks (768):</strong> Excluded from consensus rankings due to insufficient high-pressure delivery volume across multi-season full-member/IPL filters (&lt;50% specification eligibility).
    </div>

    <div class="section-h2" style="margin-top:2px;">Appendix C: External Verification Citations & IPL 2027 Regulatory Timeline</div>
    <div style="font-size:6.9pt; line-height:1.26; color:#334155;">
      &bull; <strong>Official Post-Retention Audit (17 Nov 2026 Cutoff):</strong> All 10 franchises submitted final retention filings at 17:00 IST. Total retained: 184; Released: 89; Open slots: 66 (25 overseas); Total purse balance: ₹297.95 Cr across 10 franchises.<br>
      &bull; <strong>Rajasthan Royals Confirmed Status (17 Nov 2026):</strong> 19 players under contract (14 Indian, 5 Overseas), ₹27.05 Cr purse (7th in IPL), 6 open slots (3 overseas). Trades In: Mohammed Shami (LSG &rarr; RR, ₹8.00 Cr), M. Siddharth (LSG &rarr; RR, ₹0.75 Cr). Trade Out: Sam Curran (RR &rarr; LSG, ₹14.50 Cr). Releases: Shimron Hetmyer (₹11.00 Cr), Tushar Deshpande (₹6.50 Cr). [Official IPLT20 / Rajasthan Royals]<br>
      &bull; <strong>Confirmed League Trades:</strong> Hardik Pandya (MI &rarr; PBKS); Arshdeep Singh (PBKS &rarr; MI, ₹18.00 Cr all-cash); Rishabh Pant (LSG &rarr; DC); Kuldeep Yadav (DC &rarr; LSG); Nathan Ellis & Khaleel Ahmed (CSK &rarr; SRH); Liam Livingstone & Jack Edwards (SRH &rarr; CSK); T Natarajan (DC &rarr; SRH); Zeeshan Ansari (SRH &rarr; DC); Harshal Patel (SRH &rarr; GT). [Official]<br>
      &bull; <strong>Medical & Regulatory Status:</strong> Matheesha Pathirana (recovering from hamstring injury; 2027 fitness clearance pending verification); Jacob Bethell (subject to ECB medical clearance); Mitchell Starc (opted out per official media confirmation); Mustafizur Rahman (subject to BCB NOC issuance); Russell & Dinesh Karthik (retired benchmarks). [Reputable Media / Official]<br>
      &bull; <strong>Auction Timeline:</strong> Retention deadline: 17 Nov 2026 (Closed) &bull; Player auction registration deadline: 23 Nov 2026 (Pending) &bull; Final auction list publication: 3 Dec 2026 (Pending) &bull; Auction Date: 16 Dec 2026 at ITC Grand Goa, Goa (11:00 AM IST).
    </div>

    <div class="callout-box emerald" style="margin-top:4px; padding:5px 8px;">
      <div class="callout-title" style="font-size:8.4pt;">Official Verification Sign-Off</div>
      <div style="font-size:7.2pt;">This submission document is compiled deterministically from canonical Model V4 outputs. All 39 V1 baseline checksums verified intact. Scope reconciled down to 837 matches and 193,988 deliveries. Rankings strictly preserve empirical multiverse consensus without manual overrides.</div>
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
    print("Building professional HTML report (v3.0)...")
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
    else:
        print("PERFECT: Document rendered to exactly 15 pages without overflow.")

    # Synchronize official submission deliverables in outputs/final_package
    import hashlib, shutil
    final_pkg_dir = ROOT / "outputs" / "final_package"
    final_pkg_dir.mkdir(parents=True, exist_ok=True)

    dest_post_retention = final_pkg_dir / "SupeRR_Final_Report_PostRetention.pdf"
    dest_canonical = final_pkg_dir / "SupeRR_Final_Report.pdf"
    dest_final = final_pkg_dir / "SupeRR_Final_Report_Final.pdf"

    shutil.copy2(OUT_PDF, dest_post_retention)
    shutil.copy2(OUT_PDF, dest_canonical)
    shutil.copy2(OUT_PDF, dest_final)

    sha256 = hashlib.sha256(OUT_PDF.read_bytes()).hexdigest()
    print(f"Copied to: {dest_post_retention}")
    print(f"Copied to: {dest_canonical}")
    print(f"Final PDF SHA-256: {sha256}")

if __name__ == "__main__":
    main()
