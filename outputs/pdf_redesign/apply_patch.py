import re

with open('outputs/pdf_redesign/generate_professional_report.py', 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Add specific page CSS before the closing style tag
p1_css = """
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

text = text.replace('  p {\n    margin: 0 0 4px 0;\n  }', '  p {\n    margin: 0 0 4px 0;\n  }\n' + p1_css)

# 2. Add governance card on Page 6
p6_old = 'guaranteeing zero look-ahead contamination.</p>\n  </div>\n\n  <div class="page-footer">'
p6_new = '''guaranteeing zero look-ahead contamination.</p>

    <div class="card card-tint" style="padding:10px 14px; margin-top:8px; border-left:3.5px solid #004BA0;">
      <div class="formula-title" style="color:#004BA0; font-size:9.2pt;">Multiverse Robustness Governance Guarantee</div>
      <p style="font-size:8.4pt; margin:0; line-height:1.40;">By systematically evaluating candidates across 15,150 model specifications rather than a single hand-crafted metric, researcher bias and parameter cherry-picking are entirely eliminated. Any player appearing in the consensus top 10 is mathematically proven to withstand extreme sensitivity perturbations across leverage thresholds, scoring formulations, and wicket valuations.</p>
    </div>
  </div>

  <div class="page-footer">'''
text = text.replace(p6_old, p6_new)

# 3. Add Scenario C on Page 14
p14_old = 'balance the starting XI.</p>\n      </div>\n    </div>\n  </div>\n\n  <div class="page-footer">'
p14_new = '''balance the starting XI.</p>
      </div>
    </div>

    <div class="callout-box gold" style="padding:10px 13px; margin-top:8px;">
      <div class="callout-title" style="font-size:9.4pt;">Scenario C &bull; Dynamic Impact Player Flexibility</div>
      <p style="font-size:8.3pt; margin:0; line-height:1.40;">Leverage the IPL Impact Player rule to pair defensive spin specialists like <strong>Krunal Pandya</strong> (Rank 11) or <strong>Varun Chakravarthy</strong> (Rank 13) with death-overs batting accelerators like <strong>Ashutosh Sharma</strong> (Rank 11), optimizing phase-by-phase resource allocation according to pitch par.</p>
    </div>
  </div>

  <div class="page-footer">'''
text = text.replace(p14_old, p14_new)

with open('outputs/pdf_redesign/generate_professional_report.py', 'w', encoding='utf-8') as f:
    f.write(text)

print('Updated generate_professional_report.py successfully.')
