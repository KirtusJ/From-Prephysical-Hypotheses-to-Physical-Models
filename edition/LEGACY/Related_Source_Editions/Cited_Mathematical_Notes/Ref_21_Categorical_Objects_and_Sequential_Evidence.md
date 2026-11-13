# Categorical Corrections and Sequential Evidence

*Selected sections of an unpublished mathematical note.*

**Original date:** 2026-11-09.  
**Research direction:** Kirtus Justus.  
**Mathematical and editorial assistance:** ChatGPT (OpenAI).

The selected statements, assumptions, arguments, and examples below are drawn from the original note. This editorial excerpt does not claim independent verification. Numerical results are source-reported unless established by the reproduced argument; cited literature is identified from the original note. Original section numbering is retained.


## 2. Initiality and composition

### 2.1 Weak initiality and absence of an initial object

Work in the full category of nonempty finite structures for a fixed positive-arity relational signature, without constants, with ordinary homomorphisms and loops allowed. Let $E_1$ be the singleton with every relation empty, and let $F_m$ have $m$ elements and all relations full.

Every carrier map out of $E_1$ is a homomorphism, so

$$
|\operatorname{Hom}(E_1,A)|=|A|.
$$

This gives existence, not uniqueness. The correct statement is that $E_1$ is **weakly initial**. An initial object must have exactly one arrow into every target. The Stacks Project's Definition 4.12.1 supplies that standard definition.

In fact, for every nonempty $A$,

$$
|\operatorname{Hom}(A,F_2)|=2^{|A|}\ge2.
$$

Thus the full nonempty category has no initial object at all. Its all-full singleton $F_1$ is still terminal, because the unique underlying map into it is a homomorphism.

The initial-object claim survives in the **thin homomorphism preorder** and its homomorphic-equivalence quotient, where parallel arrows are deliberately collapsed. If the empty carrier is allowed under the positive-arity/no-constant convention, the empty structure is initial in the full category.

### 2.2 Full-category and quotient composition

The absence of a full-category initial object does not by itself invalidate quotient-lattice, terminal-unit, or finite-core statements. It does exclude treating $E_1$ as the unit for full-category disjoint union:

$$|E_1\sqcup A|=|A|+1\ne|A|.$$

Binary coproducts still exist, with

$$\operatorname{Hom}(A\sqcup B,C)\cong
\operatorname{Hom}(A,C)\times\operatorname{Hom}(B,C).$$

But there is no nullary coproduct in the nonempty full category. The thin quotient's least element and join-unit do not restore a full-category unit.

A result explicitly formulated on the **thin join-poset** is not refuted by the lack of an initial object in the full category. A proof requiring that full-category initial universal property cannot apply here. The present excerpt does not supply proofs of all associated quotient or finite-core results.

These categorical terms do not describe a first moment, physical vacuum, or creation event. They express universal properties inside a supplied mathematical category.

## 3. Sequential likelihood mixture

The observed null is the complete independent-fair-bit law $P_0(y_{1:n})=2^{-n}$, not merely fair single-time marginals. Each $P_L$ is the complete observed noisy parity-memory law, at the fixed candidate parameters $\eta=1/2$, $\epsilon=1/10$, and uniform stationary initialization.

For $R_{L,n}=2^nP_L(Y_{1:n})$, prefix consistency gives

$$\mathbb E_0[R_{L,n+1}\mid\mathcal F_n]=R_{L,n}.$$

With predeclared $w_L=1/[L(L+1)]$, the exact mixture is

$$
\mathcal E_n=\frac1n+
\sum_{L=1}^{n-1}\frac{2^nP_L(Y_{1:n})}{L(L+1)},\qquad n\ge1,
$$

and $\mathcal E_0=1$. The tail is exactly $1/n$, because every $L\ge n$ candidate has uniform $n$-bit records. Nonnegativity justifies the countable mixture.

Thus $P_0(\sup_n\mathcal E_n\ge20)\le1/20$. This is an application of the established nonnegative-supermartingale crossing inequality (Howard, Ramdas, McAuliffe and Sekhon, 2020, Lemma 1), not a new general sequential theorem.

