# Page-by-Page Forensic Layout Audit: Before Optimization

**Audit Subject:** `outputs/final_package/SupeRR_Final_Report.pdf` (Original Layout)  
**Render Directory:** `outputs/pdf_redesign/before/page-01.png` to `page-15.png`  
**Contact Sheet:** `outputs/pdf_redesign/before/contact_sheet.png`  
**Image Canvas Resolution:** $1,190 \times 1,684\text{ px}$ (200 DPI equivalent)  
**Auditor:** Principal PDF Layout Specialist & Quality Assurance Engineer  

---

### Page 01 — Executive Summary & Dual Leaderboards
- **Total Usable Content Area:** $1,054 \times 1,484\text{ px}$ ($y = 120$ to $y = 1,604$).
- **Actual Content Bounding Box:** $x \in [68, 1,122]$, $y \in [120, 1,312]$ ($1,054 \times 1,192\text{ px}$).
- **Top Margin:** $68\text{ px}$ ($11.5\text{ mm}$); **Bottom Margin:** $80\text{ px}$ ($13.6\text{ mm}$).
- **Empty Vertical Space:** $292\text{ px}$ ($19.7\%$ unutilized).
- **Current Typography:** Title $13.5\text{pt}$, Body $7.2\text{pt}$, Table body $6.6\text{pt}$, Badges $5.6\text{pt}$.
- **Text Density:** Extremely dense in tables and callouts; text is legible but feels like micro-print.
- **Table Dimensions:** Table 1A & 1B each span $1,054\text{ px}$ width, height approx $160\text{ px}$ each (10 rows).
- **Image / Chart Dimensions:** No images on Page 1.
- **Header & Footer:** Masthead banner at top ($70\text{ px}$); running footer pinned at bottom ($y = 1,610$).
- **Overflow / Clipping:** None.
- **Visual Balance:** Good top-to-bottom distribution, but typography is undersized for a front-page executive brief. Tables deserve larger row height and font ($8.0\text{pt}–8.5\text{pt}$).

---

### Page 02 — Problem Understanding & Data Architecture
- **Total Usable Content Area:** $1,054 \times 1,484\text{ px}$.
- **Actual Content Bounding Box:** $x \in [68, 1,122]$, $y \in [120, 856]$ ($1,054 \times 736\text{ px}$).
- **Top Margin:** $68\text{ px}$; **Bottom Margin:** $80\text{ px}$.
- **Empty Vertical Space:** **$748\text{ px}$ ($50.4\%$ unutilized)** &mdash; bottom half is completely blank!
- **Current Typography:** Section H2 $8.8\text{pt}$, Card Titles $7.0\text{pt}$, Body copy $6.3\text{pt}$.
- **Text Density:** Artificially squashed into tiny cards with $4\text{px}$ padding.
- **Table Dimensions:** No tables on Page 2.
- **Image / Chart Dimensions:** No charts on Page 2.
- **Header & Footer:** Section header at top ($y = 70$); footer stranded at bottom ($y = 1,610$).
- **Overflow / Clipping:** None.
- **Visual Balance: SEVERELY DEFECTIVE.** Looks like an unfinished draft where content ends at mid-page. Needs generous card expansions, larger body text ($9.5\text{pt}$), larger headings ($14\text{pt}$), and a prominent architecture infographic box.

---

### Page 03 — Data Quality Audit & Empirical Pressure Validation
- **Total Usable Content Area:** $1,054 \times 1,484\text{ px}$.
- **Actual Content Bounding Box:** $x \in [68, 1,122]$, $y \in [120, 1,162]$ ($1,054 \times 1,042\text{ px}$).
- **Top Margin:** $68\text{ px}$; **Bottom Margin:** $80\text{ px}$.
- **Empty Vertical Space:** $442\text{ px}$ ($29.8\%$ unutilized).
- **Current Typography:** Table text $6.6\text{pt}$, Waterfall text $8.8\text{pt}$ numbers / $5.4\text{pt}$ labels, Body $7.2\text{pt}$.
- **Text Density:** Moderate; table rows are somewhat thin.
- **Table Dimensions:** Data scope table $1,054 \times 110\text{ px}$; outcome separation table $1,054 \times 140\text{ px}$.
- **Image / Chart Dimensions:** Two charts side-by-side clamped at $190\text{ px}$ height ($510 \times 190\text{ px}$ each).
- **Header & Footer:** Section header at top; running footer at bottom.
- **Overflow / Clipping:** None.
- **Visual Balance:** Passable, but charts are small and hard to inspect; tables can easily expand vertically with $9.0\text{pt}$ typography and $240\text{ px}$ charts.

---

