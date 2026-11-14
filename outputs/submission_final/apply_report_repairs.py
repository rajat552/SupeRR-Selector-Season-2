"""
Script to apply precise report repairs to outputs/submission_final/compile_final_report.py
and outputs/submission_final/SupeRR_Final_Report.md
"""

from pathlib import Path

compile_script_path = Path("outputs/submission_final/compile_final_report.py")
text = compile_script_path.read_text(encoding="utf-8")

# 1. Page numbering convention: "Page " counter(page) " of 15"
text = text.replace('content: "Page " counter(page) " of 14";', 'content: "Page " counter(page) " of 15";')

# 2. Page 3 table & takeaway:
old_page3 = """  <div class="section-heading">2. Empirical Pressure Separation: High Pressure vs. Normal Outcomes</div>
  <p>Does the pressure definition separate high-pressure states from normal situations? League-wide outcome rates were computed across 185,692 legal deliveries with 95% confidence intervals clustered by match (outputs/data_audit/pressure_validation.csv):</p>

  <div class="grid-2" style="align-items:center;">
    <div style="flex:1.2;">
      <table style="font-size:6.8pt;">
        <thead>
          <tr>
            <th style="text-align:left;">Role & Metric</th>
            <th>Normal (P &lt; 0.35)</th>
            <th>High Pressure (P &ge; 0.50)</th>
            <th>Net Diff</th>
            <th>Change</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td style="text-align:left;"><strong>Batter: Dismissal Prob</strong></td>
            <td>0.0470 [0.046, 0.048]</td>
            <td><strong>0.0585</strong> [0.057, 0.060]</td>
            <td>+0.0115</td>
            <td><strong style="color:#B91C1C;">+24.4%</strong></td>
          </tr>
          <tr>
            <td style="text-align:left;"><strong>Batter: Dot Ball Rate</strong></td>
            <td>35.3% [34.8%, 35.7%]</td>
            <td><strong>35.9%</strong> [35.3%, 36.6%]</td>
            <td>+0.6%</td>
            <td>+1.9%</td>
          </tr>
          <tr>
            <td style="text-align:left;"><strong>Batter: Boundary Rate</strong></td>
            <td>19.1% [18.8%, 19.5%]</td>
            <td><strong>16.4%</strong> [15.9%, 16.8%]</td>
            <td>-2.7%</td>
            <td>-14.4%</td>
          </tr>
          <tr>
            <td style="text-align:left;"><strong>Batter: Runs per Ball</strong></td>
            <td>1.382 [1.366, 1.399]</td>
            <td><strong>1.288</strong> [1.267, 1.309]</td>
            <td>-0.094</td>
            <td>-6.8%</td>
          </tr>
          <tr>
            <td style="text-align:left;"><strong>Bowler: Runs Conceded/Ball</strong></td>
            <td>1.351 [1.335, 1.368]</td>
            <td><strong>1.502</strong> [1.480, 1.524]</td>
            <td>+0.151</td>
            <td>+11.1%</td>
          </tr>
          <tr>
            <td style="text-align:left;"><strong>Bowler: Dot Ball Rate</strong></td>
            <td>38.0% [37.6%, 38.5%]</td>
            <td><strong>29.0%</strong> [28.4%, 29.5%]</td>
            <td>-9.0%</td>
            <td>-23.9%</td>
          </tr>
        </tbody>
      </table>
    </div>
    <div style="flex:1.1; text-align:center;">
      <img src="{uri_audit_chart('hp_vs_normal_outcomes.png')}" style="width:100%; max-height:185px; object-fit:contain; border:1px solid #CBD5E1; border-radius:4px;">
    </div>
  </div>

  <div class="callout-box" style="margin-top:4px;">
    <strong>Key Validation Takeaway:</strong> Under high pressure, batting dismissal hazard increases by <strong>+24.4%</strong> ($p < 0.001$) while boundary production drops by <strong>-14.4%</strong>, reflecting bowling discipline and defensive field settings. This confirms that the canonical sigmoid formulation cleanly isolates genuine high-leverage cricket conditions.
  </div>"""

new_page3 = """  <div class="section-heading">2. Empirical Pressure Separation: High Pressure vs. Normal Outcomes</div>
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
  </div>"""

assert old_page3 in text, "old_page3 block not found"
text = text.replace(old_page3, new_page3)

