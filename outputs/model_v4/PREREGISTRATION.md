# Multiverse Analysis Pre-Registration Protocol
**SupeRR Selector Season 2 — IPL 2027 Auction Analytics**
**Author:** Rajat Aggarwal
**Status:** Pre-registered Protocol (Locked)

*Written before any multiverse results were produced.*

---

## 1. Objective & Governance

This protocol specifies the multiverse (specification-curve) analysis for evaluating batter and bowler performance under pressure in T20 cricket, as mandated by the SupeRR Selector Season 2 competition problem statement. 

To eliminate researcher degrees of freedom, confirmation bias, and post-hoc narrative fitting, all analytical dimensions, mathematical models, parameter grids, and decision rules are established prior to the execution of the multiverse pipeline. Any operational deviation necessitated by technical constraints or edge cases will be formally documented with justification in `outputs/model_v4/DEVIATIONS.md`.

---

## 2. Specification Grid Dimensions

The multiverse grid systematically explores eight operational dimensions across both batting and bowling roles.

### Dimension P: Pressure Definition
Defines the delivery-level pressure weighting $w_k \in [0, 1]$ or discrete classification:
- **Batters:**
  - **P1:** Continuous batting pressure index with logistic sigmoid centered at $x_0 = 0.40$, $k = 10$.
  - **P2:** Canonical continuous batting pressure index with logistic sigmoid centered at $x_0 = 0.425$, $k = 10$.
  - **P3:** Continuous batting pressure index with logistic sigmoid centered at $x_0 = 0.45$, $k = 10$.
  - **P4:** Discrete thresholding: High-Pressure ($PI \ge 0.50$) vs. Normal ($PI < 0.35$), discarding intermediate buffer.
  - **P5 (Definition C):** Heuristic domain rule:
    - 2nd Innings (Live Chase): $\le 48$ legal balls remaining, Required Run Rate (RRR) between $7.0$ and $15.0$, and wickets down $\le 7$.
    - 1st Innings: Collapse pressure defined as $\ge 3$ wickets down before over 8.0, OR $\ge 5$ wickets down before over 14.0.
- **Bowlers:**
  - **P1:** Defending-side continuous pressure index centered at $x_0 = 0.40$, $k = 10$.
  - **P2:** Canonical defending-side continuous pressure index centered at $x_0 = 0.425$, $k = 10$.
  - **P3:** Defending-side continuous pressure index centered at $x_0 = 0.45$, $k = 10$.
  - **P4:** Defending-side discrete thresholding ($PI_{\text{def}} \ge 0.50$ vs. $< 0.35$).
  - **P5 (Definition C):** Heuristic defending domain rule:
    - 2nd Innings: Defending a live chase with $\le 48$ balls remaining, RRR between $6.0$ and $12.0$, and wickets down $\le 6$.
    - 1st Innings: Death defense defined as overs 16–20 with batting team having lost $\le 4$ wickets.
  - **P0 (Reference Only):** The legacy single-index V2 model (which conflated batter game-state with bowling pressure, inappropriately crediting bowlers for bowling at tailenders in blowouts). *Explicitly excluded from final selection rankings; evaluated solely for methodological benchmarking.*

### Dimension W: Wickets-Fallen Context in Baseline
Evaluates whether context expectations account for batting collapse / resource depletion:
- **W0:** No wickets in baseline cell definition: $Cell = (Phase, RRR\_Bucket)$ for 2nd innings, $Cell = (Phase)$ for 1st innings.
- **W1:** Wickets accounted for via discrete buckets: $Cell = (Phase, Wickets\_Bucket, RRR\_Bucket)$, where $Wickets\_Bucket \in \{0\text{--}2, 3\text{--}5, 6+\}$.

### Dimension M: Scoring Model
Evaluates the mathematical formulation of performance under pressure:
- **Model A (Absolute Pressure Performance):** Evaluates shrunk performance directly on high-pressure balls ($PWI$).
- **Model B (Maintenance & Lift):** Evaluates pressure resilience via a linear combination of baseline maintenance and pressure lift:
  $$Score = \alpha \cdot \text{PWI}_{\text{shrunk}} + (1 - \alpha) \cdot \text{Lift}_{\text{shrunk}}, \quad \alpha = 0.60$$
  where $\text{Lift}_{\text{shrunk}} = \text{PWI}_{\text{shrunk}} - \text{Normal}_{\text{shrunk}}$.
- **Model C (Interaction Ridge/Logit Regression):** Regularized delivery-level regression estimating player-specific pressure interaction coefficients $\beta_{i, \text{pressure}}$. *Evaluated across the full $(P, W, F)$ grid at canonical hyperparameters $V=6, K=120, G=\text{standard}$ due to computational intensity.*

### Dimension V: Wicket Valuation
Determines the relative run equivalent value assigned to a dismissal in composite metric calculations:
- **V=4:** Conservative wicket value ($4.0$ runs).
- **V=6:** Canonical T20 wicket value ($6.0$ runs).
- **V=8:** High-leverage wicket value ($8.0$ runs).
- **V=ctx:** Context-marginal wicket value dynamically computed from the expected run difference by phase and wickets fallen.