Marginal fairness cannot replace this null. The constant process $Y_t=B$, for one fair bit $B$, is not the null. Its rejection by a memory-sensitive test does not violate null calibration.

### 3.1 A finite power certificate for the likelihood mixture

A finite power guarantee can be proved for a specified member without making it uniform in the unknown length.

Let the true process be $L=2$, $\eta=1/2$, $\epsilon=1/10$. In $n=1950$ consecutive observed outputs, form $m=650$ disjoint length-three parity windows. Their even-parity indicators are independent Bernoulli variables with

$$p=\frac{1+\eta(1-2\epsilon)^3}{2}=\frac{157}{250}.$$

This independence follows from the established independent ideal innovations and disjoint detector windows. It is not asserted for overlapping noisy parity windows.

Their subexperiment likelihood ratio is

$$S_m=\left(\frac{157}{125}\right)^K
\left(\frac{93}{125}\right)^{m-K},\qquad K\sim\operatorname{Bin}(m,157/250).$$

Write $R_n=P_2(Y_{1:n})/P_0(Y_{1:n})$. Exactly,

$$\mathbb E_{P_2}[S_m/R_n]=\mathbb E_0[S_m]=1.$$

Since $w_2=1/6$, failure of the mixture to cross by $n$ implies $\mathcal E_n<20$ and hence $R_n<120$. For any $c>0$,

$$
P_2(\tau>n)\le
P_2(S_m<120c)+\frac1c.
$$

Take $c=40$. Exact integer comparisons show that $S_{650}\ge4800$ iff $K\ge384$. Consequently

$$
P_2(\tau>1950)
\le \sum_{k=0}^{383}\binom{650}{k}
\left(\frac{157}{250}\right)^k
\left(\frac{93}{250}\right)^{650-k}+\frac1{40}
=0.04802543035363984\ldots<0.05.
$$

Therefore the original unknown-length mixture has **anytime size at most 5% and power by 1950 outputs at least 95.19745696463602...%** at this declared alternative. The probabilities are exact rationals; decimals are summaries.

This is a sufficient bound, not a minimum stopping horizon, expected-stopping-time claim, or 95% guarantee for every memory length. It is not interchangeable with the earlier 183-innovation count-only fixed-horizon optimum. Full-mixture computation can be expensive. The finite power proof uses a component lower bound; it does not require numerically evaluating all 1949 nonconstant likelihoods to prove the inequality.

### 3.2 Pointwise eventual detection, without uniform finite depth

For any fixed candidate length $L$ actually generating the observations at the specified nondegenerate parameters, select disjoint windows of width $L+1$. Their even-parity probability is

$$p_L=\frac{1+\eta(1-2\epsilon)^{L+1}}2\ne\frac12.$$

Let $m=\lfloor n/(L+1)\rfloor$ and $S_m$ be their likelihood ratio. The strong law gives

$$\frac{\log S_m}{n}\longrightarrow
\frac{d_{\mathrm{Ber}}(p_L\Vert1/2)}{L+1}>0.$$

For each $b>0$, the identity $\mathbb E_L[S_m/R_{L,n}]=1$ and Markov's inequality give

$$P_L(R_{L,n}<S_me^{-bn})\le e^{-bn}.$$

The sum is finite. The first Borel-Cantelli lemma, followed by countably many rational $b\downarrow0$, proves

$$\liminf_{n\to\infty}\frac{\log\mathcal E_n}{n}
\ge \frac{d_{\mathrm{Ber}}(p_L\Vert1/2)}{L+1}>0\quad P_L\text{-almost surely}.$$

Thus every fixed true candidate in this mixture is eventually detected almost surely. There is still no uniform finite horizon across unrestricted $L$: for $L\ge n$, the entire observed $n$-bit record has exactly the null law. None of these per-index growth rates is a physical information rate.

## 4. Robust validity does not guarantee useful evidence growth

### 4.1 Validity of the worst-case-normalized factor

Assume a predictable conditional-bias envelope

$$p_t=P(Y_t=1\mid\mathcal F_{t-1})\in[1/2-\delta_t,1/2+\delta_t]$$

and a predictable probability forecast $q_t$. Its factor

$$F_t=\frac{2q_t(Y_t)}{1+2\delta_t|2q_t(1)-1|}$$

