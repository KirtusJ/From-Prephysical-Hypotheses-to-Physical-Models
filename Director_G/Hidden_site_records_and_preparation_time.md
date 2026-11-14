# How often can a direction detector copy the site?

**Kirtus Justus**, Theoretical Physicist, Port Coquitlam, British Columbia, Canada. Research supplement by Director G (OpenAI Codex).

The field-on source requires $m$ consecutive direction switches. Suppose the passing rail is always correctly identified, but after each pass the detector independently makes a permanent, unreported, fully distinguishing site record with probability $p$. This is one specified noisy instrument. Its tolerance depends on what is measured. The conditional state can approach the ideal Gaussian even while almost no initial walkers release before a polynomial clock deadline. Models distinguishing spatial and spin decoherence have been tested in atom walks. The independent hidden-copy law here is a model to test on this detector. [Alberti et al., experimental decoherence comparison](https://doi.org/10.1088/1367-2630/16/12/123052) · [Ideal field-on source](Field_on_source_and_release.md)

## A renewal equation within a single attempt

Fix a persistent sheet character. At each two-tick block, the passing operation is the ideal rail projection followed by $(1-p)I+p\mathcal D_X$ on density matrices, where $\mathcal D_X$ discards the off-diagonal matrix elements between different sites. The discarded outcome can be retained by the environment; summing over it gives this channel. On a failed rail, record the well and restart as before. This model assumes no loss, fresh independent copy decisions conditional on each pass, and a site record that retains the sheet. A static mixture of perfect and permanently faulty instruments has different multi-block statistics even at the same single-use copy rate.

Write $q=1-p$ and $a_j(h)$ for the one-attempt probability of $j$ consecutive ideal switches at field slope $h$, from a sharp well and rail. Let $S_j(h,p)$ be that probability with hidden records. A site copy at a pass leaves a sharp well and rail. Conditional on a fixed sector, the next ideal segment has the same success law at every such well, either rail and either parity. Thus, with $a_0=S_0=1$,

$$
S_m=\sum_{k=1}^m p^{k-1}q^{m-k}
       \sum_{\substack{l_1+\cdots+l_k=m\\l_i\ge1}}\prod_i a_{l_i}.
$$

Only the first $m-1$ copy decisions change the survival probability. The last decision does matter to the released state. The exact conditional probability that **no** copy occurred, including the last, is $q^m a_m/S_m$. The mean number of moving ticks to a release with retries at recorded failure wells is $2\sum_{j=0}^{m-1}S_j/S_m$ in this character. On a finite deadline, attempts that never produce a packet still consume time. Norm or distribution errors quoted on successful releases use a different denominator.

At zero field on the line $a_j=4^{-j}\binom{2j}{j}$. The same formula applies to the tested prefixes of a finite ring when $2m<4M$. For $0<p<1$ set $B(z)=(1-qz)^{-1/2}-1$. Summing the positive-length segments gives

$$
\sum_{m\ge0}S_m z^m
=1+\frac{B(z)}{q-pB(z)}
=\frac{q}{\sqrt{1-qz}-p}.
$$

In particular $S_1=1/2$, $S_2=(3-p)/8$, and $\sum_{j\ge0}S_j=1+1/\sqrt p$. The simple pole at $z=1+p$ comes before the square-root singularity $1/q$. Its coefficient in the form $(1-z/(1+p))^{-1}$ is $2p/(1+p)$. Removing that pole leaves an analytic function in the open disk of radius $1/q$. Consequently for fixed $0<p<1$,

$$S_m\sim \frac{2p}{1+p}(1+p)^{-m}.$$

For $p=1$, $S_m=2^{-m}$ exactly. For $p=0$, $S_m=a_m$ and the mean is $4m$. These asymptotic statements about arbitrarily large $m$ use the line or rings growing before wraparound. The checker compares the composition sum with a literal two-rail density matrix in two signs of the elementary real character, including the endpoints $p=0,1$. [Independent propagation and rational controls](check_hidden_site_records.py)

## Conditional purity and elapsed time under refinement

Consider the unit sectors of the fixed-action field-on scaling $m\delta^2\to\lambda>0$, $h=\pm F\delta^3$. The ideal comparison gives $a_j(h)\le a_j(0)$ for $j\le m$ and $a_m(h)/a_m(0)\to e^{-F^2\lambda^3/3}>0$. The same hypotheses hold in the shrinking-action regime $m^3h^2\to0$ and for zero field. They permit a uniform bound on the contributions of records containing hidden copies.

Put $A(z)=(1-z)^{-1/2}$. The sum over $k$ segment lengths is at most $[z^m]A(z)^k=\Gamma(m+k/2)/[\Gamma(k/2)\Gamma(m+1)]$. For $2\le k\le m$ the gamma quotient in the numerator divided by $\Gamma(m+1)$ is bounded by $(m+k/2)^{k/2-1}$. One way to see this for half-integers is to peel off the integer factors and use $\Gamma(x+1/2)/\Gamma(x)\le\sqrt x$ by Cauchy–Schwarz. Since $a_m(h)\ge c/\sqrt m$ for large $m$, the sum of all $k\ge2$ terms relative to $q^{m-1}a_m(h)$ is $O(p\sqrt m)$ when $p\sqrt m\to0$. Indeed the term for each $k$ is bounded by a constant times $(C p\sqrt m/q)^{k-1}/\Gamma(k/2)$. Hence

$$
S_m(h,p)=q^{m-1}a_m(h)[1+O(p\sqrt m)],\qquad
\Pr(\text{at least one copy}\mid\text{release in this attempt})=O(p\sqrt m).
$$

The released density matrix contains the ideal state with at least the clean conditional weight. Its trace distance from the ideal is therefore at most the unwanted fraction. Subsequent measurements, including the Gaussian flight, inherit this bound when referred to the latest successful home and correct flight clock. This is a sufficient purity condition. A hidden copy near an endpoint can have a small effect on particular measured probabilities.

For $mp\to\alpha<\infty$, the successful fraction relative to the ideal tends to $e^{-\alpha}$. In finite action put $K=F^2\lambda^3/3$. At relative prefix length $j/m\to x>0$ the survival factor relative to $1/\sqrt{\pi j}$ tends to $\exp(-\alpha x-Kx^3)$. The segment bound is uniform at every $j\le m$ after dividing by $a_j(0)$, and gives $S_j\le C/\sqrt{j+1}$. A Riemann sum in the retry expression yields mean moving time in flight units

$$
2\lambda e^{\alpha+K}\int_0^1 x^{-1/2}e^{-\alpha x-Kx^3}\,dx .
$$

At zero defect it recovers the field-on mean. In contrast take $p=m^{-3/4}$. The conditional copy fraction still tends to zero, while the release probability in one attempt is $O(m^{-1/2}e^{-m^{1/4}})$. Under any polynomial tick deadline the number of attempts that can start is at most polynomial. A union bound over these starts makes the unconditional release probability tend to zero. A flight histogram on the rare successes could therefore converge to its ideal prediction while the apparatus fails its preparation clock on almost every walker.

## The scale $p\sqrt m$ in zero field

At $p\sqrt m\to\theta\ge0$, the ratio of $S_m$ to $q^{m-1}a_m(0)$ has the limiting value

$$
L(\theta)=\sqrt\pi\sum_{k=1}^{\infty}\frac{\theta^{k-1}}{\Gamma(k/2)}
=1+\sqrt\pi\,\theta e^{\theta^2}\operatorname{erfc}(-\theta).
$$

For fixed $k$ the coefficient of $(A-1)^k$ is asymptotic to $m^{k/2-1}/\Gamma(k/2)$, by the binomial formula and the lower powers of $A$. The preceding gamma bound dominates the series when $\theta$ is bounded, so the limit can be taken term by term. Splitting the sum into odd and even powers, or differentiating $e^{x^2}\operatorname{erfc}(-x)$, gives the last expression. The clean conditional fraction tends to $1/L(\theta)$. This crossover is for zero field. At finite action the product of field-dependent survival factors for the segment lengths remains inside the sum.

At $m=1024$ and zero field the full-record calculation gives clean fraction 0.72489 for $p=m^{-3/4}$, with mean time 84.30 times the ideal $4m$ ticks. At $p=1/\sqrt m$ the fraction is 0.10434, compared with the limiting 0.10123. The finite values, including slow approach to the rare-release regime, are retained. [All numerical rows](results/hidden_site_records.json)

## What a detector calibration must establish

On the matched two-output witness with a localized sheet, an independent full site copy gives the two-path marker overlap $\gamma=1-p$. A measured short-word contrast could constrain $p$ if the same instrument applies at each use. A fixed nonzero tolerance on one use does not settle either scaling limit. A detector with memory can reproduce the single-use contrast and have a different survival curve. Comparing joint switch records and timeouts at multiple depths tests that extension. Published measurements of coherence within an atomic parity outcome establish such preservation on that apparatus; they do not supply a per-block copy rate for a cyclic sheet walker. [Localized witness, count nuisance and primary-source comparison](Checking_a_direction_record.md)

## How much can a finite calibration window establish?

Keep the same zero-field switch and site dephasing. Start one sharp walker independently of the detector at a stationary instant. Write $X_i=1$ when the detector would copy the site after pass $i$. For any fixed window width $d\ge1$ and $0<p<1$, there is a stationary ergodic law for these bits that agrees with independent Bernoulli$(p)$ on **every contiguous window of at most $d$ uses**. It nevertheless gives a polynomial lower bound on the chance of $m$ passes, while the independent law above decays exponentially.

Construct the detector from independent intervals. An interval lasts $B$ uses with $\Pr(B\ge b)=2/[b(b+1)]$ for $b\ge1$, so $\mathbb EB=2$. Draw $d$ independent Bernoulli$(p)$ bits and repeat them in order for those $B$ uses. At the boundary, draw both the length and the bits anew. A stationary start selects length $b$ with probability $b\Pr(B=b)/2$ and an offset uniformly among its $b$ positions. Shifting from one regeneration to the next shifts a sequence of independent intervals, so a shift-invariant event has probability zero or one. The length counter is unbounded. Conditional on the boundaries, a window of width at most $d$ encounters distinct bits within each interval and independent draws across intervals. Any control or readout confined to such a window therefore has the same outcome law if its only access to the detector memory is through the copy action and its starting state is independent of that memory.

The chance that $n$ successive uses stay in the starting interval is $\tfrac12\sum_{b\ge n}\Pr(B\ge b)=1/n$. All $d$ bits there are zero with probability $q^d$, independently of its length. Only the first $m-1$ copies affect the trace, so on the line, for $m\ge2$,

$$
S_m^{\rm mem}\ \ge\ \frac{q^d}{m-1}\,a_m
\ =\ \Omega_{p,d}(m^{-3/2}).
$$

The finite-prefix bound also holds before ring wraparound under $2m<4M$. It concerns one launch. A restart triggered by an observed failure can select a different distribution of the retained detector memory.

### The first count that separates the two detectors

Let $W$ denote the probability that all switches pass for a fixed internal copy word. Each copy splits the $m$ switches into segments, and $W$ is the product of their ideal probabilities $a_j$. Thus $S_1$ through $S_{d+1}$ agree. At $m=d+2$ all $d+1$ internal uses occupy one interval with probability $1/(d+1)$. On that event the first and last bits are identical. On its complement every interval contributes at most $d$ distinct bits and the entire word has the independent law. Given the $d-1$ middle bits, write $W_{ij}$ for endpoint choices $i,j$. The increase in survival is
$$
\frac{pq}{d+1}\,\mathbb E\big[W_{00}-W_{01}-W_{10}+W_{11}\big]>0.
$$
With no middle copy the mixed difference is $a_{d+2}-a_{d+1}+a_d/4=a_d(d^2+d+1)/[4(d+1)(d+2)]$. Otherwise the first and last uncut segments have lengths $u,v\ge2$. The difference factors into their two terms $a_j-a_1a_{j-1}$ times the intervening segment probabilities. Both terms are positive since $a_j/a_{j-1}=(2j-1)/(2j)>1/2$.

For $d=2$ and $p=1/3$, the three predictions for four passes in one attempt are as follows.

| Detector law | Probability |
|---|---:|
| Independent copies | $37/216$ |
| Regenerating detector above | $113/648$ |
| Full range over stationary copy laws with independent adjacent pairs | $[1/6,\,13/72]$ |

To see sharpness, condition on the middle bit $X_2=b$. Both endpoint marginals are Bernoulli$(p)$. Write $c_b=\Pr(X_1=X_3=1\mid X_2=b)-p^2$. The marginal constraints allow each $c_b$ anywhere in $[-\min(p^2,q^2),pq]$. Every such pair defines a stationary order-two chain. Use the specified triple law to draw the third bit given the first two, and initialize the first pair independently. Its output pair has the same product law.

The mixed differences for $b=0,1$ are $7/128$ and $1/64$, respectively. Hence $S_4-S_4^{\rm iid}=(7q/128)c_0+(p/64)c_1$, which attains both tabulated endpoints. Even exact agreement with the independent four-pass value can conceal memory. For example, $c_0=1/126$ and $c_1=-1/18$ cancel at $p=1/3$.

### A test with a fixed number of launches

Count all launches, including those that fail at the first switch. At 64 passes the independent probability is about $5.0454\times10^{-9}$. The regenerative lower bound alone is $4.9655\times10^{-4}$ to five significant figures. A prospective test could use 6,100 independent stationary launches at the specified rate and reject independence if any walker completes all 64 passes. The null probability of doing so is at most $6100 S_{64}^{\rm iid}<1/32000$. Under the specified alternative the chance of missing every launch is at most $\exp(-6100q^2a_{64}/63)<e^{-3}<1/20$. This design requires independent stationary initializations or distinct independently prepared detectors. Resetting the counter to the beginning of a new interval would change the prediction. The rates are model calculations.

[Exact stationary windows and two-rail replay](check_hidden_copy_memory.py) · [Numerical record](results/hidden_copy_memory.json) · [Lean checks of the mixed differences](lean/HiddenCopyMemory.lean) · [Instrument-specific memory in quantum processes](https://doi.org/10.1103/PhysRevLett.122.140401)
