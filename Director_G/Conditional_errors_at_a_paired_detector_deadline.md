# Both detector models meet the deadline error target

**Kirtus Justus**, Theoretical Physicist, Port Coquitlam, British Columbia, Canada. Research supplement prepared by OpenAI Codex for Director G.

For the [four-quadrillion-pair deadline rule](Deciding_at_a_paired_detector_deadline.md), the probability of a wrong decision lies between **4.85860% and 4.92988% under each model**. The two conditional probabilities can differ by at most 0.07123 percentage points. The test uses the same mass, thresholds ±4, terminal likelihood sign and fair tie-breaking as in the deadline study. The bounds apply to the two specified lossless populations at fixed M = 10⁻⁸, with fresh independent pairs. No detector data were acquired.

### Separating the errors with nearby priors

Let α and β be the probabilities of error under P and Q, let R = (α+β)/2, and let D = (α−β)/2. Under prior weights (1±h)/2 for P and (1∓h)/2 for Q the **same** discrete decision has risk R±hD. Each of these risks must exceed or equal the optimum for a more informative experiment, up to the clock overflow allowance. This gives two inequalities on D even though the discrete laws need not be reflections of each other.

Use the wider continuous observer from the deadline proof, with width 4+b and time t equal to the larger mean clock plus d. Write C for its equal-prior optimal error. The observer can reproduce the discrete decision except on the overflow event. Its probability under either law is at most ε, the uniform upper clock-tail bound. Consequently R±hD is at least the wider observer's corresponding optimal risk minus ε.

For that continuous observer, drift reflection makes both conditional errors of the sign rule equal to C. Keeping that rule therefore costs C at either changed prior. An optimal changed-prior rule moves the log-likelihood cutoff by magnitude c = log((1+h)/(1−h)). This can improve risk only in a one-sided interval between zero and the new cutoff. On this interval the improvement integrand relative to Q is the absolute difference of the two weighted likelihoods, at most h by monotonicity of the exponential and equality at the shifted cutoff. The exit atoms are outside this interval since c < 4. The surviving Q-density is bounded by the unrestricted normal density of drift −1/2 at time t, hence by exp(−t/8+c/2)/sqrt(2πt) throughout the interval. The changed-prior optimum is therefore at least C−G, where G is h times c times this density ceiling.

Let L = C−ε and let U be the earlier upper bound on equal-prior discrete risk. Then R−h|D| ≥ L−G and R ≤ U give |D| ≤ (U−L+G)/h. Both conditional errors lie between L−|D| and U+|D|. With h = 0.004, the [interval checker](check_conditional_deadline.py) shows |D| < 0.000356115. It uses the continuous-risk series and both clock tails from the deadline proof. The nearby priors enter only in this proof. Neither experimental settings nor decisions depend on them.
