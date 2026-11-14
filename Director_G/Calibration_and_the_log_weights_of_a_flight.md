# When a probability-power calibration transfers to a resolved flight profile

**Kirtus Justus**, Theoretical Physicist, Port Coquitlam, British Columbia, Canada. Research supplement by Director G (OpenAI Codex).

The [addressed-walk test](Three_signed_ticks_and_the_probability_power.md) gives a nonnegative population score \(D\) with a known dependence on the detector exponent. A flight may have far more resolved outcomes than the calibration. The following bound depends on the variation of the logarithm of the flight weights. It can stay finite as the number of outcomes grows. This gives a condition under which a calibrated readout preserves either a Schrödinger position profile or concentration around a Newtonian position. The flight dynamics and source still need their own justification. [Forced envelope and classical position](Forced_envelope_and_classical_motion.md)

## The conditional bound

Allow the launch variable \(A\) to determine the normalized ordinary flight distribution \(p_A\), its scored cells and its exponent \(q\), or to select fair path counting in the calibration. Within a powered type the flight read applies a single terminal weighting \(T_s p=p^s/Z_s\), \(Z_s=\int p^s\,d\nu\), at \(s=q\). Use counting measure on discrete cells, including any hidden cells normalized before returning a site. For a continuous density specify the reference measure \(\nu\) as part of the readout. Remove zero cells from the powered support. A detector selecting the maximum or using counting on the calibration may report any flight law for purposes of this bound. Random assignment or a separate transfer result must justify the same distribution of calibrated types on the flight population. The scientific target is the mixture of the corresponding ordinary flight laws \(\mathbb E p_A\).

Choose \(0<h<1\). For each powered type with \(|q-1|\le h\), assume that \(Z_s\) is finite and positive on an open interval containing \([1-h,1+h]\) and that
\[
\sup_{s\in[1-h,1+h]} {\rm Var}_{T_s p_A}(\log p_A)\le V .
\]
These conditions are automatic as to existence on any finite positive support. The magnitude and uniformity of \(V\) across launches require a bound. A usable flight law is also required outside this interval whenever such a type occurs. On infinite counting measure \(Z_0\) can diverge. The claim there allows arbitrary output on the far types.

Then the total variation distance between the measured flight and the ordinary comparison obeys
\[
d_{\rm TV}\le
\min\!\left(1,\,
\frac{\max(1,h\sqrt V/2)}{1-9^{-h}}\sqrt{17D}\right).
\tag{1}
\]
For \(D\), use the true calibration population mean, or a justified upper bound after accounting for loss and sampling. All probabilities refer to matched incident populations or to a single specified accepted cohort. For example, a rare herald can enrich an otherwise rare exponent. [Calibrating on the cohort that flies](Checking_a_heralded_flight_word.md)

**Derivation.** Differentiating the normalized density gives
\[
\partial_s T_sp=(T_sp)\{\log p-\mathbb E_{T_sp}\log p\}.
\]
Finiteness of \(Z_s\) on a slightly wider interval supplies an integrable majorant for the log factors by bounding them with neighboring powers above and below \(p=1\). Integration and Cauchy–Schwarz give \(d_{\rm TV}(T_qp,p)\le |q-1|\sqrt V/2\) on the indicated interval. This is the exponential-family information-length estimate applied to the flight weights. [Crooks, *Measuring thermodynamic length*](https://doi.org/10.1103/PhysRevLett.99.100602)

For a finite \(q\) put \(g(q)=1-9^{-|q-1|}\); set \(g=1\) for counting or a limiting maximum rule. The calibrated score per type satisfies \(g^2\le17 D_A\). For \(u=|q-1|\le h\), concavity gives \(1-9^{-u}\ge (u/h)(1-9^{-h})\). For \(u\ge h\), the trivial distance bound one is at most \(g/(1-9^{-h})\). Thus the right-hand factor in (1), before the square root, times \(g\) bounds the distance, also at \(q=1\) where both vanish. Average over types, use \(\mathbb E g\le\sqrt{\mathbb E g^2}\), and project to any reported site bins. The same bound survives this projection.

## A resolved Gaussian and a check with no uniform bound

For a one-dimensional normal position law of mean \(m\) and variance \(v>0\) relative to Lebesgue measure in a specified affine position coordinate, \(T_sp\) is normal with the same mean and variance \(v/s\). Writing \(\log p=\mathrm{constant}-(x-m)^2/(2v)\) gives \({\rm Var}_{T_s p}(\log p)=1/(2s^2)\). This bound is independent of \(v\), including along a sequence \(v\downarrow0\). At \(h=1/2\) equation (1) gives \(d_{\rm TV}\le\min(1,3\sqrt{17D}/2)\). Ordinary spreading at fixed \(v\) changes if the exponent changes. A shrinking packet can still converge weakly to the correct point at any fixed \(q>0\), since \(v/q\to0\). Observing the limiting center alone therefore cannot certify the readout power. This is an exact calculation on the ideal density; it makes no assertion about powers applied to experimental pixel masses or the lattice tails of an approximate Gaussian. [Native Gaussian envelope and its stated limit](Folded_field_and_native_gaussian.md)

The variance condition is substantive even on finite supports. Give one cell mass \(1/2\) and let \(2^k\) other cells share the remaining half equally. At \(s=1\), the variance of \(\log p\) is \((k\log 2)^2/4\). Keeping \(q=1+1/k\) assigns the many-cell group exactly \(1/3\) for every \(k\), so its total variation distance from ordinary is \(1/6\). Meanwhile the addressed calibration is a smooth positive-normalizer square at \(q=1\) and \(D=O(k^{-2})\). This is the earlier flight refinement control with the new calibration inserted. The finite replay also includes the reverse perturbation \(q=1-1/k\) for which the group has weight \(2/3\). [Original word-refinement example](Checking_a_heralded_flight_word.md#how-a-small-exponent-error-affects-complete-words)

If a sequence of actual flight preparations satisfies a uniform variance bound and \(D\to0\), (1) tends to zero. For positions this preserves any proved weak limit of the ordinary law. It gives neither convergence of unbounded moments nor an amplitude phase, dynamics, or a joint path from one-time positions. A change of continuous reference measure can change the powered law, so the Gaussian example cannot specify which physical degrees of freedom a detector scores. The [replay](check_flight_log_weights.py) retains the forward and reverse perturbations, the original calibration masses and finite checks of the Gaussian and variance formulas. [Numerical records](results/flight_log_weights.json)