has conditional null expectation at most one. Its denominator is the exact worst-case expectation of the unnormalized numerator. Products therefore obey the same crossing guarantee. No general power optimum is claimed.

### 4.2 A log-optimal binary alternative within the same null

Put $\ell=1/2-\delta$, $u=1/2+\delta$, with $0<\ell\le u<1$. For an interior forecast $q$, define

$$p_*=\min\{u,\max\{\ell,q\}\},\qquad
G_q(1)=\frac q{p_*},\quad G_q(0)=\frac{1-q}{1-p_*}.$$

If $q>u$, expected $G_q$ is increasing in the actual Bernoulli parameter and equals one at $u$. If $q<\ell$, it is decreasing and equals one at $\ell$. If $q$ lies inside the interval, $G_q\equiv1$. Thus it is valid throughout the same null interval.

For any nonnegative valid factor $g$,

$$
\mathbb E_q\log\frac{g(Y)}{G_q(Y)}
\le\log\mathbb E_q\frac{g(Y)}{G_q(Y)}
=\log\mathbb E_{p_*}g(Y)\le0.
$$

Hence $G_q$ maximizes expected one-step log evidence for the declared alternative Bernoulli$(q)$. This is an elementary specialization of established growth-rate-optimal e-variable and reverse-information-projection theory. Larsson, Ramdas and Ruf provide the general framework; the interval formula and example below are explicit specializations (Larsson, Ramdas and Ruf, *The numeraire e-variable and reverse information projection*).

With predictable $q_t,\ell_t,u_t$, multiplying these factors gives a nonnegative null supermartingale. This one-step expected-log criterion is not a finite-horizon Neyman-Pearson optimum or uniform power guarantee.

### 4.3 A concrete negative-growth countercontrol

Use the conditional null interval $[2/5,3/5]$ and forecast $q=13/20$, matching an independently sampled Bernoulli alternative outside that interval. The worst-case-normalized factor and clipped factor are

$$
(F(0),F(1))=(35/53,65/53),\qquad
(G(0),G(1))=(7/8,13/12).
$$

Their expected log growth in nats per observation is respectively

$$-0.01256836659866295\ldots,
\qquad +0.005291772569215716\ldots.$$

The signs do not depend on floating-point rounding:

$$65^{13}35^7<53^{20},\qquad
13^{13}7^7>12^{13}8^7.$$

Under this alternative, the product of the worst-case-normalized factors tends to zero almost surely, while the clipped product grows without bound almost surely. The former may cross early, so no claim of zero rejection probability is made. The example proves that a valid, sharply normalized factor can have unfavorable long-run growth even when its numerator forecast is correct.

This control is a separate Bernoulli experiment, not the parity-memory alternative. It does not refute the validity theorem.

### 4.4 Enlarging the null changes what rejection means

A conditional-bias null is not a memorylessness null. In the ideal parity-memory family, the conditional next-bit bias is at most $|\eta|/2$; any envelope at least that large includes the dependent process. With independent symmetric-flip readout, conditioning first on the full source history gives

$$\left|P(\widetilde Y_t=1\mid\widetilde Y_{<t})-1/2\right|
\le |\eta|(1-2\epsilon)/2.$$

For $\eta=1/2,\epsilon=1/10$, the bound is $1/5$. A test valid for every law inside an envelope this wide must retain its null error control on this memory-bearing process. Robustness cannot simultaneously preserve rejection of alternatives that the enlarged null now admits.

The predictive envelope is an input requiring justification under the actual filtration. This analysis supplies no calibration data establishing it.

## 5. Rank bounds for a specified competitor class

### 5.1 Probability-matrix rank bound

For normalized joint probability matrices $H,Q$, let $\delta=\tfrac12\|H-Q\|_1$ with entrywise $1$-norm. Zero total signed mass gives

$$\|H-Q\|_F^2\le2\delta^2.$$

If $\operatorname{rank}Q\le D$, the singular-tail inequality gives

$$\operatorname{TV}(H,Q)\ge
\sqrt{\frac12\sum_{j>D}\sigma_j(H)^2}.$$

