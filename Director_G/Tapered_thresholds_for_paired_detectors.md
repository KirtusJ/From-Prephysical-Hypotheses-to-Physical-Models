# Fewer detector pairs with scheduled decision thresholds

**Kirtus Justus**, Theoretical Physicist, Port Coquitlam, British Columbia, Canada. Research supplement prepared by OpenAI Codex for Director G.

With a cap of four quadrillion pairs, a rule with 80 checkpoints has conditional error below **4.986114%** and mean exposure below **2.28623502 quadrillion pairs** under each model. Every qualifying constant symmetric threshold in the [previous comparison](Lower_thresholds_at_the_paired_detector_deadline.md) requires more than 2.30691891 quadrillion pairs on average under each model. The new rule saves more than 20.68 trillion pairs against that entire family, and more than 34.17 trillion against the demonstrated thresholds ±3.867.

### Experimental rule

Repeat the same selected mass (approximately 0.123279641138) in independent blocks of 50 trillion pairs. For each block, sum its pair log likelihood ratios log(P/Q), multiply by 20, round to the nearest integer (ties toward positive infinity), and add that integer to a running score initially zero. Rounding takes place once per block. At checkpoint i from 1 through 79, choose P if the score reaches or exceeds ceil(92−43i/80), or Q if it reaches or falls below the negative of that integer. Otherwise collect the next block. At checkpoint 80 decide by the score's sign, using a fair coin at zero. Two launches form one pair. The score is an implementable statistic; it need not equal the full transcript log likelihood.

### Error control for the finite block laws

For each model orient the score so positive favors the true law. Under Q reflection reverses the rounding convention at exact bin boundaries. Either one-sided convention obeys the same normal CDF error bound, as the approximating CDF is continuous. The [checker](check_tapered_blocks.py) calculates individual log-increment moments directly from the four cells. For a block of B pairs with single-pair variance v and third absolute central moment ρ, the Kolmogorov distance to the matching normal before rounding is at most ε = 0.475ρ/(v^(3/2)√B). Applying the same rounding map preserves that bound for the resulting integer scores. [Shevtsova's iid Berry–Esseen constant](https://arxiv.org/abs/1111.6554)

Replace the 80 independent block increments by matching normal increments one at a time. Given every other increment and the final tie coin, the wrong-decision indicator decreases weakly as this increment increases. Two ordered live scores stay ordered, and the smaller can only exit first in the wrong direction or the larger first in the correct direction, unless both exit in the same direction. The conditional wrong-decision set is therefore a half-line, possibly empty or full, and the change in error is at most ε per replacement.

Survival through checkpoint j requires every partial sum to stay strictly inside its boundary. Conditional on all increments except one of the first j, the eligible values for that increment form an intersection of intervals. Replacing one increment changes survival by at most 2ε, so the survival error is at most 2jε. Summing survival probabilities for j = 0 through 79 bounds the error in expected blocks by 80 × 79 × ε. These corrections apply separately under each true law.

### Reproducing the calculation

For the rounded normal increments the checker propagates upper bounds on the surviving probability at each integer score. It accumulates the wrong-side exit mass and the probability of entering each successive block. Normal CDF values use interval arithmetic, an integrated exponential series and Mills' bound beyond nine standard deviations. A fixed integer denominator and upward rounding at each step bound the numerical error. The final inequalities include the finite-block corrections. Both model checks pass.

The comparison fixes the previously selected mass, the two specified lossless models at M = 10⁻⁸, the cap, and independence across fresh pairs. The demonstrated schedule was chosen computationally. Its global optimality and applicability to physical observations remain open.
