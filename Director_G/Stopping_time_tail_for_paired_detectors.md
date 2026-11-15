# How often a paired detector experiment runs past its budget

**Kirtus Justus**, Theoretical Physicist, Port Coquitlam, British Columbia, Canada. Research supplement prepared by OpenAI Codex for Director G.

The [single-mass sequential test](Stopping_on_paired_detector_evidence.md) has mean exposure about 1.86145 quadrillion pairs. Under either of the two specified laws at fixed M = 10⁻⁸, its chance of still running after 3.800950 quadrillion pairs is between 8.61824% and 8.61844%. Its 95th percentile lies above 4.51632 and at most 4.51636 quadrillion pairs. The chance of still running after five quadrillion pairs is between 3.46020% and 3.46029%, and after seven quadrillion between 0.75517% and 0.75520%. These are model probabilities for fresh independent pairs. A pair costs two launches. A decision forced at any of these deadlines would require a separate error analysis.

### Coupling the discrete stopping event to interval survival

Write a for the sequential log-likelihood threshold and b for the maximum absolute one-pair log increment at the selected mass. In the [Brownian simulation of a pair](Adaptive_exposure_for_two_paired_detector_laws.md), each relative coordinate during the pair lies in [−b,b]. Generate N pairs even if the sequential rule would already have stopped, and write S for their total Brownian clock. If the continuous path stays in (−a,a) through S, all N endpoints survive. If all endpoints survive, the continuous path stays in (−a−b,a+b) through S. This second inclusion accounts for excursions between observations.

Under each law, the iid clocks have mean m equal to twice the corresponding one-pair KL divergence and second moment at most 2Km, where K = 2b²/(1−b). Set t = Nm. The prior clock proof bounds the upper tail at t+d by exp(−d²/(4Kt+2Kd)). For the lower tail, exp(−x) ≤ 1−x+x²/2 for nonnegative x implies log E exp(−λ(τ−m)) ≤ Kmλ². Optimizing gives the lower-tail bound exp(−d²/(4Kt)). If H(w,u) denotes survival to time u in (−w,w), the discrete survival probability is at least H(a,t+d) minus the upper clock tail and at most H(a+b,t−d) plus the lower clock tail. No independence between S and path survival is needed.

### Computing continuous survival

For drift ±1/2 started at zero the two survival functions coincide by reflection. At zero drift, the absorbing heat kernel started at zero has even modes cos(kx)/w times exp(−uk²/2), with k = (2j+1)π/(2w), j starting at zero. This follows from the orthogonal Dirichlet eigenfunctions, each unnormalized cosine having squared norm w. Multiplication by exp(x/2−u/8) introduces positive drift. Integrating each mode from −w to w gives the term

$$(-1)^j\frac{2\cosh(w/2)}{w}\frac{k}{k^2+1/4}\exp[-u(k^2/2+1/8)].$$

The series is absolutely convergent for positive u. Its magnitudes decrease at both widths used here because the first k exceeds 1/2. The [interval checker](check_stopping_tail.py) encloses the sum using consecutive alternating partial sums and sets d = 0.000040. All five budget comparisons are checked separately under both laws. The percentiles describe this stopping rule only. No detector data were acquired.
