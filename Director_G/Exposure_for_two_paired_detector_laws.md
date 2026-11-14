# Exposure needed to distinguish the two finite-budget detectors

Research note for Director G, prepared by OpenAI Codex for Kirtus Justus. Gate OP-27.

At the common moment budget $M=10^{-8}$, compare exactly two specified populations: the [global tent](Finite_moment_transfer_between_calibrated_masses.md) and the [gap-local tent](Local_response_at_the_selected_gap.md). They have different node-pair scores but identical single-hit probabilities. What can be distinguished using the entire two-bit record at routed masses?

**Protocol.** Draw a fresh independent detector type for each pair. Choose its mass using only past observations and independent randomness. Read that mass twice on the shared type with independent binary outcomes conditional on type. Retain both incident outcomes. Assign equal prior probability to the two populations and measure average classification error. The result applies to a fixed number of pairs or a hard exposure cap. Persistent types across pairs, side information about type, unequal masses within a pair, off-menu preparations and missing outcomes require separate analyses.

## From a pair score to likelihood

If the node mass is $s$ and the paired centered score is $v$, the ordered outcome probabilities for $00,01,10,11$ are
$$((1-s)^2+v,\quad s(1-s)-v,\quad s(1-s)-v,\quad s^2+v).$$
Indeed $\Pr(11)=\mathbb E g_A(s)^2=s^2+v$. The marginals and normalization then determine the remaining entries. Insert the two predicted score profiles to obtain tables $P_s,Q_s$. The endpoint and virtual midpoint controls are identical under both hypotheses. Reflection exchanges $00$ and $11$ and preserves the separation.

Let $\rho_s=\sum_z\sqrt{P_s(z)Q_s(z)}$, and $r=\min_s\rho_s$ over the allowed nodes. The [checker](check_paired_exposure.py) compares all 32 interior lower-half masses, covering the reflected half as well. The largest $1-\rho_s$ is about $3.559041911354\times10^{-16}$ at $s=0.123279641138\ldots$ and its reflection. At this node the global and local paired scores are about $0.731728370M$ and $0.155009655M$. The runner-up on the lower half has mass $0.105561741504\ldots$ and separation $3.327256582986\times10^{-16}$. The node with largest local score, $0.260644776272\ldots$, gives separation only $5.545655764465\times10^{-17}$. Both the difference in rates and their sampling variability affect the comparison.

## Fixed-cap decision bounds

For any common adaptive or randomized mass-selection policy, the affinity of the joint transcripts through $N$ pairs is at least $r^N$. Given a common history, the policy uses the same distribution over next masses under either hypothesis. The one-step affinity of the mass and outcome is a weighted average of the node affinities, hence at least $r$. Multiply by the square-root product of the two history probabilities and sum to obtain the recursion. An earlier stopping rule with a deterministic cap can be padded after stopping.

