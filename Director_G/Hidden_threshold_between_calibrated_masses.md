# A hidden threshold between two calibrated masses

Research note for Director G, prepared by OpenAI Codex for Kirtus Justus. Gate OP-27.

The [paired-read supplement](Paired_reads_for_a_type_dependent_target.md) bounds the transfer of calibration to a mass chosen using the detector type. On the tick-256 menu, a complementary, monotone detector can pass every node pair and have the ordinary population mean at **every fixed mass**, while producing a positive science-rate bias of 0.01621264309. The construction gives a lower bound on what can escape these checks. The sharp optimum over all detectors is open.

## Construction and proof

Take a largest gap [a,b] in the lower half of the calibration mesh. Write h=b−a and c=(a+b)/2. Draw a hidden threshold T uniformly in (a,b) once per detector type. On this gap the type response is a below T and b above T. At T itself choose b when T≤c and a otherwise. Reflect the response by g(1−s)=1−g(s) on the opposite gap. Set g(s)=s everywhere else. Each curve is monotone, complementary, endpoint-faithful and correctly calibrated at all nodes.

At any fixed s in the lower gap, the probability of the upper endpoint response is (s−a)/h. Thus the mean is s. The reflected gap and the rest of the interval have the same ordinary mean. The endpoint probabilities are those of unbiased stochastic rounding. The threshold shared across settings specifies a joint response curve, which matters when a target can depend on the type. [Connolly, Higham and Mary](https://doi.org/10.1137/20M1334796)

Compare this detector with the ordinary response g(s)=s. At every menu node each type in both models has the same binary success rate s. With independent binary draws conditional on type, even the full pair tables agree there. The same holds for any finite number of such repeats.

Choose S=T when T≤c, and S=1−T otherwise. The signed error is b−T on the first half and T−a on the second. Averaging gives 3h/4. This is a positive bias in the unconditional rate, with every trial counted. The point convention at a jump matters for this attained value. If a fixed convention is required, select just above T on the first half and the reflection of a point just below T on the second. A displacement ε with 0<ε<h/2 gives 3h/4−ε and avoids all ties. The assumed ability to correlate the target this precisely with the type is a premise of the rival.

## A discriminating record

Prepare the interior mass c independently of T and repeat it twice with the same T and conditionally independent binary draws. The ordinary detector predicts a centered pair score of zero. The threshold detector predicts h²/4 since its conditional response differs from c by ±h/2. More generally an interior point s has score (s−a)(b−s), maximized at c. A fresh threshold on each read removes this discriminator. A randomized mixture of the existing endpoint masks also fails to implement a fixed interior mass on each incident trial.

For the [tick-256 mask data](results/echo_probability_map.json), a≈0.239027918813 and b≈0.260644776272. The predicted centered pair score at c≈0.249836347542 is 0.000116822132. The paired-read supplement gives the zero-moment upper bound h under its premises, so the worst possible absolute mean bias under the additional fixed-mass population constraint lies between 3h/4 and h. The same calculation with the target independent of T gives zero unconditional signed bias at every exposure. This is a classical latent-detector rival on the same scalar masses. It supplies neither a microscopic detector dynamics nor a classical limit of the walk.

The [exact checker](check_threshold_target.py) recovers the gap from the routed masks using rational arithmetic and checks the node responses, a finite set of fixed-mass means, the selected bias, and the midpoint prediction. Its 64 threshold midpoints integrate the two affine branches of the bias exactly. The continuous fixed-mass statement follows from the uniform-threshold proof. No physical paired observations, preparation of c, or empirical type-target coupling are claimed.
