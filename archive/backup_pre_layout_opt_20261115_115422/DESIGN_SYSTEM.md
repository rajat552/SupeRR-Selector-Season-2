# Design System: SupeRR Selector Season 2 Publication Report

This specification establishes the comprehensive visual, typographic, structural, and component design system for the **SupeRR Selector Season 2** final analytics report.

---

## 1. Page Geometry & Dimensional Specifications

- **Format:** ISO 216 A4 Portrait
- **Width:** $210\text{ mm}$ ($595.28\text{ pt}$)
- **Height:** $297\text{ mm}$ ($841.89\text{ pt}$)
- **Margins:**
  - Top: $8\text{ mm}$ ($22.7\text{ pt}$)
  - Bottom: $8\text{ mm}$ ($22.7\text{ pt}$)
  - Left / Right: $10\text{ mm}$ ($28.3\text{ pt}$)
- **Printable Area:** $190\text{ mm} \times 281\text{ mm}$
- **Target Page Count:** Exactly 15 pages. Zero overflow, zero blank pages.

---

## 2. Color Palette & Semantic Tokens

```
/* Primary Corporate & Franchise Tokens */
--rr-navy-deep:     #0B132B;  /* Deep header / cover background */
--rr-navy-primary:  #0F172A;  /* Primary headings, heavy accents */
--rr-royal-blue:    #004BA0;  /* Rajasthan Royals Royal Blue */
--rr-royal-pink:    #E91E63;  /* Rajasthan Royals Signature Pink */
--rr-pink-light:    #FCE7F3;  /* Pink pill / badge background */
--rr-gold-accent:   #D4AF37;  /* Tier 1 / elite gold accent */

/* Neutral & Surface Tokens */
--surface-white:    #FFFFFF;  /* Card base, primary canvas */
--surface-offwhite: #F8FAFC;  /* Alternating row zebra fill, formula box */
--surface-tint-blue:#F1F5F9;  /* Secondary container background */
--border-subtle:    #E2E8F0;  /* Standard container border (1px solid) */
--border-muted:     #CBD5E1;  /* Divider rules */

/* Typography Tokens */
--text-primary:     #0F172A;  /* Slate-900: High-contrast body & headlines */
--text-secondary:   #334155;  /* Slate-700: Descriptive prose */
--text-muted:       #64748B;  /* Slate-500: Captions, metadata, footnotes */
--text-on-dark:     #FFFFFF;  /* White on Navy */

/* Semantic Data Visualization Tokens */
--metric-positive:  #059669;  /* Emerald-600: Positive lift / outperformance */
--metric-negative:  #DC2626;  /* Red-600: Negative lift / underperformance */
--metric-neutral:   #D97706;  /* Amber-600: Context-dependent */
```

---

## 3. Typographic Hierarchy

- **Font Family:** `system-ui, -apple-system, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif`
- **Monospace Family:** `"JetBrains Mono", "SF Mono", Consolas, Menlo, monospace`
- **Math Engine:** KaTeX rendered vectors / mathematical CSS typesetting

| Element | Size | Weight | Tracking / Line Height | Application |
| :--- | :---: | :---: | :---: | :--- |
| **Document Masthead Title** | $17\text{ pt}$ | Bold (800) | $-0.02\text{em}$ / $1.15$ | Page 1 Main Header |
| **Document Subtitle** | $9.5\text{ pt}$ | Medium (500) | Normal / $1.25$ | Page 1 Subtitle & Metadata |
| **Page Header Title** | $11.5\text{ pt}$ | Bold (700) | $-0.01\text{em}$ / $1.2$ | Pages 2–15 Running Section Title |
| **Page Header Subtitle** | $7.2\text{ pt}$ | Medium (500) | $+0.02\text{em}$ Uppercase | Running category indicator |
| **Section Headings (H2)** | $9.0\text{ pt}$ | Bold (700) | $-0.01\text{em}$ / $1.2$ | Major section breaks |
| **Subsection Headings (H3)**| $8.0\text{ pt}$ | Semi-bold (600)| Normal / $1.2$ | Component & card titles |
| **Body Paragraphs** | $7.2\text{ pt}$ | Regular (400) | Normal / $1.38$ | Analytical prose |
| **KPI Values** | $14.0\text{ pt}$| Extra-bold (800)| $-0.02\text{em}$ / $1.0$ | Metric cards |
| **KPI Labels** | $6.2\text{ pt}$ | Semi-bold (600)| $+0.04\text{em}$ Uppercase | Metric card sub-labels |
| **Table Column Headers** | $6.6\text{ pt}$ | Bold (700) | $+0.03\text{em}$ Uppercase | Data table header cells |
| **Table Data Cells** | $6.4\text{ pt}$ | Regular (400) | Normal / $1.25$ | Numbers & values |
| **Table Highlight Names** | $6.8\text{ pt}$ | Semi-bold (600)| Normal / $1.25$ | Player names |
| **Badges & Pills** | $5.8\text{ pt}$ | Bold (700) | $+0.03\text{em}$ Uppercase | Tier 1, Status, Ranks |
| **Running Footers** | $6.0\text{ pt}$ | Regular (400) | Normal / $1.2$ | Bottom page footer |

---

## 4. Reusable Component Specifications

### 4.1 Running Page Header & Footer
- **Header:** Full-width container with flex layout. Left side displays section number and title in Royal Navy; right side displays topic tag with a subtle pink indicator bar.
- **Footer:** 3-column split: Left = `SupeRR Selector Season 2 | Proprietary Franchise Intelligence`; Center = `Pre-Registered Multiverse Architecture (3.19M Evaluations)`; Right = `Page X of 15`.

### 4.2 KPI Highlight Card Grid
- Clean 4-card or 5-card horizontal array with $1\text{px}$ subtle border (`#E2E8F0`), $2\text{px}$ top accent border (Navy/Pink/Gold/Emerald), white background, bold number, and uppercase muted label.

### 4.3 Data Tables
- Header row with dark navy fill (`#0F172A`) or tinted slate (`#F1F5F9`), crisp cell padding ($2.5\text{px}$ top/bottom, $4\text{px}$ left/right).
- Alternating zebra rows (`#FFFFFF` and `#F8FAFC`).
- Numerical cells right-aligned; ranks and badges centered; names left-aligned.

### 4.4 Player Dossier Cards
- Micro-profile card with 2-column or 3-column layout:
  - Left: Player badge, rank pill, ID, franchise, and auction eligibility status.
  - Center: Key multiverse metrics (Shrunk PWI, Raw Lift, Top-10 Frequency, Bootstrap 90% CI).
  - Right: Tactical franchise recruitment dossier for Rajasthan Royals 2026/2027.

### 4.5 Mathematical Formulation Display
- Styled mathematical equation block with light slate background (`#F8FAFC`), $1\text{px}$ border (`#E2E8F0`), left accent bar in RR Pink (`#E91E63`), typeset equations, and clean variable definitions.
