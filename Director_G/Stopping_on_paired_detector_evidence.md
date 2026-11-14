# Expected exposure when a pair experiment can stop on its evidence

**Kirtus Justus**, Theoretical Physicist, Port Coquitlam, British Columbia, Canada. Research supplement prepared by OpenAI Codex for Director G.

Use the [two specified detector laws](Exposure_for_two_paired_detector_laws.md) at the same known budget $M=10^{-8}$ with fresh independent types across pairs and both incident outcomes retained. Let $P$ denote the global tent and $Q$ the localized tent. With equal priors, minimize $(E_P\tau+E_Q\tau)/2$ over sequential tests with average classification error at most 5%. Mass selection may use past outcomes. The infimum, in quadrillion pairs, lies strictly between **1.861452480** and **1.861453214**. The constructive upper bound controls both conditional errors. Runs have no imposed length limit.

### Information required by the final decision

Let $\alpha=P(\text{choose }Q)$, $\beta=Q(\text{choose }P)$, and $e=(\alpha+\beta)/2$. Each direction of the stopped transcript's KL divergence dominates the corresponding divergence of the binary decision. Swap the two label names for the reverse direction. Joint convexity of binary KL then bounds the mean of the two decision divergences below by
$$d(1-e\Vert e)=(1-2e)\log((1-e)/e).$$
Indeed the two terms before combining are $d(1-\alpha\Vert\beta)$ and $d(1-\beta\Vert\alpha)$. For $e\le0.05$ the lower bound is at least $0.9\log19$.

The stopped log likelihood is the sum of the one-pair log ratios. The common policy's action and stopping probabilities cancel along the realized history. Given the past, each conditional expected log increment under $P$ is the chosen mass's forward KL, and under $Q$ its negative has the reverse KL. Informative increments are uniformly bounded on this finite menu; identical-law controls carry no information. Thus finite mean stopping permits summation by conditioning on each step still being taken. Infinite prior-averaged mean already satisfies the lower bound. If $D_*$ is the largest of either directional one-pair KL over all masses, then
$$ (E_P\tau+E_Q\tau)/2 \ \ge\ 0.9\log(19)/D_*.$$
Here $D_*\approx1.42361683104\times10^{-15}$ nats per pair.

### An explicit rule that almost attains the bound

Repeat mass $s=0.123279641138\ldots$. Let $L$ accumulate $\log(P_s(z)/Q_s(z))$ over the observed pair outcomes. Stop at the first exit from $(-a,a)$ and choose $P$ at the upper exit and $Q$ at the lower exit. Set $a=\log19+b$, where $b$ bounds the largest absolute one-pair increment at this mass (about $3.795\times10^{-7}$). This is a sequential probability-ratio test. [Background on the sequential probability-ratio test](https://philsci-archive.pitt.edu/11155/1/How_Much_Evidence_Should_One_Collect.pdf)

For $\tau\wedge n$, Wald's expectation identity and $|L_{\tau\wedge n}|\le a+b$ give a uniform bound on the truncated mean time under each law, because both directional divergences are positive. Hence the test terminates almost surely with finite means. Under $Q$ the stopped likelihood has expectation one; under $P$ its reciprocal has expectation one, by bounded convergence from the truncated times. The exit values consequently put *each* conditional error between
$$
l=\frac{1-e^{-a}}{e^{a+b}-e^{-a}},\qquad
u=\frac{1-e^{-a-b}}{e^a-e^{-a-b}}.
$$
The computed interval lies inside $(0.0499999629,0.0499999830)$. The expected signed log likelihood toward the true model at exit is at most $a+b-(2a+b)l$ under either model. Dividing by each directional KL bounds the two expected stopping times. Their average gives the reported upper endpoint. The [60-decimal interval checker](check_sequential_exposure.py) uses the earlier rational cell probabilities and checks both endpoints with outward margins. A same-family second reader checked the stopped-information argument, sign conventions and overshoot bounds.

The demonstrated mean is about 51% below the earlier [necessary deterministic cap](Adaptive_exposure_for_two_paired_detector_laws.md). These are different exposure criteria: an individual sequential run can exceed the fixed cap. The result supplies neither an exposure quantile nor a laboratory time forecast. It applies to these two fully specified populations; no empirical detector data entered the calculation.
