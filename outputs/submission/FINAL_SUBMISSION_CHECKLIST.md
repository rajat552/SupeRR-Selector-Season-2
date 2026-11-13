# Final Unstop Submission Checklist — SupeRR Selector Season 2 (Round 1)

Use this step-by-step manual checklist when submitting on the Unstop competition portal. **Do not reorder or substitute any player on Unstop unless regenerating and re-checking the Methodology Report.**

---

## 1. Pre-Upload Artifact Decision (Participant Sign-Off)

- [ ] **Decide on Charts `03`, `06`, `07`, `09` Label Overlaps:** Reviewed [FINAL_QUALITY_AUDIT.md](file:///c:/Users/LENOVO/OneDrive/Desktop/SupeRR-Selector-Season-2/outputs/submission/FINAL_QUALITY_AUDIT.md) Section 4. Either:
  - Proceed directly with the verified 18-page [SupeRR_Selector_Round1_Methodology_Report.pdf](file:///c:/Users/LENOVO/OneDrive/Desktop/SupeRR-Selector-Season-2/outputs/submission/SupeRR_Selector_Round1_Methodology_Report.pdf), **OR**
  - Request a targeted label-repulsion edit to `src/model_v2/visualization.py` and PDF rebuild before uploading.
- [ ] **Confirm Top-10 Composition Policy:** Confirm retaining retired/coaching performers (`Matthew Wade #2 Bat`, `Dinesh Karthik #4 Bat`, `Andre Russell #9 Bat`, `Mohit Sharma #5 Bowl`) and zero-IPL T20I specialists (`Reeza Hendricks #5 Bat`, `Sufiyan Muqeem #7 Bowl`, `Mohammad Nawaz #9 Bowl`) strictly on 2022–2026 statistical merit, clearly separated from IPL 2027 feasibility in Section 9.

---

## 2. Exact Unstop Dropdown Entry Table (Top 10 Batters — Rank 1 at Top)

Verify each dropdown entry carefully against the dataset identity (`player_id`) and Unstop search-dropdown spelling (also see [user_review_required.md](file:///c:/Users/LENOVO/OneDrive/Desktop/SupeRR-Selector-Season-2/outputs/submission/user_review_required.md)):

| Unstop Rank | Canonical Player Name | Dataset `player_id` | Composite Score | Quick Verification Note | Dropdown Selected? |
|---:|---|---:|---:|---|---:|
| **1** | **Tim David** | `6396` | `+2.434` | Unique name (`Finisher 6+`) | [ ] |
| **2** | **Matthew Wade** | `796` | `+2.267` | Australia (`Finisher 6+`; retired coach flagged in report) | [ ] |
| **3** | **Naman Dhir** | `37052` | `+2.028` | India / MI (`Finisher 6+`) | [ ] |
| **4** | **Dinesh Karthik** | `143` | `+1.764` | India / RCB (`Finisher 6+`; retired coach flagged in report) | [ ] |
| **5** | **Reeza Hendricks** | `768` | `+1.745` | South Africa (`Top 1-3`; zero IPL HP exposure) | [ ] |
| **6** | **Shashank Singh** | `2756` | `+1.609` | India / PBKS (`Finisher 6+`) | [ ] |
| **7** | **Heinrich Klaasen** | `4260` | `+1.608` | South Africa / SRH (`Middle 4-5`) | [ ] |
| **8** | **Rinku Singh** | `4708` | `+1.445` | India / KKR (`Finisher 6+`) | [ ] |
| **9** | **Andre Russell** | `1318` | `+1.434` | West Indies / KKR (`Finisher 6+`; retired IPL coach flagged) | [ ] |
| **10** | **Ashutosh Sharma** | `8101` | `+1.335` | India / DC (`Finisher 6+`) | [ ] |

---

## 3. Exact Unstop Dropdown Entry Table (Top 10 Bowlers — Rank 1 at Top)

| Unstop Rank | Canonical Player Name | Dataset `player_id` | Composite Score | Quick Verification Note | Dropdown Selected? |
|---:|---|---:|---:|---|---:|
| **1** | **Sunil Narine** | `781` | `+2.481` | West Indies / KKR (`Spin_Finger`) | [ ] |
| **2** | **Jasprit Bumrah** | `2933` | `+1.995` | India / MI (`Pace_Fast`) | [ ] |
| **3** | **Mustafizur Rahman** | `4373` | `+1.851` | Bangladesh (`Pace_Medium`) | [ ] |
| **4** | **Jamie Overton** | `2382` | `+1.839` | England / CSK (`Pace_Fast`) | [ ] |
| **5** | **Mohit Sharma** | `2878` | `+1.736` | India (`Pace_FastMedium`; retired Dec 2025 coach flagged) | [ ] |
| **6** | **Sai Kishore** | `5577` | `+1.708` | India / GT (`Spin_Finger`; check `R Sai Kishore` vs `Sai Kishore` on Unstop!) | [ ] |
| **7** | **Sufiyan Muqeem** | `34485` | `+1.665` | Pakistan (`Spin_Wrist`; check `Sufiyan Muqeem` vs `Sufyan Moqim` spelling!) | [ ] |
| **8** | **Mohsin Khan** | `6669` | `+1.625` | India / LSG (`Pace_FastMedium`) | [ ] |
| **9** | **Mohammad Nawaz** | `2490` | `+1.556` | Pakistan (`Spin_Finger`) | [ ] |
| **10** | **Josh Hazlewood** | `830` | `+1.472` | Australia / RCB (`Pace_FastMedium`) | [ ] |

*(Double-check homonym safety: `Rashid Khan` is not in the Top 10 [#14], and neither `Abdul Samad` nor `Haider Ali` appears—ensure no duplicate selection appears within either list.)*

---

## 4. Document Upload & Final Portal Checks

- [ ] **Upload File:** Upload [SupeRR_Selector_Round1_Methodology_Report.pdf](file:///c:/Users/LENOVO/OneDrive/Desktop/SupeRR-Selector-Season-2/outputs/submission/SupeRR_Selector_Round1_Methodology_Report.pdf) (18 pages, A4).
- [ ] **Check Unstop PDF Size/Format Limit:** Confirm the uploaded PDF opens cleanly in Unstop's previewer without clipped right/bottom margins or unreadable figures.
- [ ] **1:1 Parity Cross-Check:** Confirm Rank 1–10 Batters and Rank 1–10 Bowlers in the Unstop form match Page 2 of the uploaded PDF in exact order (`Tim David` #1 down to `Ashutosh Sharma` #10; `Sunil Narine` #1 down to `Josh Hazlewood` #10).
- [ ] **Zero Duplicate Check:** Confirm no player appears twice within Batters or twice within Bowlers.
- [ ] **Optional Post-Deadline Refresh (Only if submitting after Nov 17 / Dec 3, 2026):** If submitting after BCCI's November 17 retention announcement or December 3 final auction register, update the `Unverified` status column in Section 9 (`auction_feasibility.csv` & `source_register.md`) while keeping statistical rankings untouched.
- [ ] **Optional Video/Journey Upload:** Per Problem Statement Page 2, uploading a 30–60 second walkthrough video/screenshots is strictly optional and does not affect scoring.

