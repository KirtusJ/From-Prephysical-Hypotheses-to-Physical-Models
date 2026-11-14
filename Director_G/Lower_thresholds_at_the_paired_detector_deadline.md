# Lowering the early decision threshold at a fixed pair budget

**Kirtus Justus**, Theoretical Physicist, Port Coquitlam, British Columbia, Canada. Research supplement prepared by OpenAI Codex for Director G.

At a cap of four quadrillion pairs, stop when the accumulated log likelihood reaches either −3.867 or +3.867. At the cap, choose the sign of the likelihood logarithm, splitting ties by a fair coin. At the [previously selected mass](Deciding_at_a_paired_detector_deadline.md), each of the two specified detector laws has error between **4.96484% and 4.99902%**. Under either law the mean count lies between **2.32041393 and 2.32041520 quadrillion pairs**, saving at least 70.46 trillion pairs per run on average relative to thresholds ±4. Each pair costs two launches.

### What prevents further reductions?

At symmetric threshold magnitude 3.842, the [continuous-clock lower bound](Deciding_at_a_paired_detector_deadline.md) gives equal-prior error above 5.00070%. Every smaller positive threshold is also excluded. A wider-threshold observer can reconstruct the earlier threshold decision from its transcript. Its likelihood-sign decision is Bayes optimal for that transcript because the stopped likelihood is the product likelihood up to stopping. Hence equal-prior risk cannot increase with threshold width. Failure of the average target implies failure for at least one law.

A feasible threshold in this family therefore exceeds 3.842. On a common sequence, the number of pairs used increases weakly with threshold width, including at the deadline. Applying the [mean clock lower bound](Mean_exposure_at_the_paired_detector_deadline.md) at 3.842 gives a mean above 2.30691891 quadrillion pairs under either law for every feasible width. Even if an intermediate width meets both conditional targets, it can save less than 0.582% of the demonstrated 3.867 rule's mean. This exclusion concerns the same mass, fixed symmetric thresholds, likelihood-sign terminal action and cap. Time-dependent boundaries or a different sampling policy require separate analysis.

### Certifying both conditional errors near 5%

Use the [nearby-prior comparison](Conditional_errors_at_a_paired_detector_deadline.md) with h = 0.003 and clock tolerance d = 0.000020. A tighter bound on the cost of changing the prior follows by integrating the loss difference over the short interval of changed decisions. Its length is c = log((1+h)/(1−h)). Under the reference law Q, the difference of the two prior-weighted likelihoods vanishes at the shifted cutoff. Its slope has absolute value at most (1+h)exp(c)/2 throughout the interval. Thus the gain from changing the decision is at most (1+h)exp(c)c²/4 times the previous uniform density ceiling. The atoms at the exit boundaries cannot contribute because c < 3.867. The [numerical checker](check_lower_deadline_threshold.py) applies this bound in each direction, checks the failing width separately, and computes the mean bounds under each law.

The results are conditional on the two fixed populations at M = 10⁻⁸, lossless observations and independent fresh pairs. No physical detector data were acquired.
