# Deciding at a paired detector deadline

**Kirtus Justus**, Theoretical Physicist, Port Coquitlam, British Columbia, Canada. Research supplement prepared by OpenAI Codex for Director G.

Under the two specified lossless laws at fixed M = 10⁻⁸, repeat the [single selected mass](Stopping_on_paired_detector_evidence.md). Stop when the accumulated log likelihood first reaches or crosses either threshold ±a, or after N pairs, whichever comes first. Choose the law favored by the final likelihood, breaking ties by a fair coin. The following probabilities average the two conditional error probabilities with equal weights.

| Threshold a | Maximum pairs | Error probability |
|---|---:|---:|
| Original threshold ln(19) + b | 3.800950 quadrillion | 6.76043% to 6.76048% |
| 4 | 4 quadrillion | 4.89421% to 4.89427% |

Here b is the maximum absolute single-pair log increment at this mass. The second rule uses fewer than 2.708673 quadrillion pairs on average under each law. This conservative bound follows by ignoring the deadline when bounding exposure. Each pair requires two launches. These fixed choices illustrate the exposure tradeoff. Optimal thresholds and caps, individual error probabilities and applicability to physical detectors remain open.

### Comparing the information available at stopping

Use the [two-stage Brownian embedding](Adaptive_exposure_for_two_paired_detector_laws.md). Denote by S the clock after all N pairs, generating unused pairs if needed, and by U the clock when the discrete rule stops. Write H(w) for the first Brownian exit from (−w,w). Each pair stays within b of its starting log likelihood. Pathwise,

$$H(a)\wedge S\ \le U\ \le H(a+b)\wedge S.$$

Indeed the inner boundary must be hit before any discrete crossing. The outer boundary cannot be hit during a pair started strictly inside (−a,a). This comparison holds on paths with intra-pair crossings and returns.

Let t₋ and t₊ be N times the smaller and larger one-pair mean clocks across the laws. Use the [two clock tail bounds](Adaptive_exposure_for_two_paired_detector_laws.md) with K = 2b²/(1−b) and d = 0.000040. For the lower tail, the second moment bound Eτ² ≤ 2Km and exp(−x) ≤ 1−x+x²/2 give probability at most exp(−d²/(4Kt₊)) for S < t₋−d. The upper tail S > t₊+d costs at most exp(−d²/(4Kt₊+2Kd)).

At U the full Brownian experiment has likelihood ratio exp(X_U), which is exactly the discrete likelihood ratio. This follows by the stopped change of measure, since the stopped coordinate stays bounded by a+b; the independent tree coins have the same law under either hypothesis. Terminal likelihood-sign decisions therefore attain the same Bayes risk with either observation. An observer with a later stopping time can reproduce an earlier decision. For the earlier continuous experiment stopped at H(a) or t₋−d, the observer at U can copy its decision if that experiment has finished, and guess otherwise. The exceptional event is contained in the lower clock tail. Conversely the observer stopped at H(a+b) or t₊+d can copy the discrete decision except on the upper clock tail. Thus the wider, later experiment gives a lower bound after subtracting the upper tail, and the narrower, earlier experiment gives an upper bound after adding the lower tail.

### Risk at a continuous deadline

Under Q the coordinate has drift −1/2 and unit variance rate. With equal priors the error is the Q-expectation of min(1,exp(X))/2 at the stopping time. Inside either open half-interval this function has zero generator. At zero its derivative jumps by −1/2. The local-time term in the Itô–Tanaka formula therefore reduces expected error at rate one quarter of the surviving Q-density at zero. [Local time and the Tanaka formula, §5](https://galton.uchicago.edu/~lalley/Courses/385/ItoIntegral.pdf)

Starting at zero, the killed transition density there at clock u is the sum of exp(−rⱼu)/w for j ≥ 0, with rⱼ = 1/8 + ((2j+1)π/(2w))²/2. This is the absorbing interval cosine kernel multiplied by the drift factor exp(−u/8). At infinite time the error is 1/(1+exp(w)), from the two exit likelihoods and reflection of the drifts. Integrating the local-time reduction from a positive deadline t to infinity yields

$$R(w,t)=\frac{1}{1+e^w}+\sum_{j\ge0}\frac{e^{-r_jt}}{4wr_j}.$$

All terms are positive. The [checker](check_deadline_decision.py) bounds the remainder after six modes by a geometric series, since successive rate gaps are at least π²/w². It applies both clock tails before rounding. For the expected count it uses the uncapped likelihood-overshoot and Wald bounds from the single-mass analysis at a = 4. The calculation assumes a fresh independent latent type for each pair under the fixed model. No detector data were acquired.