### Dimension K: Empirical Bayes Shrinkage Strength
Controls the regularization towards league prior to avoid small-sample distortion:
- **K=60:** Moderate shrinkage (prior weight equivalent to 60 effective balls).
- **K=120:** Canonical shrinkage (prior weight equivalent to 120 effective balls).
- **K=180:** Aggressive shrinkage (prior weight equivalent to 180 effective balls).

### Dimension F: Competition & Format Scope
Tests sensitivity to competition quality and representative sample boundaries:
- **F1 (All Scope):** IPL + All T20 Internationals (excluding `Other_T20` comp IDs 2670, 3289).
- **F2 (Elite Scope):** IPL + ICC Full-Member T20 Internationals only (AFG, AUS, BAN, ENG, IND, IRE, NZ, PAK, SA, SL, WI, ZIM).
- **F3 (Franchise Scope):** Indian Premier League (IPL) matches only.

### Dimension G: Eligibility Gate
Minimum sample requirements to enter consideration:
- **Lenient:** $\ge 200$ total legal balls, $\ge 80$ HP balls, $\ge 8$ HP matches.
- **Standard:** $\ge 300$ total legal balls, $\ge 120$ HP balls, $\ge 10$ HP matches.
- **Strict:** $\ge 400$ total legal balls, $\ge 150$ HP balls, $\ge 12$ HP matches.
- *(Note: For Definition P5, high-pressure ball thresholds are scaled down proportionally to P5's global HP volume relative to P2).*

### Dimension S: Metric Composite Weights (Models A and B)
Controls the balance between scoring efficiency, boundary/wicket strike capability, and defensive control:
- **S0 (Base):** $(0.50, 0.30, 0.20)$ — Batter: (Runs/Expected, Strike Rate Lift, Dot Rate Resistance); Bowler: (ER Lift, Wicket Rate, Dot Ball %).
- **S1 (+10% w1):** $(0.60, 0.30, 0.20)$ renormalised $\rightarrow (0.5455, 0.2727, 0.1818)$
- **S2 (-10% w1):** $(0.40, 0.30, 0.20)$ renormalised $\rightarrow (0.4444, 0.3333, 0.2222)$
- **S3 (+10% w2):** $(0.50, 0.40, 0.20)$ renormalised $\rightarrow (0.4545, 0.3636, 0.1818)$
- **S4 (-10% w2):** $(0.50, 0.20, 0.20)$ renormalised $\rightarrow (0.5556, 0.2222, 0.2222)$
- **S5 (+10% w3):** $(0.50, 0.30, 0.30)$ renormalised $\rightarrow (0.4545, 0.2727, 0.2727)$
- **S6 (-10% w3):** $(0.50, 0.30, 0.10)$ renormalised $\rightarrow (0.5556, 0.3333, 0.1111)$

---

## 3. Pre-Registered Selection Rule

To determine the definitive Top-10 Batters and Top-10 Bowlers for Rajasthan Royals' IPL 2027 recruitment strategy, the following five-step algorithmic rule must be executed strictly:

1. **Candidate Pool Eligibility:**
   A player must be statistically eligible under at least $50\%$ of all valid multiverse specifications (where valid excludes Bowler P0). Players meeting $< 50\%$ eligibility are excluded from the ranking pool.

2. **Multiverse Consensus Ranking:**
   Eligible candidates are ranked in descending order of their **Multiverse Top-10 Frequency** (the proportion of valid specifications where the player finishes inside the top 10).
   - *Tie-Breaking:* Ties in Top-10 frequency are broken strictly by **Lower Median Multiverse Rank**.

3. **Bootstrap Stability Hurdle:**
   A candidate selected by Step 2 must undergo a 1,000-draw match-level stratified bootstrap under the Canonical Specification ($P2, W1, M=B, V=6, K=120, F=\text{All}, G=\text{Standard}, S=\text{Base}$).
   - **Criterion:** The player must achieve statistical eligibility in $\ge 800$ of the 1,000 bootstrap draws ($\ge 80.0\%$).
   - If a candidate fails this hurdle, they are excluded from the Top 10 as sample-dependent, and the next candidate in multiverse consensus order is evaluated.

4. **Confidence Tiering:**
   Players are classified into three confidence tiers based on multiverse consensus:
   - **Tier 1 (Core Consensus):** Multiverse Top-10 Frequency $\ge 80.0\%$. Exceptionally robust across definitions, weights, and sample scopes.
   - **Tier 2 (Strong Contender):** Multiverse Top-10 Frequency between $50.0\%$ and $79.9\%$. High-performing assets whose rank shifts moderately with specific parameter variations.
   - **Tier 3 (Context-Dependent):** Multiverse Top-10 Frequency $< 50.0\%$. Viable candidates that emerge only under targeted specifications.

5. **Final Output Determination:**
   The final Top-10 Batters and Top-10 Bowlers consist of the first 10 candidates per role who satisfy Steps 1, 2, and 3. The unfiltered canonical baseline Top 10 will be reported transparently in the Appendix for full reproducibility.
