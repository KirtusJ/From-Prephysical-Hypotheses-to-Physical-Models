# Local Stochastic Stability and Comparison-Readout Robustness

*Selected sections of an unpublished mathematical note.*

**Original date:** 2026-11-09.  
**Research direction:** Kirtus Justus.  
**Mathematical and editorial assistance:** ChatGPT (OpenAI).

The selected statements, assumptions, arguments, and examples below are drawn from the original note. This editorial excerpt does not claim independent verification. Numerical results are source-reported unless established by the reproduced argument; cited literature is identified from the original note. Original section numbering is retained.


## 1. Local associator control


A uniform all-carrier associativity bound is sufficient but unnecessary for the size-dependent distance-to-intersection estimate below. The indicated two-position associator bound suffices under exact all-size structural compatibility. Conversely, bounded-size tests do not certify a uniform all-size associativity bound.

Assume a total stochastic kernel $K_S(R,Q)$ on finite equivalence relations, with exact restriction compatibility on all finite carriers, commutativity, and pointwise idempotence. On a two-position carrier, let $a$ be the probability of equality for mixed input statuses $(1,0)$. Three-position transitivity gives $0\le a\le1/2$. For the two-position triple $(1,0,0)$, fresh conditional composition yields equality probabilities $a^2$ and $a$, so

$$
\varepsilon_2=a(1-a),\qquad
 a=\frac{1-\sqrt{1-4\varepsilon_2}}2\le2\varepsilon_2.
$$

The next operation must use the specified conditional kernel; this is not a metaphysical statement about creating new randomness. General stochastic-map and conditional-independence theory supplies background, not a proof attribution for this particular partition result. (Fritz, 2020)

Let $\kappa(R,Q)$ count pairs of distinct common blocks of $R\cap Q$ sharing a parent block in either input. Exact structural compatibility preserves every common block, forbids mergers separated by both inputs, and gives each eligible merger probability $a$. Therefore

$$
\boxed{\operatorname{TV}(K_S(R,Q),\delta_{R\cap Q})
 \le\min\{1,\kappa(R,Q)a\}.}
$$

A bound on the indicated two-position population associator suffices. The original raw-position pair count can be much larger: one 200-position input block and two 100-position blocks in the other input give $\kappa=1$, while the raw pair count is $10,000$. Exact all-size structural compatibility is still an assumption. Finite empirical tests do not establish it, and a finite sample with no observed discrepancy does not prove a zero population associator. (Justus, *Finite-Size Stochastic Stability and Readout-Robust Collision Tests*, section 2)

## 2. Pair aliases and a complete three-position discriminator

Compare the globally mixed kernel

$$
G_a(R,Q)=(1-2a)\delta_{R\cap Q}+a\delta_R+a\delta_Q,
\quad 0\le a\le\tfrac12,
$$

with the marked-common-block kernel $L_t$: independently mark common blocks $H,V,N$ with probabilities $t,t,1-2t$; merge $H$ blocks sharing an $R$ parent and $V$ blocks sharing a $Q$ parent. For $a=t^2$, the complete kernels coincide on all carriers of size at most two. The signed associator identity is:

$$
(G_a(G_a(R,Q),T))-(G_a(R,G_a(Q,T)))
=a(1-a)(\delta_T-\delta_R),
$$

where the left side denotes the difference of the composed output laws. Thus $G_a$ has all-size associativity supremum $a(1-a)$, whereas the supremum for $L_t$ is one when $t>0$. The source reports the simultaneous limit:

$$
t\to0,\quad nt\to c>0
\quad\Longrightarrow\quad
\operatorname{TV}(C_{n,t^2},C_{n,t})\to1-(1+c)e^{-c}.
$$

These comparison-law results are reported in Justus, *Finite-Size Stochastic Stability and Readout-Robust Collision Tests*, sections 3–4. The laws denoted $C_{n,u}$ and the full limit argument are not defined or proved in this selected passage; the displayed limit is retained as a source-reported assertion.

**Conditional three-position calculation.** Apply each kernel to $(\top_3,\bot_3)$. The output probabilities are:

| Output | $G_{t^2}$ | $L_t$ |
|:--|:--|:--|
| One three-position block | $t^2$ | $t^3$ |
| Each specified two-position block and singleton | $0$ | $t^2(1-t)$ |
| Three singletons | $1-t^2$ | $1-3t^2+2t^3$ |

Hence

$$
\boxed{\operatorname{TV}(G_{t^2}(\top_3,\bot_3),L_t(\top_3,\bot_3))
=3t^2(1-t).}
$$

For $t=1/10$ this equals $27/1000$. The event of exactly two blocks is impossible under $G_{t^2}$ and has probability $27/1000$ under $L_t$. With fresh independent repetitions, rejecting $G_{t^2}$ when that event appears gives size zero and power $1-(973/1000)^m$. The first integer reaching power $19/20$ is $m=110$, with power $0.9507492975\ldots$; $m=109$ gives $0.9493826285\ldots$.

