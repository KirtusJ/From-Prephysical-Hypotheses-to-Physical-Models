# Calibrating a detector when the target mass depends on its hidden state

**Kirtus Justus**, Theoretical Physicist, Port Coquitlam, British Columbia, Canada. Research supplement by Director G (OpenAI Codex).

A site detector can give the ordinary mean rate at every calibrated mass and still bias a science measurement whose mass depends on the detector's hidden state. Two reads at the same known mass can measure the missing quantity. They must share the detector state while drawing their outcomes separately. A finite mask menu then gives a bound on the science error. No such paired walk data have been acquired.

## The observable on two launches

Let \(A\) denote conditions shared by a pair of launches, and \(g_A:[0,1]\to[0,1]\) the binary response to a **pooled** kinematic mass. Assume each response is nondecreasing and endpoint-faithful. A stronger result uses per-type complementarity \(g_A(1-s)=1-g_A(s)\). A stable mass-only meter with a fresh independent physical interchange and decoding on each read can supply this symmetry. Sharing a random interchange across a pair can correlate the outcomes.

Choose a known mass \(s\) independently of \(A\). Prepare it twice and record both original-incident hit indicators \(X,Y\). Each must have conditional mean \(g_A(s)\). Conditional independence, or just zero conditional covariance, gives
\[
 \mathbb E[(X-s)(Y-s)\mid A,s]=(g_A(s)-s)^2.
\]
An independently redrawn type on the second trial gives \((\mathbb E_Ag_A(s)-s)^2\) when the two trials are independent. For shared types the residual conditional covariance adds to the right-hand side. A verified **lower** bound \(-\kappa\) on its average permits the upper correction \(+\kappa\) to the observed score. For example, equally frequent types with probabilities \(3/16,5/16\) at \(s=1/4\) give a paired score of \(1/256\). Independently redrawn types give zero. Valid joint outcome tables of shared types with conditional covariance \(-1/256\) also give zero. [Earlier comparison at one site bin](Fluctuating_site_scores_and_paired_launches.md) · [Limits of repeated measurements on an evolving mode](Shared_gain_in_repeated_phonon_checks.md)

The sign-and-return comparison can constrain the population curve \(G(s)=\mathbb E_Ag_A(s)\). Here the target mass \(S_A\) can depend arbitrarily on the type, with the same type population and the same response law in calibration and science. Additional target randomness is allowed. We bound the mean absolute error \(\mathbb E|g_A(S_A)-S_A|\), which bounds the bias in the unconditional predicted science rate. [Population echo test](Checking_probability_by_reversing_a_shell_sign.md)

## From a moment to a science-error bound

Write \(e(s)=g(s)-s\) for a single curve and \(d=|e(s)|\). If \(e(s)>0\), monotonicity gives \(e(s+v)\ge d-v\) on \(0\le v\le d\). If \(e(s)<0\), then \(-e(s-v)\ge d-v\) on the corresponding left interval. The unit range keeps the interval inside the domain. Integrating the squared triangle gives
\[
 |g(s)-s|^3\le 3\int_0^1(g(y)-y)^2\,dy .
\]
This holds for the supremum even for curves with jumps. For a complementary curve, monotonicity and \(g(1/2)=1/2\) keep \(s\) and \(g(s)\) on the same half of the domain. Reflecting the triangle into the other half gives coefficient \(3/2\). Both constants are sharp. Put one upward jump from the identity to \(a+d\) at \(a\), hold that height until \(a+d<1/2\), then resume the identity. The squared area is \(d^3/3\). Reflect the excursion with opposite sign for the complementary case.

For \(m=2^k,\ k\ge1,\ h=1/m\), choose \(J\) uniformly in \(\{1,\ldots,m\}\) and set \(s=Jh\). The missing zero node has zero error by endpoint faithfulness. Thus
\[
 M=\mathbb E[(X-Jh)(Y-Jh)]=h\sum_{j=0}^{m}\mathbb E_A e_A(jh)^2.
\]
There are exactly \(m\) assignment labels, including the endpoint one. For a positive excursion \(d>h\), round \(y\in[s,s+d-h]\) up to its next grid node \(jh\). Then \(e(jh)\ge d-h-(y-s)\). Each node covers at most length \(h\). Integrating gives \((d-h)_+^3/3\le h\sum_j e(jh)^2\); negative excursions use downward rounding. The grid and its reflection have equal weights. In the complementary case the two squared triangles lie in opposite halves and their only possible common node is the error-free midpoint. Taking expectations and using concavity of the cube root gives
\[
 \mathbb E|g_A(S_A)-S_A|\le h+(KM)^{1/3},
 \qquad K=3\ \text{in general},\quad K=3/2\ \text{with per-type complementarity}.
\]
If a herald selects a fraction \(y>0\) of incident launches, the nonnegative full-grid moment averaged over their types is at most \(M/y\). The conditional science bound uses \(M/y\), provided the post-herald response of each type is still the calibrated one.