# 3. Scope terminology for comp 2670 and 3289:
# On Page 2:
old_scope_p2 = "secondary non-elite tournaments (Other_T20 comp IDs 2670 and 3289, comprising 30 matches and 6,985 deliveries)"
new_scope_p2 = "secondary A-team / emerging representative tournaments (Mens T20 Emerging Teams Asia Cup 2024 [comp ID 2670] and Asia Cup Rising Stars 2025 [comp ID 3289], comprising 30 matches and 6,985 deliveries, which are separately excluded from the primary analytical scope)"
assert old_scope_p2 in text, "old_scope_p2 not found"
text = text.replace(old_scope_p2, new_scope_p2)

# On Page 3 (table & text):
old_scope_p3_text = "Non-primary domestic competitions (comp IDs 2670 and 3289: 30 matches, 6,985 deliveries)"
new_scope_p3_text = "Secondary A-team / emerging representative tournaments (comp IDs 2670 and 3289: Mens T20 Emerging Teams Asia Cup 2024 and Asia Cup Rising Stars 2025; 30 matches, 6,985 deliveries, separately excluded from primary scope)"
assert old_scope_p3_text in text, "old_scope_p3_text not found"
text = text.replace(old_scope_p3_text, new_scope_p3_text)

old_scope_p3_row = """      <tr>
        <td style="text-align:left;">(-) Secondary Comps (Comp IDs 2670, 3289)</td>
        <td>-30</td>
        <td>-6,985</td>
        <td>-6,730</td>
        <td style="text-align:left;">Excluded domestic tournaments; non-IPL / non-T20I.</td>
      </tr>"""
new_scope_p3_row = """      <tr>
        <td style="text-align:left;">(-) Emerging Tournaments (Comp IDs 2670, 3289)</td>
        <td>-30</td>
        <td>-6,985</td>
        <td>-6,730</td>
        <td style="text-align:left;">Emerging/A-team tournaments (Mens Emerging Teams Asia Cup, Rising Stars); non-primary scope.</td>
      </tr>"""
assert old_scope_p3_row in text, "old_scope_p3_row not found"
text = text.replace(old_scope_p3_row, new_scope_p3_row)

# 4. Wording corrections:
# "cleanly isolates" -> "separates"
text = text.replace("cleanly isolates", "separates")

# "almost certainly be retained" -> "likely to be retained"
text = text.replace("almost certainly be retained", "likely to be retained")

# Avoid repetitive "if available at auction" in line 1054
old_summary_auction = "RR's practical recruitment focus must concentrate on actionable high-ceiling players who could address these needs, if available at auction: Shashank Singh and Naman Dhir, if available at auction, to partner Ferreira in death batting, and Nathan Ellis and Eshan Malinga, if available at auction, to provide dependable death overs."
new_summary_auction = "RR's practical recruitment focus must concentrate on actionable high-ceiling players who could address these needs, if available at auction: Shashank Singh and Naman Dhir to partner Ferreira in death batting, and Nathan Ellis and Eshan Malinga to provide dependable death overs."
assert old_summary_auction in text, "old_summary_auction not found"
text = text.replace(old_summary_auction, new_summary_auction)

# 5. Author Information:
# Update byline / title
text = text.replace(
    '<div class="doc-subtitle">Submission by Rajat Aggarwal, SupeRR Selector Season 2, Round 1</div>',
    '<div class="doc-subtitle">Submission by Rajat Aggarwal | Participant — SupeRR Selector Season 2 (Round 1)</div>'
)
text = text.replace(
    '<span>Submission by Rajat Aggarwal, SupeRR Selector Season 2, Round 1.</span>',
    '<span>Rajat Aggarwal | Participant — SupeRR Selector Season 2</span>'
)
text = text.replace(
    '<span>Submission by Rajat Aggarwal, SupeRR Selector Season 2, Round 1</span>',
    '<span>Rajat Aggarwal | Participant — SupeRR Selector Season 2</span>'
)

# 6. Page 6 / 7 ANOVA consistency & chart alignment:
old_anova_text = """  <p>Across 15,150 specifications per role, top-ranked candidates consistently demonstrate high inclusion frequency. To understand ranking variance rigorously, I conducted a sequential (Type I) ANOVA on percentile ranks ($y_{{i,s}} = {{rank}}_{{i,s}} / n_{{{{eligible}}, s}}$).</p>

  <div class="sub-heading">Sequential (Type I) ANOVA Variance Decomposition on Percentile Ranks</div>"""