This is optimal within zero-size tests of these two simple laws because every other output has positive null probability. It is not a uniform test for every possible kernel, an all-size certification, or a physical experiment. Repeating only two-position experiments cannot distinguish these two kernels under their common conditional sampling contract.

## 3. Label-replacement certificate

The stipulated label distributions have core weights $(1,4,6,7)/36$ and $(2,3,5,8)/36$, plus the same tail $2^{-j-1}$, $j\ge1$. Let

$$
\mu_0=425/13608,\quad \mu_1=439/13608,\quad
\Delta=\mu_1-\mu_0=1/972.
$$

For one complete partition of $n$ independent samples,

$$
U_{n,3}=\binom n3^{-1}\sum_{B}\binom{|B|}{3}.
$$

The overlap-variance formula is

$$
V_i(n)=\sum_{r=1}^3
\frac{\binom3r\binom{n-3}{3-r}}{\binom n3}
\bigl(s_{6-r,i}-s_{3,i}^2\bigr),
$$

with binomial coefficients outside their admissible ranges set to zero. All needed source moments, including the infinite tail, are rational.

If at most $r$ sampled labels can be replaced adversarially after observing the full record, the deterministic bound is

$$
|\widetilde U-U|\le b_{n,r}
=1-\frac{\binom{n-r}{3}}{\binom n3}.
$$

Only triples containing an edited position can change. The bound is attained by changing $r$ entries of an all-equal sample to distinct fresh labels. The sufficient two-Cantelli feasibility condition is

$$
\sqrt{19V_0(n)}+\sqrt{19V_1(n)}+2b_{n,r}\le\Delta.
$$

The source reports first qualifying $n$ values $329180$, $340744$, $438049$, and $1215755$ for $r=0,1,10,100$. These are minima within this sufficient certificate, not optimal statistical sample sizes (Justus, *Finite-Size Stochastic Stability and Readout-Robust Collision Tests*, sections 5–6).

A falsely reported equality followed by transitive closure is a different error mechanism. On two equally sized true blocks, one false bridge merges the entire partition and changes $U_{n,3}$ by $3n/[4(n-1)]$. This is a failure of that reconstruction procedure, not proof that every statistic computed from noisy pair reports has order-one sensitivity. (Justus, *Finite-Size Stochastic Stability and Readout-Robust Collision Tests*, section 6.3)

## 4. An optimally Lipschitz extension to raw pair reports

### 4.1 Observation contract and score

Suppose the observer retains a binary report $z_{ij}=z_{ji}$ for every unordered pair, before transitive closure. At most $e$ reports differ from the true equality indicators. Their locations and directions may be selected after inspecting the entire sample; independence of reporting errors is not assumed.

This is an explicit readout contract. Access to all raw reports and a calibrated bound $e$ are inputs, not consequences of the partition model. It is consistent with the distinction in correlation-clustering research between inconsistent pair reports and the partition inferred from them. That literature is background only; the following statistic and proof are derived here. (Bansal, Blum and Chawla, 2004)

For a triple, let $s=z_{ij}+z_{ik}+z_{jk}$ and assign the score

$$
\phi(0)=\phi(1)=0,\qquad \phi(2)=\tfrac12,\qquad\phi(3)=1.
$$

Define

$$
\boxed{W_n(z)=\binom n3^{-1}\sum_{i<j<k}\phi(z_{ij}+z_{ik}+z_{jk}).}
$$

A genuine equivalence relation never has exactly two positive reports on a triple. On an error-free report graph, $W_n=U_{n,3}$ exactly. Half-credit for an inconsistent triple is a mathematical extension rule, not an assigned probability that its labels actually agree.

If $d_i$ denotes the positive-report degree and $T(z)$ counts complete positive triangles, the same score can be computed as

$$
W_n(z)=\frac{\sum_i\binom{d_i}{2}-T(z)}{2\binom n3}.
$$

Indeed the numerator counts a three-edge triangle twice and a two-edge triple once.

### 4.2 Sharp sensitivity and its precise optimality

Changing one report affects only $n-2$ triples, and changes each score by at most $1/2$. Therefore, for $n\ge3$,

