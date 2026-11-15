# Mean exposure at the four-quadrillion-pair deadline

**Kirtus Justus**, Theoretical Physicist, Port Coquitlam, British Columbia, Canada. Research supplement prepared by OpenAI Codex for Director G.

The [capped single-mass rule](Deciding_at_a_paired_detector_deadline.md) uses **2.39088144 to 2.39088270 quadrillion pairs on average** under either of the two specified detector laws. This saves about 40.23% on average relative to always collecting the four-quadrillion-pair cap, or 37.10% relative to the previously certified fixed design of 3.800950 quadrillion pairs. The latter fixed design has a smaller maximum. Each pair requires two launches. Thresholds, terminal decision and independent fresh-pair assumptions are the same as in the [conditional error analysis](Conditional_errors_at_a_paired_detector_deadline.md). No physical observations were acquired.

### Relating mean clock time to mean pair count

Fix one detector law. Write J for the number of pairs taken, N for the cap, U for the Brownian clock at J and S for the clock at N in the [pair embedding](Adaptive_exposure_for_two_paired_detector_laws.md). Generate any unused pairs after the decision. Each pair clock has mean m and second moment at most 2Km, with K = 2b²/(1−b) for maximum log increment b. Since entry into pair i depends only on earlier pairs, taking expectations in the finite sum of entered clocks gives E[U] = m E[J]. Independently generated clocks through the full cap give E[S] = t = Nm and Var(S) ≤ 2Kt.

Write H(w) for the first Brownian exit from (−w,w). The deadline proof sandwiches U between min(H(4),S) and min(H(4+b),S). For any H, replacing S by t in min(H,S) increases the expectation by at most E[(t−S)₊] and decreases it by at most E[(S−t)₊]. These are equal since E[S]=t, and each is at most sqrt(2Kt)/2 by Cauchy–Schwarz. This bound handles the dependence between S and H. With F(w,t) = E[min(H(w),t)], the resulting lower and upper bounds on E[J] are (F(4,t)−sqrt(2Kt)/2)/m and (F(4+b,t)+sqrt(2Kt)/2)/m.

### Evaluating the capped exit mean

Under either drift ±1/2, the uncapped mean Brownian exit time is 2w tanh(w/2). This follows by solving the mean exit equation with generator (f″ ± f′)/2, right-hand side −1 and zero boundary values. [Symmetric drift-diffusion exit mean](https://elifesciences.org/articles/49758)

Subtract the integral of the surviving probability from t to infinity. Integrating the absorbing interval cosine kernel at the origin against the drift tilt exp(x/2−u/8) gives the residual mean

$$\frac{2\cosh(w/2)}{w}\sum_{j\ge0}(-1)^j\frac{k_j e^{-r_jt}}{(k_j^2+1/4)r_j},\qquad k_j=\frac{(2j+1)\pi}{2w},\quad r_j=\frac{k_j^2}{2}+\frac18.$$

Absolute convergence at t>0 justifies integration. The term magnitudes decrease from j=1 onward at the two widths used here. The [interval checker](check_capped_mean.py) encloses the residual between consecutive partial sums ending at indices four and five and checks the reported mean interval under each law. This is a bound on the specified rule's mean, without an optimality claim.
