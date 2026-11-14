# A hidden threshold between two calibrated masses

**Kirtus Justus**, Theoretical Physicist, Port Coquitlam, British Columbia, Canada. Research supplement prepared by OpenAI Codex for Director G.

At tick 256, the 33 routed masks and their complements give 66 distinct calibration masses. The 67th node, $1/2$, is a virtual anchor fixed by per-type complementarity. Exact per-type calibration makes the science-rate bias zero for any choice among these 67 nodes, even when the choice depends on the detector type. [Paired-read calibration and the midpoint anchor](Paired_reads_for_a_type_dependent_target.md)

What if the science target can be set **between** those masses using information about the detector type? A monotone, complementary detector with the ordinary population mean at every fixed mass can then produce a bias of 0.01621264309 using one gap and its reflection. Over all gaps the sharp bias is 0.019822640675, or about 1.98226 percentage points. Both numbers assume access to the specified type-dependent targets. This tests what finite calibration can establish about the [P5 probability rule](ontology_gate_map.json).

## Construction and proof

Take a largest gap [a,b] in the lower half of the calibration mesh. Write h=b−a and c=(a+b)/2. Draw a hidden threshold T uniformly in (a,b) once per detector type. On this gap the type response is a below T and b above T. At T itself choose b when T≤c and a otherwise. Reflect the response by g(1−s)=1−g(s) on the opposite gap. Set g(s)=s everywhere else. Each curve is monotone, complementary, endpoint-faithful and correctly calibrated at all nodes.

At any fixed s in the lower gap, the probability of the upper endpoint response is (s−a)/h. Thus the mean is s. The reflected gap and the rest of the interval have the same ordinary mean. The endpoint probabilities are those of unbiased stochastic rounding. The threshold shared across settings specifies a joint response curve, which matters when a target can depend on the type. [Connolly, Higham and Mary](https://doi.org/10.1137/20M1334796)

Compare this detector with the ordinary response g(s)=s. At every menu node each type in both models has the same binary success rate s. With independent binary draws conditional on type, even the full pair tables agree there. The same holds for any finite number of such repeats.

Choose S=T when T≤c, and S=1−T otherwise. The signed error is b−T on the first half and T−a on the second. Averaging gives 3h/4. This is a positive bias in the unconditional rate, with every trial counted. The point convention at a jump matters for this attained value. If a fixed convention is required, select just above T on the first half and the reflection of a point just below T on the second. A displacement ε with 0<ε<h/2 gives 3h/4−ε and avoids all ties. The assumed ability to correlate the target this precisely with the type is a premise of the rival.

## A discriminating record

Prepare the interior mass c independently of T and repeat it twice with the same T and conditionally independent binary draws. The ordinary detector predicts a centered pair score of zero. The threshold detector predicts h²/4 since its conditional response differs from c by ±h/2. More generally an interior point s has score (s−a)(b−s), maximized at c. A fresh threshold on each read removes this discriminator. A randomized mixture of the existing endpoint masks also fails to implement a fixed interior mass on each incident trial.

For the [tick-256 mask data](results/echo_probability_map.json), a≈0.239027918813 and b≈0.260644776272. The predicted centered pair score at c≈0.249836347542 is 0.000116822132. The paired-read supplement gives the zero-moment upper bound h under its premises, which provides a general upper bound for comparison with the sharp result below. The same calculation with the target independent of T gives zero unconditional signed bias at every exposure. This is a classical latent-detector rival on the same scalar masses. It supplies neither a microscopic detector dynamics nor a classical limit of the walk.

The [exact checker](check_threshold_target.py) recovers the gap from the routed masks using rational arithmetic and checks the node responses, a finite set of fixed-mass means, the selected bias, and the midpoint prediction. Its 64 threshold midpoints integrate the two affine branches of the bias exactly. The continuous fixed-mass statement follows from the uniform-threshold proof. No physical paired observations, preparation of c, or empirical type-target coupling are claimed.

## Sharp bias for targets between calibration nodes

Assume a finite symmetric mesh containing both endpoints and the midpoint, exact per-type agreement at its nodes almost surely, monotonicity, per-type complementarity and population mean identity at every fixed mass. Zero shared-type pair moments with zero conditional covariance imply the node assumption. The target may depend measurably on the whole response curve. A positive bias and the expected absolute error have the same sharp upper limit because reflection reverses the sign of the pointwise error.

Write $h_i$ for the widths of the lower-half gaps. For a uniform location $T_i$ in $[0,h_i]$, define $D_i=\max(T_i,h_i-T_i)$. Its marginal distribution is uniform on $[h_i/2,h_i]$. No independence between gaps is imposed. Choose $t$ with $\sum_i P(D_i>t)=1$. Such a cutoff exists at or above half the largest width by continuity. With a single contributing gap one can use half its width. The sharp mean bias is

$$
B=t+\sum_{h_i>t}\frac{(h_i-t)^2}{h_i}.
$$

**Upper bound.** In a gap $[a,a+h]$, rescale each type's response to $f(x)=(g(a+hx)-a)/h$. For a fresh uniform $U$, the random binary step $1\{U\le f(x)\}$ has conditional mean $f(x)$. Its crossing location has uniform marginal distribution: at fixed $x$, the population mean of $f(x)$ is $x$, and evaluating on either side gives the same marginal crossing probability in the limit. Monotonicity confines any choice at the jump to the two one-sided limits. The supremum error of the step in mass units is therefore $D$ irrespective of its tie convention. If $L$ is the original curve's supremum error in this gap, conditional averaging and convexity give $\mathbb E(L-t)_+\le\mathbb E(D-t)_+$. Suprema are measurable using rational points and endpoints since monotone curves have one-sided limits. Complementarity covers the reflected gaps. Pointwise, $\max_i L_i\le t+\sum_i(L_i-t)_+$. Integrating the uniform excess on each active gap gives the displayed formula.

**Attainment.** Partition type space into events of probabilities $p_i=P(D_i>t)$. On event $i$, draw $D_i$ from its upper tail and each other $D_j$ from its lower tail. Ignore zero-probability cases. This preserves every required marginal and makes exactly one gap exceed $t$ almost surely. Convert each distance to a uniform crossing by taking $T_i=D_i$ or $h_i-D_i$ with equal probabilities. Use the endpoint-step response of the preceding construction in every gap and reflect it. On each incident trial choose the winning threshold, or its reflection, with the sign and jump value giving positive error $D_i$. Its expectation is $B$. A fixed one-sided jump convention gives the same supremum by arbitrarily close targets. This construction pairs the extreme responses across gaps through a shared type. Separate fixed-mass singles cannot reveal that dependence.

**Tick 256.** Of 33 lower-half gaps, 11 contribute at $t=0.019079203740\ldots$. The sharp value is $B=0.019822640675\ldots$, strictly below the largest gap $0.021616857458\ldots$. The [rational checker](check_multigap_bias.py) verifies both the integrated excess and the conditional winning-gap mean and checks the equal-two-gap control by enumerating all permutations of four midpoint ranks. The one-gap answer is $3h/4$; for two equal gaps it is $7h/8$.

This is an extremum over admissible detectors and adaptive targets. Independence of target and type gives zero signed bias instead. Experimental access to a type-dependent target and the finite-sample case with nonzero calibration moments remain open. A second Codex reader saw the proposed formula and hypotheses and independently checked the upper bound, coupling and tie convention. The proof has not been formalized in Lean.
