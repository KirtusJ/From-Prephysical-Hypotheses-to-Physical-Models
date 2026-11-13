# Sampling and Calibration of Robust Equality Comparisons

*Selected sections of an unpublished mathematical note.*

**Original date:** 2026-11-09.  
**Research direction:** Kirtus Justus.  
**Mathematical and editorial assistance:** ChatGPT (OpenAI).

The selected statements, assumptions, arguments, and examples below are drawn from the original note. This editorial excerpt does not claim independent verification. Numerical results are source-reported unless established by the reproduced argument; cited literature is identified from the original note. Original section numbering is retained.


## 2. Optimal extension for every collision order

Fix 2 <= k <= n. For a k-position subset S, let m_S(z) be its number of negative pair reports. Define

\[
\phi_k(z|_S)=\max\left\{0,1-\frac{m_S(z)}{k-1}\right\},
\qquad
W_{n,k}(z)=\binom nk^{-1}\sum_{|S|=k}\phi_k(z|_S).
\]

For k=3, this is exactly the half-credit statistic for triples.

**Clean-data identity.** In a true partition, an all-equal k-tuple has no negative comparisons. Any non-all-equal k-tuple has at least k-1 negative comparisons: the smallest cross-block cut is a singleton separated from k-1 positions. Thus W_(n,k)=U_(n,k) on every exact equivalence graph.

**Sensitivity.** One changed pair belongs to binom(n-2,k-2) k-subsets. Each local score changes by at most 1/(k-1). Hence