new_anova_text = """  <p>Across 15,150 specifications per role, top-ranked candidates consistently demonstrate high inclusion frequency. To understand ranking variance rigorously, I conducted a sequential (Type I) ANOVA on percentile ranks (y<sub>i,s</sub> = rank<sub>i,s</sub> / n<sub>eligible,s</sub>). Sequential (Type I) decomposition is order-dependent; the percentages reflect hierarchical explanatory contributions rather than uniquely isolated causal intrinsic-talent shares.</p>

  <div class="sub-heading">Sequential (Type I) ANOVA Variance Decomposition on Percentile Ranks</div>"""

assert old_anova_text in text, "old_anova_text not found"
text = text.replace(old_anova_text, new_anova_text)

# Point chart to the aligned figure outputs/submission_final/charts/fig1_variance_decomposition_aligned.png
old_chart_tag = """<img class="chart-img" style="max-height:160px;" src="{uri_chart('fig1_variance_decomposition.png')}" alt="ANOVA Variance Decomposition">"""
new_chart_tag = """<img class="chart-img" style="max-height:160px;" src="{(ROOT / 'outputs' / 'submission_final' / 'charts' / 'fig1_variance_decomposition_aligned.png').as_uri()}" alt="Sequential Type I ANOVA Variance Decomposition">"""
assert old_chart_tag in text, "old_chart_tag not found"
text = text.replace(old_chart_tag, new_chart_tag)

# 7. Mathematical Typography Cleanup across all pages:
# Page 4: math boxes
old_mb_bat1 = '<div class="math-box">PI_/bat, 1 = 0.50 S_/collapse + 0.30 S_/crr + 0.20 S_/death</div>'
new_mb_bat1 = '<div class="math-box">PI<sub>bat, 1</sub> = 0.50 &middot; S<sub>collapse</sub> + 0.30 &middot; S<sub>crr</sub> + 0.20 &middot; S<sub>death</sub></div>'
assert old_mb_bat1 in text, "old_mb_bat1 not found"
text = text.replace(old_mb_bat1, new_mb_bat1)

old_collapse_desc = "where $S_{{{{collapse}}}}$ measures wickets lost relative to par. In the second innings, chase urgency and boundary deficits govern leverage:"
new_collapse_desc = "where S<sub>collapse</sub> measures wickets lost relative to par. In the second innings, chase urgency and boundary deficits govern leverage:"
assert old_collapse_desc in text, "old_collapse_desc not found"
text = text.replace(old_collapse_desc, new_collapse_desc)

old_mb_bat2 = '<div class="math-box">PI_/bat, 2 = 0.50 S_/rrr + 0.30 S_/wkts + 0.20 S_urgency + /boost_/close</div>'
new_mb_bat2 = '<div class="math-box">PI<sub>bat, 2</sub> = 0.50 &middot; S<sub>rrr</sub> + 0.30 &middot; S<sub>wkts</sub> + 0.20 &middot; S<sub>urgency</sub> + Boost<sub>close</sub></div>'
assert old_mb_bat2 in text, "old_mb_bat2 not found"
text = text.replace(old_mb_bat2, new_mb_bat2)

old_sig_desc = "Continuous delivery weights are evaluated via logistic sigmoid centered at $x_0 = 0.425$ with slope $k = 12.5$ (scale $s = 0.08$):"
new_sig_desc = "Continuous delivery weights are evaluated via logistic sigmoid centered at x<sub>0</sub> = 0.425 with slope k = 12.5 (scale s = 0.08):"
assert old_sig_desc in text, "old_sig_desc not found"
text = text.replace(old_sig_desc, new_sig_desc)

old_mb_sig = '<div class="math-box">w_k = /11 + e^-12.5(PI_k - 0.425) = /11 + e^-(PI_k - 0.425)/0.08</p></div>'
new_mb_sig = '<div class="math-box">w<sub>k</sub> = 1 / [1 + e<sup>-12.5 &middot; (PI<sub>k</sub> - 0.425)</sup>] = 1 / [1 + e<sup>-(PI<sub>k</sub> - 0.425) / 0.08</sup>]</div>'
assert old_mb_sig in text, "old_mb_sig not found"
text = text.replace(old_mb_sig, new_mb_sig)