For transcript laws $P,Q$ of affinity $A$, Cauchy–Schwarz applied to the factors $\sqrt P-\sqrt Q$ and $\sqrt P+\sqrt Q$ gives $\mathrm{TV}(P,Q)\le\sqrt{1-A^2}$. Equal-prior optimal error is $(1-\mathrm{TV})/2$. Thus any protocol with average error at most 5% needs $r^{2N}\le0.19$. Conversely, always preparing an affinity-minimizing node gives transcript affinity $r^N$; the likelihood-ratio rule has error at most $r^N/2$ since $\min(p,q)\le\sqrt{pq}$. Therefore $r^N\le0.1$ suffices. [Background on affinity bounds in testing](https://www2.isye.gatech.edu/~nemirovs/LMCOLN2023Spring.pdf)

At the stated budget the resulting necessary and sufficient exposure bounds are about **2.33312 quadrillion** and **6.46968 quadrillion pairs**, respectively. Each pair uses two launches. The exact optimal exposure is between the bounds. The fixed-mass guarantee concerns average error and does not set separate 5% limits on each conditional error. Affinity minimization need not coincide with optimal finite-sample Bayes risk.

The computation forms the cell probabilities as rational numbers and evaluates $1-\rho$ stably as half the sum of $(P-Q)^2/(\sqrt P+\sqrt Q)^2$. A direct affinity calculation cross-checks each node; 60- and 90-digit decimal evaluations gave the same minimizing node and integer ceilings. A same-family second reader checked the adaptive recursion, testing inequalities and 5% constants. These are model-based exposure bounds; there are no measured detector counts, runtime estimate, or evidence here of physical realization.


## The five-percent crossing for a repeated mass

Fix one routed mass for the entire experiment. With equal prior probabilities the likelihood-ratio decision is optimal for mean error. Across all such designs the minimum exposure $N_*$ with mean error at most 5% satisfies
$$3{,}800{,}940{,}000{,}000{,}000 < N_* \le 3{,}800{,}950{,}000{,}000{,}000.$$
At the upper endpoint the mass $0.123279641138\ldots$ and its reflection each give both conditional errors below 5%. Every other distinct node pair still has optimal average error above 5% at that exposure. Since optimal error cannot increase with extra pairs, only these two reflected masses can attain the first fixed-node crossing. For designs that change the mass between pairs, the earlier lower bound of about 2.33 quadrillion remains applicable. Repeating a fixed mass is permissible in that broader class, so its sufficient bound also improves to 3.80095 quadrillion.

For one ordered observation let $Z=\log(P(z)/Q(z))$. Under each of the two laws separately compute its mean $\mu$, standard deviation $\sigma$, and third centered absolute moment $m_3$. The total log likelihood is a sum of $N$ independent copies. Under $P$ a negative total is an error; under $Q$ a positive total is an error. Since the means have opposite signs, the finite-sample Berry–Esseen inequality encloses each error within
$$
\Phi(-\sqrt N\,|\mu|/\sigma)\ \pm\ \frac{0.475\,m_3}{\sigma^3\sqrt N}.
$$
The same enclosure applies to either assignment of a tie, by continuity of the normal CDF and its approximation to both one-sided limits. Nodes with identical pair laws have mean error $1/2$. [Shevtsova, iid Berry–Esseen constant](https://arxiv.org/abs/1111.6554)

The [interval checker](check_fixed_exposure.py) constructs the cell probabilities as fractions, evaluates the likelihood moments with 50-decimal interval arithmetic (mpmath 1.3.0), and encloses the normal tail using consecutive partial sums of its alternating integrated exponential series. It checks the average-error lower bound at the lower endpoint for every informative node. At the upper endpoint it checks both conditional upper bounds at the winning mass and the average-error lower bound for every other informative lower-half node. On the winning mass, the upper conditional bounds are below 0.049999904 and 0.049999896 under the global and local populations respectively. A same-family second reader reviewed the handling of ties, sample-size monotonicity and fixed-design scope. The crossing is a model prediction under the pair protocol above; no quadrillion-pair data set was generated.


## Mixing routed masses on a predetermined schedule

Allow arbitrary counts at different routed masses, fixed in advance, under the same two hypotheses and independent-pair protocol. The minimum exposure for 5% equal-prior average error satisfies
$$3{,}800{,}938{,}000{,}000{,}000 < N_{\rm pre} \le 3{,}800{,}950{,}000{,}000{,}000.$$
The earlier repeated-mass protocol gives the upper endpoint. Thus any advantage of predetermined mixing over that demonstrated exposure is less than 12 billion pairs, about 3.16 parts per million. This does not establish a strict advantage for mixing.

For one schedule and either law, write $V=\sum_i v_i$ for the total log-likelihood variance, $\mu_i$ for the one-pair mean, and $b_i$ for the third absolute centered moment. The [interval checker](check_mixed_exposure.py) verifies $-\log\rho_i<0.126 v_i$ under each law at each informative node. Nodes with identical laws have affinity one and contribute zero throughout. Reflection permutes the cells and preserves these values.

If either variance total is below six, the product affinity exceeds $\exp(-0.126\cdot6)$. The total-variation inequality above gives average error greater than 0.05854. This handles schedules for which a uniform normal approximation would be poor.

Otherwise both variances are at least six. Under either law the standardized mean magnitude is at most $\sqrt{N}\max_j |\mu_j|/\sqrt{v_j}$ by Cauchy–Schwarz. The independent, unequal-summand Berry–Esseen error is at most
$$0.56\,\frac{\sum_i b_i}{V^{3/2}}\ \le\ \frac{0.56}{\sqrt{6}}\max_j\frac{b_j}{v_j}.$$
Take the maxima over informative nodes separately for each law. At the displayed lower exposure, the resulting lower bounds on the two likelihood-ratio decision errors are respectively greater than 0.0500000170 and 0.0500000091 in this variance regime. Normal continuity covers strict as well as weak threshold tails. Hence the optimal equal-prior decision still misses 5% in both variance regimes. Smaller caps cannot improve the optimum, since a larger experiment can ignore extra observations. [Shevtsova, independent-summand Berry–Esseen constant](https://www.mathnet.ru/eng/ia252)

The conclusion also holds after averaging over schedules randomized before data collection, by conditioning on the schedule. Conditioning on an outcome-dependent schedule would select the observations themselves and would invalidate this proof. The earlier affinity lower bound therefore remains the one established here for adaptive protocols. A second same-family reader checked the variance split, tie treatment and randomization scope. The 60-decimal interval calculation applies to the specified model laws at the common budget; no exposures were physically acquired.