### Page 04 — Pressure Mechanics & Mathematical Formulations
- **Total Usable Content Area:** $1,054 \times 1,484\text{ px}$.
- **Actual Content Bounding Box:** $x \in [68, 1,122]$, $y \in [120, 812]$ ($1,054 \times 686\text{ px}$).
- **Top Margin:** $68\text{ px}$; **Bottom Margin:** $80\text{ px}$.
- **Empty Vertical Space:** **$792\text{ px}$ ($53.8\%$ unutilized)** &mdash; content terminates at $48\%$ of usable height!
- **Current Typography:** H2 $8.8\text{pt}$, Math font $8.6\text{pt}$, Worked examples body $6.3\text{pt}$.
- **Text Density:** Extremely cramped into miniature formula cards.
- **Table Dimensions:** None.
- **Image / Chart Dimensions:** None.
- **Header & Footer:** Header at top; footer stranded with $792\text{ px}$ of white space above it.
- **Overflow / Clipping:** None.
- **Visual Balance: SEVERELY DEFECTIVE.** Mathematical equations look tiny and inconsequential. Needs large display math boxes ($12\text{pt}$ math fonts), full parameter breakdown tables, and expanded worked example dossiers.

---

### Page 05 — Performance Measurement Framework & Baselines
- **Total Usable Content Area:** $1,054 \times 1,484\text{ px}$.
- **Actual Content Bounding Box:** $x \in [68, 1,122]$, $y \in [120, 823]$ ($1,054 \times 703\text{ px}$).
- **Top Margin:** $68\text{ px}$; **Bottom Margin:** $80\text{ px}$.
- **Empty Vertical Space:** **$781\text{ px}$ ($52.6\%$ unutilized)** &mdash; bottom half completely empty.
- **Current Typography:** Formulas $8.6\text{pt}$, Model cards $6.1\text{pt}$, Body $7.2\text{pt}$.
- **Text Density:** Compressed cards; tiny equations.
- **Table Dimensions:** None.
- **Image / Chart Dimensions:** None.
- **Header & Footer:** Standard running header and footer.
- **Overflow / Clipping:** None.
- **Visual Balance: SEVERELY DEFECTIVE.** The core statistical framework (LPO baselines, Dirichlet shrinkage, Wicket valuation) is compressed into a tiny zone. Must expand with detailed formula displays and structured 3-model comparative cards.

---

### Page 06 — Fair Comparisons & Multiverse Specification Grid
- **Total Usable Content Area:** $1,054 \times 1,484\text{ px}$.
- **Actual Content Bounding Box:** $x \in [68, 1,122]$, $y \in [120, 740]$ ($1,054 \times 614\text{ px}$).
- **Top Margin:** $68\text{ px}$; **Bottom Margin:** $80\text{ px}$.
- **Empty Vertical Space:** **$864\text{ px}$ ($58.6\%$ unutilized)** &mdash; nearly $60\%$ of the page is empty!
- **Current Typography:** Table body $6.6\text{pt}$, Card body $6.3\text{pt}$.
- **Text Density:** 8-dimension table has tiny row heights ($22\text{ px}$ per row).
- **Table Dimensions:** $1,054 \times 195\text{ px}$.
- **Image / Chart Dimensions:** None.
- **Header & Footer:** Standard header and footer.
- **Overflow / Clipping:** None.
- **Visual Balance: SEVERELY DEFECTIVE.** The central methodological centerpiece (the 15,150-specification multiverse) looks miniature and sparse. Needs generous table row padding, dimension level pills, and expanded sample gating containers.

---

### Page 07 — ANOVA Variance Decomposition & Curves
- **Total Usable Content Area:** $1,054 \times 1,484\text{ px}$.
- **Actual Content Bounding Box:** $x \in [68, 1,122]$, $y \in [120, 904]$ ($1,054 \times 784\text{ px}$).
- **Top Margin:** $68\text{ px}$; **Bottom Margin:** $80\text{ px}$.
- **Empty Vertical Space:** **$700\text{ px}$ ($47.2\%$ unutilized)**.
- **Current Typography:** Table font $6.6\text{pt}$, Callout body $6.3\text{pt}$.
- **Text Density:** Moderate.
- **Table Dimensions:** $1,054 \times 145\text{ px}$.
- **Image / Chart Dimensions:** Figure 2 clamped at $190\text{ px}$ height ($700 \times 190\text{ px}$).
- **Header & Footer:** Standard running header and footer.
- **Overflow / Clipping:** None.
- **Visual Balance: DEFECTIVE.** Figure 2 (ANOVA Variance Decomposition) is one of the most important charts in the submission; it is cramped at $190\text{ px}$. Expanding Figure 2 to $380\text{ px}$ height and enlarging table row height will fill the page with perfect visual elegance.

---