old_mb_bowl = '<div class="math-box">PI_/bowl, 1 = /max(S_/death, S_/top) /times /damp_/collapse</div>'
new_mb_bowl = '<div class="math-box">PI<sub>bowl, 1</sub> = max(S<sub>death</sub>, S<sub>top</sub>) &times; Damp<sub>collapse</sub></div>'
assert old_mb_bowl in text, "old_mb_bowl not found"
text = text.replace(old_mb_bowl, new_mb_bowl)

# Worked examples math cleanup:
old_we1 = "Continuous pressure index $PI_{{{{bat}}}} = 0.8648$. Sigmoid weight $w_k = 0.9959$. Shashank strikes a 6. LPO context baseline: expected runs 1.1087, expected dismissal 0.0396. Net impact: $+4.8913$ runs above expected $+ 0.2379$ dismissal avoidance ($V=6.0$) = <strong>+5.1292 runs</strong>, weighted at 0.9959 into his high-pressure sample."
new_we1 = "Continuous pressure index PI<sub>bat</sub> = 0.8648. Sigmoid weight w<sub>k</sub> = 0.9959. Shashank strikes a 6. LPO context baseline: expected runs 1.1087, expected dismissal 0.0396. Net impact: +4.8913 runs above expected + 0.2379 dismissal avoidance (V = 6.0) = <strong>+5.1292 runs</strong>, weighted at 0.9959 into his high-pressure sample."
assert old_we1 in text, "old_we1 not found"
text = text.replace(old_we1, new_we1)

old_we2 = "Bowler Jasprit Bumrah (ID 2933) bowls to Shubman Gill (ID 6288). Defending pressure index $PI_{{{{bowl}}}} = 0.7958$, sigmoid weight $w_k = 0.9904$. Bumrah dismisses Gill <strong>Bowled</strong>, conceding 0 runs. LPO baseline: expected runs conceded 1.6681, expected wicket 0.0489. Net impact: $+1.6681$ runs saved $+ 5.7064$ wicket value ($V=6.0$) = <strong>+7.3745 runs</strong> created/saved, weighted at 0.9904 into Bumrah's defending ledger."
new_we2 = "Bowler Jasprit Bumrah (ID 2933) bowls to Shubman Gill (ID 6288). Defending pressure index PI<sub>bowl</sub> = 0.7958, sigmoid weight w<sub>k</sub> = 0.9904. Bumrah dismisses Gill <strong>Bowled</strong>, conceding 0 runs. LPO baseline: expected runs conceded 1.6681, expected wicket 0.0489. Net impact: +1.6681 runs saved + 5.7064 wicket value (V = 6.0) = <strong>+7.3745 runs</strong> created/saved, weighted at 0.9904 into Bumrah's defending ledger."
assert old_we2 in text, "old_we2 not found"
text = text.replace(old_we2, new_we2)

old_fn_p4 = "<span>Zero look-ahead: all state variables evaluated strictly at $t - 1$ pre-ball release.</span>"
new_fn_p4 = "<span>Zero look-ahead: all state variables evaluated strictly at t - 1 pre-ball release.</span>"
assert old_fn_p4 in text, "old_fn_p4 not found"
text = text.replace(old_fn_p4, new_fn_p4)

# Page 5: math boxes & text
old_p5_lpo = '<p>For player $i$ on delivery $k$ in match state cell $c$, player $i$\'s own historical contributions are strictly subtracted to eliminate self-leakage:\n      <div class="math-box">/hat/mu_-i, c = //sum_j /ne i, j /in c y_j/sum_j /ne i, j /in c n_j</div>'
new_p5_lpo = '<p>For player i on delivery k in match state cell c, player i\'s own historical contributions are strictly subtracted to eliminate self-leakage:\n      <div class="math-box">&mu;&#770;<sub>-i, c</sub> = (&sum;<sub>j &ne; i, j &isin; c</sub> y<sub>j</sub>) / (&sum;<sub>j &ne; i, j &isin; c</sub> n<sub>j</sub>)</div>'
assert old_p5_lpo in text, "old_p5_lpo not found"
text = text.replace(old_p5_lpo, new_p5_lpo)

