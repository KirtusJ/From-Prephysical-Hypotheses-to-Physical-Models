# What a pilot-controlled preparation measures

**Kirtus Justus**, Theoretical Physicist, Port Coquitlam, British Columbia, Canada. Research supplement by Director G (OpenAI Codex).

A hit or miss can choose the next preparation in the walk. The [single-gap threshold experiment](Threshold_pilot_and_adaptive_preparation.md) predicts a rate excess for that choice. Randomizing the science preparation after observing the pilot lets us measure the value of feedback for any binary detector. Under additional assumptions it measures the covariance of two response probabilities. Its distance from a sharp upper bound then constrains how closely the population behaves like detectors with individual thresholds.

## An observable contrast

Fix a pilot mass $z$. Record its hit $X$ and assign the science target $s_1=s$ or $s_0=1-s$ using fresh randomization with known probabilities $e_j(x)>0$ in each occurring pilot stratum. Put $p=\Pr(X=1)$ and $d_{xj}=\mathbb E[Y-s_j\mid X=x,J=j]$, where $Y$ is the science hit. Retain every incident block, including misses, with both binary outcomes defined at the stated clock. If an outcome is unclassified, its possible values must be included as bounds, or the reading mechanism modeled. Deleting such blocks changes the population.

For a policy choosing target $j$ with probability $\pi_j(x)$, the mean excess is

$$
V(\pi)=\sum_x\Pr(X=x)\sum_j\pi_j(x)d_{xj}
=\mathbb E\!\left[\frac{\pi_J(X)}{e_J(X)}(Y-s_J)\right].
$$