### Page 08 — Consensus Batters: Full Table & Profiles 1–5
- **Total Usable Content Area:** $1,054 \times 1,484\text{ px}$.
- **Actual Content Bounding Box:** $x \in [68, 1,122]$, $y \in [120, 1,094]$ ($1,054 \times 968\text{ px}$).
- **Top Margin:** $68\text{ px}$; **Bottom Margin:** $80\text{ px}$.
- **Empty Vertical Space:** $510\text{ px}$ ($34.8\%$ unutilized).
- **Current Typography:** Table 2A body $6.4\text{pt}$, Profile names $7.6\text{pt}$, Metrics $6.0\text{pt}$, Dossier prose $6.5\text{pt}$.
- **Text Density:** Dense in table, compact in dossiers.
- **Table Dimensions:** Table 2A spans $1,054 \times 210\text{ px}$.
- **Image / Chart Dimensions:** None.
- **Header & Footer:** Standard header and footer.
- **Overflow / Clipping:** None.
- **Visual Balance:** Reasonable, but profile cards 1–5 (Shashank, David, Dhir, Karthik, Klaasen) feel squashed into the lower half. Expanding dossier padding, metric badge fonts, and table cell heights will achieve a full 85% fill.

---

### Page 09 — Batters 6–10 Profiles & Resilience Landscape
- **Total Usable Content Area:** $1,054 \times 1,484\text{ px}$.
- **Actual Content Bounding Box:** $x \in [68, 1,122]$, $y \in [120, 970]$ ($1,054 \times 844\text{ px}$).
- **Top Margin:** $68\text{ px}$; **Bottom Margin:** $80\text{ px}$.
- **Empty Vertical Space:** **$634\text{ px}$ ($43.1\%$ unutilized)**.
- **Current Typography:** Profile names $7.6\text{pt}$, Metrics $6.0\text{pt}$, Prose $6.5\text{pt}$.
- **Text Density:** Moderately sparse; bottom area below Figure 3 is empty.
- **Table Dimensions:** None.
- **Image / Chart Dimensions:** Figure 3 clamped at $190\text{ px}$ height.
- **Header & Footer:** Standard header and footer.
- **Overflow / Clipping:** None.
- **Visual Balance: DEFECTIVE.** Figure 3 (Maintenance vs Lift) is tiny and difficult to read. Expanding Figure 3 to $360\text{ px}$ height and enlarging dossier typography transforms this into an editorial spread.

---

### Page 10 — Consensus Bowlers: Full Table & Profiles 1–5
- **Total Usable Content Area:** $1,054 \times 1,484\text{ px}$.
- **Actual Content Bounding Box:** $x \in [68, 1,122]$, $y \in [120, 1,027]$ ($1,054 \times 901\text{ px}$).
- **Top Margin:** $68\text{ px}$; **Bottom Margin:** $80\text{ px}$.
- **Empty Vertical Space:** **$577\text{ px}$ ($39.3\%$ unutilized)**.
- **Current Typography:** Table 2B body $6.4\text{pt}$, Profile names $7.6\text{pt}$, Metrics $6.0\text{pt}$, Prose $6.5\text{pt}$.
- **Text Density:** Similar to Page 8.
- **Table Dimensions:** Table 2B spans $1,054 \times 210\text{ px}$.
- **Image / Chart Dimensions:** None.
- **Header & Footer:** Standard header and footer.
- **Overflow / Clipping:** None.
- **Visual Balance:** Table 2B and profiles 1–5 (Narine, Bumrah, Rashid, Pathirana, E. Malinga) need larger metric pills, more vertical breathing room, and $8.2\text{pt}$ table font.

---

### Page 11 — Bowlers 6–10 Profiles & Resilience Landscape
- **Total Usable Content Area:** $1,054 \times 1,484\text{ px}$.
- **Actual Content Bounding Box:** $x \in [68, 1,122]$, $y \in [120, 935]$ ($1,054 \times 809\text{ px}$).
- **Top Margin:** $68\text{ px}$; **Bottom Margin:** $80\text{ px}$.
- **Empty Vertical Space:** **$669\text{ px}$ ($45.5\%$ unutilized)**.
- **Current Typography:** Profile names $7.6\text{pt}$, Metrics $6.0\text{pt}$, Prose $6.5\text{pt}$.
- **Text Density:** Sparse below Figure 4.
- **Table Dimensions:** None.
- **Image / Chart Dimensions:** Figure 4 clamped at $190\text{ px}$ height.
- **Header & Footer:** Standard header and footer.
- **Overflow / Clipping:** None.
- **Visual Balance: DEFECTIVE.** Same issue as Page 9. Figure 4 must be enlarged to $360\text{ px}$, and profile dossiers for Ellis, Noor, Arshdeep, Prasidh, Bhuvneshwar expanded.

