# Transfer to a type-dependent mass with nonzero node errors

**Kirtus Justus**, Theoretical Physicist, Port Coquitlam, British Columbia, Canada. Research supplement prepared by OpenAI Codex for Director G.

How much bias can remain when paired calibration reads permit small errors at the nodes? Assume the same detector-type population in calibration and science, monotone endpoint-faithful and complementary response curves, and exact population calibration at every fixed mass. Allow science targets to depend on type and to take values between the calibration nodes. The [zero-budget result](Hidden_threshold_between_calibrated_masses.md) assumes exact per-type node calibration. Here the paired moments bound the mean squared node errors. For the tick-256 mesh the upper limit tends to the sharp zero-budget value, and a construction shows that every positive budget permits a strictly larger bias. The rate at which the true optimum rises is open.

## A certificate from paired moments

Write $x_0=0<\cdots<x_n=1/2$ for the lower-half nodes, $h_i=x_i-x_{i-1}$ for their gaps, and $v_j=\mathbb E(g(x_j)-x_j)^2$. Endpoint faithfulness and complementarity give $v_0=v_n=0$. Under the symmetric gap-weighted assignment of the [paired-read protocol](Paired_reads_for_a_type_dependent_target.md), the combined weight of an interior node and its reflection is $W_j=h_j+h_{j+1}$. Thus the full moment is $M=\sum_{j=1}^{n-1}W_jv_j$. Reading it from a binary pair requires the shared-type and conditional covariance assumptions stated in that protocol. Here $M$ denotes a population moment or a valid upper limit on it.

Let $t$ and $B_0$ be the optimal zero-budget cutoff and bias, and put $q_i=(1-t/h_i)_+$ and $c_j=(q_j+q_{j+1})/2$. If the node moments are separately available, a uniform bound on the adaptive mean absolute error is

$$
B_0+\sqrt{\sum_{j=1}^{n-1}v_j}+\sum_{j=1}^{n-1}c_j\sqrt{v_j}.
$$

With only the aggregate budget this is at most

$$
B_0+\left(\frac{1}{\sqrt{\min_j W_j}}+
\sqrt{\sum_j c_j^2/W_j}\right)\sqrt M .
$$

**Derivation.** Clip the type response in each mass gap $[a,b]$ to that same interval. Monotonicity bounds the absolute change by the largest absolute error at any node on that type. Its expectation is at most the square root of the sum of the node moments on the lower half, since reflection preserves magnitudes. At a fixed interior mass $z$, the clipped population response differs from $z$ by
$\mathbb E(a-g(z))_+-\mathbb E(g(z)-b)_+$. This difference lies between $-\mathbb E(g(b)-b)_+$ and $\mathbb E(a-g(a))_+$.

Threshold-randomize the clipped curve in vertically rescaled coordinates as in the zero-budget proof, assigning an all-upper step to a crossing at $a$ and an all-lower step to $b$. If $T$ is this crossing, its CDF in the gap is the rescaled mean clipped response at continuity points. For $D=\max(T-a,b-T)$ and $h/2\le u<h$, the event $D>u$ consists of two disjoint tails, at $b-u$ and $a+u$. Relative to a uniform crossing, their total probability increases by at most
$[\mathbb E(a-g(a))_++\mathbb E(g(b)-b)_+]/h$. One-sided limits cover atoms; individual threshold levels do not affect the tail integral. Integrating from $t$ to $h$ costs at most $q_i$ times this sum of one-sided node errors. When $h\le t$ the cost is zero. Conditional averaging of the steps bounds the clipped curve's excess over $t$ by the step excess. Sum over gaps as in the zero-budget proof. Exact population calibration makes each one-sided node mean equal to half the mean absolute error there, at most $\sqrt{v_j}/2$. Grouping neighboring gaps yields the first bound. Weighted Cauchy–Schwarz gives the aggregate form.

## An attainable increase

Remove one interior node $x_j$ and its reflection from the *construction*, while continuing to test them in calibration. Apply the attaining threshold coupling to the merged mesh. All fixed-mass population means still equal their inputs. The only errors on the original nodes occur at the omitted pair. At $x_j$ the response is one of its two neighbors, with mean $x_j$, hence has variance $h_jh_{j+1}$. The full moment cost is $M_j=W_jh_jh_{j+1}$. Let $B_j$ be the sharp adaptive bias on the merged mesh. Mixing this population with the original zero-cost extremizer in proportion $\lambda=\min(1,M/M_j)$ realizes bias $B_0+\lambda(B_j-B_0)$. The target can depend on the mixture label, as allowed by the original type-dependent protocol. Every trial is counted.

On the actual menu, comparing each of the 32 interior deletions gives the steepest initial increase for $x_{23}=0.339023657794\ldots$ and its reflection. Its full cost is $0.0000146089538636\ldots$ and the initial slope is $643.96943195\ldots$. The aggregate upper coefficient is $16.80774605\ldots$. At budget $10^{-8}$ the attainable bias is about **1.982908 percentage points** and the uniform upper bound is about **2.150342 percentage points**. These numbers bound the worst case under the hypotheses. They are not observed detector performance. The lower slope is optimal only among the tested single-node deletions. No sharp finite-budget constant or exponent is asserted.

As a discriminator for this particular mixture, repeat the original omitted node twice with the same type and conditionally independent binary outcomes. The predicted centered score there is $\lambda h_jh_{j+1}$, versus zero for the zero-cost extremizer. Measuring that score does not itself establish fixed-mass population calibration everywhere or physical coupling of science target to detector type. The [exact coefficient checker](check_finite_moment_gap.py) uses the routed mask numerators and verifies the node cost by a direct binary calculation. Its printed bias estimates are rounded. The equations above give the bounds. A same-family second reader received the proposed upper inequality and checked the clipping, tail signs and endpoint atoms. No empirical data or formal proof assistant was used.
