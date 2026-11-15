# PDFME Local Setup & Tooling Architecture

This document details the local installation, configuration, and architectural integration of the official open-source [`pdfme`](https://github.com/pdfme/pdfme.git) toolchain for the **SupeRR Selector Season 2** publication-grade PDF engineering pipeline.

---

## 1. Upstream Clone Details

- **Target Directory:** `.tools/pdfme-upstream/`
- **Repository URL:** `https://github.com/pdfme/pdfme.git`
- **Commit Hash:** `60d73ae0a0b707c241c14e3c70bcec9670c56113`
- **Commit Message:** `chore(deps): bump the minor-and-patch group across 2 directories with 16 updates (#1706)`
- **Git Ignored Status:** Verified ignored via `.gitignore` (`.tools/` rule). No upstream artifacts or node modules are tracked in the primary analytics repository.

---

## 2. Environment & CLI Versions

- **Node.js:** `v22.14.0` (Satisfies Node >= 20.0.0 requirement)
- **npm:** `10.9.2`
- **pdfme CLI:** `@pdfme/cli@6.2.8`
- **CLI Commands Available:**
  - `generate`: Generates PDF documents from JSON template and input datasets.
  - `validate`: Validates template schema compliance.
  - `pdf2img`: Renders PDF pages directly into high-fidelity image formats (PNG/JPEG) for visual inspection.
  - `pdf2size`: Analyzes page geometry, aspect ratio, and physical dimensions.
  - `doctor`: Diagnoses template structure, missing font glyphs, and rendering schema integrity.

---

## 3. Upstream Monorepo Architecture Overview

The `pdfme` framework operates as a TypeScript monorepo structured into specialized packages:

| Package | Purpose |
| :--- | :--- |
| `@pdfme/common` | Core type definitions, bounding-box coordinate systems, and schema interfaces. |
| `@pdfme/schemas` | Pluggable rendering primitives: Text, Multi-line Text, Image, Table, SVG, Barcodes/QR, Shapes. |
| `@pdfme/generator` | Headless PDF generation engine utilizing `pdf-lib` to compose schemas onto blank or template PDFs. |
| `@pdfme/ui` | Interactive visual canvas editor for template manipulation and WYSIWYG element alignment. |
| `@pdfme/manipulator`| Document merging, splitting, extraction, and page reordering primitives. |
| `@pdfme/converter` | PDF-to-image and visual asset rasterization wrappers. |
| `@pdfme/cli` | Command-line interface providing headless generation, size inspection, image rasterization, and validation. |

---

## 4. Local Reproduction & Verification Commands

```powershell
# 1. Run pdfme environment diagnostics
npx @pdfme/cli doctor

# 2. Inspect target PDF dimensions
npx @pdfme/cli pdf2size outputs/final_package/SupeRR_Final_Report.pdf

# 3. Rasterize PDF pages to PNG for forensic QA inspection
npx @pdfme/cli pdf2img outputs/final_package/SupeRR_Final_Report.pdf --output outputs/pdf_redesign/original_render/
```

---

## 5. Licensing and Attribution

- **License:** MIT License
- **Copyright:** (c) pdfme contributors / madogiwa Inc.
- **Upstream Repository:** [https://github.com/pdfme/pdfme](https://github.com/pdfme/pdfme)
- **Compliance:** Used as an external local tooling asset under the terms of the MIT License. Upstream source code and licenses are fully preserved in `.tools/pdfme-upstream/LICENSE.md`.
