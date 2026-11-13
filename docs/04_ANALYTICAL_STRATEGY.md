# 04 — Proposed Analytical Strategy (Draft for Review)

> **Status:** Proposed framework only. No model code or player rankings have been executed yet. Final design choices will be locked after Phase 0 review.

## 1. Defining Match Pressure (Zero Look-Ahead Bias)
Every delivery $t$ in an innings is evaluated using **only pre-delivery state** (runs scored, wickets lost, legal balls remaining before ball $t$ is bowled):

### Option A — Continuous Composite Pressure Index ($PI_t \in [0, 1]$) [Recommended Primary]
- **2nd Innings (Chases):**
  - **Required Run Rate Ratio:** $RRR_t / \text{ParRR}$ (where $RRR_t = 6 \times \text{RunsNeeded}_t / \text{BallsRemaining}_t$, capped sensibly near the final balls, and $\text{ParRR}$ is venue/competition-adjusted or league par ~8.5).
  - **Resource Scarcity (DLS-inspired):** Wickets lost $W_t$ combined with balls remaining $B_t$ (losing 4+ wickets with >60 runs needed creates acute collapse pressure even at moderate RRR).
  - **Exclusion of Dead/One-Sided States:** If a chase is mathematically over or virtually won (e.g., $RRR_t < 4.0$ with $\ge 6$ wickets in hand, or $RRR_t > 24.0$ with $\le 2$ wickets in hand in non-final overs), pressure drops rather than monotonically rising.
- **1st Innings (Setting a Target):**
  - **Collapse Pressure:** Wickets lost $W_t$ relative to expected wickets at over $O_t$ (e.g., $\ge 2$ wickets down in Powerplay, $\ge 4$ down before over 12).
  - **Scoring-Rate Deficit:** Current Run Rate ($CRR_t$) lagging behind competition/venue par at that stage, forcing acceleration without losing wickets.
- **High-Pressure Threshold:** Deliveries in the **top quartile or top 25–30%** of $PI_t$ (e.g., $PI_t \ge 0.65$), plus sensitivity checks at $PI_t \ge 0.60$ and $PI_t \ge 0.75$.

### Option B — Discrete Situational Regimes (Validation / Interpretability Layer)
Explicitly tag interpretable cricket situations:
1. *Early Collapse* ($W_t \ge 3$ within overs 1–6, or $W_t \ge 4$ within overs 1–10).
2. *Tight Chase* (2nd inn, $RRR_t \in [9.0, 16.0]$ with $\le 36$ balls left and $\ge 2$ wickets in hand).
3. *Tight Defence* (Bowling in 2nd inn when $RRR_t \in [8.0, 15.0]$ and match is within 1–2 hits of par).
4. *Knockout / High-Stakes* (`knock_out = 1` as an optional multiplier/sensitivity check).

## 2. Performance Measurement & Baselines
- **Batting Metrics (per legal ball / ball faced):**
  - **Strike Rate (SR)** and **Runs Above Expected (RAE)** relative to phase/innings baseline.
  - **Boundary %** (`4s + 6s`) and **Dot-Ball %** (control vs stagnation).
  - **Survival / Dismissal Rate** (balls per dismissal) — crucial under collapse pressure.
  - **Baseline:** Each batter's own performance in **non-pressure** deliveries ($PI_t < 0.40$) *and* phase-adjusted expected scoring rate, so we measure **Pressure Lift** ($\Delta_{\text{pressure}} = \text{Perf}_{\text{high-pressure}} - \text{Perf}_{\text{normal}}$) alongside **Absolute Pressure Floor** (preventing weak players with low baselines from ranking #1 solely due to a small positive delta).
- **Bowling Metrics (per legal ball):**
  - **Economy Rate (ER)** and **Dot-Ball %** (run-containment under pressure).
  - **Bowling Strike Rate / Wickets per 24 balls** (bowler-credited wickets only: `Caught`, `Bowled`, `LBW`, `Stump`, `Hit Wicket`).
  - **Boundary Conceded %** (execution under death/chase pressure).
  - **Baseline:** Each bowler's own non-pressure ER, dot%, and wicket rate (adjusted for phase/format).

## 3. Fair Comparisons: IPL vs T20I & Context Adjustments
- **Competition Tiering:** Keep IPL and T20I tagged separately throughout. Test whether T20I includes mismatches against lower-ranked associate teams (e.g., via team-strength / competition-level weighting or sensitivity run restricted to IPL + Full-Member T20Is).
- **Primary Competition Scope:** Exclude the 30 `Other_T20` (A-team) matches from the primary ranking, and run a sensitivity check including them.
- **Venue/Season Par Adjustment:** Account for scoring inflation (2024–2026 IPL high-scoring seasons vs 2022) and bowling-friendly venues by centering delivery outcomes against competition-season-phase par.

## 4. Eligibility, Sample-Size Treatment & Reliability
- **Minimum Sample-Size Gates (to be tuned in EDA):**
  - Batters: e.g., minimum total balls faced (e.g., $\ge 250$–$300$ balls) AND minimum high-pressure balls faced (e.g., $\ge 80$–$100$ balls) across $\ge 8$–$10$ distinct high-pressure matches.
  - Bowlers: e.g., minimum total legal balls bowled (e.g., $\ge 250$–$300$ balls) AND minimum high-pressure legal balls (e.g., $\ge 80$–$100$ balls) across $\ge 8$–$10$ distinct high-pressure matches.
- **Empirical Bayes / Shrinkage:** Shrink extreme small-sample pressure deltas toward the population mean proportional to $n / (n + k)$, preventing 30-ball wonders from dominating.
- **Cross-Match Consistency (Reliability):** Measure match-level variance / interquartile stability (e.g., % of high-pressure appearances where the player beat par/baseline, or bootstrap confidence intervals) so one outlier innings does not masquerade as reliability.

## 5. Validation & Sensitivity Plan
1. **Face Validity Check:** Verify that high-$PI$ buckets genuinely exhibit lower win-margin certainty and higher match leverage than low-$PI$ buckets.
2. **Threshold Sensitivity:** Compare Top-10 stability across $PI$ cutoffs (top 20%, 25%, 30%) and alternative weighting of delta vs absolute pressure performance.
3. **Format Sensitivity:** Compare rankings under (a) IPL + All T20I, (b) IPL + Full-Member T20I, and (c) IPL-only.
4. **Bootstrap Stability:** Resample matches (1,000 iterations) to report rank uncertainty and confidence intervals for all Top-10 batters and bowlers.

