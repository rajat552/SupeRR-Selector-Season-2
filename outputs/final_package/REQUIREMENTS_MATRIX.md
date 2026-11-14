# Requirements Traceability Matrix
**SupeRR Selector Season 2 — Final Submission Deliverable**
**Author:** Lead Data Scientist
**Target Document:** `outputs/submission_final/SupeRR_Final_Report.pdf` (and companion `.md`)

This matrix maps every explicit instruction, analytical mandate, and governance rule from the official problem statement (`Round 1 Problem Statement _ SupeRR Selector Season 2.docx.pdf`) and the live Unstop submission interface to the corresponding section of the final methodology report and codebase.

---

| # | Source | Core Requirement / Mandate | Report Section & Page | Verification & Evidence Artifact |
|---|---|---|---|---|
| **R1** | Problem Statement & Form | Two ordered Top-10 lists (Batters, Bowlers) on Page 1 | **Page 1 (Executive Summary)** | `outputs/model_v4/final_top10_batters.csv`, `outputs/model_v4/final_top10_bowlers.csv` |
| **R2** | Problem Statement | Performance in high-pressure situations compared with usual performance (Maintenance & Lift) | **Page 1, Section 4 (Performance Measurement)** | Shrunk $PWI$, normal baseline, raw lift, maintenance lift ($PWI - 0.35 \times \text{Normal}$) |
| **R3** | Problem Statement | Pressure definition, rationale, and situational mechanics | **Section 3 (Defining Pressure in T20 Cricket)** | Batter PI vs. Bowler PI; worked delivery examples for both disciplines |
| **R4** | Problem Statement | Performance measurement: metrics, LPO baselines, scoring logic | **Section 4 (Performance Measurement Framework)** | LPO hierarchical expected runs/wickets, non-overlapping wicket values, EB shrinkage ($K=120$) |
| **R5** | Problem Statement | Fair comparisons: sample size gates, match context, format separation | **Section 5 (Fair Comparisons & Scope Governance)** | 3-tier eligibility gates (lenient/standard/strict), IPL vs. T20I splits, match-level clustering |
| **R6** | Problem Statement | Empirical evidence for each Top-10 player and specific ordering | **Section 6 (Consensus Rankings & Player Evidence)** | 2–3 evidence sentences per player with volume, shrunk rates, lifts, and consistency |
| **R7** | Problem Statement | Reliability & limitations: cross-match consistency, uncertainty | **Section 7 (Model Reliability, Uncertainty & Limitations)** | Beta-binomial consistency, bootstrap confidence intervals, out-of-sample caveats |
| **R8** | Problem Statement | Multiverse specification curve & pre-registered selection rule | **Section 8 (Multiverse Specification Curve Analysis)** | Pre-registration protocol, 15,150 specs/role, variance decomposition, specification curves |
| **R9** | Submission Form | Rajasthan Royals squad needs, tactical fit, and auction targets | **Section 9 (Rajasthan Royals Strategic Recruitment Dossier)** | Recomputed RR 2026 figures from raw data, gap analysis, 20 player profiles |
| **R10** | Submission Form | Verified public player availability & source register | **Section 9, Table 3; Appendix B** | `outputs/submission_final/source_register.md` (all 20 players verified with official URLs & dates) |
| **R11** | Submission Form | Blank "PARTICIPANT RECOMMENDATION" column for human review | **Page 1 & Section 9 (Dossier Tables)** | Dedicated empty column for user sign-off prior to auction table |
| **R12** | Governance (AGENTS.md) | Zero look-ahead, strict pre-delivery state, cricket accounting | **Section 2 & Appendix C (Mathematical Architecture)** | Pre-delivery features only, revised balls in overs, non-bowler wicket exclusions |
| **R13** | Governance (AGENTS.md) | Immutable baseline & raw data integrity preservation | **Appendix D (Reproducibility & Verification)** | 39/39 SHA-256 checksums verified against `integrity_manifest_pre.json` |
| **R14** | Submission Styling | First-person singular ("I"), plain English, 12–15 page PDF limit | **Entire Report Layout** | `SupeRR_Final_Report.pdf` (compiled via WeasyPrint, verified 13–14 pages) |
| **R15** | Banned Terms | No biomechanical speed/RPM claims, no "World Cup", no false certitude | **Entire Report Language** | Strict terminology compliance; zero speed gun / release height / ball tracking claims |

---

## Sign-Off Verification
Every analytical requirement is fully reconciled against data-driven outputs in `outputs/model_v4/`. No speculative overrides or unverified claims are present in the final submission.