old_wkt_desc = "The non-overlapping context-marginal empirical estimate (**7.82 runs**) is evaluated across the multiverse as a sensitivity variant."
new_wkt_desc = "The non-overlapping context-marginal empirical estimate (7.82 runs) is evaluated across the multiverse as a sensitivity variant."
assert old_wkt_desc in text, "old_wkt_desc not found"
text = text.replace(old_wkt_desc, new_wkt_desc)

old_eb_desc = "I applied Empirical Bayes shrinkage toward zero based on Kish's effective sample size $N_{{{{eff}}}} = (/sum w_k)^2 / /sum w_k^2$:\n      <div class=\"math-box\">/PWI_/shrunk = /N_/effN_/eff + 120 /cdot /PWI_/raw</div>"
new_eb_desc = "I applied Empirical Bayes shrinkage toward zero based on Kish's effective sample size N<sub>eff</sub> = (&sum; w<sub>k</sub>)<sup>2</sup> / &sum; w<sub>k</sub><sup>2</sup>:\n      <div class=\"math-box\">PWI<sub>shrunk</sub> = [N<sub>eff</sub> / (N<sub>eff</sub> + 120)] &middot; PWI<sub>raw</sub></div>"
assert old_eb_desc in text, "old_eb_desc not found"
text = text.replace(old_eb_desc, new_eb_desc)

old_mb_b = '<div class="math-box">/Score_/Model B = 0.50 /cdot z(/PWI_/shrunk) + 0.30 /cdot z(/MaintLift_/shrunk) + 0.20 /cdot z(/Consistency_/EB)</div>\n  where ${{MaintLift}} = {{PWI}}_{{{{shrunk}}}} - 0.35 /cdot /max({{Normal}}_{{{{shrunk}}}}, {{floor}})$. This properly balances absolute capability with baseline resilience.'
new_mb_b = '<div class="math-box">Score<sub>Model B</sub> = 0.50 &middot; z(PWI<sub>shrunk</sub>) + 0.30 &middot; z(MaintLift<sub>shrunk</sub>) + 0.20 &middot; z(Consistency<sub>EB</sub>)</div>\n  where MaintLift = PWI<sub>shrunk</sub> - 0.35 &middot; max(Normal<sub>shrunk</sub>, Floor). This properly balances absolute capability with baseline resilience.'
assert old_mb_b in text, "old_mb_b not found"
text = text.replace(old_mb_b, new_mb_b)

# Page 6: grid equation
old_mb_grid = '<div class="math-box">/Total Specifications = 30/,(P /times W /times F) /times [504/,(/Model A/B specs) + 1/,(/Model C spec)] = 15,150</div>'
new_mb_grid = '<div class="math-box">Total Specifications = 30 (P &times; W &times; F) &times; [504 (Model A/B specs) + 1 (Model C spec)] = 15,150</div>'
assert old_mb_grid in text, "old_mb_grid not found"
text = text.replace(old_mb_grid, new_mb_grid)

# Page 13: Walk forward correlations
old_wf_bat = "<strong>Canonical Batting Stability:</strong> Spearman $r = {0.0508}$ ($p = 0.7864$, uninformative out-of-sample across 31 common players)."
new_wf_bat = "<strong>Canonical Batting Stability:</strong> Spearman r = 0.0508 (p = 0.7864, uninformative out-of-sample across 31 common players)."
assert old_wf_bat in text, "old_wf_bat not found"
text = text.replace(old_wf_bat, new_wf_bat)

old_wf_bowl = "<strong>Canonical Bowling Stability:</strong> Spearman $r = {0.2646}$ ($p = 0.0721$, modest positive correlation across 47 common players)."
new_wf_bowl = "<strong>Canonical Bowling Stability:</strong> Spearman r = 0.2646 (p = 0.0721, modest positive correlation across 47 common players)."
assert old_wf_bowl in text, "old_wf_bowl not found"
text = text.replace(old_wf_bowl, new_wf_bowl)

old_wf_disc = "Bowling pressure performance demonstrates modest stability ($r = 0.26$), but still contains significant season-to-season variation."
new_wf_disc = "Bowling pressure performance demonstrates modest stability (r = 0.26), but still contains significant season-to-season variation."
assert old_wf_disc in text, "old_wf_disc not found"
text = text.replace(old_wf_disc, new_wf_disc)

compile_script_path.write_text(text, encoding="utf-8")
print("SUCCESS: Updated compile_final_report.py with all repairs.")