**Routed walk masks.** The tick-256 walk supplies scalar masses common to all coin states. The [actual shell masks](results/echo_probability_map.json) and their complements give 66 distinct nodes. Per-type complementarity supplies a zero-error midpoint anchor. These 67 nodes, including the endpoints, have maximum gap \(h<0.021617\). No physical half-mass mask is required for this calculation. For unequal node spacings, sample a gap with probability equal to its width, then choose either bounding node fairly. Each node's weight \(w_i\) is half the sum of its neighboring gaps, including just one gap at each end. The zero-error anchor contributes zero to this assignment. Use a recorded control assignment for such virtual nodes.

Define \(M_w=\sum_i w_i\mathbb E e_A(x_i)^2\). Rounding upward assigns each node its left gap as weight, while downward rounding assigns its right gap. These directed sums agree for every complementary curve on the symmetric mesh, and each equals the sum with weights \(w_i\). Using one directed triangle gives the safe certificate \(h+(3M_w)^{1/3}\). Equal spacing permitted the tighter two-triangle count above. Gaps between actual scalar masks determine the resolution of this experiment.

## Incident accounting and finite exposure

One pair is one statistical unit. For fixed \(s\), its signed score takes the values \(s^2,\,-s(1-s),\,(1-s)^2\). Record every assigned pair, setting, original launch and unresolved bit. For missing bits under a complete binary model, taking the maximum score over possible completions bounds the complete-data mean from above. A source loss that changes the underlying outcome law requires a separate model.

For \(B\) independent pair blocks with the stipulated population and assignment weights, a one-sided upper limit on the mean complete-pair score at failure probability \(\alpha\) is the observed mean upper score plus \(\tfrac54\sqrt{\log(1/\alpha)/(2B)}\). The score range \([-1/4,1]\) gives the factor \(5/4\). Apply any justified covariance correction and clip the resulting upper moment to \([0,1]\). Consecutive pairs from one drifting detector require a dependence analysis. [Hoeffding, Theorem 2](https://doi.org/10.1080/01621459.1963.10500830)

## A detector that hides its bias at a moving mass

Take \(C\) uniform on \([1/8,3/8]\), an independent fair sign \(\sigma\), and \(0<r\le1/8\). Write \(t_C(s)=(r-|s-C|)_+\), \(f_C(s)=t_C(s)-t_C(1-s)\) and
\[
 g_{C,\sigma}(s)=s+\sigma f_C(s).
\]
Each piecewise-linear response has slopes drawn from \(0,1,2\), is complementary, and takes the correct endpoint values. At every fixed mass its population mean is exactly ordinary. Choose the science mass \(S=C\) for positive sign and \(S=1-C\) for negative sign. Then \(g_{C,\sigma}(S)-S=r\) on every launch.

For every type the integrated squared error is \(4r^3/3\). At any fixed \(s\), only one reflected half contributes. Integrating its squared tent over centers of density four gives a pointwise population second moment at most \(8r^3/3\), with equality at \(s=1/4\). Thus even exact population calibration together with a uniform pointwise moment bound cannot improve the cube-root exponent. For a finite blind spot, use \(h=1/8,\ C=3/16,\ r=1/16\) and the same two signs. All grid singles and same-type independent pairs agree with the ordinary model. The type-dependent target has bias \(h/2\).

This detector is a rival for calibration transfer. The physical requirements still open are the repeatable type, its conditional pair covariance, scalar preparation, and actual incident outcomes under the pooled read. [Exact checker](check_paired_curve_calibration.py) · [Inputs, results and counterexamples](results/paired_curve_calibration.json)