---

### Page 12 — Rajasthan Royals 2026 Squad Audit
- **Total Usable Content Area:** $1,054 \times 1,484\text{ px}$.
- **Actual Content Bounding Box:** $x \in [68, 1,122]$, $y \in [120, 679]$ ($1,054 \times 559\text{ px}$).
- **Top Margin:** $68\text{ px}$; **Bottom Margin:** $80\text{ px}$.
- **Empty Vertical Space:** **$925\text{ px}$ ($62.3\%$ unutilized)** &mdash; content takes barely $37.7\%$ of usable height!
- **Current Typography:** Table font $6.6\text{pt}$, Callout prose $6.3\text{pt}$.
- **Text Density:** Microscopic; completely stranded at top of page.
- **Table Dimensions:** RR squad table spans $1,054 \times 170\text{ px}$.
- **Image / Chart Dimensions:** None.
- **Header & Footer:** Standard header and footer.
- **Overflow / Clipping:** None.
- **Visual Balance: SEVERELY DEFECTIVE.** The franchise recruitment recommendations look like an afterthought. Expanding the RR squad audit table, increasing font to $8.8\text{pt}$, and designing generous, executive recruitment strategy cards will utilize 82% of the page.

---

### Page 13 — Model Reliability, Limitations & Walk-Forward
- **Total Usable Content Area:** $1,054 \times 1,484\text{ px}$.
- **Actual Content Bounding Box:** $x \in [68, 1,122]$, $y \in [120, 787]$ ($1,054 \times 667\text{ px}$).
- **Top Margin:** $68\text{ px}$; **Bottom Margin:** $80\text{ px}$.
- **Empty Vertical Space:** **$817\text{ px}$ ($55.1\%$ unutilized)**.
- **Current Typography:** Callout body $6.2\text{pt}$, Table $6.6\text{pt}$.
- **Text Density:** Sparse.
- **Table Dimensions:** Excluded candidates table spans $1,054 \times 85\text{ px}$.
- **Image / Chart Dimensions:** Figures 5A & 5B clamped at $190\text{ px}$ height.
- **Header & Footer:** Standard header and footer.
- **Overflow / Clipping:** None.
- **Visual Balance: SEVERELY DEFECTIVE.** Out-of-sample validation and bootstrap intervals are critical findings. Figures 5A & 5B must be expanded to $280\text{ px}$ height, and stability callouts given proper editorial dignity.

---

### Page 14 — Players Next in Line (Ranks 11–15) & Contingency Targets
- **Total Usable Content Area:** $1,054 \times 1,484\text{ px}$.
- **Actual Content Bounding Box:** $x \in [68, 1,122]$, $y \in [120, 610]$ ($1,054 \times 490\text{ px}$).
- **Top Margin:** $68\text{ px}$; **Bottom Margin:** $80\text{ px}$.
- **Empty Vertical Space:** **$994\text{ px}$ ($67.0\%$ unutilized)** &mdash; **THE WORST PAGE IN THE REPORT!**
- **Current Typography:** Table font $6.6\text{pt}$, Callout prose $6.3\text{pt}$.
- **Text Density:** Barely occupies $33\%$ of the page.
- **Table Dimensions:** Two 5-row tables, each $1,054 \times 115\text{ px}$.
- **Image / Chart Dimensions:** None.
- **Header & Footer:** Standard header and footer.
- **Overflow / Clipping:** None.
- **Visual Balance: CATASTROPHICALLY EMPTY.** Two tiny tables floating at the very top. Needs full-width depth charts with generous padding, player role badges, and detailed contingency scenarios.

---

### Page 15 — Appendix: Baseline Lists, Governance & Reproducibility
- **Total Usable Content Area:** $1,054 \times 1,484\text{ px}$.
- **Actual Content Bounding Box:** $x \in [68, 1,122]$, $y \in [120, 865]$ ($1,054 \times 745\text{ px}$).
- **Top Margin:** $68\text{ px}$; **Bottom Margin:** $80\text{ px}$.
- **Empty Vertical Space:** **$739\text{ px}$ ($49.8\%$ unutilized)**.
- **Current Typography:** Code font $5.8\text{pt}$, Citation font $6.0\text{pt}$, Table $6.6\text{pt}$.
- **Text Density:** Microscopic code box; $50\%$ blank space at bottom.
- **Table Dimensions:** Two baseline tables, each $510 \times 190\text{ px}$.
- **Image / Chart Dimensions:** None.
- **Header & Footer:** Standard header and footer.
- **Overflow / Clipping:** None.
- **Visual Balance: DEFECTIVE.** Terminal commands and citations are too small. Enlarging code box to $8.0\text{pt}$, expanding citation list, and creating a formal governance verification seal will achieve a balanced final page.