\[
|W_{n,k}(z)-W_{n,k}(z')|
\le \min\left\{1,\frac{k\,d_H(z,z')}{n(n-1)}\right\}.
\]

**Optimality in the exact-extension class.** The one-block partition and the partition consisting of a singleton plus a block of n-1 have collision-score difference k/n and pair-report Hamming distance n-1. Any extension agreeing at both endpoints must change by at least k/[n(n-1)] along some edge of a shortest edit path. The displayed extension achieves this global constant. Removing one edge from the all-equal graph achieves equality. A removed matching gives equality for its multi-edit linear bound as well.

The conclusion is an exact-extension Lipschitz optimum, not minimum testing risk. No claim is made that this function is the unique optimal extension. This is an elementary extension of the supplied argument, with no novelty priority asserted.

## 3. A sparse observation contract

The complete-report experiment at n=329180 contains 54,179,571,610 unordered pair entries. That number describes its complete menu, not a universal minimum measurement cost. A sampled observation scheme therefore requires its own analysis.

The alternative here is:

1. Draw n raw labels independently from one of the two fixed paintboxes.
2. A complete potential pair-report graph z is fixed, possibly depending on the entire raw sample and on additional detector randomness, but independently of subsequent query randomization.
3. At most e entries of z differ from true equality, with rho=e/binom(n,2) bounded in advance.
4. Draw B triples independently and uniformly with replacement from all triples of the n indices. Query their three reports and average the half-credit scores.

Write the result as \(\widehat W_{n,B}\). This requires at most 3B pair-query calls. Cached repeated pairs may reduce the number of distinct queried entries. A complete matrix need not be materialized if the report oracle implements one consistent, query-independent assignment. Stable random access to the same n samples is an additional observation assumption.

Drawing tuples from an existing sample is established incomplete-U-statistic methodology (Clémençon, Colin and Bellet, 2016). It is not equivalent to drawing a smaller raw sample and computing all comparisons on that smaller sample. The robust perturbation certificate below is derived here; it is not attributed to (Clémençon, Colin and Bellet, 2016).

### 3.1 Source randomness and query randomness must both be counted

Conditional on the raw sample and fixed graph,

\[
\mathbb E[\widehat W_{n,B}\mid X,z]=W_n(z),
\qquad
\operatorname{Var}(\widehat W_{n,B}\mid X,z)
=\frac{v(z)}B,
\]

where v(z) is the finite-population variance of its triple scores. The sampled scores are conditionally independent given the complete fixed graph. They are not generally independent after averaging over the source sample.

For error-free reports,

\[
\operatorname{Var}(\widehat W_{n,B})
=\left(1-\frac1B\right)V_i(n)
+\frac{\mu_i(1-\mu_i)}B,
\]

where mu_i is the third collision moment and V_i(n) is the full U-statistic variance. This is the specialization of the established incomplete-U variance identity (Clémençon, Colin and Bellet, 2016, equation (21)). Increasing B alone cannot remove the original-source variance V_i(n).

### 3.2 Robust sparse certificate

Let

\[
b=\min\{1,3\rho/2\},
\qquad |W_n(z)-U_{n,3}(X)|\le b.
\]

Introduce an analytical auxiliary variable, not an implementable correction requiring hidden labels:

\[
R=U_{n,3}+\widehat W_{n,B}-W_n(z).
\]

It has mean mu_i. Conditional centering makes its query noise uncorrelated with U_(n,3). Since scores lie in [0,1],

\[
\operatorname{Var}(R)
=V_i(n)+\frac{\mathbb E v(z)}B
\le V_i(n)+\frac{\mathbb E W_n(z)}B
\le V_i(n)+\frac{\mu_i+b}B=:A_i.
\]

Also |widehat W-R| <= b. For a threshold c with positive margins

\[
d_0=c-\mu_0-b,
\qquad d_1=\mu_1-c-b,
\]

Cantelli therefore gives

\[
\alpha\le\frac{A_0}{A_0+d_0^2},
\qquad
\beta\le\frac{A_1}{A_1+d_1^2}.
\]

These are unconditional guarantees over the iid source sample and query randomization, uniformly over the admitted precommitted corruption graphs. The corruptions may depend on the full source record; they need not be independent or identically distributed.

### 3.3 Exact numerical witness

Use the source paintboxes with cores (1,4,6,7)/36 and (2,3,5,8)/36 and common tail 2^(-j-1), j>=1. Their collision moments are

\[
\mu_0=425/13608,\quad \mu_1=439/13608,\quad \Delta=1/972.
\]

Choose

\[
n=2{,}000{,}000,\quad B=10{,}000{,}000,\quad
\rho=1/10000,\quad b=3/20000,
\quad c=99179/3125000=0.03173728.
\]

The variance V_i(n) is evaluated from the exact source moments through degree five. The source reports the following exact rational bounds

\[
\alpha\le
\frac{25032226015092744528840625}{634998927977903024107964257}
=0.0394208949215168\ldots<0.04,
\]

\[
\beta\le
\frac{27900695463010851341340625}{699384194430517969365104257}
=0.0398932313386483\ldots<0.04.
\]

Thus at most 30,000,000 pair-query calls give this certificate, instead of reading all 1,999,999,000,000 pairs at this larger raw sample size. The allowed fixed error count is at most 199,999,900 pair entries, corresponding to 0.01% of the complete pair population.

This trades more raw samples and extra randomized sampling variance for far fewer queried pair entries. It is not a minimum-cost procedure, an equal-total-resource comparison to the original n=329180 experiment, or a claim that a physical implementation supplies persistent query access. No simulation of two million physical labels or ten million queries was performed; the certificate is established through exact moment and error-bound arithmetic.

## 4. Why the report graph must not respond adversarially to the query design

The precommitment requirement is indispensable to this proof and can fail spectacularly.

After learning the B sampled triples, an adversary can set every queried pair report to positive. At most 3B entries differ from true equality, whatever the latent source record. For the numerical witness,

\[
3B=30{,}000{,}000<199{,}999{,}900=e_{\max}.
\]

Its global error fraction is at most 30,000,000/1,999,999,000,000, approximately 0.00150000075%, which is below the nominal 0.01% budget. Nevertheless every sampled triple scores one and the null is rejected with probability one.

This does not contradict the full-graph Lipschitz bound. The complete graph average still obeys that deterministic bound. It contradicts treating a query-selected average as an unbiased sample of a graph chosen after the sampled indices become known.

A corruption rule may inspect the entire raw sample under the positive theorem. It may not select its error locations in response to the independent random query seed. Fixed repeated responses alone are insufficient if their initial values were chosen after query disclosure.

## 5. A finite-population calibration audit and its limits

Assume, additionally, that an independent reference reveals the true equality of sampled pairs. This reference must be warranted separately; comparison transitivity or a second implementation of the same lossy detector is not automatically such a reference.

For the same fixed graph, let M=binom(n,2), let E be its unknown actual error count, and audit s uniformly chosen distinct pair positions independently of the graph. The number of audit discrepancies is hypergeometric. In particular,

\[
\Pr(\text{zero discrepancies}\mid E)
=\frac{\binom{M-E}s}{\binom Ms}
\le (1-E/M)^s.
\]

No independence among the E errors is assumed. Sampling-without-replacement theory is established background (Serfling, 1974); the exact expression here follows directly by counting audit subsets.

For tolerance rho_0=1/10000 and s=46050,

\[
(9999/10000)^{46050}<1/100.
\]

The source reports checking this inequality by integer exponentiation. Thus, if the report graph was committed before auditing, a graph exceeding that error tolerance passes the zero-discrepancy gate with probability below 1%.

This is a repeated-sampling false-pass guarantee, not a posterior statement that a particular accepted graph has 99% probability of being good. If all submitted graphs are bad, every accepted one is still bad, despite a small acceptance probability.

### 5.1 Whole-procedure type-I control without invalid conditioning

Run the sparse test only if the audit observes no discrepancies. Keep the threshold and query design fixed in advance. Assume audit indices and sparse-query indices are independently randomized, and neither is disclosed before the graph is fixed.

Let G={E <= e_max}. On G, the sparse bound controls false rejection. For a data-dependent good/bad event, one must not simply condition on audit acceptance and reuse the iid variance of U_(n,3).

Instead define

\[
R^*=U_{n,3}+\mathbf 1_G(\widehat W_{n,B}-W_n(z)).
\]

Conditional centering still gives E R*=mu_i and

\[
\operatorname{Var}(R^*)
=V_i(n)+\mathbb E[\mathbf1_Gv(z)]/B
\le V_i(n)+(\mu_i+b)/B.
\]

The final inequality uses W<=U+b on G and U>=0. The good-graph rejection event is bounded using R*. The bad-graph false-pass contribution is at most gamma=1/100, pointwise in the raw sample and committed graph. Hence

\[
\Pr_0(\text{reject after audit})
\le 0.0394208949215168\ldots+0.01
=0.0494208949215168\ldots<0.05.
\]

No 95% power claim follows merely from this coverage calculation.

### 5.2 Calibration acceptance is a separate power obligation

At the tolerance boundary E/M=1/10000, this zero-discrepancy gate passes with probability at most (9999/10000)^46050, approximately 0.0099993992. If audit failure means no positive detection, total power at that boundary is at most approximately 1%, even if the downstream statistic is excellent.

If the actual error fraction is instead uniformly bounded by rho_good, the audit-failure probability is at most s*rho_good by a union bound. When rho_good <= rho_0,

\[
\text{whole-procedure power}
\ge 1-\beta-s\rho_{\rm good}.
\]

For rho_good=10^(-8), the numerical sparse certificate gives power at least 0.9596462686613517. This positive guarantee is conditional on the stronger actual-quality premise, not something established by the zero-error audit alone. For error-free graphs the audit always passes.

The audit certifies a single fixed finite report population, not future apparatus performance or another record under drift. The gold-standard access, sampling randomness, commitment, and transfer to new records all require independent justification.

## 6. What remains physically open

The common-readout erasure example establishes that a consistent reported partition need not preserve a distinction in the underlying preparation. More comparisons from the same uninformative readout cannot restore a distinction that it removes exactly.

The results give a mathematically explicit sparse observation alternative and propagate a finite calibration gate into an overall type-I bound. They do not demonstrate their premises in hardware. The finite population can be much larger than the queried subset; persistent sample identity and a stable pair-response map are still resources. No physical measurement cost, error mechanism, calibration truth source, or independence guarantee has been derived from a prephysical hypothesis.

Mathematical selection and useful conditional statistics remain valid achievements. Metaphysical uniqueness is not required to recognize them. The distinction from an empirically supported total foundation remains unchanged.


## Mathematical sources identified in the original note


- Kirtus Justus, *Local Stochastic Stability and Comparison-Readout Robustness* (9 November 2026). Unpublished companion mathematical note; internal research provenance and self-citation, not independent external corroboration.

- S. Clémençon, I. Colin and A. Bellet, *Scaling-up Empirical Risk Minimization: Optimization of Incomplete U-statistics*, Journal of Machine Learning Research 17(76) (2016), 1–36, Definition 5 and equation (21). https://jmlr.org/papers/v17/15-012.html . Tuple sampling and the variance identity; not attribution for the adversarial report-graph extension or its numerical certificate.

- R. J. Serfling, *Probability Inequalities for the Sum in Sampling without Replacement*, Annals of Statistics 2(1) (1974), 39–48. Background for finite-population sampling; the zero-discrepancy hypergeometric expression above follows by direct counting.
