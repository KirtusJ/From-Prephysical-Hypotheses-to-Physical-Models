# Choosing when another detector block is worth its cost

**Kirtus Justus**, Theoretical Physicist, Port Coquitlam, British Columbia, Canada. Research supplement prepared by OpenAI Codex for Director G.

At the same four-quadrillion-pair deadline, changing the 79 early thresholds saves **more than 22.37 trillion pairs per run on average under either law** relative to the [linear taper](Tapered_thresholds_for_paired_detectors.md). The new rule has conditional error below **4.998137%** and mean exposure below **2.26361520 quadrillion pairs** under each law. The previous rule has mean exposure above **2.28599349 quadrillion pairs** under each law. Its certified error ceiling is tighter at 4.986114%.

### Decision rule

Use the same selected mass and independent blocks of 50 trillion pairs. In each block round 20 times its total log likelihood ratio log(P/Q) to the nearest integer, with ties toward positive infinity. Accumulate those integers. At each early checkpoint choose P or Q when the score reaches or crosses the positive or negative threshold, respectively. At checkpoint 80 decide by sign and split ties fairly. The [checker](check_cost_designed_schedule.py) gives all 79 integer thresholds in observation order. They begin at 81, reach 73 at checkpoint 40, and fall from 37 to 33, 29, 24 and 17 over the last five early decisions. Each pair requires two launches.

### How the thresholds were chosen

A numerical backward recursion prices another block at 0.000768 units of decision loss, with unit loss for a wrong decision. In the design approximation, use a block normal with variance t = 11.388934/80 and mean t/2 under P. Let p[d] be the probability that the rounded increment is d. Work on integer scores j from −180 through 180, with x = j/20. Initialize terminal value V(x) = exp(−|x|/2)/2. For the preceding checkpoint compare this same immediate stopping loss to the continuation score

$$0.000768\cosh(x/2)+\sum_{d=-100}^{100}\sqrt{p[d]p[-d]}\ V(x+d/20).$$

Keep the smaller value and take the first nonnegative score where stopping wins as the threshold. Values beyond |x| = 7 were set to immediate stopping after each iteration, and the finite convolution used zero padding. Repeating for 79 steps gives the thresholds in reverse observation order. This computation proposes a schedule. The finite detector block laws govern the subsequent certificate, so the validity of the bounds does not require the recursion to be exact or the price to be optimal.

### Checking the comparison

The checker uses the finite-law error and survival corrections proved for the linear taper. Stop widths are fixed before observations, so the same one-block replacement argument applies to each schedule. To demonstrate a saving, it propagates a lower bound on the earlier schedule's survival masses and subtracts the finite-block correction from its mean. For the new schedule it propagates upper bounds, adding the corresponding corrections to its error and mean. The rational-denominator calculation subtracts or adds the CDF rounding allowance at each interior bin and rounds the propagated masses in the required direction. Both laws pass separately. The two certified means differ by at least 0.02237829 quadrillion pairs.

The comparison assumes the two specified lossless laws at M = 10⁻⁸ and fresh independent pairs. It does not establish an optimal schedule or validate a physical detector.