$$
\boxed{|W_n(z)-W_n(z')|
\le\min\left\{1,\frac{3\,d_H(z,z')}{n(n-1)}\right\},}
$$

where $d_H$ counts changed unordered-pair reports. In particular,

$$
|W_n(\widetilde z)-U_{n,3}(z)|
\le\bar b_{n,e}:=\min\{1,3e/[n(n-1)]\}.
$$

**Sharpness.** Starting with an all-equal graph, flip one positive report to negative. Every affected triple changes from score one to one-half, attaining $3/[n(n-1)]$. Removing a matching of $e\le\lfloor n/2\rfloor$ reports attains the $e$-edit bound because a triple cannot contain two disjoint matching edges.

**Optimal extension theorem.** Consider any real-valued function of arbitrary pair-report graphs agreeing with $U_{n,3}$ on every exact equivalence-report graph. Compare the one-block partition with the partition consisting of one singleton and a block of size $n-1$. Their scores differ by $3/n$, while their report graphs differ in exactly $n-1$ edges. Telescoping along an edge-edit path shows that the function's maximum single-edge change is at least

$$
\frac{3/n}{n-1}=\frac3{n(n-1)}.
$$

The constructed $W_n$ attains this lower bound. Thus its **global one-edge Lipschitz constant is optimal in that precisely specified extension class**. This is not an optimality theorem for statistical testing risk, hardware accuracy, computational cost, or every multi-edge perturbation class.

For the source's false bridge between two true blocks, the unclosed reports create $n-2$ two-edge triples. Here the new score changes by exactly $3/[n(n-1)]$, instead of the order-one change caused by global transitive closure. The two calculations use different postprocessing rules on the same raw error.

## 5. Exact detection certificates with bounded pair-report errors

Under the same independently sampled source distributions, $W_n=U_{n,3}$ on the latent error-free data. The deterministic error bound therefore transfers the existing variance calculation. A threshold $c$ has both one-sided errors at most $1/20$ if

$$
c-\mu_0-\bar b_{n,e}\ge\sqrt{19V_0(n)},\qquad
\mu_1-c-\bar b_{n,e}\ge\sqrt{19V_1(n)}.
$$

Such a threshold exists for these sufficient inequalities exactly when

$$
\boxed{\sqrt{19V_0(n)}+\sqrt{19V_1(n)}+2\bar b_{n,e}\le\Delta.}
$$

Put $D=\Delta-2\bar b_{n,e}$ and $z=D^2/19-V_0-V_1$. Feasibility is equivalent to $D>0$, $z\ge0$, and $z^2\ge4V_0V_1$, allowing exact rational checks.

| Maximum corrupted unordered-pair reports $e$ | First $n$ passing this sufficient certificate |
|---:|---:|
| 0 | 329,180 |
| 1 | 329,180 |
| 10 | 329,180 |
| 100 | 329,184 |
| 1,000 | 329,216 |
| 1,000,000 | 360,784 |

The positive decreasing variance decomposition and the decreasing bias $\bar b_{n,e}$ establish monotonicity for each fixed $e$. The source reports that every stated boundary passes and the preceding integer fails, using exact rational comparisons; decimal arithmetic only proposes thresholds. The boundary computations are not independently repeated in this excerpt.

For $n=329180$ and $e=10$, one accepted threshold is

$$
c=\frac{31718431530157178464099}{10^{24}}.
$$

This theorem does not compare equal resource budgets with the label-replacement theorem. One replaced label can alter many pair reports. Conversely a single erroneous pair followed by transitive closure can merge many unaltered labels. Error units, raw data access, and processing must remain explicit.

### 5.1 A resource limitation and a fixed-fraction boundary

At $n=329180$, retaining all pair reports means $\binom n2=54,179,571,610$ reports. This is not a demonstrated efficient detector. Compressing them first into a partition can destroy the raw-error accounting used in the theorem. Subsampling requires a separate variance and observation analysis.

If the erroneous-pair fraction is at most $\rho$, so $e\le\rho\binom n2$, then $\bar b_{n,e}\le3\rho/2$. The variance tends to zero, so this worst-case certificate can work at large $n$ whenever

$$
\boxed{\rho<\Delta/3=1/2916\approx0.000342935528.}
$$

This is approximately $0.0342936\%$ of the pair reports. It is a sufficient-radius boundary for this statistic and bound, not an information-theoretic impossibility threshold. An error *rate* that stays fixed is not diluted in the same manner as a fixed number of errors.

## 6. A common lossy readout can erase the source distinction completely

There is a separate negative control. Name the four core symbols $1,2,3,4$, distinct from all tail symbols. Apply the same deterministic readout to both candidate sources: merge symbols $1,2$, merge symbols $3,4$, and preserve every tail symbol.

Both pushed-forward laws have core weights

$$
\left(\frac5{36},\frac{13}{36}\right)
$$

and the same unchanged geometric tail. Thus their complete recorded i.i.d. laws, and every equality partition of those records, are identical for every sample size. Every test on those records has power equal to its size.

This does not contradict the robust certificates: the lossy map is not asserted to meet their small bounded-error assumptions. It demonstrates why the observation map itself must be warranted. The detector is common to the two hypotheses; no hypothesis-dependent readout has been used. The symbol naming is supplied comparison structure, not a physically derived reference.


## Mathematical sources identified in the original note


- Kirtus Justus, *Finite-Size Stochastic Stability and Readout-Robust Collision Tests* (9 November 2026), sections 2–6. Unpublished companion mathematical note; internal research provenance, not independent external corroboration.

- T. Fritz, *A synthetic approach to Markov kernels, conditional independence and theorems on sufficient statistics*, Advances in Mathematics 370 (2020), 107239. https://arxiv.org/abs/1908.07021 . General stochastic-map background, not proof attribution for the partition-specific bounds.

- N. Bansal, A. Blum and S. Chawla, *Correlation Clustering*, Machine Learning 56 (2004), 89–113. DOI: 10.1023/B:MACH.0000033116.57574.95 . Background for distinguishing pair judgments from an inferred partition; the score and sensitivity proof above are not attributed to that paper.