Conditioning on the recorded stratum and randomized action proves both equalities. This evaluates a change of policy if it uses the same pilot procedure, preparations and outcome mechanisms, the policy label supplies no other input to the apparatus, and each science assignment is randomized independently of the potential readings within its pilot stratum. Independent time assignment or conditioning on recorded design strata can be needed if conditions drift. This is the sequential randomization principle used to evaluate adaptive strategies. [Murphy, 2005](https://doi.org/10.1002/sim.2022)

Compare $J=X$ with a fresh independent bit $J$ of the same hit frequency $p$. Both policies send the same marginal mixture of science preparations. For $0<p<1$ their difference is

$$D(z,s)=p(1-p)\{d_{11}-d_{10}-d_{01}+d_{00}\}.$$

For a deterministic pilot the policies coincide and $D=0$. The reassigned bit can be supplied by an independently sampled pilot in the same population. Swapping labels between neighboring blocks in a drifting session can preserve correlations with the science detector. Reassignment changes the routing decision; both policies physically perform the pilot. The contrast by itself cannot separate pre-existing conditions from a state written by the pilot.

## What follows under a persistent response

Suppose the response curve $g_A$ is shared across a block. Conditional on type $A$, the pilot has mean $g_A(z)$. Conditional on type, pilot outcome and assignment, the science mean is $g_A(s)$ at target $s$ and $1-g_A(s)$ at its reflection. Draw types from the same population across settings. Then

$$D(z,s)=2\operatorname{Cov}(g_A(z),g_A(s)).$$

Indeed the conditional mean difference between the two science *hit* rates is $2g_A(s)-1$, and subtracting the independent-bit policy multiplies this by $X-p$ before averaging. The two policies have equal mean assigned target. A lower-triangular set of such readings therefore predicts its transpose. The matrix $D(z_i,z_j)$ over a common grid must be positive semidefinite, since its quadratic form is twice a variance. Refreshing the science type independently makes the contrast zero. A common drift of both readings can itself supply the shared type, so a positive result does not locate its physical cause. [Paired-read covariance controls](Paired_reads_for_a_type_dependent_target.md)

Fix $[a,b]$ in the lower half with $h=b-a>0$. Assume typewise monotonicity and exact typewise endpoint calibration $g_A(a)=a$, $g_A(b)=b$. These give $a\le T=g_A(s)\le b$ in the gap. For $\mu=\mathbb E T$, the measured deficit from the maximal own-bit advantage is

$$\delta(s)=2(\mu-a)(b-\mu)-D(s,s)=2\mathbb E[(T-a)(b-T)].$$

This expands the bounded-variance inequality of Bhatia and Davis. It vanishes precisely for an endpoint-valued response almost surely. With $\mu=s$, the largest advantage is $2(s-a)(b-s)$, reaching $h^2/2$ at the midpoint. The uniform threshold rival attains it. For $0<\epsilon\le h/2$, the fraction of types with $a+\epsilon\le T\le b-\epsilon$ is at most $\min(1,\delta(s)/(2\epsilon(h-\epsilon)))$. At $s=(a+b)/2$ the nontrivial bound is sharp by mixing equal endpoint masses with equal masses at $a+\epsilon,b-\epsilon$. A nonzero empirical upper bound on the deficit should account for uncertainty in the singles and the feedback contrast. [Bhatia and Davis, 2000](https://doi.org/10.1080/00029890.2000.12005203)

There is a cross-check when the fixed-mass population means equal the prepared masses. For $a\le z\le s\le b$, expansion and monotonicity give

$$
0\le (z-a)(b-s)-D(z,s)/2
=\mathbb E[(g_A(z)-a)(b-g_A(s))]
\le \tfrac12\min(\delta(z),\delta(s)).
$$

Both upper bounds follow by replacing the smaller first factor or the smaller second factor by its value at the other mass. Even one saturated diagonal determines the appropriate cross entries with that mass, provided the two means and the ordering hold.

## Reconstructing a threshold on the gap

Assume exact population means $\mathbb E g_A(s)=s$ throughout this gap and measurable monotone sample curves. Draw one auxiliary $V$ uniformly on $(0,1)$ independently of $A$, and use the **same** $V$ at every mass. Define

$$H(s)=a+h\mathbf1\{V\le (g_A(s)-a)/h\}.$$

The endpoint-valued $H$ is nondecreasing for every such draw. Its crossing location is uniform on the gap, since for each fixed $s$, $\Pr(H(s)=b)=(s-a)/h$; neighboring rational cuts give the same continuous distribution for the crossing under either convention at its jump. For each fixed input $T$, averaging the two possible errors over $V$ gives $2(T-a)(b-T)/h$. Thus

$$\mathbb E|g_A(s)-H(s)|=\delta(s)/h.$$

Integrating gives a coupling bound on the mean integrated absolute difference over the gap. Saturation at all points of a countable dense subset gives agreement there on a single event of probability one. Monotonicity on either side of the random crossing gives agreement everywhere except possibly at that one point on each sample curve. An input chosen using the exact threshold can hit that point, so the convention at the jump matters for such a protocol.

Saturation at finitely many points only identifies a crossing bracket for each type. For example, draw a uniform threshold, keep its endpoint values at all tested nodes, and linearly interpolate between successive nodes on each curve. The curves still have the ordinary population mean throughout the gap. They reproduce every randomized two-read table on that mesh under fresh conditional noise. In the interval containing the crossing, interior masses see a ramp. An interior probe can separate the constructions. [Finite-menu thresholds](Hidden_threshold_between_calibrated_masses.md)

## An invasive detector with the same records

Consider the uniform threshold rival with $a=1/8$, $b=3/8$ and midpoint $s=z=1/4$. A memory device draws its first $X$ as an ordinary Bernoulli$(1/4)$, stores that bit, and sets its next direct hit probability to $5/16$ after a hit and $11/48$ after a miss. It complements these probabilities for the reflected science action. These are the threshold rival's conditional means from Bayes' rule. For either action all joint cells match, including a randomized or feedback-selected science target. The direct single is $1/4$ when assigned independently; the resulting advantage is $1/32$. There is no pre-existing threshold in this implementation. For an entire panel the device can store the pilot setting and outcome and use the corresponding conditional table for each science target. Distinguishing the two explanations requires an independently justified restriction on what the pilot can write or what the science meter can read.

The [exact checker](check_pilot_feedback.py) enumerates joint records, randomized assignments, drift and reset controls, finite-mesh response curves and their threshold coupling. These are population statements for the stipulated operations. No experiment has yet supplied these records or closed the probability-rule or empirical-correspondence gate.
