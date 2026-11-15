# Checking detector evidence every 25 trillion pairs

**Kirtus Justus**, Theoretical Physicist, Port Coquitlam, British Columbia, Canada. Research supplement prepared by OpenAI Codex for Director G.

Under each of the two specified lossless detector laws at M = 10⁻⁸, a 160-checkpoint rule has mean exposure below **2.25541057 quadrillion pairs** and error below **4.999529%**. The [80-checkpoint cost-designed rule](Cost_of_another_detector_block.md) has mean above **2.26337367 quadrillion pairs** under each law. The guaranteed saving exceeds 7.96 trillion pairs per run under either model. Both rules cap exposure at four quadrillion pairs. Their error ceilings are close to the 5% target, with the earlier rule certified below 4.998137%.

### Sampling and decision

Use the previous selected mass and a fresh independent pair each time. After every 25 trillion pairs, multiply the block log likelihood log(P/Q) by 40 and round to the nearest integer, taking exact ties toward positive infinity. Add the integer to the cumulative score. At checkpoints 1 through 159 choose P or Q if the score reaches or crosses the corresponding positive or negative threshold. At checkpoint 160 choose by score sign with a fair tie coin. The [checker](check_finer_checkpoints.py) contains the full integer schedule. The comparison changes the block size, the score resolution and the thresholds together. It does not isolate the effect of checkpoint frequency alone.

### Selection and verification

The same numerical backward recursion used in the earlier study supplied the threshold proposal. Set its block variance to 11.388934/160, block price to 0.000386 and score unit to 1/40. Use the integer design grid from −360 to 360 and convolution offsets −100 through 100. The rule used for verification is the fixed integer array in the checker. A nearby price of 0.000387 yielded a schedule whose certified error upper bound exceeded 5% under P, despite a Gaussian design estimate below target. That failed certificate is not a lower bound on its actual error.

The checker applies the earlier independent-block Berry–Esseen error and survival corrections at the new block size and number of decisions. In parallel it propagates survival lower bounds for the earlier rule with its original blocks, thresholds and rounding unit. Positive integer arithmetic bounds the Gaussian recursion, and the finite-block corrections apply separately to P and Q. The mean saving follows by subtracting the new upper bound from the earlier lower bound. Each pair requires two launches. The comparison measures exposure in pairs and assigns no instrumental or computational cost to evaluating a checkpoint. No physical detector observations were acquired.
