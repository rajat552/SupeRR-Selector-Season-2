# PDFME Capability Matrix & Architectural Trade-off Analysis

This document evaluates the operational capabilities, architectural constraints, and design trade-offs of using `@pdfme` in high-density, publication-grade sports analytics reporting for **SupeRR Selector Season 2**.

---

## 1. Native `@pdfme` Capabilities & Primitives

The `@pdfme` library provides a template-first PDF engine built on top of `pdf-lib`. Its native primitives include:

| Feature / Primitive | Native Support | Implementation Mechanism | Evaluation for SupeRR Final Report |
| :--- | :---: | :--- | :--- |
| **Fixed Schema Coordinates** | Full | JSON template with explicit `(x, y, width, height)` per element | Ideal for cover pages, KPI cards, and structured scorecards. |
| **Dynamic Tables** | Full | `@pdfme/schemas` table plugin | Provides column width control, padding, alternating row colors, and head styles. |
| **Multi-page Flow** | Partial | Page-array templates (`basePdf` per page or uniform) | Each page requires an explicit schema array. Content does not arbitrarily auto-flow across page breaks without explicit pagination logic. |
| **Images & Raster Graphics**| Full | Base64 or binary data URLs (`image/png`, `image/jpeg`) | Seamless embedding of pre-rendered Matplotlib / Seaborn figures and radar charts. |
| **Vector & SVG** | Full | `@pdfme/schemas` SVG plugin | Direct vector drawing for icons, badge emblems, and geometric accents. |
| **Custom Typography** | Full | TTF / WOFF custom font injection | Supports Inter, Outfit, Fira Code, and JetBrains Mono with explicit font definition maps. |
| **CLI & Headless Operations**| Full | `@pdfme/cli` (`pdf2size`, `pdf2img`, `generate`, `doctor`)| Excellent for automated CI verification, geometry checking, and page rasterization audits. |

---

## 2. Engineering Realities for 15-Page High-Density Cricket Analytics

### A. Template Coordinates vs. Analytical Density
A 15-page sports analytics report containing 15,150 specification descriptions, leave-one-out baselines, 10-player deep-dive profiles, bootstrap confidence intervals, and Rajasthan Royals squad balance tables contains over 25,000 data cells and words. In a pure coordinate-based JSON template, manually hand-coding 25,000 coordinate boxes across 15 pages is brittle, prone to text clipping, and unmaintainable.

### B. Mathematical Typography (KaTeX / LaTeX)
Statistical formulas (such as the ball-level pressure index $P_i$, Dirichlet-multinomial Bayesian shrinkage $\alpha_0$, and leave-player-out contextual expectation $\mathbb{E}[R_{i,c}]$) require precise mathematical typography. `@pdfme` text schemas render plain text glyphs without a native LaTeX equation parser. Mathematical expressions must therefore be compiled to SVG/vector or rendered via math-engine typography prior to embedding.

### C. Data Table Pagination & Wrapping
Cricket metrics (such as `105.7 ± 14.2`, strike rates, boundary percentages, and auction statuses) demand pixel-perfect column widths, vertical centering, and zero-overflow wrapping. 

---

## 3. Evaluated Architectural Options

### Option A: Pure JSON Schema Template Generation via `@pdfme/generator`
- **Pros:** Uses `@pdfme/generator` directly in Node.js.
- **Cons:** Auto-flowing 15 distinct publication pages with varying card grids, double columns, and mixed charts requires custom polyfill layout code. LaTeX formula rendering requires external pre-rendering.

### Option B: Headless Web Standards (Playwright / Chromium Engine) + `@pdfme/cli` Inspection & Verification
- **Pros:** 
  - Full modern CSS grid, flexbox, Paged Media (`@page`), and KaTeX math typography support.
  - Pixel-perfect visual hierarchy identical to top sports analytics whitepapers (The Athletic, CricViz, ESPN Cricinfo).
  - High-resolution vector PDF compilation via modern headless layout engine.
  - Deep integration with `@pdfme/cli` for automated page geometry validation (`pdf2size`), visual regression image extraction (`pdf2img`), and rendering diagnostic audits (`doctor`).
- **Cons:** Requires headless browser runtime (already verified available in local environment via Playwright / Chrome / Edge).

### Option C: Python ReportLab Canvas Flowables
- **Pros:** Native Python execution.
- **Cons:** `reportlab` is not installed in the workspace environment, and installing external binary packages is unnecessary given the rich web standards and `@pdfme` toolchains already present.

---

## 4. Architectural Decision: The Verified Publication Pipeline

We adopt **Option B**:
1. **Layout & Typesetting Engine:** High-precision CSS Paged Media specification (`@page { size: A4; margin: 0; }`) with modern typography, KaTeX formula compilation, embedded SVG icons, and verified data tables.
2. **Headless Generation:** Offline headless PDF generation preserving exact vector elements, embedded fonts, and print color fidelity (`prefers-color-scheme: light`, exact CMYK/RGB matching).
3. **pdfme Forensic Verification Suite:**
   - `@pdfme/cli pdf2size` validates page count (strictly 15 pages) and dimensions ($210 \times 297\text{ mm}$ A4 portrait).
   - `@pdfme/cli pdf2img` extracts high-resolution 300-DPI PNGs for visual inspection, typography alignment, and forensic auditing.
   - Comprehensive QA automated scripts verify statistical consistency, table totals, and zero-defect layout.