The singular-value projection argument does not claim that a truncated singular-value decomposition is a probability model. HMM boundary-state factorization supplies the necessary rank restriction; nonnegative realization remains an additional question. Ohta, *On the Realization of Hidden Markov Models and Tensor Decomposition*, supplies the established realization background.

### 5.2 Marginal-sensitive refinement

Let

$$r=\operatorname{TV}(H_X,Q_X),\qquad
c=\operatorname{TV}(H_Y,Q_Y),\qquad
T_D=\sum_{j>D}\sigma_j(H)^2.$$

Write $A=H-Q$. For a positive entry $A_{ij}=x$, the negative mass in its row is at least $x-r$, and that in its column is at least $x-c$. These two negative sets are disjoint, so total negative mass $\delta\ge2x-r-c$. The analogous argument for negative entries gives

$$\|A\|_{\max}\le\frac{\delta+r+c}{2}.$$

It follows that

$$T_D\le\|A\|_F^2\le\delta(\delta+r+c),$$

and therefore

$$\boxed{
\operatorname{TV}(H,Q)\ge
\max\left\{\sqrt{T_D/2},
\frac{\sqrt{(r+c)^2+4T_D}-(r+c)}2\right\}.
}$$

Upper bounds on the marginal discrepancies may be substituted into the second term because it decreases with $r+c$. No empirical bounds are supplied here.

If both block marginals are matched exactly, this improves to

$$\boxed{\operatorname{TV}(H,Q)\ge\sqrt{T_D}.}$$

The underlying norm inequality $\|A\|_F\le\operatorname{TV}(H,Q)$ is sharp for zero row and column sums, as a two-by-two signed cycle shows. That sharpness does not establish attainability of the entire rank bound by a probability model or HMM.

### 5.3 The specified noisy matrix

For $L=2,\eta=1/2,\epsilon=1/10$, the spectrum remains $(1/4,8/125,8/125,1/25)$.

| Maximum rank / classical states | Arbitrary normalized competitor | Both block marginals matched |
|:--|:--|:--|
| 1 | $\sqrt{153/31250}\approx0.0699714$ | $\sqrt{153/15625}\approx0.0989545$ |
| 2 | $\sqrt{89/31250}\approx0.0533667$ | $\sqrt{89/15625}\approx0.0754718$ |
| 3 | $1/\sqrt{1250}\approx0.0282843$ | $1/25=0.04$ |

There is a still stronger exact result for rank one **with those marginals fixed**. The target has uniform four-element past and future marginals. A normalized rank-one competitor preserving both is uniquely $Q_{ij}=1/16$. Direct rational arithmetic yields

$$\inf_{\substack{\operatorname{rank}Q=1\\Q_X=H_X,\ Q_Y=H_Y}}
\operatorname{TV}(H,Q)=\frac{21}{125}=0.168.$$

The independent-fair-bit process attains this particular rank-one competitor. No claim is made that the same number applies when its marginals may vary, or that the two- and three-state lower bounds are attained.


## Limits of the selected passage


Some arguments summarize earlier unpublished mathematical notes from the same research program. These are internal research provenance and self-citation, not external corroboration. The excerpt reproduces only the displayed categorical, sequential, and matrix-norm arguments; it does not certify all related proof chains.


## Mathematical sources identified in the original note


- The Stacks Project, Definition 4.12.1, *Initial and final objects*. https://stacks.math.columbia.edu/tag/002B . Source of the unique-arrow definition; not a claim that the particular counterexample is published there.

- S. R. Howard, A. Ramdas, J. McAuliffe and J. Sekhon, *Time-uniform Chernoff bounds via nonnegative supermartingales*, Probability Surveys 17 (2020), 257–317; Lemma 1. https://arxiv.org/abs/1808.03204 . General crossing inequality; not the 1950-output certificate.

- M. Larsson, A. Ramdas and J. Ruf, *The numeraire e-variable and reverse information projection*, author manuscript. https://arxiv.org/abs/2402.18810 . General expected-log and numeraire criteria; the binary interval specialization is given above without a novelty claim.

- Y. Ohta, *On the Realization of Hidden Markov Models and Tensor Decomposition*, author manuscript. https://arxiv.org/abs/2008.11487 . Rank necessity and the distinction from nonnegative realization; not the marginal-sensitive bound.
